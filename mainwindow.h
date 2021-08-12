/**
* @file     mainwindow.h
* @brief    项目主函数头文件
* @details  主要包含主窗口界面的函数声明
* @author   LIN Guocheng
* @date     2021-8-6
* @version  0.0.1
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


#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "items.h"
#include "ioset.h"
#include <QMainWindow>

class SimulationScene;

//  宏定义
QT_BEGIN_NAMESPACE
class QAction;
class QToolBox;
class QSpinBox;
class QComboBox;
class QFontComboBox;
class QButtonGroup;
class QLineEdit;
class QGraphicsTextItem;
class QFont;
class QToolButton;
class QAbstractButton;
class QGraphicsView;
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow();

private slots:
    void buttonGroupClicked(int id);
    void deleteItem();
    void pointerGroupClicked(int id);
    void bringToFront();
    void sendToBack();
    void itemInserted(Items *item);
    void textInserted(QGraphicsTextItem *item);
    void currentFontChanged(const QFont &font);
    void fontSizeChanged(const QString &size);
    void sceneScaleChanged(const QString &scale);
    void handleFontChange();
    void itemSelected(QGraphicsItem *item);
    void about();
    void setGetValueWindow(); // 唤醒窗口

private:
    void createToolBox();   // 创建工具箱
    void createActions();   // 槽函数连接
    void createMenus();  // 创建菜单栏
    void createToolbars();  // 创建工具栏
    QWidget *createBackgroundCellWidget(const QString &text,
                                        const QString &image);
    QWidget *createCellWidget(const QString &text,
                              Items::ItemType type);
    QMenu *createColorMenu(const char *slot, QColor defaultColor);
    QIcon createColorToolButtonIcon(const QString &image, QColor color);
    QIcon createColorIcon(QColor color);

    SimulationScene    *scene;
    QGraphicsView       *view;

    //  创建操作行为
    QAction *exitAction;
    QAction *addAction;
    QAction *deleteAction;
    QAction *setGetAction;

    QAction *toFrontAction;
    QAction *sendBackAction;
    QAction *aboutAction;

    QAction *boldAction;
    QAction *underlineAction;
    QAction *italicAction;
    QAction *textAction;
    QAction *fillAction;
    QAction *lineAction;

    //  创建菜单
    QMenu   *fileMenu;
    QMenu   *itemMenu;
    QMenu   *AboutMenu;

    //  创建工具栏
    QToolBar    *textToolBar;
    QToolBar    *editToolBar;
    QToolBar    *colorToolBar;
    QToolBar    *pointerToolBar;

    //  创建组合框
    QComboBox   *sceneScaleCombo;
    QComboBox   *fontSizeCombo;
    QFontComboBox    *fontCombo;
    QComboBox *itemColorCombo;
    QComboBox *textColorCombo;

    QToolBox    *toolBox;
    QButtonGroup    *buttonGroup;
    QButtonGroup    *pointerTypeGroup;

    //  test
    IOset       *setGetWindow;
};

#endif // MAINWINDOW_H
