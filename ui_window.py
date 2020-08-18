'''
Author       : velvet
Date         : 2020-06-30 18:36:09
LastEditTime : 2020-08-14 20:51:25
LastEditors  : velvet
Description  : 
FilePath     : \wave_analysis\ui_window.py
'''
#coding=utf-8
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont
from image_draw import MplWidget
from image_draw import DrawPicture
import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Point import Point
from matplotlib.figure import Figure

class Ui_MainWindow(object):
    def __init__(self):
        self.stdo = 1
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("主窗口")
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(15)
        QToolTip.setFont(QFont('SansSerif', 14)) # 显示提示语setFont
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(1010, 30, 70, 45))
        self.startButton.setFont(font)
        self.startButton.setObjectName("开始")
        self.startButton.setToolTip('按下这个按钮，就可以<b>开始采集</b>了！')
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(1100, 30, 70, 45))
        self.stopButton.setFont(font)
        self.stopButton.setObjectName("停止")
        self.stopButton.setToolTip('按下这个按钮，就可以<b>停止采集</b>了！')
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(1190, 30, 70, 45))
        self.clearButton.setFont(font)
        self.clearButton.setObjectName("清零")
        self.clearButton.setToolTip('按下这个按钮，就可以<b>数据清零</b>了！')
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(1010, 480, 241, 181))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        # 设置图像显示界面
        self.mpl = MplWidget(self.centralwidget)
        self.mpl.setEnabled(True)
        self.mpl.setGeometry(QtCore.QRect(21, 21, 971, 531))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mpl.sizePolicy().hasHeightForWidth())
        self.mpl.setSizePolicy(sizePolicy)
        self.mpl.setMinimumSize(QtCore.QSize(0, 400))
        self.mpl.setObjectName("图像显示界面")
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(500, 580, 81, 31))
        self.textBrowser_3.setObjectName("textBrowser_3")
        self.textBrowser_4 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_4.setGeometry(QtCore.QRect(780, 580, 81, 31))
        self.textBrowser_4.setObjectName("textBrowser_4")
        self.textBrowser_6 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_6.setGeometry(QtCore.QRect(500, 630, 81, 31))
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.textBrowser_5 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_5.setGeometry(QtCore.QRect(780, 630, 81, 31))
        self.textBrowser_5.setObjectName("textBrowser_5")
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(230, 630, 81, 31))
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.textBrowser_7 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_7.setGeometry(QtCore.QRect(230, 580, 81, 31))
        self.textBrowser_7.setMinimumSize(QtCore.QSize(0, 0))
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(1010, 130, 241, 331))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.tableWidget.setFont(font)
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setGridStyle(QtCore.Qt.DashLine)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setObjectName("tableWidget")
        self.button_Browse = QtWidgets.QPushButton(self.centralwidget)
        self.button_Browse.setGeometry(QtCore.QRect(1170, 90, 80, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.button_Browse.setFont(font)
        self.button_Browse.setObjectName("选择目录")
        self.button_Browse.setToolTip('按下这个按钮，进行<b>文件目录选择</b>。你可以在此选择波形信号文件绘制其图像。')
        self.line_Directory = QtWidgets.QLineEdit(self.centralwidget)
        self.line_Directory.setGeometry(QtCore.QRect(1010, 90, 150, 30))
        self.line_Directory.setObjectName("显示目录")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(120, 590, 84, 16))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 640, 105, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(410, 590, 61, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(410, 640, 75, 16))
        self.label_4.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(680, 590, 90, 16))
        self.label_5.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(680, 640, 90, 16))
        self.label_6.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 26))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu")
        self.menu_display = QtWidgets.QMenu(self.menubar)
        self.menu_display.setObjectName("menu_display")
        self.menu_analy = QtWidgets.QMenu(self.menubar)
        self.menu_analy.setObjectName("menu_analy")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        self.menu_about = QtWidgets.QMenu(self.menubar)
        self.menu_about.setObjectName("menu_about")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open = QtWidgets.QAction(MainWindow)
        self.action_open.setObjectName("action_open")
        self.action_save = QtWidgets.QAction(MainWindow)
        self.action_save.setObjectName("action_save")
        self.action_saveas = QtWidgets.QAction(MainWindow)
        self.action_saveas.setObjectName("action_saveas")
        self.action_multi = QtWidgets.QAction(MainWindow)
        self.action_multi.setObjectName("action_multi")
        self.action_QT = QtWidgets.QAction(MainWindow)
        self.action_QT.setObjectName("action_QT")
        self.action_PYQT = QtWidgets.QAction(MainWindow)
        self.action_PYQT.setObjectName("action_PYQT")
        self.action_ZJU = QtWidgets.QAction(MainWindow)
        self.action_ZJU.setObjectName("action_ZJU")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.action_exit.setStatusTip('Exit it')
        self.action_start = QtWidgets.QAction(MainWindow)
        self.action_start.setObjectName("action_start")
        self.action_start.setStatusTip('Start it')
        self.action_pause = QtWidgets.QAction(MainWindow)
        self.action_pause.setObjectName("action_pause")
        self.action_pause.setStatusTip('Pause it')
        self.action_stop = QtWidgets.QAction(MainWindow)
        self.action_stop.setObjectName("action_stop")
        self.action_stop.setStatusTip('Stop it')
        self.action1 = QtWidgets.QAction(MainWindow)
        self.action1.setObjectName("action1")
        self.action2 = QtWidgets.QAction(MainWindow)
        self.action2.setObjectName("action2")
        self.action1_2 = QtWidgets.QAction(MainWindow)
        self.action1_2.setObjectName("action1_2")
        self.action2_2 = QtWidgets.QAction(MainWindow)
        self.action2_2.setObjectName("action2_2")
        self.action3 = QtWidgets.QAction(MainWindow)
        self.action3.setObjectName("action3")
        self.action4 = QtWidgets.QAction(MainWindow)
        self.action4.setObjectName("action4")
        self.action6 = QtWidgets.QAction(MainWindow)
        self.action6.setObjectName("action6")
        self.action7 = QtWidgets.QAction(MainWindow)
        self.action7.setObjectName("action7")
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_saveas)
        self.menu_file.addAction(self.action_exit)
        self.menu_file.addAction(self.action4)
        self.menu_display.addAction(self.action_start)
        self.menu_display.addAction(self.action_pause)
        self.menu_display.addAction(self.action_stop)
        self.menu_analy.addAction(self.action1)
        self.menu_analy.addAction(self.action2)
        self.menu_help.addAction(self.action1_2)
        self.menu_help.addAction(self.action2_2)
        self.menu_help.addAction(self.action3)
        self.menu_about.addAction(self.action_multi)
        self.menu_about.addAction(self.action_QT)
        self.menu_about.addAction(self.action_PYQT)
        self.menu_about.addAction(self.action_ZJU)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_display.menuAction())
        self.menubar.addAction(self.menu_analy.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())
        self.menubar.addAction(self.menu_about.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ZJUsoft"))
        self.startButton.setText(_translate("MainWindow", "开始"))
        self.stopButton.setText(_translate("MainWindow", "停止"))
        self.clearButton.setText(_translate("MainWindow", "清零"))
        self.label_1.setText(_translate("MainWindow", "   当前道数"))
        self.label_2.setText(_translate("MainWindow", "当前道粒子计数"))
        self.label_3.setText(_translate("MainWindow", "  总道数"))
        self.label_4.setText(_translate("MainWindow", "总粒子计数"))
        self.label_5.setText(_translate("MainWindow", "查看道数起始"))
        self.label_6.setText(_translate("MainWindow", "查看道数终点"))
        self.button_Browse.setText(_translate("MainWindow", "选择目录"))
        self.menu_file.setTitle(_translate("MainWindow", "文件"))
        self.menu_display.setTitle(_translate("MainWindow", "显示"))
        self.menu_analy.setTitle(_translate("MainWindow", "分析"))
        self.menu_help.setTitle(_translate("MainWindow", "帮助"))
        self.menu_about.setTitle(_translate("MainWindow", "关于"))
        self.action_open.setText(_translate("MainWindow", "打开"))
        self.action_save.setText(_translate("MainWindow", "保存"))
        self.action_saveas.setText(_translate("MainWindow", "另存为"))
        self.action_multi.setText(_translate("MainWindow", "关于本软件"))
        self.action_QT.setText(_translate("MainWindow", "关于QT"))
        self.action_PYQT.setText(_translate("MainWindow", "关于PYQT"))
        self.action_ZJU.setText(_translate("MainWindow", "关于ZJU"))
        self.action_exit.setText(_translate("MainWindow", "退出"))
        self.action_start.setText(_translate("MainWindow", "开始显示"))
        self.action_pause.setText(_translate("MainWindow", "暂停显示"))
        self.action_stop.setText(_translate("MainWindow", "停止显示"))
        self.action1.setText(_translate("MainWindow", "1"))
        self.action2.setText(_translate("MainWindow", "2"))
        self.action1_2.setText(_translate("MainWindow", "1"))
        self.action2_2.setText(_translate("MainWindow", "2"))
        self.action3.setText(_translate("MainWindow", "3"))
        self.action4.setText(_translate("MainWindow", "4"))
        self.action6.setText(_translate("MainWindow", "6"))
        self.action7.setText(_translate("MainWindow", "7"))

# 用于测试界面
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mplMainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mplMainWindow)
    mplMainWindow.show()
    sys.exit(app.exec_())