import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import UVLIF.gui.configuration_ui as main
from UVLIF.configuration.save_config import save_config_file
from UVLIF.configuration.load_config import load_config
from UVLIF.read.read import read_FT
import os

class configuration_window(QtWidgets.QMainWindow, main.Ui_MainWindow):
    
    def __init__(self, parent = None):
        super(configuration_window, self).__init__(parent)
        self.cfg = {}
        self.instrument_cfg = {}
        self.setupUi(self)
        self.mainDirectoryButton.clicked.connect(self.directory_browse_main)
        self.load_instrument_names()
        self.load_modes()
        self.load_table_view()
        self.saveButton.clicked.connect(self.save_configuration)
        self.ftButton.clicked.connect(self.load_ft)
        self.msgbox = QtWidgets.QMessageBox()

    def load_config(self, cfg):

       '''
       Either the window will be loaded when the user clicks new config, or when
       they click open config. When they click open config this function will be 
       used to load the configuration file that they select
       '''
       
       self.cfg = cfg

       if 'main_directory' in cfg:
         self.mainDirectoryLineEdit.setText(cfg['main_directory'])
       if self.all_in_cfg(['FT.minimum', 'FT.mean', 'FT.std', 'FT.maximum'], cfg):
         self.set_table(cfg['FT.minimum'], cfg['FT.mean'], cfg['FT.std'], cfg['FT.maximum'])
       if 'instrument_filename' in cfg:
         instrument = os.path.basename(cfg['instrument_filename']).strip('.proto')
         self.instrumentBox.setCurrentText(instrument)
       if 'ambient' in cfg:
         if cfg['ambient'] == True:
           self.modeBox.setCurrentText('Ambient')
         else:
           self.modeBox.setCurrentText('Laboratory')
         
         
       
    # consider moving this to a util file
    def all_in_cfg(self, parameter_list, cfg):
      for item in parameter_list:
        if item not in cfg.keys():
          return False
      else:
        return True
          
        
        
    

    def set_table(self, minimum, mean, std, maximum):
        for i, stat in enumerate([minimum, mean, std, maximum]):
          for j, value in enumerate(stat):
            self.ftModel.item(i, j).setText(str(value))

    def load_ft(self):

      try:

        # load the instrument configuration
        self.instrument_cfg.update(load_config(self.get_instrument_filename()))

        # get the filenames from the user
        self.cfg['filenames'], _ = QtWidgets.QFileDialog.getOpenFileNames()
        minimum, mean, std, maximum = read_FT(self.instrument_cfg, self.cfg['filenames'])

        # set the table view model data
        self.set_table(minimum, mean, std, maximum)

        self.cfg['FT.minimum'] = list(minimum)
        self.cfg['FT.mean'] = list(mean)
        self.cfg['FT.std'] = list(std)
        self.cfg['FT.maximum'] = list(maximum)     

      except Exception as e:
        # if something goes wrong let the user know
        self.msgbox.setText("Error loading FT : " + str(e))
        self.msgbox.exec()



    def directory_browse_main(self):
        message = "Please navigate to the main directory"
        directory = QtWidgets.QFileDialog.getExistingDirectory()

        if directory:
            self.mainDirectoryLineEdit.setText(directory)

    def load_instrument_names(self):

        # get the instrument directory (should be root/configuration/instrument)
        # which we can get to from the directory of the following file (root/gui)
        file_dir = os.path.dirname(__file__)
        instrument_dir = os.path.join(file_dir, '..', "configuration", "instrument")
        self.instrument_dir = os.path.abspath(instrument_dir) #convert the .. to actual directory

        # output each instrument to the instrument combobox
        for filename in os.listdir(instrument_dir):
          self.instrumentBox.addItem(filename.strip('.proto'))

    def load_modes(self):

      # function for loading the different modes available in the software into the
      # mode combo box
      for mode in ['Ambient', 'Laboratory']:
        self.modeBox.addItem(mode)

    def load_table_view(self):

      # function for loading the FT table, which will include the minimum, mean, std and max
      self.ftModel =  QtGui.QStandardItemModel() # create a new model
      self.ftView.setModel(self.ftModel) # set the tableview model to the model created

      # for each of the statistics add a row to the model
      statistics_list = ['minimum', 'mean', 'standard deviation', 'maximum']

      # for each stat populate the model with three items each a zero (one for each FL channel)
      for statistic in statistics_list:
        # create a new row with three items each "0" and non editible
        row = []
        for _ in range(3):
          item = QtGui.QStandardItem("0")
          item.setEditable(False)
          row.append(item)

        self.ftModel.appendRow(row)

      # set horizontal and vertical headers
      self.ftModel.setVerticalHeaderLabels(statistics_list) # add vertical headers
      self.ftModel.setHorizontalHeaderLabels(["FL1", "FL2", "FL3"])

      # expand to fit
      self.ftView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
      self.ftView.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

      # disable the selection
      self.ftView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
      self.ftView.setFocusPolicy(QtCore.Qt.NoFocus)

    def get_instrument_filename(self):
      return os.path.join(self.instrument_dir, self.instrumentBox.currentText() + '.proto')

    def save_configuration(self):
      try:

        #If main directory does not exist then display error otherwise store it in the config
        main_directory = os.path.abspath(self.mainDirectoryLineEdit.text())

        #In the case no text is entered the current directory is and displayed
        self.mainDirectoryLineEdit.setText(main_directory) 

        if not os.path.exists(main_directory) or main_directory == '':
          dialog = QtWidgets.QMessageBox()
          dialog.setText("The main directory entered does not exist.")
          dialog.exec_()
          return
        else:
          self.cfg['main_directory'] = main_directory

        # Output the selection from the instrument combobox to the config
        instrument_fname = self.get_instrument_filename()
        self.cfg['instrument_filename'] = instrument_fname


        # Output the selection from the mode combobox to the config
        if self.modeBox.currentText == 'Ambient':
          self.cfg['ambient'] = True
        else:
          self.cfg['ambient'] = False

        #Save this to file
        config_filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Configuration")
        save_config_file(self.cfg, config_filename)
        self.parent().update()


        self.close()
      except Exception as e:
        dialog = QtWidgets.QMessageBox()
        dialog.setText("There was an error in saving the configuration : {}".format(str(e)))
        dialog.exec_()
