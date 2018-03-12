# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UVLIF/gui/analysis_configuration.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1414, 895)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.addButton = QtWidgets.QPushButton(Dialog)
        self.addButton.setObjectName("addButton")
        self.gridLayout.addWidget(self.addButton, 4, 2, 1, 1)
        self.saveButton = QtWidgets.QPushButton(Dialog)
        self.saveButton.setObjectName("saveButton")
        self.gridLayout.addWidget(self.saveButton, 4, 0, 1, 1)
        self.removeButton = QtWidgets.QPushButton(Dialog)
        self.removeButton.setObjectName("removeButton")
        self.gridLayout.addWidget(self.removeButton, 4, 3, 1, 1)
        self.paramView = QtWidgets.QListView(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.paramView.sizePolicy().hasHeightForWidth())
        self.paramView.setSizePolicy(sizePolicy)
        self.paramView.setObjectName("paramView")
        self.gridLayout.addWidget(self.paramView, 0, 0, 1, 1)
        self.valueView = QtWidgets.QListView(Dialog)
        self.valueView.setObjectName("valueView")
        self.gridLayout.addWidget(self.valueView, 0, 2, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Configure Analysis"))
        self.addButton.setText(_translate("Dialog", "+"))
        self.saveButton.setText(_translate("Dialog", "Save"))
        self.removeButton.setText(_translate("Dialog", "-"))

