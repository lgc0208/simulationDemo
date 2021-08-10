/**
* @file     items.h
* @brief    项目功能项函数声明头文件
* @details  主要包含功能项具体的函数声明
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
* <tr><td>2021/08/09  <td>0.0.2    <td>LIN Guocheng  <td>增加器件计算函数
* <tr><td>2021/08/10  <td>0.0.3    <td>LIN Guocheng  <td>将器件输入输出值改为私有属性，并增加get/set函数
* </table>
*
**********************************************************************************
*/

#ifndef ITEMS_H
#define ITEMS_H

#include <QGraphicsPixmapItem>
#include <QList>

QT_BEGIN_NAMESPACE
class QPixmap;
class QGraphicsItem;
class QGraphicsScene;
class QTextEdit;
class QGraphicsSceneMouseEvent;
class QMenu;
class QGraphicsSceneContextMenuEvent;
class QPainter;
class QStyleOptionGraphicsItem;
class QWidget;
class QPolygonF;
QT_END_NAMESPACE

class Arrow;

class Items : public QGraphicsPolygonItem
{

public:
    enum { Type = UserType + 15};   // 自定义图形象类型的最小值
    enum ItemType { test }; // 与可选择的项一一对应

    Items(ItemType itemType, QMenu *contextMenu, QGraphicsItem *parent = 0);

    void removeArrow(Arrow *arrow);
    void removeArrows();
    ItemType itemType() const { return myItemType;}
    QPolygonF polygon() const { return myPolygon;}
    void addArrow(Arrow *arrow);
    QPixmap image() const;  // 将可选择的项绘制到 QPixmap 上
    int type() const override { return Type;}

    //  器件具体功能实现
    void setInputNum(double inputNum);
    double getOutputNum();
    double calculateResult(ItemType myItemType, double inputNum);

protected:
    void contextMenuEvent(QGraphicsSceneContextMenuEvent *event) override;
    QVariant itemChange(GraphicsItemChange change, const QVariant &value) override;

private:
    double inputNum = 0;
    double outputNum = 0;
    ItemType myItemType;
    QPolygonF myPolygon;
    QMenu *myContextMenu;
    QList <Arrow *> arrows; // 令可选项知道什么时候移动和更新箭头
};

#endif // ITEMS_H
