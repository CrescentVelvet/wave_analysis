'''
Author       : velvet
Date         : 2020-08-07 22:37:28
LastEditTime : 2020-12-29 11:51:31
LastEditors  : velvet
Description  : 
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
# import datetime
import collect_data
import threading
import queue

class image_flag:
    sim_flag    = 0 # 仿真测试开关
    thread_flag = 0 # 多线程开关
    start_flag  = 0 # 采集数据开关
    clear_flag  = 0 # 清零数据开关
    info_string = ['zero']  # 返回的信息
    draw_once = 0 # 只绘制一次画面
    data1 = np.zeros(1000)  # 保存静态数据
    parsed = dict() # 完整的回包数据
    bps = 115200 # 全局波特率

class image_control:
    # 开始采集数据
    def start_to_collect():
        image_flag.start_flag = 1
        print('开始采集数据')
    
    # 停止采集数据
    def stop_to_collect():
        image_flag.start_flag = 0
        print('停止采集数据')
    
    # 清零全部数据
    def clear_data():
        image_flag.clear_flag = 1
        print('数据已全部清零')

    # 更新状态信息
    def update_info():
        info_str = image_flag.info_string[0]
        print('更新了状态信息')
        return info_str

    # 只绘制一次画面
    def draw_once_data():
        image_flag.draw_once = 1
        print('打开文件绘制图像')

# 为了在ui_window里调用，使用了全局变量
# 主体界面显示
win = pg.GraphicsLayoutWidget(show=False)
win.setWindowTitle('wave display')
# 显示鼠标坐标
label_data = pg.LabelItem(justify='right')
label_data.setPos(0, 0)
win.addItem(label_data)
# # 显示当前时间————失败：与label_data无法在同一个layout上
# label_time = pg.LabelItem(justify='right')
# label_time.setPos(0, 0)
# win.addItem(label_time)
# 添加两个画图界面：上图p1，下图p2
p1 = win.addPlot(row=1, col=0)
p2 = win.addPlot(row=2, col=0)
# 添加下图选区
region = pg.LinearRegionItem()
# 显示鼠标十字线
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
vb = p1.vb
ptr = 0

if image_flag.sim_flag == 0:
    print("现在是实际测试")
    image_flag.bps = 57600
    # image_flag.bps = 115200
    time_out = 1
    port_list = list(serial.tools.list_ports.comports())
    # 输入端口序号
    for i in range(len(port_list)):
        print('序号：', i, '---', '端口COM：', serial.Serial(list(port_list[i])[0], image_flag.bps, timeout=time_out).name)
    # COM_NUM = input('请输入序号来选择端口COM:')
    # ser = serial.Serial(list(port_list[COM_NUM])[0], image_flag.bps, timeout=time_out)
    ser = serial.Serial(list(port_list[0])[0], image_flag.bps, timeout=time_out) # 直接选取默认端口
    # cmd_query_data = bytes.fromhex('fa f5 01 02 00 00 0e fe') # 查询数据
    cmd_query_data = bytes.fromhex('01 32 00 00 33') # 查询数据修改
    cmd_query_param = bytes.fromhex('fa f5 01 01 00 00 0f fe') # 查询参数
    cmd_enable_MCA = bytes.fromhex('fa f5 01 00 00 00 10 fe') # enable_MCA
    cmd_disable_MCA = bytes.fromhex('fa f5 02 00 00 00 0f fe') # disable_MCA
    # cmd_query_data_and_clear = bytes.fromhex('fa f5 02 02 00 00 0d fe') # 查询数据并清零
    cmd_query_data_and_clear = bytes.fromhex('01 33 00 00 34') # 查询数据并清零修改
    # 命令需要再次核对
    cmd_query_data_and_param = bytes.fromhex('fa f5 03 02 00 00 0c fe') # 查询数据和参数
    cmd_query_data_and_param_and_clear = bytes.fromhex('01 33 00 00 34') # 查询数据和参数并清零数据
    
else:
    print("现在是仿真测试")
    print(image_flag.bps)

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
    def update_region_above():
        region.setZValue(10)
        # 获取上图选区范围
        minX, maxX = region.getRegion()
        p1.setXRange(minX, maxX, padding=0)

    # 移动上图改变下图选区
    def update_region_below(window, viewRange):
        rgn = viewRange[0]
        region.setRegion(rgn)

    # 显示鼠标十字线
    def mouseMoved(evt):
        pos = evt[0]
        if p1.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            # 获取鼠标坐标
            mouse_x = int(mousePoint.x())
            # 获取上图选区范围
            minX, maxX = region.getRegion()
            # 边界检测
            if maxX > 1000 or minX < 0:
                maxX = 1000
                minX = 0
            # 将鼠标坐标映射到上图并取整
            if mouse_x > 1000:
                mouse_x = 1000
                print("已超出边界")
            elif mouse_x < 0:
                mouse_x = 0
                print("已超出边界")
            # index = int( (mouse_x-0) / (len(image_flag.data1)-0) * (maxX - minX) + minX )
            # data_sum = sum(image_flag.data1)
            index = int(mouse_x)
            if index > minX and index < maxX:
                label_data.setText("<span style='font-size: 12pt', span style='color: green'>x=%6.1d,\t  <span style='color: purple'>y=%6.1d,\t <span style='color: yellow'>当前道计数=%6.1d个,\t <span style='color: white'>全部道计数=%6.1d个</span>" % (int(mousePoint.x()), int(mousePoint.y()), int(image_flag.data1[index]), int(sum(image_flag.data1))))
            # print(image_flag.data1)
            # print(mouse_x, "---", index, "---", image_flag.data1[index])
            # # 当前日期时间————失败：与label_data无法在同一个layout上
            # time_data = datetime.datetime.now()
            # time_str = datetime.datetime.strftime(time_data,'%Y-%m-%d %H:%M:%S')
            # label_time.setText(time_str)
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
        # 减少数据量，相邻数据取平均
        data2 = np.zeros(len(image_flag.data1)//10)
        avg_flag = 0
        for i in range(len(image_flag.data1)):
            data2[i//10] += image_flag.data1[i]
            if (i+1) % 10 != 0:
                avg_flag += 1
            elif (i+1) % 10 == 0 or i == len(image_flag.data1)-1:
                data2[i//10] /= avg_flag
                avg_flag = 0
        # 绘制直方图(上图)
        # np.histogram处理累计数据
        # hist, bin_edges = np.histogram(data1, bins=len(data1))
        # self.curve_1 = p1.plot(bin_edges, hist, stepMode=True, fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        # np.linspace创建等差数列
        # self.curve_1 = p1.plot(data2, pen="b")
        # self.curve_1 = p1.plot(np.linspace(10, len(data2), len(data2)+1), data2, stepMode=True, fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        self.curve_1 = p1.plot(np.linspace(10, len(data2), len(data2)), data2, stepMode=False, fillLevel=0, fillOutline=True, brush=(0,0,255,150))
        # 绘制折线图(下图)
        self.curve_2 = p2.plot(image_flag.data1, pen="y")

        # 设置选区初始范围
        region.setRegion([250, 350])
        minX, maxX = region.getRegion()
        p1.setXRange(minX, maxX, padding=0)
        # 移动下图选区改变上图
        region.sigRegionChanged.connect(DrawPicture.update_region_above)
        # 移动上图改变下图选区
        p1.sigRangeChanged.connect(DrawPicture.update_region_below)
        # 添加鼠标十字线
        p1.addItem(vLine, ignoreBounds=True)
        p1.addItem(hLine, ignoreBounds=True)
        # 十字线跟随鼠标移动
        proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=DrawPicture.mouseMoved)
        p1.proxy = proxy
        layout.addWidget(win)

        self.timer = QtCore.QTimer()
        # self.timer2 = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        # self.timer.timeout.connect(self.update_graph)
        # self.timer.timeout.connect(self.update_data)
        self.timer.start(50)

    # 更新数据
    def update_data(self):
        image_flag.info_string[0] = '————————'
        global p1, ptr, ser, cmd_query_data, cmd_query_data_and_clear, cmd_query_data_and_param_and_clear, cmd_query_data_and_param
        # 更新随机数据
        # data1 = np.zeros(1000)
        # 实际测试
        if image_flag.start_flag == 1:
            if image_flag.sim_flag == 0:
                # self.multi_thread()
                ser.write(cmd_query_data)
                recv = ser.read(10240).hex()
                # print("recv:", recv)
                parsed = collect_data.parse_signal_and_params(recv)
                image_flag.parsed = parsed
                for item in parsed.keys():
                    if item is not 'DATA':
                        image_flag.info_string.append(parsed[item])
                # print(parsed)
                image_flag.data1 = np.array(parsed['DATA'], dtype=np.int64)
            # 仿真测试
            elif image_flag.sim_flag == 1:
                # data1 = 1000 * pg.gaussianFilter(np.random.random(size=1000), 10) + 300 * np.random.random(size=1000)
                recv = '0142000c000000000000000000000000000000000000010000000000000000000000000000000000000000200000' \
                'fd01003f1400ea1100b619018aef05933206b6ca0413df03784e03b4fd029baf022178025b4502341e02baf00191d00100' \
                'b501cc8901838801756801c355017d43016b3201a92601881801820c015a030199f900d2ef0008ec00c9dd00d9d8007bd1' \
                '00bfc4006ac5002cc10005bb008fb6000bb1006cac0018a600d8a400ce9c00d499001896009b94009c8e008e8d00d38800' \
                '9f7c007285001c8100dc7f00be7e00697d00717b00327900897800da7700247600457200a37200996d003a6a00cb68007b' \
                '61000666002062001f62004d5f00fa5b002a5b009d58001757006c5400375200f05100fa5000bb4e00734d00174b003246' \
                '003f48006d4700d64600514700b94500a64400904200414300064200354200d64100324200084000124100703f004e3d00' \
                '3b3f00af3e00393f00e43e003f3e001b3e00183d00493e00b43b00523b00203b00613b006737006b38009636004430002a' \
                '3400283300d53200063100102f00402e00dc2c00f92a005b2900f92700202600632500d423003c22001a2000441b00ec1d' \
                '00321d00701b00f11a007c1900df17009a1700461600251500a81400811400a41300941200d211000311002f0f001e1000' \
                'a00f00150f00ef0e005e0e00bf0d00900d002a0d002b0d00680c00240c00ed0b00820b00440b00160b00fb09008b0a0010' \
                '0a002e0a008b0a00e70900a80900ad09000b0a005709001509001e09006d0900d10800280900e50800e107005608004808' \
                '009108008008004708003a0800d40700080800fb0700ed0700fa0700d70700b307008107007c0700660700f80700780700' \
                '750700f607006607009607007d07008a07007507003907003007009707006207006e07002b07000507001107001e0700c2' \
                '0600e20600fa06007d0600990600a80600760600a706008306008b06002006005c0600a70500990500b00500df05007205' \
                '006705005b0500100500f504000405007e0400ae04003b04006204001904000f0400290400860300a70300800300700300' \
                '6803002f0300060300000300f60200ee02009b02008b0200980200770200450200660200210200550200090200f201000c' \
                '0200b50100c40100be01009f0100ae0100920100b301008c01005d01006401005901004601005c01004f01004701002e01' \
                '002e01003301002501001801002301001701001d0100fb0000200100ff0000000100ff0000080100e70000e60000e60000' \
                'eb0000ec0000e60000e80000d40000e40000c50000de0000af0000ce0000ad0000960000b70000ab0000bf00009a0000c2' \
                '0000d90000b50000b00000ca0000c00000b10000ab0000be0000ab0000ba0000ad00009c00008900009900009f00009f00' \
                '007f00008e0000950000980000a600008e00009300008b0000a10000a300008300009300009100008100007f0000860000' \
                '8300008800009200008900007900008600007800008600008a00007100007f00006600007900007b00007a000076000069' \
                '00006800007d00006a00007400007a00006e00006800007300005700004f00007400005900006f00007600005100006000' \
                '006800006100006000006200006200005000005d00005a00006700005b0000560000600000710000720000520000640000' \
                '6800005e00005d00005f00006700004600005900004800004800004900005400004300005000005300004d00004e000041' \
                '00004e00004e00005300003c00005100004b00004c00004a00003a00004500004900004b00004600005400006300004500' \
                '005400005a00004000004a00004b00004300005800003d00003f00004c00004400003700004a00004400003b0000340000' \
                '3700004600004100004000003a00003700003300004a00003200003000004300003800004100003f00003d000039000035' \
                '00003600004f00004700003d00003400003f00002b00003600003000004300002f00003b00002c00003400003900003300' \
                '003500003900003400003b00002c00003400002700002c00002800002e0000370000420000460000300000310000410000' \
                '3500002b00002b00003400003600003200002a00002000003000003500003000003600002a00002e00003200002700002a' \
                '00003100003300002a00003100003200003800002e00003400003000003b00002f00002e00002d00001f00003500002100' \
                '002300002e00001d00002900002c00002d00002900002b0000200000290000220000280000320000320000330000240000' \
                '3600003000002700002b00003800002800002100002600002700002d00002d00002200002b000029000030000023000027' \
                '00002b00002200002900002500002300002900002c00003200002300002100003400002800002700002c00002100002800' \
                '002400002000002900002200002700002400002100002700002100002c00002700002300003700002800001e0000260000' \
                '2e00001900002400002a00001f00001c00001a00002300002100002100002900002800002600002100002100001d000019' \
                '00001f00001c00001f00002400001d00001200002200001d00001c00002400001c00001900002100001400002600002400' \
                '002500001c00001e00002000001800001600001d00002400001900001f00001800001f00001f00002600001f00001e0000' \
                '1600001e00001900001900002600001600002600002300001c00002200001d00002500002300001f00001d00001700001b' \
                '00001d00002400001900001800001f00002000002100001c00002400001700001c00001e00001a00001900001b00001c00' \
                '001900001900002100001d00001c00002100001b00001e00001800001300001600001a0000180000170000280000140000' \
                '1800001e00001b00001400001b00001e00001500001c00001000001f00001a00001500001a00001600001d00001700001a' \
                '00001a00001300001000001e00001900001f00001e00001a00001800001900001e00001b00001400001800001300002100' \
                '001d00001800001200001400001f00001300001f00001000001600001700001600001b0000160000100000180000110000' \
                '2100001400001500001c00001500001a00001f00001700001800001500001500001200001600001a00000e00001b000017' \
                '00001500001300001d00001800002200000e00001000001600001800001b00001800001f00001900001f00001900001900' \
                '001800001600001300001a00001c00001700001900001f00001600001b00001b00001a00001600001900001500001c0000' \
                '2100001b00001700001500002000001400001c000019000018000023000019000013000019000015000016000025000014' \
                '00001a00001b00001600001900001900001b00002100002000002200001e00002800002200002200002400002200002300' \
                '002400001b00001e00002900002700001d00002800002300002700002400002300002a0000200000270000220000240000' \
                '1c00002100002000002500002600002800002b00002400003000002200002700002800003400002c00002700002500001e' \
                '00001b00002f00002d00002d00002e00002a00002600002500003800002a00003100002b00003800002a00003000002f00' \
                '002900003300002500002a00003400003500003300003500003500002a00002d00003f00002800003f0000410000290000' \
                '2f00002e00002d00003000003600003900003300003800004100004100003800003e00004000003d00002d000030000033' \
                '00003f00003800003400003800003500003e00003a00003000003c00004b00004600003a00003b00003c00004500003c00' \
                '004900004300003e00004400004a00004100004100004100004100003e00003f00003c0000440000410000310000370000' \
                '5000003f00004500005200004e00004800004000004500004900003f00004d00003c00004e00003e000042000054000057' \
                '00004b00004200005100004200004700004b00004400003c00004400004300004e00005a00004900004200004700003b00' \
                '004300005300004300004a00004700004f00004100004d00005200004b00004000005300004700004f00004700003f0000' \
                '4100005300004f00004d00005100005c00005a00005100004900005b00003c00006000005300004a00005d00003b000039' \
                '00005d00003e00005900004000004700004600004d00005300004b00004a00003d00005200000e8d0066ac'
                parsed = collect_data.parse_signal_and_params(recv)
                image_flag.parsed = parsed
                for item in parsed.keys():
                    if item is not 'DATA':
                        image_flag.info_string.append(parsed[item])
                # print(parsed)
                image_flag.data1 = np.array(parsed['DATA'], dtype=np.int64)
                if image_flag.start_flag == 1:
                    image_flag.data1 = 300 * np.random.random(size=1000)
        # 绘制图像并开始采集
        if image_flag.start_flag == 1 or image_flag.draw_once == 1:
            self.curve_1.setData(image_flag.data1)
            self.curve_2.setData(image_flag.data1)
            image_flag.draw_once = 0
        # 清零图像并停止采集
        if image_flag.clear_flag == 1:
            # 清零电路板数据
            if image_flag.sim_flag == 0:
                ser.write(cmd_query_data_and_param_and_clear)
            # 清零软件存储数据
            image_flag.data1 = np.zeros(1000)
            self.curve_1.setData(image_flag.data1)
            self.curve_2.setData(image_flag.data1)
            image_flag.clear_flag = 0
            image_flag.start_flag = 0


        # 更新label数据（当前道数与总道数）

        # minX, maxX = region.getRegion()
        # mouse_x = int(mousePoint.x())
        # # 将鼠标坐标映射到上图并取整
        # index = int( (mouse_x-0) / (len(data1)-0) * (maxX - minX) + minX )
        # if index > minX and index < maxX:
        #     label_data.setText("<span style='font-size: 12pt', span style='color: green'>x=%6.1f,\t  <span style='color: purple'>y=%6.1f,\t <span style='color: yellow'>当前道计数=%6.1d个</span>" % (mousePoint.x(), mousePoint.y(), int(data1[index])))
        #     print(data1)
        # print(minX)

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
