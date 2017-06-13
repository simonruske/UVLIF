import os
from UVLIF2.configuration.load_config import load_config_files
from UVLIF2.read.read import read_files

cfg = load_config_files()
read_files(cfg)
