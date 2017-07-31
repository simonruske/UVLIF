import os, sys
from UVLIF2.configuration.load_config import load_config_files
from UVLIF2.read.read import read_files
from UVLIF2.plot.plot import plot
from UVLIF2.utils.cleaner import clean
from UVLIF2.utils.filelist import create_filelist_laboratory
from UVLIF2.analysis.analysis import analyse

cfg = load_config_files()
if len(sys.argv) == 1:
  read_files(cfg)
  analyse(cfg)
  plot(cfg)

elif sys.argv[1] == 'clean':
  clean(cfg, sys.argv[2:])

elif sys.argv[1] == 'create' and sys.argv[2] == 'filelist':
  input_directory = os.path.join(cfg['main_directory'], "data")
  output_directory = os.path.join(cfg['main_directory'], "output")
  create_filelist_laboratory(cfg, input_directory, output_directory)

else:
  print("Did not recognise that command")



