import os
import warnings
from datetime import datetime

def check(cfg):

  # check that the main directory exists
  if not os.path.exists(cfg['main_directory']):
    raise IOError("Missing main directory {}".format(cfg['main_directory']))

  # check that data and output directories exist
  if not os.path.exists(os.path.join(cfg['main_directory'], "data")):
    raise IOError("Missing data directory in {}, please create one in the project folder and then"
                   "put your data in it".format(cfg['main_directory']))

  if not os.path.exists(os.path.join(cfg['main_directory'], "output")):
    os.mkdir(os.path.join(cfg['main_directory'], "output"))

def load_file(cfg, directory, filename, mode):

  '''
  Function used to load a file from a directory

  Parameters 
  ----------
  cfg['main_directory'] (str):
    main directory containing for example output and data directories    

  directory : str 
    directory from which the file will be read from 

  filename : str
    The name of the file to be read

  mode : str
    'r' for read mode, 'w' for write mode

  Returns
  -------
  f : file
    object for the file that can be looped over
  '''

  full_filename = os.path.join(cfg['main_directory'], directory, filename)
  f = open(full_filename, mode)
  print(f)
  return f

def search_for_line(f, search_term, limit):

  '''
  Function that searches for a particular line in a file

  Parameters 
  ----------
  limit : int 
    The maximum number of lines to search before giving up

  search_term : str 
    The term at the start of the line to search for

  Returns 
  -------
  line : str
    The line starting with the search term

  '''

  for i in range(limit):
    line = f.readline()
    if line[:len(search_term)] == search_term:
      break

  else:
    raise ValueError("Could not find {} in the file".format(search_term))

  return line.strip('\n')

def str2date(cfg, string, strip):

  '''
  Function that converts a string into a 
  date time object
  
  Parameters 
  ----------
  cfg : dict
    dictionary of configuration, here we use it to specify the date format

  string : str 
    string to be converted to date time object

  strip : str
    text to be stripped from string

  Returns 
  -------
  date : DateTime object
    converted line

  '''
  date_format = cfg['date_format']
  date = string.strip(strip).strip('\n').strip(',').replace(' ', '')

  # The length of the date may be 18, 17 or 16 characters, try each
  for i in [18, 17, 16]:
    try:  
      date_output = datetime.strptime(date[:i], date_format)
      break
      
    except Exception:
      continue
  else:
    raise ValueError("Could not recognise date")

  return date_output
  

def get_date(cfg, f):

  '''
  Function that gets the date from a particular file 

  Parameters 
  ----------
  f : file
    The file to be read

  Returns
  -------
  start : datetime object:
    The start date/time from the file

  '''

  line = search_for_line(f, "Start Date/Time", 100)
  start = str2date(cfg, line, "Start Date/Time : ")
  return start

def file_exists(cfg, directory, filename):

  '''
  Function that checks if a file exists in a particular directory

  Parameters 
  ----------
  cfg['main_directory'] (str):
    The main directory which contains the directory to be searched

  directory (str) : 
    The directory to search for the file in 

  filename (str) : 
    The name of the file to search for
  '''

  if os.path.exists(os.path.join(cfg['main_directory'], directory, filename)):
    return True

  else:
    return False

def any_file_exists(cfg, directory, filelist):
  
  '''
  Function that checks whether any file within a list exists

  Parameters 
  ----------
  cfg['main_directory'] (str):
    The main directory that stores all the folders

  directory (str) : 
    The directory within the main directory to search

  filelist (list) :
    A list of files to search for
  '''

  data_exists = False

  for filename in filelist:
    if file_exists(cfg, directory, filename):
      data_exists = True

  return data_exists
