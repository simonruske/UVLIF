# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UVLIF/gui/plot.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, plot_window):
        plot_window.setObjectName("plot_window")
        plot_window.setGeometry(QtCore.QRect(0, 0, 1354, 900))
        self.gridLayout = QtWidgets.QGridLayout(plot_window)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(plot_window)
        QtCore.QMetaObject.connectSlotsByName(plot_window)

    def retranslateUi(self, plot_window):
        _translate = QtCore.QCoreApplication.translate
        plot_window.setWindowTitle(_translate("Form", "Plot"))