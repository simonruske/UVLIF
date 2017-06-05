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

def sort_filelist(dates, files):

  '''
  Function that sorts a list of dates
  '''
  idx = np.argsort(dates)
  dates = np.array(dates)[idx]
  files = np.array(files)[idx]

  return dates, files

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
