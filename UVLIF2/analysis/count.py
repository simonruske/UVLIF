from collections import Counter
import os
from UVLIF2.utils.filelist import load_filelist
import numpy as np

def count(cfg, data, labels):
  files, f_labels = load_filelist(cfg, os.path.join(cfg['main_directory'], 'output'), 'filelist.csv')
  f_labels = np.array(f_labels, 'int')
  counts = Counter(labels)

  f = open(os.path.join(cfg['main_directory'], 'output', 'results.csv'), 'w')

  for label in np.sort(np.unique(f_labels)):
    f.write(str(label) + ',' + str(counts[label]) + '\n')
  f.close()

