from unittest import TestCase
import numpy as np
from UVLIF2.analysis.analysis import analyse
import os

class test_analysis(TestCase):

  '''
  For the analysis we are mostly running code from sklearn which has it's own testing suites
  so within this test we are focussing primarily that everything is able to run
  '''

  def prepare(self):

    # Create the test data
    data = np.random.rand(50, 5)
    labels = np.random.randint(2, size = 50)

    # create directories
    main_directory = os.path.join(os.curdir, "test_analysis")
    os.mkdir(main_directory)
    os.mkdir(os.path.join(main_directory, "output"))

    # set up config 
    cfg = {}
    cfg['main_directory'] = main_directory 

    # Save the test data
    np.savetxt(os.path.join(main_directory, "output", 'data.csv'), data, delimiter=',')
    np.savetxt(os.path.join(main_directory, "output", 'labels.csv'), labels, delimiter=',')

    return cfg, data, labels

  @classmethod
  def tearDownClass(cls):
    os.remove(os.path.join(os.curdir, "test_analysis", "output", 'data.csv'))
    os.remove(os.path.join(os.curdir, "test_analysis", "output", 'labels.csv'))
    os.rmdir(os.path.join(os.curdir, "test_analysis", "output"))
    os.rmdir(os.path.join(os.curdir, "test_analysis"))

  def test_analysis(self):


    cfg, data, labels = self.prepare()

    cfg['analysis'] = ['LDA', 'QDA', 'GNB', 'RF', 'GB', 'AB', 'KNN']
    analyse(cfg)


