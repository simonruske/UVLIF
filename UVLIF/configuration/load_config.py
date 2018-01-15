'''
A set of functions that can be used to load configuration files
'''

import os

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

def parse_tuple_string(string, tuple_type):

  '''
  Function that takes a string of tuples e.g. "(500, 400, 200), (300, 200, 100)"
  and converts to a list of tuples [(500, 400, 200), (300, 200, 100)]
  

  Parameters 
  ----------
  string : str
    The string to parsed

  tuple_type : type
    type of each element in the tuple

  Returns 
  -------
  tuple_list : list
    A list of tuples corresponding to the string entered
  '''

  tuple_list = [] # empty tuple list

  for character in string:

    # if character is open bracket create a new tuple
    if character == '(':
      new_tuple = []
      new_element = ''

    # if character is closed bracket append the new tuple
    elif character == ')':
      new_tuple.append(tuple_type(new_element))
      tuple_list.append(tuple(new_tuple))
      


    # if character is a comma end the current element and append to the
    # new_tuple list
    elif character == ',':
      new_tuple.append(tuple_type(new_element))
      new_element = ''

    else:
      new_element += character

  return tuple_list
    
      


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
  rest, value = line.strip('\n').split('::')
  var_type, name = rest.split(' ')[:2]
  
  name = str(name.replace(' ', '')) 


  if var_type != 'string':
    value = value.replace(' ', '')

  if var_type.startswith("list(tuple"):
    tuple_type = var_type.split(',')[1].replace(')', '') # convert var_type to the tuple type
    type_dict = {'int':int, 'float':float, 'string':str} # dictionary from string to type
    if tuple_type not in type_dict:
      raise ValueError("Could not understand the tuple type in line {}".format(line))


    return name, parse_tuple_string(value, type_dict[tuple_type])

  if var_type == 'none':
    return name, str(value)

  elif var_type == 'int':
    return name, int(value)

  elif var_type == 'float':
    return name, float(value)

  elif var_type == 'string':
    return name, str(value[1:])

  elif var_type == 'char':
    return name, bytes(value.encode()).decode('unicode_escape')

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
      l = load_integer_list(item, l)

    elif var_type == 'float':
      l.append(float(item))

    elif var_type == 'string':
      l.append(str(item))

  return l


def load_integer_list(item, l):

  '''
  Function that converts a string of an integer list to
  the said list. The list may contain "1-20" which is 
  shorthand for 1, 2, ..., 20

  Parameters 
  ----------
  item : string
    e.g. 1 or 1:20
  l : list
    list to append the item/items to
  '''

  if '-' in item:
    start, end = item.split('-')
    start, end = int(start), int(end)
    for i in range(start, end):
      l.append(i)

  else:
    l.append(int(item))

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

def load_config_files(filename=None):

  '''
  Function that loads the main, analysis and instrument configuration files

  Parameters
  ----------
  filename : str 
    The name of the main configuration file

  Returns 
  -------
  cfg : dict
    Configuration dictionary created from the configuration files.

  '''

  if not filename:
    filename = "main.proto"

  if os.path.exists(filename):
    cfg = load_config(filename)

  else:
    raise IOError("Could not find config file")

  cfg.update(load_config(cfg['instrument_filename']))
  cfg.update(load_config(cfg['analysis_filename']))

  return(cfg)

