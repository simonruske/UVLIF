from unittest import TestCase
from UVLIF.utils.filelist import create_filelist_laboratory, sort_filelist,\
                                  create_filelist_ambient, load_filelist
import UVLIF
import os
from datetime import datetime

class test_filelist(TestCase):

  def test_create_filelist_laboratory(self):
    # this doesn't actually check that the filelist created is correct
    cfg = {}
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF.__file__))[0]
    filelist_name = os.path.join(cfg['main_directory'], "tests", "filelist.csv") 

    create_filelist_laboratory(cfg, "tests", "tests")
    self.assertEqual(os.path.exists(filelist_name), True) 
    os.remove(filelist_name)

  def test_create_filelist_ambient(self):    

    cfg = {}
    cfg['date_format'] = "%d/%m/%Y%H:%M:%S"
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF.__file__))[0] 
    dates, files = create_filelist_ambient(cfg, os.path.join("tests", "test_directory"), "tests")


  def test_sort_filelist(self):

    d1 = datetime(year = 2015, month = 5, day = 1) 
    d2 = datetime(year = 2014, month = 4, day = 2) 
    d3 = datetime(year = 2014, month = 4, day = 30)

    dates = [d1, d2, d3]
    files = ['f1.txt', 'f2.txt', 'f3.txt']

    dates, files = sort_filelist(dates, files)
    self.assertEqual(dates[0], d2)
    self.assertEqual(dates[1], d3)
    self.assertEqual(dates[2], d1)
    self.assertEqual(files[0], 'f2.txt')
    self.assertEqual(files[1], 'f3.txt')
    self.assertEqual(files[2], 'f1.txt')

  def test_load_filelist_not_found(self):
    cfg = {}
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF.__file__))[0]
    test_path = os.path.join(cfg['main_directory'], "tests", "test_files")
    with self.assertRaises(ValueError):
      files, labels = load_filelist(cfg, test_path, "alien.txt")

  def test_load_filelist(self):
    
    cfg = {}
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF.__file__))[0]
    test_path = os.path.join(cfg['main_directory'], "tests", "test_files")
    
    files, labels = load_filelist(cfg, test_path, "filelist_1.txt")
    self.assertEqual(files[0], "file1.txt")
    self.assertEqual(files[1], "file2.txt")
    self.assertEqual(labels[0], '1')
    self.assertEqual(labels[1], '2')
    self.assertEqual(len(files), 2)
    self.assertEqual(len(labels), 2)
    
    with self.assertRaises(ValueError):
      files, labels = load_filelist(cfg, test_path, "filelist_2.txt")

    with self.assertRaises(IOError):
      files, labels = load_filelist(cfg, test_path, "filelist_3.txt") 
    
    
    
