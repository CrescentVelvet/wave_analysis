#coding=utf-8
from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg \
import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Point import Point
import sys
import serial.tools.list_ports
import time
import collect_data

# 为了在ui_window里调用，使用了全局变量
# 主体界面显示
win = pg.GraphicsLayoutWidget(show=False)
win.setWindowTitle('wave display')
# 显示鼠标坐标
label = pg.LabelItem(justify='right')
win.addItem(label)
# 添加两个画图界面：上图p1，下图p2
p1 = win.addPlot(row=1, col=0)
p2 = win.addPlot(row=2, col=0)
# 添加下图选区
region = pg.LinearRegionItem()
# 显示鼠标十字线
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
# 添加随机数据
data1 = 1500 * pg.gaussianFilter(np.random.random(size=1000), 10) + 300 * np.random.random(size=1000)
vb = p1.vb
ptr = 0

#***
bps = 115200
time_out = 1
port_list = list(serial.tools.list_ports.comports())
if len(port_list) < 1:
    print("当前没有插入USB设备")
    print("请插入USB设备")
    # ser = 0
    sys.exit()
else:
    print("当前已插入USB设备的COM如下，前为序号，后为COM编号：")
    for i in range(len(port_list)):
        print(i, '---', serial.Serial(list(port_list[i])[0], bps, timeout=time_out).name)
    # COM_NUM = input('Please input an order number to choose a COM:')
    ser = serial.Serial(list(port_list[0])[0], bps, timeout=time_out)

cmd_query_data = bytes.fromhex('fa f5 01 02 00 00 0e fe') # 查询数据
cmd_query_param = bytes.fromhex('fa f5 01 01 00 00 0f fe') # 查询参数
cmd_enable_MCA = bytes.fromhex('fa f5 01 00 00 00 10 fe') # enable_MCA
cmd_disable_MCA = bytes.fromhex('fa f5 02 00 00 00 0f fe') # disable_MCA
cmd_query_data_and_clear = bytes.fromhex('fa f5 02 02 00 00 0d fe') # 查询数据并清零
cmd_query_data_and_param = bytes.fromhex('fa f5 03 02 00 00 0c fe') # 查询数据和参数
cmd_query_data_and_param_and_clear = bytes.fromhex('fa f5 04 02 00 00 0b fe') # 查询数据和参数并清零数据

# matplotlib画布基类
class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(facecolor = 'white')
        self.fig.set_label('time (s)')
        self.ax = self.fig.add_subplot(111) # abc，a*b网格的第c个图
        self.ax.set_title('Original Wave')
        self.ax.set_ylabel(r'$Amplitude(V)$')
        self.ax.set_xticklabels( ('0', '1.0', '2.0', '3.0', '4.0',  '5.0'))
        self.ax.xlable = ('time(s)')
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
                                QtWidgets.QSizePolicy.Expanding,
                                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class DrawPicture(object):
    # 移动下图选区改变上图
    def update():
        region.setZValue(10)
        minX, maxX = region.getRegion()
        p1.setXRange(minX, maxX, padding=0)

    # 移动上图改变下图选区
    def updateRegion(window, viewRange):
        rgn = viewRange[0]
        region.setRegion(rgn)

    # 显示鼠标十字线
    def mouseMoved(evt):
        pos = evt[0]
        if p1.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            # print(mousePoint)
            index = int(mousePoint.x())
            if index > 0 and index < len(data1):
                label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>" % (mousePoint.x(), data1[index]))
                label.setPos(mousePoint.x(), mousePoint.y())
            vLine.setPos(mousePoint.x())
            hLine.setPos(mousePoint.y())


# 单个画布
# 添加pyqtgraph画布
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        # 添加layout用于pyqtgraph绘制
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        # 进行下图选区
        region.setZValue(10)
        p2.addItem(region, ignoreBounds=True)
        p1.setAutoVisible(y=True)
        self.curve_1 = p1.plot(data1, pen="r")
        self.curve_2 = p2.plot(data1, pen="w")
        # 设置选区初始范围
        region.setRegion([250, 350])
        minX, maxX = region.getRegion()
        p1.setXRange(minX, maxX, padding=0)
        # 移动下图选区改变上图
        region.sigRegionChanged.connect(DrawPicture.update)
        # 移动上图改变下图选区
        p1.sigRangeChanged.connect(DrawPicture.updateRegion)
        # 添加鼠标十字线
        p1.addItem(vLine, ignoreBounds=True)
        p1.addItem(hLine, ignoreBounds=True)
        # 十字线跟随鼠标移动
        proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=DrawPicture.mouseMoved)
        p1.proxy = proxy
        layout.addWidget(win)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(5000)

    # 更新数据
    def update(self):
        global p1, ptr, ser, cmd_query_data, cmd_query_data_and_clear, cmd_query_data_and_param_and_clear, cmd_query_data_and_param
        # data1 = 1500 * pg.gaussianFilter(np.random.random(size=1000), 10) + 300 * np.random.random(size=1000)
        ser.write(cmd_query_data_and_param_and_clear)
        recv = ser.read(10240).hex()
        # print(recv)
        parsed = collect_data.parse_signal_and_params(recv)
        print(parsed)
        data1 = np.array(parsed['DATA'], dtype=np.int64)
        self.curve_1.setData(data1)
        self.curve_2.setData(data1)
        

# 单个画布
# 添加matplotlib画布
# class MplWidget(QtWidgets.QWidget):
#     def __init__(self, parent = None):
#         QtWidgets.QWidget.__init__(self, parent)
        # self.canvas = MplCanvas()
        # self.vbl = QtWidgets.QVBoxLayout()
        # self.vbl.addWidget(self.canvas)
        # self.setLayout(self.vbl)

# # 用于测试绘图
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     # 主体界面显示，上图p1，下图p2
#     win = pg.GraphicsLayoutWidget(show=True)
#     win.setWindowTitle('wave display')
#     # 显示鼠标坐标
#     label = pg.LabelItem(justify='right')
#     win.addItem(label)
#     # 添加两个画图界面
#     p1 = win.addPlot(row=1, col=0)
#     p2 = win.addPlot(row=2, col=0)
#     # 进行下图选区
#     region = pg.LinearRegionItem()
#     region.setZValue(10)
#     p2.addItem(region, ignoreBounds=True)
#     p1.setAutoVisible(y=True)
#     # 添加随机数据
#     data1 = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
#     data2 = 15000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
#     p1.plot(data1, pen="r")
#     p1.plot(data2, pen="g")
#     p2.plot(data1, pen="w")
#     # 由下图选区更新上图
#     region.sigRegionChanged.connect(DrawPicture.update)
#     p1.sigRangeChanged.connect(DrawPicture.updateRegion)
#     # 设置选区初始范围
#     region.setRegion([1000, 2000])
#     # 显示鼠标十字线
#     vLine = pg.InfiniteLine(angle=90, movable=False)
#     hLine = pg.InfiniteLine(angle=0, movable=False)
#     p1.addItem(vLine, ignoreBounds=True)
#     p1.addItem(hLine, ignoreBounds=True)
#     vb = p1.vb
#     proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=DrawPicture.mouseMoved)
#     sys.exit(app.exec_())