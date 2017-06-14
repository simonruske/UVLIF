import os, sys
from UVLIF2.configuration.load_config import load_config_files
from UVLIF2.read.read import read_files
from UVLIF2.utils.cleaner import clean

cfg = load_config_files()
if len(sys.argv) == 1:
  read_files(cfg)

elif sys.argv[1] == 'clean':
  clean(cfg, sys.argv[2:])


