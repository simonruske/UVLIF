from collections import Counter
import os
from UVLIF.utils.filelist import load_filelist
from UVLIF.analysis.preprocess import preprocess
import numpy as np

def count(cfg, data, labels):
  files, _ = load_filelist(cfg, os.path.join(cfg['main_directory'], 'output'), 'filelist.csv')
  f_labels = np.genfromtxt(os.path.join(cfg['main_directory'], "output", "file_labels.csv"), delimiter=',')
  f_labels = np.array(f_labels, 'int')
  counts = Counter(f_labels)
  
  # get counts after preprocessing
  data, f_labels = preprocess(cfg, data, f_labels)
  counts_post_filter = Counter(f_labels)

  # saving the counts
  if not os.path.exists(os.path.join(cfg['main_directory'], 'output', 'results')):
    os.mkdir(os.path.join(cfg['main_directory'], 'output', 'results'))
  f = open(os.path.join(cfg['main_directory'], 'output','results', 'results.csv'), 'w')

  

  for label in np.sort(np.unique(f_labels)):
    f.write(str(files[label]) + ',' + str(counts[label]) + ',' + str(counts_post_filter[label])+ '\n')
  f.close()

