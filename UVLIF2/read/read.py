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




