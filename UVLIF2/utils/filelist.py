from UVLIF2.utils.files import load_file, get_date
from UVLIF2.utils.directories import list_files
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

  f = load_file(cfg, output_directory, 'filelist.csv', 'w')
  for filename in list_files(cfg, input_directory):
    f.write(filename + '\n')
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
    dates.append(get_date(f))
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
