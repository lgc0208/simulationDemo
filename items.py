from PySide6.QtCore import (QPointF, Qt, QRectF)
from PySide6.QtGui import (QPainter, QPainterPath, QPen, QPixmap, QPolygonF, QImage, QFont)
from PySide6.QtWidgets import (QGraphicsItem, QGraphicsPolygonItem)
from nrzook import nrz_ook
from rz33ook import rz33_ook
from rz50ook import rz50_ook
from rz66ook import rz66_ook

class Items(QGraphicsPolygonItem):
    NRZOOK, RZ33OOk, RZ50OOK, RZ66OOK, TestItem = range(5)

    def __init__(self, item_type, contextMenu, parent=None, scene=None):
        super().__init__(parent, scene)
        
        self.__inputNum = 0     # 输入值
        self.__outputNum = 0    #输出值
        self.__E0 = 3   # 调制器信号幅度
        self.__fc = 4   # 调制器信号频率
        
        self.arrows = []        
        self.item_type = item_type
        self._my_context_menu = contextMenu

        path = QPainterPath()
        if self.item_type == self.NRZOOK:
            
#            self._my_polygon = QPolygonF([
#                    QPointF(-100/2, -100/2), QPointF(100/2, -100/2),
#                    QPointF(100/2, 100/2), QPointF(-100/2, 100/2),
#                    QPointF(-100/2, -100/2)])
            path = QPainterPath()
            timesFont = QFont("Times", 30)
            timesFont.setStyleStrategy(QFont.ForceOutline)
            path.addText(-65, 25, timesFont, "NRZ-OOK")
#            path.moveTo(-100/2, -100.0/2)
#            path.lineTo(100.0/2, -100.0/2)
#            path.lineTo(100.0/2, 100.0/2)
#            path.lineTo(-100.0/2, 100.0/2)
            path.closeSubpath()
            path.setFillRule(Qt.WindingFill)
            self._my_polygon = path.toFillPolygon()
    
            #self.img = QImage(':/images/background1.png')
    
        elif self.item_type == self.TestItem:
            path = QPainterPath()
            timesFont = QFont("Times", 30)
            timesFont.setStyleStrategy(QFont.ForceOutline)
            path.addText(-65, 25, timesFont, "乘方器")
            path.closeSubpath()
            path.setFillRule(Qt.WindingFill)
            self._my_polygon = path.toFillPolygon()
            #self.img = QImage(':/images/power.png')
        
        elif self.item_type == self.RZ33OOk:
            path = QPainterPath()
            timesFont = QFont("Times", 30)
            timesFont.setStyleStrategy(QFont.ForceOutline)
            path.addText(-65, 25, timesFont, "RZ33-OOk")
            path.closeSubpath()
            path.setFillRule(Qt.WindingFill)
            self._my_polygon = path.toFillPolygon()
            
        elif self.item_type == self.RZ50OOK:
            path = QPainterPath()
            timesFont = QFont("Times", 30)
            timesFont.setStyleStrategy(QFont.ForceOutline)
            path.addText(-65, 25, timesFont, "RZ50-OOK")
            path.closeSubpath()
            path.setFillRule(Qt.WindingFill)
            self._my_polygon = path.toFillPolygon()
            
        elif self.item_type == self.RZ66OOK:
            path = QPainterPath()
            timesFont = QFont("Times", 30)
            timesFont.setStyleStrategy(QFont.ForceOutline)
            path.addText(-65, 25, timesFont, "RZ66-OOK")
            path.closeSubpath()
            path.setFillRule(Qt.WindingFill)
            self._my_polygon = path.toFillPolygon()
            #self.img = QImage(':/images/power.png')
        else:
            
            self._my_polygon = QPolygonF([
                    QPointF(-120/2, -80/2), QPointF(-70/2, 80/2),
                    QPointF(120/2, 80/2), QPointF(70/2, -80/2),
                    QPointF(-120/2, -80/2)])
            
            #self.img = QImage(':/images/background1.png')
        #self.setPolygon(self.img)
        #self.setImg(self.img)
        self.setPolygon(self._my_polygon)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
    
    # 删除单个连接线
    def remove_arrow(self, arrow):
        try:
            self.arrows.remove(arrow)
        except ValueError:
            pass

    # 删除多个连接线
    def remove_arrows(self):
        for arrow in self.arrows[:]:
            arrow.start_item().remove_arrow(arrow)
            arrow.end_item().remove_arrow(arrow)
            self.scene().removeItem(arrow)

    # 添加连接线
    def add_arrow(self, arrow):
        self.arrows.append(arrow)

    # 图标
    
    def image(self):
        
        pixmap = QPixmap(250, 250)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.black, 8))
        painter.translate(125, 125)
        painter.drawPolyline(self._my_polygon)
        #rect = QRectF(200,100,self.img.width()/2,self.img.height()/2)
        #painter.drawImage(rect, self.img)
        #pixmap = QPixmap(self.img)
        return pixmap
        
        #img = self.getImgUrl()
        #return img
    
    # 菜单栏
    def contextMenuEvent(self, event):
        self.scene().clearSelection()
        self.setSelected(True)
        self._my_context_menu.exec(event.screenPos())
        
    # 当项目被选中时发出信号
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            for arrow in self.arrows:
                arrow.updatePosition()

        return value
    

    
    # 计算结果
    def calculateResult(self, itemType, inputNum):
        if(itemType == self.TestItem):
            outputNum = inputNum * inputNum
            self.__inputNum = inputNum
            self.__outputNum = outputNum
            print("TestItem:")
            print("inputNum = ", self.__inputNum)
            print("outputNum = ", self.__outputNum)            
        elif(itemType == self.NRZOOK):
            nrz = nrz_ook(self.getE0(), self.getfc())
            outputNum = nrz.E_out(inputNum)
            self.__inputNum = inputNum
            self.__outputNum =  outputNum
            print("NRZOOK:")
            print("inputNum = ", self.__inputNum)
            print("outputNum = ", outputNum.real, "+j", outputNum.imag)
        elif(itemType == self.RZ33OOk):
            rz33 = rz33_ook(self.getE0(), self.getfc())
            outputNum = rz33.E_out(inputNum)
            self.__inputNum = inputNum
            self.__outputNum =  outputNum
            print("RZ33OOk:")
            print("inputNum = ", self.__inputNum)
            print("outputNum = ", outputNum.real, "+j", outputNum.imag)
        elif(itemType == self.RZ50OOK):
            rz50 = rz50_ook(self.getE0(), self.getfc())
            outputNum = rz50.E_out(inputNum)
            self.__inputNum = inputNum
            self.__outputNum =  outputNum
            print("RZ50OOK:")
            print("inputNum = ", self.__inputNum)
            print("outputNum = ", outputNum.real, "+j", outputNum.imag)
        elif(itemType == self.RZ66OOK):
            rz66 = rz66_ook(self.getE0(), self.getfc())
            outputNum = rz66.E_out(inputNum)
            self.__inputNum = inputNum
            self.__outputNum =  outputNum
            print("RZ66OOK:")
            print("inputNum = ", self.__inputNum)
            print("outputNum = ", outputNum.real, "+j", outputNum.imag)
        return outputNum            
        
    
##################SET-GET METHOD##############################
    # 设置输入值
    def setInputNum(self, inputNum):
        self.__inputNum = inputNum
    
    # 得到输入值
    def getInputNum(self):
        return self.__inputNum
    
    # 设置输出值
    def setOutputNum(self, outputNum):
        self.__outputNum = outputNum
        
    # 得到输出值
    def getOutputNum(self):
        return self.__outputNum
    
    # 设置调制器幅度
    def setE0(self, E0):
        self.__E0 = E0
    
    # 得到调制器幅度
    def getE0(self):
        return self.__E0
    
    # 设置调制器频率
    def setfc(self, fc):
        self.__fc = fc
        
    # 得到调制器频率
    def getfc(self):
        return self.__fc
    
    # 设置输入值
    def setImg(self, imgUrl):
        self.imgUrl = imgUrl
    
    # 得到输入值
    def getImg(self):
        return self.imgUrl
##################SET-GET METHOD##############################