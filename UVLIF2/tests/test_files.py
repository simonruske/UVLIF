from unittest import TestCase
import os
from UVLIF2.utils.files import load_file, search_for_line, str2date, get_date,\
                               file_exists, any_file_exists
import UVLIF2
from datetime import datetime

class test_files(TestCase):

  def test_load_file(self):
    cfg = {}
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    f = load_file(cfg, os.path.join("tests", "test_files"), "file.txt", 'w')
    f.write("hello")
    f.close()
    f = load_file(cfg, os.path.join("tests", "test_files"), "file.txt", 'r')
    self.assertEqual(f.readline(), "hello")

  def test_search_for_line(self):
    main_path = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    f = open(os.path.join(main_path, "tests", "test_files", "test_search.txt"))
    line = search_for_line(f, "is", 5)
    self.assertEqual(line, "is")
    with self.assertRaises(ValueError):
      line = search_for_line(f, "alien", 5)

  def test_str2date(self):
    cfg = {}
    cfg['date_format'] = "%d/%m/%Y %H:%M:%S"
    correct_date = datetime(day = 5, month = 6, year = 2016, hour = 15, minute = 20, second=30)
    self.assertEqual(str2date(cfg, "Date : 05/06/2016 15:20:30", "Date : "), correct_date)

  def test_get_date(self):
    cfg = {}
    cfg['date_format'] = "%d/%m/%Y %H:%M:%S"
    main_path = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    f = open(os.path.join(main_path, "tests", "test_files", "test_date.txt"))
    correct_date = datetime(day = 5, month = 6, year = 2016, hour = 15, minute = 20, second=30)
    self.assertEqual(get_date(cfg, f), correct_date)

  def test_get_date2(self):
    cfg = {}
    cfg['date_format'] = "%m/%d/%Y %H:%M:%S"
    main_path = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    f = open(os.path.join(main_path, "tests", "test_files", "test_date2.txt"))
    correct_date = datetime(day = 4, month = 1, year = 2013, hour = 9, minute = 23, second=17)
    self.assertEqual(get_date(cfg, f), correct_date)

  def test_get_date3(self):
    cfg = {}
    cfg['date_format'] = "%m/%d/%Y %H:%M:%S"
    main_path = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    f = open(os.path.join(main_path, "tests", "test_files", "test_date3.txt"))
    correct_date = datetime(day = 21, month = 1, year = 2013, hour = 9, minute = 23, second=17)
    self.assertEqual(get_date(cfg, f), correct_date)

  def test_file_exists_true(self):
    cfg = {}
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    test = file_exists(cfg, os.path.join("tests", "test_files"), "file.txt")
    self.assertEqual(test, True)

  def test_file_exists_false(self):
    cfg = {}
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    test = file_exists(cfg, os.path.join("tests", "test_files"), "alien.txt")
    self.assertEqual(test, False)

  def test_any_file_exists_true(self):
    cfg = {}
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    files = ["file.txt", "alien.txt"]
    test = any_file_exists(cfg, os.path.join("tests", "test_files"), files)
    self.assertEqual(test, True)

  def test_any_file_exists_false(self):
    cfg = {}
    cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    files = ["alien_1.txt", "alien_2.txt"]
    test = any_file_exists(cfg, os.path.join("tests", "test_files"), files)
    self.assertEqual(test, False)
  
    

   
