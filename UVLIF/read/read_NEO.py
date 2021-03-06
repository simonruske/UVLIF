import os
import h5py
import numpy as np
import logging
from UVLIF.utils.filelist import load_filelist_NEO

def read_FT_NEO(cfg):
  '''
  Function that loads forced trigger data from the
  main directory specified
  '''
  logging.basicConfig(filename=cfg['log_filename'],level=logging.DEBUG)
  logging.info("Loading forced trigger files from directory")
  FT_files = find_FT_files(cfg)
  FT = load_FT_files(FT_files)
  
  return FT_files, FT
  
def load_FT_files(FT_files):
  '''
  Loads a list of forced trigger files
  '''
  
  FT = []
  
  logging.info("Loading in forced trigger files")
  for filename in FT_files:
    FT.append(load_FT_file(filename))
    
  # stack FT array
  FT = np.vstack(FT)

  return FT

def load_FT_file(filename):
  logging.info("Loading forced trigger file {}".format(filename))
  f = h5py.File(filename) # load file
  N = len(f['NEO']['ParticleData']['Xe1_FluorPeak']) # number of particles in file
  cur_X = np.zeros((N, 3)) # empty array
  
  # load in FL data only
  cur_X[:, 0] = f['NEO']['ParticleData']['Xe1_FluorPeak'][:, 1]
  cur_X[:, 1:] = f['NEO']['ParticleData']['Xe2_FluorPeak']
  
  return cur_X

  
def find_FT_files(cfg):
  '''
  Loops through main directory searching for FT files
  '''
  logging.info("Searching directory for forced trigger files")
  
  FT_files = []
  # loop through directory looking for folders called FT
  for dirpath, dirnames, filenames in os.walk(cfg['main_directory']):
    dirpath = os.path.join(dirpath) # fix slashes
    if os.path.split(dirpath)[-1] == 'FT': # if folder is called FT
      FT_files += [os.path.join(dirpath, filename) for filename in filenames] # append files to list
  return FT_files
      
  
def split_info(info):

  '''
  Function that splits the information on a file into 
  the date, the description and the label

  Parameters 
  ----------
  info : str 
    The information about the file 

  Returns 
  -------
  date : str
    The date for the file in YYYYMMDD format

  folder : str
    The folder within the date directory

  description : str
    The description of the file from the first line of the Notes.txt file
  
  '''

  location, description = info[0].strip('\n').split(" : ")
  date, folder = location.split(' ')
  

  return date, folder, description, info[1]

def list_files(cfg, date, folder, description):

  '''
  Function that lists the files in the same directory as the Notes.txt
  file that matches the description.

  Parameters
  ----------
  cfg['main_directory'] : str
    The main directory containing the data and output folders

  date : str
    The date for the file in YYYYMMDD format

  folder : str
    The folder within the date directory

  description : str
    Description of the file

    
  '''

  main_dir = cfg['main_directory']
  data_dir = os.path.join(main_dir, "data")
  
  files = []

  for filename in os.listdir(os.path.join(data_dir, date, folder)):
    filename = os.path.join(data_dir, date, folder, filename)
    if os.path.splitext(filename)[1] == '.h5':
      files.append(filename)

  return(files)
  
def read_NEO_new(cfg):
 
  # get the output directory which should contain the filelist
  output_directory = os.path.join(cfg['main_directory'], "output")
  
  # check the output directory exists
  if not os.path.isdir(output_directory):
    logging.info("Could not find the output directory when loading the filelist for the NEO"
                 "notifying the user")
    raise ValueError("The output directory could not be found")
    
    
  # load in the filelist
  files, labels = load_filelist_NEO(cfg, output_directory, "filelist.csv")
  
  data_list = [] # each item will be an array of each file
  label_list = []

  for file, label in zip(files, labels): # load in every file
    logging.info("Reading {}".format(file))
    try:
      X, y = read_NEO_file_new(cfg, file, label)
    
    except ValueError:
      logging.info("There was a problem in loading {}".format(file))
      continue 
    

    if len(X) == 0:
      continue
    data_list.append(X)
    label_list.append(y)
    
  # stack the data and labels into a single array
  data = np.vstack(data_list)
  labels = np.concatenate(label_list)
  
  

  # remove infinity or nans (consider moving this to preprocessing function
  logging.info("Removing nans and infinities")
  idx = ~np.isnan(data).any(axis = 1)
  data = data[idx]
  labels = labels[idx]
  idx = ~np.isinf(data).any(axis = 1)
  data = data[idx]
  labels = labels[idx]
  return data, labels
  
def read_NEO_file_new(cfg, file, label):
  f = h5py.File(file, 'r')
  
  # check the file is not empty
  N = number_of_particles(f)

  if N == 0:
    logging.info("Empty file")
    return [], []
    
    
  cur_X = np.zeros((N, 5)) # preallocate array 
  load_data(cur_X, f) # load in the data
  y = [label] * N # create a list of labels

  return cur_X, y  
  
def read_NEO_file(cfg, filename, X, y, label):
  f = h5py.File(filename)
  if len(f['NEO']['ParticleData']['Size_um']) == 0:
    print('Empty file : {}'.format(filename))
    return -1
  N = number_of_particles(f)
  cur_X = np.zeros((N, 5))
  load_data(cur_X, f)
  X.append(cur_X)
  y += [label] * len(cur_X)
  return 0
  

def read_NEO(cfg, info, g, l):

  logging.basicConfig(filename=cfg['log_filename'],level=logging.DEBUG)
  filename, label = info[0], info[1]

  # split the info into date and description
  logging.info("Attempting to read {}".format(filename))
  try:
    X = []
    y = []  
    flag = read_NEO_file(cfg, filename, X, y, label)


    logging.info("Finished reading files, saving")
    g = open(os.path.join(cfg['main_directory'], "output", "data.csv"), 'a')
    l = open(os.path.join(cfg['main_directory'], "output", "labels.csv"), 'a')
    X = np.vstack(X)
    y = np.array(y, 'float')
    np.savetxt(g, X, delimiter=',')
    np.savetxt(l, y, delimiter=',')
  except ValueError:
    print("Skipping {}, {}, {}".format(date, folder, description))

    
def check_file(f):
  if 'NEO' not in f.keys():
    raise ValueError("Could not find NEO data in file")
    
def number_of_particles(f):
  check_file(f)
    

  total = 0
  for line in f['NEO']['ParticleData']['Size_um']:
    total += 1
  return total

def load_data(cur_X, f):
  cur_X[:, 0] = f['NEO']['ParticleData']['Size_um']
  cur_X[:, 1] = f['NEO']['ParticleData']['Asphericity']
  cur_X[:, 2] = f['NEO']['ParticleData']['Xe1_FluorPeak'][:, 1]
  cur_X[:, 3:] = f['NEO']['ParticleData']['Xe2_FluorPeak']

def read_NEO_file(cfg, filename, X, y, label):
  f = h5py.File(filename)
  if len(f['NEO']['ParticleData']['Size_um']) == 0:
    print('Empty file : {}'.format(filename))
    return -1
  N = number_of_particles(f)
  cur_X = np.zeros((N, 5))
  load_data(cur_X, f)
  X.append(cur_X)
  y += [label] * len(cur_X)
  return 0
