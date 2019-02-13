# HIDDEN IMPORTS (for packaging as .exe etc)
from sklearn.tree import _utils
from sklearn.neighbors import typedefs

# IMPORTS
import subprocess
import os, logging
import numpy as np
from collections import Counter

# sklearn

from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import adjusted_rand_score


# UVLIF imports 

from UVLIF.utils.directories import create_directory
from UVLIF.configuration.load_config import load_config

# other UVLIF analysis imports
from UVLIF.analysis.clustering.proportion import proportion
from UVLIF.analysis.clustering.cluster_utils import extract
from UVLIF.analysis.clustering.validation import validation
from UVLIF.analysis.clustering.cluster_utils import standardise
from UVLIF.analysis.supervised.supervised import basic_analysis_supervised
from UVLIF.analysis.unsupervised.HCA.HCA import basic_analysis_HCA
from UVLIF.analysis.utilities.preprocess import preprocess
from UVLIF.analysis.basic.count import count

# neo reading imports
from UVLIF.read.read_NEO import read_NEO_new

try:
  from fastcluster import linkage_vector
except Exception:
  print('Fastcluster not installed')

def analyse(cfg):

  # begin logging of file
  logging.basicConfig(filename= cfg['log_filename'], level=logging.DEBUG)
  logging.info('=== begining analysis ===')

  # start logging

  # If analysis not requested by the user, skip this ste

  if 'analysis' not in cfg:
    print("Analysis was not requested, so was skipped")
    return
    
  if 'ambient' in cfg and cfg['ambient'] == True:
    raise NotImplementedError('Ambient Mode not yet implemented')

  if cfg['analysis'] == ['HCA_all']:
    data, labels = load_data(cfg)
    analyse_HCA_all(cfg, data, labels)

  if cfg['analysis'] == ['HCA_all_index']:
    data, labels = load_data(cfg)
    analyse_HCA_all_index(cfg, data, labels)

  if cfg['analysis'] == ['KM_all']:
    data, labels = load_data(cfg)
    analyse_KM_all(cfg, data, labels)

  if cfg['analysis'] == ['GB_all']:
    data, labels = load_data(cfg)
    analyse_GB_all(cfg, data, labels)

  if cfg['analysis'] == ['DBSCAN_all']:
    data, labels = load_data(cfg)
    analyse_DBSCAN_all(cfg, data, labels)
	
  if cfg['analysis'] == ['count']:
    data, labels = load_data(cfg)
    return count(cfg, data, labels)

  if os.path.isfile(os.path.join(cfg['main_directory'], "output", "results", "results.csv")):
    print("Analysis already complete")
    return

  # begin analysis by loading and preprocessing data
  
  data, labels = load_data(cfg)
  data, labels = preprocess(cfg, data, labels)
  print(len(data))

  # begin the classification
  print("Classifying ...")
  for method in cfg['analysis']:
    # load parameters from config file
    parameters = parameter_dict(cfg, method)
    grid_search = is_grid(parameters)
    

    print(method + " ...")

    if grid_search:
      clf, scr = grid_analysis(cfg, method, data, labels, parameters)

    else:
      clf, scr = basic_analysis(cfg, method, data, labels, parameters)

    # save everything
    create_directory(cfg, os.path.join("output", "results"))
    create_directory(cfg, os.path.join("output", "classifiers"))
    save_results(cfg, method, scr)
    
def save_results(cfg, method, scr):
  results_directory = os.path.join(cfg['main_directory'], "output", "results")
  f = open(os.path.join(results_directory, "results.csv"), "a+")
  f.write("{},{}\n".format(method, scr))
  f.close()

def parameter_dict(cfg, method):

  default_parameters = default_parameter_dict(method)
  parameters = {}
  for key, value in cfg.items():
    if key.startswith(method + '.'):
      default_parameter = default_parameters[key]
      parameters[key.replace(method + '.', '')] = parse_value(value, default_parameter, key.replace(method + '.', ""))

  return parameters

def default_parameter_dict(method):
    default_parameters = {}
    current_directory = os.path.abspath(__file__).strip('analysis.py')
    analysis_list_directory = os.path.join(current_directory + '..', 'configuration', 'analysis')
    analysis_list_directory = os.path.abspath(analysis_list_directory) #convert .. to directory
    for item in os.listdir(analysis_list_directory):
      cfg = load_config(os.path.join(analysis_list_directory, item))
      if cfg['shorthand'] == method:
        default_parameters.update(cfg)
        return default_parameters
    else:
      raise ValueError('Could not find configuration file for {}'.format(method))

def parse_value(value, default_parameter, parameter_name):

  if type(value) == list:
    new_value = []
    for item in value:
      
      # if the default parameter is float
      if type(default_parameter) == float:
        new_value.append(float(item))

      # if a default parameter has been set which is a different type to normal
      # e.g. gamma by default may be set to 'auto', but any float is also acceptable
      if type(default_parameter) == list and default_parameter[0] == 'default':
         if value == default_parameter[1]:
           new_value.append(default_parameter[1])
         elif default_parameter[-1] == 'float':
           new_value.append(float(item)) 

      if type(default_parameter) == list and type(default_parameter[0]) == tuple:
        new_value.append(tuple(item))

      if type(default_parameter) == list and type(default_parameter[0]) == str:
        new_value.append(str(item))
        

  if len(new_value) == 0:
    raise ValueError("Could not parse the parameter {}".format(parameter_name))

  return new_value

def is_grid(parameters):
  # returns true if there are multiple entries for at least one 
  # parameter and hence needing grid search
  for _, value in parameters.items():
    if len(value) > 1:
      return True
  else:
    return False 
    


def load_data(cfg):

  if 'instrument_filename' in cfg and 'WIBSNEO' in cfg['instrument_filename']:
    data, labels = read_NEO_new(cfg)
    #raise ValueError("Not yet implemented")
    return data, labels
    
    
 

  print("Reading in the data ...")

  # filenames / directories
  output_directory = os.path.join(cfg['main_directory'], "output")
  data_name = os.path.join(output_directory, 'data.csv')
  labels_name = os.path.join(output_directory, 'labels.csv')


  # get number of particles and number of data points
  f = open(data_name)
  N = 0 
  for line in f:
    N += 1

  if N == 0:
    raise ValueError("There were no particles found to be read in")

  M = len(line.strip('\n').split(','))

  # preallocate arrays
  data = np.zeros((N, M), dtype = 'float')
  labels = np.zeros(N, dtype = 'float')

  # load the data
  f = open(data_name)
  for i, line in enumerate(f):
    for j, item in enumerate(line.strip('\n').split(',')):
      data[i, j] = float(item)

  # load the labels
  f = open(labels_name)
  for i, line in enumerate(f):
    labels[i] = float(line.strip('\n'))


  return data, labels

def get_classifiers():
  classifiers = {'LDA':LinearDiscriminantAnalysis, 'QDA':QuadraticDiscriminantAnalysis,\
                 'DT':DecisionTreeClassifier, 'RF':RandomForestClassifier,\
                 'GB':GradientBoostingClassifier, 'AB':AdaBoostClassifier,\
                 'GNB':GaussianNB, 'KNN':KNeighborsClassifier, \
                 'MLP':MLPClassifier, 'SVC':SVC, 'LSV':LinearSVC}
  return classifiers

def basic_analysis(cfg, method, data, labels, parameters):
  clf = None
  if method in get_classifiers().keys():
    classifiers = get_classifiers()
    clf = classifiers[method](**parameters)
    clf, scr = basic_analysis_supervised(cfg, data, labels, clf)
  elif method in ['HCA']:
    scr = basic_analysis_HCA(cfg, method, data, labels, parameters)
  elif method == 'KMeans':
    scr = basis_analysis_kmeans(cfg, method, data, labels, parameters)
  elif method == 'DBSCAN':
    scr = dbscan_analysis(cfg, method, data, labels, parameters)
  return clf, scr

def load_params(cfg, root):
  params = {}
  for item, value in cfg.items():
    if root in item:
      params[item.strip(root)] = value
  return params



  
