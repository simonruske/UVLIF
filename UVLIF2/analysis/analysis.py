from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

import os
import numpy as np


def analyse(cfg):
  if 'analysis' not in cfg:
    print("Analysis was not requested, so was skipped")
    return

  print("Analysing ...")
  data, labels = load_data(cfg)
  for method in cfg['analysis']:
    if method in ['LDA']:
      basic_analysis(cfg, method, data, labels)
  return

def load_data(cfg):
  print("Reading in the data ...")
  output_directory = os.path.join(cfg['main_directory'], "output")
  data = np.genfromtxt(os.path.join(output_directory, 'data.csv'), delimiter=',')
  labels = np.genfromtxt(os.path.join(output_directory, 'labels.csv'), delimiter=',')
  return data, labels

def basic_analysis(cfg, method, data, labels):
  classifiers = {'LDA':LinearDiscriminantAnalysis()}
  clf = classifiers[method]
  train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.5)
  clf.fit(train_data, train_labels)
  scr = clf.score(test_data, test_labels)
  print(str(method) + ": " + str(scr))
  
