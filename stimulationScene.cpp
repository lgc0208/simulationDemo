#include "stimulationScene.h"
#include "arrow.h"
#include <QTextCursor>
#include <QGraphicsSceneMouseEvent>
#include <iostream>

StimulationScene::StimulationScene(QMenu *itemMenu, QObject *parent)
    :QGraphicsScene(parent)
{
    myItemMenu = itemMenu;
    myMode = moveItem;
    myItemType = Items::test;
    line = 0;
    textItem = 0;
    myItemColor = Qt::white;
    myTextColor = Qt::black;
    myLineColor = Qt::black;
}

/**
 * @brief StimulationScene::setFont 设置字体
 * @param font  QFont字体
 */
void StimulationScene::setFont(const QFont &font)
{
    myFont = font;
    if(isItemChange(TextItem::Type))
    {
        QGraphicsTextItem *item = qgraphicsitem_cast <TextItem *> (selectedItems().first());
        if(item)
            item->setFont(myFont);
    }
}

/**
 * @brief StimulationScene::setMode 设置操作模式
 * @param mode  Mode操作模式类型
 */
void StimulationScene::setMode(Mode mode)
{
    myMode = mode;
}

/**
 * @brief StimulationScene::setItemType 设置可选项的种类
 * @param type  项的种类ItemType
 */
void StimulationScene::setItemType(Items::ItemType type)
{
    myItemType = type;
}

/**
 * @brief StimulationScene::editorLostFocus 文本框失去焦点时，如果项目没有文本，则删除它
 * @param item  TextItem
 */
void StimulationScene::editorLostFocus(TextItem *item)
{
    QTextCursor cursor = item->textCursor();
    cursor.clearSelection();
    item->setTextCursor(cursor);

    if (item->toPlainText().isEmpty()) {
        removeItem(item);
        item->deleteLater();
    }
}

/**
 * @brief StimulationScene::mousePressEvent 处理鼠标点击事件
 * @param mouseEvent    QGraphicsSceneMouseEvent
 */
void StimulationScene::mousePressEvent(QGraphicsSceneMouseEvent *mouseEvent)
{
    //  如果不是左键点击，则跳过此函数
    if (mouseEvent->button() != Qt::LeftButton)
        return;

    Items *item;
    switch (myMode) {
        //  插入项
        case insertItem:
            item = new Items(myItemType, myItemMenu);
            item->setBrush(myItemColor);
            addItem(item);
            item->setPos(mouseEvent->scenePos());
            emit itemInserted(item);
            break;
        //  插入连接线
        case insertLine:
            line = new QGraphicsLineItem(QLineF(mouseEvent->scenePos(),
                                        mouseEvent->scenePos()));
            line->setPen(QPen(myLineColor, 2));
            addItem(line);
            break;
        //  插入文本
        case insertText:
            textItem = new TextItem();
            textItem->setFont(myFont);
            textItem->setTextInteractionFlags(Qt::TextEditorInteraction);
            textItem->setZValue(1000.0);
            connect(textItem, SIGNAL(lostFocus(DiagramTextItem*)),
                    this, SLOT(editorLostFocus(DiagramTextItem*)));
            connect(textItem, SIGNAL(selectedChange(QGraphicsItem*)),
                    this, SIGNAL(itemSelected(QGraphicsItem*)));
            addItem(textItem);
            textItem->setDefaultTextColor(myTextColor);
            textItem->setPos(mouseEvent->scenePos());
            emit textInserted(textItem);
    default:
        ;
    }
    QGraphicsScene::mousePressEvent(mouseEvent);
}

/**
 * @brief StimulationScene::mouseMoveEvent  调用 QGraphicsScene::mouseMoveEvent 处理项的移动
 * @param mouseEvent    QGraphicsSceneMouseEvent
 */
void StimulationScene::mouseMoveEvent(QGraphicsSceneMouseEvent *mouseEvent)
{
    //  模式为插入连接线且屏幕区域内存在连接线
    if (myMode == insertLine && line != 0) {
        QLineF newLine(line->line().p1(), mouseEvent->scenePos());
        line->setLine(newLine);
    } else if (myMode == moveItem) {
        QGraphicsScene::mouseMoveEvent(mouseEvent);
    }
}

/**
 * @brief StimulationScene::mouseReleaseEvent   处理鼠标松开后的事件
 * @param mouseEvent    QGraphicsSceneMouseEvent
 */
void StimulationScene::mouseReleaseEvent(QGraphicsSceneMouseEvent *mouseEvent)
{
    //  判断是否需要加入连接线
    if (line != 0 && myMode == insertLine) {
        QList<QGraphicsItem *> startItems = items(line->line().p1());
        if (startItems.count() && startItems.first() == line)
            startItems.removeFirst();
        QList<QGraphicsItem *> endItems = items(line->line().p2());
        if (endItems.count() && endItems.first() == line)
            endItems.removeFirst();

        removeItem(line);
        delete line;

        //  判断连接线的两侧是否存在不同的两个项
        if (startItems.count() > 0 && endItems.count() > 0 &&
            startItems.first()->type() == Items::Type &&
            endItems.first()->type() == Items::Type &&
            startItems.first() != endItems.first()) {
            Items *startItem = qgraphicsitem_cast <Items *> (startItems.first());
            Items *endItem = qgraphicsitem_cast <Items *> (endItems.first());
            Arrow *arrow = new Arrow(startItem, endItem);
            startItem->addArrow(arrow);
            endItem->addArrow(arrow);
            arrow->setZValue(-1000.0);
            addItem(arrow);
            arrow->updatePosition();
        }
    }
    line = 0;
    QGraphicsScene::mouseReleaseEvent(mouseEvent);
}

/**
 * @brief StimulationScene::isItemChange    检查所选项是否存在并且是否是指定类型
 * @param type  int类型，与enum中的列表对应
 * @return  若对应，返回true；否则返回false
 */
bool StimulationScene::isItemChange(int type)
{
    foreach (QGraphicsItem *item, selectedItems()) {
        if (item->type() == type)
            return true;
    }
    return false;
}
