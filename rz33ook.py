# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 14:46:03 2021

光调制器 RZ33-OOK

@author: lishu
"""
import math

import numpy as np
import matplotlib.pyplot as plt


#RZ33-OOK类
class rz33_ook:
    def __init__(self, E0, fc):
    #输入信号参数-幅度和频率
        self.E0 = E0
        self.fc = fc
        self.wc = 2*math.pi*fc
        return
    def E_in(self,t):#输入信号函数
        y = self.E0 * math.sin(self.wc*t)
        return y
    def E_out(self,t):#输出信号函数
        y = self.E_in(t) * math.cos((math.pi/2) * (math.sin(self.wc*t)))
        return y

#############################调试部分
##测试 常数的定义
#pi = math.pi
#i = complex(0,1)
#E = float(input("E="))
#f = float(input("f="))
#
##测试 采样点
#x = np.linspace(0,1,1400)
##生成调制器对象
#rz33ook = rz33_ook(E,f)
#y = np.zeros(len(x))
#for j in range(0,len(x)):
#    y[j] = rz33ook.E_out(x[j])
#    j += 1 
#print(y)
## 分辨率参数-dpi，画布大小参数-figsize
#plt.figure(dpi=300,figsize=(24,8))
## 改变文字大小参数-fontsize
#plt.xticks(fontsize=10)
#plt.plot(x,y)

