# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainUI.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from draw_pad import DrawPad
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, Form):
        Form.setObjectName("MainWindow")
        Form.resize(662, 531)
        # self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menu = QtWidgets.QMenu(self.menubar)
        #
        # self.menu_2 = QtWidgets.QMenu(self.menubar)

        self.widget = DrawPad(Form)
        self.widget.setGeometry(QtCore.QRect(0, 50, 291, 321))
        self.widget.setObjectName("widget")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(330, 120, 71, 21))
        self.pushButton.setObjectName("pushButton")

        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(420, 50, 211, 321))
        self.plainTextEdit.setStyleSheet("font: 250pt \"Agency FB\";")
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 170, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("MainWindow", "Made by Autumn"))
        self.pushButton.setText(_translate("MainWindow", "预   测"))
        self.pushButton_2.setText(_translate("MainWindow", "清   空"))
        # self.menubar.setTitle(_translate("MainWindow", "基于手写检测"))
        # self.menubar_2.setTitle(_translate("MainWindow", "基于图片检测"))
