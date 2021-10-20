from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys


app=QtWidgets.QApplication([])
dlg=uic.loadUi("untitlednova.ui")

estagio = chot = ccold = qsi = qsj = 0

def divisaoquente(estagio,chot,qsi,fracao_quente):
	dlg.divisaotrocador3=uic.loadUi("divisaohot1.ui")
	estagio = int(float(dlg.divisaotrocador3.comboBox_3.currentText()))
	chot = int(float(dlg.divisaotrocador3.comboBox.currentText()))
	qsi = int(float(dlg.divisaotrocador3.comboBox_2.currentText()))       #não precisa de janela de erro
	for i in range(qsi):      												#pq já vai tá o número máximo de correntes
		Fharr[estagio-1][chot-1][i] = float(fracao_quente[i]*100)
		Qtotalh0[chot-1][i] = Qtotalh01[chot-1]*(Fharr[estagio-1][chot-1][i]/100)
		#(Qtotalh0)
	nhotc = qsi + (nhot - 1)
	##(nhotc)
	##("Fharr", Fharr)
	return(Fharr,nhotc)

def divisaofria():
	dlg.divisaotrocador=uic.loadUi("divisaocold1.ui")
	estagio = int(float(dlg.divisaotrocador.comboBox_3.currentText()))
	ccold = int(float(dlg.divisaotrocador.comboBox.currentText()))
	qsj = int(float(dlg.divisaotrocador.comboBox_2.currentText()))
	for j in range(qsj):
		Fcarr[estagio-1][ccold-1][j] = float(fracao_fria[i]*100)
		Qtotalc0[ccold-1][j] = Qtotalc01[ccold-1]*(Fcarr[estagio-1][ccold-1][j]/100)
		#(Qtotalc0)
	ncoldc = qsj + (ncold - 1)
	##(ncoldc)
	##(Fcarr)
	return (Fcarr,ncoldc)
