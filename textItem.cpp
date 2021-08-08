#include "textItem.h"
#include "stimulationScene.h"

TextItem::TextItem(QGraphicsItem *parent)
    : QGraphicsTextItem(parent)
{
    setFlag(QGraphicsItem::ItemIsMovable);
    setFlag(QGraphicsItem::ItemIsSelectable);
}

/**
 * @brief TextItem::itemChange
 * @param change
 * @param value
 * @return
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
