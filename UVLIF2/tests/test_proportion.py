from unittest import TestCase
from UVLIF2.analysis.clustering.proportion import proportion
import numpy as np 

class test_proportion(TestCase):

  def test_proportion_1(self):
    labels_1 = [1, 2, 3, 4]
    labels_2 = [1, 2, 3, 4]
    m = proportion(labels_1, labels_2, matching = True)
    self.assertTrue(np.all(m == np.array([[1, 0, 0, 0], [0, 1, 0, 0],\
                                          [0, 0, 1, 0], [0, 0, 0, 1]])))
    p = proportion(labels_1, labels_2, matching = False)
    self.assertEqual(p, 1.0)
    
