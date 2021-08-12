/**
* @file     arrow.h
* @brief    项目连接线函数头文件
* @details  主要包含连接线功能的函数声明
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

#ifndef ARROW_H
#define ARROW_H

#include "items.h"
#include <QGraphicsLineItem>

QT_BEGIN_NAMESPACE
class QGraphicsPolygonItem;
class QGraphicsLineItem;
class QGraphicsScene;
class QRectF;
class QGraphicsSceneMouseEvent;
class QPainterPath;
QT_END_NAMESPACE

class Arrow : public QGraphicsLineItem
{
public:
    enum {Type = UserType + 4};

    Arrow(Items *startItem, Items *endItem, QGraphicsItem *parent = 0);

    int type() const override { return Type;}
    QRectF boundingRect() const override;
    QPainterPath shape() const override;
    Items *startItem() const { return myStartItem;}
    Items *endItem() const { return myEndItem;}

    void updatePosition();  // 更新起终点坐标

protected:
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = 0) override;    // 绘制连接线

private:
    Items *myStartItem; // 起始项
    Items *myEndItem;   // 终止项
    QPolygonF arrowHead;    // QT 向量
    QColor myColor; // 颜色
};

#endif // ARROW_H
