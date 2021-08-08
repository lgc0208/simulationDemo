/**
* @file     main.cpp
* @brief    QT 程序运行主函数
* @details  主要包含主窗口界面的展示函数
* @author   LIN Guocheng
* @date     2021-8-6
* @version  V0.0.1
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

#pragma execution_character_set("utf-8")
#include "mainwindow.h"

#include <QApplication>

int main(int argv, char *args[])
{
    Q_INIT_RESOURCE(stimulationDemo);

    QApplication app(argv, args);
    MainWindow mainWindow;
    mainWindow.setGeometry(100, 100, 800, 500);
    mainWindow.show();

    return app.exec();
}
