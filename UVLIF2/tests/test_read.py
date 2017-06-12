from unittest import TestCase
from UVLIF2.read.read import prepare_laboratory, prepare_ambient
import UVLIF2
import os

class test_read(TestCase):

  def __init__(self, *args, **kwargs):
    super(test_read, self).__init__(*args, **kwargs)
    self.cfg = {}
    self.cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    self.input_dir = os.path.join("tests", "test_files") # input from testfiles
    self.output_dir = "tests" # set output to temp directory


    self.addCleanup(self.clean)

  def clean(self, *args, **kwargs):
    full_output_dir = os.path.join(self.cfg['main_directory'], self.output_dir)
    for filename in ['data.csv', 'FT.csv', 'labels.csv', 'times.csv']:
      full_filename = os.path.join(full_output_dir, filename)
      if os.path.exists(full_filename):
        os.remove(full_filename) 


  def test_prepare_laboratory_FT_only(self):
    files, labels, forced, g, l = prepare_laboratory(self.cfg, self.input_dir, self.output_dir,\
                                                       'filelist_4.txt')
    self.assertEqual(files, ['f1.txt', 'f2.txt'])
    self.assertEqual(labels, ['F', 'F'])
    self.assertNotEqual(forced, None)
    self.assertEqual(g, None)
    self.assertEqual(l, None)

  def test_prepare_laboratory_data_only(self):
    files, labels, forced, g, l = prepare_laboratory(self.cfg, self.input_dir, self.output_dir,\
                                                       'filelist_5.txt')
    self.assertEqual(files, ['f1.txt', 'f2.txt', 'f3.txt'])
    self.assertEqual(labels, ['1', '2', '3'])
    self.assertEqual(forced, None)
    self.assertNotEqual(g, None)
    self.assertNotEqual(l, None)
     

  def test_prepare_laboratory_both(self):
    files, labels, forced, g, l = prepare_laboratory(self.cfg, self.input_dir, self.output_dir,\
                                                       'filelist_6.txt')
    self.assertEqual(files, ['f1.txt', 'f2.txt'])
    self.assertEqual(labels, ['F', '1'])
    self.assertNotEqual(forced, None)
    self.assertNotEqual(g, None)
    self.assertNotEqual(l, None)

  def test_prepare_ambient_time_specified(self):
    self.cfg['time_stamp_specified'] = True
    self.input_dir = os.path.join("tests", "test_files_ambient")
    files, forced, g, time_handle = prepare_ambient(self.cfg, self.input_dir, self.output_dir)
    self.assertEqual(len(files), 2)
    self.assertEqual(files[0], 'test_1.txt')
    self.assertEqual(files[1], 'test_2.txt')
    


  








