'''
A set of functions that can be used to load configuration files
'''

def set_cfg(cfg, name, value):
  '''
  Function that sets a variable to the configuration dictionary

  Parameters 
  ----------
  name : str 
    name of variable to be set 

  value : various
    value for said global variable to be set to 

  '''
  cfg[name] = value

def convert_line(line):

  ''' 
  Function that converts a line from string to the requested type

  Parameters 
  ----------
  line : str
    the line to be converted, will include type, name and value

  returns
    name : str
      Name of the variable to be stored 

    value : various
      will return either string, int, float or list depending on the line
  '''
  # Parse the line into var_type, name, var_type
  rest, value = line.strip('\n').split(':')
  var_type, name = rest.split(' ')[:2]
  
  name = str(name.replace(' ', '')) 
  value = value.replace(' ', '')

  if var_type == 'int':
    return name, int(value)

  elif var_type == 'float':
    return name, float(value)

  elif var_type == 'string':
    return name, str(value)

  elif var_type == 'char':
    return name, value.decode('string_escape')

  elif var_type == 'bool':
    if value.lower() == 'true':
      return name, True
    
    elif value.lower() == 'false':
      return name, False
    
    else:
      raise ValueError('Bool must be set to true of false ({})'.format(name))
      

  elif var_type == 'list(int)':
    return name, read_list(value, 'int')

  elif var_type == 'list(float)':
    return name, read_list(value, 'float')

  elif var_type == 'list(string)':
    return name, read_list(value, 'string')

  else:
    raise ValueError() # We catch unrecognised lines in read_config instead

def read_list(value, var_type):

  '''
  Function that converts a string of a list to a list

  Parameters
  ----------
  value : str
    The list as a string prior to conversion

  Returns
  -------
  value : list
    The list once converted
  '''

  l = []

  for item in value.split(','):
    item = item.replace(" ", "")

    if var_type == 'int':
      l.append(int(item))

    elif var_type == 'float':
      l.append(float(item))

    elif var_type == 'string':
      l.append(str(item))

  return l


def load_config(filename):

  '''
  Function that loads a config file and converts the lines to global variables

  Parameters 
  ----------
  filename : str 
    The name of the file to be read in 

  Returns
  -------

  cfg : dict
    Dictionary to store the config variables
  '''

  f = open(filename)
  cfg = {}

  for line in f:

    line = line.split('//')[0]

    # Skip empty lines

    if len(line) <= 1:
      continue

    try:
      name, value = convert_line(line)

    except Exception:
      raise ValueError("Could not recognise the line '{}' in file {}".format(line, filename))
   
    set_cfg(cfg, name, value)

  return(cfg)








