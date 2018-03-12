def analyse_GB_all(cfg, data, labels):
  f = open(os.path.join(cfg['main_directory'], 'output', 'overall_GB_results.csv'), 'w')
  i = 0
  for take_logs in [True, False]:
    cfg['take_logs'] = take_logs
    for remove_size in [0, 0.8]:
      cfg['remove_size'] = True
      cfg['size_threshold'] = remove_size

      for number_of_std in [0, 3, 9]:
        cfg['number_of_std'] = number_of_std
        if number_of_std == 0:
          cfg['remove_FT'] = True
        else:
          cfg['remove_FT'] = False
          
        for standardise_method in ['zscore', 'range']:
          cfg['standardise_method'] = standardise_method
          p_data, p_labels = preprocess(cfg, data.copy(), labels.copy()) 



          clf = GradientBoostingClassifier()
          kf = KFold(n_splits = 5, shuffle = True)
          result = np.zeros(len(p_labels))
          for i, (train, test) in enumerate(kf.split(p_data, p_labels)):
            train_data = p_data[train]
            test_data = p_data[test]
            train_labels = p_labels[train]
            test_labels = p_labels[test]
            clf.fit(train_data, train_labels)
            result[test] = clf.predict(test_data)

          score = adjusted_rand_score(result, p_labels)
             
          line = ','.join([str(take_logs), str(remove_size), str(number_of_std), str(standardise_method), str(score)]) + '\n'
          print(line)
          f.write(line)
  f.close()