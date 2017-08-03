from unittest import TestCase
import numpy as np
from UVLIF2.analysis.analysis import analyse, load_params
import atexit
import os
import shutil

class test_analysis(TestCase):

  '''
  For the analysis we are mostly running code from sklearn which has it's own testing suites
  so within this test we are focussing primarily that everything is able to run
  '''

  @classmethod
  def setUpClass(cls):
    main_directory = os.path.join(os.curdir, "test_analysis")
    os.mkdir(main_directory)
    os.mkdir(os.path.join(main_directory, "output"))


  @classmethod
  def tearDownClass(cls):
    shutil.rmtree(os.path.join(os.curdir, "test_analysis"))


  def prepare(self):

    # Create the test data
    data = np.random.rand(50, 5)
    labels = np.random.randint(2, size = 50)

    # create directories
    main_directory = os.path.join(os.curdir, "test_analysis")

    # set up config 
    cfg = {}
    cfg['main_directory'] = main_directory 

    # Save the test data
    np.savetxt(os.path.join(main_directory, "output", 'data.csv'), data, delimiter=',')
    np.savetxt(os.path.join(main_directory, "output", 'labels.csv'), labels, delimiter=',')

    return cfg, data, labels

  def test_analysis(self):
    cfg, data, labels = self.prepare()
    cfg['analysis'] = ['LDA', 'QDA', 'GNB', 'RF', 'GB', 'AB', 'KNN']
    analyse(cfg)

  def test_neural_network_analysis_non_default(self):
    cfg, data, labels = self.prepare()
    cfg['analysis'] = ['NN']
    cfg['NN_default_param'] = False
    analyse(cfg)

  def test_load_params(self):
    cfg = {'NN.activation':'relu', 'other_param':'junk'}
    params = load_params(cfg, 'NN.')
    self.assertEqual(params, {'activation':'relu'})
