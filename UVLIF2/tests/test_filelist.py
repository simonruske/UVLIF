from unittest import TestCase
from UVLIF2.utils.filelist import create_filelist_laboratory, sort_filelist, create_filelist_ambient
import UVLIF2
import os
from datetime import datetime

class test_filelist(TestCase):

  def test_create_filelist_laboratory(self):
    # this doesn't actually check that the filelist created is correct
    cfg = {}
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    filelist_name = os.path.join(cfg['main_directory'], "tests", "filelist.csv") 

    create_filelist_laboratory(cfg, "tests", "tests")
    self.assertEqual(os.path.exists(filelist_name), True) 
    os.remove(filelist_name)

  def test_create_filelist_ambient(self):    

    cfg = {}
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF2.__file__))[0] 
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

    
