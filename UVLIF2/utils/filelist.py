from UVLIF2.utils.files import load_file
from UVLIF2.utils.directories import list_files
import os

def create_filelist_laboratory(cfg, input_directory, output_directory):

  '''
  Function used to create a file list file which lists the contents of
  the input directory specified. The file list is saved in the output directory.
  
  Parameters 
  ----------
  cfg['main_directory'] : str
    The main directory that contains the input and output directory

  input_directory : str
    The directory to be listed and stored in the filelist

  output_directory : str 
    The directory where the filelist will be stored

  '''

  f = load_file(cfg, output_directory, 'filelist.csv', 'w')
  for filename in list_files(cfg, input_directory):
    f.write(filename + '\n')
  f.close()

  
