from PyQt5 import QtWidgets
from UVLIF2.gui.main import main_window
import sys

def run():  
    app = QtWidgets.QApplication(sys.argv)
    main = main_window()
    main.show()
    sys.exit(app.exec_())
