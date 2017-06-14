import os

def clean(cfg, filenames):

  '''
  Function that removes all the files specified in the filenames list

  Parameters
  ----------
 
  cfg['main_directory'] : str
    The main directory that contains the output directory which contains the files

  filenames : list 
    A list of files to be removed, set this to 'all' if you wish to remove all the files in 
    the output directory
  '''

  if filenames == 'all':
    filenames = os.listdir(os.path.join(cfg['main_directory'], 'output'))

  for filename in filenames:
    full_filename = os.path.join(cfg['main_directory'], 'output', filename)
    if os.path.exists(full_filename):
      os.remove(full_filename)
