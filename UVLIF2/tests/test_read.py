from unittest import TestCase
from UVLIF2.utils.files import file_exists
from UVLIF2.read.read import prepare_laboratory, prepare_ambient, convert_info, close_files,\
                             write_start_end_date, line2list, check_output_list, output_list2str,\
                             write_line_laboratory, write_line_ambient, read_file
import UVLIF2
import os
from datetime import datetime

class test_read(TestCase):

  def __init__(self, *args, **kwargs):
    super(test_read, self).__init__(*args, **kwargs)
    self.cfg = {}
    self.cfg['main_directory'] = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    self.input_dir = os.path.join("tests", "test_files") # input from testfiles
    self.output_dir = "tests" # set output to temp directory


    self.addCleanup(self.clean)
    self.addCleanup(self.clean_write_line_test)

  def clean(self, *args, **kwargs):
    full_output_dir = os.path.join(self.cfg['main_directory'], self.output_dir)
    for filename in ['data.csv', 'FT.csv', 'labels.csv', 'times.csv', 'startend.csv']:
      full_filename = os.path.join(full_output_dir, filename)
      if os.path.exists(full_filename):
        os.remove(full_filename) 


  def test_prepare_laboratory_FT_only(self):
    file_info, forced, g, l = prepare_laboratory(self.cfg, self.input_dir, self.output_dir,\
                                                       'filelist_4.txt')
    correct_files = ['f1.txt', 'f2.txt']
    correct_labels = ['F', 'F']
    for i, (filename, label) in enumerate(file_info):
      self.assertEqual(filename, correct_files[i])
      self.assertEqual(label, correct_labels[i])

    self.assertNotEqual(forced, None)
    self.assertEqual(g, None)
    self.assertEqual(l, None)

  def test_prepare_laboratory_data_only(self):
    file_info, forced, g, l = prepare_laboratory(self.cfg, self.input_dir, self.output_dir,\
                                                       'filelist_5.txt')
    correct_files = ['f1.txt', 'f2.txt', 'f3.txt']
    correct_labels = ['1', '2', '3']
    for i, (filename, label) in enumerate(file_info):
      self.assertEqual(filename, correct_files[i])
      self.assertEqual(label, correct_labels[i])
    self.assertEqual(forced, None)
    self.assertNotEqual(g, None)
    self.assertNotEqual(l, None)
     

  def test_prepare_laboratory_both(self):
    file_info, forced,g, l = prepare_laboratory(self.cfg, self.input_dir, self.output_dir,\
                                                       'filelist_6.txt')
    correct_files = ['f1.txt', 'f2.txt']
    correct_labels = ['F', '1']
    for i, (filename, label) in enumerate(file_info):
      self.assertEqual(filename, correct_files[i])
      self.assertEqual(label, correct_labels[i])


    self.assertNotEqual(forced, None)
    self.assertNotEqual(g, None)
    self.assertNotEqual(l, None)

  def test_prepare_ambient_time_specified(self):
    self.cfg['time_stamp_specified'] = True
    self.input_dir = os.path.join("tests", "test_files_ambient")
    files, forced, g, time_handle, earliest_date, latest_date = prepare_ambient(self.cfg, self.input_dir, self.output_dir)
    self.assertEqual(len(files), 2)
    self.assertEqual(files[0], 'test_1.txt')
    self.assertEqual(files[1], 'test_2.txt')

  def test_convert_info_laboratory(self):
    cfg = {}
    cfg['ambient'] = False
    files = ['f1.txt', 'f2.txt']
    labels = ['1', '2']
    for i, info in enumerate(zip(files, labels)):
      file, label = convert_info(cfg, info)
      self.assertEqual(file, files[i])
      self.assertEqual(label, labels[i])
    
  def test_convert_info_ambient_FT(self):
    cfg = {}
    cfg['ambient'] = True
    cfg['FT_char'] = 'FT'
    files = ['FT1.txt', 'FT2.txt']
    for i, info in enumerate(files):
      file, is_FT = convert_info(cfg, info)
      self.assertEqual(file, files[i])
      self.assertEqual(is_FT, True)

  def test_convert_info_ambient_data(self):
    cfg = {}
    cfg['ambient'] = True
    cfg['FT_char'] = 'FT'
    files = ['f1.txt', 'f2.txt']
    for i, info in enumerate(files):
      file, is_FT = convert_info(cfg, info)
      self.assertEqual(file, files[i])
      self.assertEqual(is_FT, False)

  def test_close_files(self):
    g = open('data.csv', 'w')
    forced = open('FT.csv', 'w')
    l = None
    close_files([g, l, forced])

    self.assertTrue(g.closed)
    self.assertTrue(forced.closed)
    self.assertEqual(l, None)
    for filename in ['data.csv', 'FT.csv']:
      os.remove(filename)

  def test_write_start_end_date(self):

    write_start_end_date(self.cfg, self.output_dir, '05/01/2016', '05/02/2016')
    self.assertTrue(file_exists(self.cfg, self.output_dir, "startend.csv"))

  def test_line2list(self):

    line = '1.0,2.0,3.0,4.0\n'
    cfg = {}
    cfg['delimiter'] = ','
    cfg['needed_cols'] = [0, 2]
    output_list = ['1.0', '3.0']
    self.assertEqual(line2list(cfg, line), output_list)

  def test_check_output_list_correct(self):
    output_list = ['1.0', '3.0']
    self.assertTrue(check_output_list(output_list))
    
  def test_check_output_list_incorrect(self):
    output_list = ['1.0', 'G.0']
    self.assertFalse(check_output_list(output_list))

  def test_output_list2str(self):
    output_list = ['1.0', '3.0']
    output_str = '1.0,3.0\n'
    self.assertEqual(output_list2str(output_list), output_str)

  def prepare_write_line_test(self):
    g = open('data.csv', 'w')
    l = open('labels.csv', 'w')
    forced = open('FT.csv', 'w')
    return g, l, forced

  def clean_write_line_test(self):
    for filename in ['data.csv', 'labels.csv', 'FT.csv', 'times.csv']:
      if os.path.exists(filename):
        os.remove(filename)

  def test_write_line_laboratory_forced(self):
    g, l, forced = self.prepare_write_line_test()
    write_line_laboratory(g, l, forced, 'hello\n', 'F')
    close_files([g, l, forced])
    forced = open('FT.csv')
    self.assertEqual(forced.readline(), 'hello\n')
    forced.close()

  def test_write_line_laboratory_data(self):
    g, l, forced = self.prepare_write_line_test()
    write_line_laboratory(g, l, forced, 'hello\n', '1')
    close_files([g, l, forced])
    g = open('data.csv')
    l = open('labels.csv')
    self.assertEqual(g.readline(), 'hello\n')
    self.assertEqual(l.readline(), '1\n')
    close_files([g, l])

  def test_write_line_ambient_forced(self):
    g = open('data.csv', 'w')
    forced = open('FT.csv', 'w')
    write_line_ambient(g, forced, 'hello\n', True)
    close_files([g, forced])
    forced = open('FT.csv')
    self.assertEqual(forced.readline(), 'hello\n')
    forced.close()

  def test_write_line_ambient_data(self):
    g = open('data.csv', 'w')
    forced = open('FT.csv', 'w')
    write_line_ambient(g, forced, 'hello\n', False)
    close_files([g, forced])
    g = open('data.csv')
    self.assertEqual(g.readline(), 'hello\n')
    g.close()

  def test_write_line_ambient_time(self):
    g = open('data.csv', 'w')
    forced = open('FT.csv', 'w')
    time_handle = open('times.csv', 'w')
    cur_date = datetime(year=2016, month=12, day = 1)
    write_line_ambient(g, forced, 'hello\n', False, cur_date, time_handle)
    close_files([g, forced, time_handle])
    time_handle = open('times.csv')
    self.assertEqual(time_handle.readline(), str(cur_date) + '\n')

  def test_read_file_ambient_FT_1(self):
    cfg = {}
    cfg['ambient'] = True
    cfg['FT_char'] = 'FT'
    cfg['valid_ext'] = ['.txt', '.csv']
    cfg['file_name_specified'] = True
    cfg['time_stamp_specified'] = True
    cfg['main_directory'] = os.path.join(self.cfg['main_directory'], "tests")
    cfg['delimiter'] = ','
    cfg['needed_cols'] = [7, 8, 10, 14, 15]
    info = 'FT_clear.csv'
    g = open('data.csv', 'w')
    forced = open('FT.csv', 'w')
    read_file(cfg, info, g, forced)
    close_files([g, forced])
    forced = open('FT.csv')
    self.assertEqual(forced.readline(), '10,32,149,0.01968,-1\n')
    self.assertEqual(forced.readline(), '18,24,190,0.01968,-1\n')
    self.assertEqual(forced.readline(), '9,28,211,0.01968,-1\n')




    

  
    


   

    

    


  








