from unittest import TestCase
import os
from UVLIF2.configuration.load_config import set_cfg, convert_line, load_config, load_config_files

class test_read_config(TestCase):

  def setUp(self):
    self.addCleanup(self.clean)

  def clean(self):
    dirname, _ = os.path.split(os.path.abspath(__file__))
    os.remove(os.path.join(dirname, "main.proto"))

  def test_set_cfg(self):

    cfg = {}
    set_cfg(cfg, 'simon', 'ruske')
    self.assertEqual(cfg, {'simon':'ruske'})

  def test_convert_line_int(self):
     
    name, value = convert_line('int my_integer :: 1') 
    self.assertEqual(name, 'my_integer')
    self.assertEqual(value, 1)
    
  def test_convert_line_float(self):
    name, value = convert_line('float my_float :: 1.0')
    self.assertEqual(name, 'my_float')
    self.assertEqual(value, 1.0)

  def test_convert_line_string(self):
    name, value = convert_line('string my_string :: hello')
    self.assertEqual(name, 'my_string')
    self.assertEqual(value, 'hello')

  def test_convert_line_char(self):
    name, value = convert_line('char delimiter :: \t')
    self.assertEqual(name, 'delimiter')
    self.assertEqual(value, '\t')

  def test_convert_line_bool_true(self):
    name, value = convert_line('bool remove_FL :: True')
    self.assertEqual(name, 'remove_FL')
    self.assertEqual(value, True)

  def test_convert_line_bool_false(self):
    name, value = convert_line('bool remove_FL :: False')
    self.assertEqual(name, 'remove_FL')
    self.assertEqual(value, False)

  def test_convert_line_bool_neither(self):
    with self.assertRaises(ValueError):
      name, value = convert_line('bool remove_FL :: junk')


  def test_convert_line_list_int(self):
    name, value = convert_line('list(int) int_list :: 1, 2, 3, 4, 5')
    self.assertEqual(name, 'int_list')
    self.assertEqual(value, [1, 2, 3, 4, 5])

  def test_convert_line_list_int_shorthand(self):
    name, value = convert_line('list(int) int_list :: 1, 2, 10-12')
    self.assertEqual(name, 'int_list')
    self.assertEqual(value, [1, 2, 10, 11])

  def test_convert_line_list_float(self):
    name, value = convert_line('list(float) threshold :: 1.0, 2.5, 3.5')
    self.assertEqual(name, 'threshold')
    self.assertEqual(value, [1.0, 2.5, 3.5])

  def test_convert_line_list_string(self):
    name, value = convert_line('list(string) str_list :: the, cat, went, out')
    self.assertEqual(name, 'str_list')
    self.assertEqual(value, ['the', 'cat', 'went', 'out'])

  def test_convert_line_date(self):
    name, value = convert_line('string date_format :: %d/%m/%Y %H:%M:%S')
    self.assertEqual(name, 'date_format')
    self.assertEqual(value, '%d/%m/%Y%H:%M:%S')

  def test_convert_line_list_unknown(self):
    with self.assertRaises(ValueError):
      convert_line('alien my_alien :: tree')

  def test_load_config_missing(self):
    dirname, _ = os.path.split(os.path.abspath(__file__))
    with self.assertRaises(IOError):
      load_config(os.path.join(dirname, 'nonexistantfile.proto'))

  def test_load_config_found(self):
    dirname, _ = os.path.split(os.path.abspath(__file__))
    load_config(os.path.join(dirname,'test_files', 'test.proto'))

  def test_load_config_found_error(self):
    dirname, _ = os.path.split(os.path.abspath(__file__))
    with self.assertRaises(ValueError):
      load_config(os.path.join(dirname,'test_files', 'test_error.proto'))

  def test_load_config_files(self):
    dirname, _ = os.path.split(os.path.abspath(__file__))
    os.chdir(dirname)
    
    # test that we get IO error if we try reading in before the file is created
    with self.assertRaises(IOError):
      cfg = load_config_files()

    if os.path.exists('main.proto'):
      os.remove('main.proto')
    f = open('main.proto', 'w')
    i_file = os.path.join(dirname, "test_files", "i1.proto")
    a_file = os.path.join(dirname, "test_files", "a1.proto")
    f.write("string instrument_filename :: {}\n".format(i_file))
    f.write("string analysis_filename :: {}\n".format(a_file))
    f.close()
    cfg = load_config_files()
    self.assertIn("instrument_filename", cfg)
    self.assertIn("analysis_filename", cfg)
    self.assertIn("instrument_param", cfg)
    self.assertIn("analysis_param", cfg)
    if os.path.exists('main.proto'):
      os.remove('main.proto')
