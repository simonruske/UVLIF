from PyQt5 import QtWidgets, QtCore
import UVLIF.gui.main_ui as main

# for redirecting the standard output
import io
from contextlib import redirect_stderr, redirect_stdout

from UVLIF.configuration.load_config import load_config
from UVLIF.configuration.save_config import save_config_file
from UVLIF.utils.cleaner import clean
from UVLIF.analysis.analysis import analyse
from UVLIF.read.read import read_files

# imports for dialog windows
from UVLIF.gui.configuration import configuration_window
from UVLIF.gui.analysis import analysis_window
from UVLIF.gui.filelist import filelist_window

import os, sys, subprocess, logging

class main_window(QtWidgets.QMainWindow, main.Ui_MainWindow):

  def __init__(self, log_filename = None, parent = None):
    super(main_window, self).__init__(parent)
    self.log_filename = log_filename
    #thread for reading 
    self.readThread = TaskThread(self)
    self.readThread.function = read_files
    
    
    # fix for mac menubar
    self.menuBar().setNativeMenuBar(False)

    #msgbox
    self.msgBox = QtWidgets.QMessageBox()
    
    self.cfg = {}
    self.cfg_loaded = False
    self.analysis_cfg = {}
    self.analysis_cfg_loaded = False

    # set size
    self.resize(QtWidgets.QDesktopWidget().availableGeometry(self).size() * 0.7)

    # child windows
    self.configuration_window = configuration_window(self)
    self.analysis_window = analysis_window(self)
    self.filelist_window = filelist_window(self)


    # running start up functions
    self.setupUi(self)
    self.settings = load_config(self.settings_filename())
    self.setup_configuration()
    self.update()

    # ===============================
    # connecting buttons to functions
    # ===============================

    # textboxes changed
    self.mainLineEdit.textChanged.connect(self.update)
    self.analysisLineEdit.textChanged.connect(self.update)

    # clean buttons
    self.actionCleanAll.triggered.connect(self.clean_all)
    self.actionCleanProcessedData.triggered.connect(self.clean_data)
    self.actionCleanResults.triggered.connect(self.clean_results)
    self.actionCleanFilelist.triggered.connect(self.clean_filelist)

    self.actionExit.triggered.connect(self.close)
    self.actionNewConfiguration.triggered.connect(self.new_configuration_window)
    self.actionNewAnalysis.triggered.connect(self.open_analysis_window)
    self.actionEditConfiguration.triggered.connect(self.open_configuration_window)

    self.analysisLineEdit.textChanged.connect(self.update_analysis_config)
    self.configurationPushButton.clicked.connect(self.configurationPushButtonClicked)
    self.analysisPushButton.clicked.connect(self.analysisPushButtonClicked)

    # action buttons
    self.fileButton.clicked.connect(self.create_filelist)
    self.analyseButton.clicked.connect(self.analyse)
    self.createButton.clicked.connect(self.create)
   


  def open_analysis_window(self):
    self.analysis_window.show()
    self.update()    

  def configurationPushButtonClicked(self):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(self)
    self.mainLineEdit.setText(filename)

  def analysisPushButtonClicked(self):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(self)
    self.analysisLineEdit.setText(filename)

  def update(self):
    self.update_main_config()
    self.update_analysis_config()
    self.update_status()
    self.update_buttons()

  def update_buttons(self):
    try:
      if not self.cfg_loaded or 'ambient' not in self.cfg:
        self.set_buttons_enabled([False, False, False])
      elif not self.filelist_exists and self.cfg['ambient'] == False:
        self.set_buttons_enabled([True, False, False])

    except Exception as e:
      self.msgBox.setText("Error loading buttons : " + str(e))
      self.msgBox.exec_()
    
      

  def set_buttons_enabled(self, status):
    self.fileButton.setEnabled(status[0])
    self.createButton.setEnabled(status[1])
    self.analyseButton.setEnabled(status[2])

  def update_configuration_status(self, lineEdit, lineStatus):
    # get the filename from the textbox
    cfg = {}
    filename = lineEdit.text()

    #if the configuration file exists load it and set the status to loaded and green
    if os.path.exists(filename):
      cfg = load_config(filename)
      flag = True
      lineStatus.setStyleSheet("QLineEdit {background-color:green}")
      lineStatus.setText('LOADED')

    else:
      flag = False
      lineStatus.setStyleSheet("QLineEdit {background-color:red}")
      lineStatus.setText('NOT FOUND')
    return cfg, flag

  def update_main_config(self):
    parameters = {
      'lineEdit' : self.mainLineEdit,
      'lineStatus' : self.lineEditMainStatus,
    }
    self.cfg, self.cfg_loaded = self.update_configuration_status(**parameters)
    if 'ambient' in self.cfg:
      flag = self.cfg['ambient']
      self.status_visibility(self.filelistLabel, self.fileStatus, self.fileButton, not flag)

  def update_analysis_config(self):
    parameters = {
      'lineEdit' : self.analysisLineEdit,
      'lineStatus' : self.lineEditAnalysisStatus,
    }
    self.analysis_cfg, self.analysis_cfg_loaded = self.update_configuration_status(**parameters)

  def update_status(self):

    # check if the main directory is in the cfg and exists
    if 'main_directory' in self.cfg and os.path.exists(self.cfg['main_directory']):
      main_directory = self.cfg['main_directory']
      
      # check the output directory exists
      output_directory = os.path.join(main_directory, 'output')
      output_directory_exists = os.path.exists(output_directory)
      if not output_directory_exists:
        os.mkdir(output_directory)
      
      # if data.csv is in the output directory then set processed_data as true
      if 'data.csv' in os.listdir(output_directory):
        self.processed_data_exists = True
      else:
        self.processed_data_exists = False
      if 'filelist.csv' in os.listdir(output_directory):
        self.filelist_exists = True
      else:
        self.filelist_exists = False

      # if results directory is in output directory and results.csv exists
      # set results_exists as true
      results_directory = os.path.join(output_directory, "results")
      results_file = os.path.join(results_directory, "results.csv")
      if os.path.exists(results_directory) and os.path.exists(results_file):
        self.results_exists = True
      else:
        self.results_exists = False
      
    else:
      self.processed_data_exists = False
      self.results_exists = False
      self.filelist_exists = False

    self.display_status(self.processed_data_exists, self.dataStatus, self.createButton)
    self.display_status(self.results_exists, self.resultsStatus, self.analyseButton)
    self.display_status(self.filelist_exists, self.fileStatus, self.fileButton)

  def display_status(self, flag, statusbox, button):
    if flag == True:
      statusbox.setText("YES")
      statusbox.setStyleSheet("QLineEdit {background-color:green}")
      button.setEnabled(False)
    else:
      statusbox.setText("NO")
      statusbox.setStyleSheet("QLineEdit {background-color:red}")
      button.setEnabled(True)

  def setup_configuration(self):
    
    if 'main_directory' in self.settings:
      self.mainLineEdit.setText(self.settings['main_directory'])
      self.update_main_config()
    if 'analysis_directory' in self.settings:
      self.analysisLineEdit.setText(self.settings['analysis_directory'])
      self.update_analysis_config()

  def load_configuration(self):
    config_filename, _ = QtWidgets.QFileDialog.getOpenFileName()
    cfg = load_config(config_filename)
    self.configuration_window.load_config(cfg)

  def open_configuration_window(self):
    self.load_configuration()
    self.configuration_window.show()
    self.update()

  def new_configuration_window(self):
    self.configuration_window.show()
    self.update()

  def cfg_ok(self):
    if self.cfg_loaded == False:
      dialog = QtWidgets.QMessageBox()
      dialog.setText('Please load a configuration first!')
      dialog.exec_()
      return False
    else:
      return True

  def analyse(self):
    cfg = self.cfg
    cfg.update(self.analysis_cfg)
    try:
      analyse(cfg)
      subprocess.call(["xdg-open", os.path.join(cfg['main_directory'], "output", "results", "results.csv")])
      self.update()

    except Exception as e:
      dialog = QtWidgets.QMessageBox()
      dialog.setText(str(e))
      dialog.exec_()


  def settings_filename(self):
    # gets the settings filename
    current_directory = os.path.abspath(__file__.replace('main.py', ''))
    filename = os.path.join(current_directory, 'settings.proto')
    return filename

  def closeEvent(self, *args, **kwargs):
    # overwrite the closeEvent function to save the settings file
    super(QtWidgets.QMainWindow, self).closeEvent(*args, **kwargs)
    filename = self.settings_filename()

    # if no filename specified then close
    if filename == '':
      return


    #update the settings dictionary
    self.update_settings()

    #Get the current directory and save the settings proto there

    save_config_file(self.settings, filename)
    sys.exit()

  def update_settings(self):
    # update the settings file to include the contents of the main configuration text box
    # and the analysis configuration textbox only if the configurations are loaded
    if self.cfg_loaded == True:
      self.settings['main_directory'] = self.mainLineEdit.text()
    if self.analysis_cfg_loaded == True:
      self.settings['analysis_directory'] = self.analysisLineEdit.text()

  def load_instrument_cfg(self):
    if 'instrument_filename' in self.cfg:
      self.instrument_cfg = load_config(self.cfg['instrument_filename'])

  def onProgress(self, i):
    self.progress.setValue(i)
    self.readThread.quit()

  def onProgress_labels(self, my_string):
    self.progress.setLabelText(my_string)

  def onError(self, error_string):
    self.progress.close()
    self.clean_data()
    self.msgBox.setText(error_string)
    self.msgBox.exec_()
    

  def create(self):

    try:

      # show the error/warnings/progress dialog    
      cfg = {}
      cfg.update(self.cfg)
      self.load_instrument_cfg()
      cfg.update(self.instrument_cfg)
      self.progress = QtWidgets.QProgressDialog()


      # progress bar 

      # set the progress bar in the config so it can be changed by the underlying code
      cfg['progress_bar'] = self.progress

      # pass the config above to the read thread
      self.readThread.cfg = cfg

      # connect notifications for the bar and the label to corresponding functions
      self.readThread.notifyProgress.connect(self.onProgress)
      self.readThread.notifyProgress_labels.connect(self.onProgress_labels)
      self.readThread.notifyError.connect(self.onError)

      # show the progress bar and start the thread
      self.progress.show()
      self.readThread.start()

    except Exception as e:
      self.msgBox.setText("Error while creating data : {}".format(e))
      self.msgBox.exec_()

  def status_visibility(self, label, textbox, button, flag):
    label.setVisible(flag)
    textbox.setVisible(flag)
    button.setVisible(flag)

  def create_filelist(self):
  
    '''
    Function that allows user to create a filelist when 
    they press the corresponding button.
    '''
    logging.info("Attempting to create a filelist.")
    
    try:
      self.load_instrument_cfg()
      self.filelist_window.show()
      self.filelist_window.update()
      self.update()
      
    
    except Exception as e:
      logging.info("There was an error in creating the filelist"
                   ", notifying the user")
    
      self.msgBox.setText("Error while creating filelist : {}".format(e))
      self.msgBox.exec_()

  # cleaning functions
  
  def clean_all(self):
    if self.cfg_ok():
      clean(self.cfg, ['all'])
      self.update()

  def clean_data(self):
    if self.cfg_ok():
      clean(self.cfg, ['data'])
      self.update()

  def clean_results(self):
    if self.cfg_ok():
      clean(self.cfg, ['results'])
      self.update()

  def clean_filelist(self):
    if self.cfg_ok():
      clean(self.cfg, ['filelist.csv'])
      self.update()


class TaskThread(QtCore.QThread):
  notifyProgress = QtCore.pyqtSignal(int)
  notifyProgress_labels = QtCore.pyqtSignal(str)
  notifyError = QtCore.pyqtSignal(str)
  

  def __init__(self, parent):
    QtCore.QThread.__init__(self)

  def run(self):
    cfg = self.cfg
    cfg['progress'] = self.notifyProgress
    cfg['progress_labels'] = self.notifyProgress_labels
    try:
      self.function(cfg)
    except Exception as e:
      self.notifyError.emit(str(e))
