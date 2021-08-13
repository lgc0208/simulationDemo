/**
* @file     ioset.cpp
* @brief    设置对应项的输入及显示输出的功能文件
* @details  主要包含连接线功能的函数实现
* @author   LIN Guocheng
* @date     2021-8-14
* @version  1.0.1
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
* </table>
*
**********************************************************************************
*/

#include "ioset.h"
#include "items.h"
#include "ui_ioset.h"

/**
 * @brief IOset::IOset  ui类对应构造函数
 * @param parent   QWidget
 */
IOset::IOset(QWidget *parent)
    : QDialog(parent),
    ui(new Ui::IOset)
{
    ui->setupUi(this);
    setWindowTitle(tr("Set Input or Get Output"));
}

/**
 * @brief IOset::~IOset ui类对应析构函数
 */
IOset::~IOset()
{
    delete ui;
}

/**
 * @brief IOset::getOutputValue 获取主窗口对应项的输出值，并显示在文本框中
 * @param outputNum 输出值
 */
void IOset::getOutputValue(double outputNum)
{
    QString outputStr;

    ui->outputValue->setText(outputStr.setNum(outputNum));
}

/**
 * @brief IOset::on_SetInput_clicked    Set Input 按钮点击事件，将inputValue更新到item的inputNum中
 * @param item  需要更新的item
 */
void IOset::on_SetInput_clicked()
{
    bool ok;
    QString valueStr = ui->inputValue->text();  // 获取文本框内容
    if(valueStr == NULL)
            return;
    double inputValue = valueStr.toDouble(&ok);
    emit sendInputValue(inputValue);

}



