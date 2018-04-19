from PyQt5 import QtWidgets, QtGui, QtCore
from UVLIF.gui.main import main_window
import sys
import os
import time

import ctypes


def run():

    myappid = 'SimonRuske.UVBAT.0.1' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    

    app = QtWidgets.QApplication(sys.argv)

    
    # set up icon directory
    cur_file = os.path.realpath(__file__) # fullname of current file
    cur_dir = os.path.split(cur_file)[0] # directory of current file
    icon_directory = os.path.join(cur_dir, "icons") # directory of the icons
    
    # load icons
    
    icon = QtGui.QIcon()
    
    icon.addFile(os.path.join(icon_directory, "16.png"), QtCore.QSize(16,16))    
    icon.addFile(os.path.join(icon_directory, "24.png"), QtCore.QSize(24,24))
    icon.addFile(os.path.join(icon_directory, "32.png"), QtCore.QSize(32,32))
    icon.addFile(os.path.join(icon_directory, "48.png"), QtCore.QSize(48,48))
    icon.addFile(os.path.join(icon_directory, "256.png"), QtCore.QSize(256,256))
    
    tray_icon = QtWidgets.QSystemTrayIcon(icon, app)

    # splash screen 
    splash_pix = QtGui.QPixmap(os.path.join(icon_directory, "splash.png"))
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)

    
    # Add progress bar
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
    main = main_window()
    main.show()
        
    splash.finish(main)


    
    sys.exit(app.exec_())
