# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ioset.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_IOset(object):
    def setupUi(self, IOset):
        if not IOset.objectName():
            IOset.setObjectName(u"IOset")
        IOset.resize(400, 300)
        self.label = QLabel(IOset)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 80, 121, 16))
        self.label_2 = QLabel(IOset)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(60, 160, 101, 16))
        self.outputValue = QLabel(IOset)
        self.outputValue.setObjectName(u"outputValue")
        self.outputValue.setGeometry(QRect(210, 160, 111, 16))
        self.outputValue.setFrameShape(QFrame.Panel)
        self.outputValue.setFrameShadow(QFrame.Sunken)
        self.inputValue = QLineEdit(IOset)
        self.inputValue.setObjectName(u"inputValue")
        self.inputValue.setGeometry(QRect(210, 80, 113, 23))
        self.SetInput = QPushButton(IOset)
        self.SetInput.setObjectName(u"SetInput")
        self.SetInput.setGeometry(QRect(70, 230, 251, 24))

        self.retranslateUi(IOset)

        QMetaObject.connectSlotsByName(IOset)
    # setupUi

    def retranslateUi(self, IOset):
        IOset.setWindowTitle(QCoreApplication.translate("IOset", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("IOset", u"Input Value", None))
        self.label_2.setText(QCoreApplication.translate("IOset", u"Output Value", None))
        self.outputValue.setText("")
        self.SetInput.setText(QCoreApplication.translate("IOset", u"Set Input", None))
    # retranslateUi

