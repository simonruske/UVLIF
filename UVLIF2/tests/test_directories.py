from unittest import TestCase
from UVLIF2.utils.directories import directory_exists, create_directory, list_directory, list_files
import UVLIF2
import os

class test_directories(TestCase):

  def test_directory_exists(self):
    self.cfg = {}
    self.cfg['main_directory'] = os.path.split(UVLIF2.__file__)[0]
    self.assertEqual(True, directory_exists(self.cfg, "tests"))

  def test_directory_not_exists(self):
    self.cfg = {}
    self.cfg['main_directory'] = os.path.split(UVLIF2.__file__)[0]
    self.assertEqual(False, directory_exists(self.cfg, "alien"))

  def test_create_directory(self):
    self.cfg = {}
    self.cfg['main_directory'] = os.path.split(UVLIF2.__file__)[0]
    create_directory(self.cfg, "temp") 
    self.assertEqual(directory_exists(self.cfg, "temp"), True)
    os.rmdir(os.path.join(self.cfg['main_directory'], "temp"))

  def test_list_directory(self):
    self.cfg = {}
    self.cfg['main_directory'] = os.path.split(UVLIF2.__file__)[0]
    directory_list = list_directory(self.cfg, "tests")
    self.assertIn("test_files", directory_list)

  def test_list_files(self):
    self.cfg = {}
    self.cfg['main_directory'] = os.path.split(UVLIF2.__file__)[0]
    file_list = []
    for filename in list_files(self.cfg, "tests"):
      file_list.append(filename)
    self.assertIn("test_directories.py", file_list)
      
    


    
    
    
    
