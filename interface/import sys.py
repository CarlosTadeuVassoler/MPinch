import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pylab as P

import random


app=QtWidgets.QApplication([])
dlg=uic.loadUi("untitled.ui")

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        dlg.pinchbutton.button.clicked.connect(self.plot)

        # set the layout
        layout=dlg.caixinha()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        self.figure.clear()
        n=4
        correntes=[[165.0, 55.0, 3.0, 'quente'], [145.0, 25.0, 1.5, 'quente'], [85.0, 145.0, 4.0, 'fria'], [25.0, 140.0, 2.0, 'fria']]
        dT=[110.0, 120.0, -60.0, -115.0]
        dTmin = 10
        Tdecre=[165.0, 145.0, 145.0, 140.0, 85.0, 55.0, 25.0, 25.0]
        Tmax = Tdecre[0]
        Tmin = Tdecre[-1]
        cascat2certo=[80.0, 80.0, 82.5, 0.0, 75.0, 60.0, 60.0]
        P.subplot(121)
        for i in range(n):
            if correntes[i][3] == 'quente':
                P.arrow(i * 0.5, correntes[i][0], 0.0, -dT[i], fc="r", ec="r", head_width=0.05, head_length=2)
            if correntes[i][3] == 'fria':
                P.arrow(i * 0.5, correntes[i][0], 0.0, -dT[i], fc="b", ec="b", head_width=0.05, head_length=2)
        P.xlim([-0.5, n / 2])
        P.ylim([Tmin-dTmin, Tmax+dTmin])
        P.matplotlib.pyplot.grid(which='major', axis='y')
        self.canvas.draw()



dlg.show()
app.exec()