def convert_element(name, value):

  ''' 
  Function that converts a line from string to the requested type

  Parameters 
  ----------
    name : str
      Name of the variable to be stored 

    value : various
      will be either string, int, float or list depending on the element

  Returns
  -------
    line : str 
  '''
  if type(value) == int:
    return 'int {} :: {}'.format(name, value)

  elif type(value) == float:
    return 'float {} :: {}'.format(name, value)

  elif type(value) == str:
    return 'string {} :: {}'.format(name, value)

  elif type(value) == bool:
    return 'bool {} :: {}'.format(name, value)

  # if list is empty return empty line
  elif type(value) == list and len(value) == 0:
    return ''

  elif type(value) == list and type(value[0]) == str:
    line = 'list(string) {} :: '.format(name)
    for item in value:
      line += item + ', '
    return line[:-2]
    

  else:
    raise ValueError() # We catch unrecognised lines in read_config instead


def save_config_file(cfg, filename):

  '''
  Function that saves a configuration to a file
  
  Parameters
  ----------
  cfg : dict
    Dictionary of configuration parameters
  
  filename : str
    Name of the file to save the configuration to

  '''

  g = open(filename, 'w')

  for name, value in cfg.items():
    g.write(convert_element(name, value) + '\n')

  g.close()


