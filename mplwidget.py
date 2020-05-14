# Python Qt4 bindings for GUI objects 
from PyQt5 import QtGui
from PyQt5 import QtWidgets

# import the Qt4Agg FigureCanvas object, that binds Figure to 
# Qt4Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt5agg \
import FigureCanvasQTAgg as FigureCanvas

# Matplotlib Figure object 
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):
    """Class to represent the FigureCanvas widget"""
    def __init__(self):
        # setup Matplotlib Figure and Axis
        self.fig = Figure(facecolor = 'white')
        self.fig.set_label('time (s)')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Original Wave')
        self.ax.set_ylabel(r'$Amplitude(V)$')
        self.ax.set_xticklabels( ('0', '1.0', '2.0', '3.0', '4.0',  '5.0'))
        self.ax.xlable = ('time(s)')
        # initialization of the canvas
        FigureCanvas.__init__(self, self.fig)
        # we define the widget as expandable
        FigureCanvas.setSizePolicy(self,
        QtWidgets.QSizePolicy.Expanding,
        QtWidgets.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)
        
class MplWidget(QtWidgets.QWidget):
    """Widget defined in Qt Designer"""
    def __init__(self, parent = None):
        # initialization of Qt MainWindow widget
        QtWidgets.QWidget.__init__(self, parent)
        # set the canvas to the Matplotlib widget
        self.canvas = MplCanvas()
        # create a vertical box layout
        self.vbl = QtWidgets.QVBoxLayout()
        # add mpl widget to vertical box
        self.vbl.addWidget(self.canvas)
        # set the layout to th vertical box
        self.setLayout(self.vbl)
