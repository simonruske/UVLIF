from UVLIF.plot.plot_concentrations import plot_concentrations
from UVLIF.plot.plot_fractions import plot_fractions, plot_fractions_ABC
from UVLIF.plot.plot_diurnal import plot_diurnal_ABC
from UVLIF.plot.plot_clusters import plot_clusters
from UVLIF.plot.plot_classifier_accuracy import plot_classifier_accuracy
from UVLIF.plot.plot_mbs_summary import plot_mbs_summary

def plot(cfg):

  if 'plot_list' in cfg:

    if 'plot_fractions' in cfg['plot_list']:
      plot_fractions(cfg)

    if 'plot_fractions_ABC' in cfg['plot_list']:
      plot_diurnal_ABC(cfg)

    if 'plot_diurnal_ABC' in cfg['plot_list']:
      plot_diurnal_ABC(cfg)

    if 'plot_clusters' in cfg['plot_list']:
      plot_clusters(cfg)

    if 'plot_concentrations' in ['plot_list']:
      plot_concentrations(cfg)

    if 'plot_classifier_accuracy' in cfg['plot_list']:
      plot_classifier_accuracy(cfg)

    if 'plot_mbs_summary' in cfg['plot_list']:
      plot_mbs_summary(cfg)
      

  else:
    print('Plotting not requested')


