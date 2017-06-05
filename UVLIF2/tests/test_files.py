from unittest import TestCase
import os
from UVLIF2.utils.files import load_file, search_for_line, str2date, get_date
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
    correct_date = datetime(day = 5, month = 6, year = 2016, hour = 15, minute = 20, second=30)
    self.assertEqual(str2date("Date : 05/06/2016 15:20:30", "Date : "), correct_date)

  def test_get_date(self):
    main_path = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    f = open(os.path.join(main_path, "tests", "test_files", "test_date.txt"))
    correct_date = datetime(day = 5, month = 6, year = 2016, hour = 15, minute = 20, second=30)
    self.assertEqual(get_date(f), correct_date)
    

   
