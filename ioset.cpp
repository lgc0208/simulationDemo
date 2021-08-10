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
}

/**
 * @brief IOset::~IOset ui类对应析构函数
 */
IOset::~IOset()
{
    delete ui;
}
/*
void IOset::setItem(Items item)
{
   //this->item = item;
}*/

/**
 * @brief IOset::on_SetInput_clicked    Set Input 按钮点击事件，将inputValue更新到item的inputNum中
 * @param item  需要更新的item
 *//*
void IOset::on_SetInput_clicked()
{
    bool ok;
    QString tmpStr;
    QString valueStr = ui->inputValue->text();  // 获取文本框内容
    if(valueStr == NULL)
            return;
    double inputValue = valueStr.toDouble(&ok);
    item.setInputNum(inputValue);
}*/

/**
 * @brief IOset::on_GetOutput_clicked   Get Output 按钮点击事件，将outputValue更新到标签栏
 * @param item  正在操作的item
 */
void IOset::on_GetOutput_clicked()
{
    //double outputValue = item.getOutputNum();
    bool ok;
    QString tmpStr;
    QString valueStr = ui->inputValue->text();  // 获取文本框内容
    if(valueStr == NULL)
            return;
    double inputValue = valueStr.toDouble(&ok);

    double outputValue = 2*inputValue;

    QString outputStr;
    ui->outputValue->setText(outputStr.setNum(outputValue));
}

