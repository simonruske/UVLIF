import UVLIF2.gui.analysis_ui as main
from PyQt5 import QtWidgets, QtCore
import os
from UVLIF2.configuration.load_config import load_config
from UVLIF2.configuration.save_config import save_config_file

class analysis_window(QtWidgets.QDialog, main.Ui_Dialog):

  def __init__(self, parent = None):
    super(analysis_window, self).__init__(parent)
    self.setupUi(self)
    self.shorthand = {}
    self.populate_list()
    self.checkAllButton.clicked.connect(self.check_all)
    self.uncheckAllButton.clicked.connect(self.uncheck_all)
    self.saveButton.clicked.connect(self.save)
    self.cfg = {}
    

  def populate_list(self):
    current_directory = os.path.abspath(__file__).strip('analysis.py')
    analysis_list_directory = os.path.join(current_directory + '..', 'configuration', 'analysis')
    analysis_list_directory = os.path.abspath(analysis_list_directory) #convert .. to directory
    for item in os.listdir(analysis_list_directory):
      cfg = load_config(os.path.join(analysis_list_directory, item))
      item = str(item).replace('.proto', '')
      
      self.listWidget.addItem(item)
      
      self.shorthand[item] = cfg['shorthand']
      

    #add checkbox to each
    for i in range(self.listWidget.count()):
      item = self.listWidget.item(i)
      item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
      item.setCheckState(QtCore.Qt.Unchecked)

  def check_all(self):
    for i in range(self.listWidget.count()):
      item = self.listWidget.item(i)
      item.setCheckState(QtCore.Qt.Checked)

  def uncheck_all(self):
    for i in range(self.listWidget.count()):
      item = self.listWidget.item(i)
      item.setCheckState(QtCore.Qt.Unchecked)

  def save(self):
    filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Saving Analysis Config")
      
    self.cfg['analysis'] = []
    for i in range(self.listWidget.count()):
      item = self.listWidget.item(i)
      if item.checkState() == QtCore.Qt.Checked:
        self.cfg['analysis'].append(self.shorthand[item.text()])
    save_config_file(self.cfg, filename)
    self.close()
    




    
