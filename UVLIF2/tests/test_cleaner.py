from unittest import TestCase
from UVLIF2.utils.cleaner import clean
import UVLIF2
import os

class test_cleaner(TestCase):

  def prepare(self):
    cfg = {}
    root_dir = os.path.split(os.path.abspath(UVLIF2.__file__))[0]
    cfg['main_directory'] = os.path.join(root_dir, "tests")
    f = open(os.path.join(cfg['main_directory'], "output", 'data.csv'), 'w')
    g = open(os.path.join(cfg['main_directory'], "output", 'labels.csv'), 'w')
    f.close()
    g.close()
    return cfg

  def test_clean(self):
    cfg = self.prepare()
    clean(cfg, ['data.csv', 'labels.csv'])
    self.assertNotIn('data.csv', os.listdir(cfg['main_directory']))
    self.assertNotIn('labels.csv', os.listdir(cfg['main_directory']))

  def test_clean_all(self):
    cfg = self.prepare()
    clean(cfg, 'all')
    self.assertEqual(len(os.listdir(os.path.join(cfg['main_directory'], 'output'))), 0)
