from sklearn.cluster import DBSCAN

def dbscan_analysis(cfg, method, data, labels, parameters):
  clusterer = DBSCAN(min_samples = len(data) * 0.07, eps = 0.4)
  cluster_labels = clusterer.fit_predict(data)
  print(adjusted_rand_score(cluster_labels, labels))
  print(proportion(cluster_labels, labels, matching = True))

def analyse_DBSCAN_all(cfg, data, labels):

  f = open(os.path.join(cfg['main_directory'], 'output', 'overall_DB_results.csv'), 'w')
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

          if len(p_data) > 40000:
            continue

          clusterer = DBSCAN(min_samples = len(p_data) * 0.01, eps = .4)
          cluster_labels = clusterer.fit_predict(p_data)

          # all labels
          p1 = adjusted_rand_score(cluster_labels, p_labels)

          p2 = adjusted_rand_score(cluster_labels[cluster_labels != -1], p_labels[cluster_labels != -1])
          p3 = np.round(sum(cluster_labels == -1) / len(cluster_labels) * 100, 1)

          line = ','.join([str(take_logs), str(remove_size), str(number_of_std), str(standardise_method), str(p1), str(p2), str(p3)]) + '\n'
          print(line)
          f.write(line)
		  

  
def dbscan_analysis_grid(cfg, method, data, labels, parameters):

  min_samples_list = list(np.arange(0.1, 1.0, 0.1) / 100) + list(np.arange(1, 11) / 100)
  min_samples_list = np.array(min_samples_list, 'float') * len(data)

  eps_list = np.arange(0.1, 1.1, 0.1)
  min_N = len(min_samples_list)
  eps_N = len(eps_list)
  results_1 = np.zeros((min_N, eps_N))
  results_2 = np.zeros((min_N, eps_N))
  results_3 = np.zeros((min_N, eps_N))
  for i, min_samples in enumerate(min_samples_list):
    for j, eps in enumerate(eps_list):
      try:
        clusterer = DBSCAN(min_samples = min_samples, eps = eps)
        cluster_labels = clusterer.fit_predict(data)

        # all labels
        p = adjusted_rand_score(cluster_labels, labels)

        print(min_samples, eps, p)
        results_1[i, j] = p
        #labels classified
        p = adjusted_rand_score(cluster_labels[cluster_labels != -1], labels[cluster_labels != -1])
        print(p)
        results_2[i, j] = p
        
        # noise
        p3 = np.round(sum(cluster_labels == -1) / len(cluster_labels) * 100, 1)
        print(p3)
        results_3[i,j] = p3
      except Exception:
        results_1[i, j] = -1
        results_2[i, j] = -1
        results_3[i, j] = -1

  np.savetxt(os.path.join(cfg['main_directory'], 'output', 'overall.csv'), results_1, delimiter=',')
  np.savetxt(os.path.join(cfg['main_directory'], 'output', 'wonoise.csv'), results_2, delimiter=',')
  np.savetxt(os.path.join(cfg['main_directory'], 'output', 'noise.csv'), results_3, delimiter=',')