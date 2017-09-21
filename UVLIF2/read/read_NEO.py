import os
import h5py
import numpy as np


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
  

def read_NEO(cfg, info, g, l):


  print(info)
  # split the info into date and description
  date, folder, description, label = split_info(info)

  try:
    X = []
    y = []
    for filename in list_files(cfg, date, folder, description):
      flag = read_NEO_file(cfg, filename, X, y, label)
      if flag == -1:
        return

    g = open(os.path.join(cfg['main_directory'], "output", "data.csv"), 'a')
    l = open(os.path.join(cfg['main_directory'], "output", "labels.csv"), 'a')
    X = np.vstack(X)
    y = np.array(y, 'float')
    np.savetxt(g, X, delimiter=',')
    np.savetxt(l, y, delimiter=',')
  except ValueError:
    print("Skipping {}, {}, {}".format(date, folder, description))

def number_of_particles(f):
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
