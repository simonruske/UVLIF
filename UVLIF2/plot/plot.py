from UVLIF2.plot.plot_concentrations import plot_concentrations
from UVLIF2.plot.plot_fractions import plot_fractions, plot_fractions_ABC
from UVLIF2.plot.plot_diurnal import plot_diurnal_ABC
from UVLIF2.plot.plot_clusters import plot_clusters

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

  else:
    print('Plotting not requested')

