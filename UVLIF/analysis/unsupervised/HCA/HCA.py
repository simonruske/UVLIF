def analyse_HCA_all(cfg, data, labels):
  f = open(os.path.join(cfg['main_directory'], "output", "overall_HCA_results.csv"), 'w')
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
          for link in ['ward', 'centroid', 'median', 'single']:
            i += 1
            l = linkage_vector(p_data, link)
            e = extract(l, 1, 10)
            v = validation(p_data, e)
            best = 0
            best_idx = 0
            for idx, item in enumerate(e):
              if adjusted_rand_score(item, p_labels) > best:
                best = adjusted_rand_score(item, p_labels)
                best_idx = idx

            CH_score = adjusted_rand_score(e[v-1], p_labels)
            line = ','.join([str(take_logs), str(remove_size), str(number_of_std), str(standardise_method), str(link), str(best), str(CH_score), str(best_idx + 1), str(v)]) + '\n'
            print(line)
            f.write(line)
  f.close()
  
  
def basic_analysis_HCA(cfg, method, data, labels, parameters):

  print('Clustering ...')
  print(parameters)
  l = linkage_vector(data, parameters['linkage'][0])

  print('Extracting Cluster results ...')
  e = extract(l, 1, 10)

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


  # index analysis
  if 'indices' in parameters and parameters['indices'] == ['True']:
    print('Running index analysis')
    index_log = os.path.join(cfg['main_directory'], "output", "indices.txt")
    with open(index_log, 'w') as outfile:
      subprocess.call(["Rscript", os.path.join(os.path.dirname(__file__),  "indices.R"), ext, pdata, str(len(data)), str(len(data[0])), str(len(e)), str(len(e[0]))], stdout=outfile)

  # Compare first 10 clusters to optimal
  prop = []
  for i in range(10):
    print(i+1, adjusted_rand_score(e[i], labels))
    prop.append(adjusted_rand_score(e[i], labels))
  print("Maximum achieved : {}".format(max(prop)))
  print("Result Achieved by CH index : {}".format(prop[v-1]))
  print(proportion(e[v-1], labels, matching = True))


  # clusters found from ch index
  print('{} clusters found'.format(v))

  return max(prop)