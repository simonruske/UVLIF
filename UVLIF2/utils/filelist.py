from UVLIF2.utils.files import load_file, get_date
from UVLIF2.utils.directories import list_files
from datetime import datetime, timedelta

import os
import numpy as np

def create_filelist_laboratory(cfg, input_directory, output_directory):

  '''
  Function used to create a file list file which lists the contents of
  the input directory specified. The file list is saved in the output directory.
  
  Parameters 
  ----------
  cfg['main_directory'] : str
    The main directory that contains the input and output directory

  input_directory : str
    The directory to be listed and stored in the filelist

  output_directory : str 
    The directory where the filelist will be stored


  '''
  if 'instrument' in cfg:
    if cfg['instrument'] == 'NEO':
      return create_filelist_NEO(cfg, input_directory, output_directory)
    elif cfg['instrument'] == 'PLAIR':
      return create_filelist_PLAIR(cfg, input_directory, output_directory)


  f = load_file(cfg, output_directory, 'filelist.csv', 'w')
  for filename in list_files(cfg, input_directory):
    f.write(filename + '\n')
  f.close()

def create_filelist_PLAIR(cfg, input_directory, output_directory):

  f = load_file(cfg, output_directory, 'filelist.csv', 'w')
  f.write('Time Format : %Y/%m/%d %H/%M/%S\n')
  f.write('Description, Start Time, End Time, Label\n')
  f.close()
  

def create_filelist_ambient(cfg, input_directory, output_directory):

  '''
  Function used to create a filelist in the output directory that creates a filelist listing 
  the contents of the input directory in order of date.

  Parameters 
  ----------
  input_directory : str
    The directory that contains the input and the output directory

  output_directory : str 
   The directory where the filelist will be stored  
  '''


  files = list_files(cfg, input_directory)

  dates = []
  filelist = []

  for filename in files:
    f = load_file(cfg, input_directory, filename, 'r')
    dates.append(get_date(cfg, f))
    filelist.append(filename)
    f.close()

  return sort_filelist(dates, filelist)

def sort_filelist(dates, files):

  '''
  Function that sorts a list of dates
  '''
  idx = np.argsort(dates)
  dates = np.array(dates)[idx]
  files = np.array(files)[idx]

  return dates, files

def create_filelist_NEO(cfg, input_directory, output_directory):

  # creat the filelist
  f = load_file(cfg, output_directory, 'filelist.csv', 'w')

  # Loop through the days
  for day_directory in os.listdir(input_directory):

    # loop through the directories for each day
    for item in os.listdir(os.path.join(input_directory, day_directory)):
      if os.path.isdir(os.path.join(input_directory, day_directory, item)):

        # for each files in the directory
        for filename in os.listdir(os.path.join(input_directory, day_directory, item)):

          if filename == 'Notes.txt':
            g = open(os.path.join(input_directory, day_directory, item, 'Notes.txt'))
            description = g.readline().strip('\n')
            if description != '':
              f.write(day_directory + " " + item + " : " + description +'\n')

def search_file_PLAIR(cfg, date):

  main_dir = cfg['main_directory']
  data_dir = os.path.join(main_dir, 'data')

  for C_directory in os.listdir(data_dir):
    C_directory = os.path.join(data_dir, C_directory)
    for C_file in os.listdir(C_directory):
      date_str = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
      date_str += str(date.hour).zfill(2) + str(date.minute).zfill(2)
      
      if date_str in C_file:
        return os.path.join(main_dir, data_dir, C_directory, C_file)


  return None



def load_filelist_PLAIR(cfg, directory, filename):

  f = load_file(cfg, directory, filename, 'r')


  # get the time format
  time_format = f.readline().strip('\n').strip(',').strip('Time Format : ')

  # skip the header
  f.readline()

  # read the rest
  files = []
  labels = []

  for line in f:
    description, start, end, label = line.strip('\n').split(',')
    start = datetime.strptime(start, time_format)
    end = datetime.strptime(end, time_format)

    # loop through dates
    cur_date = start
    while cur_date < end:
      cur_date += timedelta(minutes = 1)
      filename = search_file_PLAIR(cfg, cur_date)
      if filename != None:
        files.append(filename)
        labels.append(label)

  return files, labels


    
  
  


           
def load_filelist(cfg, directory, filename):

  '''
  Function that loads a filelist created using the create_filelist_laboratory function

  Parameters
  ----------
  directory : str 
    The directory in which the filelist is stored

  filename : str
    The name of the filelist file
  '''

  #TODO THIS SHOULD BE PUT IN A FUNCTION!!
  filelist_filename = os.path.join(cfg['main_directory'], directory, filename)
  if not os.path.isfile(filelist_filename):
    raise ValueError("The filelist could not be found")

  if 'instrument' in cfg and cfg['instrument'] == 'PLAIR':
    return load_filelist_PLAIR(cfg, directory, filename)
    

  f = load_file(cfg, directory, filename, 'r')
  files = []
  labels = []
 
  # main loop
  for line in f:
    try: 
      file, label = line.strip('\n').split(',')
    except ValueError:
      raise ValueError("Unable to read file list, check the labels are "
                       "filled in correctly")

    if label.strip() != '0':
      files.append(file)
      labels.append(label.strip())

  # Check the lists are not of length '0'
  if len(files) == 0 or len(labels) == 0:
    raise IOError("There are no files or labels to be read.")

  f.close()
  return files, labels
