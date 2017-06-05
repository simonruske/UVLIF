import os
import warnings
from datetime import datetime

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

def str2date(string, strip):

  '''
  Function that converts a string into a 
  date time object
  
  Parameters 
  ----------
  string : str 
    string to be converted to date time object

  strip : str
    text to be stripped from string

  Returns 
  -------
  date : DateTime object
    converted line

  '''

  date = string.strip(strip).strip('\n')
  date = datetime.strptime(date[:19], "%d/%m/%Y %H:%M:%S")
  return date
  

def get_date(f):

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
  start = str2date(line, "Start Date/Time : ")
  return start
