import sys
from PySide6.QtCore import (QRect, QRectF, QSize, Qt)
from PySide6.QtGui import (QAction, QColor, QFont, QIcon, QIntValidator,
                           QPainter, QPixmap, QBrush)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QComboBox,
                               QFontComboBox, QGraphicsView, QGridLayout,
                               QHBoxLayout, QLabel, QMainWindow, QMenu,
                               QMessageBox, QSizePolicy, QToolBox, QToolButton,
                               QWidget)


from items import Items
from ioset import IOSet
from mainScene import MainScene
import simulationDemo_rc

# 主窗口类
class MainWindow(QMainWindow):
    insert_text_button = 10

    def __init__(self):
        super().__init__()
        
        self.create_actions()
        self.create_menus()
        self.create_tool_box()

        self.scene = MainScene(self._item_menu)
        self.scene.setSceneRect(QRectF(0, 0, 5000, 5000))
        self.scene.item_inserted.connect(self.item_inserted)
        self.scene.text_inserted.connect(self.text_inserted)
        self.scene.item_selected.connect(self.item_selected)

        self.create_toolbars()

        layout = QHBoxLayout()
        layout.addWidget(self._tool_box)
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.widget = QWidget()
        self.widget.setLayout(layout)

        self.setCentralWidget(self.widget)
        self.setWindowTitle("Simulation Demo in Python 2021")
        
        self.setGetWindow = IOSet()
        self.setGetWindow.new_input_value.connect(self.getInputValue)

        
        
     #★ 唤醒子窗口
    def setGetValueWindow(self):
        inputNum = 0
        # 遍历所选择的项
        for item in self.scene.selectedItems():
            # 确认不同类型的可操作性项
            if isinstance(item, Items):
                inputNum = item.getInputNum()
                outputNum = item.calculateResult(item.item_type, inputNum)
                self.setGetWindow.ui.inputValue.setText(str(inputNum).strip('(').strip(')'))
                self.setGetWindow.ui.outputValue.setText(str(outputNum).strip('(').strip(')'))
                self.setGetWindow.ui.E0Value.setText(str(item.getE0()))
                self.setGetWindow.ui.FcValue.setText(str(item.getfc()))
                # 若为 TextItem
                if item.item_type == item.TestItem:
                    self.setGetWindow.ui.E0Value.setVisible(False)
                    self.setGetWindow.ui.FcValue.setVisible(False)
                    self.setGetWindow.ui.labelE0.setVisible(False)
                    self.setGetWindow.ui.labelFc.setVisible(False)
                # 若为NRZOOK
                elif item.item_type == item.NRZOOK or item.RZ33OOk or item.RZ50OOK or item.RZ66OOK:
                    self.setGetWindow.ui.E0Value.setVisible(True)
                    self.setGetWindow.ui.FcValue.setVisible(True)
                    self.setGetWindow.ui.labelE0.setVisible(True)
                    self.setGetWindow.ui.labelFc.setVisible(True)
                self.setGetWindow.ui.outputValue.setText(str(item.getOutputNum()).strip('(').strip(')'))
                self.setGetWindow.show()
                    
                
        
    
    #★ 获取用户设定的值
    def getInputValue(self, inputNum, E0, fc):
        for item in self.scene.selectedItems():
            if isinstance(item, Items):
                if item.item_type == item.NRZOOK or item.RZ33OOk or item.RZ50OOK or item.RZ66OOK:
                    item.setInputNum(inputNum)
                    item.setE0(E0)
                    item.setfc(fc)
                elif item.item_type == item.TestItem:
                    item.setInputNum(inputNum)
                else:
                    print("getInputValue出现问题")
                item.calculateResult(item.item_type, inputNum)
        self.setGetWindow.close()
    
    # 创建工具盒
    def create_tool_box(self):
    
        self._button_group = QButtonGroup()
        self._button_group.setExclusive(False)
        self._button_group.idClicked.connect(self.button_group_clicked)
        
        # 器件选择框
        layout = QGridLayout()
        layout.addWidget(self.create_cell_widget("乘方器", Items.TestItem),
                0, 0)
        layout.addWidget(self.create_cell_widget("NRZ-OOK调制器", Items.NRZOOK),
                         0, 1)
        layout.addWidget(self.create_cell_widget("RZ33-OOK调制器", Items.RZ33OOk),
                         1, 0)
        layout.addWidget(self.create_cell_widget("RZ50-OOK调制器", Items.RZ50OOK),
                         1, 1)
        layout.addWidget(self.create_cell_widget("RZ66-OOK调制器", Items.RZ66OOK),
                         2, 0)
        
        # 添加文字按钮
        text_button = QToolButton()
        text_button.setCheckable(True)
        self._button_group.addButton(text_button, self.insert_text_button)
        text_button.setIcon(QIcon(QPixmap(':/images/textpointer.png')
                            .scaled(30, 30)))
        text_button.setIconSize(QSize(50, 50))

        text_layout = QGridLayout()
        text_layout.addWidget(text_button, 0, 1, Qt.AlignHCenter)
        text_layout.addWidget(QLabel("文本框"), 2, 1, Qt.AlignCenter)
        text_widget = QWidget()
        text_widget.setLayout(text_layout)
        layout.addWidget(text_widget, 2, 1)

        layout.setRowStretch(3, 10)
        layout.setColumnStretch(2, 10)

        item_widget = QWidget()
        item_widget.setLayout(layout)

        self._background_button_group = QButtonGroup()
        self._background_button_group.buttonClicked.connect(self.background_button_group_clicked)

        # 背景选择框
        background_layout = QGridLayout()
        background_layout.addWidget(self.create_background_cell_widget("蓝色格子",
                ':/images/background1.png'), 0, 0)
        background_layout.addWidget(self.create_background_cell_widget("白色格子",
                ':/images/background2.png'), 0, 1)
        background_layout.addWidget(self.create_background_cell_widget("灰色格子",
                ':/images/background3.png'), 1, 0)
        background_layout.addWidget(self.create_background_cell_widget("空白格子",
                ':/images/background4.png'), 1, 1)

        background_layout.setRowStretch(2, 10)
        background_layout.setColumnStretch(2, 10)

        background_widget = QWidget()
        background_widget.setLayout(background_layout)

        self._tool_box = QToolBox()
        self._tool_box.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Ignored))
        self._tool_box.setMinimumWidth(item_widget.sizeHint().width())
        self._tool_box.addItem(item_widget, "可选项")
        self._tool_box.addItem(background_widget, "背景项")
        
    
    # 背景选择按钮
    def background_button_group_clicked(self, button):
        buttons = self._background_button_group.buttons()
        for myButton in buttons:
            if myButton != button:
                button.setChecked(False)

        text = button.text()
        if text == "蓝色格子":
            self.scene.setBackgroundBrush(QBrush(QPixmap(':/images/background1.png')))
        elif text == "白色格子":
            self.scene.setBackgroundBrush(QBrush(QPixmap(':/images/background2.png')))
        elif text == "灰色格子":
            self.scene.setBackgroundBrush(QBrush(QPixmap(':/images/background3.png')))
        else:
            self.scene.setBackgroundBrush(QBrush(QPixmap(':/images/background4.png')))

        self.scene.update()
        self.view.update()

    # 背景选择按钮点击事件
    def button_group_clicked(self, idx):
        buttons = self._button_group.buttons()
        for button in buttons:
            if self._button_group.button(idx) != button:
                button.setChecked(False)

        if idx == self.insert_text_button:
            self.scene.set_mode(MainScene.InsertText)
        else:
            self.scene.set_item_type(idx)
            self.scene.set_mode(MainScene.InsertItem)

    # 删除项
    def delete_item(self):
        for item in self.scene.selectedItems():
            if isinstance(item, Items):
                item.remove_arrows()
            self.scene.removeItem(item)

    # 指针点击事件
    def pointer_group_clicked(self, i):
        self.scene.set_mode(self._pointer_type_group.checkedId())

    # 将项置于表面
    def bring_to_front(self):
        if not self.scene.selectedItems():
            return

        selected_item = self.scene.selectedItems()[0]
        overlap_items = selected_item.collidingItems()

        z_value = 0
        for item in overlap_items:
            if (item.zValue() >= z_value and isinstance(item, Items)):
                z_value = item.zValue() + 0.1
        selected_item.setZValue(z_value)

    # 将项送至底部
    def send_to_back(self):
        if not self.scene.selectedItems():
            return

        selected_item = self.scene.selectedItems()[0]
        overlap_items = selected_item.collidingItems()

        z_value = 0
        for item in overlap_items:
            if (item.zValue() <= z_value and isinstance(item, Items)):
                z_value = item.zValue() - 0.1
        selected_item.setZValue(z_value)
    
    # 插入项
    def item_inserted(self, item):
        self._pointer_type_group.button(MainScene.MoveItem).setChecked(True)
        self.scene.set_mode(self._pointer_type_group.checkedId())
        self._button_group.button(item.item_type).setChecked(False)

    # 插入文本
    def text_inserted(self, item):
        self._button_group.button(self.insert_text_button).setChecked(False)
        self.scene.set_mode(self._pointer_type_group.checkedId())

    # 改变当前字体
    def current_font_changed(self, font):
        self.handle_font_change()

    # 改变字号
    def font_size_changed(self, font):
        self.handle_font_change()

    # 改变屏幕大小
    def scene_scale_changed(self, scale):
        new_scale = int(scale[:-1]) / 100.0
        old_matrix = self.view.transform()
        self.view.resetTransform()
        self.view.translate(old_matrix.dx(), old_matrix.dy())
        self.view.scale(new_scale, new_scale)
        
    # 改变字体颜色
    def text_color_changed(self):
        self._text_action = self.sender()
        self._font_color_tool_button.setIcon(self.create_color_tool_button_icon(
                    ':/images/textpointer.png',
                    QColor(self._text_action.data())))
        self.text_button_triggered()

    # 改变项颜色
    def item_color_changed(self):
        self._fill_action = self.sender()
        self._fill_color_tool_button.setIcon(self.create_color_tool_button_icon(
                    ':/images/floodfill.png',
                    QColor(self._fill_action.data())))
        self.fill_button_triggered()

    # 改变线条颜色
    def line_color_changed(self):
        self._line_action = self.sender()
        self._line_color_tool_button.setIcon(self.create_color_tool_button_icon(
                    ':/images/linecolor.png',
                    QColor(self._line_action.data())))
        self.line_button_triggered()

    # 文本按钮触发事件
    def text_button_triggered(self):
        self.scene.set_text_color(QColor(self._text_action.data()))

    # 填充按钮触发事件
    def fill_button_triggered(self):
        self.scene.set_item_color(QColor(self._fill_action.data()))
        
    # 线条按钮触发事件
    def line_button_triggered(self):
        self.scene.set_line_color(QColor(self._line_action.data()))

    # 粗体/斜体/下划线设置
    def handle_font_change(self):
        font = self._font_combo.currentFont()
        font.setPointSize(int(self._font_size_combo.currentText()))
        if self._bold_action.isChecked():
            font.setWeight(QFont.Bold)
        else:
            font.setWeight(QFont.Normal)
        font.setItalic(self._italic_action.isChecked())
        font.setUnderline(self._underline_action.isChecked())

        self.scene.set_font(font)

    # 选择项
    def item_selected(self, item):
        font = item.font()
        #color = item.defaultTextColor()
        self._font_combo.setCurrentFont(font)
        self._font_size_combo.setEditText(str(font.pointSize()))
        self._bold_action.setChecked(font.weight() == QFont.Bold)
        self._italic_action.setChecked(font.italic())
        self._underline_action.setChecked(font.underline())
        
    # 关于
    def about(self):
        QMessageBox.about(self, "简介", "待添加")


    # 绑定动作和快捷键
    def create_actions(self):
        self._to_front_action = QAction(
                QIcon(':/images/bringtofront.png'), "上移一层",
                self, shortcut="Ctrl+F", statusTip="Bring item to front",
                triggered=self.bring_to_front)

        self._send_back_action = QAction(
                QIcon(':/images/sendtoback.png'), "下移一层", self,
                shortcut="Ctrl+B", statusTip="Send item to back",
                triggered=self.send_to_back)

        self._delete_action = QAction(QIcon(':/images/delete.png'),
                "删除", self, shortcut="Delete",
                statusTip="Delete item from demo",
                triggered=self.delete_item)
        
        self._set_get_action = QAction(
                QIcon(":/images/delete.png"), "操作", self,
                shortcut="Ctrl+E", triggered = self.setGetValueWindow)

        self._exit_action = QAction("退出", self, shortcut="Ctrl+X",
                statusTip="Quit the demo", triggered=self.close)

        self._bold_action = QAction(QIcon(':/images/bold.png'),
                "Bold", self, checkable=True, shortcut="Ctrl+B",
                triggered=self.handle_font_change)

        self._italic_action = QAction(QIcon(':/images/italic.png'),
                "Italic", self, checkable=True, shortcut="Ctrl+I",
                triggered=self.handle_font_change)

        self._underline_action = QAction(
                QIcon(':/images/underline.png'), "下划线", self,
                checkable=True, shortcut="Ctrl+U",
                triggered=self.handle_font_change)

        self._about_action = QAction("关于", self, shortcut="Ctrl+B",
                triggered=self.about)
        
       

    # 创建菜单
    def create_menus(self):
        self._file_menu = self.menuBar().addMenu("文件")
        self._file_menu.addAction(self._exit_action)

        self._item_menu = self.menuBar().addMenu("项目")
        self._item_menu.addAction(self._delete_action)
        self._item_menu.addSeparator()
        self._item_menu.addAction(self._to_front_action)
        self._item_menu.addAction(self._send_back_action)
        self._item_menu.addAction(self._set_get_action)

        self._about_menu = self.menuBar().addMenu("帮助")
        self._about_menu.addAction(self._about_action)

    # 创建工具栏
    def create_toolbars(self):
        self._edit_tool_bar = self.addToolBar("编辑")
        self._edit_tool_bar.addAction(self._delete_action)
        self._edit_tool_bar.addAction(self._to_front_action)
        self._edit_tool_bar.addAction(self._send_back_action)

        self._font_combo = QFontComboBox()
        self._font_combo.currentFontChanged.connect(self.current_font_changed)

        self._font_size_combo = QComboBox()
        self._font_size_combo.setEditable(True)
        for i in range(8, 30, 2):
            self._font_size_combo.addItem(str(i))
        validator = QIntValidator(2, 64, self)
        self._font_size_combo.setValidator(validator)
        self._font_size_combo.currentIndexChanged.connect(self.font_size_changed)

        self._font_color_tool_button = QToolButton()
        self._font_color_tool_button.setPopupMode(QToolButton.MenuButtonPopup)
        self._font_color_tool_button.setMenu(
                self.create_color_menu(self.text_color_changed, Qt.black))
        self._text_action = self._font_color_tool_button.menu().defaultAction()
        self._font_color_tool_button.setIcon(
                self.create_color_tool_button_icon(':/images/textpointer.png',
                        Qt.black))
        self._font_color_tool_button.setAutoFillBackground(True)
        self._font_color_tool_button.clicked.connect(self.text_button_triggered)

        self._fill_color_tool_button = QToolButton()
        self._fill_color_tool_button.setPopupMode(QToolButton.MenuButtonPopup)
        self._fill_color_tool_button.setMenu(
                self.create_color_menu(self.item_color_changed, Qt.white))
        self._fill_action = self._fill_color_tool_button.menu().defaultAction()
        self._fill_color_tool_button.setIcon(
                self.create_color_tool_button_icon(':/images/floodfill.png',
                        Qt.white))
        self._fill_color_tool_button.clicked.connect(self.fill_button_triggered)

        self._line_color_tool_button = QToolButton()
        self._line_color_tool_button.setPopupMode(QToolButton.MenuButtonPopup)
        self._line_color_tool_button.setMenu(
                self.create_color_menu(self.line_color_changed, Qt.black))
        self._line_action = self._line_color_tool_button.menu().defaultAction()
        self._line_color_tool_button.setIcon(
                self.create_color_tool_button_icon(':/images/linecolor.png',
                        Qt.black))
        self._line_color_tool_button.clicked.connect(self.line_button_triggered)

        self._text_tool_bar = self.addToolBar("字体")
        self._text_tool_bar.addWidget(self._font_combo)
        self._text_tool_bar.addWidget(self._font_size_combo)
        self._text_tool_bar.addAction(self._bold_action)
        self._text_tool_bar.addAction(self._italic_action)
        self._text_tool_bar.addAction(self._underline_action)

        self._color_tool_bar = self.addToolBar("颜色")
        self._color_tool_bar.addWidget(self._font_color_tool_button)
        self._color_tool_bar.addWidget(self._fill_color_tool_button)
        self._color_tool_bar.addWidget(self._line_color_tool_button)

        pointer_button = QToolButton()
        pointer_button.setCheckable(True)
        pointer_button.setChecked(True)
        pointer_button.setIcon(QIcon(':/images/pointer.png'))
        line_pointer_button = QToolButton()
        line_pointer_button.setCheckable(True)
        line_pointer_button.setIcon(QIcon(':/images/linepointer.png'))

        self._pointer_type_group = QButtonGroup()
        self._pointer_type_group.addButton(pointer_button, MainScene.MoveItem)
        self._pointer_type_group.addButton(line_pointer_button,
                MainScene.InsertLine)
        self._pointer_type_group.idClicked.connect(self.pointer_group_clicked)

        self._scene_scale_combo = QComboBox()
        self._scene_scale_combo.addItems(["50%", "75%", "100%", "125%", "150%"])
        self._scene_scale_combo.setCurrentIndex(2)
        self._scene_scale_combo.currentTextChanged.connect(self.scene_scale_changed)

        self._pointer_toolbar = self.addToolBar("Pointer type")
        self._pointer_toolbar.addWidget(pointer_button)
        self._pointer_toolbar.addWidget(line_pointer_button)
        self._pointer_toolbar.addWidget(self._scene_scale_combo)

    # 创建背景单元格部件
    def create_background_cell_widget(self, text, image):
        button = QToolButton()
        button.setText(text)
        button.setIcon(QIcon(image))
        button.setIconSize(QSize(50, 50))
        button.setCheckable(True)
        self._background_button_group.addButton(button)

        layout = QGridLayout()
        layout.addWidget(button, 0, 0, Qt.AlignHCenter)
        layout.addWidget(QLabel(text), 1, 0, Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    # 创建项部件
    def create_cell_widget(self, text, item_type):
        item = Items(item_type, self._item_menu)
        icon = QIcon(item.image().scaled(500, 500))

        button = QToolButton()
        button.setIcon(icon)
        button.setIconSize(QSize(50, 50))
        button.setCheckable(True)
        self._button_group.addButton(button, item_type)

        layout = QGridLayout()
        layout.addWidget(button, 0, 0, Qt.AlignHCenter)
        layout.addWidget(QLabel(text), 1, 0, Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

    # 创建颜色选择菜单
    def create_color_menu(self, slot, defaultColor):
        colors = [Qt.black, Qt.white, Qt.red, Qt.blue, Qt.yellow]
        names = ["黑色", "白色", "红色", "蓝色", "黄色"]

        color_menu = QMenu(self)
        for color, name in zip(colors, names):
            action = QAction(self.create_color_icon(color), name, self,
                    triggered=slot)
            action.setData(QColor(color))
            color_menu.addAction(action)
            if color == defaultColor:
                color_menu.setDefaultAction(action)
        return color_menu

    # 创建颜色按钮图标
    def create_color_tool_button_icon(self, imageFile, color):
        pixmap = QPixmap(50, 80)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        image = QPixmap(imageFile)
        target = QRect(0, 0, 50, 60)
        source = QRect(0, 0, 42, 42)
        painter.fillRect(QRect(0, 60, 50, 80), color)
        painter.drawPixmap(target, image, source)
        painter.end()

        return QIcon(pixmap)

    # 创建颜色图标
    def create_color_icon(self, color):
        pixmap = QPixmap(20, 20)
        painter = QPainter(pixmap)
        painter.setPen(Qt.NoPen)
        painter.fillRect(QRect(0, 0, 20, 20), color)
        painter.end()
        return QIcon(pixmap)
    
    # 重写窗口关闭函数，解决关闭主程序的窗口但子窗口仍显示的问题
    def closeEvent(self, event):
        sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.setGeometry(100, 100, 800, 500)
    main_window.show()

    sys.exit(app.exec())
    