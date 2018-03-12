def analyse_KM_all(cfg, data, labels):
  f = open(os.path.join(cfg['main_directory'], 'output', 'overall_KM_results.csv'), 'w')
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

          res = []
          e = []
          for i in range(1,11):
            clf = KMeans(n_clusters=i).fit(p_data)
            e.append(clf.labels_)
            res.append(adjusted_rand_score(clf.labels_, p_labels))
          e = np.array(e, 'float')
          v = validation(p_data, e)   

          CH_score = adjusted_rand_score(e[v-1], p_labels)
          line = ','.join([str(take_logs), str(remove_size), str(number_of_std), str(standardise_method), str(np.max(res)), str(CH_score), str(np.argmax(res)+1), str(v)]) + '\n'
          print(line)
          f.write(line)
  f.close()
  
  
def basis_analysis_kmeans(cfg, method, data, labels, parameters):
  print('Performing kmeans analysis')
  res = []
  for i in range(1,11):
    clf = KMeans(n_clusters=i).fit(data)
    res.append(proportion(clf.labels_, labels))
    print(i, res[-1])
	
  return -1