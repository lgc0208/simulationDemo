/**
* @file     SimulationScene.h
* @brief    项目场景函数头文件
* @details  主要包含SimulationScene类的声明
* @author   LIN Guocheng
* @date     2021-8-13
* @version  1.0.0
**********************************************************************************
* @attention
* QT版本：5.12.11
* @par 修改日志:
* <table>
* <tr><th>Date        <th>Version  <th>Author    <th>Description
* <tr><td>2021/08/06  <td>0.0.1    <td>LIN Guocheng  <td>创建初始版本
* <tr><td>2021/08/13  <td>1.0.0    <td>LIN Guocheng  <td>完成第一代基础版本的适配
* </table>
*
**********************************************************************************
*/
#ifndef SIMULATIONSCENE_H
#define SIMULATIONSCENE_H
#include <QGraphicsScene>
#include "items.h"
#include "textItem.h"

QT_BEGIN_NAMESPACE
class QGraphicsSceneMouseEvent;
class QMenu;
class QPointF;
class QGraphicsLineItem;
class QFont;
class QGraphicsTextItem;
class QColor;
QT_END_NAMESPACE

class SimulationScene : public QGraphicsScene
{
    Q_OBJECT

public:
    enum Mode {insertItem, insertLine, insertText, moveItem};   // 4 种运行模式：插入项，插入连接线，插入文本，移动项

    explicit SimulationScene(QMenu *itemMenu, QObject *parent = 0);
    QFont font() const { return myFont;}

    void setFont(const QFont &font);    // 设置字体

public slots:
    void setMode(SimulationScene::Mode mode);    // 设置当前模式
    void setItemType(Items::ItemType type); // 设置项种类
    void editorLostFocus(TextItem *item);   // 文本框失去焦点

signals:
    void itemInserted(Items *item); // 插入项
    void textInserted(QGraphicsTextItem *item); // 插入文本框
    void itemSelected(QGraphicsItem *item); // 选择项

protected:
    void mousePressEvent(QGraphicsSceneMouseEvent *mouseEvent) override;    // 重写鼠标点击事件
    void mouseMoveEvent(QGraphicsSceneMouseEvent *mouseEvent) override;     // 重写鼠标移动事件
    void mouseReleaseEvent(QGraphicsSceneMouseEvent *mouseEvent) override;  // 重写鼠标松开事件

private:
    bool isItemChange(int type);    // 判断项是否改变
    Items::ItemType myItemType;
    QMenu *myItemMenu;
    Mode myMode;
    bool leftButtonDown;
    QPointF startPoint;
    QGraphicsLineItem *line;
    QFont myFont;
    QColor myItemColor;
    QColor myTextColor;
    QColor myLineColor;
    TextItem *textItem;
};

#endif // SIMULATIONSCENE_H
