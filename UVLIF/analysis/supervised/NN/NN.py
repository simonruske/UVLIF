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