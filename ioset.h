/**
* @file     ioset.h
* @brief    设置对应项的输入及显示输出的功能文件
* @details  主要包含连接线功能的函数声明
* @author   LIN Guocheng
* @date     2021-8-14
* @version  1.0.2
**********************************************************************************
* @attention
* QT版本：5.12.11
* @par 修改日志:
* <table>
* <tr><th>Date        <th>Version  <th>Author    <th>Description
* <tr><td>2021/08/06  <td>0.0.1    <td>LIN Guocheng  <td>创建初始版本
* <tr><td>2021/08/12  <td>0.0.2    <td>LIN Guocheng  <td>增加与主页面交互的输入输出值窗口
* <tr><td>2021/08/13  <td>1.0.0    <td>LIN Guocheng  <td>完成第一代基础版本的适配
* <tr><td>2021/08/14  <td>1.0.1    <td>LIN Guocheng  <td>增加了子窗口名
* <tr><td>2021/08/14  <td>1.0.2    <td>LIN Guocheng  <td>补充子窗口的输入值显示,将getOutputValue(double)修改为getIOValue(double,double)
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

private slots:
    void on_SetInput_clicked();
    void getIOValue(double inputNum, double outputNum);


signals:
    void sendInputValue(double inputNum);

private:
    Ui::IOset *ui;

};

#endif // IOSET_H
