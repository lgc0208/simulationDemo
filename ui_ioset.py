# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ioset.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_IOset(object):
    def setupUi(self, IOset):
        IOset.setObjectName("IOset")
        IOset.resize(400, 300)
        self.label = QtWidgets.QLabel(IOset)
        self.label.setGeometry(QtCore.QRect(60, 80, 121, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(IOset)
        self.label_2.setGeometry(QtCore.QRect(60, 160, 101, 16))
        self.label_2.setObjectName("label_2")
        self.outputValue = QtWidgets.QLabel(IOset)
        self.outputValue.setGeometry(QtCore.QRect(210, 160, 111, 16))
        self.outputValue.setFrameShape(QtWidgets.QFrame.Panel)
        self.outputValue.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.outputValue.setText("")
        self.outputValue.setObjectName("outputValue")
        self.inputValue = QtWidgets.QLineEdit(IOset)
        self.inputValue.setGeometry(QtCore.QRect(210, 80, 113, 23))
        self.inputValue.setObjectName("inputValue")
        self.SetInput = QtWidgets.QPushButton(IOset)
        self.SetInput.setGeometry(QtCore.QRect(70, 230, 251, 24))
        self.SetInput.setObjectName("SetInput")

        self.retranslateUi(IOset)
        QtCore.QMetaObject.connectSlotsByName(IOset)

    def retranslateUi(self, IOset):
        _translate = QtCore.QCoreApplication.translate
        IOset.setWindowTitle(_translate("IOset", "输入输出设置界面"))
        self.label.setText(_translate("IOset", "Input Value"))
        self.label_2.setText(_translate("IOset", "Output Value"))
        self.SetInput.setText(_translate("IOset", "Set Input"))

