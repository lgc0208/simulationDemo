"""
    File Name:          ioset.py
    Author:             LIN Guocheng
    Version:            0.0.1
    Description:        输入输出子窗口
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal

from ui_ioset import Ui_IOset

class IOSet(QWidget):
    
    new_input_value = Signal(complex, float, float)
    
    def __init__(self):
        super(IOSet, self).__init__()
        self.ui = Ui_IOset()
        self.ui.setupUi(self)
        self.ui.SetInput.clicked.connect(self.on_SetInput_clicked)

        
    def on_SetInput_clicked(self):
        inputValueStr = self.ui.inputValue.text()
        E0ValueStr = self.ui.E0Value.text()
        fcValueStr = self.ui.FcValue.text()
        
        self.new_input_value.emit(float(inputValueStr), 
                                  float(E0ValueStr), 
                                  float(fcValueStr))