from PyQt5 import QtWidgets, QtGui, QtCore
from UVLIF.gui.main import main_window
import sys, os, time
from datetime import datetime

import logging
import ctypes #for windows to show the icon in task bar

def run():

    '''
    Function to run the gui
    
    '''
    
    # start the log file
    cur_dir = os.path.dirname(__file__) # directory of current file
    sys.stderr = open(os.path.join(cur_dir, "gui.log"), "a")
    sys.stdout = open(os.path.join(cur_dir, "gui.log"), "a")
    log_filename = os.path.join(cur_dir, "gui.log")
    
    logging.basicConfig(filename = log_filename, level = logging.DEBUG)
    logging.info('New session : {}'.format(str(datetime.now())))

    # Set application id in windows
    logging.info("Setting application id for windows")
    myappid = 'SimonRuske.UVBAT.0.1' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    

    # starting application
    logging.info("Starting Application")
    app = QtWidgets.QApplication(sys.argv)

    # set up icon directory
    cur_file = os.path.realpath(__file__) # fullname of current file
    cur_dir = os.path.split(cur_file)[0] # directory of current file
    icon_directory = os.path.join(cur_dir, "icons") # directory of the icons
    
    # load icons
    logging.info("Loading Application icons")   
    icon = QtGui.QIcon()
    
    icon.addFile(os.path.join(icon_directory, "16.png"), QtCore.QSize(16,16))    
    icon.addFile(os.path.join(icon_directory, "24.png"), QtCore.QSize(24,24))
    icon.addFile(os.path.join(icon_directory, "32.png"), QtCore.QSize(32,32))
    icon.addFile(os.path.join(icon_directory, "48.png"), QtCore.QSize(48,48))
    icon.addFile(os.path.join(icon_directory, "256.png"), QtCore.QSize(256,256))
    
    tray_icon = QtWidgets.QSystemTrayIcon(icon, app)

    # splash screen 
    logging.info("Displaying Splash Screen")
    splash_pix = QtGui.QPixmap(os.path.join(icon_directory, "splash.png"))
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)

    # Add progress bar
    logging.info("Displaying progress bar on splash screen")
    progressBar = QtWidgets.QProgressBar(splash)
    progressBar.setMaximum(10)
    progressBar.setGeometry(0,0, splash_pix.width()+ 75, 20)
    splash.show()
    
    
    for i in range(1, 11):
      progressBar.setValue(i)
      t = time.time()
      while time.time() < t + 0.1:
        app.processEvents()
    
    time.sleep(1)
    app.setWindowIcon(icon)
    main = main_window(log_filename = log_filename)
    main.show()
        
    splash.finish(main)

    sys.exit(app.exec_())