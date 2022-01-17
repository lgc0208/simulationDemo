"""
    File Name:          nrzook.py
    Author:             LI Shuyuan
    Version:            0.0.1
    Description:        幅度调制器NRZ-OOK
    History:            
        1.  Date:           2021-10-8
            Author:         LIN Guocheng
            Modification:   删除测试部分，对平台进行适配
"""
import math
import random
'''
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
'''

#NRZ-OOK类
class nrz_ook:
    def __init__(self, E0, fc):
    #输入信号参数-幅度和频率
        self.E0 = E0
        self.fc = fc
        self.wc = 2*math.pi*fc
        return
    def E_in(self,t):#输入信号函数
        y = abs(self.E0) * ( math.cos(self.wc*t) + complex(0,1)*math.sin(self.wc*t))
        return y
    def a(self,t):#[TODO] a(t)含义？
        y = random.choice([-1,1]) #a(t)=±1
        return y
    def E_out(self,t):#输出信号函数
        y = complex(self.E_in(t) * math.cos((math.pi/4) * (self.a(t)-1) ) * ( pow(2,1/2) + complex(0,1)*pow(2,1/2)))
        return y
    
    