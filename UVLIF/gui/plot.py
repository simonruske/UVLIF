import UVLIF.gui.plot_ui as main
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np


# matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class plot_window(QtWidgets.QDialog, main.Ui_Form):

  def __init__(self, parent = None):
    super(plot_window, self).__init__(parent)
    self.setupUi(self)
    
    sc = MplCanvas(self)
    self.verticalLayout.addWidget(sc)
    self.move(self.parent().geometry().center() - self.rect().center())
    

class MplCanvas(FigureCanvas):

  def __init__(self, parent = None, width = 5, height = 4, dpi = 100):
  
    fig = Figure(figsize = (width, height), dpi = dpi)
    self.axes = fig.add_subplot(111)
    
    FigureCanvas.__init__(self, fig)
    
    FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding,
                               QtWidgets.QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)
    
    self.compute_initial_figure()
    
  def compute_initial_figure(self):
  
    t = np.arange(0.0, 3.0, 0.01)
    s = np.sin(2 * np.pi * t)
    self.axes.plot(t, s)