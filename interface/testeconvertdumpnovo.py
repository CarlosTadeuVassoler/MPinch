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
from variaveistempload2 import VariaveisTempLoad
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from prog_carlos import *
from prog_carlos_abaixo import *
from converter_unidades import *

from matplotlib.figure import Figure


matriz = []
matriz_armazenada = []
matriz_trocadores_abaixo = []
utilidades = []
utilidades_abaixo = []

app=QtWidgets.QApplication([])
dlg=uic.loadUi("untitlednova.ui")
dlg.TempLoad=uic.loadUi("TempLoad.ui")

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
nstages=2
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
correntestrocador=[]
nlinhas=1
nlinhas2=1
somatorio=0
somatorio2=0
estagio=0
qsi=0
qsj=0
fracao_quente=0
fracao_fria=0
ccold=0
chot=0
Fharr=0
Fcarr=0
ncoldc=0
nhotc=0
Qtabela0 = Qhot0 = Qcold0 = Thin0 = Tcout0 =0
opcao = 0
alternativa = 0
ntrocadores = []
Qarr = np.array ([0])


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
	#print(temptable)
	if (dlg.comboBox.currentText()) == 'Kelvin':
		temptable=temptable[0:] + ' K'
	else:
		temptable=temptable[0:] + ' ºF'
	return temptable

def colocarunidadescp(temptable):
	temptable=str(temptable)
	#print(temptable)
	if (dlg.comboBox.currentText()) == 'Kelvin':
		temptable=temptable[0:] + ' kW/K'
	else:
		temptable=temptable[0:] + ' Btu/ºF'
	return temptable

def HotnCold (tin,ten,i,) :      #ve se é corrente quente ou fria
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
	global correntes, dTmin, correntesncorrigidas, ntrocadores
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
	#print(type(correntes[0][2]))
	dlg.pinchbutton.setEnabled(True)
	#print(n)
	if (dlg.tempcombo1.currentText()) == 'Imperial units':
		unidadeusada[0]="Temperature (ºF)"
		unidadeusada[1]="Enthalpy (Btu)"
		unidadeusada[2]="Enthalpy (Btu)"
	dTmin=float(dlg.lineEdit_2.text())
	correntesncorrigidas=correntes
	#print(correntesncorrigidas,correntes)
	correntes[1][2]=1.5
	correntestrocadorr()
	ntrocadores=[0]*n

def apertarpinchbutton():
	global donee,alreadypinched,plotou, Th0, Thf, CPh, Tc0, Tcf, CPc
	#print(donee)
	Th0, Thf, CPh, Tc0, Tcf, CPc = [], [], [], [], [], []
	if donee == 1 :
		global correntes, dTmin, Tdecre, Tmin, Tmax, cascat2certo ,dT, estagios,cascat2,utilidadesquente,menor,pinchf,pinchq
		global n
		global dT
		dTmin, Tdecre, Tmin, Tmax, cascat2certo,dT,pinchf,pinchq,cascat2,utilidadesquente,menor = pontopinch(correntes, n, dTmin, Tdecre, Tmin, Tmax, cascat2certo, dT,pinch,dH,cascat,utilidadesquente,menor,cascat2)
		#print(dT)
		plotargrafico1(correntes, n, caixinha,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch,unidadeusada,plotou)
		plotargrafico2(correntes, n, caixinha3,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,pinchf,pinchq,unidadeusada)
		plotargrafico3(correntes, n, caixinha4,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,pinchf,pinchq,menor,cascat2,unidadeusada)
		estagios=estruturas(correntes, n, dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,estagios)
		trocador(correntes, n,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,estagios)
		#print(nhot,ncold,correntesncorrigidas)
		for i in range (n): #correção das temperaturas
			if correntesncorrigidas[i][3] == "Hot":
				correntesncorrigidas [i][0]=(correntesncorrigidas[i][0]) + (dTmin)/2
				correntesncorrigidas [i][1]=(correntesncorrigidas[i][1]) + (dTmin)/2
			if correntesncorrigidas[i][3] == "Cold":
				correntesncorrigidas [i][0]=(correntesncorrigidas[i][0]) - (dTmin)/2
				correntesncorrigidas [i][1]=(correntesncorrigidas[i][1]) - (dTmin)/2

		for i in range(n):
			if correntesncorrigidas[i][3] == "Hot":
				Th0.append(correntesncorrigidas[i][0])
				Thf.append(correntesncorrigidas[i][1])
				CPh.append(correntesncorrigidas[i][2])
			if correntesncorrigidas[i][3] == "Cold":
				Tc0.append(correntesncorrigidas[i][0])
				Tcf.append(correntesncorrigidas[i][1])
				CPc.append(correntesncorrigidas[i][2])
		#tudo(Th0, Thf, CPh, Tc0, Tcf, CPc)

		#abaixo(correntes,pinchq,pinchf,n,nhot,ncold)
		#acima(correntes,pinchq,pinchf,n,nhot,ncold)
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
		#print(correntes,correntes,correntes)
		dlg.comboBox_50.setEnabled(False) #fechar combobox de subhot stream
		dlg.comboBox_51.setEnabled(False) #fechar combobox de subcold stream
		dlg.comboBox_53.setEnabled(False) #fechar combobox de subhot stream
		dlg.comboBox_54.setEnabled(False) #fechar combobox de subcold stream

		return alreadypinched,plotou

def grandcomposite () :
	dlg.canvas2.hide()
	dlg.canvas3.show()

def THD () :
	dlg.canvas3.hide()
	dlg.canvas2.show()

def ligarspins():
	if dlg.comboBox_5.currentIndex() != 0:
		dlg.doubleSpinBox.setEnabled(True)
	else:
		dlg.doubleSpinBox.setEnabled(False)
	if dlg.comboBox_50.currentIndex() != 0:
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

def correntesnoscombos(nhot,ncold): #preenche as caixinhas

	nstages=2
	nsubstages=2

	for i in range (nhot):
		dlg.comboBox_2.addItem(str(i+1))     #acima   add heat ex
		dlg.comboBox_9.addItem(str(i+1))     #acima   quadro de correntes quentes
		dlg.comboBox_35.addItem(str(i+1))   #abaixo   add heat ex
		dlg.comboBox_43.addItem(str(i+1))    #abaixo   quadro de correntes quentes
		dlg.TempLoad.comboBox.addItem(str(i+1))
	for i in range (ncold):
		dlg.comboBox_5.addItem(str(i+1))      #acima add heat ex
		dlg.comboBox_10.addItem(str(i+1))     #acima quadro correntes frias
		dlg.comboBox_36.addItem(str(i+1))     #abaixo add heat ex
		dlg.comboBox_44.addItem(str(i+1))     #abaixo quadro de correntes frias
		dlg.TempLoad.comboBox_2.addItem(str(i+1))
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
	#print("correntestrocador",correntestrocador)

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

def checaresgotadosabaixo():
	contadordutyhot=0
	contadordutycold=0
	for i in range (nhot):
		if dlg.tableWidget_15.item(i,3).text() == "0.0":
			contadordutyhot=contadordutyhot+1
	if contadordutyhot == nhot:
		dlg.comboBox_44.setEnabled(True)
		dlg.pushButton_21.setEnabled(True)
	for i in range (ncold):
		if dlg.tableWidget_17.item(i,3).text() == "0.0":
			contadordutycold=contadordutycold+1
	if contadordutycold == ncold:                          ## aqui tava contadordutyhot == nhot
		dlg.comboBox_43.setEnabled(True)
		dlg.pushButton_20.setEnabled(True)
	if contadordutyhot == nhot and contadordutycold == ncold:        #mexer aqui, pra liberar os combobox de utilidade no acima
		dlg.comboBox_43.setEnabled(False)
		dlg.comboBox_44.setEnabled(False)
		dlg.pushButton_20.setEnabled(False)
		dlg.pushButton_21.setEnabled(False)

def coldsplit1():
	global nhot,ncold, nstages
	dlg.divisaotrocador=uic.loadUi("divisaocold1.ui")
	dlg.divisaotrocador.show()

	nstages=2
	nsubstages=2

	for i in range (ncold):
		dlg.divisaotrocador.comboBox.addItem(str(i+1))
	for i in range (nhot):                                   #split - o numero máximo de divisões é igual ao numero de correntes quentes
		dlg.divisaotrocador.comboBox_2.addItem(str(i+1))
	for i in range (nstages):
		dlg.divisaotrocador.comboBox_3.addItem(str(i+1))

	def coldsplit2(nsplit):
		global somatorio
		dlg.divisaotrocador2=uic.loadUi("divisaocold2.ui")
		dlg.divisaotrocador2.show()

		coldsplitspinbox=[0]*nsplit #variáveis
		coldsplitlabel=[0]*nsplit

		for i in range(nsplit): # criar variável
			coldsplitspinbox[i]=QtWidgets.QDoubleSpinBox(dlg)
			coldsplitlabel[i]=QtWidgets.QLabel(dlg)
			dlg.divisaotrocador2.verticalLayout_2.addWidget(coldsplitspinbox[i])
			coldsplitspinbox[i].setSingleStep(float(0.1))
			coldsplitspinbox[i].setMaximum(1)
			coldsplitlabel[i].setText("Substream {}".format(i+1))
			myFont=QtGui.QFont()
			myFont.setBold(True)
			coldsplitlabel[i].setFont(myFont)
			dlg.divisaotrocador2.verticalLayout.addWidget(coldsplitlabel[i])
			somatorio=float(coldsplitspinbox[i].value())+somatorio

		def dadosusercoldsplit():
			global somatorio2, estagio, ccold, qsj, fracao_fria
			estagio = int(float(dlg.divisaotrocador.comboBox_3.currentText())) #estagios
			ccold = int(float(dlg.divisaotrocador.comboBox.currentText())) # numero de correntes
			qsj = int(float(dlg.divisaotrocador.comboBox_2.currentText())) # numero subcorrentes


			for i in range (qsj):
				dlg.comboBox_51.addItem(str(i+1))    #Adiciona em sub cold stream, mas tem que estar na matriz! Arrumar isso dps

			fracao_fria=[0]*nsplit
			for i in range(nsplit):
				fracao_fria[i] = float(coldsplitspinbox[i].value())
				somatorio2=float(coldsplitspinbox[i].value())+somatorio2

			#print(estagio, "\n")
			#print(ccold, "\n")
			#print(qsj, "\n")
			#print(coldsplitspinbox)
			#print(fracao_fria)

		dlg.divisaotrocador2.pushButton.clicked.connect(lambda: dadosusercoldsplit())


		def somatoriocoldsplit():
			global somatorio2, estagio, ccold, qsj, fracao_fria
			if somatorio2 != 1.0:
				msg = QMessageBox()
				msg.setText("The fractions are exceeding the limit")
				#	msg.setInformativeText('More information')   e aqui?
				msg.setWindowTitle("Error")
				msg.exec_()

			else:
				dlg.divisaotrocador2.close()
				dlg.divisaotrocador.close()
				Fcarr,ncoldc=acima(correntes,pinchq,pinchf,n,nhot,ncold,dlg,dTmin,estagio,ccold,qsj,fracao_fria)
				#print("teste fcarr e ncoldc", Fcarr,ncoldc)

			somatorio2=0

		dlg.divisaotrocador2.pushButton.clicked.connect(lambda: somatoriocoldsplit())

	dlg.divisaotrocador.pushButton.clicked.connect(lambda: coldsplit2(int(dlg.divisaotrocador.comboBox_2.currentText())))

def hotsplit1():
	global nhot,ncold,nstages
	dlg.divisaotrocador3=uic.loadUi("divisaohot1.ui")
	dlg.divisaotrocador3.show()

	nstages=2
	nsubstages=2

	for i in range (ncold):
		dlg.divisaotrocador3.comboBox.addItem(str(i+1))
	for i in range (nhot):                                   #split - o numero máximo de divisões é igual ao numero de correntes quentes
		dlg.divisaotrocador3.comboBox_2.addItem(str(i+1))
	for i in range (nstages):
		dlg.divisaotrocador3.comboBox_3.addItem(str(i+1))

	def hotsplit2(nsplit):
		dlg.divisaotrocador4=uic.loadUi("divisaohot2.ui")
		dlg.divisaotrocador4.show()

		hotsplitspinbox=[0]*nsplit #variável qualquer só pra fazer a função funcionar
		hotsplitlabel=[0]*nsplit

		for i in range(nsplit):
			hotsplitspinbox[i]=QtWidgets.QDoubleSpinBox(dlg)
			hotsplitlabel[i]=QtWidgets.QLabel(dlg)
			dlg.divisaotrocador4.verticalLayout_2.addWidget(hotsplitspinbox[i])
			hotsplitspinbox[i].setSingleStep(float(0.1))
			hotsplitspinbox[i].setMaximum(1)
			hotsplitlabel[i].setText("Substream {}".format(i+1))
			myFont=QtGui.QFont()
			myFont.setBold(True)
			hotsplitlabel[i].setFont(myFont)
			dlg.divisaotrocador4.verticalLayout.addWidget(hotsplitlabel[i])

		def dadosuserhotsplit():
			global somatorio, estagio, chot, qsi, fracao_quente
			estagio = int(float(dlg.divisaotrocador3.comboBox_3.currentText())) #corrente dividida nesse estágio
			chot = int(float(dlg.divisaotrocador3.comboBox.currentText())) #numero da corrente dividida
			qsi = int(float(dlg.divisaotrocador3.comboBox_2.currentText())) #em quantas correntes foi dividida

			for i in range (qsi):
				dlg.comboBox_50.addItem(str(i+1))

			fracao_quente=[0]*nsplit
			for i in range(nsplit):
				fracao_quente[i] = float(hotsplitspinbox[i].value())
				somatorio=float(hotsplitspinbox[i].value())+somatorio

			#print("opa ", estagio, "\n")
			#print(chot, "\n")
			#print(qsi, "\n")
			#print(hotsplitspinbox)
			#print(fracao_quente[1])

		dlg.divisaotrocador4.pushButton.clicked.connect(lambda: dadosuserhotsplit())

		def somatoriohotsplit():
			global somatorio, estagio, chot, qsi, fracao_quente
			if somatorio != 1.0:
				msg = QMessageBox()
				msg.setText("Make sure the fractions somatory are 1.0")
				#	msg.setInformativeText('More information')   e aqui?
				msg.setWindowTitle("Error!")
				msg.exec_()

			else:
				dlg.divisaotrocador4.close()
				dlg.divisaotrocador3.close()
				Fharr,nhotc=acimaaddtrocador(correntes,pinchq,pinchf,n,nhot,ncold,dlg,dTmin,estagio,chot,qsi,fracao_quente,qsj,fracao_fria,ccold)
				#print("teste fharr e nhotc", Fharr,nhotc)

			somatorio=0



		dlg.divisaotrocador4.pushButton.clicked.connect(lambda: somatoriohotsplit())

	dlg.divisaotrocador3.pushButton.clicked.connect(lambda: hotsplit2(int(dlg.divisaotrocador3.comboBox_2.currentText())))




def printar():
	dlg.tableWidget_3.setRowCount(nhot)
	dlg.tableWidget_4.setRowCount(ncold)
	for corrente in range(nhot):
		dlg.tableWidget_3.setItem(corrente, 0, QTableWidgetItem(str(float('{:.1f}'.format(pinchq)))))
		dlg.tableWidget_3.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente[corrente])))))
		dlg.tableWidget_3.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(Th0[corrente])))))
		dlg.tableWidget_3.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente[corrente])))))
	for corrente in range(ncold):
		dlg.tableWidget_4.setItem(corrente, 0, QTableWidgetItem(str(float('{:.1f}'.format(pinchf)))))
		dlg.tableWidget_4.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria[corrente])))))
		dlg.tableWidget_4.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(Tcf[corrente])))))
		dlg.tableWidget_4.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio[corrente])))))

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
	nova_matriz = inserir_trocador(dlg, dados_do_trocador)
	try:
		matriz_armazenada.append(nova_matriz[-1])
	except:
		pass
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
							pass
		dlg.comboBox_10.setEnabled(False)
		dlg.pushButton_8.setEnabled(False)
		trocador_remover = matriz_armazenada[indice_remover]
		calor_atual_quente[trocador_remover[0]-1] += trocador_remover[6]
		calor_atual_frio[trocador_remover[1]-1] += trocador_remover[6]
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
		pass
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

def inserir_teste_abaixo():
	dados_do_trocador = ler_dados_abaixo(dlg)
	nova_matriz = inserir_trocador_abaixo(dlg, dados_do_trocador)
	try:
		matriz_trocadores_abaixo.append(nova_matriz[-1])
	except:
		pass
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
							pass
		dlg.comboBox_43.setEnabled(False)
		dlg.pushButton_20.setEnabled(False)
		trocador_remover = matriz_trocadores_abaixo[indice_remover]
		calor_atual_quente_abaixo[trocador_remover[0]-1] += trocador_remover[6]
		calor_atual_frio_abaixo[trocador_remover[1]-1] += trocador_remover[6]
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
		pass
	printar_abaixo()

def printar_abaixo():
	dlg.tableWidget_15.setRowCount(nhot)
	dlg.tableWidget_17.setRowCount(ncold)
	for corrente in range(nhot):
		dlg.tableWidget_15.setItem(corrente, 0, QTableWidgetItem(str(float('{:.1f}'.format(pinchq)))))
		dlg.tableWidget_15.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_abaixo[corrente])))))
		dlg.tableWidget_15.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(Thf[corrente])))))
		dlg.tableWidget_15.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente_abaixo[corrente])))))
	for corrente in range(ncold):
		dlg.tableWidget_17.setItem(corrente, 0, QTableWidgetItem(str(float('{:.1f}'.format(pinchf)))))
		dlg.tableWidget_17.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_abaixo[corrente])))))
		dlg.tableWidget_17.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(Tc0[corrente])))))
		dlg.tableWidget_17.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio_abaixo[corrente])))))

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



#streams
dlg.pinchbutton.setEnabled(False) #block o botao pinch até apertar done
dlg.tabWidget.setTabEnabled(1,False) #block stream diagram até fazer o pinch
dlg.tabWidget.setTabEnabled(2,False) #block composite curver até fazer o pinch
dlg.tabWidget.setTabEnabled(3,False) #block heat exchangers até fazer o pinch
dlg.tabWidget.setTabEnabled(4,False) #block heat exchangers network até fazer o pinch
dlg.pushButton.clicked.connect(apertaradd) #add stream
dlg.donebutton.clicked.connect(apertardone) #done
dlg.pinchbutton.clicked.connect(apertarpinchbutton) #pinch
#criar actionopen pra abrir um excel?
dlg.actionOpen_2.triggered.connect(openfile) #file > open
dlg.tableWidget.itemChanged.connect(itemedited) #le excel?
#mudança de sistema de unidades
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
dlg.pushButton_9.clicked.connect(hotsplit1)
dlg.pushButton_13.clicked.connect(coldsplit1)
dlg.comboBox_9.setEnabled(False) #corrente quente que vai utilizade
dlg.comboBox_10.setEnabled(False) #corrente fria que vai utilidade
dlg.pushButton_7.setEnabled(False) #add utility hot
dlg.pushButton_8.setEnabled(False) #add utility cold
dlg.pushButton_6.clicked.connect(inserir_teste)
dlg.pushButton_10.clicked.connect(remover_teste)
dlg.pushButton_14.clicked.connect(calcular_calor_teste)
dlg.pushButton_8.clicked.connect(utilidade_teste_acima)


#below
dlg.radioButton_17.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(True)) #quando marca o heat load libera a linha pra digitar
dlg.radioButton_20.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(False)) #block o heat load quando max heat ta ativado
dlg.radioButton_20.setChecked(True) #por padrao abre o prog com max heat selecionado
dlg.pushButton_12.clicked.connect(coldsplit1)
dlg.pushButton_11.clicked.connect(hotsplit1)
dlg.comboBox_43.setEnabled(False) #corrente quente que vai utilizade
dlg.comboBox_44.setEnabled(False) #corrente fria que vai utilidade
dlg.pushButton_20.setEnabled(False) #add utility hot
dlg.pushButton_21.setEnabled(False) #add utility cold
dlg.pushButton_18.clicked.connect(inserir_teste_abaixo)
dlg.pushButton_15.clicked.connect(remover_teste_abaixo)
dlg.pushButton_20.clicked.connect(utilidade_teste_abaixo)
dlg.pushButton_17.clicked.connect(calcular_calor_abaixo)


header = dlg.tableWidget.horizontalHeader()
header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)




dlg.show()
dlg.showMaximized()
app.exec()

x = input("oi")
