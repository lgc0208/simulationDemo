<h2 align="center"> 基于 PySide 6 的光通信系统仿真平台搭建探索 </h2>
<p align="center"><b>2021-2022大学生创新创业训练项目/电子工程学院/北京邮电大学</b></p>

<p align="center">
    <img src="https://badgen.net/github/license/lgc0208/simulationDemo/">
    <img src="https://badgen.net/github/commits/lgc0208/simulationDemo/master/">
    <img src="https://badgen.net/github/releases/lgc0208/simulationDemo/">    
    <img src="https://badgen.net/github/release/lgc0208/simulationDemo/">
    <img src="https://badgen.net/github/last-commit/lgc0208/simulationDemo/master/">
</p>

## 目录

- [环境依赖](#环境依赖)
- [目录结构描述](#目录结构描述)
- [项目简介](#项目简介)
- [运行方式](#运行方式)
- [贡献者](#贡献者)


## 环境依赖
- PySide6 6.3.1
- numpy 1.23.0
- matplotlib 3.3.3

## 目录结构描述

```
├── README.md              // 说明文档
├── LICENSE                // 开源协议
├── arrow.py               // 箭头类
├── ioset.py	           // 输入输出窗口类
├── items.py	           // 工具栏类
├── mainScene.py     	   // 主窗口构建类
├── nrzook.py     	   // NRZOOK 器件类
├── rz33ook.py     	   // RZ33OOK 器件类
├── rz50ook.py     	   // RZ50OOK 器件类
├── rz66ook.py     	   // RZ66OOK 器件类
├── simulationDemo_rc.py   // 初始化资源类
├── simulationDemo.py      // 项目启动入口
├── textItem.py     	   // 文本框类
├── ui_ioset.py     	   // 输入输出窗口的 UI 界面类
└── image                  // 图文件夹
```

## 项目简介

项目以Python 3为主要开发语言，借助QT官方提供的Pyside 6库进行可视化呈现。项目的组成部分包括了仿真软件主窗口MainWindow类，负责放置各类元器件的Items类，负责控制仿真软件窗口中文字的TextItem类，负责软件与用户的交互逻辑实现的IOSet类，负责为用户展示元器件信息的SimulationScene类以及负责仿真软件器件间通信逻辑的Arrow类。同时，针对后期可能加入的不同类型器件，我们规定了器件类所需要具有的结构。当开发者添加新的器件类时，只需要在仿真软件的主窗口类的对应位置中加入新器件类型的引用，即可完成新器件与软件平台的耦合。

**存在问题、建议及需要说明的情况：** 受技术所限，目前平台只能实现输入输出信号的瞬时仿真，不能连续仿真。另外器件参数的设置窗口目前是各器件公用的，使用时会降低一些体验感。后期将会对此做出针对性改进。目前已封装的器件均为理想模型，与实际器件相关特性仍有一定差距，后期考虑引入信道的色散、系统整体的热噪声和外界的高斯白噪声，使本平台仿真结果更接近实际结果。由于项目成员缺乏一定设计经验，目前平台整体外观较为简单，后期将提高其整体美观性。

## 运行方式

安装完成对应环境后，输入

```bash
python simulationDemo.py
```

## 贡献者
- [LIN Guocheng](https://github.com/lgc0208)
- [JIAN Jie](https://github.com/jessica-jane)
- [LI Shuyuan](https://github.com/JCM-lsy)
