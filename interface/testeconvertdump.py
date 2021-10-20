from PyQt5 import QtWidgets , uic, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
import numpy as np
from funcPPinch import pontopinch
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pylab as P
from canvas import plotargrafico1,plotargrafico2,plotargrafico3
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import xlrd
from estruturas import estruturas
from functrocador import trocador
import re
import sys
import random
from Abaixoteste10 import abaixo
from Acimateste10 import acima
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from matplotlib.figure import Figure


app=QtWidgets.QApplication([])
dlg=uic.loadUi("untitlednova.ui")

dlg.lineEdit.setPlaceholderText("K")
dlg.lineEdit2.setPlaceholderText("K")
dlg.lineEdit3.setPlaceholderText("kW/K")
dlg.lineEdit3_2.setPlaceholderText("kW/(m²K)")

n=0
pinch=0
correntes=[]
dT=[2,2,2]
Tmin=0
Tmax=0
dTmin = 10
Tdecre=[]
cascat2certo=[]
donee=0
caixinha=dlg.caixinha
tabwid=dlg.tableWidget
flagplot=0
dH=0
cascat=[]
utilidadesquente=0
caixinha3=dlg.caixinha3
caixinha4=dlg.caixinha4
estagios=[0]
nstages=0
pinchf=0
pinchq=0
menor=0
cascat2=[]
unidadeusada=["Temperature (K)","Enthalpy (kJ)","Enthalpy (kJ)"]
alreadypinched=0
plotou=0
utilidadesquente=0
ncold=0
nhot=0
correntesncorrigidas=[]
nlinhas=1
nlinhas2=1



def openfile():
	dlg.tableWidget.blockSignals(True)
	global n
	Tk().withdraw()
	filename = askopenfilename()
	workbook = xlrd.open_workbook(filename)
	worksheet = workbook.sheet_by_index(0)
	k=0
	while k != -1:
		try:
			if (worksheet.cell(k+1, 0).value) != '':
				k=k+1
				n=n+1
		except IndexError:
			break
	dlg.tableWidget.setRowCount(n)
	for i in range (n):#[0]=Tent  [1]=Tsai  [2]=CP  [3]=tipo
		x1=0
		for j in range (3):
			x1=(worksheet.cell(i+1, j+1).value)
			dlg.tableWidget.setItem(i, j, QTableWidgetItem(str(x1)))
	for i in range (n):
		HotnCold (float(dlg.tableWidget.item(i,0).text()), float(dlg.tableWidget.item(i,1).text()), i)
		for j in range (2):
			temptable=str(dlg.tableWidget.item(i, j).text())
			if (dlg.comboBox.currentText()) == 'Kelvin':
				temptable=temptable[0:] + ' K'
				if j==1:
					cptable=str(dlg.tableWidget.item(i, 2).text())
					cptable=cptable[0:] + ' kW/K'
					dlg.tableWidget.setItem(i, 2, QTableWidgetItem(cptable))
			else:
				temptable=temptable[0:] + ' ºF'
				if j==1:
					cptable=str(dlg.tableWidget.item(i, 2).text())
					cptable=cptable[0:] + ' Btu/ºF'
					dlg.tableWidget.setItem(i, 2, QTableWidgetItem(cptable))
			dlg.tableWidget.setItem(i, j, QTableWidgetItem(temptable))
	dlg.tableWidget.blockSignals(False)

def colocarunidadestemp(temptable):
	temptable=str(temptable)
	print(temptable)
	if (dlg.comboBox.currentText()) == 'Kelvin':
		temptable=temptable[0:] + ' K'
	else:
		temptable=temptable[0:] + ' ºF'
	return temptable

def colocarunidadescp(temptable):
	temptable=str(temptable)
	print(temptable)
	if (dlg.comboBox.currentText()) == 'Kelvin':
		temptable=temptable[0:] + ' kW/K'
	else:
		temptable=temptable[0:] + ' Btu/ºF'
	return temptable

def HotnCold (tin,ten,i,) :
	global ncold,nhot
	if tin < ten:
		dlg.tableWidget.setItem(i, 3, QTableWidgetItem('Cold'))
		nhot=nhot+1
	if tin > ten:
		dlg.tableWidget.setItem(i, 3, QTableWidgetItem('Hot'))
		ncold=ncold+1
	return(ncold,nhot)

def itemedited(item):
    dlg.tableWidget.blockSignals(True)
    row = item.row()
    col = item.column() ## 	x2=re.findall("\d+", x2)       x2=float(x2[0])
    tin=dlg.tableWidget.item(row, 0).text()
    tin=re.findall("\d+", tin)
    tin=float(tin[0])
    ten=dlg.tableWidget.item(row, 1).text()
    ten=re.findall("\d+", ten)
    ten=float(ten[0])
    HotnCold(tin, ten, row)
    tin=str(tin)
    ten=str(ten)
    if (dlg.comboBox.currentText()) == 'Kelvin':
    	tin=tin[0:] + ' K'
    	ten=ten[0:] + ' K'
    else:
    	tin=tin[0:] + ' ºF'
    	ten=ten[0:] + ' ºF'
    dlg.tableWidget.setItem(row, 0, QTableWidgetItem((tin)))
    dlg.tableWidget.setItem(row, 1, QTableWidgetItem((ten)))
    global alreadypinched
    print (alreadypinched)
    if alreadypinched > 0:
    	dlg.canvas2.destroy()
    	dlg.canvas3.destroy()
    	dlg.pinchbutton.setEnabled(False)
    	dlg.tabWidget.setTabEnabled(1,False)
    	dlg.tabWidget.setTabEnabled(2,False)
    global correntes
    correntes=[]
    return correntes
    dlg.tableWidget.blockSignals(False)



def KpC (temp) :
	temp=temp-273.15
	round(temp, 2)
	temp=float(str(round(temp, 3)))
	return temp

def CpK (temp) :
	temp=temp+273.15
	temp=float(str(round(temp, 3)))
	return temp

def CpF (temp) :
	temp=temp*1.8+32
	temp=float(str(round(temp, 3)))
	return temp

def FpC (temp) :
	temp=(temp-32)/1.8
	temp=float(str(round(temp, 3)))
	return temp

def FpR (temp) :
	temp=temp+459.67
	temp=float(str(round(temp, 3)))
	return temp

def RpF (temp) :
	temp=temp-459.67
	temp=float(str(round(temp, 3)))
	return temp

def kWpbtu (cp) :
	cp= 0.2388459*cp
	cp=float(str(round(cp, 3)))
	return cp

def btupkW (cp) :
	cp= cp/0.2388459
	cp=float(str(round(cp, 3)))
	return cp

def apertaradd () :
	global n
	n=n+1
	dlg.tableWidget.blockSignals(True)
	dlg.tableWidget.setRowCount(n)
	dlg.tableWidget.setItem(n-1, 0, QTableWidgetItem(str(colocarunidadestemp(dlg.lineEdit.text()))))
	dlg.tableWidget.setItem(n-1, 1, QTableWidgetItem(str(colocarunidadestemp(dlg.lineEdit2.text()))))
	dlg.tableWidget.setItem(n-1, 2, QTableWidgetItem(str(colocarunidadescp(dlg.lineEdit3.text()))))
	g1=float(dlg.lineEdit.text())
	g2=float(dlg.lineEdit2.text())
	if g1 < g2:
		dlg.tableWidget.setItem(n-1, 3, QTableWidgetItem('Cold'))
	if g1 > g2:
		dlg.tableWidget.setItem(n-1, 3, QTableWidgetItem('Hot'))
	if (dlg.comboBox.currentText()) == 'Celsius':
		dlg.tableWidget.setItem(n-1, 4, QTableWidgetItem('ºC'))
	if (dlg.comboBox.currentText()) == 'Fahrenheit':
		dlg.tableWidget.setItem(n-1, 4, QTableWidgetItem('ºF'))
	if (dlg.comboBox.currentText()) == 'Kelvin':
		dlg.tableWidget.setItem(n-1, 4, QTableWidgetItem('K'))
	if (dlg.comboBox.currentText()) == 'Rankine':
		dlg.tableWidget.setItem(n-1, 4, QTableWidgetItem('R'))
	dlg.tableWidget.blockSignals(False)

#def abrirdivisao ():
#	global nhot,ncold
#	dlg.menu=uic.loadUi("divisao.ui")                     >>>> Tirar do código: as divisões tão mais embaixo
#	dlg.menu.show()
#	for i in range (nhot):
#		dlg.menu.comboBox.addItem(str(i+1))
#	for i in range (ncold):
#		dlg.menu.comboBox_2.addItem(str(i+1))


def apertardone () :
	global correntes, dTmin, correntesncorrigidas
	global donee
	donee=1
	for i in range (n):#[0]=Tent  [1]=Tsai  [2]=CP  [3]=tipo
		x1=[]
		for j in range (4):			
			x2=dlg.tableWidget.item(i, j).text()
			if j<3:
				x2=re.findall("\d+", x2)
				x2=float(x2[0])
			x1.append(x2)
		correntes.append(x1)
	print(type(correntes[0][2]))
	dlg.pinchbutton.setEnabled(True)
	print(n)
	if (dlg.tempcombo1.currentText()) == 'Imperial units':
		unidadeusada[0]="Temperature (ºF)"
		unidadeusada[1]="Enthalpy (Btu)"
		unidadeusada[2]="Enthalpy (Btu)"
	dTmin=float(dlg.lineEdit_2.text())
	correntesncorrigidas=correntes
	print("GDFSGPSDFPGDFSPGDSFPGPDFSPGSDFPGPSDFPGP",correntesncorrigidas,correntes)
	correntes[1][2]=1.5


def apertarpinchbutton () :
	global donee,alreadypinched,plotou
	print(donee)
	if donee == 1 :
		global correntes, dTmin, Tdecre, Tmin, Tmax, cascat2certo ,dT, estagios,cascat2,utilidadesquente,menor,pinchf,pinchq
		global n
		global dT
		dTmin, Tdecre, Tmin, Tmax, cascat2certo,dT,pinchf,pinchq,cascat2,utilidadesquente,menor = pontopinch(correntes, n, dTmin, Tdecre, Tmin, Tmax, cascat2certo, dT,pinch,dH,cascat,utilidadesquente,menor,cascat2)
		print(dT)
		plotargrafico1(correntes, n, caixinha,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch,unidadeusada,plotou)
		plotargrafico2(correntes, n, caixinha3,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,pinchf,pinchq,unidadeusada)
		plotargrafico3(correntes, n, caixinha4,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,pinchf,pinchq,menor,cascat2,unidadeusada)
		estagios=estruturas(correntes, n, dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,estagios)
		trocador(correntes, n,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,estagios)
		print("mano funciona ",nhot,ncold,correntesncorrigidas)
		for i in range (n): #correção das temperaturas
			if correntesncorrigidas[i][3] == "Hot":
				correntesncorrigidas [i][0]=(correntesncorrigidas[i][0]) + (dTmin)/2
				correntesncorrigidas [i][1]=(correntesncorrigidas[i][1]) + (dTmin)/2
			if correntesncorrigidas[i][3] == "Cold":
				correntesncorrigidas [i][0]=(correntesncorrigidas[i][0]) - (dTmin)/2
				correntesncorrigidas [i][1]=(correntesncorrigidas[i][1]) - (dTmin)/2
		#abaixo(correntes,pinchq,pinchf,n,nhot,ncold)
		#acima(correntes,pinchq,pinchf,n,nhot,ncold)
		dlg.tabWidget.setTabEnabled(1,True)
		dlg.tabWidget.setTabEnabled(2,True)
		dlg.tabWidget.setTabEnabled(3,True)
		alreadypinched=1
		plotou=1
		print(correntes,pinchq,pinchf,n,nhot,ncold)
		for i in range(nhot):
			addsetashot()
		for i in range(ncold):
			addsetascold()
		criarrede()
		setarcorrentes()
		correntesnoscombos(nhot,ncold)
		print(correntes,correntes,correntes)
		return alreadypinched,plotou


def grandcomposite () :
	dlg.canvas2.hide()
	dlg.canvas3.show()

def THD () :
	dlg.canvas3.hide()
	dlg.canvas2.show()

def SI () :
	dlg.comboBox.setCurrentIndex(0)
	dlg.comboBox_3.setCurrentIndex(0)
	dlg.lineEdit.setPlaceholderText("K")
	dlg.lineEdit2.setPlaceholderText("K")
	dlg.lineEdit3.setPlaceholderText("kW/K")
	dlg.lineEdit3_2.setPlaceholderText("kW/(m²K)")
	if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != '') :
		dlg.lineEdit.setText(str(CpK(FpC(float(dlg.lineEdit.text())))))
		dlg.lineEdit2.setText(str(CpK(FpC(float(dlg.lineEdit2.text())))))
	if (dlg.lineEdit3.text() != ''):
		dlg.lineEdit3.setText(str(btupkW(float(dlg.lineEdit3.text()))))

def sistemaingles () :
	dlg.comboBox.setCurrentIndex(2)
	dlg.comboBox_3.setCurrentIndex(1)
	dlg.lineEdit.setPlaceholderText("ºF")
	dlg.lineEdit2.setPlaceholderText("ºF")
	dlg.lineEdit3.setPlaceholderText("Btu/(hºF)")
	dlg.lineEdit3_2.setPlaceholderText("Btu/(ft²hºF)")
	if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
		dlg.lineEdit.setText(str(CpF(KpC(float(dlg.lineEdit.text())))))
		dlg.lineEdit2.setText(str(CpF(KpC(float(dlg.lineEdit2.text())))))
	if (dlg.lineEdit3.text() != ''):
		dlg.lineEdit3.setText(str(kWpbtu(float(dlg.lineEdit3.text()))))

def celsius ():
	if (dlg.tempcombo1.currentText()) == 'SI':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(CpK(float(dlg.lineEdit.text()))))
			dlg.lineEdit2.setText(str(CpK(float(dlg.lineEdit2.text()))))
		dlg.comboBox.setCurrentIndex(0)
	if (dlg.tempcombo1.currentText()) == 'Imperial units':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(CpF(float(dlg.lineEdit.text()))))
			dlg.lineEdit2.setText(str(CpF(float(dlg.lineEdit2.text()))))
		dlg.comboBox.setCurrentIndex(2)

def kelvin ():
	if (dlg.tempcombo1.currentText()) == 'Imperial units':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(CpF(KpC(float(dlg.lineEdit.text())))))
			dlg.lineEdit2.setText(str(CpF(KpC(float(dlg.lineEdit2.text())))))
		dlg.comboBox.setCurrentIndex(2)

def farenheit ():
	if (dlg.tempcombo1.currentText()) == 'SI':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(CpK(FpC(float(dlg.lineEdit.text())))))
			dlg.lineEdit2.setText(str(CpK(FpC(float(dlg.lineEdit2.text())))))
		dlg.comboBox.setCurrentIndex(0)

def rankine () :
	if (dlg.tempcombo1.currentText()) == 'SI':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(CpK(FpC(RpF(float(dlg.lineEdit.text()))))))
			dlg.lineEdit2.setText(str(CpK(FpC(RpF(float(dlg.lineEdit2.text()))))))
		dlg.comboBox.setCurrentIndex(0)
	if (dlg.tempcombo1.currentText()) == 'Imperial units':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(RpF(float(dlg.lineEdit.text()))))
			dlg.lineEdit2.setText(str(RpF(float(dlg.lineEdit2.text()))))
		dlg.comboBox.setCurrentIndex(2)

def btu () :
	if (dlg.tempcombo1.currentText()) == 'Imperial units':
		if (dlg.lineEdit3.text() != ''):
			dlg.lineEdit3.setText(str(kWpbtu(float(dlg.lineEdit3.text()))))
		dlg.comboBox_3.setCurrentIndex(0)

def kW () :
		if (dlg.tempcombo1.currentText()) == 'SI':
			if (dlg.lineEdit3.text() != ''):
				dlg.lineEdit3.setText(str(btupkW(float(dlg.lineEdit3.text()))))
		dlg.comboBox_3.setCurrentIndex(1)

def ligarspins():
	if dlg.comboBox_5.currentIndex() != 0:
		dlg.doubleSpinBox.setEnabled(True)
	else:
		dlg.doubleSpinBox.setEnabled(False)
	if dlg.comboBox_6.currentIndex() != 0:
		dlg.doubleSpinBox_2.setEnabled(True)
	else:
		dlg.doubleSpinBox_2.setEnabled(False)

def addsetashot ():
	dlg.label_12 = QtWidgets.QLabel(dlg)
	dlg.im = QPixmap("flechared.png")
	dlg.label_12.setPixmap(dlg.im)
	dlg.label_12.setAlignment(QtCore.Qt.AlignCenter)
	dlg.label_12.setScaledContents(True)
	dlg.label_12.setMaximumSize(750,150)
	dlg.gridLayout_7.addWidget(dlg.label_12)
	dlg.label_12.show()
	dlg.radio = QtWidgets.QRadioButton(dlg.label_12)
	dlg.gridLayout_7.addWidget(dlg.radio)
	dlg.radio.show()
	p = dlg.geometry().bottomRight() - dlg.radio.geometry().bottomRight() - QPoint(100, 100)
	dlg.radio.move(p)
	print(dlg.label_12.y())

def addsetascold ():
	dlg.label_12 = QtWidgets.QLabel(dlg)
	dlg.im = QPixmap("flechablue.png")
	dlg.label_12.setPixmap(dlg.im)
	dlg.label_12.setAlignment(QtCore.Qt.AlignCenter)
	dlg.label_12.setScaledContents(True)
	dlg.label_12.setMaximumSize(750,150)
	dlg.gridLayout_7.addWidget(dlg.label_12)
	dlg.label_12.show()

def correntesnoscombos(nhot,ncold):
	
	nstages=2
	nsubstages=2

	for i in range (nhot):
		dlg.comboBox_2.addItem(str(i+1))     #acima   add heat ex
		dlg.comboBox_9.addItem(str(i+1))     #acima   quadro de correntes quentes
		dlg.comboBox_35.addItem(str(i+1))   #abaixo   add heat ex
		dlg.comboBox_43.addItem(str(i+1))    #abaixo   quadro de correntes quentes
	for i in range (ncold):
		dlg.comboBox_5.addItem(str(i+1))      #acima add heat ex
		dlg.comboBox_10.addItem(str(i+1))     #acima quadro correntes frias
		dlg.comboBox_36.addItem(str(i+1))     #abaixo add heat ex
		dlg.comboBox_44.addItem(str(i+1))     #abaixo quadro de correntes frias
	for i in range (nstages):
		dlg.comboBox_8.addItem(str(i+1))    #acima
		dlg.comboBox_39.addItem(str(i+1))   #abaixo
	for i in range (nsubstages):
		dlg.comboBox_7.addItem(str(i+1))    #acima
		dlg.comboBox_40.addItem(str(i+1))    #abaixo

def criarrede2():      #funçao nao utilizada
	dlg.rede=pg.GraphicsLayoutWidget()
	hour = [1,2,3,4,5,6,7,8,9,10]
	temperature = [30,32,34,32,33,31,29,32,35,45]
	a1 = pg.ArrowItem(angle=0, tipAngle=90, headLen=40, tailLen=50, tailWidth=15, pen={'color': 'r', 'width': 3}, clickable=True)
	a1.setPos(10,0)
	p=dlg.rede.addPlot(row=0, col=0)
	p.addItem(a1)
	c=pg.plot(hour, temperature)
	dlg.rede.setBackground('w')
	p.hideAxis('left')
	dlg.gridLayout_8.addWidget(dlg.rede)
	p.addItem(c)
	def cormud():
		c.setPen('rgb'[2], width=3)
	c.sigClicked.connect(cormud)

def criarrede():       #funçao que cria as setas
	dlg.rede=pg.PlotWidget()
	hour = [0,50]
	temperature = [20,20]
	c=pg.PlotCurveItem(hour, temperature,clickable=True,pen='r', width=15)
	dlg.rede.addItem(c)
	dlg.rede.setBackground('w')
	dlg.gridLayout_8.addWidget(dlg.rede)
	dlg.rede.hideAxis('left')
	dlg.rede.setMouseEnabled(x=False, y=False)
	#a1 = pg.ArrowItem(angle=180, tipAngle=90, headLen=40, tailLen=50, tailWidth=15, pen={'color': 'r', 'width': 3}, clickable=True)
	a1 = pg.ArrowItem(angle=180, tipAngle=90, headLen=40, tailLen=0, tailWidth=15, clickable=True, brush=(0,0,255))
	a1.setPos(55,20)
	dlg.rede.addItem(a1)
	c.setPen("b", width=15)
	def cormud():
		c.setPen("g", width=15)
	c.sigClicked.connect(cormud)
	#d = {}
	#for x in range(1, nhot):
	    #d["string{0}".format(x)] = pg.PlotCurveItem(hour, temperature[x],clickable=True,pen='r', width=15)
	    #dlg.rede.additem()
	#for x in range(0, 2):
	    #globals()['linha%s' % x] = pg.PlotCurveItem(hour, temperature[x],clickable=True,pen='r', width=15)
	    #print(globals()('linha%s' % x))
	    #dlg.rede.additem('linha%s' % x)
	#------------------
	#d = {}
	#temperature2 = [[30,30],[40,40]]
	#for x in range(0, 1):
	    #d["linha{0}".format(x)] = pg.PlotCurveItem(hour, temperature2[x],clickable=True,pen='r', width=15)
	    #print("llllllllllllllllllll",d["linha0"])
	    #dlg.rede.additem(d["linha0"])


def setarcorrentes():
	global correntes, dTmin, Tdecre, Tmin, Tmax, cascat2certo ,dT, estagios,cascat2,utilidadesquente,menor,nhot,ncold,pinchq,pinchf,n,correntesncorrigidas
	global n
	global dT
	print("meu como é possivel",correntesncorrigidas)
	print(n)
	#dlg.tableWidget_2.setRowCount(n)
	#dlg.tableWidget_2.setColumnCount(1)
	dlg.tableWidget_3.setRowCount(nhot)
	dlg.tableWidget_4.setRowCount(ncold)
	#dlg.tableWidget_3.setColumnCount(1)
	for i in range (n):#[0]=Tent  [1]=Tsai  [2]=CP  [3]=tipo
		#dlg.tableWidget_2.setItem(i, 0, QTableWidgetItem(str(correntes[i][0])))
		if correntes[i][3] == "Hot":
			dlg.tableWidget_3.setItem(i, 2, QTableWidgetItem(str(correntesncorrigidas[i][0])))
			dlg.tableWidget_3.setItem(i, 1, QTableWidgetItem(str(pinchq)))
			dlg.tableWidget_3.setItem(i, 0, QTableWidgetItem(str(pinchq)))
			Qmct=correntes[i][2]*(correntes[i][0]-pinchq)
			dlg.tableWidget_3.setItem(i, 3, QTableWidgetItem(str(Qmct)))

	j=0
	for i in range (n):#[0]=Tent  [1]=Tsai  [2]=CP  [3]=tipo
		if correntes[i][3] == "Cold":
			dlg.tableWidget_4.setItem(j, 0, QTableWidgetItem(str(pinchf)))
			dlg.tableWidget_4.setItem(j, 1, QTableWidgetItem(str(pinchf)))
			dlg.tableWidget_4.setItem(j, 2, QTableWidgetItem(str(correntesncorrigidas[i][1])))
			Qmct=correntes[i][2]*(pinchf-correntes[i][1])
			dlg.tableWidget_4.setItem(j, 3, QTableWidgetItem(str(Qmct)))
			j=j+1
			print(pinchf)
		print(correntes[i][0],"kkkkkkkkkkkk")

def trocadoracima ():
	global nlinhas
	tfinalh=0
	tfinalc=0
	qtotalh0=0
	qtotalc0=0
	calorquente=(float(dlg.tableWidget_3.item(float(dlg.comboBox_2.currentText())-1,3).text()))
	calorfrio=(float(dlg.tableWidget_3.item(float(dlg.comboBox_5.currentText())-1,3).text()))
	tfinalh,tfinalc,qtotalh0,qtotalc0=acima(correntesncorrigidas,pinchq,pinchf,n,nhot,ncold,dlg,dTmin)
	dlg.tableWidget_3.setItem(float(dlg.comboBox_2.currentText())-1, 1, QTableWidgetItem(str(tfinalh))) #só da certo se tiver tudo quente depois tudo frio
	dlg.tableWidget_4.setItem(float(dlg.comboBox_5.currentText())-1, 1, QTableWidgetItem(str(tfinalc)))
	dlg.tableWidget_3.setItem(float(dlg.comboBox_2.currentText())-1, 3, QTableWidgetItem(str(qtotalh0)))
	dlg.tableWidget_4.setItem(float(dlg.comboBox_2.currentText())-1, 3, QTableWidgetItem(str(qtotalc0)))
	dlg.tableWidget_2.setRowCount(nlinhas)
	dlg.tableWidget_2.setItem(nlinhas-1,0,QTableWidgetItem(str(dlg.comboBox_2.currentText())))
	dlg.tableWidget_2.setItem(nlinhas-1,1,QTableWidgetItem(str(dlg.comboBox_5.currentText())))
	if (str(dlg.comboBox_6.currentText())) == "do not split stream":
		dlg.tableWidget_2.setItem(nlinhas-1,2,QTableWidgetItem(str("Not split")))
	else:
		dlg.tableWidget_2.setItem(nlinhas-1,2,QTableWidgetItem(str(dlg.comboBox_6.currentText())))
	if (str(dlg.comboBox_4.currentText())) == "do not split stream":
		dlg.tableWidget_2.setItem(nlinhas-1,3,QTableWidgetItem(str("Not split")))
	else:
		dlg.tableWidget_2.setItem(nlinhas-1,3,QTableWidgetItem(str(dlg.comboBox_4.currentText())))
	calorfrio=calorfrio*-1
	if calorquente > calorfrio:
		dlg.tableWidget_2.setItem(nlinhas-1,6,QTableWidgetItem(str(abs(int(calorfrio)))))
	else:
		dlg.tableWidget_2.setItem(nlinhas-1,6,QTableWidgetItem(str(abs(int(calorquente)))))
	dlg.tableWidget_2.setItem(nlinhas-1,7,QTableWidgetItem(str((float(dlg.tableWidget_3.item(float(dlg.comboBox_2.currentText())-1,1).text())))))
	dlg.tableWidget_2.setItem(nlinhas-1,8,QTableWidgetItem(str((float(dlg.tableWidget_4.item(float(dlg.comboBox_5.currentText())-1,1).text())))))
	nlinhas=nlinhas+1
	checaresgotadosacima()

def trocadorabaixo ():
	global nlinhas
	tfinalh=0
	tfinalc=0
	qtotalh0=0
	qtotalc0=0
	calorquente=(float(dlg.tableWidget_3.item(float(dlg.comboBox_2.currentText())-1,3).text()))
	calorfrio=(float(dlg.tableWidget_3.item(float(dlg.comboBox_5.currentText())-1,3).text()))
	tfinalh,tfinalc,qtotalh0,qtotalc0=acima(correntesncorrigidas,pinchq,pinchf,n,nhot,ncold,dlg,dTmin)
	dlg.tableWidget_15.setItem(float(dlg.comboBox_2.currentText())-1, 1, QTableWidgetItem(str(tfinalh))) #só da certo se tiver tudo quente depois tudo frio
	dlg.tableWidget_17.setItem(float(dlg.comboBox_5.currentText())-1, 1, QTableWidgetItem(str(tfinalc)))
	dlg.tableWidget_15.setItem(float(dlg.comboBox_2.currentText())-1, 3, QTableWidgetItem(str(qtotalh0)))
	dlg.tableWidget_17.setItem(float(dlg.comboBox_2.currentText())-1, 3, QTableWidgetItem(str(qtotalc0)))
	dlg.tableWidget_14.setRowCount(nlinhas)
	dlg.tableWidget_14.setItem(nlinhas-1,0,QTableWidgetItem(str(dlg.comboBox_2.currentText())))
	dlg.tableWidget_14.setItem(nlinhas-1,1,QTableWidgetItem(str(dlg.comboBox_5.currentText())))
	if (str(dlg.comboBox_6.currentText())) == "do not split stream":
		dlg.tableWidget_2.setItem(nlinhas-1,2,QTableWidgetItem(str("Not split")))
	else:
		dlg.tableWidget_2.setItem(nlinhas-1,2,QTableWidgetItem(str(dlg.comboBox_6.currentText())))
	if (str(dlg.comboBox_4.currentText())) == "do not split stream":
		dlg.tableWidget_2.setItem(nlinhas-1,3,QTableWidgetItem(str("Not split")))
	else:
		dlg.tableWidget_2.setItem(nlinhas-1,3,QTableWidgetItem(str(dlg.comboBox_4.currentText())))
	calorfrio=calorfrio*-1
	if calorquente > calorfrio:
		dlg.tableWidget_2.setItem(nlinhas-1,6,QTableWidgetItem(str(abs(int(calorfrio)))))
	else:
		dlg.tableWidget_2.setItem(nlinhas-1,6,QTableWidgetItem(str(abs(int(calorquente)))))
	dlg.tableWidget_2.setItem(nlinhas-1,7,QTableWidgetItem(str((float(dlg.tableWidget_3.item(float(dlg.comboBox_2.currentText())-1,1).text())))))
	dlg.tableWidget_2.setItem(nlinhas-1,8,QTableWidgetItem(str((float(dlg.tableWidget_4.item(float(dlg.comboBox_5.currentText())-1,1).text())))))
	nlinhas=nlinhas+1
	checaresgotadosacima()	

def trocadorutilidade ():
	global nlinhas2
	tfinalh=0
	tfinalc=0
	qtotalh0=0
	qtotalc0=0
	calorquente=(float(dlg.tableWidget_3.item(float(dlg.comboBox_2.currentText())-1,3).text()))
	calorfrio=(float(dlg.tableWidget_3.item(float(dlg.comboBox_5.currentText())-1,3).text()))
	tfinalh,tfinalc,qtotalh0,qtotalc0=acima(correntesncorrigidas,pinchq,pinchf,n,nhot,ncold,dlg)
	dlg.tableWidget_3.setItem(float(dlg.comboBox_2.currentText())-1, 1, QTableWidgetItem(str(tfinalh))) #só da certo se tiver tudo quente depois tudo frio
	dlg.tableWidget_4.setItem(float(dlg.comboBox_5.currentText())-1, 1, QTableWidgetItem(str(tfinalc)))
	dlg.tableWidget_3.setItem(float(dlg.comboBox_2.currentText())-1, 3, QTableWidgetItem(str(qtotalh0)))
	dlg.tableWidget_4.setItem(float(dlg.comboBox_2.currentText())-1, 3, QTableWidgetItem(str(qtotalc0)))
	dlg.tableWidget_2.setRowCount(nlinhas)
	dlg.tableWidget_2.setItem(nlinhas-1,0,QTableWidgetItem(str(dlg.comboBox_2.currentText())))
	dlg.tableWidget_2.setItem(nlinhas-1,1,QTableWidgetItem(str(dlg.comboBox_5.currentText())))
	if (str(dlg.comboBox_6.currentText())) == "do not split stream":
		dlg.tableWidget_2.setItem(nlinhas-1,2,QTableWidgetItem(str("Not split")))
	else:
		dlg.tableWidget_2.setItem(nlinhas-1,2,QTableWidgetItem(str(dlg.comboBox_6.currentText())))
	if (str(dlg.comboBox_4.currentText())) == "do not split stream":
		dlg.tableWidget_2.setItem(nlinhas-1,3,QTableWidgetItem(str("Not split")))
	else:
		dlg.tableWidget_2.setItem(nlinhas-1,3,QTableWidgetItem(str(dlg.comboBox_4.currentText())))
	calorfrio=calorfrio*-1
	if calorquente > calorfrio:
		dlg.tableWidget_2.setItem(nlinhas-1,6,QTableWidgetItem(str(abs(int(calorfrio)))))
	else:
		dlg.tableWidget_2.setItem(nlinhas-1,6,QTableWidgetItem(str(abs(int(calorquente)))))
	dlg.tableWidget_2.setItem(nlinhas-1,7,QTableWidgetItem(str((float(dlg.tableWidget_3.item(float(dlg.comboBox_2.currentText())-1,1).text())))))
	dlg.tableWidget_2.setItem(nlinhas-1,8,QTableWidgetItem(str((float(dlg.tableWidget_4.item(float(dlg.comboBox_5.currentText())-1,1).text())))))
	nlinhas2=nlinhas2+1
	checaresgotadosacima()

def checaresgotadosacima():
	contadordutyhot=0
	contadordutycold=0
	for i in range (nhot):
		if dlg.tableWidget_3.item(i,3).text() == "0.0":
			contadordutyhot=contadordutyhot+1
	if contadordutyhot == nhot:
		dlg.comboBox_10.setEnabled(True)
		dlg.pushButton_8.setEnabled(True)
	for i in range (ncold):
		if dlg.tableWidget_4.item(i,3).text() == "0.0":
			contadordutycold=contadordutycold+1
	if contadordutyhot == nhot:
		dlg.comboBox_10.setEnabled(True)
		dlg.pushButton_8.setEnabled(True)
	if contadordutyhot == nhot and contadordutycold == ncold:        #mexer aqui, pra liberar os combobox de utilidade no acima
		dlg.comboBox_9.setEnabled(False)
		dlg.comboBox_10.setEnabled(False)
		dlg.pushButton_7.setEnabled(False)
		dlg.pushButton_8.setEnabled(False)

def addutilitycoldacima():
	global nlinhas
	print(int(dlg.comboBox_10.currentText()))
	calorfrioquetava=(float(dlg.tableWidget_3.item(float(dlg.comboBox_2.currentText())-1,3).text()))
	if dlg.tableWidget_4.item((int(dlg.comboBox_10.currentText()))-1,3).text() == "0.0":
		msg = QMessageBox()
		msg.setText("Stream already exhausted")
		#msg.setInformativeText('More information')
		msg.setWindowTitle("Error")
		msg.exec_()
	else:
		dlg.tableWidget_2.setRowCount(nlinhas)
		dlg.tableWidget_2.setItem(nlinhas-1,0,QTableWidgetItem(str("Hot Utility")))
		dlg.tableWidget_2.setItem(nlinhas-1,1,QTableWidgetItem(str(dlg.comboBox_5.currentText())))
		dlg.tableWidget_4.setItem((int(dlg.comboBox_10.currentText()))-1,3,QTableWidgetItem("0.0"))
		dlg.tableWidget_4.setItem((int(dlg.comboBox_10.currentText()))-1,1,QTableWidgetItem(str(dlg.tableWidget_4.item((int(dlg.comboBox_10.currentText()))-1,2).text())))
		if (str(dlg.comboBox_6.currentText())) == "do not split stream":
			dlg.tableWidget_2.setItem(nlinhas-1,2,QTableWidgetItem(str("Not split")))
		else:
			dlg.tableWidget_2.setItem(nlinhas-1,2,QTableWidgetItem(str(dlg.comboBox_6.currentText())))
		if (str(dlg.comboBox_4.currentText())) == "do not split stream":
			dlg.tableWidget_2.setItem(nlinhas-1,3,QTableWidgetItem(str("Not split")))
		else:
			dlg.tableWidget_2.setItem(nlinhas-1,3,QTableWidgetItem(str(dlg.comboBox_4.currentText())))
		dlg.tableWidget_2.setItem(nlinhas-1,6,QTableWidgetItem(str(abs(int(calorfrioquetava)))))
		dlg.tableWidget_2.setItem(nlinhas-1,7,QTableWidgetItem(str("---")))
		dlg.tableWidget_2.setItem(nlinhas-1,8,QTableWidgetItem(str((float(dlg.tableWidget_4.item(float(dlg.comboBox_5.currentText())-1,1).text())))))
		checaresgotadosacima()
		nlinhas=nlinhas+1
	
def ativarHe_acima ():
	dlg.lineEdit_5.setEnabled(True)
	dlg.lineEdit_6.setEnabled(False)
	dlg.lineEdit_7.setEnabled(False)

def ativarTHot_acima():
	dlg.lineEdit_5.setEnabled(False)
	dlg.lineEdit_6.setEnabled(True)
	dlg.lineEdit_7.setEnabled(False)

def ativarTCold_acima():
	dlg.lineEdit_5.setEnabled(False)
	dlg.lineEdit_6.setEnabled(False)
	dlg.lineEdit_7.setEnabled(True)

def ativarQmax_acima():
	dlg.lineEdit_5.setEnabled(False)
	dlg.lineEdit_6.setEnabled(False)
	dlg.lineEdit_7.setEnabled(False)

def ativarHe_abaixo ():
	dlg.lineEdit_25.setEnabled(True)
	dlg.lineEdit_26.setEnabled(False)
	dlg.lineEdit_27.setEnabled(False)

def ativarTHot_abaixo():
	dlg.lineEdit_25.setEnabled(False)
	dlg.lineEdit_26.setEnabled(True)
	dlg.lineEdit_27.setEnabled(False)

def ativarTCold_abaixo():
	dlg.lineEdit_25.setEnabled(False)
	dlg.lineEdit_26.setEnabled(False)
	dlg.lineEdit_27.setEnabled(True)

def ativarQmax_abaixo():
	dlg.lineEdit_25.setEnabled(False)
	dlg.lineEdit_26.setEnabled(False)
	dlg.lineEdit_27.setEnabled(False)


def coldsplit1():
	global nhot,ncold, nstages
	dlg.divisaotrocador=uic.loadUi("divisaocold1.ui")
	dlg.divisaotrocador.show()

	if nhot>=ncold:
		nstages=nhot
	else:
		nstages=ncold

	for i in range (ncold):
		dlg.divisaotrocador.comboBox.addItem(str(i+1))
	for i in range (nhot):                                   #split - o numero máximo de divisões é igual ao numero de correntes quentes
		dlg.divisaotrocador.comboBox_2.addItem(str(i+1))
	for i in range (nstages):
		dlg.divisaotrocador.comboBox_3.addItem(str(i+1))     # numero de estágios. É o máximo de número de correntes?

	def coldsplit2(nsplit):
		dlg.divisaotrocador2=uic.loadUi("divisaocold2.ui")
		dlg.divisaotrocador2.show()

		coldsplitspinbox=[0]*nsplit #variáveis
		coldsplitlabel=[0]*nsplit

		for i in range(nsplit): # criar variável 
			coldsplitspinbox[i]=QtWidgets.QDoubleSpinBox(dlg)
			coldsplitlabel[i]=QtWidgets.QLabel(dlg)
			dlg.divisaotrocador2.verticalLayout_2.addWidget(coldsplitspinbox[i])
			coldsplitlabel[i].setText("Substream {}".format(i+1))
			myFont=QtGui.QFont()
			myFont.setBold(True)
			coldsplitlabel[i].setFont(myFont)
			dlg.divisaotrocador2.verticalLayout.addWidget(coldsplitlabel[i])

		def dadosusercoldsplit():
			estagio = int(float(dlg.divisaotrocador.comboBox_3.currentText())) #estagios
			ccold = int(float(dlg.divisaotrocador.comboBox.currentText())) # numero de correntes
			qsj = int(float(dlg.divisaotrocador.comboBox_2.currentText())) # numero subcorrentes
			fracao_fria=[0]*nsplit
			for i in range(nsplit):
				fracao_fria[i] = float(coldsplitspinbox[i].value())

			print(estagio, "\n")
			print(ccold, "\n")    
			print(qsj, "\n")
			print(coldsplitspinbox)
			print(fracao_fria)

		dlg.divisaotrocador2.buttonBox.clicked.connect(lambda: dadosusercoldsplit())

	dlg.divisaotrocador.pushButton.clicked.connect(lambda: coldsplit2(int(dlg.divisaotrocador.comboBox_2.currentText())))

def hotsplit1():
	global nhot,ncold, stages
	dlg.divisaotrocador3=uic.loadUi("divisaohot1.ui")
	dlg.divisaotrocador3.show()

	if nhot>=ncold:
		nstages=nhot
	else:
		nstages=ncold

	for i in range (ncold):
		dlg.divisaotrocador3.comboBox.addItem(str(i+1))
	for i in range (nhot):                                   #split - o numero máximo de divisões é igual ao numero de correntes quentes
		dlg.divisaotrocador3.comboBox_2.addItem(str(i+1))
	for i in range (nstages):
		dlg.divisaotrocador3.comboBox_3.addItem(str(i+1))     # numero de estágios. Qual o número maximo? ncold?

	def hotsplit2(nsplit):
		dlg.divisaotrocador4=uic.loadUi("divisaohot2.ui")
		dlg.divisaotrocador4.show()

		hotsplitspinbox=[0]*nsplit #variável qualquer só pra fazer a função funcionar
		hotsplitlabel=[0]*nsplit

		for i in range(nsplit): 
			hotsplitspinbox[i]=QtWidgets.QDoubleSpinBox(dlg)
			hotsplitlabel[i]=QtWidgets.QLabel(dlg)
			dlg.divisaotrocador4.verticalLayout_2.addWidget(hotsplitspinbox[i])
			hotsplitlabel[i].setText("Substream {}".format(i+1))
			myFont=QtGui.QFont()
			myFont.setBold(True)
			hotsplitlabel[i].setFont(myFont)
			dlg.divisaotrocador4.verticalLayout.addWidget(hotsplitlabel[i])
			
		def dadosuserhotsplit():
			estagio = int(float(dlg.divisaotrocador3.comboBox_3.currentText())) #estagios
			chot = int(float(dlg.divisaotrocador3.comboBox.currentText())) # numero de correntes
			qsi = int(float(dlg.divisaotrocador3.comboBox_2.currentText())) # numero subcorrentes
			fracao_quente=[0]*nsplit
			for i in range(nsplit):
				fracao_quente[i] = float(hotsplitspinbox[i].value())

			print(estagio, "\n")
			print(chot, "\n")    
			print(qsi, "\n")
			print(hotsplitspinbox)
			print(fracao_quente)

		dlg.divisaotrocador4.pushButton.clicked.connect(lambda: dadosuserhotsplit())

	dlg.divisaotrocador3.pushButton.clicked.connect(lambda: hotsplit2(int(dlg.divisaotrocador3.comboBox_2.currentText())))



dlg.pinchbutton.setEnabled(False)
dlg.tabWidget.setTabEnabled(1,False)
dlg.tabWidget.setTabEnabled(2,False)
dlg.tabWidget.setTabEnabled(3,False)
dlg.comboBox_9.setEnabled(False)
dlg.comboBox_10.setEnabled(False)
dlg.pushButton_7.setEnabled(False)
dlg.pushButton_8.setEnabled(False)
#dlg.pushButton_9.clicked.connect(abrirdivisaotrocador) esse é o split stream antigo (embaixo de add heat exchanger)
dlg.pushButton.clicked.connect(apertaradd)
dlg.donebutton.clicked.connect(apertardone)
dlg.pinchbutton.clicked.connect(apertarpinchbutton)
dlg.actionOpen_2.triggered.connect(openfile)
dlg.tableWidget.itemChanged.connect(itemedited)
dlg.tempcombo1.currentIndexChanged.connect(lambda i: i == 0 and SI())
dlg.tempcombo1.currentIndexChanged.connect(lambda i: i == 1 and sistemaingles())
dlg.comboBox.currentIndexChanged.connect(lambda i: i == 1 and celsius())
dlg.comboBox.currentIndexChanged.connect(lambda i: i == 0 and kelvin())
dlg.comboBox.currentIndexChanged.connect(lambda i: i == 2 and farenheit())
dlg.comboBox.currentIndexChanged.connect(lambda i: i == 3 and rankine())
dlg.comboBox_3.currentIndexChanged.connect(lambda i: i == 0 and btu())
dlg.comboBox_3.currentIndexChanged.connect(lambda i: i == 1 and kW())
dlg.pushButton_3.clicked.connect(abrirdivisao)
dlg.pushButton_6.clicked.connect(trocadoracima)
dlg.radioButton.toggled.connect(ativarHe_acima)
dlg.radioButton_2.toggled.connect(ativarTHot_acima)
dlg.radioButton_3.toggled.connect(ativarTCold_acima)
dlg.radioButton_4.toggled.connect(ativarQmax_acima)
dlg.radioButton_4.setChecked(True)
dlg.radioButton_17.toggled.connect(ativarHe_abaixo)
dlg.radioButton_18.toggled.connect(ativarTHot_abaixo)
dlg.radioButton_19.toggled.connect(ativarTCold_abaixo)
dlg.radioButton_20.toggled.connect(ativarQmax_abaixo)
dlg.radioButton_20.setChecked(True)
dlg.pushButton_8.clicked.connect(addutilitycoldacima)
dlg.pushButton_9.clicked.connect(hotsplit1)
dlg.pushButton_13.clicked.connect(coldsplit1)
dlg.pushButton_12.clicked.connect(coldsplit1)
dlg.pushButton_11.clicked.connect(hotsplit1)


header = dlg.tableWidget.horizontalHeader()
header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)






dlg.show()
dlg.showMaximized()
app.exec()