from PyQt5 import QtWidgets , uic
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
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
from Abaixo import abaixo
from acima import acima

from matplotlib.figure import Figure


app=QtWidgets.QApplication([])
dlg=uic.loadUi("untitled.ui")

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
    	dlg.canvas2.hide()
    	dlg.canvas3.hide()
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

def apertardone () :
	global correntes, dTmin
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
	correntes[1][2]=1.5


def apertarpinchbutton () :
	global donee,alreadypinched,plotou
	print(donee)
	if donee == 1 :
		global correntes, dTmin, Tdecre, Tmin, Tmax, cascat2certo ,dT, estagios,cascat2,utilidadesquente,menor
		global n
		global dT
		dTmin, Tdecre, Tmin, Tmax, cascat2certo,dT,pinchf,pinchq,cascat2,utilidadesquente,menor = pontopinch(correntes, n, dTmin, Tdecre, Tmin, Tmax, cascat2certo, dT,pinch,dH,cascat,utilidadesquente,menor,cascat2)
		print(dT)
		plotargrafico1(correntes, n, caixinha,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch,unidadeusada,plotou)
		plotargrafico2(correntes, n, caixinha3,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,pinchf,pinchq,unidadeusada)
		plotargrafico3(correntes, n, caixinha4,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,pinchf,pinchq,menor,cascat2,unidadeusada)
		estagios=estruturas(correntes, n, dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,estagios)
		trocador(correntes, n,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,estagios)
		print("kkkkkkkk",nhot,ncold)
		#abaixo(correntes,pinchq,pinchf,n,nhot,ncold)
		#acima(correntes,pinchq,pinchf,n,nhot,ncold)
		dlg.tabWidget.setTabEnabled(1,True)
		dlg.tabWidget.setTabEnabled(2,True)
		alreadypinched=1
		plotou=1
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

dlg.pinchbutton.setEnabled(False)
dlg.tabWidget.setTabEnabled(1,False)
dlg.tabWidget.setTabEnabled(2,False)
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


header = dlg.tableWidget.horizontalHeader()
header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)





dlg.show()
dlg.showMaximized()
app.exec()