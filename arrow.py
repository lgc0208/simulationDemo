# -*- coding: utf-8 -*-
import math

from PySide6.QtCore import (QLineF, QPointF, QRectF, QSizeF, Qt)
from PySide6.QtGui import (QPen, QPolygonF)
from PySide6.QtWidgets import (QGraphicsItem, QGraphicsLineItem)

class Arrow(QGraphicsLineItem):
    def __init__(self, startItem, endItem, parent=None, scene=None):
        super().__init__(parent, scene)

        self._arrow_head = QPolygonF()

        self._my_start_item = startItem
        self._my_end_item = endItem
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self._my_color = Qt.black
        self.setPen(QPen(self._my_color, 2, Qt.SolidLine,
                Qt.RoundCap, Qt.RoundJoin))

    # 设置颜色
    def set_color(self, color):
        self._my_color = color

    # 返回起始项
    def start_item(self):
        return self._my_start_item

    # 返回终止项
    def end_item(self):
        return self._my_end_item

    # 检测碰撞，图形场景使用边界矩形来知道场景的哪些区域需要更新
    def boundingRect(self):
        extra = (self.pen().width() + 20) / 2.0
        p1 = self.line().p1()
        p2 = self.line().p2()
        rect = QRectF(p1, QSizeF(p2.x() - p1.x(), p2.y() - p1.y()))
        return rect.normalized().adjusted(-extra, -extra, extra, extra)

    # 返回一个带有箭头和路径的连接线
    def shape(self):
        path = super(Arrow, self).shape()
        path.addPolygon(self._arrow_head)
        return path

    # 更新箭头位置
    def update_position(self):
        start = self.mapFromItem(self._my_start_item, 0, 0)
        end = self.mapFromItem(self._my_end_item, 0, 0)
        self.setLine(QLineF(start, end))

    # 绘制函数
    def paint(self, painter, option, widget=None):
        if (self._my_start_item.collidesWithItem(self._my_end_item)):
            return

        my_start_item = self._my_start_item
        my_end_item = self._my_end_item
        my_color = self._my_color
        my_pen = self.pen()
        my_pen.setColor(self._my_color)
        arrow_size = 20.0
        painter.setPen(my_pen)
        painter.setBrush(self._my_color)

        center_line = QLineF(my_start_item.pos(), my_end_item.pos())
        end_polygon = my_end_item.polygon()
        p1 = end_polygon.at(0) + my_end_item.pos()

        intersect_point = QPointF()
        for i in end_polygon:
            p2 = i + my_end_item.pos()
            poly_line = QLineF(p1, p2)
            intersectType, intersect_point = poly_line.intersects(center_line)
            if intersectType == QLineF.BoundedIntersection:
                break
            p1 = p2

        self.setLine(QLineF(intersect_point, my_start_item.pos()))
        line = self.line()

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrow_head1 = QPointF(math.sin(angle + math.pi / 3.0) * arrow_size,
                              math.cos(angle + math.pi / 3) * arrow_size)
        arrow_p1 = line.p1() + arrow_head1
        arrow_head2 = QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrow_size,
                              math.cos(angle + math.pi - math.pi / 3.0) * arrow_size)
        arrow_p2 = line.p1() + arrow_head2

        self._arrow_head.clear()
        for point in [line.p1(), arrow_p1, arrow_p2]:
            self._arrow_head.append(point)

        painter.drawLine(line)
        painter.drawPolygon(self._arrow_head)
        if self.isSelected():
            painter.setPen(QPen(my_color, 1, Qt.DashLine))
            my_line = QLineF(line)
            my_line.translate(0, 4.0)
            painter.drawLine(my_line)
            my_line.translate(0, -8.0)
            painter.drawLine(my_line)