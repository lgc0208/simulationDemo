/**
* @file     textItem.h
* @brief    可编辑文本项类声明头文件
* @details  主要包含可编辑文本项类声明
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

#ifndef TEXTITEM_H
#define TEXTITEM_H

#include <QGraphicsTextItem>
#include <QPen>

QT_BEGIN_NAMESPACE
class QFocusEvent;
class QGraphicsItem;
class QGraphicsScene;
class QGraphicsSceneMouseEvent;
QT_END_NAMESPACE

class TextItem : public QGraphicsTextItem
{
    Q_OBJECT    // 只有加入了Q_OBJECT，你才能使用QT中的signal和slot机制

public:
    enum { Type = UserType + 3};

    TextItem(QGraphicsItem *parent = 0);

    int type() const override {return Type;}

signals:
    void lostFocus(TextItem *item); // 文本项失去焦点
    void selectedChange(QGraphicsItem *item);   // 文本项被选中

protected:
    QVariant itemChange(GraphicsItemChange change, const QVariant &value) override; // 当文本项失去焦点时，通知主页面
    void focusOutEvent(QFocusEvent *event) override;    // 当文本项被选中时，通知主页面
    void mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event) override;   // 重写处理鼠标事件的函数
};

#endif // TEXTITEM_H
