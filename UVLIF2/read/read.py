from collections import Counter
from UVLIF2.utils.filelist import load_filelist, create_filelist_ambient
from UVLIF2.utils.files import load_file
from UVLIF2.utils.directories import list_directory
import numpy as np

def prepare_laboratory(cfg, input_directory, output_directory, filename):

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

  return files, labels, forced, g, l

def prepare_ambient(cfg, input_directory, output_directory):

  g = load_file(cfg, output_directory, 'data.csv', 'w')
  forced = load_file(cfg, output_directory, 'FT.csv', 'w')
  time_handle = load_file(cfg, output_directory, 'times.csv', 'w')

  # If time stamp is specified then create list in date order
  if cfg['time_stamp_specified']:
    dates, files = create_filelist_ambient(cfg, input_directory, output_directory)

  else:
    files = list_directory(cfg, directory)

  return files, forced, g, time_handle

