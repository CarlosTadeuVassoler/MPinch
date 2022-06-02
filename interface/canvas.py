import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets , uic, QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pylab as P

import random

def Gc2(n,dlg,Tdecre,menor,cascat2,unidadeusada, plot=True):
	plt.close("all")
	plt.style.use('default')
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	cascat3 = []
	cascat3.append(menor)
	for i in range(2*n-1):
	    cascat3.append(cascat2[i])
	for i in range(2*n-1):
	    ax.plot([cascat3[i], cascat3[i+1]], [Tdecre[i], Tdecre[i+1]], color = 'k')
	ax.set_xlabel("Enthalpy ({})".format(unidadeusada[2]))
	ax.set_ylabel("Temperature ({})".format(unidadeusada[0]))
	ax.grid(axis="x", color="gray", linewidth=1, linestyle="--")
	ax.grid(axis="y", color="gray", linewidth=1, linestyle="--")
	plt.title('Grand Composite Curve')
	fig.savefig("Gc2.png", bbox_inches="tight", pad_inches=0.5)
	if plot:
		dlg.graficodt2.setPixmap(QtGui.QPixmap("Gc2.png"))
	else:
		return fig

def Gc1(n,dlg,Tdecre,menor,cascat2,unidadeusada, plot=True):
	plt.close("all")
	plt.style.use('default')
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	cascat3 = []
	cascat3.append(menor)
	for i in range(2*n-1):
	    cascat3.append(cascat2[i])
	for i in range(2*n-1):
	    ax.plot([cascat3[i], cascat3[i+1]], [Tdecre[i], Tdecre[i+1]], color = 'k')

	ax.grid(axis="x", color="gray", linewidth=1, linestyle="--")
	ax.grid(axis="y", color="gray", linewidth=1, linestyle="--")
	ax.set_xlabel("Enthalpy ({})".format(unidadeusada[2]))
	ax.set_ylabel("Temperature ({})".format(unidadeusada[0]))
	plt.title('Grand Composite Curve')
	fig.savefig("Gc1.png", bbox_inches="tight", pad_inches=0.5)
	if plot:
		dlg.graficodt1.setPixmap(QtGui.QPixmap("Gc1.png"))
	else:
		return fig
