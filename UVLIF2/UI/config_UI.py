import UVLIF2
import os

# Allow for input in both python 2 & 3
try: input = raw_input
except NameError : pass

def select_configuration(config_type):
  root = os.path.split(UVLIF2.__file__)[0]
  option_names = os.listdir(os.path.join(root, "configuration", config_type))
  options = {}
  
  for i, option_name in enumerate(option_names):
    print('{}) {}'.format(i + 1, os.path.splitext(option_name)[0]))
    options[str(i + 1)] = i + 1
  
  while True:
  
    try: 
      choice = input("Please enter the {} option you would like to use : ".format(config_type))
      choice_name = option_names[options[choice] - 1]
      break
   
    except KeyError:
      print("Please enter a value from 1 to {}".format(i+1))

    print("Loading {} ...".format(choice_name))
  
  
