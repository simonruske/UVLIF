# HIDDEN IMPORTS (for packaging as .exe etc)
from sklearn.tree import _utils
from sklearn.neighbors import typedefs

# IMPORTS
import subprocess
import os
import numpy as np
from collections import Counter


from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans

# UVLIF imports 

from UVLIF.utils.directories import create_directory
from UVLIF.configuration.load_config import load_config

# other UVLIF analysis imports
from UVLIF.analysis.clustering.proportion import proportion
from UVLIF.analysis.clustering.cluster_utils import extract
from UVLIF.analysis.clustering.validation import validation
from UVLIF.analysis.preprocess import preprocess
from UVLIF.analysis.clustering.cluster_utils import standardise
from UVLIF.analysis.count import count

try:
  from fastcluster import linkage_vector
except Exception:
  print('Fastcluster not installed')


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
    clf, scr = basic_analysis_supervised(cfg, method, data, labels, parameters)
  elif method in ['HCA']:
    scr = basic_analysis_HCA(cfg, method, data, labels, parameters)
  elif method == 'KMeans':
    scr = basis_analysis_kmeans(cfg, method, data, labels, parameters)
  return clf, scr

def basis_analysis_kmeans(cfg, method, data, labels, parameters):
  print('Performing kmeans analysis')
  res = []
  for i in range(1,11):
    clf = KMeans(n_clusters=i).fit(data)
    res.append(proportion(clf.labels_, labels))
    print(i, res[-1])
    

  return -1

def basic_analysis_HCA(cfg, method, data, labels, parameters):

  print('Clustering ...')
  l = linkage_vector(data, parameters['linkage'][0])

  print('Extracting Cluster results ...')
  e = extract(l, 1, 20)

  print('Saving extracted clusters to file ...')
  ext = os.path.join(cfg['main_directory'], "output", 'extract.csv')
  f = open(ext, 'w')
  e = np.array(e, 'str')
  for line in e:
    f.write(','.join(line) + '\n')
  f.close()

  v = validation(data, e)
  print(validation(data, e, index = True))

  print('Saving processed data to file')
  pdata = os.path.join(cfg['main_directory'], "output", 'processed_data.csv')
  f = open(pdata, 'w')
  data = np.array(data, 'str')
  for line in data:
    f.write(','.join(line) + '\n')
  f.close()

  '''
  # index analysis
  print('Running index analysis')
  index_log = os.path.join(cfg['main_directory'], "output", "indices.txt")
  with open(index_log, 'w') as outfile:
    subprocess.call(["Rscript", os.path.join(os.path.dirname(__file__),  "indices.R"), ext, pdata, str(len(data)), str(len(data[0])), str(len(e)), str(len(e[0]))], stdout=outfile)
  '''

  # Compare first 10 clusters to optimal
  for i in range(10):
    print(i+1, proportion(e[i], labels))

  print('{} clusters found'.format(v))
  print(Counter(e[v-1]))

  return proportion(e[v-1], labels)
  
def basic_analysis_supervised(cfg, method, data, labels, parameters):

  classifiers = get_classifiers()
  clf = classifiers[method](**parameters)
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

def grid_analysis(cfg, method, data, labels, parameters):

  print('Multiple Options for a Single Parameter Detected Performing Grid Search')

  train_data, test_data, train_labels, test_labels = train_test_split(data, labels,\
                                                                      test_size = 0.5)
  classifiers = get_classifiers()
  default_clf = classifiers[method]()
  clf = GridSearchCV(default_clf, parameters)
  clf.fit(train_data, train_labels)
  print("Best parameters found : ", clf.best_params_)
  scr = clf.score(test_data, test_labels)
  
  return clf, scr
 
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



  
