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
   // void on_SetInput_clicked();

    void on_GetOutput_clicked();

private:
    Ui::IOset *ui;

};

#endif // IOSET_H
