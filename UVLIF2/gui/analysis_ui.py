# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UVLIF2/gui/analysis.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(756, 505)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.uncheckAllButton = QtWidgets.QPushButton(Dialog)
        self.uncheckAllButton.setObjectName("uncheckAllButton")
        self.gridLayout.addWidget(self.uncheckAllButton, 2, 0, 1, 1)
        self.checkAllButton = QtWidgets.QPushButton(Dialog)
        self.checkAllButton.setObjectName("checkAllButton")
        self.gridLayout.addWidget(self.checkAllButton, 1, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
        self.saveButton = QtWidgets.QPushButton(Dialog)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Analysis"))
        self.uncheckAllButton.setText(_translate("Dialog", "Uncheck All"))
        self.checkAllButton.setText(_translate("Dialog", "Check All"))
        self.saveButton.setText(_translate("Dialog", "Save"))

