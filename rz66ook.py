"""
    File Name:          rz66ook.py
    Author:             LI Shuyuan
    Version:            0.0.1
    Description:        光调制器RZ66-OOK
    History:            
        1.  Date:           2021-10-8
            Author:         LIN Guocheng
            Modification:   删除测试部分，对平台进行适配
"""
import math

import numpy as np
import matplotlib.pyplot as plt


#RZ66-OOK类
class rz66_ook:
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
        y = complex(0,1) * self.E_in(t) * math.cos((math.pi/2) * (math.sin(self.wc*t)))
#        y1 = y.real
#        y2 = y.imag
#        return y1,y2
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
#rz60ook = rz60_ook(E,f)
#y1 = np.zeros(len(x))
#y2 = np.zeros(len(x))
#for j in range(0,len(x)):
#    y1[j],y2[j] = rz60ook.E_out(x[j])
#    j += 1 
#print(y1,y2)
## 分辨率参数-dpi，画布大小参数-figsize
#plt.figure(dpi=300,figsize=(24,8))
## 改变文字大小参数-fontsize
#plt.xticks(fontsize=10)
#plt.plot(x,y1)
#plt.plot(x,y2)
