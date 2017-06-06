from unittest import TestCase
from UVLIF2.read.read import prepare_laboratory
import UVLIF2
import os

class test_read(TestCase):

  def __init__(self, *args, **kwargs):
    super(test_read, self).__init__(*args, **kwargs)
    self.cfg = {}
    self.cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    self.input_dir = os.path.join("tests", "test_files") # input from testfiles
    self.output_dir = os.path.join("tests", "temp") # set output to temp directory
    if not os.path.exists(os.path.join(self.cfg['main_directory'], "temp")):
      os.mkdir(os.path.join(self.cfg['main_directory'], "temp")) # create temp directory

    self.addCleanup(self.clean)

  def clean(self, *args, **kwargs):
    super(test_read, self).__init__(*args, **kwargs)
    os.rmdir(os.path.join(self.cfg['main_directory'], "temp")) # cleanup


  def test_prepare_laboratory_FT_only(self):
    files, labels, forced, g, l = prepare_laboratory(self.cfg, self.input_dir, self.output_dir,\
                                                       'filelist_4.csv')

  def test_prepare_laboratory_data_only(self):
    files, labels, forced, g, l = prepare_laboratory(self.cfg, self.input_dir, self.output_dir,\
                                                       'filelist_5.csv')    

  def test_prerpare_laboratory_both(self):
    files, labels, forced, g, l = prepare_laboratory(self.cfg, self.input_dir, self.output_dir,\
                                                       'filelist_6.csv')
