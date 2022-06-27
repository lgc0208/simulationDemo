"""
    File Name:          mainScene.py
    Author:             LIN Guocheng
    Version:            0.0.1
    Description:        主场景类，定义了操作窗口
"""
from PySide6.QtCore import (QLineF, Qt, Signal)
from PySide6.QtGui import (QFont, QPen)
from PySide6.QtWidgets import (QGraphicsItem, QGraphicsLineItem,
                               QGraphicsTextItem, QGraphicsScene)


from arrow import Arrow
from textItem import TextItem
from items import Items


class MainScene(QGraphicsScene):
    InsertItem, InsertLine, InsertText, MoveItem = range(4)

    item_inserted = Signal(Items)

    text_inserted = Signal(QGraphicsTextItem)

    item_selected = Signal(QGraphicsItem)

    def __init__(self, itemMenu, parent=None):
        super().__init__(parent)

        self._my_item_menu = itemMenu
        self._my_mode = self.MoveItem
        self._my_item_type = 0
        self.line = None
        self._text_item = None
        self._my_item_color = Qt.white
        self._my_text_color = Qt.black
        self._my_line_color = Qt.black
        self._my_font = QFont()

    # 设置线条颜色
    def set_line_color(self, color):
        self._my_line_color = color
        if self.is_item_change(Arrow):
            item = self.selectedItems()[0]
            item.set_color(self._my_line_color)
            self.update()

    # 设置文本颜色
    def set_text_color(self, color):
        self._my_text_color = color
        if self.is_item_change(TextItem):
            item = self.selectedItems()[0]
            item.setDefaultTextColor(self._my_text_color)

    # 设置可选项颜色
    def set_item_color(self, color):
        self._my_item_color = color
        if self.is_item_change(Items):
            item = self.selectedItems()[0]
            item.setBrush(self._my_item_color)

    # 设置字体
    def set_font(self, font):
        self._my_font = font
        if self.is_item_change(TextItem):
            item = self.selectedItems()[0]
            item.setFont(self._my_font)

    # 设置操作模式
    def set_mode(self, mode):
        self._my_mode = mode

    # 设置可选项种类
    def set_item_type(self, type):
        self._my_item_type = type

    # 失去焦点
    def editor_lost_focus(self, item):
        cursor = item.textCursor()
        cursor.clearSelection()
        item.setTextCursor(cursor)

        if not item.toPlainText():
            self.removeItem(item)
            item.deleteLater()

    # 鼠标点击事件
    def mousePressEvent(self, mouseEvent):
        if (mouseEvent.button() != Qt.LeftButton):
            return

        if self._my_mode == self.InsertItem:
            item = Items(self._my_item_type, self._my_item_menu)
            item.setBrush(self._my_item_color)
            self.addItem(item)
            item.setPos(mouseEvent.scenePos())
            self.item_inserted.emit(item)
        elif self._my_mode == self.InsertLine:
            self.line = QGraphicsLineItem(QLineF(mouseEvent.scenePos(),
                                                 mouseEvent.scenePos()))
            self.line.setPen(QPen(self._my_line_color, 2))
            self.addItem(self.line)
        elif self._my_mode == self.InsertText:
            text_item = TextItem()
            text_item.setFont(self._my_font)
            text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
            text_item.setZValue(1000.0)
            text_item.lost_focus.connect(self.editor_lost_focus)
            text_item.selected_change.connect(self.item_selected)
            self.addItem(text_item)
            text_item.setDefaultTextColor(self._my_text_color)
            text_item.setPos(mouseEvent.scenePos())
            self.text_inserted.emit(text_item)

        super(MainScene, self).mousePressEvent(mouseEvent)

    # 鼠标移动事件
    def mouseMoveEvent(self, mouseEvent):
        if self._my_mode == self.InsertLine and self.line:
            new_line = QLineF(self.line.line().p1(), mouseEvent.scenePos())
            self.line.setLine(new_line)
        elif self._my_mode == self.MoveItem:
            super(MainScene, self).mouseMoveEvent(mouseEvent)

    # 鼠标释放事件
    def mouseReleaseEvent(self, mouseEvent):
        if self.line and self._my_mode == self.InsertLine:
            start_items = self.items(self.line.line().p1())
            if len(start_items) and start_items[0] == self.line:
                start_items.pop(0)
            end_items = self.items(self.line.line().p2())
            if len(end_items) and end_items[0] == self.line:
                end_items.pop(0)

            self.removeItem(self.line)
            self.line = None

            if (len(start_items) and len(end_items) and
                    isinstance(start_items[0], Items) and
                    isinstance(end_items[0], Items) and
                    start_items[0] != end_items[0]):
                start_item = start_items[0]
                end_item = end_items[0]
                arrow = Arrow(start_item, end_item)
                arrow.set_color(self._my_line_color)
                start_item.add_arrow(arrow)
                end_item.add_arrow(arrow)
                arrow.setZValue(-1000.0)
                self.addItem(arrow)
                arrow.update_position()

                # 连接箭头释放后进行传值
                end_item.calculateResult(end_item.item_type,
                                         start_item.getOutputNum()+end_item.getInputNum())

        self.line = None
        super(MainScene, self).mouseReleaseEvent(mouseEvent)

    # 是否可选项发生改变
    def is_item_change(self, type):
        for item in self.selectedItems():
            return True
        return False
