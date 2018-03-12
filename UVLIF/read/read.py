from collections import Counter
from UVLIF.utils.filelist import load_filelist, create_filelist_ambient
from UVLIF.utils.files import load_file, get_date, search_for_line, any_file_exists, check
from UVLIF.utils.directories import list_directory
from UVLIF.read.read_NEO import read_NEO
from UVLIF.read.read_PLAIR import read_PLAIR

import numpy as np
from datetime import datetime, timedelta
import warnings
import os
import shutil
from copy import copy
import sys

def read_FT(cfg, filenames):

  # function used to read a forced trigger file
  FT = []
  for filename in filenames:
    f = open(filename)
    if cfg['time_stamp_specified']:
      start = get_date(cfg, f)
    header = f.readline()
    for line in f:
      FT.append(line.strip('\n').split(cfg['delimiter']))

  FT = np.array(FT, 'float')

  if 'FL_cols' in cfg.keys():
    idx = cfg['FL_cols']
  else:
    raise ValueError("Could not find the indices of the columns for the fluorescent channels in the instrument configuration file.")

  FT = FT[:, idx]

  minimum = np.min(FT, 0)
  mean = np.mean(FT, 0)
  std = np.std(FT, 0)
  maximum = np.max(FT, 0)

  return minimum, mean, std, maximum


def prepare_laboratory(cfg, input_directory, output_directory, filename):

  '''
  Function used to make preparations for analysis of laboratory data

  Parameters 
  ----------
  cfg : dict
    Configuration dictionary 

  input_directory : str 
    The directory containing the data files 
 
  output_directory : str 
    The directory to store the output files 

  filename : str
    The filename of the filelist
  '''

  forced, g, l, file_l = None, None, None, None

  files, labels = load_filelist(cfg, output_directory, filename)

  file_types = Counter(labels)

  # If we have forced trigger files then create FT.csv
  if 'F' in file_types:
    forced = load_file(cfg, output_directory, "FT.csv", 'w')

  # If we have at least one file that isn't forced trigger file create data
  # and labels
  if sum(np.unique(labels) != 'F') != 0:
    g = load_file(cfg, output_directory, "data.csv", 'w')
    l = load_file(cfg, output_directory, "labels.csv", 'w')
    file_l = load_file(cfg, output_directory, "file_labels.csv", 'w')

  cfg['number_of_files'] = len(files) 

  return zip(files, labels), forced, g, l, file_l

def prepare_ambient(cfg, input_directory, output_directory):

  '''
  Function used to make preparations for analysis of ambient data 

  Parameters 
  ----------
  cfg : dict 
    Configuration dictionary

  input_directory : str
    The directory containing the data files

  output_directory : str
    The directory to store the output files
  '''

  forced, g, l = None, None, None
  g = load_file(cfg, output_directory, 'data.csv', 'w')
  forced = load_file(cfg, output_directory, 'FT.csv', 'w')
  time_handle = load_file(cfg, output_directory, 'times.csv', 'w')

  # If time stamp is specified then create list in date order
  if cfg['time_stamp_specified']:

    dates, file_info = create_filelist_ambient(cfg, input_directory, output_directory)

    # get the earliest and latest time 
    cfg['earliest_date'] = datetime.min
    cfg['latest_date'] = datetime.max

  else:
    file_info = list_directory(cfg, directory)

  cfg['number_of_files'] = len(file_info)

  return file_info, forced, g, time_handle

def convert_info(cfg, info):

  '''
  Function that splits info into file and label in the laboratory case and into just 
  file in the ambient case. In the ambient case we also check if the file is FT as 
  it we do not have labels for each file.

  Parameters
  ----------
  cfg['ambient'] : bool
    Specifies whether the package is in ambient or laboratory mode

  cfg['FT_char'] : str
    The characters that must be contained within the filename for the file to be 
    forced trigger

  info : zip or files
    This will either be a zip of the files and labels if in laboratory mode, 
    or just the files in ambient mode
  '''

  if cfg['ambient']:
    file = info
    is_FT = False
    if cfg['FT_char'].lower() in file.lower():
      is_FT = True
    return file, is_FT

  else:
    file, label = info
    return file, label

def close_files(handles):

  '''
  Closes all the files which are open

  Parameters 
  ----------
  handles : list 
    A list of file handles to be closed
  '''

  for handle in handles:
    if handle != None:
      handle.close()

def write_start_end_date(cfg, output_directory):

  '''
  Function that writes the start and end date to file

  Parameters 
  ----------
  output_directory : str
    Directory within the main directory where the output files should be saved

  cfg['earliest_date'] : str 
    The earliest date from the analysis 

  cfg['latest_date'] : str 
    The latest date from the analysis

  '''
  start_end_handle = load_file(cfg, output_directory, 'startend.csv', 'w')
  start_end_handle.write('Earliest_date, ' + str(cfg['earliest_date']) + '\n')
  start_end_handle.write('Latest_date, ' + str(cfg['latest_date']) + '\n')
  start_end_handle.close()

def line2list(cfg, line):

  '''
  Converts a line from the file to a list, removing the columns which are not required

  Parameters 
  ----------

  cfg['delimiter'] : str 
    The delimiter used to separate the columns 

  cfg['needed_cols'] : list
    A list of all of the columns which are a needed

  Returns 
  -------
  output_list : str
    A list containing the data from the required columns only

  '''
  line = line.strip('\n').split(cfg['delimiter'])
  output_list = []

  for i in cfg['needed_cols']:
    output_list.append(line[i])

  return output_list

def line2list_FT(cfg, line):

  '''
  Does the same as line2list but also outputs the FT number for the particle

  Parameters 
  ----------
  see line2list

  Returns
  -------
  output_list:
    see line2list

  FT : int
    A number to identify whether or not the particle is FT (instrument dependent)
  '''

  line = line.strip('\n').split(cfg['delimiter'])
  output_list = []
  for i in cfg['needed_cols']:
    output_list.append(line[i])
  FT = int(float(line[cfg['FT_idx']]))

  return output_list, FT
   


def check_output_list(output_list):

  '''
  Checks that the output list can be converted to float, 
  this is to handle errors should a file be corrupted

  Parameters 
  ----------
  output_list : str 
    An output list from line2str

  Returns
  -------
  output_float : bool
    True if the output_list can be converted to float, False otherwise
  '''

  output_float = True
  for output in output_list:
    try:
      float(output)
    except Exception:
      output_float = False

  return output_float

def output_list2str(output_list):

  '''
  Function that converts the output list back to string
  so that it can be saved to file
  
  Parameters 
  ----------
  output_list : list
    A list of floating point numbers to be converted to a 
    comma delimitted string
  '''

  output_str = ','.join(output_list) + '\n'
  return output_str

def write_line_laboratory(g, l, file_l, forced, output_str, label, file_label):

  '''
  Write a particular line to file if in laboratory mode.

  Parameters 
  ----------
  g : file handle
    The file handle for the data output file 

  l : file_handle
    The file handle for the labels

  forced : file_handle
    The file handle for the forced trigger file

  output_str : str
    The string to be saved to file

  label : str 
    The label for the file
  '''

  # check if the file is forced trigger from label
  if label == 'F':
    forced.write(output_str)

  else:
    g.write(output_str)
    l.write(label + '\n')
    file_l.write(str(file_label) + '\n')

def write_line_ambient(g, forced, output_str, is_FT, cur_time = None, time_handle = None):

  '''
  Writes a line to file if in ambient mode.

  Parameters 
  ----------
  g : handle
    The handle for the data file 

  forced : handle
    The handle for the forced trigger file

  output_str : str 
    String of the line to be saved to file

  is_FT : bool
    True if file is FT

  time_handle : handle
    The handle for the time file



  cur_time : datetime object
    The current time for the particle to be written to file
  '''

  if is_FT:
    forced.write(output_str)

  else:
    g.write(output_str)

  if time_handle and not is_FT:
    time_handle.write(str(cur_time) + "\n")

def convert_line(cfg, line):

  '''
  Function that calls either line2list_FT or line2list
  depending on whether the FT column index is specified 
  in the instrument configuration. If the FT_idx is 
  specified any line which is FT 
  '''  

  # If FT column specified get the info from it
  if 'FT_idx' in cfg:
    output_list, FT = line2list_FT(cfg, line)
    cfg['FT'] = FT
    update_FT(cfg)

    # if column is forced trigger return -1
    if FT == 1:
      cfg['cur_FT_data'].append(output_list)
      return -1
    else:
      return output_list

  else:
    output_list = line2list(cfg, line)
    return output_list

def reset_threshold(cfg):
  cfg['cur_FT_data'] = []

def average_FT(cfg):
  cur_FT = np.array(cfg['cur_FT_data'], 'float')
  cfg['cur_FT_mean'] = np.mean(cur_FT, 0)
  cfg['cur_FT_std'] = np.std(cur_FT, 0)


def update_FT(cfg):

    # Check if the instrument files are written in blocks
    if cfg['FT_blocks'] == True and cfg['FT'] != cfg['FT_prev']:
      if cfg['FT'] == 1:
        reset_threshold(cfg)
      else:
        average_FT(cfg)

    if 'FT_idx' in cfg:
      cfg['FT_prev'] = copy(cfg['FT'])

def readd_background(cfg, output_list):
  output_array = np.array(output_list, float)
  output_array[:1024] = output_array[:1024] + np.floor(cfg['cur_FT_mean'][:1024])
  output_list = list(np.array(output_array, 'str'))

  return output_list

def read_file(cfg, info, g, forced, file_label = None, file_l = None, l = None, time_handle = None):

  # Needs documentation

  if 'instrument' in cfg:
    if cfg['instrument'] == 'NEO':
      return read_NEO(cfg, info, g, l)

    elif cfg['instrument'] == 'PLAIR':

      # create a temp directory in the main directory
      if os.path.exists(os.path.join(cfg['main_directory'], "temp")):
        shutil.rmtree(os.path.join(cfg['main_directory'], "temp"))
      os.mkdir(os.path.join(cfg['main_directory'], "temp"))

      read_PLAIR(cfg, info, g, l)

      # remove the temp directory when finished
      shutil.rmtree(os.path.join(cfg['main_directory'], "temp"))

      return


  # convert information
  if cfg['ambient']:
    file, is_FT = convert_info(cfg, info)


  else:
    file, label = convert_info(cfg, info)


  if 'progress_labels' in cfg:
    cfg['progress_labels'].emit(str(file))
  else:
    print(file)

  # skip file if extension not in valid_ext
  if os.path.splitext(file)[1] not in cfg['valid_ext']:
    return

  
  # open file
  f = load_file(cfg, "data", file, 'r')

  # search for line containing filename
  if cfg['file_name_specified']:
    try:
      filename = search_for_line(f, "Filename:", 100)
    except ValueError():
      warnings.warn("We could not find a filename in {} so we move onto"\
                    "the next file.".format(file))
      return

  # Search for a time stamp

  if cfg['time_stamp_specified']:
    start = get_date(cfg, f)
    if cfg['ambient'] and not is_FT:
      cfg['earliest_date'] = min(start, cfg['earliest_date'])

  header = f.readline()



  for j, line in enumerate(f):

    #convert line
    try:
      output_list = convert_line(cfg, line)

      if output_list == -1:
        continue

    except IndexError:
      warning = "There was a particle on line {} of file {} that had missing data "\
                "so was skipped"
      warnings.warn(warning.format(j, file), RuntimeWarning)
      continue

    # Get current time
    if cfg['time_stamp_specified']:
      cur_time = start + timedelta(milliseconds = int(line[0]))


    # check the output_list can be converted to floating point
    output_float = check_output_list(output_list)

    # If we are using the MBS we need to add the background back in (especially for 
    # supervised analysis)
    if 'readd_background' in cfg and cfg['readd_background'] == True:
      output_list = readd_background(cfg, output_list)

    # remove particles that are too small
    if 'size_threshold' in cfg and float(output_list[-1]) < cfg['size_threshold']:
      continue
      

    # If we cannot convert the output to float then warn user and move onto the next line
    if not output_float:
      warnings.warn("We found a particle on line {} in {} that had measurements that could"\
                  "not be converted to float. We have skipped this line, {}.".format(j, file))
      continue

    # Otherwise convert list to string
    else:
      output_str = output_list2str(output_list)

    # Write the line
    if not cfg['ambient']:

      write_line_laboratory(g, l, file_l, forced, output_str, label, file_label)

    elif cfg['ambient'] and cfg['time_stamp_specified']:
      write_line_ambient(g, forced, output_str, is_FT, cur_time = cur_time, time_handle = time_handle)

    else:
      write_line_ambient(g, forced, output_str, is_FT)
  
  



  f.close()




def read_files(cfg):

  # If any data files exist write message suggesting deletion if user wishes to recreate them
  if any_file_exists(cfg, 'output', ['data.csv', 'FT.csv', 'times.csv']):
    print("Data files have been found in the output directory, hence creation of the "
          "data files has been skipped, if you wish to recreate them please run "
          "'python UVLIF.py clean data' before running again\n")
    return

  check(cfg)

  # if in ambient mode then prepare ambient otherwise prepare for laboratory
  if cfg['ambient']:
    file_info, forced, g, time_handle = prepare_ambient(cfg, 'data', 'output')

  else:
    file_info, forced, g, l, file_l = prepare_laboratory(cfg, 'data', 'output', 'filelist.csv')

  # =========================
  # MAIN LOOP : Read in files
  # =========================

  particle = 0
  cfg['FT_prev'] = None
  cfg['FT'] = None
  cfg['cur_FT_data'] = []

  # in in gui mode then set the range of the progress bar
  if 'progress_bar' in cfg:
    cfg['progress_bar'].setRange(0, cfg['number_of_files']-1)  

  for file_num, info in enumerate(file_info):
    

    if 'progress' in cfg and file_num :
      cfg['progress'].emit(file_num)


    if cfg['ambient']:
      read_file(cfg, info, g, forced, time_handle = time_handle)
    else:
      read_file(cfg, info, g, forced, l = l, file_label = file_num, file_l = file_l)
    

  # Save the earliest and latest date
  if cfg['ambient'] and cfg['time_stamp_specified']:
    write_start_end_date(cfg, 'output')
    time_handle.close()

  if cfg['ambient']:
    close_files([g, forced])

