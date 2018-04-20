import UVLIF.gui.filelist_ui as main
from PyQt5 import QtWidgets, QtGui, QtCore
import os, logging

class filelist_window(QtWidgets.QDialog, main.Ui_Dialog):


  def __init__(self, parent = None):

    super(filelist_window, self).__init__(parent)
    self.desktop = QtWidgets.QDesktopWidget()
    self.setupUi(self)

    # set up the tableView
    self.initialise()

    # connect the save button
    self.pushButton.pressed.connect(self.save)
    
    # message box for errors
    self.msgBox = QtWidgets.QMessageBox()
    
    # set up logs
    log_filename = parent.log_filename
    logging.basicConfig(filename = log_filename, level = logging.DEBUG)
    
    
  def initialise(self):
  
    '''
    function for initialising the tableView
    '''
    
    self.model = QtGui.QStandardItemModel()
    
    self.tableView.setModel(self.model)
    self.model.setHorizontalHeaderLabels(["Filename", "Group"])
    self.model.setItem(0, 0, QtGui.QStandardItem())
    self.model.setItem(0, 1, QtGui.QStandardItem())
    self.set_stretch()
    
  def initialise_NEO(self):
  
    '''
    function for intialising the tableView for NEO
    '''
    
    # create a new model and set the table view to that model
    self.model = QtGui.QStandardItemModel()
    self.tableView.setModel(self.model)
    
    # set header
    self.model.setHorizontalHeaderLabels(["Directory", "Filename", "Notes", "Group"])
    
    # add empty item
    self.model.setItem(0, 0, QtGui.QStandardItem())
    self.model.setItem(0, 1, QtGui.QStandardItem())
    self.model.setItem(0, 2, QtGui.QStandardItem())
    self.model.setItem(0, 3, QtGui.QStandardItem())
    
    # set stretchyness of cols
    self.tableView.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
    self.tableView.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)
    self.tableView.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
    self.tableView.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Interactive)

    
  def set_stretch(self):
    self.tableView.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
    self.tableView.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Interactive)

  def update(self):
  
    '''
    Function for updating the filelist table
    '''
    logging.info("Attempting to update filelist table view")
    
    # start by checking if we're working with a NEO
    # get the instrument from the configuration
    if 'instrument_filename' not in self.parent().cfg:
      logging.info("Could not find instrument filename in"
                   " configuration, raising error.")
      raise ValueError("Instrument filename not specified in config")
    else:
      instrument_filename = self.parent().cfg['instrument_filename']
      
    logging.info(instrument_filename)
    logging.info(os.path.split(instrument_filename)[-1])
    if os.path.split(instrument_filename)[-1] == 'WIBSNEO.proto':
      logging.info("NEO identified, updating table accordingly")
      self.initialise_NEO()
      self.loadtable_NEO()
      
    else:
      self.initialise()
      self.loadtable()
      
  def loadtable_NEO(self):
    '''
    Function for loading the filelist for the NEO
    '''
  
    logging.info("Loading the filelist table for the NEO")
    
    # main directory
    dir = os.path.join(self.parent().cfg['main_directory'])
    data_files = []
    descriptions = []
    directories = []
    
    # search directory for data files
    for dirpath, dirnames, filenames in os.walk(dir):
      # check the directory contains a notes file and .h5 file
      notes_found = False
      data_found = False
      data_filenames = []
      for filename in filenames:
        if filename == 'Notes.txt':
          notes_found = True
        else:
          
          _, ext = os.path.splitext(filename)

          if ext == '.h5':
            data_found = True
            data_filenames.append(filename)
            

      # if data and notes are found then append info
      if data_found and notes_found:
        for data_filename in data_filenames:
          data_files.append(data_filename)
          with open(os.path.join(dirpath, "Notes.txt")) as f:
            descriptions.append(f.read())
          directories.append(dirpath) # add directory to list
    
    
    # load the files and discriptions into table
    logging.info("Finished searching, loading files into table")
    for i, (filename, description, directory) in enumerate(zip(data_files, descriptions, directories)):
      # create new item
      for j in range(4):
        self.model.setItem(i, j, QtGui.QStandardItem())
      
      # set the values of the new item
      for j, value in enumerate([directory, filename, description, 'None']):
        self.model.item(i, j).setText(value)
      
      # set first three columns to disables
      for j in range(3):
        self.model.item(i, j).setEnabled(False)
      
      # align last column
      self.model.item(i, 3).setTextAlignment(QtCore.Qt.AlignHCenter)

    
    
    
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
  
    # output string to be saved to file
    output = ''
    
    # loop through the table
    for i in range(self.model.rowCount()):
      # get row
      row = [self.model.item(i, j).text() for j in range(self.model.columnCount())]
      
      # if user hasn't labelled file as none then output
      if not row[-1] == "None":
        output += ','.join(row) + '\n'

    #If output isn't empty
    if output != '':
      f = open(os.path.join(self.parent().cfg['main_directory'], "output", "filelist.csv"), 'w')
      f.write(output)
      self.parent().update()
      self.close()

    else:
      self.msgBox.setText("At least one file must be placed into a group")
      self.msgBox.exec_()
