#include "arrow.h"

#include <qmath.h>
#include <QPen>
#include <QPainter>

Arrow::Arrow(Items *startItem, Items *endItem, QGraphicsItem *parent)
    : QGraphicsLineItem(parent)
{
    myStartItem = startItem;
    myEndItem = endItem;
    setFlag(QGraphicsItem::ItemIsSelectable, true);
    myColor = Qt::black;
    setPen(QPen(myColor, 2, Qt::SolidLine, Qt::RoundCap, Qt::RoundJoin));
}

/**
 * @brief Arrow::boundingRect   重写 QGraphicsLineItem 函数以检测碰撞
 *  我们需要重新实现这个函数，因为Arrow比QGraphicsLineItem的边界矩形大。
 *  图形场景使用边界矩形来知道场景的哪些区域需要更新。
 * @return  返回重写后的矩形 QRectF
 */
QRectF Arrow::boundingRect() const
{
    qreal extra = (pen().width() + 20) / 2.0;
    return QRectF(line().p1(), QSizeF(line().p2().x() - line().p1().x(), line().p2().y() - line().p1().y())).normalized().adjusted(-extra, -extra, extra, extra);
}

/**
 * @brief Arrow::shape  重写 QGraphicsLineItem 函数以检测是否选择
 * @return  返回一个带有箭头和路径的连接线 QPainterPath
 */
QPainterPath Arrow::shape() const
{
    QPainterPath path = QGraphicsLineItem::shape();
    path.addPolygon(arrowHead);
    return path;
}

/**
 * @brief Arrow::updatePosition 在起止项之间设立连接线
 */
void Arrow::updatePosition()
{
    QLineF line(mapFromItem(myStartItem, 0, 0), mapFromItem(myEndItem, 0, 0));
    setLine(line);
}

/**
 * @brief Arrow::paint  连接线绘制函数
 * @param painter   QPainter
 */
void Arrow::paint(QPainter *painter, const QStyleOptionGraphicsItem *, QWidget *)
{
    //  若起止项有重合，则不画线
    if(myStartItem->collidesWithItem(myEndItem))
        return;

    //  设置需要进行绘制的笔和刷子
    QPen myPen = pen();
    myPen.setColor(myColor);
    qreal arrowSize = 20;
    painter->setPen(myPen);
    painter->setBrush(myColor);
    QLineF centerLine(myStartItem->pos(), myEndItem->pos());
    QPolygonF endPolygon = myEndItem->polygon();
    QPointF p1 = endPolygon.first() + myEndItem->pos();
    QPointF p2;
    QPointF intersectPoint;
    QLineF polyLine;


    //  找到要绘制箭头的位置，即直线和结束项相交的地方。
    //  这是通过取多边形中每个点之间的线并检查它是否与箭头的线相交来完成。
    //  由于线的起点和终点被设置为项目的中心，箭头线应该与多边形的一条且仅一条线相交
    for(int i = 0; i < endPolygon.count(); i++)
    {
        p2 = endPolygon.at(i) + myEndItem->pos();
        polyLine = QLineF(p1, p2);
        QLineF::IntersectType intersectType = polyLine.intersect(centerLine, &intersectPoint);
        if(intersectType == QLineF::BoundedIntersection)
            break;
        p1 = p2;
    }
    setLine(QLineF(intersectPoint, myStartItem->pos()));


    //  计算x轴和箭头之间的夹角。把箭头转到这个角度。如果角度是负的，就改变箭头的方向
    double angle = std::atan2(-line().dy(), line().dx());
    QPointF arrowP1 = line().p1() + QPointF(sin(angle + M_PI / 3) * arrowSize,
                                       cos(angle + M_PI / 3) * arrowSize);
    QPointF arrowP2 = line().p1() + QPointF(sin(angle + M_PI - M_PI / 3) * arrowSize,
                                       cos(angle + M_PI - M_PI / 3) * arrowSize);

    arrowHead.clear();
    arrowHead << line().p1() << arrowP1 << arrowP2;

    //  如果选择了这条线，画两条与箭头的线平行的虚线表示
    painter->drawLine(line());
    painter->drawPolygon(arrowHead);
    if (isSelected()) {
        painter->setPen(QPen(myColor, 1, Qt::DashLine));
        QLineF myLine = line();
        myLine.translate(0, 4.0);
        painter->drawLine(myLine);
        myLine.translate(0,-8.0);
        painter->drawLine(myLine);
    }
}

