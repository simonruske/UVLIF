import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import UVLIF.gui.configuration_ui as main
from UVLIF.configuration.save_config import save_config_file
import os

'''
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        dialog = QtWidgets.QFileDialog(self, options = options)
        size_object = QtWidgets.QDesktopWidget().screenGeometry(-1)
        dialog.setFileMode(2)
        dialog.exec()
        directory = dialog.directory()
'''

class configuration_window(QtWidgets.QMainWindow, main.Ui_MainWindow):
    
    def __init__(self, parent = None):
        super(configuration_window, self).__init__(parent)
        self.cfg = {}
        self.setupUi(self)
        self.mainDirectoryButton.clicked.connect(self.directory_browse_main)
        self.load_instrument_names()
        self.saveButton.clicked.connect(self.save_configuration)

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
          self.comboBox.addItem(filename.strip('.proto'))

    def save_configuration(self):
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
        instrument_fname = os.path.join(self.instrument_dir, self.comboBox.currentText() + '.proto')
        self.cfg['instrument_filename'] = instrument_fname

        #Output whether ambient is selected
        self.cfg['ambient'] = self.checkBox.isChecked()

        #Output whether FT is selected
        self.cfg['FT'] = self.checkBox_2.isChecked()

        #Ouput FT_character
        self.cfg['FT_char'] = self.lineEdit_3.text()

        #Save this to file
        config_filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Configuration")
        save_config_file(self.cfg, config_filename)
        self.close()



        

            

        


        


