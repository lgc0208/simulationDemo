"""
    File Name:          ui_ioset.py
    Author:             LIN Guocheng
    Version:            1.0.0
    Description:        界面样式类，设定了输入输出子窗口的样式
"""

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

        # 输入值 标签设置
        self.labelInput = QtWidgets.QLabel(IOset)
        self.labelInput.setGeometry(QtCore.QRect(60, 80, 120, 20))
        self.labelInput.setObjectName("inputValueLabel")

        # 输入值 输入框设置
        self.inputValue = QtWidgets.QLineEdit(IOset)
        self.inputValue.setGeometry(QtCore.QRect(210, 80, 120, 20))
        self.inputValue.setObjectName("inputValue")

        # E0 标签设置
        self.labelE0 = QtWidgets.QLabel(IOset)
        self.labelE0.setGeometry(QtCore.QRect(60, 110, 120, 20))
        self.labelE0.setObjectName("E0Label")

        # E0 输入框设置
        self.E0Value = QtWidgets.QLineEdit(IOset)
        self.E0Value.setGeometry(QtCore.QRect(210, 110, 120, 20))
        self.E0Value.setObjectName("E0Value")

        # Fc 标签设置
        self.labelFc = QtWidgets.QLabel(IOset)
        self.labelFc.setGeometry(QtCore.QRect(60, 140, 120, 20))
        self.labelFc.setObjectName("FcLabel")

        # Fc 输入框设置
        self.FcValue = QtWidgets.QLineEdit(IOset)
        self.FcValue.setGeometry(QtCore.QRect(210, 140, 120, 20))
        self.FcValue.setObjectName("FcValue")

        # 输出值 标签设置
        self.labelOnput = QtWidgets.QLabel(IOset)
        self.labelOnput.setGeometry(QtCore.QRect(60, 170, 120, 20))
        self.labelOnput.setObjectName("outputValueLabel")

        # 输出值 输出框设置
        self.outputValue = QtWidgets.QLabel(IOset)
        self.outputValue.setGeometry(QtCore.QRect(210, 170, 120, 20))
        self.outputValue.setFrameShape(QtWidgets.QFrame.Panel)
        self.outputValue.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.outputValue.setText("")
        self.outputValue.setObjectName("outputValue")

        # 按钮设置
        self.SetInput = QtWidgets.QPushButton(IOset)
        self.SetInput.setGeometry(QtCore.QRect(60, 200, 270, 30))
        self.SetInput.setObjectName("SetInput")

        self.retranslateUi(IOset)
        QtCore.QMetaObject.connectSlotsByName(IOset)

    # 设置文本名称
    def retranslateUi(self, IOset):
        _translate = QtCore.QCoreApplication.translate
        IOset.setWindowTitle(_translate("IOset", "输入输出设置界面"))
        self.labelInput.setText(_translate("IOset", "输入值"))
        self.labelOnput.setText(_translate("IOset", "输出值"))
        self.SetInput.setText(_translate("IOset", "确认输入值"))
        self.labelE0.setText(_translate("IOset", "输入E0值"))
        self.labelFc.setText(_translate("IOset", "输入Fc值"))
