from unittest import TestCase
from UVLIF2.utils.filelist import create_filelist_laboratory
import os
import UVLIF2

class test_filelist(TestCase):

  def test_create_filelist_laboratory(self):
    cfg = {}
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    create_filelist_laboratory(cfg, 'tests', 'tests')
    filelist_filename = os.path.join(cfg['main_directory'], 'tests', "filelist.csv")
    self.assertEqual(os.path.exists(filelist_filename), True)
    os.remove(filelist_filename)


