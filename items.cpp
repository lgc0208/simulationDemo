#include "items.h"
#include "arrow.h"

#include <QGraphicsScene>
#include <QGraphicsSceneContextMenuEvent>
#include <QMenu>
#include <QPainter>

Items::Items(ItemType itemType, QMenu *contextMenu, QGraphicsItem *parent)
    :QGraphicsPolygonItem(parent)
{
    myItemType = itemType;
    myContextMenu = contextMenu;

    switch (myItemType) {
        case test:
            myPolygon << QPointF(-100, -100) << QPointF(100, -100)
                      << QPointF(100, 100) << QPointF(-100, 100)
                      << QPointF(-100, -100);
            break;
        default:
            myPolygon << QPointF(-120, -80) << QPointF(-70, 80)
                      << QPointF(120, 80) << QPointF(70, -80)
                      << QPointF(-120, -80);
            break;
    }
    setPolygon(myPolygon);
    setFlag(QGraphicsItem::ItemIsMovable, true);    // 设置项可移动
    setFlag(QGraphicsItem::ItemIsSelectable, true); // 设置项可选中
    setFlag(QGraphicsItem::ItemSendsGeometryChanges, true); // 设置通知可发送
}

/**
 * @brief Items::removeArrow    当与连接线相关的项被删除时，删除该连接线
 * @param arrow Arrow
 */
void Items::removeArrow(Arrow *arrow)
{
    int index = arrows.indexOf(arrow);
    if(index != -1)
        arrows.removeAt(index);
}

/**
 * @brief Items::removeArrows   当一个项被删除时，删除与这个项有关的所有连接线
 */
void Items::removeArrows()
{
    foreach (Arrow *arrow, arrows)
    {
        arrow->startItem()->removeArrow(arrow); // 起始项删除箭头
        arrow->endItem()->removeArrow(arrow);   // 终止项删除箭头
        scene()->removeItem(arrow); // 删除箭头项
        delete arrow;
    }
}

/**
 * @brief Items::addArrow   将箭头添加到箭头列表
 * @param arrow 要添加的箭头Arrow
 */
void Items::addArrow(Arrow *arrow)
{
    arrows.append(arrow);
}

/**
 * @brief Items::image  为工具箱中的工具按钮创建图标
 * @return QPixmap
 */
QPixmap Items::image() const
{
    QPixmap pixmap(250, 250);
    pixmap.fill(Qt::transparent);
    QPainter painter(&pixmap);
    painter.setPen(QPen(Qt::black, 8));
    painter.translate(125, 125);
    painter.drawPolyline(myPolygon);

    return pixmap;
}

/**
 * @brief Items::contextMenuEvent   鼠标右键时显示菜单，默认情况下不选择项目
 * @param event QGraphicsSceneContextMenuEvent
 */
void Items::contextMenuEvent(QGraphicsSceneContextMenuEvent *event)
{
    scene()->clearSelection();  // 清除其他项的选中状态
    setSelected(true);  // 此项可选，则该项为选中状态
    myContextMenu->exec(event->screenPos());    // 在事件发生的地方显示菜单
}

/**
 * @brief Items::itemChange 如果项移动，更新箭头连接的位置
 * @param change    项移动事件GraphicsItemChange
 * @param value     QVariant
 * @return 箭头连接线更新结果
 */
QVariant Items::itemChange(GraphicsItemChange change, const QVariant &value)
{
    if(change == QGraphicsItem::ItemPositionChange)
    {
        foreach(Arrow *arrow, arrows)
        {
            arrow->updatePosition();
        }
    }
    return value;
}
