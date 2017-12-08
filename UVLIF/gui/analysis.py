import UVLIF.gui.analysis_ui as main
from UVLIF.gui.analysis_configuration import analysis_configuration_window
from PyQt5 import QtWidgets, QtCore
import os
from UVLIF.configuration.load_config import load_config
from UVLIF.configuration.save_config import save_config_file

class analysis_window(QtWidgets.QDialog, main.Ui_Dialog):

  def __init__(self, parent = None):
    super(analysis_window, self).__init__(parent)
    self.setupUi(self)
    self.cfg = {}
    self.analysis_options = {}
    self.shorthand = {}
    self.populate_list()

    # activate boxes
    self.activate_std_box()
    self.activate_size_box()


    self.analysis_configuration_window = analysis_configuration_window(self)
    
    self.msgBox = QtWidgets.QMessageBox()
   

    # connecting buttons
    self.editButton.clicked.connect(self.edit)
    self.checkAllButton.clicked.connect(self.check_all)
    self.uncheckAllButton.clicked.connect(self.uncheck_all)
    self.saveButton.clicked.connect(self.save)
    self.FTBox.stateChanged.connect(self.activate_std_box)
    self.sizeBox.stateChanged.connect(self.activate_size_box)
    

  def activate_box(self, box, lineedit, label):
    if box.isChecked():
      lineedit.setEnabled(True)
      label.setEnabled(True)
       
    else:
      lineedit.setEnabled(False)
      label.setEnabled(False)

  def activate_std_box(self):
    self.activate_box(self.FTBox, self.stdEdit, self.stdLabel)

  def activate_size_box(self):
    self.activate_box(self.sizeBox, self.sizeEdit, self.sizeLabel)

  def edit(self):
    
    item = self.listWidget.currentItem()
    if item == None:
      self.msgBox.setText("Please select a method to be edited")
      self.msgBox.exec_()
    else:
      self.analysis_configuration_window.setWindowTitle("Editing " + item.text())
      self.analysis_configuration_window.method = item.text()
      self.analysis_configuration_window.update()
      self.analysis_configuration_window.show()
    

  def populate_list(self):
    current_directory = os.path.abspath(__file__).strip('analysis.py')
    analysis_list_directory = os.path.join(current_directory + '..', 'configuration', 'analysis')
    analysis_list_directory = os.path.abspath(analysis_list_directory) #convert .. to directory
    for item in os.listdir(analysis_list_directory):
      cfg = load_config(os.path.join(analysis_list_directory, item))
      
      item = str(item).replace('.proto', '')
      
      self.listWidget.addItem(item)
      
      self.shorthand[item] = cfg['shorthand']
      self.analysis_options.update(cfg)
      del self.analysis_options['shorthand']
      

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

    try:
      filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Saving Analysis Config")
      
      self.cfg['analysis'] = []
      for i in range(self.listWidget.count()):
        item = self.listWidget.item(i)
        if item.checkState() == QtCore.Qt.Checked:
          self.cfg['analysis'].append(self.shorthand[item.text()])
      if self.FTBox.checkState() == QtCore.Qt.Checked:
        self.cfg['remove_FT'] = True
        self.cfg['number_of_std'] = self.stdEdit.text()
      if self.sizeBox.checkState() == QtCore.Qt.Checked:
        self.cfg['remove_size'] = True
        self.cfg['size_threshold'] = self.sizeEdit.text()
      save_config_file(self.cfg, filename)
      self.close()
    except Exception as e:
      self.msgBox.setText(str(e))
      self.msgBox.exec_()
     




    
