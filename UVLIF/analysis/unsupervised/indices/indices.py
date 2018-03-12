def process(cfg, data, labels, i):
  print('processing')

  l = linkage_vector(data, 'ward')
  e = extract(l, 1, 10)

  ext = os.path.join(cfg['main_directory'], "output", 'extract.csv')
  f = open(ext, 'w')
  e = np.array(e, 'str')
  for line in e:
    f.write(','.join(line) + '\n')
  f.close()

  print('Saving processed data to file')
  pdata = os.path.join(cfg['main_directory'], "output", 'processed_data.csv')
  f = open(pdata, 'w')
  data = np.array(data, 'str')
  for line in data:
    f.write(','.join(line) + '\n')
  f.close()

  if not os.path.exists(os.path.join(cfg['main_directory'], "output", "indices")):
    os.mkdir(os.path.join(cfg['main_directory'], "output", "indices"))

  HCA_log = open(os.path.join(cfg['main_directory'], "output", "indices", "HCA_{}.txt".format(i)), 'w')
  for line in e:
    HCA_log.write(str(proportion(line, labels)) + ',' + str(adjusted_rand_score(line, labels)) + '\n')

  index_log = os.path.join(cfg['main_directory'], "output", "indices", "indices_{}.txt".format(i))
  with open(index_log, 'w') as outfile:
    subprocess.call(["Rscript", os.path.join(os.path.dirname(__file__),  "indices_reduced.R"), ext, pdata, str(len(data)), str(len(data[0])), str(len(e)), str(len(e[0]))], stdout=outfile)

