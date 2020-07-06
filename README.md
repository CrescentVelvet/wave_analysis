## wave_analysis
# 踩坑记录
pyqt5中调用pyqtgraph绘图，需要新建widget并添加layout，将其设置为主widget。

ui_window中无法调用未实例化的绘图变量，在image_draw中设置为全局变量。
