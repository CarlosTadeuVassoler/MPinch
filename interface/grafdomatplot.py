import matplotlib
matplotlib.use('Qt4Agg')

import sys
from PyQt4 import QtCore, QtGui, uic
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


qtCreatorFile = "main.ui" # my Qt Designer file 

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.csvbutton.clicked.connect(self.plot)

    def plot(self):

        filePath="data.csv"
        df= pd.read_csv(str(filePath),index_col='date')
        ax = self.canvas.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(df, '*-')
        self.canvas.draw()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())