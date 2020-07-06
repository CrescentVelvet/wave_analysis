#coding=utf-8
from __future__ import with_statement
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from ui_window import Ui_MainWindow
import os
import matplotlib.pyplot as plt
from pylab import *
from PyQt5.QtWidgets import QMessageBox
import sys
import time
import asyncio
import threading
import queue

class DesignerMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # 主窗口继承
        super(DesignerMainWindow, self).__init__(parent) 
        self.setWindowTitle("波形显示界面")              
        self.setupUi(self)
        # 主界面上的按钮触发开始与停止采集函数的进程
        self.startButton.clicked.connect(self.startButton_callback)
        self.stopButton.clicked.connect(self.stopButton_callback)
        # 主界面菜单栏上的帮助与更多选项跳转到信息介绍窗口
        self.action_QT.triggered.connect(self.QT_callback)
        self.action_PYQT.triggered.connect(self.PYQT_callback)
        self.action_ZJU.triggered.connect(self.ZJU_callback)
        self.action_exit.triggered.connect(app.quit)
        # 选择目录按钮下面的文件栏
        self.tableWidget.setHorizontalHeaderLabels(['filename'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.line_Directory.setReadOnly(True)
        self.textEdit.setReadOnly(True)
        # 点击选择目录按钮打开文件
        self.button_Browse.clicked.connect(self.browse_callback)

    def startButton_callback(self):
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(True)
        self.button_Browse.setEnabled(True)

    def stopButton_callback(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(False)
        self.button_Browse.setEnabled(False)

    def QT_callback(self):
        # 设置帮助菜单中的关于QT的信息介绍
        QMessageBox.aboutQt(self, 'About QT')

    def PYQT_callback(self):
        # 设置帮助菜单中的关于PYQT的信息介绍
        QMessageBox.about(self, 'About PYQT5', '<p><p style="text-align:justify; ' 
            + ' font-family:&quot;font-size:16px;background-color:#FFFFFF; '
            + ' ">PyQt5 is dual licensed on all platforms under the Riverbank Commercial License and the GPL v3. '
            + ' Your PyQt5 license must be compatible with your Qt license. '
            + ' If you use the GPL version then your own code must also use a compatible license.'
            + ' </p><p style="text-align:justify;font-family:&quot;font-size:16px;background-color:#FFFFFF;">PyQt5, '
            + ' unlike Qt, is not available under the LGPL.</p><p style="text-align:justify;font-family:&quot;font-size:16px; '
            + ' background-color:#FFFFFF;">You can purchase a commercial PyQt5 license&nbsp; '
            + ' <a class="reference external" href="https://www.riverbankcomputing.com/commercial/buy">here</a>.</p></p>')

    def ZJU_callback(self):
        # 设置帮助菜单中的关于浙江大学的信息介绍
        QMessageBox.about(self, 'About ZJU', '<p>866 Yuhangtang Rd, Hangzhou 310058, P.R. China&nbsp;</p><p>Copyright &copy; '
            + ' 2018 <a href="http://www.zju.edu.cn/" target="_blank">Zhejiang University</a>&nbsp;</p><p>Seeking Truth, Pursuing Innovation.</p>')
    
    def browse_callback(self):
        # 选择文件夹后将文件夹中所有的" .txt" 文件列出来
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Find Folder", QtCore.QDir.currentPath())
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.line_Directory.setText(directory)
        dirIterator = QtCore.QDirIterator(directory,  ['*.txt'])

        while(dirIterator.hasNext()):
            dirIterator.next()
            dataname = dirIterator.filePath()
            name = QtWidgets.QTableWidgetItem(dataname)
            analysis = QtWidgets.QTableWidgetItem('Not Yet')
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, name)

class my_threading(threading.Thread):
    def __init__(self, ID, name, counter):
        threading.Thread.__init__(self)
        self.ID = ID
        self.name = name
        self.counter = counter
    def run(self):
        print ("开始线程：" + self.name)
        process_data(self.ID,self.name, self.counter)
        print ("退出线程：" + self.name)

def process_data(id, name, counter):
    while not thread_flag:
        id += 1
        if id >= 4:
            data = counter.get()
            print ("%s processing %s" % (name, data))
        time.sleep(1)

# 主程序
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    t = QtCore.QElapsedTimer()
    t.start()
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap("logo.jpg"))
    while t.elapsed() < 1000:
        splash.show()
    splash.finish(splash)
    MultiChannel_window = DesignerMainWindow()
    MultiChannel_window.show()

    # thread_flag = 0
    # thread_list = ["draw_pictures", "collect_data", "analy_data"]
    # number = ["One", "Two", "Three", "Four", "Five"]
    # work_queue = queue.Queue(10)
    # threads = []
    # thread_ID = 1
    # for num in number:
    #     work_queue.put(num)
    # for thread_name in thread_list:
    #     thread = my_threading(thread_ID, thread_name, work_queue)
    #     thread.start()
    #     threads.append(thread)
    #     thread_ID += 1
    # while not work_queue.empty():
    #     pass
    # thread_flag = 1
    # for t in threads:
    #     t.join()
    # print("退出主线程")

    sys.exit(app.exec_())