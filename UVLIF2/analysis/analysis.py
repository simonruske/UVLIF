from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import GridSearchCV
from UVLIF2.analysis.clustering.cluster_utils import standardise
import os
import numpy as np

def analyse(cfg):

  # If analysis not requested by the user, skip this step
  if 'analysis' not in cfg:
    print("Analysis was not requested, so was skipped")
    return

  print("Analysing ...")
  data, labels = load_data(cfg)
  for method in cfg['analysis']:

    # Do basic analysis for everything apart from support vector machines and neural networks 
    # as they require some parameters modifying.
    if method in ['LDA', 'QDA', 'GNB', 'DT', 'RF', 'GB', 'AB', 'KNN']:
      basic_analysis(cfg, method, data, labels)

    elif method in ['SVC', 'LSVC']:
      support_vector_machine_analysis(cfg, method, data, labels)

    elif method == 'NN':
      neural_network_analysis(cfg, data, labels)
    
  return

def load_data(cfg):
  print("Reading in the data ...")
  output_directory = os.path.join(cfg['main_directory'], "output")
  data = np.genfromtxt(os.path.join(output_directory, 'data.csv'), delimiter=',')
  labels = np.genfromtxt(os.path.join(output_directory, 'labels.csv'), delimiter=',')
  return data, labels

def basic_analysis(cfg, method, data, labels):
  classifiers = {'LDA':LinearDiscriminantAnalysis(), 'QDA':QuadraticDiscriminantAnalysis(),\
                 'DT':DecisionTreeClassifier(), 'RF':RandomForestClassifier(),\
                 'GB':GradientBoostingClassifier(), 'AB':AdaBoostClassifier(),\
                 'GNB':GaussianNB(), 'KNN':KNeighborsClassifier()}
  clf = classifiers[method]
  train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.5)
  clf.fit(train_data, train_labels)
  scr = clf.score(test_data, test_labels)
  print(str(method) + ": " + str(scr))

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


def neural_network_analysis(cfg, data, labels):
  print("Neural Networks not yet implemented.")
  return
  
