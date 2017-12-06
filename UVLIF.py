import os, sys
from UVLIF.configuration.load_config import load_config_files
from UVLIF.read.read import read_files
from UVLIF.plot.plot import plot
from UVLIF.utils.cleaner import clean
from UVLIF.utils.files import check
from UVLIF.utils.filelist import create_filelist_laboratory
from UVLIF.analysis.analysis import analyse
from UVLIF.gui.gui import run


if len(sys.argv) == 1:
  cfg = load_config_files()
  read_files(cfg)
  analyse(cfg)
  plot(cfg)

elif sys.argv[1] == 'clean':
  cfg = load_config_files()
  check(cfg)
  clean(cfg, sys.argv[2:])

elif sys.argv[1] == 'create' and sys.argv[2] == 'filelist':
  cfg = load_config_files()
  check(cfg)
  input_directory = os.path.join(cfg['main_directory'], "data")
  output_directory = os.path.join(cfg['main_directory'], "output")
  create_filelist_laboratory(cfg, input_directory, output_directory)

elif sys.argv[1] == 'gui':
  run()

else:
  print("Did not recognise that command")



