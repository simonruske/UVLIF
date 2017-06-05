import os

''' 
Functions to manage the data and output directories
'''


def directory_exists(cfg, directory):

  '''
  Function that checks a particular directory exists
  
  Parameters 
  ----------
  cfg['main_direcory'] (str):
    The main directory that should contain the data and output directories

  directory (str):
    The directory to look for e.g. output
  ''' 

  full_directory = os.path.join(cfg['main_directory'], directory)

  if os.path.exists(full_directory):
    return True

  else:
    return False

def create_directory(cfg, directory):

  '''
  Function that creates a directory if it doesn't already exist

  Parameters 
  ----------
  cfg['main_directory'] (str):
    The main directory that should contain the data and ouput directories

  directory (str):
    The directory to create

  '''

  if not directory_exists(cfg, directory):
    full_directory = os.path.join(cfg['main_directory'], directory)
    os.mkdir(full_directory)

def list_directory(cfg, directory):

  '''
  Function that lists the contents of a directory

  Parameters 
  ----------
  cfg['main_directory'] (str)
    The main directory that should contain the data and output directories

  directory (str):
    The directory to list
  '''

  return os.listdir(os.path.join(cfg['main_directory'], directory))

def list_files(cfg, directory):

  '''
  Function that returns an iterator of the files in a directory

  Parameters 
  ----------
  cfg['main_directory'] (str):
    The main directory that should contain the data and output directories

  directory (str):
    The directory to list the files
  '''

  for file in os.listdir(os.path.join(cfg['main_directory'], directory)):
    if os.path.isfile(os.path.join(cfg['main_directory'], directory, file)):
      yield file


