import os
from UVLIF2.configuration.load_config import load_config

cfg = load_config(os.path.join(os.curdir, "UVLIF2", "configuration", "instrument", "instrument_1.proto"))

print(cfg)
