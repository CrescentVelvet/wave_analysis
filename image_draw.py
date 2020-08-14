'''
Author       : velvet
Date         : 2020-08-07 22:37:28
LastEditTime : 2020-08-14 20:33:52
LastEditors  : velvet
Description  : 
FilePath     : \wave_analysis\image_draw.py
'''
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
import threading
import queue

class image_flag:
    sim_flag = 1 # 仿真测试开关
    thread_flag = 0 # 多线程开关
    start_flag = 0# 采集数据开关
    clear_flag = 0# 清零数据开关

class image_control:
    # 开始采集数据
    def start_to_collect():
        image_flag.start_flag = 1
        print("开始采集数据")
    
    # 停止采集数据
    def stop_to_collect():
        image_flag.start_flag = 0
        print("停止采集数据")
    
    # 清零全部数据
    def clear_data():
        image_flag.clear_flag = 1
        print("数据已全部清零")

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

if image_flag.sim_flag == 0:
    print("现在是实际测试")
    bps = 115200
    time_out = 1
    port_list = list(serial.tools.list_ports.comports())
    # 输入端口序号
    # for i in range(len(port_list)):
        # print(i, '---', serial.Serial(list(port_list[i])[0], bps, timeout=time_out).name)
    # COM_NUM = input('Please input an order number to choose a COM:')
    # ser = serial.Serial(list(port_list[COM_NUM])[0], bps, timeout=time_out)
    ser = serial.Serial(list(port_list[0])[0], bps, timeout=time_out)
    cmd_query_data = bytes.fromhex('fa f5 01 02 00 00 0e fe') # 查询数据
    cmd_query_param = bytes.fromhex('fa f5 01 01 00 00 0f fe') # 查询参数
    cmd_enable_MCA = bytes.fromhex('fa f5 01 00 00 00 10 fe') # enable_MCA
    cmd_disable_MCA = bytes.fromhex('fa f5 02 00 00 00 0f fe') # disable_MCA
    cmd_query_data_and_clear = bytes.fromhex('fa f5 02 02 00 00 0d fe') # 查询数据并清零
    cmd_query_data_and_param = bytes.fromhex('fa f5 03 02 00 00 0c fe') # 查询数据和参数
    cmd_query_data_and_param_and_clear = bytes.fromhex('fa f5 04 02 00 00 0b fe') # 查询数据和参数并清零数据
    
else:
    print("现在是仿真测试")

# class my_threading(threading.Thread):
#     def __init__(self, ID, name, counter):
#         threading.Thread.__init__(self)
#         self.ID = ID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print ("开始线程：" + self.name)
#         process_data(self.ID,self.name, self.counter)
#         print ("退出线程：" + self.name)

# def process_data(id, name, counter):
#     while not thread_flag:
#         id += 1
#         if id >= 4:
#             data = counter.get()
#             print ("%s processing %s" % (name, data))
#         time.sleep(1)

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
                label.setText("<span style='font-size: 12pt'>当前时间=%6.1fs， <span style='color: green'>x=%6.1f,  <span style='color: red'>y=%6.1f, <span style='color: yellow'>当前道计数=%6.1f个</span>" % (time.time()%100, mousePoint.x(), mousePoint.y(), data1[index]))
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

        # self.update()

        self.timer = QtCore.QTimer()
        # self.timer2 = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        # self.timer.timeout.connect(self.update_graph)
        # self.timer.timeout.connect(self.update_data)
        self.timer.start(500)

    # 更新数据
    def update(self):
        # 当前时间
        # print(time.time())
        global p1, ptr, ser, cmd_query_data, cmd_query_data_and_clear, cmd_query_data_and_param_and_clear, cmd_query_data_and_param
        # 更新随机数据
        data1 = 1500 * pg.gaussianFilter(np.random.random(size=1000), 10) + 300 * np.random.random(size=1000)
        if image_flag.sim_flag == 0:
            # self.multi_thread()
            ser.write(cmd_query_data_and_param_and_clear)
            recv = ser.read(10240).hex()
            # print(recv)
            parsed = collect_data.parse_signal_and_params(recv)
            # print(parsed)
            data1 = np.array(parsed['DATA'], dtype=np.int64)
        # 绘制图像并开始采集
        if image_flag.start_flag == 1:
            self.curve_1.setData(data1)
            self.curve_2.setData(data1)
        # 清零图像并停止采集
        if image_flag.clear_flag == 1:
            data1 = np.zeros(1000)
            self.curve_1.setData(data1)
            self.curve_2.setData(data1)
            image_flag.clear_flag = 0
            image_flag.start_flag = 0

'''
description: 多线程的失败尝试
param {type} 
return {type} 
'''
    # def multi_thread(self):
    #     thread_list = ["draw_pictures", "collect_data"]
    #     number = ["One", "Two"]
    #     work_queue = queue.Queue(10)
    #     threads = []
    #     thread_ID = 1
    #     for num in number:
    #         work_queue.put(num)
    #     for thread_name in thread_list:
    #         thread = my_threading(thread_ID, thread_name, work_queue)
    #         thread.start()
    #         threads.append(thread)
    #         thread_ID += 1
    #     while not work_queue.empty():
    #         pass
    #     thread_flag = 0
    #     for t in threads:
    #         t.join()
    #     print("退出线程")

    # def update_graph(self):
    #     self.curve_1.setData(data1)
    #     self.curve_2.setData(data1)

    # def update_data(self):
    #     global p1, ptr, ser, cmd_query_data, cmd_query_data_and_clear, cmd_query_data_and_param_and_clear, cmd_query_data_and_param
    #     ser.write(cmd_query_data_and_param_and_clear)
    #     recv = ser.read(10240).hex()
    #     # print(recv)
    #     parsed = collect_data.parse_signal_and_params(recv)
    #     # print(parsed)
    #     data1 = np.array(parsed['DATA'], dtype=np.int64)

'''
description: 单个画布
param {type} 
return {type} 
'''
# 添加matplotlib画布
# class MplWidget(QtWidgets.QWidget):
#     def __init__(self, parent = None):
#         QtWidgets.QWidget.__init__(self, parent)
        # self.canvas = MplCanvas()
        # self.vbl = QtWidgets.QVBoxLayout()
        # self.vbl.addWidget(self.canvas)
        # self.setLayout(self.vbl)

'''
description: 用于测试绘图
param {type} 
return {type} 
'''
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