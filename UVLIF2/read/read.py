from collections import Counter
from UVLIF2.utils.filelist import load_filelist, create_filelist_ambient
from UVLIF2.utils.files import load_file
from UVLIF2.utils.directories import list_directory
import numpy as np
from datetime import datetime


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

  forced, g, l = None, None, None

  files, labels = load_filelist(cfg, input_directory, filename)

  file_types = Counter(labels)

  # If we have forced trigger files then create FT.csv
  if 'F' in file_types:
    forced = load_file(cfg, output_directory, "FT.csv", 'w')

  # If we have at least one file that isn't forced trigger file create data
  # and labels
  if sum(np.unique(labels) != 'F') != 0:
    g = load_file(cfg, output_directory, "data.csv", 'w')
    l = load_file(cfg, output_directory, "labels.csv", 'w')

  return zip(files, labels), forced, g, l

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
    earliest_date = datetime.min
    latest_date = datetime.max

  else:
    file_info = list_directory(cfg, directory)

  return file_info, forced, g, time_handle, earliest_date, latest_date

def convert_info(cfg, info):

  '''
  Function that splits info into file and label in the laboratory case and into just 
  file in the ambient case. In the ambient case we also check if the file is FT as 
  it we do not have labels for each file.
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
  '''

  for handle in handles:
    if handle != None:
      handle.close()

def write_start_end_date(cfg, output_directory, earliest_date, latest_date):

  # NEEDS TEST

  '''
  Function that writes the start and end date to file
  '''
  start_end_handle = load_file(cfg, output_directory, 'startend.csv', 'w')
  start_end_handle.write('Earliest_date, ' + str(earliest_date) + '\n')
  start_end_handle.write('Latest_date, ' + str(latest_date) + '\n')
  start_end_handle.close()


def read_file(cfg):

  # NEEDS TEST

  return

def read_files(cfg):

  # NEEDS TEST

  # If any data files exist write message suggesting deletion if user wishes to recreate them
  if any_file_exists(cfg, 'output_directory', ['data.csv', 'FT.csv', 'times.csv']):
    print("Data files have been found in the output directory, hence creation of the "
          "data files has been skipped, if you wish to recreate them please run "
          "'python UVLIF.py clean_data' before running again\n")
    return

  # if in ambient mode then prepare ambient otherwise prepare for laboratory
  if cfg['ambient']:
    file_info, forced, g, time_handle, earliest_date, latest_date = prepare_ambient(cfg, 'data', 'output')

  else:
    file_info, forced, g, l = prepare_laboratory(cfg, 'data', 'output', 'filelist.csv')

  # =========================
  # MAIN LOOP : Read in files
  # =========================
  particle = 0
  for file_num, info in enumerate(file_info):
    read_file(cfg)

  # Save the earliest and latest date
  if cfg['ambient'] and cfg['time_stamp_specified']:
    write_start_end_date(cfg, 'output', earliest_date, latest_date)

  close_files([g, l, forced])




  
  


