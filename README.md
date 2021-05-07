## wave_analysis

# 用到的库

python 3.5.4

PyQt 5.13.0

serial 0.0.97

pyserial 3.4

numpy 1.16.4

pyqtgraph 0.11.0

matplotlib 3.0.3

dicttoxml 1.7.4

# 踩坑记录

pyqt5中调用pyqtgraph绘图，需要新建widget并添加layout，将其设置为主widget。

ui_window中无法调用未实例化的绘图变量，在image_draw中设置为全局变量。

打包EXE文件
```sh
pyinstaller -F -i .\logo.ico .\main_window.py
```

## ubuntu环境配置

```sh
pip install pyqtgraph
pip install serial --ignore-installed PyYAML
pip install pyserial
pip install dicttoxml
```
