import os
import numpy as np

def load_FT(cfg, data):

  '''
  Parameters
  ----------

  cfg['main_directory'] : str
    directory that contains the output and data directories
  '''
  FT_name = check_FT(cfg)
  FT = None
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
  FT = load_FT(cfg, data)
  threshold = get_threshold(FT, number_of_std)
  idx = np.any(data[:, :3] > threshold[:3], 1)
  data = data[idx]
  labels = labels[idx]
  return data, labels

def remove_size(cfg, data, labels):

  '''
  Removes data which does not exceed a size threshold
  '''

  size_threshold = float(cfg['size_threshold'])
  idx = data[:, 4] > size_threshold
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
  return data, labels


