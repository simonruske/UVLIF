# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UVLIF/gui/main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1414, 895)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.labelMain = QtWidgets.QLabel(self.groupBox)
        self.labelMain.setObjectName("labelMain")
        self.gridLayout.addWidget(self.labelMain, 0, 0, 1, 1)
        self.mainLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.mainLineEdit.setObjectName("mainLineEdit")
        self.gridLayout.addWidget(self.mainLineEdit, 0, 1, 1, 1)
        self.configurationPushButton = QtWidgets.QPushButton(self.groupBox)
        self.configurationPushButton.setObjectName("configurationPushButton")
        self.gridLayout.addWidget(self.configurationPushButton, 0, 2, 1, 1)
        self.lineEditMainStatus = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditMainStatus.sizePolicy().hasHeightForWidth())
        self.lineEditMainStatus.setSizePolicy(sizePolicy)
        self.lineEditMainStatus.setStyleSheet("QLineEdit{background-color:red}")
        self.lineEditMainStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditMainStatus.setReadOnly(True)
        self.lineEditMainStatus.setObjectName("lineEditMainStatus")
        self.gridLayout.addWidget(self.lineEditMainStatus, 0, 3, 1, 1)
        self.labelAnalysis = QtWidgets.QLabel(self.groupBox)
        self.labelAnalysis.setObjectName("labelAnalysis")
        self.gridLayout.addWidget(self.labelAnalysis, 1, 0, 1, 1)
        self.analysisLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.analysisLineEdit.setObjectName("analysisLineEdit")
        self.gridLayout.addWidget(self.analysisLineEdit, 1, 1, 1, 1)
        self.analysisPushButton = QtWidgets.QPushButton(self.groupBox)
        self.analysisPushButton.setObjectName("analysisPushButton")
        self.gridLayout.addWidget(self.analysisPushButton, 1, 2, 1, 1)
        self.lineEditAnalysisStatus = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditAnalysisStatus.sizePolicy().hasHeightForWidth())
        self.lineEditAnalysisStatus.setSizePolicy(sizePolicy)
        self.lineEditAnalysisStatus.setStyleSheet("QLineEdit{background-color:red}")
        self.lineEditAnalysisStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEditAnalysisStatus.setReadOnly(True)
        self.lineEditAnalysisStatus.setObjectName("lineEditAnalysisStatus")
        self.gridLayout.addWidget(self.lineEditAnalysisStatus, 1, 3, 1, 1)
        self.verticalLayout.addWidget(self.groupBox, 0, QtCore.Qt.AlignTop)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dataStatus = QtWidgets.QLineEdit(self.groupBox_2)
        self.dataStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.dataStatus.setReadOnly(True)
        self.dataStatus.setObjectName("dataStatus")
        self.gridLayout_2.addWidget(self.dataStatus, 1, 1, 1, 1)
        self.analyseButton = QtWidgets.QPushButton(self.groupBox_2)
        self.analyseButton.setObjectName("analyseButton")
        self.gridLayout_2.addWidget(self.analyseButton, 2, 2, 1, 1)
        self.createButton = QtWidgets.QPushButton(self.groupBox_2)
        self.createButton.setObjectName("createButton")
        self.gridLayout_2.addWidget(self.createButton, 1, 2, 1, 1)
        self.resultsLabel = QtWidgets.QLabel(self.groupBox_2)
        self.resultsLabel.setObjectName("resultsLabel")
        self.gridLayout_2.addWidget(self.resultsLabel, 2, 0, 1, 1)
        self.resultsStatus = QtWidgets.QLineEdit(self.groupBox_2)
        self.resultsStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.resultsStatus.setReadOnly(True)
        self.resultsStatus.setObjectName("resultsStatus")
        self.gridLayout_2.addWidget(self.resultsStatus, 2, 1, 1, 1)
        self.dataLabel = QtWidgets.QLabel(self.groupBox_2)
        self.dataLabel.setObjectName("dataLabel")
        self.gridLayout_2.addWidget(self.dataLabel, 1, 0, 1, 1)
        self.filelistLabel = QtWidgets.QLabel(self.groupBox_2)
        self.filelistLabel.setObjectName("filelistLabel")
        self.gridLayout_2.addWidget(self.filelistLabel, 0, 0, 1, 1)
        self.fileStatus = QtWidgets.QLineEdit(self.groupBox_2)
        self.fileStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.fileStatus.setReadOnly(True)
        self.fileStatus.setObjectName("fileStatus")
        self.gridLayout_2.addWidget(self.fileStatus, 0, 1, 1, 1)
        self.fileButton = QtWidgets.QPushButton(self.groupBox_2)
        self.fileButton.setObjectName("fileButton")
        self.gridLayout_2.addWidget(self.fileButton, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2, 0, QtCore.Qt.AlignTop)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1414, 19))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuConfiguration = QtWidgets.QMenu(self.menubar)
        self.menuConfiguration.setObjectName("menuConfiguration")
        self.menuAnalysis = QtWidgets.QMenu(self.menubar)
        self.menuAnalysis.setObjectName("menuAnalysis")
        self.menuClean = QtWidgets.QMenu(self.menubar)
        self.menuClean.setObjectName("menuClean")
        MainWindow.setMenuBar(self.menubar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionNewConfiguration = QtWidgets.QAction(MainWindow)
        self.actionNewConfiguration.setObjectName("actionNewConfiguration")
        self.actionNewAnalysis = QtWidgets.QAction(MainWindow)
        self.actionNewAnalysis.setObjectName("actionNewAnalysis")
        self.actionCleanAll = QtWidgets.QAction(MainWindow)
        self.actionCleanAll.setObjectName("actionCleanAll")
        self.actionCleanResults = QtWidgets.QAction(MainWindow)
        self.actionCleanResults.setObjectName("actionCleanResults")
        self.actionCleanProcessedData = QtWidgets.QAction(MainWindow)
        self.actionCleanProcessedData.setObjectName("actionCleanProcessedData")
        self.actionCleanFilelist = QtWidgets.QAction(MainWindow)
        self.actionCleanFilelist.setObjectName("actionCleanFilelist")
        self.actionEditConfiguration = QtWidgets.QAction(MainWindow)
        self.actionEditConfiguration.setObjectName("actionEditConfiguration")
        self.menuFile.addAction(self.actionExit)
        self.menuConfiguration.addAction(self.actionNewConfiguration)
        self.menuConfiguration.addAction(self.actionEditConfiguration)
        self.menuAnalysis.addAction(self.actionNewAnalysis)
        self.menuClean.addAction(self.actionCleanAll)
        self.menuClean.addAction(self.actionCleanFilelist)
        self.menuClean.addAction(self.actionCleanProcessedData)
        self.menuClean.addAction(self.actionCleanResults)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConfiguration.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menubar.addAction(self.menuClean.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "UVLIF"))
        self.groupBox.setTitle(_translate("MainWindow", "Configuration"))
        self.labelMain.setText(_translate("MainWindow", "Main:"))
        self.configurationPushButton.setText(_translate("MainWindow", "..."))
        self.lineEditMainStatus.setText(_translate("MainWindow", "NOT LOADED"))
        self.labelAnalysis.setText(_translate("MainWindow", "Analysis:"))
        self.analysisPushButton.setText(_translate("MainWindow", "..."))
        self.lineEditAnalysisStatus.setText(_translate("MainWindow", "NOT LOADED"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Status"))
        self.analyseButton.setText(_translate("MainWindow", "Analyse"))
        self.createButton.setText(_translate("MainWindow", "Create"))
        self.resultsLabel.setText(_translate("MainWindow", "Results Created:"))
        self.dataLabel.setText(_translate("MainWindow", "Processsed Data Created:"))
        self.filelistLabel.setText(_translate("MainWindow", "Filelist Created: "))
        self.fileButton.setText(_translate("MainWindow", "Create Filelist"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuConfiguration.setTitle(_translate("MainWindow", "Configuration"))
        self.menuAnalysis.setTitle(_translate("MainWindow", "Analysis"))
        self.menuClean.setTitle(_translate("MainWindow", "Clean"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionNewConfiguration.setText(_translate("MainWindow", "New Configuration"))
        self.actionNewAnalysis.setText(_translate("MainWindow", "New Analysis"))
        self.actionCleanAll.setText(_translate("MainWindow", "Clean All"))
        self.actionCleanResults.setText(_translate("MainWindow", "Clean Results"))
        self.actionCleanProcessedData.setText(_translate("MainWindow", "Clean Data"))
        self.actionCleanFilelist.setText(_translate("MainWindow", "Clean Filelist"))
        self.actionEditConfiguration.setText(_translate("MainWindow", "Edit Configuration"))

