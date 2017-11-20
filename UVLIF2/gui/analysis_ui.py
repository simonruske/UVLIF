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
        Dialog.resize(1414, 895)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.checkAllButton = QtWidgets.QPushButton(Dialog)
        self.checkAllButton.setObjectName("checkAllButton")
        self.gridLayout.addWidget(self.checkAllButton, 8, 2, 1, 1)
        self.editButton = QtWidgets.QPushButton(Dialog)
        self.editButton.setObjectName("editButton")
        self.gridLayout.addWidget(self.editButton, 8, 0, 1, 2)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 1, 0, 1, 3)
        self.uncheckAllButton = QtWidgets.QPushButton(Dialog)
        self.uncheckAllButton.setObjectName("uncheckAllButton")
        self.gridLayout.addWidget(self.uncheckAllButton, 12, 2, 1, 1)
        self.FTBox = QtWidgets.QCheckBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FTBox.sizePolicy().hasHeightForWidth())
        self.FTBox.setSizePolicy(sizePolicy)
        self.FTBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.FTBox.setAutoFillBackground(False)
        self.FTBox.setStyleSheet("")
        self.FTBox.setChecked(False)
        self.FTBox.setObjectName("FTBox")
        self.gridLayout.addWidget(self.FTBox, 4, 0, 1, 1)
        self.stdLabel = QtWidgets.QLabel(Dialog)
        self.stdLabel.setObjectName("stdLabel")
        self.gridLayout.addWidget(self.stdLabel, 4, 1, 1, 1)
        self.stdEdit = QtWidgets.QLineEdit(Dialog)
        self.stdEdit.setStyleSheet("")
        self.stdEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.stdEdit.setObjectName("stdEdit")
        self.gridLayout.addWidget(self.stdEdit, 4, 2, 1, 1)
        self.saveButton = QtWidgets.QPushButton(Dialog)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 12, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Analysis"))
        self.checkAllButton.setText(_translate("Dialog", "Check All"))
        self.editButton.setText(_translate("Dialog", "Edit"))
        self.uncheckAllButton.setText(_translate("Dialog", "Uncheck All"))
        self.FTBox.setText(_translate("Dialog", "Remove Non-Fluorescent"))
        self.stdLabel.setText(_translate("Dialog", "Number of Standard Deviations:"))
        self.stdEdit.setText(_translate("Dialog", "3"))
        self.saveButton.setText(_translate("Dialog", "Save"))

