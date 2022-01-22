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
import re
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from prog_carlos import *
from prog_carlos_abaixo import *
from converter_unidades import *
from matplotlib.figure import Figure
from PIL import Image
import turtle



app=QtWidgets.QApplication([])
dlg=uic.loadUi("MPinch.ui")
dlg.lineEdit.setPlaceholderText("K")
dlg.lineEdit2.setPlaceholderText("K")
dlg.lineEdit3.setPlaceholderText("kW/K")
dlg.lineEdit3_2.setPlaceholderText("kW/(m²K)")

matriz = []
matriz_armazenada = []
matriz_trocadores_abaixo = []
utilidades = []
utilidades_abaixo = []
dTmin = 10
donee=0
cascat=[]
nstages=2
unidadeusada=["Temperature (K)","Enthalpy (kJ)","Enthalpy (kJ)"]
alreadypinched=0
plotou=0
correntesncorrigidas=[]
correntestrocador=[]
corrente_quente_presente_acima = []
corrente_fria_presente_acima = []
corrente_quente_presente_abaixo = []
corrente_fria_presente_abaixo = []
correntes_quentes = []
correntes_frias = []




def openfile():
	global n
	n = 0

	dlg.tableWidget.blockSignals(True)
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
	correntes = []
	dlg.tableWidget.setRowCount(n)
	for i in range (n):#[0]=Tent  [1]=Tsai  [2]=CP  [3]=tipo
		dados_da_corrente = []
		for j in range (3):
			dados_da_corrente.append(worksheet.cell(i+1, j+1).value)
			#x1=(worksheet.cell(i+1, j+1).value)
			#dlg.tableWidget.setItem(i, j, QTableWidgetItem(str(x1)))
		correntes.append(dados_da_corrente)
		print(correntes)
	for i in range (n):
		HotnCold(float(dlg.tableWidget.item(i,0).text()), float(dlg.tableWidget.item(i,1).text()), i)
		#for j in range (2):
		#	temptable=str(dlg.tableWidget.item(i, j).text())
		#	if (dlg.comboBox.currentText()) == 'Kelvin':
		#		temptable=temptable[0:] + ' K'
		#		if j==1:
		#			cptable=str(dlg.tableWidget.item(i, 2).text())
		#			cptable=cptable[0:] + ' kW/K'
		#			dlg.tableWidget.setItem(i, 2, QTableWidgetItem(cptable))
		#	else:
		#		temptable=temptable[0:] + ' ºF'
		#		if j==1:
		#			cptable=str(dlg.tableWidget.item(i, 2).text())
		#			cptable=cptable[0:] + ' Btu/ºF'
		#			dlg.tableWidget.setItem(i, 2, QTableWidgetItem(cptable))
		#	dlg.tableWidget.setItem(i, j, QTableWidgetItem(temptable))
	dlg.tableWidget.blockSignals(False)

def colocarunidadestemp(temptable):
	temptable=str(temptable)
	if (dlg.comboBox.currentText()) == 'Kelvin':
		temptable=temptable[0:] + ' K'
	else:
		temptable=temptable[0:] + ' ºF'
	return temptable

def colocarunidadescp(temptable):
	temptable=str(temptable)
	if (dlg.comboBox.currentText()) == 'Kelvin':
		temptable=temptable[0:] + ' kW/K'
	else:
		temptable=temptable[0:] + ' Btu/ºF'
	return temptable

def HotnCold (tin,ten,i) :      #ve se é corrente quente ou fria
	global ncold,nhot
	if tin < ten:
		dlg.tableWidget.setItem(i, 3, QTableWidgetItem('Cold'))
		ncold=ncold+1
	if tin > ten:
		dlg.tableWidget.setItem(i, 3, QTableWidgetItem('Hot'))
		nhot=nhot+1

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
    #print (alreadypinched)
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

def apertaradd () :
	global n, ncold, nhot
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
		ncold += 1
	if g1 > g2:
		dlg.tableWidget.setItem(n-1, 3, QTableWidgetItem('Hot'))
		nhot += 1
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
	global correntes, dTmin, correntesncorrigidas
	global donee
	correntes = []
	donee=1
	for i in range (n):#[0]=Tent  [1]=Tsai  [2]=CP  [3]=tipo
		x1=[]
		for j in range (4):
			if j<3:
				x2=float(dlg.tableWidget.item(i, j).text())
			else:
				x2=dlg.tableWidget.item(i, j).text()
			#if j<3:
			#	x2=re.findall("\d+", x2)
			#	x2=float(x2[0])
			x1.append(x2)
		correntes.append(x1)
	#print(type(correntes[0][2]))
	dlg.pinchbutton.setEnabled(True)
	#'print(n)
	if (dlg.tempcombo1.currentText()) == 'Imperial units':
		unidadeusada[0]="Temperature (ºF)"
		unidadeusada[1]="Enthalpy (Btu)"
		unidadeusada[2]="Enthalpy (Btu)"
	dTmin=float(dlg.lineEdit_2.text())
	correntesncorrigidas=correntes
	#print(correntesncorrigidas,correntes)
	#correntes[1][2]=1.5
	correntestrocadorr()

def apertarpinchbutton():
	global donee,alreadypinched,plotou, Th0, Thf, CPh, Tc0, Tcf, CPc
	Th0, Thf, CPh, Tc0, Tcf, CPc = [], [], [], [], [], []
	if donee == 1 :
		global correntes, dTmin, Tdecre, Tmin, Tmax, cascat2certo ,dT,cascat2,utilidadesquente,menor,pinchf,pinchq
		global n
		global dT
		Tdecre = []
		Tmin=0
		Tmax=0
		cascat2certo=[]
		dT=[2,2,2]
		cascat2=[]
		utilidadesquente=0
		pinchf=0
		pinchq=0
		menor=0
		pinch=0
		dH = 0
		dTmin, Tdecre, Tmin, Tmax, cascat2certo,dT,pinchf,pinchq,cascat2,utilidadesquente,menor = pontopinch(correntes, n, dTmin, Tdecre, Tmin, Tmax, cascat2certo, dT,pinch,dH,cascat,utilidadesquente,menor,cascat2)
		caixinha=dlg.caixinha
		tabwid=dlg.tableWidget
		flagplot=0
		caixinha3=dlg.caixinha3
		caixinha4=dlg.caixinha4
		plotargrafico1(correntes, n, caixinha,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch,unidadeusada,plotou)
		plotargrafico2(correntes, n, caixinha3,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,pinchf,pinchq,unidadeusada)
		plotargrafico3(correntes, n, caixinha4,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,pinchf,pinchq,menor,cascat2,unidadeusada)
		for i in range (n): #correção das temperaturas
			if correntesncorrigidas[i][3] == "Hot":
				correntesncorrigidas [i][0]=(correntesncorrigidas[i][0]) + (dTmin)/2
				correntesncorrigidas [i][1]=(correntesncorrigidas[i][1]) + (dTmin)/2
			if correntesncorrigidas[i][3] == "Cold":
				correntesncorrigidas [i][0]=(correntesncorrigidas[i][0]) - (dTmin)/2
				correntesncorrigidas [i][1]=(correntesncorrigidas[i][1]) - (dTmin)/2

		print(n)
		print(nhot)
		print(ncold)
		for i in range(n):
			if correntesncorrigidas[i][3] == "Hot":
				Th0.append(correntesncorrigidas[i][0])
				Thf.append(correntesncorrigidas[i][1])
				CPh.append(correntesncorrigidas[i][2])
			if correntesncorrigidas[i][3] == "Cold":
				Tc0.append(correntesncorrigidas[i][0])
				Tcf.append(correntesncorrigidas[i][1])
				CPc.append(correntesncorrigidas[i][2])

		dlg.tabWidget.setTabEnabled(1,True)
		dlg.tabWidget.setTabEnabled(2,True)
		dlg.tabWidget.setTabEnabled(3,True)
		dlg.tabWidget.setTabEnabled(4,True)
		alreadypinched=1
		plotou=1
		for i in range(nhot):
			addsetashot()
		for i in range(ncold):
			addsetascold()
		criarrede()
		receber_pinch(Th0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf)
		receber_pinch_abaixo(Thf, Tc0, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf)
		printar()
		printar_abaixo()
		correntesnoscombos(nhot,ncold)
		testar_correntes()
		testar_correntes_abaixo()
		dlg.comboBox_50.setEnabled(True) #fechar combobox de subhot stream
		dlg.comboBox_51.setEnabled(True) #fechar combobox de subcold stream
		dlg.comboBox_53.setEnabled(True) #fechar combobox de subhot stream
		dlg.comboBox_54.setEnabled(True) #fechar combobox de subcold stream

		return alreadypinched,plotou

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
	#print(dlg.label_12.y())

def addsetascold ():
	dlg.label_12 = QtWidgets.QLabel(dlg)
	dlg.im = QPixmap("flechablue.png")
	dlg.label_12.setPixmap(dlg.im)
	dlg.label_12.setAlignment(QtCore.Qt.AlignCenter)
	dlg.label_12.setScaledContents(True)
	dlg.label_12.setMaximumSize(750,150)
	dlg.gridLayout_7.addWidget(dlg.label_12)
	dlg.label_12.show()

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
	a1 = pg.ArrowItem(angle=180, tipAngle=90, headLen=40, tailLen=0, tailWidth=15, brush=(0,0,255))
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

def correntestrocadorr():
	global correntestrocador, correntes
	for i in range (n):
		x=[]
		for j in range (4):
			x.append(correntes[i][j])
		correntestrocador.append(x)




def openfile_teste():
	global n, nhot, ncold, correntes
	n, nhot, ncold = 0, 0, 0

	#le o excel
	dlg.tableWidget.blockSignals(True)
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

	#armazena as correntes e calcula a quantidade de quentes e frias
	correntes = []
	dlg.tableWidget.setRowCount(n)
	for i in range (n):
		dados_da_corrente = []
		for j in range (3):
			dados_da_corrente.append(worksheet.cell(i+1, j+1).value)
		if dados_da_corrente[0] > dados_da_corrente[1]:
			dados_da_corrente.append("Hot")
			nhot += 1
		else:
			dados_da_corrente.append("Cold")
			ncold += 1
		correntes.append(dados_da_corrente)

	#printa as correntes pro usuário na tabela de streams
	for corrente in range(len(correntes)):
		for coluna in range(4):
			dlg.tableWidget.setItem(corrente, coluna, QTableWidgetItem(str(correntes[corrente][coluna])))
	dlg.tableWidget.blockSignals(False)

def done_teste():
	global dTmin, done

	#libera o pinch e armazena as correntes numa variável que vai ser mudada de acordo com o pinch
	done = True
	dlg.pinchbutton.setEnabled(True)
	dTmin=float(dlg.lineEdit_2.text())

def pinch_teste():
	global done, Th0, Thf, CPh, Tc0, Tcf, CPc, Thf_acima, Th0_abaixo, Tc0_acima, Tcf_abaixo
	Th0, Thf, CPh, Tc0, Tcf, CPc, Thf_acima, Th0_abaixo, Tc0_acima, Tcf_abaixo = [], [], [], [], [], [], [], [], [], []
	if done:
		global correntes, dTmin, pinchf, pinchq, n
		pinchf, pinchq = pontopinch(correntes, n, dTmin)
		#arruma as temperaturas baseado no pinch
		for i in range (n): #correção das temperaturas
			if correntes[i][3] == "Hot":
				correntes_quentes.append(1)
				correntes[i][0] += dTmin/2
				correntes[i][1] += dTmin/2
				Th0.append(correntes[i][0])
				Thf.append(correntes[i][1])
				CPh.append(correntes[i][2])
				if correntes[i][1] >= pinchq: #corrente quente nao bate no pinch acima
					Thf_acima.append(correntes[i][1])
					corrente_quente_presente_abaixo.append(False)
				else:
					Thf_acima.append(pinchq)
					corrente_quente_presente_abaixo.append(True)
				if correntes[i][0] <= pinchq: #corrente quente não bate no pinch abaixo
					Th0_abaixo.append(correntes[i][0])
					corrente_quente_presente_acima.append(False)
				else:
					Th0_abaixo.append(pinchq)
					corrente_quente_presente_acima.append(True)

			if correntes[i][3] == "Cold":
				correntes_frias.append(1)
				correntes[i][0] -= dTmin/2
				correntes[i][1] -= dTmin/2
				Tc0.append(correntes[i][0])
				Tcf.append(correntes[i][1])
				CPc.append(correntes[i][2])
				if correntes[i][0] >= pinchf: #corrente fria não bate no pinch acima
					Tc0_acima.append(correntes[i][0])
					corrente_fria_presente_abaixo.append(False)
				else:
					Tc0_acima.append(pinchf)
					corrente_fria_presente_abaixo.append(True)
				if correntes[i][1] <= pinchf: #corrente fria não bate no pinch abaixo
					Tcf_abaixo.append(correntes[i][1])
					corrente_fria_presente_acima.append(False)
				else:
					Tcf_abaixo.append(pinchf)
					corrente_fria_presente_acima.append(True)

		#manda tudo pro backend
		receber_pinch(Th0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, Thf_acima, Tc0_acima)
		receber_pinch_abaixo(Thf, Tc0, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, Th0_abaixo, Tcf_abaixo)
		printar()
		printar_abaixo()
		correntesnoscombos(nhot,ncold)
		testar_correntes(dlg)
		testar_correntes_abaixo(dlg)


		#libera botões e coisas
		dlg.tabWidget.setTabEnabled(1,True)
		dlg.tabWidget.setTabEnabled(2,True)
		dlg.tabWidget.setTabEnabled(3,True)
		dlg.tabWidget.setTabEnabled(4,True)
		dlg.comboBox_50.setEnabled(True)
		dlg.comboBox_51.setEnabled(True)
		dlg.comboBox_53.setEnabled(True)
		dlg.comboBox_54.setEnabled(True)




def desenhar_rede(correntes_quentes, correntes_frias):
	global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo
	turtle.delay(0)
	turtle.setup(width=1.0, height=1.0)
	temp = turtle.Turtle()
	temp.shapesize(0.001, 0.001, 0.001)
	temp.penup()

	y_acima, y_abaixo = 200, 200

	def quentes(onde, correntes_desenho, presente):
		global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo
		distancia_x = 500
		for i in range(len(correntes_desenho)):
			if presente[i]:
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].color("red")
				correntes_desenho[i].pensize(3)
				correntes_desenho[i].penup()
				correntes_desenho_sub_acima = [0] * nhot
				correntes_desenho_sub_abaixo = [0] * nhot
				if onde == "above":
					correntes_desenho[i].setx(-distancia_x)
					correntes_desenho[i].sety(y_acima)
					correntes_desenho[i].pendown()
					temp.sety(y_acima - 8)
					temp.setx(-distancia_x - len(str(Th0[i]))*6 - 4)
					temp.write(str(Th0[i]), align="left", font=("Arial", 10, "normal"))
					if Thf_acima[i] != pinchq:
						temp.setx(-94)
						temp.write(str(Thf_acima[i]), align="left", font=("Arial", 10, "normal"))
					if not dividida_quente[i]:
						temp.setx(-distancia_x - 138)
						temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]))), align="left", font=("Arial", 10, "normal"))
					else:
						correntes_desenho_sub_acima[i] = [0] * (quantidade_quente[i] - 1)
						for j in range(quantidade_quente[i]-1):
							temp.sety(y_acima - 8)
							temp.setx(-distancia_x - 138)
							temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]*fracoes_quentes[i][j]))), align="left", font=("Arial", 10, "normal"))
							correntes_desenho_sub_acima[i][j] = turtle.Turtle()
							correntes_desenho_sub_acima[i][j].color("red")
							correntes_desenho_sub_acima[i][j].pensize(3)
							correntes_desenho_sub_acima[i][j].penup()
							correntes_desenho_sub_acima[i][j].setx(-distancia_x + 20)
							correntes_desenho_sub_acima[i][j].sety(y_acima)
							correntes_desenho_sub_acima[i][j].pendown()
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(30)
							correntes_desenho_sub_acima[i][j].left(90)
							if Thf_acima[i] == pinchq:
								correntes_desenho_sub_acima[i][j].forward(distancia_x - 44)
							else:
								correntes_desenho_sub_acima[i][j].forward(distancia_x - 140)
							correntes_desenho_sub_acima[i][j].left(90)
							correntes_desenho_sub_acima[i][j].forward(30*(j+1))
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(20)
							y_acima -= 30
						temp.sety(y_acima - 8)
						temp.setx(-distancia_x - 138)
						temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]*fracoes_quentes[i][quantidade_quente[i]-1]))), align="left", font=("Arial", 10, "normal"))
					if Thf_acima[i] == pinchq:
						correntes_desenho[i].forward(distancia_x - 4)
					else:
						correntes_desenho[i].forward(distancia_x - 100)
				elif onde == "below":
					correntes_desenho[i].sety(y_abaixo)
					temp.sety(y_abaixo - 8)
					temp.setx(distancia_x + 6)
					temp.write(str(Thf[i]), align="left", font=("Arial", 10, "normal"))
					if Th0_abaixo[i] != pinchq:
						temp.setx(100 - len(str(Th0[i]))*6 - 4)
						temp.write(str(Th0_abaixo[i]), align="left", font=("Arial", 10, "normal"))
					temp.setx(distancia_x + 90)
					if not dividida_quente_abaixo[i]:
						temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]))), align="left", font=("Arial", 10, "normal"))
					else:
						correntes_desenho_sub_abaixo[i] = [0] * (quantidade_quente_abaixo[i] - 1)
						for j in range(quantidade_quente_abaixo[i]-1):
							temp.sety(y_abaixo - 8)
							temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]*fracoes_quentes_abaixo[i][j]))), align="left", font=("Arial", 10, "normal"))
							correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
							correntes_desenho_sub_abaixo[i][j].color("red")
							correntes_desenho_sub_abaixo[i][j].pensize(3)
							correntes_desenho_sub_abaixo[i][j].penup()
							correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
							if Th0_abaixo[i] == pinchq:
								correntes_desenho_sub_abaixo[i][j].setx(24)
								correntes_desenho_sub_abaixo[i][j].pendown()
								correntes_desenho_sub_abaixo[i][j].right(90)
								correntes_desenho_sub_abaixo[i][j].forward(30)
								correntes_desenho_sub_abaixo[i][j].left(90)
								correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 44)
							else:
								correntes_desenho_sub_abaixo[i][j].setx(120)
								correntes_desenho_sub_abaixo[i][j].pendown()
								correntes_desenho_sub_abaixo[i][j].right(90)
								correntes_desenho_sub_abaixo[i][j].forward(30)
								correntes_desenho_sub_abaixo[i][j].left(90)
								correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 140)
							correntes_desenho_sub_abaixo[i][j].left(90)
							correntes_desenho_sub_abaixo[i][j].forward(30*(j+1))
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(20)
							y_abaixo -= 30
						temp.sety(y_abaixo - 8)
						temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]*fracoes_quentes_abaixo[i][quantidade_quente_abaixo[i]-1]))), align="left", font=("Arial", 10, "normal"))
					if Th0_abaixo[i] == pinchq:
						correntes_desenho[i].setx(4)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x - 4)
					else:
						correntes_desenho[i].setx(100)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x - 100)
			if onde == "above":
				if dividida_quente[i] and dividida_quente_abaixo[i]:
					if quantidade_quente[i] < quantidade_quente_abaixo[i]:
						y_acima -= 30 * (quantidade_quente_abaixo[i] - quantidade_quente[i])
				elif dividida_quente_abaixo[i]:
					y_acima -= 30 * (quantidade_quente_abaixo[i] - 1)
			elif onde == "below":
				if dividida_quente[i] and dividida_quente_abaixo[i]:
					if quantidade_quente[i] > quantidade_quente_abaixo[i]:
						y_abaixo -= 30 * (quantidade_quente[i] - quantidade_quente_abaixo[i])
				elif dividida_quente[i]:
					y_abaixo -= 30 * (quantidade_quente[i] - 1)
			y_acima -= 30
			y_abaixo -= 30

	def frias(onde, correntes_desenho, presente):
		global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo
		distancia_x = 500
		for i in range(len(correntes_desenho)):
			if presente[i]:
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].color("blue")
				correntes_desenho[i].pensize(3)
				correntes_desenho[i].penup()
				correntes_desenho_sub_acima = [0] * ncold
				correntes_desenho_sub_abaixo = [0] * ncold
				if onde == "above":
					correntes_desenho[i].sety(y_acima)
					correntes_desenho[i].left(180)
					temp.sety(y_acima - 8)
					temp.setx(-distancia_x - len(str(Tcf[i]))*6 - 4)
					temp.write(str(Tcf[i]), align="left", font=("Arial", 10, "normal"))
					if Tc0_acima[i] != pinchf:
						temp.setx(-94)
						temp.write(str(Tc0_acima[i]), align="left", font=("Arial", 10, "normal"))
					temp.setx(-distancia_x - 138)
					if not dividida_fria[i]:
						temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]))), align="left", font=("Arial", 10, "normal"))
					else:
						correntes_desenho_sub_acima[i] = [0] * (quantidade_fria[i] - 1)
						for j in range(quantidade_fria[i] - 1):
							temp.sety(y_acima - 8)
							temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]*fracoes_frias[i][j]))), align="left", font=("Arial", 10, "normal"))
							correntes_desenho_sub_acima[i][j] = turtle.Turtle()
							correntes_desenho_sub_acima[i][j].color("blue")
							correntes_desenho_sub_acima[i][j].pensize(3)
							correntes_desenho_sub_acima[i][j].penup()
							correntes_desenho_sub_acima[i][j].sety(y_acima)
							if Tc0_acima[i] == pinchf:
								correntes_desenho_sub_acima[i][j].setx(-24)
								correntes_desenho_sub_acima[i][j].pendown()
								correntes_desenho_sub_acima[i][j].right(90)
								correntes_desenho_sub_acima[i][j].forward(30)
								correntes_desenho_sub_acima[i][j].right(90)
								correntes_desenho_sub_acima[i][j].forward(distancia_x - 44)
							else:
								correntes_desenho_sub_acima[i][j].setx(-120)
								correntes_desenho_sub_acima[i][j].pendown()
								correntes_desenho_sub_acima[i][j].right(90)
								correntes_desenho_sub_acima[i][j].forward(30)
								correntes_desenho_sub_acima[i][j].right(90)
								correntes_desenho_sub_acima[i][j].forward(distancia_x - 140)
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(30*(j+1))
							correntes_desenho_sub_acima[i][j].left(90)
							correntes_desenho_sub_acima[i][j].forward(20)
							y_acima -= 30
						temp.sety(y_acima - 8)
						temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]*fracoes_frias[i][quantidade_fria[i]-1]))), align="left", font=("Arial", 10, "normal"))
					if Tc0_acima[i] == pinchf:
						correntes_desenho[i].setx(-4)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x - 4)
					else:
						correntes_desenho[i].setx(-100)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x - 100)
				elif onde == "below":
					correntes_desenho[i].sety(y_abaixo)
					correntes_desenho[i].left(180)
					correntes_desenho[i].setx(distancia_x)
					correntes_desenho[i].pendown()
					temp.sety(y_abaixo - 8)
					temp.setx(distancia_x + 6)
					temp.write(str(Tc0[i]), align="left", font=("Arial", 10, "normal"))
					if Tcf_abaixo[i] != pinchf:
						temp.setx(100 - len(str(Tcf_abaixo[i]))*6 - 4)
						temp.write(str(Tcf_abaixo[i]), align="left", font=("Arial", 10, "normal"))
					temp.setx(distancia_x + 90)
					if not dividida_fria_abaixo[i]:
						temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]))), align="left", font=("Arial", 10, "normal"))
					else:
						correntes_desenho_sub_abaixo[i] = [0] * (quantidade_fria_abaixo[i] - 1)
						for j in range(quantidade_fria_abaixo[i]-1):
							temp.sety(y_abaixo - 8)
							temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]*fracoes_frias_abaixo[i][j]))), align="left", font=("Arial", 10, "normal"))
							correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
							correntes_desenho_sub_abaixo[i][j].color("blue")
							correntes_desenho_sub_abaixo[i][j].pensize(3)
							correntes_desenho_sub_abaixo[i][j].penup()
							correntes_desenho_sub_abaixo[i][j].setx(distancia_x - 20)
							correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
							correntes_desenho_sub_abaixo[i][j].pendown()
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(30)
							correntes_desenho_sub_abaixo[i][j].right(90)
							if Tcf_abaixo[i] == pinchf:
								correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 44)
							else:
								correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 140)
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(30*(j+1))
							correntes_desenho_sub_abaixo[i][j].left(90)
							correntes_desenho_sub_abaixo[i][j].forward(20)
							y_abaixo -= 30
						temp.sety(y_abaixo - 8)
						temp.write("Cp = " + str(float('{:.3f}'.format(correntes[i][2]*fracoes_frias_abaixo[i][quantidade_fria_abaixo[i]-1]))), align="left", font=("Arial", 10, "normal"))
					if Tcf_abaixo[i] == pinchf:
						correntes_desenho[i].forward(distancia_x - 4)
					else:
						correntes_desenho[i].forward(distancia_x - 100)
			if onde == "above":
				if dividida_fria_abaixo[i] and dividida_fria[i]:
					if quantidade_fria_abaixo[i] > quantidade_fria[i]:
						y_acima -= 30 * (quantidade_fria_abaixo[i] - quantidade_fria[i])
				elif dividida_fria_abaixo[i]:
					y_acima -= 30 * (quantidade_fria_abaixo[i] - 1)
			elif onde == "below":
				if dividida_fria[i] and dividida_fria_abaixo[i]:
					if quantidade_fria[i] > quantidade_fria_abaixo[i]:
						y_abaixo -= 30 * (quantidade_fria[i] - quantidade_fria_abaixo[i])
				elif dividida_fria[i]:
					y_abaixo -= 30 * (quantidade_fria[i] - 1)

			y_acima -= 30
			y_abaixo -= 30

	def pinch(tamanho):
		pinch = turtle.Turtle()
		pinch.shapesize(0.001, 0.001, 0.001)
		pinch.pensize(2)
		pinch.right(90)
		pinch.penup()
		pinch.sety(235)
		temp.sety(240)
		temp.setx(-len(str(pinchq))*3)
		temp.write(str(pinchq), align="left", font=("Arial", 10, "normal"))
		temp.right(90)
		tamanho = 235 - tamanho
		if str(tamanho)[-1] == 5:
			tamanho += 5

		for i in range(int(tamanho/10)+1):
			pinch.pendown()
			pinch.forward(5)
			pinch.penup()
			pinch.forward(5)
			temp.forward(10)
		temp.forward(20)
		temp.write(str(pinchf), align="left", font=("Arial", 10, "normal"))

	def inserir_trocador_desenho(onde, corrente_quente, corrente_fria, subestagio, trocadorr):
		trocador = turtle.Turtle()
		trocador.pensize(1.5)
		trocador.color("black", "white")
		trocador.shapesize(0.001, 0.001, 0.001)
		trocador.penup()
		if onde == "above":
			trocador.setx(-subestagio*50)
			temp.setx(-subestagio*50 - len(str(trocadorr[6]))*3)
			if dividida_quente[trocadorr[0]-1]:
				trocador.sety(corrente_quente.pos()[1] - 10 - 30*(trocadorr[2]-1))
				temp.sety(corrente_quente.pos()[1] + 10 - 30*(trocadorr[2]-1))
			else:
				trocador.sety(corrente_quente.pos()[1]-10)
				temp.sety(corrente_quente.pos()[1]+10)
			trocador.pendown()
			trocador.begin_fill()
			trocador.circle(10)
			trocador.end_fill()
			if dividida_fria[trocadorr[1]-1]:
				trocador.sety(corrente_fria.pos()[1] - 10 - 30*(trocadorr[3]-1))
			else:
				trocador.sety(corrente_fria.pos()[1] - 10)
			trocador.begin_fill()
			trocador.circle(10)
			trocador.end_fill()
		elif onde == "below":
			trocador.setx(subestagio*50)
			temp.setx(subestagio*50 - len(str(trocadorr[6]))*3)
			if dividida_quente_abaixo[trocadorr[0]-1]:
				trocador.sety(corrente_quente.pos()[1] - 10 - 30*(trocadorr[2]-1))
				temp.sety(corrente_quente.pos()[1] + 10 - 30*(trocadorr[2]-1))
			else:
				trocador.sety(corrente_quente.pos()[1]-10)
				temp.sety(corrente_quente.pos()[1]+10)
			trocador.pendown()
			trocador.begin_fill()
			trocador.circle(10)
			trocador.end_fill()
			if dividida_fria_abaixo[trocadorr[1]-1]:
				trocador.sety(corrente_fria.pos()[1] - 10 - 30*(trocadorr[3]-1))
			else:
				trocador.sety(corrente_fria.pos()[1] - 10)
			trocador.begin_fill()
			trocador.circle(10)
			trocador.end_fill()

		temp.write(str(trocadorr[6]), align="left", font=("Arial", 10, "normal"))

	def utilidade_desenho(onde, corrente, subestagio, calor):
		utilidade = turtle.Turtle()
		utilidade.pensize(1.5)
		utilidade.shapesize(0.001, 0.001, 0.001)
		utilidade.penup()
		if onde == "above":
			utilidade.color("black", "red")
			utilidade.setx(-subestagio*50)
			temp.setx(-subestagio*50 - len(str(calor))*3)
		elif onde == "below":
			utilidade.color("black", "blue")
			utilidade.setx(subestagio*50)
			temp.setx(subestagio*50 - len(str(calor))*3)
		utilidade.sety(corrente.pos()[1]-10)
		utilidade.pendown()
		utilidade.begin_fill()
		utilidade.circle(10)
		utilidade.end_fill()
		temp.sety(corrente.pos()[1]+10)
		temp.write(str(calor), align="left", font=("Arial", 10, "normal"))


	quentes("above", correntes_quentes, corrente_quente_presente_acima)
	frias("above", correntes_frias, corrente_fria_presente_acima)
	tamanho_acima = y_acima
	y_acima, y_abaixo = 200, 200
	quentes("below", correntes_quentes, corrente_quente_presente_abaixo)
	frias("below", correntes_frias, corrente_fria_presente_abaixo)
	tamanho_abaixo = y_abaixo
	if tamanho_acima > tamanho_abaixo:
		tamanho = tamanho_acima
	else:
		tamanho = tamanho_abaixo
	pinch(tamanho)

	if len(matriz_armazenada) > 0:
		subestagio = 0
		foi_pra_frente = False
		i = 0
		for trocadorr in matriz_armazenada:
			if Thf_acima[trocadorr[0]-1] != pinchq:
				if not foi_pra_frente and i < 2:
					subestagio += 2 - i
					foi_pra_frente = True
			if Tc0_acima[trocadorr[1]-1] != pinchf:
				if not foi_pra_frente and i < 2:
					subestagio += 2 - i
					foi_pra_frente = True
			subestagio += 1
			i += 1
			inserir_trocador_desenho("above", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr)

		if len(utilidades) > 0:
			for utilidadee in utilidades:
				subestagio += 1
				utilidade_desenho("above", correntes_frias[utilidadee[0]-1], subestagio, utilidadee[1])

	if len(matriz_trocadores_abaixo) > 0:
		subestagio = 0
		foi_pra_frente = False
		i = 0
		for trocadorr in matriz_trocadores_abaixo:
			if Th0_abaixo[trocadorr[0]-1] != pinchq:
				if not foi_pra_frente and i < 2:
					subestagio += 2 - i
					foi_pra_frente = True
			if Tcf_abaixo[trocadorr[1]-1] != pinchf:
				if not foi_pra_frente and i < 2:
					subestagio += 2 - i
					foi_pra_frente = True
			subestagio += 1
			i += 1
			inserir_trocador_desenho("below", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr)

		if len(utilidades_abaixo) > 0:
			for utilidadee in utilidades_abaixo:
				subestagio += 1
				utilidade_desenho("below", correntes_quentes[utilidadee[0]-1], subestagio, utilidadee[1])



	turtle.done()



def correntesnoscombos(nhot,ncold):

	nstages=2
	nsubstages=2

	for i in range (nhot):
		dlg.comboBox_2.addItem(str(i+1))     #acima   add heat ex
		dlg.comboBox_9.addItem(str(i+1))     #acima   quadro de correntes quentes
		dlg.comboBox_35.addItem(str(i+1))   #abaixo   add heat ex
		dlg.comboBox_43.addItem(str(i+1))    #abaixo   quadro de correntes quentes
		dlg.comboBox_51.addItem(str(i+1))	#n max de sub frias é o número de correntes quentes
		dlg.comboBox_54.addItem(str(i+1))
	for i in range (ncold):
		dlg.comboBox_5.addItem(str(i+1))      #acima add heat ex
		dlg.comboBox_10.addItem(str(i+1))     #acima quadro correntes frias
		dlg.comboBox_36.addItem(str(i+1))     #abaixo add heat ex
		dlg.comboBox_44.addItem(str(i+1))     #abaixo quadro de correntes frias
		dlg.comboBox_50.addItem(str(i+1))	#n max de sub quentes é o nomero de correntes frias
		dlg.comboBox_53.addItem(str(i+1))
	for i in range (nstages):
		dlg.comboBox_8.addItem(str(i+1))    #acima
		dlg.comboBox_39.addItem(str(i+1))   #abaixo
	for i in range (nsubstages):
		dlg.comboBox_7.addItem(str(i+1))    #acima
		dlg.comboBox_40.addItem(str(i+1))

def violou_dtmin(trocador_violado, onde, dados_do_trocador):
	dlg.dtmin = uic.loadUi("dtmin.ui")
	dlg.dtmin.show()
	text = "ΔT = " + str(float('{:.1f}'.format(trocador_violado[6])))
	textfrio = "ΔT = " + str(float('{:.1f}'.format(trocador_violado[7])))

	if onde == "above":
		dlg.dtmin.label_7.setText(str(len(matriz_armazenada)))
		dlg.dtmin.pushButton.clicked.connect(lambda: above(dados_do_trocador))
	if onde == "below":
		dlg.dtmin.label_7.setText(str(len(matriz_trocadores_abaixo)))
		dlg.dtmin.pushButton.clicked.connect(lambda: below(dados_do_trocador))

	dlg.dtmin.label_3.setText(text)
	dlg.dtmin.label_4.setText(textfrio)

	if trocador_violado[6] < dTmin:
		dlg.dtmin.label_3.setStyleSheet("QLabel {color: red}")
	if trocador_violado[7] < dTmin:
		dlg.dtmin.label_4.setStyleSheet("QLabel {color: red}")

	dlg.dtmin.pushButton_2.clicked.connect(lambda: dlg.dtmin.close())


	def above(dados_do_trocador):
		indice = len(matriz_armazenada) - 1
		remover_trocador(dlg, dados_do_trocador, indice, matriz_armazenada)
		printar()
		checaresgotadosacima()
		dlg.dtmin.close()

	def below(dados_do_trocacdor):
		indice = len(matriz_trocadores_abaixo) - 1
		remover_trocador_abaixo(dlg, dados_do_trocador, indice, matriz_trocadores_abaixo)
		printar_abaixo()
		checaresgotadosabaixo()
		dlg.dtmin.close()

def dividir_corrente(divisao, onde):
	global divtype
	divtype = divisao
	dlg.DivisaoQuente = uic.loadUi("DivisaoQuente.ui")
	dlg.DivisaoFria = uic.loadUi("DivisaoQuente.ui")
	if divtype == "Q":
		for i in range(nhot):
			dlg.DivisaoQuente.comboBox_2.addItem(str(i+1))
		for i in range(nstages):
			dlg.DivisaoQuente.comboBox.addItem(str(i+1))
		for i in range(ncold):
			dlg.DivisaoQuente.comboBox_3.addItem(str(i+1))
		dlg.DivisaoQuente.show()
	elif divtype == "F":
		dlg.DivisaoFria.label_5.setText("Split Cold Stream")
		for i in range(ncold):
			dlg.DivisaoFria.comboBox_2.addItem(str(i+1))
		for i in range(nstages):
			dlg.DivisaoFria.comboBox.addItem(str(i+1))
		for i in range(nhot):
			dlg.DivisaoFria.comboBox_3.addItem(str(i+1))
		dlg.DivisaoFria.show()


	def confirm():
		global caixa_fracao, quantidade, corrente, estagio
		if divtype == "Q":
			quantidade = int(dlg.DivisaoQuente.comboBox_3.currentText())
			estagio = int(dlg.DivisaoQuente.comboBox.currentText())
			corrente = int(dlg.DivisaoQuente.comboBox_2.currentText())
		if divtype == "F":
			quantidade = int(dlg.DivisaoFria.comboBox_3.currentText())
			estagio = int(dlg.DivisaoFria.comboBox.currentText())
			corrente = int(dlg.DivisaoFria.comboBox_2.currentText())

		if verificar_trocador_estagio(estagio) and onde == "above":
			QMessageBox.about(dlg, "Error!", "There is already a heat exchanger in this position, remove it before making the division.")
			return

		if verificar_trocador_estagio_abaixo(estagio) and onde == "below":
			QMessageBox.about(dlg, "Error!", "There is already a heat exchanger in this position, remove it before making the division.")
			return

		if divtype == "Q":
			dlg.DivisaoQuente.pushButton_3.setEnabled(True)
			dlg.DivisaoQuente.pushButton.setEnabled(False)
		if divtype == "F":
			dlg.DivisaoFria.pushButton_3.setEnabled(True)
			dlg.DivisaoFria.pushButton.setEnabled(False)

		caixa_fracao = [0] * quantidade
		caixa_corrente = [0] * quantidade

		for i in range(quantidade):
			caixa_fracao[i] = QtWidgets.QDoubleSpinBox(dlg)
			caixa_corrente[i] = QtWidgets.QLabel(dlg)
			if divtype == "Q":
				dlg.DivisaoQuente.verticalLayout_3.addWidget(caixa_corrente[i])
				dlg.DivisaoQuente.verticalLayout_3.addWidget(caixa_fracao[i])
			if divtype == "F":
				dlg.DivisaoFria.verticalLayout_3.addWidget(caixa_corrente[i])
				dlg.DivisaoFria.verticalLayout_3.addWidget(caixa_fracao[i])
			caixa_fracao[i].setSingleStep(float(0.1))
			caixa_fracao[i].setMaximum(1)
			caixa_fracao[i].setMinimum(0)
			caixa_corrente[i].setText("Substream {}".format(i+1))
			caixa_corrente[i].setAlignment(Qt.AlignCenter)
			caixa_fracao[i].setAlignment(Qt.AlignCenter)

	def split(onde):
		soma = 0
		fracao = [0] * quantidade
		for i in range(quantidade):
			soma += float(caixa_fracao[i].value())
			fracao[i] = float(caixa_fracao[i].value())
		# if soma != 1:
		# 	QMessageBox.about(dlg, "Error!", "The sum of the fractions must be equals 1.")
		# 	return

		if onde == "above":
			divisao_de_correntes(divtype, estagio, corrente, quantidade, fracao)
			testar_correntes(dlg)
		elif onde == "below":
			divisao_de_correntes_abaixo(divtype, estagio, corrente, quantidade, fracao)
			testar_correntes_abaixo(dlg)

		if divtype == "Q":
			dlg.DivisaoQuente.close()
		if divtype == "F":
			dlg.DivisaoFria.close()

		printar()

	dlg.DivisaoQuente.pushButton.clicked.connect(lambda: confirm())
	dlg.DivisaoQuente.pushButton_3.clicked.connect(lambda: split(onde))
	dlg.DivisaoQuente.pushButton_2.clicked.connect(lambda: dlg.DivisaoQuente.close())
	dlg.DivisaoFria.pushButton.clicked.connect(lambda: confirm())
	dlg.DivisaoFria.pushButton_3.clicked.connect(lambda: split(onde))
	dlg.DivisaoFria.pushButton_2.clicked.connect(lambda: dlg.DivisaoFria.close())


#above
def printar():
	dlg.tableWidget_3.clearContents()
	dlg.tableWidget_4.clearContents()

	pinch_quente_texto = "Hot Pinch Temperature: " + str(pinchq)
	pinch_frio_texto = "Cold Pinch Temperature: " + str(pinchf)

	dlg.label_15.setText(pinch_quente_texto)
	dlg.label_12.setText(pinch_frio_texto)

	if dlg.checkBox.isChecked():
		linha = 0
		linhas = 0
		for i in quantidade_quente:
			linhas += i
		dlg.tableWidget_3.setRowCount(linhas)
		for corrente in range(nhot):
			if dividida_quente[corrente]:
				for sub in range(quantidade_quente[corrente]):
					text = str(corrente+1) + "." + str(sub+1)
					dlg.tableWidget_3.setItem(linha, 0, QTableWidgetItem(text))
					dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0[corrente])))))
					if corrente_quente_presente_acima[corrente]:
						dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente[corrente][sub])))))
						dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf_acima[corrente])))))
						dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente_sub[corrente][sub])))))
					else:
						dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_3.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0[corrente])))))
				if corrente_quente_presente_acima[corrente]:
					dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_mesclada[corrente])))))
					dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf_acima[corrente])))))
					dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente[corrente])))))
				else:
					dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem("-"))
					dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem("-"))
					dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem("-"))
					dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem("-"))
				linha += 1
	else:
		dlg.tableWidget_3.setRowCount(nhot)
		for corrente in range(nhot):
			dlg.tableWidget_3.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
			dlg.tableWidget_3.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0[corrente])))))
			if corrente_quente_presente_acima[corrente]:
				dlg.tableWidget_3.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_mesclada[corrente])))))
				dlg.tableWidget_3.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf_acima[corrente])))))
				dlg.tableWidget_3.setItem(corrente, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente[corrente])))))
			else:
				dlg.tableWidget_3.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_3.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_3.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_3.setItem(corrente, 4, QTableWidgetItem("-"))

	if dlg.checkBox_2.isChecked():
		linha = 0
		linhas = 0
		for i in quantidade_fria:
			linhas += i
		dlg.tableWidget_4.setRowCount(linhas)
		for corrente in range(ncold):
			if dividida_fria[corrente]:
				for sub in range(quantidade_fria[corrente]):
					text = str(corrente+1) + "." + str(sub+1)
					dlg.tableWidget_4.setItem(linha, 0, QTableWidgetItem(text))
					dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf[corrente])))))
					if corrente_fria_presente_acima[corrnte]:
						dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria[corrente][sub])))))
						dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0_acima[corrente])))))
						dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio_sub[corrente][sub])))))
					else:
						dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_4.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf[corrente])))))
				if corrente_fria_presente_acima[corrente]:
					dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_mesclada[corrente])))))
					dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0_acima[corrente])))))
					dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio[corrente])))))
				else:
					dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem("-"))
					dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem("-"))
					dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem("-"))
					dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem("-"))
				linha += 1
	else:
		dlg.tableWidget_4.setRowCount(ncold)
		for corrente in range(ncold):
			dlg.tableWidget_4.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
			dlg.tableWidget_4.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf[corrente])))))
			if corrente_fria_presente_acima[corrente]:
				dlg.tableWidget_4.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_mesclada[corrente])))))
				dlg.tableWidget_4.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0_acima[corrente])))))
				dlg.tableWidget_4.setItem(corrente, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio[corrente])))))
			else:
				dlg.tableWidget_4.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_4.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_4.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_4.setItem(corrente, 4, QTableWidgetItem("-"))


	dlg.tableWidget_2.setRowCount(len(matriz_armazenada))
	if len(matriz_armazenada) > 0:
		for trocador in range(0, len(matriz_armazenada)):
			dlg.tableWidget_2.setItem(trocador, 0, QTableWidgetItem(str(matriz_armazenada[trocador][0]))) #chot
			dlg.tableWidget_2.setItem(trocador, 1, QTableWidgetItem(str(matriz_armazenada[trocador][1]))) #ccold
			dlg.tableWidget_2.setItem(trocador, 2, QTableWidgetItem(str(matriz_armazenada[trocador][2]))) #sbhot
			dlg.tableWidget_2.setItem(trocador, 3, QTableWidgetItem(str(matriz_armazenada[trocador][3]))) #sbcold
			dlg.tableWidget_2.setItem(trocador, 4, QTableWidgetItem(str(matriz_armazenada[trocador][4]))) #sk
			dlg.tableWidget_2.setItem(trocador, 5, QTableWidgetItem(str(matriz_armazenada[trocador][5]))) #k
			dlg.tableWidget_2.setItem(trocador, 6, QTableWidgetItem(str(float('{:.1f}'.format(matriz_armazenada[trocador][6]))))) # calor trocado
			dlg.tableWidget_2.setItem(trocador, 7, QTableWidgetItem(str(float('{:.1f}'.format(matriz_armazenada[trocador][7]))))) #Thin
			dlg.tableWidget_2.setItem(trocador, 8, QTableWidgetItem(str(float('{:.1f}'.format(matriz_armazenada[trocador][8]))))) #Tcout
			dlg.tableWidget_2.setItem(trocador, 9, QTableWidgetItem(str(matriz_armazenada[trocador][9]))) #fração hot
			dlg.tableWidget_2.setItem(trocador, 10, QTableWidgetItem(str(matriz_armazenada[trocador][10]))) #fraçao cold
		dlg.lineEdit_5.setText(str("0"))

	if len(utilidades) > 0:
		dlg.tableWidget_2.setRowCount(len(matriz_armazenada) + len(utilidades))
		for utilidade in range(0, len(utilidades)):
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 0, QTableWidgetItem(str("Hot Utility")))
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 1, QTableWidgetItem(str(utilidades[utilidade][0])))
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 6, QTableWidgetItem(str(float('{:.1f}'.format(utilidades[utilidade][1])))))

def inserir_teste():
	dados_do_trocador = ler_dados(dlg)
	try:
		nova_matriz, violou, trocador_violado = inserir_trocador(dlg, dados_do_trocador)
		matriz_armazenada.append(nova_matriz[-1])
	except:
		print("erro inserir teste")
		return
	if violou:
		violou_dtmin(trocador_violado, "above", dados_do_trocador)
		printar()
		checaresgotadosacima()
	else:
		printar()
		checaresgotadosacima()

def remover_teste():
	indice_remover = dlg.tableWidget_2.currentRow()
	if indice_remover <= len(matriz_armazenada) - 1:
		if len(utilidades) > 0:
			for i in range(len(Tc0),-1, -1):
				for j in range(len(utilidades)):
					if utilidades[j][0] == i+1:
						try:
							remover_utilidade(i+1, j, utilidades)
						except:
							print("erro remover teste")
		dlg.comboBox_10.setEnabled(False)
		dlg.pushButton_8.setEnabled(False)
		trocador_remover = matriz_armazenada[indice_remover]
		remover_trocador(dlg, trocador_remover, indice_remover, matriz_armazenada)
		atualizar_matriz(matriz_armazenada)
	else:
		indice_remover = dlg.tableWidget_2.currentRow() - len(matriz_armazenada)
		utilidade_remover = utilidades[indice_remover]
		corrente_remover_utilidade = utilidade_remover[0]
		remover_utilidade(corrente_remover_utilidade, indice_remover, utilidades)
	printar()

def utilidade_teste_acima():
	corrente = int(dlg.comboBox_10.currentText())
	utilidadee = adicionar_utilidade(dlg, corrente)
	try:
		utilidades.append(utilidadee[-1])
		utilidades.sort()
	except:
		print("erro utilidade teste acima")
	printar()

def calcular_calor_teste():
	dlg.TempLoadAbove=uic.loadUi("TempLoadAbove.ui")
	dlg.TempLoadAbove.show()

	for i in range (nhot):
		dlg.TempLoadAbove.comboBox.addItem(str(i+1))
	for i in range (ncold):
		dlg.TempLoadAbove.comboBox_2.addItem(str(i+1))
	for i in range(nstages):
		dlg.TempLoadAbove.comboBox_5.addItem(str(i+1))
	for i in range(nsk):
		dlg.TempLoadAbove.comboBox_6.addItem(str(i+1))

	dlg.TempLoadAbove.comboBox.setCurrentText(str(dlg.comboBox_2.currentText()))
	dlg.TempLoadAbove.comboBox_2.setCurrentText(str(dlg.comboBox_5.currentText()))
	dlg.TempLoadAbove.comboBox_3.setCurrentText(str(dlg.comboBox_50.currentText()))
	dlg.TempLoadAbove.comboBox_4.setCurrentText(str(dlg.comboBox_51.currentText()))
	dlg.TempLoadAbove.comboBox_5.setCurrentText(str(dlg.comboBox_8.currentText()))
	dlg.TempLoadAbove.comboBox_6.setCurrentText(str(dlg.comboBox_7.currentText()))

	dlg.TempLoadAbove.pushButton_2.clicked.connect(lambda: dlg.TempLoadAbove.close())
	dlg.TempLoadAbove.pushButton.clicked.connect(lambda: caixa_de_temperatura(dlg))

def checaresgotadosacima():
	contadordutycold = 0
	contadordutyhot = 0

	for corrente in range(nhot):
		if calor_atual_quente[corrente] == 0:
			contadordutyhot += 1
	for corrente in range(ncold):
		if calor_atual_frio[corrente] == 0:
			contadordutycold += 1

	objetivo_quente = nhot
	objetivo_frio = ncold


	if contadordutyhot == objetivo_quente:
		dlg.comboBox_10.setEnabled(True)
		dlg.pushButton_8.setEnabled(True)
	else:
		dlg.comboBox_10.setEnabled(False)
		dlg.pushButton_8.setEnabled(False)

	if contadordutycold == objetivo_frio:
		dlg.comboBox_9.setEnabled(True)
		dlg.pushButton_7.setEnabled(True)
	else:
		dlg.comboBox_9.setEnabled(False)
		dlg.pushButton_7.setEnabled(False)

	if contadordutyhot == objetivo_quente and contadordutycold == objetivo_frio:
		dlg.comboBox_9.setEnabled(False)
		dlg.comboBox_10.setEnabled(False)
		dlg.pushButton_7.setEnabled(False)
		dlg.pushButton_8.setEnabled(False)

#below
def printar_abaixo():
	dlg.tableWidget_15.clearContents()
	dlg.tableWidget_17.clearContents()

	pinch_quente_texto = "Hot Pinch Temperature: " + str(pinchq)
	pinch_frio_texto = "Cold Pinch Temperature: " + str(pinchf)

	dlg.label_17.setText(pinch_quente_texto)
	dlg.label_21.setText(pinch_frio_texto)

	if dlg.checkBox_9.isChecked():
		linha = 0
		linhas = 0
		for i in quantidade_quente_abaixo:
			linhas += i
		dlg.tableWidget_15.setRowCount(linhas)
		for corrente in range(nhot):
			if dividida_quente_abaixo[corrente]:
				for sub in range(quantidade_quente_abaixo[corrente]):
					text = str(corrente+1) + "." + str(sub+1)
					dlg.tableWidget_15.setItem(linha, 0, QTableWidgetItem(text))
					dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0_abaixo[corrente])))))
					if corrente_quente_presente_abaixo[corrente]:
						dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_abaixo[corrente][sub])))))
						dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf[corrente])))))
						dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente_sub_abaixo[corrente][sub])))))
					else:
						dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_15.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0_abaixo[corrente])))))
				if corrente_quente_presente_abaixo[corrente]:
					dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_mesclada_abaixo[corrente])))))
					dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf[corrente])))))
					dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente_abaixo[corrente])))))
				else:
					dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem("-"))
					dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem("-"))
					dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem("-"))
					dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem("-"))

				linha += 1
	else:
		dlg.tableWidget_15.setRowCount(nhot)
		for corrente in range(nhot):
			dlg.tableWidget_15.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
			dlg.tableWidget_15.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0_abaixo[corrente])))))
			if corrente_quente_presente_abaixo[corrente]:
				dlg.tableWidget_15.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_mesclada_abaixo[corrente])))))
				dlg.tableWidget_15.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf[corrente])))))
				dlg.tableWidget_15.setItem(corrente, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente_abaixo[corrente])))))
			else:
				dlg.tableWidget_15.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_15.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_15.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_15.setItem(corrente, 4, QTableWidgetItem("-"))

	if dlg.checkBox_10.isChecked():
		linha = 0
		linhas = 0
		for i in quantidade_fria_abaixo:
			linhas += i
		dlg.tableWidget_17.setRowCount(linhas)
		for corrente in range(ncold):
			if dividida_fria_abaixo[corrente]:
				for sub in range(quantidade_fria_abaixo[corrente]):
					text = str(corrente+1) + "." + str(sub+1)
					dlg.tableWidget_17.setItem(linha, 0, QTableWidgetItem(text))
					dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf_abaixo[corrente])))))
					if corrente_fria_presente_abaixo[corrente]:
						dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_abaixo[corrente][sub])))))
						dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0[corrente])))))
						dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio_sub_abaixo[corrente][sub])))))
					else:
						dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_17.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf_abaixo[corrente])))))
				if corrente_fria_presente_abaixo[corrente]:
					dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_mesclada_abaixo[corrente])))))
					dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0[corrente])))))
					dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio_abaixo[corrente])))))
				else:
					dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem("-"))
					dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem("-"))
					dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem("-"))
					dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem("-"))
				linha += 1
	else:
		dlg.tableWidget_17.setRowCount(ncold)
		for corrente in range(ncold):
			dlg.tableWidget_17.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
			dlg.tableWidget_17.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf_abaixo[corrente])))))
			if corrente_fria_presente_abaixo[corrente]:
				dlg.tableWidget_17.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_mesclada_abaixo[corrente])))))
				dlg.tableWidget_17.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0[corrente])))))
				dlg.tableWidget_17.setItem(corrente, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio_abaixo[corrente])))))
			else:
				dlg.tableWidget_17.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_17.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_17.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_17.setItem(corrente, 4, QTableWidgetItem("-"))


	dlg.tableWidget_14.setRowCount(len(matriz_trocadores_abaixo))
	if len(matriz_trocadores_abaixo) > 0:
		for trocador in range(0, len(matriz_trocadores_abaixo)):
			dlg.tableWidget_14.setItem(trocador, 0, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][0]))) #chot
			dlg.tableWidget_14.setItem(trocador, 1, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][1]))) #ccold
			dlg.tableWidget_14.setItem(trocador, 2, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][2]))) #sbhot
			dlg.tableWidget_14.setItem(trocador, 3, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][3]))) #sbcold
			dlg.tableWidget_14.setItem(trocador, 4, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][4]))) #sk
			dlg.tableWidget_14.setItem(trocador, 5, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][5]))) #k
			dlg.tableWidget_14.setItem(trocador, 6, QTableWidgetItem(str(float('{:.1f}'.format(matriz_trocadores_abaixo[trocador][6]))))) # calor trocado
			dlg.tableWidget_14.setItem(trocador, 7, QTableWidgetItem(str(float('{:.1f}'.format(matriz_trocadores_abaixo[trocador][7]))))) #Thin
			dlg.tableWidget_14.setItem(trocador, 8, QTableWidgetItem(str(float('{:.1f}'.format(matriz_trocadores_abaixo[trocador][8]))))) #Tcout
			dlg.tableWidget_14.setItem(trocador, 9, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][9]))) #fração hot
			dlg.tableWidget_14.setItem(trocador, 10, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][10]))) #fraçao cold
		dlg.lineEdit_25.setText(str("0"))

	if len(utilidades_abaixo) > 0:
		dlg.tableWidget_14.setRowCount(len(matriz_trocadores_abaixo) + len(utilidades_abaixo))
		for utilidade in range(0, len(utilidades_abaixo)):
			dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 0, QTableWidgetItem(str("Cold Utility")))
			dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 1, QTableWidgetItem(str(utilidades_abaixo[utilidade][0])))
			dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 6, QTableWidgetItem(str(float('{:.1f}'.format(utilidades_abaixo[utilidade][1])))))

def inserir_teste_abaixo():
	dados_do_trocador = ler_dados_abaixo(dlg)
	try:
		nova_matriz, violou, trocador_violado = inserir_trocador_abaixo(dlg, dados_do_trocador)
		matriz_trocadores_abaixo.append(nova_matriz[-1])
	except:
		print("erro, inserir teste abaixo")
		return
	if violou:
		violou_dtmin(trocador_violado, "below", dados_do_trocador)
		printar_abaixo()
		checaresgotadosabaixo()
	else:
		printar_abaixo()
		checaresgotadosabaixo()

def remover_teste_abaixo():
	indice_remover = dlg.tableWidget_14.currentRow()
	if indice_remover <= len(matriz_trocadores_abaixo) - 1:
		if len(utilidades_abaixo) > 0:
			for i in range(nhot, -1, -1):
				for j in range(len(utilidades_abaixo)):
					if utilidades_abaixo[j][0] == i+1:
						try:
							remover_utilidade_abaixo(i+1, j, utilidades_abaixo)
						except:
							print("erro remover teste abaixo")
		dlg.comboBox_43.setEnabled(False)
		dlg.pushButton_20.setEnabled(False)
		trocador_remover = matriz_trocadores_abaixo[indice_remover]
		remover_trocador_abaixo(dlg, trocador_remover, indice_remover, matriz_trocadores_abaixo)
		atualizar_matriz_abaixo(matriz_trocadores_abaixo)
	else:
		indice_remover = dlg.tableWidget_14.currentRow() - len(matriz_trocadores_abaixo)
		utilidade_remover = utilidades_abaixo[indice_remover]
		corrente_remover_utilidade = utilidade_remover[0]
		remover_utilidade_abaixo(corrente_remover_utilidade, indice_remover, utilidades_abaixo)
	printar_abaixo()

def utilidade_teste_abaixo():
	corrente = int(dlg.comboBox_43.currentText())
	utilidadee = adicionar_utilidade_abaixo(dlg, corrente)
	try:
		utilidades_abaixo.append(utilidadee[-1])
		utilidades_abaixo.sort()
	except:
		print("utilidade teste abaixo")
	printar_abaixo()

def calcular_calor_abaixo():
	dlg.TempLoadBelow = uic.loadUi("TempLoadBelow.ui")
	dlg.TempLoadBelow.show()

	for i in range(nhot):
		dlg.TempLoadBelow.comboBox.addItem(str(i+1))
	for i in range(ncold):
		dlg.TempLoadBelow.comboBox_2.addItem(str(i+1))
	for i in range(nstages):
		dlg.TempLoadBelow.comboBox_5.addItem(str(i+1))
	for i in range(nsk):
		dlg.TempLoadBelow.comboBox_6.addItem(str(i+1))

	dlg.TempLoadBelow.comboBox.setCurrentText(str(dlg.comboBox_35.currentText()))
	dlg.TempLoadBelow.comboBox_2.setCurrentText(str(dlg.comboBox_36.currentText()))
	dlg.TempLoadBelow.comboBox_3.setCurrentText(str(dlg.comboBox_53.currentText()))
	dlg.TempLoadBelow.comboBox_4.setCurrentText(str(dlg.comboBox_54.currentText()))
	dlg.TempLoadBelow.comboBox_5.setCurrentText(str(dlg.comboBox_39.currentText()))
	dlg.TempLoadBelow.comboBox_6.setCurrentText(str(dlg.comboBox_40.currentText()))


	dlg.TempLoadBelow.pushButton.clicked.connect(lambda: caixa_de_temperatura_abaixo(dlg))
	dlg.TempLoadBelow.pushButton_2.clicked.connect(lambda: dlg.TempLoadBelow.close())

def checaresgotadosabaixo():
	contadordutyhot=0
	contadordutycold=0

	for corrente in range(nhot):
		if dividida_quente_abaixo[corrente]:
			for sub in range(quantidade_quente_abaixo[corrente]):
				if calor_atual_quente_sub_abaixo[corrente][sub] == 0:
					contadordutyhot += 1
		else:
			if calor_atual_quente_abaixo[corrente] == 0:
				contadordutyhot += 1
	for corrente in range(ncold):
		if dividida_fria_abaixo[corrente]:
			for sub in range(quantidade_fria_abaixo[corrente]):
				if calor_atual_frio_sub_abaixo[corrente][sub] == 0:
					contadordutycold += 1
		else:
			if calor_atual_frio_abaixo[corrente] == 0:
				contadordutycold += 1

	objetivo_quente = 0
	objetivo_frio = 0

	for i in quantidade_quente_abaixo:
		objetivo_quente += i
	for i in quantidade_fria_abaixo:
		objetivo_frio += i

	if contadordutyhot == objetivo_quente:
		dlg.comboBox_44.setEnabled(True)
		dlg.pushButton_21.setEnabled(True)
	else:
		dlg.comboBox_44.setEnabled(False)
		dlg.pushButton_21.setEnabled(False)

	if contadordutycold == objetivo_frio:
		dlg.comboBox_43.setEnabled(True)
		dlg.pushButton_20.setEnabled(True)
	else:
		dlg.comboBox_43.setEnabled(False)
		dlg.pushButton_20.setEnabled(False)

	if contadordutyhot == objetivo_quente and contadordutycold == objetivo_frio:
		dlg.comboBox_43.setEnabled(False)
		dlg.comboBox_44.setEnabled(False)
		dlg.pushButton_20.setEnabled(False)
		dlg.pushButton_21.setEnabled(False)




#streams
dlg.pinchbutton.setEnabled(False) #block o botao pinch até apertar done
dlg.tabWidget.setTabEnabled(1,False) #block stream diagram até fazer o pinch
dlg.tabWidget.setTabEnabled(2,False) #block composite curver até fazer o pinch
dlg.tabWidget.setTabEnabled(3,False) #block heat exchangers até fazer o pinch
dlg.tabWidget.setTabEnabled(4,True) #block heat exchangers network até fazer o pinch
dlg.pushButton.clicked.connect(apertaradd) #add stream
dlg.actionOpen_2.triggered.connect(openfile_teste) #file > open
dlg.donebutton.clicked.connect(done_teste) #done
dlg.pinchbutton.clicked.connect(pinch_teste) #pinch
#dlg.tableWidget.itemChanged.connect(itemedited)
dlg.tempcombo1.currentIndexChanged.connect(lambda i: i == 0 and SI(dlg))
dlg.tempcombo1.currentIndexChanged.connect(lambda i: i == 1 and sistemaingles(dlg))
dlg.comboBox.currentIndexChanged.connect(lambda i: i == 1 and celsius(dlg))
dlg.comboBox.currentIndexChanged.connect(lambda i: i == 0 and kelvin(dlg))
dlg.comboBox.currentIndexChanged.connect(lambda i: i == 2 and farenheit(dlg))
dlg.comboBox.currentIndexChanged.connect(lambda i: i == 3 and rankine(dlg))
dlg.comboBox_3.currentIndexChanged.connect(lambda i: i == 0 and btu(dlg))
dlg.comboBox_3.currentIndexChanged.connect(lambda i: i == 1 and kW(dlg))

#above
dlg.radioButton.toggled.connect(lambda: dlg.lineEdit_5.setEnabled(True)) #quando marca o heat load libera a linha pra digitar
dlg.radioButton_4.toggled.connect(lambda: dlg.lineEdit_5.setEnabled(False)) #block o heat load quando max heat ta ativado
dlg.radioButton_4.setChecked(True) #por padrao abre o prog com max heat selecionado
dlg.pushButton_9.clicked.connect(lambda: dividir_corrente("Q", "above"))
dlg.pushButton_13.clicked.connect(lambda: dividir_corrente("F", "above"))
dlg.comboBox_9.setEnabled(False) #corrente quente que vai utilizade
dlg.comboBox_10.setEnabled(False) #corrente fria que vai utilidade
dlg.pushButton_7.setEnabled(False) #add utility hot
dlg.pushButton_8.setEnabled(False) #add utility cold
dlg.checkBox.stateChanged.connect(printar) #show splited streams printa tudo dnv
dlg.checkBox_2.stateChanged.connect(printar) #show splited streams printa tudo dnv
dlg.pushButton_6.clicked.connect(inserir_teste) #add heat exchanger
dlg.pushButton_10.clicked.connect(remover_teste) #remove heat exchanger
dlg.pushButton_14.clicked.connect(calcular_calor_teste) #choose stream temperature to calculate heat
dlg.pushButton_8.clicked.connect(utilidade_teste_acima) #add cold utility
dlg.pushButton_16.clicked.connect(lambda: desenhar_rede(correntes_quentes, correntes_frias))

#below
dlg.radioButton_17.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(True)) #quando marca o heat load libera a linha pra digitar
dlg.radioButton_20.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(False)) #block o heat load quando max heat ta ativado
dlg.radioButton_20.setChecked(True) #por padrao abre o prog com max heat selecionado
dlg.pushButton_12.clicked.connect(lambda: dividir_corrente("F", "below"))
dlg.pushButton_11.clicked.connect(lambda: dividir_corrente("Q", "below"))
dlg.comboBox_43.setEnabled(False) #corrente quente que vai utilizade
dlg.comboBox_44.setEnabled(False) #corrente fria que vai utilidade
dlg.pushButton_20.setEnabled(False) #add utility hot
dlg.pushButton_21.setEnabled(False) #add utility cold
dlg.checkBox_9.stateChanged.connect(printar_abaixo) #show splited streams printa tudo dnv
dlg.checkBox_10.stateChanged.connect(printar_abaixo) #show splited streams printa tudo dnv
dlg.pushButton_18.clicked.connect(inserir_teste_abaixo) #add heat exchanger
dlg.pushButton_15.clicked.connect(remover_teste_abaixo) #remove heat exchanger
dlg.pushButton_17.clicked.connect(calcular_calor_abaixo) #choose stream temperature to calculate heat
dlg.pushButton_20.clicked.connect(utilidade_teste_abaixo) #add hot utility
dlg.pushButton_19.clicked.connect(lambda: desenhar_rede(correntes_quentes, correntes_frias))


header = dlg.tableWidget.horizontalHeader()
header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)



dlg.show()
dlg.showMaximized()
app.exec()
