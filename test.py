# -*- coding: utf-8 -*-
"""
In this example we draw two different kinds of histogram.
"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

win = pg.GraphicsLayoutWidget(show=True)
win.resize(800,350)
plt1 = win.addPlot()
plt2 = win.addPlot()

data1 = 300 * np.random.random(size=1000)
data2 = np.zeros(len(data1)//10)
for i in range(len(data1)):
	data2[i//10] += data1[i]
	if (i+1) % 10 == 0:
		data2[i//10] /= 10
plt1.plot(data2, pen="r")
plt2.plot(np.linspace(0, len(data2), len(data2)), data2, stepMode=False, fillLevel=0, fillOutline=True, brush=(0,0,255,150))

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
