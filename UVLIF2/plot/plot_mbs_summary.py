import os
import numpy as np
import matplotlib.pyplot as plt

def plot_mbs_summary(cfg):

  print("Plotting MBS summary ...")

  # load in the data and the labels
  output_directory = os.path.join(cfg['main_directory'], "output")
  data = np.genfromtxt(os.path.join(output_directory, "data.csv"), delimiter=',')
  file_labels = np.genfromtxt(os.path.join(output_directory, "file_labels.csv"), delimiter=',')

  # remove the shape info
  FL = data[:, 1024:-1]
  size = data[:, -1]

  # relabel
  new_labels = np.zeros(len(file_labels))
  for i, sample_idx in enumerate(cfg['plot_mbs_summary.groups']):
    new_labels[file_labels == i] = sample_idx

  #find the average for each group
  averages = []
  for sample_idx in np.unique(new_labels):
    # skip samples which are labelled as zero
    if sample_idx == 0:
      pass
    else:
      averages.append(np.mean(FL[new_labels == sample_idx], 0))

  for average in averages:
    plt.plot(average)
  plt.show()



  
