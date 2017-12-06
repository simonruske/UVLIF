from unittest import TestCase
from UVLIF.utils.cleaner import clean
import UVLIF
import os

class test_cleaner(TestCase):

  def prepare(self):
    cfg = {}
    root_dir = os.path.split(os.path.abspath(UVLIF.__file__))[0]
    cfg['main_directory'] = os.path.join(root_dir, "tests")
    return cfg

  def prepare_all(self):
    cfg = self.prepare()
    for filename in ['data.csv', 'labels.csv']:
      f = open(os.path.join(cfg['main_directory'], "output", filename), 'w')
      f.close()
    return cfg

  def prepare_data(self):
    cfg = self.prepare()
    for filename in ['data.csv', 'labels.csv', 'FT.csv', 'startend.csv', 'times.csv', 'junk.csv']:
      f = open(os.path.join(cfg['main_directory'], 'output', filename), 'w')
      f.close()
    return cfg 

  def prepare_results(self):
    cfg = self.prepare()
    os.mkdir(os.path.join(cfg['main_directory'], "output", "results"))
    f = open(os.path.join(cfg['main_directory'], "output", "results", "results.csv"), 'w')
    f.close()
    return cfg
    
  def test_clean(self):
    cfg = self.prepare_all()
    clean(cfg, ['data.csv', 'labels.csv'])
    self.assertNotIn('data.csv', os.listdir(os.path.join(cfg['main_directory'], "output")))
    self.assertNotIn('labels.csv', os.listdir(os.path.join(cfg['main_directory'], "output")))

  def test_clean_all(self):
    cfg = self.prepare_all()
    clean(cfg, ['all'])
    self.assertEqual(len(os.listdir(os.path.join(cfg['main_directory'], 'output'))), 0)

  def test_clean_data(self):
    cfg = self.prepare_data()
    clean(cfg, ['data'])
    output_directory = os.path.join(cfg['main_directory'], 'output')
    dir_list = os.listdir(output_directory)
    self.assertEqual(len(dir_list), 1)
    self.assertEqual(dir_list, ['junk.csv'])
    os.remove(os.path.join(output_directory, 'junk.csv'))

  def test_clean_results(self):
    cfg = self.prepare_results()
    clean(cfg, ['results'])
    results_directory = os.path.join(cfg['main_directory'], "output", "results")
    self.assertNotIn('results.csv', os.listdir(results_directory))
    os.rmdir(results_directory)

