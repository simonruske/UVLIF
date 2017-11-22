# HIDDEN IMPORTS
from sklearn.tree import _utils
from sklearn.neighbors import typedefs

# IMPORTS

from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from UVLIF2.analysis.clustering.cluster_utils import standardise
from UVLIF2.analysis.count import count
from UVLIF2.utils.directories import create_directory
import os
import numpy as np
from UVLIF2.analysis.clustering.proportion import proportion

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
  # Gets the threshold fro
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
  if 'remove_FT' in cfg:
    data, labels = remove_nFL(cfg, data, labels)

  if 'remove_size' in cfg:
    data, labels = remove_size(cfg, data, labels)
  return data, labels


def analyse(cfg):

  # If analysis not requested by the user, skip this step

  if 'analysis' not in cfg:
    print("Analysis was not requested, so was skipped")
    return

  if cfg['analysis'] == 'count':
    data, labels = load_data(cfg)
    return count(cfg, data, labels)

  if os.path.isfile(os.path.join(cfg['main_directory'], "output", "results", "results.csv")):
    print("Analysis already complete")
    return

  print("Analysing ...")
  data, labels = load_data(cfg)
  data, labels = preprocess(cfg, data, labels)
  print("Classifying ...")
  for method in cfg['analysis']:
    print(method + " ...")
    # Do basic analysis for everything apart from support vector machines and neural networks 
    # as they refquire some parameters modifying.

    if method in ['SVC', 'LSVC']:
      support_vector_machine_analysis(cfg, method, data, labels)

    elif method == 'NN' and 'NN_grid_search' in cfg and cfg['NN_grid_search'] == True:
      neural_network_analysis_grid_search(cfg, data, labels)

    elif method == 'NN' and 'NN_default_param' in cfg and cfg['NN_default_param'] == False:
      neural_network_analysis_non_default(cfg, data, labels)

    else:
      clf, scr = basic_analysis(cfg, method, data, labels)

    # save everything
    create_directory(cfg, os.path.join("output", "results"))
    create_directory(cfg, os.path.join("output", "classifiers"))
    save_results(cfg, method, scr)
    
def save_results(cfg, method, scr):
  results_directory = os.path.join(cfg['main_directory'], "output", "results")
  f = open(os.path.join(results_directory, "results.csv"), "a+")
  f.write("{},{}\n".format(method, scr))
  f.close()
    

def load_data(cfg):

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

  if 'instrument' in cfg and cfg['instrument'] == 'NEO':
    idx = np.invert(np.any(np.isnan(data), 1))
    data = data[idx]
    labels = labels[idx]
    idx = data[:, 0] > 0.8
    data = data[idx]
    labels = labels[idx]

  return data, labels

def basic_analysis(cfg, method, data, labels):
  classifiers = {'LDA':LinearDiscriminantAnalysis(), 'QDA':QuadraticDiscriminantAnalysis(),\
                 'DT':DecisionTreeClassifier(), 'RF':RandomForestClassifier(),\
                 'GB':GradientBoostingClassifier(), 'AB':AdaBoostClassifier(),\
                 'GNB':GaussianNB(), 'KNN':KNeighborsClassifier(), \
                 'MLP':MLPClassifier()}
  clf = classifiers[method]
  train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.5)
  clf.fit(train_data, train_labels)
  scr = clf.score(test_data, test_labels)

  # matching matrix
  print(proportion(clf.predict(test_data), test_labels, matching = True))
  
  return clf, scr

def support_vector_machine_analysis(cfg, method, data, labels):

  # support vector classifiers
  classifiers = {'SVC':SVC(), 'LSVC':LinearSVC()}
  

  # standardise the data using z-score
  s_data = standardise(data, 'zscore')

  # get a sample of say 10%
  s = np.random.randint(len(s_data), size = len(s_data)//10)
  data_sample = s_data[s]
  label_sample = labels[s]

  # split into training and testing data
  train_data, test_data, train_labels, test_labels = train_test_split(data_sample, label_sample,\
                                                                      test_size = 0.5)

  # set the grid space to search
  if method == 'SVC':
    parameters = {'gamma':[1, 10, 100, 1000], 'C':[1, 10, 100, 1000]}
  elif method == 'LSVC':
    parameters = {'C':[1, 10, 100, 1000]}

  svr = classifiers[method]

  clf = GridSearchCV(svr, parameters)
  clf.fit(train_data, train_labels)

  scr = clf.score(test_data, test_labels)
  print(clf.best_params_)

  # Select the best classifiers for the support vector machine method selected
  if method == 'SVC':
    best_C, best_gamma = clf.best_params_['C'], clf.best_params_['gamma']
    clf = SVC(C = best_C, gamma = best_gamma)

  elif method == 'LSVC':
    best_C = clf.best_params_['C']
    clf = LinearSVC(C = best_C)

  clf.fit(train_data, train_labels)
  scr = clf.score(test_data, test_labels)
  print(scr)

def neural_network_analysis_grid_search(cfg, data, labels):

  data = standardise(data, 'zscore')

  # split into training and testing data
  train_data, test_data, train_labels, test_labels = train_test_split(data, labels,\
                                                                      test_size = 0.5)

  clf = MLPClassifier(max_iter = 1000)
  # set the grid space to search
  parameters = {'solver':['lbfgs', 'sgd', 'adam'], 'activation':['logistic', 'tanh', 'relu'],\
                'hidden_layer_sizes':[(300), (500, 10)]}

  # test the space
  mlp_classifier = MLPClassifier(max_iter=1000)
  clf = GridSearchCV(mlp_classifier, parameters)
  clf.fit(train_data, train_labels)
  scr = clf.score(test_data, test_labels)
  print(clf.best_params_)
  print(scr)

def neural_network_analysis_non_default(cfg, data, labels):
  data = standardise(data, 'zscore')
  # split into training and testing data
  train_data, test_data, train_labels, test_labels = train_test_split(data, labels,\
                                                                      test_size = 0.5)
  params = load_params(cfg, 'NN.')
  clf = MLPClassifier(**params)
  print(clf)
  clf.fit(train_data, train_labels)
  scr = clf.score(test_data, test_labels)
  print(scr)

'''
This definitely needs to be moved to utils
'''

def load_params(cfg, root):
  params = {}
  for item, value in cfg.items():
    if root in item:
      params[item.strip(root)] = value
  return params



  
