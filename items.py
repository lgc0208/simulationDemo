from PySide6.QtCore import (QPointF, Qt)
from PySide6.QtGui import (QPainter, QPainterPath, QPen, QPixmap, QPolygonF)
from PySide6.QtWidgets import (QGraphicsItem, QGraphicsPolygonItem)
from nrzook import nrz_ook

class Items(QGraphicsPolygonItem):
    NRZOOK, TestItem = range(2)

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
            self._my_polygon = QPolygonF([
                    QPointF(-100/2, -100/2), QPointF(100/2, -100/2),
                    QPointF(100/2, 100/2), QPointF(-100/2, 100/2),
                    QPointF(-100/2, -100/2)])
        elif self.item_type == self.TestItem:
            self._my_polygon = QPolygonF([
                    QPointF(-100/2, 0), QPointF(0, 100/2),
                    QPointF(100/2, 0), QPointF(0, -100/2),
                    QPointF(-100/2, 0)])
        else:
            self._my_polygon = QPolygonF([
                    QPointF(-120/2, -80/2), QPointF(-70/2, 80/2),
                    QPointF(120/2, 80/2), QPointF(70/2, -80/2),
                    QPointF(-120/2, -80/2)])

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
        return pixmap

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
            print("outputNum = ", outputNum[0], "+j", outputNum[1])
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
##################SET-GET METHOD##############################