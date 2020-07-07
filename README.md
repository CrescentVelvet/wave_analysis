## wave_analysis

# 用到的库

numpy1.16.4

PyQt5

matplotlib3.0.3

pylab

serial

pyqtgraph0.11.0

dicttoxml-1.7.4

# 踩坑记录

pyqt5中调用pyqtgraph绘图，需要新建widget并添加layout，将其设置为主widget。

ui_window中无法调用未实例化的绘图变量，在image_draw中设置为全局变量。

打包EXE文件
```sh
pyinstaller -F -i .\logo.ico .\main_window.py
```