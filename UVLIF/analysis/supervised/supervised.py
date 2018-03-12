import os
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.externals import joblib
from ...analysis.clustering.proportion import proportion


def basic_analysis_supervised_KFold(cfg, data, labels, clf):
  K = len(np.unique(labels))
  print(K)
  overall_matching = np.zeros((K, K))
  kf = StratifiedKFold(n_splits = 5, shuffle = True)
  for i, (train, test) in enumerate(kf.split(data, labels)):
    train_data = data[train]
    test_data = data[test]
    train_labels = labels[train]
    test_labels = labels[test]
    clf.fit(train_data, train_labels)
    overall_matching += proportion(clf.predict(test_data), test_labels, matching = True)
    joblib.dump(clf, os.path.join(cfg['main_directory'], 'output', 'GB_{}.pkl'.format(i)))
  print(np.array(overall_matching, 'int'))

  #data[:, 0:3] = data[:, 0:3] + np.array([19 + 14 + 20])
  clf.fit(data, labels)

  joblib.dump(clf, os.path.join(cfg['main_directory'], 'output', 'GB.pkl'))

  return clf, clf.score(data, labels)

def basic_analysis_supervised(cfg, data, labels, clf):
  clf, scr = basic_analysis_supervised_KFold(cfg, data, labels, clf)
  '''
  classifiers = get_classifiers()
  clf = classifiers[method](**parameters)
  train_data, test_data, train_labels, test_labels = train_test_split(data, labels, test_size=0.5)
  clf.fit(train_data, train_labels)
  scr = clf.score(test_data, test_labels)

  # matching matrix
  print(proportion(clf.predict(test_data), test_labels, matching = True))
  
  return clf, scr
  '''
  return clf, scr
  
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