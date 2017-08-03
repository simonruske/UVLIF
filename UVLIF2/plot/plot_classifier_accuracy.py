import matplotlib.pyplot as plt
import numpy as np
import os

def load_results(cfg):
  classifiers = []
  results = []
  f = open(os.path.join(cfg['main_directory'], "output", "results", "results.csv"))
  for line in f:
    classifier, result = line.strip('\n').split(',')
    classifiers.append(classifier)
    results.append(result)
  return np.array(classifiers, 'str'), np.array(results, 'float')

def plot_classifier_accuracy(cfg):
  classifiers, res = load_results(cfg)
  index = np.arange(len(res))
  bar_width = 0.75
  plt.bar(index, res, bar_width)
  plt.xticks(index, classifiers)
  plt.ylim(np.min(res) - 0.05, np.max(res) + 0.05)
  plt.show()
  
