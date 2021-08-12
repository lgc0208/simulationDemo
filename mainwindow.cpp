/**
* @file     mainwindow.cpp
* @brief    项目主函数文件
* @details  主要包含主窗口界面的函数实现，QT 的 MainWindow 类，代表了展示给用户的 GUI 界面。
 *          MainWindow类在QMainWindow中创建和布局小部件。
 *          类将输入从小部件转发到DiagramScene。
 *          当图场景的文本项更改，或者一个图项或一个图文本项被插入到场景中时，它也会更新它的小部件。
 *          这个类还从场景中删除项目，这决定了项目在相互重叠时的绘制顺序。
* @author   LIN Guocheng
* @date     2021-8-6
* @version  V0.0.1
**********************************************************************************
* @attention
* QT版本：5.12.11
* @par 修改日志:
* <table>
* <tr><th>Date        <th>Version  <th>Author    <th>Description
* <tr><td>2021/08/06  <td>0.0.1    <td>LIN Guocheng  <td>创建初始版本
* </table>
*
**********************************************************************************
*/

#include "mainwindow.h"
#include "arrow.h"
#include "items.h"
#include "simulationScene.h"
#include "textItem.h"
#include "ioset.h"
#include <QtWidgets>
#include <QGraphicsSceneMouseEvent>
#include <iostream>
using namespace std;

const int InsertTextButton = 10;

MainWindow::MainWindow()
{
    createActions();
    createToolBox();
    createMenus();

    scene = new SimulationScene(itemMenu, this);
    scene->setSceneRect(QRectF(0, 0, 5000, 5000));
    connect(scene, SIGNAL(itemInserted(Items*)),
            this, SLOT(itemInserted(Items*)));
    connect(scene, SIGNAL(textInserted(QGraphicsTextItem*)),
            this, SLOT(textInserted(QGraphicsTextItem*)));
    connect(scene, SIGNAL(itemSelected(QGraphicsItem*)),
            this, SLOT(itemSelected(QGraphicsItem*)));
    createToolbars();



    QHBoxLayout *layout = new QHBoxLayout;
    layout->addWidget(toolBox);
    view = new QGraphicsView(scene);
    layout->addWidget(view);

    QWidget *widget = new QWidget;
    widget->setLayout(layout);

    setCentralWidget(widget);
    setWindowTitle(tr("SimulationDemo Version 0.0.1"));
    setUnifiedTitleAndToolBarOnMac(true);
}

/**
 * @brief   MainWindow::buttonGroupClicked  根据不同的图标切换不同的运行模式
 * @param   id  点击的按键对应的id
 */
void MainWindow::buttonGroupClicked(int id)
{
    //  定义按键集合
    QList<QAbstractButton *> buttons = buttonGroup->buttons();

    //  遍历 buttons 中的 QAbstractButton 项，设置 buttons 中的元素为未选中状态
    foreach (QAbstractButton *button, buttons) {
        if (buttonGroup->button(id) != button)
            button->setChecked(false);
    }

    //  根据点击的图标设定程序执行模式为： 插入文字模式 或 插入项模式
    if (id == InsertTextButton) {
        scene->setMode(SimulationScene::insertText);
    } else {
        scene->setItemType(Items::ItemType(id));
        scene->setMode(SimulationScene::insertItem);
    }
}

/**
 * @brief MainWindow::deleteItem()  删除对应的项
 */
void MainWindow::deleteItem()
{
    //  遍历所有选择的项，如果为箭头，执行该部分代码
    foreach (QGraphicsItem *item, scene->selectedItems()) {
        if (item->type() == Arrow::Type) {
            scene->removeItem(item);    // 从场景内移除所有 item 及其子类
            //  如果 item 是类型 Arrow 则返回指定 item 转换为 Arrow 类型，否则返回 0
            Arrow *arrow = qgraphicsitem_cast<Arrow *>(item);
            arrow->startItem()->removeArrow(arrow);
            arrow->endItem()->removeArrow(arrow);
            delete item;
        }
    }

    //  遍历所有选择的项，如果为图，执行该部分代码
    foreach (QGraphicsItem *item, scene->selectedItems()) {
         if (item->type() == Items::Type)
             qgraphicsitem_cast <Items *> (item)->removeArrows();
         scene->removeItem(item);
         delete item;
     }
}

/**
 * @brief MainWindow::pointerGroupClicked   决定场景是否是ItemMove或InsertLine模式
 */
void MainWindow::pointerGroupClicked(int)
{
    scene->setMode(SimulationScene::Mode(pointerTypeGroup->checkedId()));
}

/**
 * @brief MainWindow::bringToFront()    将页面下方的项移到表面
 */
void MainWindow::bringToFront()
{
    //  如果未指定项，则跳过该函数
    if (scene->selectedItems().isEmpty())
        return;

    QGraphicsItem *selectedItem = scene->selectedItems().first();
    QList<QGraphicsItem *> overlapItems = selectedItem->collidingItems(); // 遍历所有相互存在碰撞的项

    qreal zValue = 0;
    //  遍历所有与选择的项存在碰撞的项，将所选择的项移到最上层
    foreach (QGraphicsItem *item, overlapItems) {
        if (item->zValue() >= zValue && item->type() == Items::Type)
            zValue = item->zValue() + 0.1;
    }
    selectedItem->setZValue(zValue);
}

/**
 * @brief MainWindow::sendToBack()  将页面表面的项移到下面
 */
void MainWindow::sendToBack()
{
    //  若未指定项，跳过该函数
    if (scene->selectedItems().isEmpty())
        return;

    QGraphicsItem *selectedItem = scene->selectedItems().first();
    QList<QGraphicsItem *> overlapItems = selectedItem->collidingItems();

    qreal zValue = 0;
    //  遍历所有存在重叠的项，将所选择的项移到最下层
    foreach (QGraphicsItem *item, overlapItems) {
        if (item->zValue() <= zValue && item->type() == Items::Type)
            zValue = item->zValue() - 0.1;
    }
    selectedItem->setZValue(zValue);
}


/**
 * @brief MainWindow::itemInserted  插入新的项
 * @param item    所需要插入的项
 */
void MainWindow::itemInserted(Items *item)
{
    pointerTypeGroup->button(int(SimulationScene::moveItem))->setChecked(true);
    scene->setMode(SimulationScene::Mode(pointerTypeGroup->checkedId()));
    buttonGroup->button(int(item->itemType()))->setChecked(false);
}

/**
 * @brief MainWindow::textInserted  插入文本框
 * @param QGraphicsTextItem 格式化的文本项
 */
void MainWindow::textInserted(QGraphicsTextItem *)
{
    buttonGroup->button(InsertTextButton)->setChecked(false);
    scene->setMode(SimulationScene::Mode(pointerTypeGroup->checkedId()));
}

/**
 * @brief MainWindow::currentFontChanged    修改文本字体
 * @param QFont    Qt控件文字属性
 */
void MainWindow::currentFontChanged(const QFont &)
{
    handleFontChange();
}

/**
 * @brief MainWindow::fontSizeChanged   修改文本字体大小-绑定事件
 * @param QString   字符串类型，表示大小
 */
void MainWindow::fontSizeChanged(const QString &)
{
    handleFontChange();
}

/**
 * @brief MainWindow::sceneScaleChanged 更改界面显示比例
 * @param  scale   表征页面显示比例的字符串
 */
void MainWindow::sceneScaleChanged(const QString &scale)
{
    double newScale = scale.left(scale.indexOf(tr("%"))).toDouble() / 100.0;
    QMatrix oldMatrix = view->matrix();
    view->resetMatrix();
    view->translate(oldMatrix.dx(), oldMatrix.dy());
    view->scale(newScale, newScale);
}

/**
 * @brief   MainWindow::handleFontChange    修改字体形态
 */
void MainWindow::handleFontChange()
{
    QFont font = fontCombo->currentFont();
    font.setPointSize(fontSizeCombo->currentText().toInt());    // 设置大小
    font.setWeight(boldAction->isChecked() ? QFont::Bold : QFont::Normal);  // 设置粗细
    font.setItalic(italicAction->isChecked());  // 设置是否斜体
    font.setUnderline(underlineAction->isChecked());    // 设置是否下划线

    scene->setFont(font);
}


/**
 * @brief MainWindow::itemSelected  选择指定项
 * @param item      QGraphicsItem类型，表示所选择的项
 */
void MainWindow::itemSelected(QGraphicsItem *item)
{
    TextItem *textItem = qgraphicsitem_cast <TextItem *> (item);
    QFont font = textItem->font();
    fontCombo->setCurrentFont(font);
    fontSizeCombo->setEditText(QString().setNum(font.pointSize()));
    boldAction->setChecked(font.weight() == QFont::Bold);
    italicAction->setChecked(font.italic());
    underlineAction->setChecked(font.underline());
}

/**
 * @brief MainWindow::about  简介页面
 */
void MainWindow::about()
{
    QMessageBox::about(this, tr("简介"), tr("简介详细"));
}

/**
 * @brief MainWindow::createToolBox 创建工具箱
 */
void MainWindow::createToolBox()
{
    buttonGroup = new QButtonGroup(this);   // 创建 button group
    buttonGroup->setExclusive(false);   //  取消按钮组互斥
    //  QT中的连接函数，将信号发送者 buttonGroup 对象中的信号 buttonClicked 与
    //  接受者 this 中的 buttonGroupClicked 槽函数联系起来
    connect(buttonGroup, SIGNAL(buttonClicked(int)),
            this, SLOT(buttonGroupClicked(int)));

    //  添加框图控件
    QGridLayout *layout = new QGridLayout;
    layout->addWidget(createCellWidget(tr("测试框"), Items::test), 0, 0);

    //添加工具按钮组
    QToolButton *textButton = new QToolButton;
    textButton->setCheckable(true); // 可以选中
    buttonGroup->addButton(textButton, InsertTextButton);
    textButton->setIcon(QIcon(QPixmap(":/images/textpointer.png")));
    textButton->setIconSize(QSize(50, 50));
    QGridLayout *textLayout = new QGridLayout;
    textLayout->addWidget(textButton, 0, 0, Qt::AlignHCenter);
    textLayout->addWidget(new QLabel(tr("文本框")), 1, 0, Qt::AlignCenter);
    QWidget *textWidget = new QWidget;
    textWidget->setLayout(textLayout);
    layout->addWidget(textWidget, 0, 1);

    //  设置行列的伸缩空间
    layout->setRowStretch(3, 10);
    layout->setColumnStretch(2, 10);

    QWidget *itemWidget = new QWidget;
    itemWidget->setLayout(layout);

    toolBox = new QToolBox;
    toolBox->setSizePolicy(QSizePolicy(QSizePolicy::Maximum, QSizePolicy::Ignored));    // 标准拉伸
    toolBox->setMinimumWidth(itemWidget->sizeHint().width());   // 设置最小宽度
    toolBox->addItem(itemWidget, tr("测试控件栏"));
}

/**
 * @brief MainWindow::createActions 创建顶部操作栏
 */
void MainWindow::createActions()
{
    toFrontAction = new QAction(QIcon(":/images/bringtofront.png"),
                                tr("浮于表面"), this);
    toFrontAction->setShortcut(tr("Ctrl+F"));   // 设定快捷键
    toFrontAction->setStatusTip(tr("浮于表面"));    // 设定提示语
    connect(toFrontAction, SIGNAL(triggered()), this, SLOT(bringToFront()));

    sendBackAction = new QAction(QIcon(":/images/sendtoback.png"), tr("沉于底部"), this);
    sendBackAction->setShortcut(tr("Ctrl+T"));  // 设定快捷键
    sendBackAction->setStatusTip(tr("沉于底部"));   // 设定提示语
    connect(sendBackAction, SIGNAL(triggered()), this, SLOT(sendToBack()));

    // test
    setGetAction = new QAction(QIcon(":/images/delete.png"), tr("操作"), this);
    setGetAction->setShortcut(tr("Ctrl+E"));
    setGetAction->setStatusTip(tr("操作"));
    connect(setGetAction, SIGNAL(triggered()), this, SLOT(setGetValueWindow()));


    deleteAction = new QAction(QIcon(":/images/delete.png"), tr("删除"), this);
    deleteAction->setShortcut(tr("Delete"));    // 设定快捷键
    deleteAction->setStatusTip(tr("删除控件")); // 设定提示语
    connect(deleteAction, SIGNAL(triggered()), this, SLOT(deleteItem()));

    exitAction = new QAction(tr("退出"), this);
    exitAction->setShortcuts(QKeySequence::Quit);
    exitAction->setStatusTip(tr("退出示例"));
    connect(exitAction, SIGNAL(triggered()), this, SLOT(close()));

    boldAction = new QAction(tr("加粗"), this);
    boldAction->setCheckable(true);
    QPixmap pixmap(":/images/bold.png");
    boldAction->setIcon(QIcon(pixmap));
    boldAction->setShortcut(tr("Ctrl+B"));
    connect(boldAction, SIGNAL(triggered()), this, SLOT(handleFontChange()));

    italicAction = new QAction(QIcon(":/images/italic.png"), tr("斜体"), this);
    italicAction->setCheckable(true);
    italicAction->setShortcut(tr("Ctrl+I"));
    connect(italicAction, SIGNAL(triggered()), this, SLOT(handleFontChange()));

    underlineAction = new QAction(QIcon(":/images/underline.png"), tr("下划线"), this);
    underlineAction->setCheckable(true);
    underlineAction->setShortcut(tr("Ctrl+U"));
    connect(underlineAction, SIGNAL(triggered()), this, SLOT(handleFontChange()));

    aboutAction = new QAction(tr("关于"), this);
    aboutAction->setShortcut(tr("F1"));
    connect(aboutAction, SIGNAL(triggered()), this, SLOT(about()));
}

/**
 * @brief MainWindow::createMenus   创建菜单栏
 */
void MainWindow::createMenus()
{
    fileMenu = menuBar()->addMenu(tr("文件"));
    fileMenu->addAction(exitAction);

    itemMenu = menuBar()->addMenu(tr("控件"));
    itemMenu->addAction(deleteAction);
    itemMenu->addSeparator();
    itemMenu->addAction(toFrontAction);
    itemMenu->addAction(sendBackAction);
    itemMenu->addAction(setGetAction);

    AboutMenu = menuBar()->addMenu(tr("帮助"));
    AboutMenu->addAction(aboutAction);
}

/**
 * @brief MainWindow::createToolbars    创建工作台
 */
void MainWindow::createToolbars()
{
    editToolBar = addToolBar(tr("编辑"));
    editToolBar->addAction(deleteAction);
    editToolBar->addAction(toFrontAction);
    editToolBar->addAction(sendBackAction);

    fontCombo = new QFontComboBox();
    connect(fontCombo, SIGNAL(currentFontChanged(QFont)),
            this, SLOT(currentFontChanged(QFont)));

    fontSizeCombo = new QComboBox;
    fontSizeCombo->setEditable(true);
    for (int i = 8; i < 30; i = i + 2)
        fontSizeCombo->addItem(QString().setNum(i));
    QIntValidator *validator = new QIntValidator(2, 64, this);
    fontSizeCombo->setValidator(validator);
    connect(fontSizeCombo, SIGNAL(currentIndexChanged(QString)),
            this, SLOT(fontSizeChanged(QString)));


    textToolBar = addToolBar(tr("字体"));
    textToolBar->addWidget(fontCombo);
    textToolBar->addWidget(fontSizeCombo);
    textToolBar->addAction(boldAction);
    textToolBar->addAction(italicAction);
    textToolBar->addAction(underlineAction);

    QToolButton *pointerButton = new QToolButton;
    pointerButton->setCheckable(true);
    pointerButton->setChecked(true);
    pointerButton->setIcon(QIcon(":/images/pointer.png"));

    QToolButton *linePointerButton = new QToolButton;
    linePointerButton->setCheckable(true);
    linePointerButton->setIcon(QIcon(":/images/linepointer.png"));

    pointerTypeGroup = new QButtonGroup(this);
    pointerTypeGroup->addButton(pointerButton, int(SimulationScene::moveItem));
    pointerTypeGroup->addButton(linePointerButton, int(SimulationScene::insertLine));
    connect(pointerTypeGroup, SIGNAL(buttonClicked(int)),
            this, SLOT(pointerGroupClicked(int)));

    sceneScaleCombo = new QComboBox;
    QStringList scales;
    //  可供选择的背景缩放参数
    scales << tr("50%") << tr("75%") << tr("100%") << tr("125%") << tr("150%");
    sceneScaleCombo->addItems(scales);
    sceneScaleCombo->setCurrentIndex(2);
    connect(sceneScaleCombo, SIGNAL(currentIndexChanged(QString)),
            this, SLOT(sceneScaleChanged(QString)));

    pointerToolBar = addToolBar(tr("指针类型"));
    pointerToolBar->addWidget(pointerButton);
    pointerToolBar->addWidget(linePointerButton);
    pointerToolBar->addWidget(sceneScaleCombo);
}

/**
 * @brief MainWindow::createCellWidget  创建单元部件
 */
QWidget *MainWindow::createCellWidget(const QString &text, Items::ItemType type)
{

    Items item(type, itemMenu);
    QIcon icon(item.image());

    QToolButton *button = new QToolButton;
    button->setIcon(icon);  // 设置按键图标
    button->setIconSize(QSize(50, 50)); // 设置按键大小
    button->setCheckable(true); // 可选择状态
    buttonGroup->addButton(button, int(type));

    QGridLayout *layout = new QGridLayout;
    layout->addWidget(button, 0, 0, Qt::AlignHCenter);
    layout->addWidget(new QLabel(text), 1, 0, Qt::AlignCenter);

    QWidget *widget = new QWidget;
    widget->setLayout(layout);

    return widget;
}


//test
void MainWindow::setGetValueWindow()
{
    double outputNum = 0;
    //  遍历所有选择的项，如果为图，执行该部分代码
    foreach (QGraphicsItem *item, scene->selectedItems()) {
         if (item->type() == Items::Type)
             outputNum = qgraphicsitem_cast <Items *> (item)->getOutputNum();
     }

    setGetWindow = new IOset();
    setGetWindow->setModal(true);
    QObject::connect(this, SIGNAL(sendOutputValue(double)), setGetWindow, SLOT(getOutputValue(double)));
    emit sendOutputValue(outputNum);
    connect(setGetWindow,SIGNAL(sendInputValue(double)),this,SLOT(getInputValue(double)));
    setGetWindow->show();

}

void MainWindow::getInputValue(double inputNum)
{
    foreach (QGraphicsItem *item, scene->selectedItems()) {
         if (item->type() == Items::Type)
         {
             qgraphicsitem_cast <Items *> (item)->getItemType();
             qgraphicsitem_cast <Items *> (item)->setInputNum(inputNum);
             qgraphicsitem_cast <Items *> (item)->calculateResult(
                         qgraphicsitem_cast <Items *> (item)->getItemType(), inputNum);
         }

     }
}
