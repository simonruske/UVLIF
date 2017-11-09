import UVLIF2.gui.filelist_ui as main
from PyQt5 import QtWidgets, QtGui, QtCore
import os

class filelist_window(QtWidgets.QDialog, main.Ui_Dialog):
  def __init__(self, parent = None):
    super(filelist_window, self).__init__(parent)
    self.desktop = QtWidgets.QDesktopWidget()
    self.setupUi(self)
    self.model = QtGui.QStandardItemModel()
    self.msgBox = QtWidgets.QMessageBox()
    self.tableView.setModel(self.model)
    self.model.setHorizontalHeaderLabels(["Filename", "Group"])
    self.model.setItem(0, 0, QtGui.QStandardItem())
    self.model.setItem(0, 1, QtGui.QStandardItem())
    self.set_stretch()

    # connect the save button
    self.pushButton.pressed.connect(self.save)
       
  def set_stretch(self):
    self.tableView.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
    self.tableView.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)

  def update(self):
    self.loadtable()
    
  def loadtable(self):
    data_directory = os.path.join(self.parent().cfg['main_directory'], "data")
    files = []
    for filename in os.listdir(data_directory):
      _, ext = os.path.splitext(filename)
      if ext in self.parent().instrument_cfg['valid_ext']:
        files.append(filename)
    
    for i, filename in enumerate(files):
      self.model.setItem(i, 0, QtGui.QStandardItem())
      self.model.setItem(i, 1, QtGui.QStandardItem())
      self.model.item(i, 0).setText(filename)
      self.model.item(i, 1).setText('None')
      self.model.item(i, 0).setEnabled(False)
      self.model.item(i, 1).setTextAlignment(QtCore.Qt.AlignHCenter)

  def save(self):

    output = ''
    for i in range(self.model.rowCount()):
      name, group = self.model.item(i, 0).text(), self.model.item(i, 1).text()
      if not group == "None":
        output += str(name) + ',' + str(group)+"\n"

    if output != '':
      f = open(os.path.join(self.parent().cfg['main_directory'], "output", "filelist.csv"), 'w')
      f.write(output)
      self.parent().update()
      self.close()

    else:
      self.msgBox.setText("At least one file must be placed into a group")
      self.msgBox.exec_()
