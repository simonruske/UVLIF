import UVLIF.gui.plot_ui as main
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from scipy.cluster.hierarchy import dendrogram


# matplotlib imports
import logging
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from UVLIF.read.read_NEO import read_NEO_file_new
from fastcluster import linkage_vector

class plot_window(QtWidgets.QDialog, main.Ui_plot_window):

  def __init__(self, parent = None):
    super(plot_window, self).__init__(parent)
    self.setupUi(self)
    
    self.sc = MplCanvas(self)
    self.verticalLayout.addWidget(self.sc)
    self.move(self.parent().geometry().center() - self.rect().center())
    
    # other parameters
    self.filenames = None
    self.cfg = {}

class MplCanvas(FigureCanvas):

  def __init__(self, parent = None, width = 5, height = 4, dpi = 100):
  
    fig = Figure(figsize = (width, height), dpi = dpi)
    self.axes = fig.add_subplot(111)
    
    FigureCanvas.__init__(self, fig)
    
    FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                               QtWidgets.QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)
    
  def load_files(self):
    
    self.sizes = []
    self.means = []
    self.textlabels = []
    logging.info(self.parent().filenames)
    logging.info(self.parent().notes)
    
    for file, note in zip(self.parent().filenames, self.parent().notes):
      try:
        data, _ = read_NEO_file_new(self.parent().cfg, file, 0)
        if len(data) != 0:
          idx = ~np.isnan(data).any(axis = 1)
          data = data[idx]

          idx = ~np.isinf(data).any(axis = 1)
          data = data[idx]

        if len(data) != 0:
          self.means.append(np.mean(data, 0))
          self.sizes.append(data[:, 0])
          self.textlabels.append(note + ' (' + str(len(data)) + ')')
          
      except Exception as e:
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(file + " : " + str(e))
        msgBox.exec_()
      
        
    
  def compute_initial_figure(self):
    try:
      self.load_files()
      self.axes.cla()
      logging.info(len(self.means))
      self.means = (self.means - np.mean(self.means))/np.std(self.means)
      l = linkage_vector(self.means, 'ward')
      dn = dendrogram(l, ax = self.axes, orientation = 'right', labels = self.textlabels, leaf_font_size = 18)
      self.draw()
      
    except Exception as e:
      logging.info("Creatinging message box")
      msgBox = QtWidgets.QMessageBox()
      logging.info("Setting text")
      msgBox.setText(str(e))
      logging.info("exec")
      
      msgBox.exec_()
    
      
    