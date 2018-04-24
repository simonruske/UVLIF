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
    
    #set logging file
    self.log_filename = log_filename
    
    #thread for reading 
    self.readThread = TaskThread(self)
    self.readThread.function = read_files
    
    #thread for analysing 
    self.analysisThread = TaskThread(self)
    self.analysisThread.function = analyse
    
    
    # fix for mac menubar
    self.menuBar().setNativeMenuBar(False)

    #msgbox
    self.msgBox = QtWidgets.QMessageBox()
    
    self.cfg = {}
    self.cfg_loaded = False
    self.main_cfg = {}
    self.analysis_cfg = {}
    
    
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
    
    self.set_initial_form_configuration()
    self.settings = load_config(self.settings_filename())
    self.setup_configuration()

    self.connect_buttons()
    
    self.update()
    
  def connect_buttons(self):
  
    '''
    This function will be called on initialisation to connect
    all of the buttons to their corresponding functions
    '''
    
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

    
    self.analysisLineEdit.textChanged.connect(self.update)
    self.configurationPushButton.clicked.connect(self.configurationPushButtonClicked)
    self.analysisPushButton.clicked.connect(self.analysisPushButtonClicked)

    # action buttons
    self.fileButton.clicked.connect(self.create_filelist)
    self.analyseButton.clicked.connect(self.analyse)
    self.createButton.clicked.connect(self.create)  
   
  def set_initial_form_configuration(self):
  
    '''
    This function will be called upon initialisation of
    the main form and will set the parameters for each of the
    elements to their default characteristics
    
    Elements
    --------
    main configuration line
      state - loaded or not found
      
    analysis_configuration line
      state - loaded or not found
      
    filelist status
      state - yes or no
      visibility - visible or invisible
      enabled - enabled or disabled
      
    data status
      state - yes or no
      visibility - visible or invisible
      enabled - enabled or disabled
      
    results status
      state - yes or no
      visibility - should always be visible
      enabled - enabled or disabled
      
    '''
    
    # =============
    # CONFIGURATION
    # =============
    
    self.main_state = 'NOT FOUND'
    self.analysis_state = 'NOT FOUND'
    
    # ======
    # STATUS
    # ======
    
    # filelist
    self.filelist_state = 'NO'
    self.filelist_visible = True
    self.filelist_enabled = False
    
    # data
    self.data_state = 'NO'
    self.data_visible = True
    self.data_enabled = False
    
    # results
    self.result_state = 'NO'
    self.result_visible = True
    self.result_enabled = False

  def display_form(self):
  
    '''
    Function that displays the form using current
    state elements
    '''
    
    self.display_configuration()
    self.display_status()
    
  def display_configuration(self):
  
    '''
    Function that displays the configuration
    using current state elements
    '''
    
    self.display_status_box(self.lineEditMainStatus, self.main_state)
    self.display_status_box(self.lineEditAnalysisStatus, self.analysis_state)
    
  def display_status(self):

    '''
    Function that displays the status using the current 
    state elements
    '''
    
    # displays the status boxes
    self.display_status_box(self.dataStatus, self.data_state)
    self.display_status_box(self.resultsStatus, self.result_state)
    self.display_status_box(self.fileStatus, self.filelist_state)
    
    # sets to visible or invisible
    self.set_status_visibility(self.filelistLabel, self.fileStatus, self.fileButton, self.filelist_visible)
    self.set_status_visibility(self.dataLabel, self.dataStatus, self.createButton, self.data_visible)
    self.set_status_visibility(self.resultsLabel, self.resultsStatus, self.analyseButton, self.result_visible)
    
    
    # sets to enabled or not enabled
    self.set_status_enabled(self.filelistLabel, self.fileStatus, self.fileButton, self.filelist_enabled)
    self.set_status_enabled(self.dataLabel, self.dataStatus, self.createButton, self.data_enabled)
    self.set_status_enabled(self.resultsLabel, self.resultsStatus, self.analyseButton, self.result_enabled)
    
    
    return
    
  def set_status_enabled(self, label, textbox, button, flag):

      '''
      Function that sets a status line to either enabled or disabled
      
      Paramters
      ---------
      label, textbox, button
        objects that form part of the line to set visibility for
        
      flag : bool
        True for enabled, false for disabled
      '''  
      button.setEnabled(flag)   
    
  def set_status_visibility(self, label, textbox, button, flag):

    '''
    Function that sets a status line to either visible
    or invisible
    
    Paramters
    ---------
    label, textbox, button
      objects that form part of the line to set visibility for
      
    flag : bool
      True for visible, false for invisible
    '''    
  
    label.setVisible(flag)
    textbox.setVisible(flag)
    button.setVisible(flag)
    
    
   
    
    
  def display_status_box(self, lineStatus, current_status):
  
    '''
    Function that displays a status box
    
    Parameter
    ---------
    lineStatus : 
      the line status to be updated
      
    current_status:
      the current status of the line : 
        loaded or yes as positive
        not found or no as negative
    '''
    
    if current_status in ['LOADED', 'YES']: # green for loaded
      lineStatus.setStyleSheet("QLineEdit {background-color:green}")
      lineStatus.setText(current_status)
  
    elif current_status in ['NOT FOUND', 'NO', 'INVALID']: # red for not found
      lineStatus.setStyleSheet("QLineEdit {background-color:red}")
      lineStatus.setText(current_status)
        
  def open_analysis_window(self):
    self.analysis_window.show()
    self.update()    

  def configurationPushButtonClicked(self):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(self)
    self.mainLineEdit.setText(filename)
    self.update()

  def analysisPushButtonClicked(self):
    filename, _ = QtWidgets.QFileDialog.getOpenFileName(self)
    self.analysisLineEdit.setText(filename)
    self.update()

  def update(self):
    '''
    Function that updates the form
    '''
    logging.info("updating the form")
    self.update_form()
    logging.info("displaying the form")
    self.display_form() 
    self.cfg.update(self.main_cfg)
    self.cfg.update(self.analysis_cfg)
    
  
  def update_form(self):
  
    '''
    Function for updating the form
    '''
    logging.info("updating the analysis line")
    self.update_configuration_status(analysis = True)
    logging.info("updating the main line")
    self.update_configuration_status(analysis = False)
    
    # update the status box
    self.update_status()
    
  def update_configuration_status(self, analysis = False):
  
    '''
    Function for updating either the main or analysis configuration
    status
    
    Parameters 
    ----------
    analysis : bool
      Set to true to update the analysis, and false to update main
    
    '''
    logging.info("=== begining update of the status box ===")
  
    cfg = {}
    
    # if analysis is true set up to change analysis boxes
    if analysis:
      lineEdit = self.analysisLineEdit
    else:
      lineEdit = self.mainLineEdit
    
    filename = lineEdit.text() # text from line edit`
    
    #if the configuration file exists load it and set the status to loaded and green
    if os.path.isfile(filename):
      logging.info("Found the file specified")
      cfg = load_config(filename)
      
      # check that parameters required are in the config
      if not analysis:
        for item in ['main_directory', 'instrument_filename', 'ambient']:
          if item not in cfg:
            message = "Could not find {} in the configuration file".format(item)
            logging.info(message)
            cfg = {}
            flag = 'INVALID'
            break 
        else:
          flag = 'LOADED'
      else:
        flag = 'LOADED'

    else:
      logging.info("File is not found")
      flag = 'NOT FOUND'
      
    # update cfg
    if flag == 'LOADED' and analysis:
      self.analysis_cfg = cfg
      self.analysis_cfg_loaded = True
      
    elif flag == 'LOADED' and not analysis:
      self.main_cfg = cfg
      self.cfg_loaded = True
      if 'WIBSNEO.proto' in self.main_cfg['instrument_filename']:
        self.data_visible = False
        
      else:
        self.data_visible = True
      
      
    # update flags
    if analysis:
      self.analysis_state = flag
    else:
      self.main_state = flag
      
    logging.info("=== finished update of the status box ===")
    
  def update_status(self):
    logging.info("Updating status box")

    # check if the main directory is in the cfg and exists
    logging.info("Checing the main directory exists")
    if 'main_directory' in self.cfg and os.path.exists(self.cfg['main_directory']):
      main_directory = self.cfg['main_directory']
      
      logging.info("Checking the output directory exists")
      # check the output directory exists
      output_directory = os.path.join(main_directory, 'output')
      output_directory_exists = os.path.exists(output_directory)
      
      if not output_directory_exists:
        logging.info("Creating output directory")
        os.mkdir(output_directory)
      
      # if data.csv is in the output directory then set processed_data as true
      logging.info("Checking the output directory for files")
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
      
    logging.info("Filelist button")
    # conditions for filelist button to be enabled
    # 1) main proto to be loaded
    # 2) filelist doesn't already exists
    # 3) in laboratory mode
    
    if self.main_state == 'LOADED' and\
       not self.filelist_exists and\
       self.main_cfg['ambient'] == False:
         
         self.filelist_enabled = True
    else:
         self.filelist_enabled = False   

    logging.info("Data button")
    # conditions for data button to be enabled
    # 1) main proto to be loaded
    # 2) filelist already exists unless in ambient mode
    # 3) data doesn't already exist
    if self.main_state == 'LOADED' and not self.processed_data_exists:
      if self.main_cfg['ambient']:
        self.data_enabled = True
      elif not self.main_cfg['ambient'] and self.filelist_exists:
        self.data_enabled = True
      else:
        self.data_enabled = False
    else:
      self.data_enabled = False

    # conditions for results button to be enabled
    # 1) data exists or isn't needed
    # 2) analysis and main proto exist
    # 3) results don't already exist
    logging.info("Result button")
    if self.main_state == 'LOADED' and\
       self.analysis_state == 'LOADED' and\
      (self.processed_data_exists or self.data_visible == False) and\
      not self.results_exists:
        self.result_enabled = True
    else:
      self.result_enabled = False
    
    
    # update statuses
    if self.filelist_exists:
      self.filelist_state = 'YES'
    else:
      self.filelist_state = 'NO'

    if self.processed_data_exists:
      self.data_state = 'YES'

    else: 
      self.data_state = 'NO'

    if self.results_exists:
      self.result_state = 'YES'

    else:
      self.result_state = 'NO'    
    
    logging.info("Filelist exists : {}".format(self.filelist_exists))
    logging.info("Processed data exists : {}".format(self.processed_data_exists))
    logging.info("Results exists : {}".format(self.results_exists))

  def setup_configuration(self):
    
    if 'main_directory' in self.settings:
      self.mainLineEdit.setText(self.settings['main_directory'])
      self.update()
    if 'analysis_directory' in self.settings:
      self.analysisLineEdit.setText(self.settings['analysis_directory'])
      self.update()

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

    # update the configuration with the log filename
    cfg['log_filename'] = self.log_filename
    
    try:
      logging.info("Analysis button pressed: conducting analysis")
      analyse(cfg)
      
      
      logging.info("Attempting to open the results file")
      
      #open the file
      results_file = os.path.join(cfg['main_directory'], "output", "results", "results.csv")
      os.startfile(results_file)

      
      
      #subprocess.call(["xdg-open", )])
      self.update()

    except Exception as e:
      dialog = QtWidgets.QMessageBox()
      dialog.setText(str(e))
      dialog.exec_()


  def settings_filename(self):
    # gets the settings filename
    current_directory = os.path.abspath(__file__.replace('main.py', ''))
    filename = os.path.join(current_directory, 'settings.proto')
    
	# if it doesn't already exist then create it
    if not os.path.isfile(filename):
      self.create_settings_file(filename)
	
    return filename
	
  def create_settings_file(self, filename):
    f = open(filename, 'w')
    f.close()
	
	
	
	
	

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
    
    # on completion update the form
    if i == self.progress.maximum():
      self.update()

  def onProgress_labels(self, my_string):
    self.progress.setLabelText(my_string)

  def onError(self, error_string):
    self.progress.close()
    self.clean_data()
    self.msgBox.setText(error_string)
    self.msgBox.exec_()
    

  def create(self):

    try:

      # log creation
      logging.info("Attempting to create data")
    
      # show the error/warnings/progress dialog    
      cfg = {}
      cfg['log_filename'] = self.log_filename
      cfg.update(self.cfg)
      
      # loading instrument config
      logging.info("loading instrument coniguration")
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
      
      # start process of reading
      logging.info("Starting to read the files")
      self.readThread.start()

    except Exception as e:
      self.msgBox.setText("Error while creating data : {}".format(e))
      self.msgBox.exec_()

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
