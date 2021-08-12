/**
* @file     ioset.h
* @brief    设置对应项的输入及显示输出的功能文件
* @details  主要包含连接线功能的函数声明
* @author   LIN Guocheng
* @date     2021-8-12
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
#ifndef IOSET_H
#define IOSET_H

#include "items.h"
#include <QDialog>

namespace Ui {
class IOset;
}

class IOset : public QDialog
{
    Q_OBJECT

public:
    explicit IOset(QWidget *parent = nullptr);
    ~IOset();
    //Items item;
    //void setItem(Items item);

private slots:
    void on_SetInput_clicked();

    void getOutputValue(double outputNum);


signals:
    void sendInputValue(double inputNum);

private:
    Ui::IOset *ui;

};

#endif // IOSET_H
