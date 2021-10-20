from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys


y=([0.2,0.8])
print(y[1])

x = np.array ([])
x.resize(2, 2, 2)
for i in range(2):

	x[0][0][i]=y[i]



print(x)


