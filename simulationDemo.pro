QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    arrow.cpp \
    ioset.cpp \
    items.cpp \
    main.cpp \
    mainwindow.cpp \
    simulationScene.cpp \
    textItem.cpp

HEADERS += \
    arrow.h \
    ioset.h \
    items.h \
    mainwindow.h \
    simulationScene.h \
    textItem.h

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += \
    simulationDemo.qrc

msvc {
QMAKE_CFLAGS += /utf-8
QMAKE_CXXFLAGS += /utf-8
}

FORMS += \
    ioset.ui
