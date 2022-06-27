"""
    File Name:          textItem.py
    Author:             LIN Guocheng
    Version:            1.0.0
    Description:        文本框类，用于实现平台的文本框操作
"""
from PySide6.QtCore import (Qt, Signal)
from PySide6.QtWidgets import (QGraphicsItem, QGraphicsTextItem)

# 文本框


class TextItem(QGraphicsTextItem):
    lost_focus = Signal(QGraphicsTextItem)

    selected_change = Signal(QGraphicsItem)

    def __init__(self, parent=None, scene=None):
        super().__init__(parent, scene)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    # 当项目被选中时发出信号
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            self.selected_change.emit(self)
        return value

    # 焦点离开后的事件
    def focusOutEvent(self, event):
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.lost_focus.emit(self)
        super(TextItem, self).focusOutEvent(event)

    # 鼠标双击事件
    def mouseDoubleClickEvent(self, event):
        if self.textInteractionFlags() == Qt.NoTextInteraction:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)
        super(TextItem, self).mouseDoubleClickEvent(event)
