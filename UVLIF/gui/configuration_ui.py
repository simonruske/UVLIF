# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UVLIF/gui/configuration.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1110, 712)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.modeBox = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modeBox.sizePolicy().hasHeightForWidth())
        self.modeBox.setSizePolicy(sizePolicy)
        self.modeBox.setObjectName("modeBox")
        self.gridLayout.addWidget(self.modeBox, 11, 1, 1, 2)
        self.instrumentBox = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.instrumentBox.sizePolicy().hasHeightForWidth())
        self.instrumentBox.setSizePolicy(sizePolicy)
        self.instrumentBox.setObjectName("instrumentBox")
        self.gridLayout.addWidget(self.instrumentBox, 3, 1, 1, 1)
        self.mainDirectoryButton = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainDirectoryButton.sizePolicy().hasHeightForWidth())
        self.mainDirectoryButton.setSizePolicy(sizePolicy)
        self.mainDirectoryButton.setObjectName("mainDirectoryButton")
        self.gridLayout.addWidget(self.mainDirectoryButton, 1, 2, 1, 1)
        self.saveButton = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 12, 0, 1, 3)
        self.mainDirectoryLineEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainDirectoryLineEdit.sizePolicy().hasHeightForWidth())
        self.mainDirectoryLineEdit.setSizePolicy(sizePolicy)
        self.mainDirectoryLineEdit.setObjectName("mainDirectoryLineEdit")
        self.gridLayout.addWidget(self.mainDirectoryLineEdit, 1, 1, 1, 1)
        self.instrumentLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.instrumentLabel.sizePolicy().hasHeightForWidth())
        self.instrumentLabel.setSizePolicy(sizePolicy)
        self.instrumentLabel.setObjectName("instrumentLabel")
        self.gridLayout.addWidget(self.instrumentLabel, 3, 0, 1, 1)
        self.instrumentButton = QtWidgets.QPushButton(self.groupBox)
        self.instrumentButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.instrumentButton.sizePolicy().hasHeightForWidth())
        self.instrumentButton.setSizePolicy(sizePolicy)
        self.instrumentButton.setObjectName("instrumentButton")
        self.gridLayout.addWidget(self.instrumentButton, 3, 2, 1, 1)
        self.mainDirectoryLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainDirectoryLabel.sizePolicy().hasHeightForWidth())
        self.mainDirectoryLabel.setSizePolicy(sizePolicy)
        self.mainDirectoryLabel.setObjectName("mainDirectoryLabel")
        self.gridLayout.addWidget(self.mainDirectoryLabel, 1, 0, 1, 1)
        self.modeLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modeLabel.sizePolicy().hasHeightForWidth())
        self.modeLabel.setSizePolicy(sizePolicy)
        self.modeLabel.setObjectName("modeLabel")
        self.gridLayout.addWidget(self.modeLabel, 11, 0, 1, 1)
        self.ftView = QtWidgets.QTableView(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ftView.sizePolicy().hasHeightForWidth())
        self.ftView.setSizePolicy(sizePolicy)
        self.ftView.setObjectName("ftView")
        self.gridLayout.addWidget(self.ftView, 4, 1, 1, 1)
        self.ftLabel = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ftLabel.sizePolicy().hasHeightForWidth())
        self.ftLabel.setSizePolicy(sizePolicy)
        self.ftLabel.setObjectName("ftLabel")
        self.gridLayout.addWidget(self.ftLabel, 4, 0, 1, 1)
        self.ftButton = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ftButton.sizePolicy().hasHeightForWidth())
        self.ftButton.setSizePolicy(sizePolicy)
        self.ftButton.setObjectName("ftButton")
        self.gridLayout.addWidget(self.ftButton, 4, 2, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionNew_Configuration = QtWidgets.QAction(MainWindow)
        self.actionNew_Configuration.setObjectName("actionNew_Configuration")
        self.actionLoad_Configuration = QtWidgets.QAction(MainWindow)
        self.actionLoad_Configuration.setObjectName("actionLoad_Configuration")
        self.actionSave_Configuration = QtWidgets.QAction(MainWindow)
        self.actionSave_Configuration.setObjectName("actionSave_Configuration")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "New Configuration ..."))
        self.groupBox.setTitle(_translate("MainWindow", "Configuration"))
        self.mainDirectoryButton.setText(_translate("MainWindow", "..."))
        self.saveButton.setText(_translate("MainWindow", "Save Configuration"))
        self.instrumentLabel.setText(_translate("MainWindow", "Instrument :"))
        self.instrumentButton.setText(_translate("MainWindow", "..."))
        self.mainDirectoryLabel.setText(_translate("MainWindow", "Main Directory:"))
        self.modeLabel.setText(_translate("MainWindow", "Mode:"))
        self.ftLabel.setText(_translate("MainWindow", "Forced Trigger:"))
        self.ftButton.setText(_translate("MainWindow", "Load"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionNew_Configuration.setText(_translate("MainWindow", "New Configuration"))
        self.actionLoad_Configuration.setText(_translate("MainWindow", "Load Configuration"))
        self.actionSave_Configuration.setText(_translate("MainWindow", "Save Configuration"))

