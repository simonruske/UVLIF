import os
import numpy as np
from UVLIF.analysis.clustering.cluster_utils import standardise

def load_FT(cfg, data):

  '''
  Function to be depreciated to be replaced with FT mean, std to be loaded from
  the main.proto

  Parameters
  ----------

  cfg['main_directory'] : str
    directory that contains the output and data directories
  '''
  FT_name = check_FT(cfg)
  FT = None

  # try to load in the forced trigger from a forced trigger file (to be depreciated)
  if FT_name:
    FT = np.genfromtxt(FT_name, delimiter=',')

  else:


    raise ValueError("No forced trigger file was found")

  # If the forced trigger file is empty raise error
  if len(FT) == 0:
    raise ValueError("The forced trigger file was empty")
 


  FT = np.array(FT, 'float')
  return FT


def check_FT(cfg):
  '''
  Checks there is an FT.csv file in the output directory and returns
  the location if it exists
  '''
  main_dir = cfg['main_directory']
  output_dir = os.path.join(main_dir, "output")
  if 'FT.csv' in os.listdir(output_dir):
    return os.path.join(output_dir, 'FT.csv')
  else:
    return None

def get_threshold(FT, number_of_std):
  # Gets the threshold from FT
  return np.mean(FT, 0) + float(number_of_std) * np.std(FT, 0)

def remove_nFL(cfg, data, labels):

  '''
  Removes data which doesn't exceed a fluorescent threshold
  '''
  number_of_std = cfg['number_of_std']

  try:
    FT = load_FT(cfg, data)
    threshold = get_threshold(FT, number_of_std)
  
  except ValueError:
    pass

  if 'FT.mean' in cfg and 'FT.std' in cfg:
    threshold = np.array(cfg['FT.mean'], 'float') + float(number_of_std) * np.array(cfg['FT.std'], 'float')

  else:
    raise ValueError('Could not load FT data')




  idx = np.any(data[:, :3] > threshold[:3], 1)
  data = data[idx]
  labels = labels[idx]
  return data, labels

def remove_size(cfg, data, labels):

  '''
  Removes data which does not exceed a size threshold
  '''

  size_threshold = float(cfg['size_threshold'])
  idx = data[:, -2] > size_threshold
  data = data[idx]
  labels = labels[idx]
  return data, labels

def preprocess(cfg, data, labels):

  '''
  Function to preprocess the data before analysis

  Parameters 
  ----------
  '''

  # open a preprocess log file
  g = open(os.path.join(cfg['main_directory'], "output", "preprocess_log.txt"), 'w')

  g.write("Initial number of particles : {}\n".format(len(data)))

  if 'remove_FT' in cfg:
    data, labels = remove_nFL(cfg, data, labels)
    g.write("Particles after removal of non-fluorescent data : {}\n".format(len(data)))

  if 'remove_size' in cfg:
    data, labels = remove_size(cfg, data, labels)
    g.write("Particles after removal of particles under size threshold : {}\n".format(len(data)))


  # check that there are no negative values for size and AF
  
  idx = np.all(data[:, -2:] > 0, 1)
  data = data[idx]
  labels = labels[idx]

  # take logs of last two cols
  if 'take_logs' in cfg and cfg['take_logs'] == True:
    data[:, -2:] = np.log(data[:, -2:])

  # standardise the data
  if 'standardise_method' in cfg:
    data = standardise(data, cfg['standardise_method'])

  return data, labels


