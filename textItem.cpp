/**
* @file     textItem.cpp
* @brief    文本编辑框函数文件
* @details  主要包含文本编辑框功能的实现
*           textItem类继承了QGraphicsTextItem，并添加了移动可编辑文本项的可能性。
*           可编辑的QGraphicsTextItems被设计成在适当的位置进行固定，当用户单击项目时开始编辑。
*           使用textItem，编辑以双击开始，留下可进行交互和移动的单单击。
* @author   LIN Guocheng
* @date     2021-8-9
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

#include "textItem.h"
#include "stimulationScene.h"

TextItem::TextItem(QGraphicsItem *parent)
    : QGraphicsTextItem(parent)
{
    setFlag(QGraphicsItem::ItemIsMovable);
    setFlag(QGraphicsItem::ItemIsSelectable);
}

/**
 * @brief TextItem::itemChange  当项目被选中时发出selectedChanged信号。
 * 主窗口使用这个信号来更新小部件，这些小部件将字体属性显示为选定文本项的字体
 * @param change    GraphicsItemChange
 * @param value     QVariant
 * @return  selectedChanged信号
 */
QVariant TextItem::itemChange(GraphicsItemChange change, const QVariant &value)
{
    if(change == QGraphicsItem::ItemSelectedHasChanged)
        emit selectedChange(this);
    return value;
}

/**
 * @brief TextItem::focusOutEvent   若文本框为空，则在失去文本项焦点的时候删除该文本项
 * @param event QFocusEvent
 */
void TextItem::focusOutEvent(QFocusEvent *event)
{
    setTextInteractionFlags(Qt::NoTextInteraction);
    emit lostFocus(this);
    QGraphicsTextItem::focusOutEvent(event);
}

/**
 * @brief TextItem::mouseDoubleClickEvent   当发生双击事件后，调用QGraphicsTextItem使项可编辑
 * @param event 鼠标双击事件
 */
void TextItem::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)
{
    if(textInteractionFlags() == Qt::NoTextInteraction)
        setTextInteractionFlags(Qt::TextEditorInteraction);
    QGraphicsTextItem::mouseDoubleClickEvent(event);
}
