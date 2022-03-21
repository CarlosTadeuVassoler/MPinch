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
import tkinter
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
from svg_turtle import SvgTurtle
import os
from custo2 import varia



app=QtWidgets.QApplication([])
dlg=uic.loadUi("MPinch.ui")


matriz = []
matriz_armazenada = []
matriz_trocadores_abaixo = []
utilidades = []
utilidades_abaixo = []
dTmin = 10
donee=0
done = False
cascat=[]
nstages=1
subestagio_trocador = 0
subestagio_trocador_abaixo = 0
unidadeusada=["Temperature (K)","Enthalpy (kJ)","Enthalpy (kJ)"]
alreadypinched=0
plotou=0
corrente_quente_presente_acima = []
corrente_fria_presente_acima = []
corrente_quente_presente_abaixo = []
corrente_fria_presente_abaixo = []
correntes_quentes = []
correntes_frias = []
n = nhot = ncold = n_util = 0
correntes = []
e_utilidade = []
e_utilidade_quente = []
e_utilidade_fria = []
correntes_util = []



#######################
def formatando(valor,index):
	if valor>=1_000_000:
		fomatador = '{:1.1f}M'.format(valor*0.000_001)
	else:
		fomatador = '{:1.0f}K'.format(valor * 0.001)

	return fomatador

def otimizafun():
	start=float(dlg.dtstart.text())
	step=float(dlg.dtstep.text())
	stop=float(dlg.dtstop.text())

	dlg.sc = QtWidgets.QLabel(dlg)

	global variadt, yplot, custoopano, custocapital, custocapitalanual, custototanual,uf,uq
	uf,uq,variadt, yplot, custoopano, custocapital, custocapitalanual, custototanual=varia(start,step,stop,correntes)


	row = 0
	valorbonito = []
	valorbonito = np.round(variadt, 3)
	dlg.TABELA.setRowCount(len(valorbonito))

	for data in range(0, len(valorbonito)):
		dlg.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(np.round(variadt[data], 3))))
		dlg.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(np.round(yplot[data], 2))))
		dlg.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(np.round(custoopano[data], 2))))
		dlg.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(np.round(custocapitalanual[data], 2))))
		dlg.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(np.round(custototanual[data], 2))))
		row += 1

	# print(variadt)
	dlg.sc = myCanvas()
	print(dlg.sc)
	dlg.l = QVBoxLayout(dlg.dtminxcusto)

	dlg.l.addWidget(dlg.sc)
	y=[0]
	x=[0]
	dlg.sc.plot(x, y)


	dlg.sc2 = myCanvas2()
	dlg.l = QVBoxLayout(dlg.dtminxarea)
	dlg.l.addWidget(dlg.sc2)
	dlg.sc2.plot(x, y)


	dlg.sc3 = myCanvas3()
	dlg.l = QVBoxLayout(dlg.dtminxut)
	dlg.l.addWidget(dlg.sc3)
	dlg.sc3.plot(x, y)

class myCanvas(FigureCanvas):
	def __init__(self):
		self.fig=Figure()
		FigureCanvas.__init__(self,self.fig)

	def plot(self,x,y):
		self.fig.clear()

		plt.style.use('ggplot')
		self.ax= self.fig.add_subplot(111)
		self.ax.clear()
		self.ax.yaxis.set_major_formatter(formatando)
		self.ax.plot(variadt,custoopano, label='C.Operacional x ΔTmin')
		self.ax.plot(variadt,custocapitalanual, label='C.Capital x ΔTmin', color='k')
		self.ax.plot(variadt,custototanual, label='C.Total x ΔTmin', color='r')
		self.ax.set_xlabel('ΔTmin')
		self.ax.set_ylabel('Cost')
		self.ax.legend()
		self.ax.grid(True)
		self.draw()

class myCanvas2(FigureCanvas):
	def __init__(self):
		self.fig=Figure()
		FigureCanvas.__init__(self,self.fig)

	def plot(self,x,y):
		self.fig.clear()

		plt.style.use('ggplot')
		self.ax= self.fig.add_subplot(111)
		self.ax.yaxis.set_major_formatter(formatando)

		# print(variadt)
		self.ax.plot(variadt,yplot, label='Area x ΔTmin', color='r')
		self.ax.set_xlabel('ΔTmin')
		self.ax.set_ylabel('Area')
		self.ax.legend()
		self.ax.grid(True)
		self.draw()

class myCanvas3(FigureCanvas):
	def __init__(self):
		self.fig=Figure()
		FigureCanvas.__init__(self,self.fig)

	def plot(self,x,y):
		self.fig.clear()

		plt.style.use('ggplot')
		self.ax= self.fig.add_subplot(111)
		#self.ax.yaxis.set_major_formatter(formatando)
		self.ax.plot(variadt,uq, label='Hot utility x ΔTmin', color='r')
		self.ax.plot(variadt, uf, label='Cold utility x ΔTmin', color='b')
		self.ax.set_xlabel('ΔTmin')
		self.ax.set_ylabel('Utility')
		self.ax.legend()
		self.ax.grid(True)
		self.draw()
########################





#inputs e coisas com eles
def openfile_teste():
	global n, nhot, ncold, correntes

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
		dados_da_corrente.append(0.5)
		correntes.append(dados_da_corrente)
		e_utilidade.append(False)

	#printa as correntes pro usuário na tabela de streams
	for corrente in range(len(correntes)):
		for coluna in range(5):
			dlg.tableWidget.setItem(corrente, coluna, QTableWidgetItem(str(correntes[corrente][coluna])))


	dlg.tableWidget.blockSignals(False)
	for i in range(n):
		for j in range(5):
			item = dlg.tableWidget.item(i, j)
			item.setTextAlignment(Qt.AlignHCenter)

def apertaradd() :
	global n, ncold, nhot, correntes
	n += 1
	dados_da_corrente = []
	if n == 1:
		dlg.sistema_unidades.setEnabled(False)
		dlg.temp_unidade.setEnabled(False)
		dlg.cp_unidade.setEnabled(False)
		dlg.pelicula_unidade.setEnabled(False)
		dlg.temp_unidade_util.setEnabled(False)
		dlg.pelicula_unidade_util.setEnabled(False)

	if float(dlg.stream_supply.text().replace(",", ".")) < float(dlg.stream_target.text().replace(",", ".")):
		tipo = "Cold"
		ncold += 1
	else:
		tipo = "Hot"
		nhot += 1

	dados_da_corrente.append(float(dlg.stream_supply.text().replace(",",".")))
	dados_da_corrente.append(float(dlg.stream_target.text().replace(",", ".")))
	dados_da_corrente.append(float(dlg.stream_cp.text().replace(",", ".")))
	dados_da_corrente.append(tipo)
	dados_da_corrente.append(float(dlg.stream_pelicula.text().replace(",", ".")))

	dlg.tableWidget.blockSignals(True)
	dlg.tableWidget.setRowCount(n)
	dlg.tableWidget.setItem(n-1, 0, QTableWidgetItem(str(dados_da_corrente[0])))
	dlg.tableWidget.setItem(n-1, 1, QTableWidgetItem(str(dados_da_corrente[1])))
	dlg.tableWidget.setItem(n-1, 2, QTableWidgetItem(str(dados_da_corrente[2])))
	dlg.tableWidget.setItem(n-1, 3, QTableWidgetItem(dados_da_corrente[3]))
	dlg.tableWidget.setItem(n-1, 4, QTableWidgetItem(str(dados_da_corrente[4])))

	for i in range(5):
		item = dlg.tableWidget.item(n-1, i)
		item.setTextAlignment(Qt.AlignHCenter)

	correntes.append(dados_da_corrente)
	e_utilidade.append(False)

	dlg.tableWidget.blockSignals(False)

def add_utilidade():
	global n, n_util, ncold, nhot, correntes_util
	dlg.donebutton.setEnabled(False)
	dlg.botao_addstream.setEnabled(False)
	# n += 1
	n_util += 1
	dados_da_corrente = []

	if float(dlg.util_inlet.text().replace(",", ".")) < float(dlg.util_outlet.text().replace(",", ".")):
		tipo = "Cold"
	else:
		tipo = "Hot"

	dados_da_corrente.append(float(dlg.util_inlet.text().replace(",", ".")))
	dados_da_corrente.append(float(dlg.util_outlet.text().replace(",", ".")))
	dados_da_corrente.append(1)
	dados_da_corrente.append(tipo)
	dados_da_corrente.append(float(dlg.util_pelicula.text().replace(",", ".")))


	dlg.tableWidget_5.blockSignals(True)
	dlg.tableWidget_5.setRowCount(n_util)
	dlg.tableWidget_5.setItem(n_util-1, 0, QTableWidgetItem(dlg.utilidade.currentText()))
	dlg.tableWidget_5.setItem(n_util-1, 1, QTableWidgetItem(str(dados_da_corrente[0])))
	dlg.tableWidget_5.setItem(n_util-1, 2, QTableWidgetItem(str(dados_da_corrente[1])))
	dlg.tableWidget_5.setItem(n_util-1, 3, QTableWidgetItem(dados_da_corrente[3]))
	dlg.tableWidget_5.setItem(n_util-1, 4, QTableWidgetItem(str(dados_da_corrente[4])))

	for i in range(5):
		item = dlg.tableWidget_5.item(n_util-1, i)
		item.setTextAlignment(Qt.AlignHCenter)

	correntes_util.append(dados_da_corrente)
	e_utilidade.append(True)

	dlg.tableWidget_5.blockSignals(False)

def done_teste():
	global dTmin, done, correntes
	lista_cps = []

	for corrente in correntes:
		lista_cps.append(corrente[2])

	novos_cps = unidades_compativeis(dlg.temp_unidade.currentIndex(), dlg.cp_unidade.currentIndex(), dlg.pelicula_unidade.currentIndex(), lista_cps)

	for i in range(len(correntes)):
		correntes[i][2] = round(novos_cps[i], 3)

	dTmin=float(dlg.lineEdit_2.text().replace(",", "."))
	pinchf, pinchq, util_quente, util_fria, coisas_graficos = pontopinch(correntes, len(correntes), dTmin)
	dlg.done = uic.loadUi("done.ui")
	dlg.done.show()
	dlg.done.hot_temp.setText("Hot: " + str(pinchq) + " " + dlg.temp_unidade.currentText())
	dlg.done.cold_temp.setText("Cold: " + str(pinchf) + " " + dlg.temp_unidade.currentText())
	dlg.done.precisa_quente.setText("Hot Utility Demand: " + str(util_quente) + " " + "kW")
	dlg.done.precisa_fria.setText("Cold Utility Demand: " + str(util_fria) + " " + "kW")
	done = True
	grafico = QPixmap("diagrama_th.png")
	x = QtWidgets.QLabel(dlg)
	x.setPixmap(grafico)
	x.setAlignment(QtCore.Qt.AlignCenter)
	x.setScaledContents(True)
	dlg.done.diagrama_th.addWidget(x)
	grafico = QPixmap("grande_composta.png")
	x = QtWidgets.QLabel(dlg)
	x.setPixmap(grafico)
	x.setAlignment(QtCore.Qt.AlignCenter)
	x.setScaledContents(True)
	dlg.done.grande_composta.addWidget(x)

	def cancelar():
		global done
		done = False
		dlg.done.close()

	def liberar_utilidades():
		dlg.pinchbutton.setEnabled(True)
		dlg.botao_addutility.setEnabled(True)
		dlg.util_inlet.setEnabled(True)
		dlg.util_outlet.setEnabled(True)
		dlg.util_pelicula.setEnabled(True)
		dlg.donebutton.setEnabled(False)
		dlg.botao_addstream.setEnabled(False)
		dlg.done.close()

	def pinch_sem_util():
		pinch_teste()
		dlg.done.close()

	dlg.done.cancelar.clicked.connect(cancelar)
	dlg.done.escolher_utilidades.clicked.connect(liberar_utilidades)
	dlg.done.pinch_sem_utilidades.clicked.connect(pinch_sem_util)




	# Tdecre = coisas_graficos[0]
	# Tmin = coisas_graficos[1]
	# Tmax = coisas_graficos[2]
	# cascat2certo = coisas_graficos[3]
	# dT = coisas_graficos[4]
	# cascat2 = coisas_graficos[5]
	# utilidadesquente = coisas_graficos[6]
	# menor = coisas_graficos[7]
	# pinch = coisas_graficos[8]
	# plotargrafico1(correntes, n, caixinha,dlg,Tmin,Tmax,dTmin,dT,Tdecre,pinch,unidadeusada,plotou)
	# diagrama_th = plotargrafico2(correntes, len(correntes), dlg,Tmin,Tmax,dTmin,dT,Tdecre,pinch,cascat2certo,cascat,utilidadesquente,pinchf,pinchq,unidadeusada)
	# plotargrafico3(correntes, n, caixinha4,dlg,Tmin,Tmax,dTmin,dT,Tdecre,pinch, cascat2certo,cascat,utilidadesquente,pinchf,pinchq,menor,cascat2,unidadeusada)
	# dlg.done.grande_composta.addWidget(diagrama_th)
	# dlg.caixinha3.addWidget(diagrama_th)

def pinch_teste():
	global done, Th0, Thf, CPh, Tc0, Tcf, CPc, Thf_acima, Th0_abaixo, Tc0_acima, Tcf_abaixo
	Th0, Thf, CPh, Tc0, Tcf, CPc, Thf_acima, Th0_abaixo, Tc0_acima, Tcf_abaixo = [], [], [], [], [], [], [], [], [], []
	if done:
		global correntes, correntes_util, dTmin, pinchf, pinchq, n, util_quente, util_fria, nhot, ncold
		pinchf, pinchq, util_quente, util_fria, a = pontopinch(correntes, n, dTmin)
		for util in correntes_util:
			if util[3] == "Hot":
				util[2] = util_quente/(util[0] - util[1])
				nhot += 1
			else:
				util[2] = util_fria/(util[1] - util[0])
				ncold += 1

		correntes += correntes_util
		n += len(correntes_util)
		#arruma as temperaturas baseado no pinch
		for i in range (n): #correção das temperaturas
			if correntes[i][3] == "Hot":
				correntes_quentes.append(1)
				if e_utilidade[i]:
					e_utilidade_quente.append(True)
				else:
					e_utilidade_quente.append(False)
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
				if e_utilidade[i]:
					e_utilidade_fria.append(True)
				else:
					e_utilidade_fria.append(False)
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
		testar_correntes(dlg, True)
		testar_correntes_abaixo(dlg)

		#libera botões e coisas
		dlg.tabWidget.setTabEnabled(1,True)
		dlg.tabWidget.setTabEnabled(2,True)
		dlg.tabWidget.setTabEnabled(3,True)
		dlg.tabWidget.setTabEnabled(4,True)
		dlg.tabWidget.setCurrentIndex(3)
		dlg.pinchbutton.setEnabled(False)
		dlg.botao_addstream.setEnabled(False)
		dlg.botao_addutility.setEnabled(False)
		dlg.donebutton.setEnabled(False)

def correntesnoscombos(nhot,ncold):
	nstages=1
	nsubstages=20
	for i in range (nhot):
		dlg.comboBox_2.addItem(str(i+1)) #acima   add heat ex
		dlg.comboBox_9.addItem(str(i+1)) #acima   quadro de correntes quentes
		dlg.comboBox_35.addItem(str(i+1))   #abaixo   add heat ex
		dlg.comboBox_43.addItem(str(i+1))#abaixo   quadro de correntes quentes
		dlg.comboBox_51.addItem(str(i+1))	#n max de sub frias é o número de correntes quentes
		dlg.comboBox_54.addItem(str(i+1))
	for i in range (ncold):
		dlg.comboBox_5.addItem(str(i+1))  #acima add heat ex
		dlg.comboBox_10.addItem(str(i+1)) #acima quadro correntes frias
		dlg.comboBox_36.addItem(str(i+1)) #abaixo add heat ex
		dlg.comboBox_44.addItem(str(i+1)) #abaixo quadro de correntes frias
		dlg.comboBox_50.addItem(str(i+1))	#n max de sub quentes é o nomero de correntes frias
		dlg.comboBox_53.addItem(str(i+1))

def unidades(header=True):
	if not header:
		if dlg.sistema_unidades.currentIndex() != 2:
			dlg.temp_unidade.setCurrentIndex(dlg.sistema_unidades.currentIndex())
			dlg.cp_unidade.setCurrentIndex(dlg.sistema_unidades.currentIndex())
			dlg.pelicula_unidade.setCurrentIndex(dlg.sistema_unidades.currentIndex())
			dlg.temp_unidade_util.setCurrentIndex(dlg.sistema_unidades.currentIndex())
			dlg.pelicula_unidade_util.setCurrentIndex(dlg.sistema_unidades.currentIndex())
			dlg.temp_unidade.setEnabled(False)
			dlg.cp_unidade.setEnabled(False)
			dlg.pelicula_unidade.setEnabled(False)
			dlg.temp_unidade_util.setEnabled(False)
			dlg.pelicula_unidade_util.setEnabled(False)
		else:
			dlg.temp_unidade.setEnabled(True)
			dlg.cp_unidade.setEnabled(True)
			dlg.pelicula_unidade.setEnabled(True)
			dlg.temp_unidade_util.setEnabled(True)
			dlg.pelicula_unidade_util.setEnabled(True)

	headerrr = ["Supply Temperature ({})".format(dlg.temp_unidade.currentText()),
				"Target Temperature ({})".format(dlg.temp_unidade.currentText()),
				"CP ({})".format(dlg.cp_unidade.currentText()),
				"Stream Type",
				"h ({})".format(dlg.pelicula_unidade.currentText())]
	dlg.tableWidget.setHorizontalHeaderLabels(headerrr)
	headerrr = ["Utility",
				"Inlet Temperature ({})".format(dlg.temp_unidade_util.currentText()),
				"Outlet Temperature ({})".format(dlg.temp_unidade_util.currentText()),
				"Utility Type",
				"h ({})".format(dlg.pelicula_unidade_util.currentText())]
	dlg.tableWidget_5.setHorizontalHeaderLabels(headerrr)

def unidades_compativeis(unidade_temp, unidade_cp, unidade_pelicula, cp_printar):
	#0:si
	#1:eng
	#2:si
	#3:eng
	cp_contas = []

	if (unidade_temp == 0 or unidade_temp == 2) and (unidade_cp != 0 or unidade_pelicula != 0):
		if unidade_cp != 0:
			print("cp incompativel")
			for cp in cp_printar:
				cp_contas.append(cp * 0.00052753)
		if unidade_pelicula != 0:
			#converter aqui a unidade pelicula para 0
			print("pelicula incompativel")
	elif (unidade_temp == 1 or unidade_temp == 3) and (unidade_cp != 1 or unidade_pelicula != 1):
		if unidade_cp != 1:
			print("cp incompativel 1")
			for cp in cp_printar:
				cp_contas.append(cp / 0.00052753)
		if unidade_pelicula != 1:
			#converter aqui pelicula pra 1
			print("pelicula incompativel 1")
	else:
		cp_contas = cp_printar

	return cp_contas



#parte de desenhos
def desenhar_rede(correntes_quentes, correntes_frias, teste=False):
	global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo
	turtle.delay(0)
	turtle.setup(width=1.0, height=1.0)
	temp = turtle.Turtle()
	temp.speed(1000)
	temp.shapesize(0.001, 0.001, 0.001)
	temp.penup()
	temperatura = turtle.Turtle()
	temperatura.speed(1000)
	temperatura.shapesize(0.001, 0.001, 0.001)
	temperatura.penup()
	ident = turtle.Turtle()
	ident.speed(1000)
	ident.shapesize(0.001, 0.001, 0.001)
	ident.penup()
	y_acima, y_abaixo = 200, 200

	def quentes(onde, correntes_desenho, presente):
		global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo
		distancia_x = 500
		for i in range(len(correntes_desenho)):
			if presente[i]:
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].speed(1000)
				if e_utilidade_quente[i]:
					correntes_desenho[i].color("orange")
				else:
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
						temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]))), align="left", font=("Arial", 10, "normal"))
					else:
						correntes_desenho_sub_acima[i] = [0] * (quantidade_quente[i] - 1)
						for j in range(quantidade_quente[i]-1):
							temp.sety(y_acima - 8)
							temp.setx(-distancia_x - 138)
							temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]*fracoes_quentes[i][j]))), align="left", font=("Arial", 10, "normal"))
							correntes_desenho_sub_acima[i][j] = turtle.Turtle()
							if e_utilidade_quente[i]:
								correntes_desenho_sub_acima[i][j].color("orange")
							else:
								correntes_desenho_sub_acima[i][j].color("red")
							correntes_desenho_sub_acima[i][j].pensize(3)
							correntes_desenho_sub_acima[i][j].shapesize(0.001, 0.001, 0.001)
							correntes_desenho_sub_acima[i][j].penup()
							correntes_desenho_sub_acima[i][j].setx(-distancia_x + 20)
							correntes_desenho_sub_acima[i][j].sety(y_acima)
							correntes_desenho_sub_acima[i][j].pendown()
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(40)
							correntes_desenho_sub_acima[i][j].left(90)
							if Thf_acima[i] == pinchq:
								correntes_desenho_sub_acima[i][j].forward(distancia_x - 44)
							else:
								correntes_desenho_sub_acima[i][j].forward(distancia_x - 140)
							correntes_desenho_sub_acima[i][j].left(90)
							correntes_desenho_sub_acima[i][j].forward(40*(j+1))
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(20)
							y_acima -= 40
						temp.sety(y_acima - 8)
						temp.setx(-distancia_x - 138)
						temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]*fracoes_quentes[i][quantidade_quente[i]-1]))), align="left", font=("Arial", 10, "normal"))
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
						temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]))), align="left", font=("Arial", 10, "normal"))
					else:
						correntes_desenho_sub_abaixo[i] = [0] * (quantidade_quente_abaixo[i] - 1)
						for j in range(quantidade_quente_abaixo[i]-1):
							temp.sety(y_abaixo - 8)
							temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]*fracoes_quentes_abaixo[i][j]))), align="left", font=("Arial", 10, "normal"))
							correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
							correntes_desenho_sub_abaixo[i][j].color("red")
							correntes_desenho_sub_abaixo[i][j].pensize(3)
							correntes_desenho_sub_abaixo[i][j].shapesize(0.001, 0.001, 0.001)
							correntes_desenho_sub_abaixo[i][j].penup()
							correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
							if Th0_abaixo[i] == pinchq:
								correntes_desenho_sub_abaixo[i][j].setx(24)
								correntes_desenho_sub_abaixo[i][j].pendown()
								correntes_desenho_sub_abaixo[i][j].right(90)
								correntes_desenho_sub_abaixo[i][j].forward(40)
								correntes_desenho_sub_abaixo[i][j].left(90)
								if fechar_corrente_abaixo[i]:
									correntes_desenho_sub_abaixo[i][j].forward((len(matriz_trocadores_abaixo)+1)*55)
									temperatura.sety(y_abaixo + 1)
									temperatura.setx((len(matriz_trocadores_abaixo)+1)*55 + len(str(round(temp_misturador_abaixo[i], 1)))*3.5)
									temperatura.write(str(round(temp_misturador_abaixo[i], 1)), align="left", font=("Arial", 8, "normal"))
								else:
									correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 44)
							else:
								correntes_desenho_sub_abaixo[i][j].setx(120)
								correntes_desenho_sub_abaixo[i][j].pendown()
								correntes_desenho_sub_abaixo[i][j].right(90)
								correntes_desenho_sub_abaixo[i][j].forward(40)
								correntes_desenho_sub_abaixo[i][j].left(90)
								if fechar_corrente_abaixo[i]:
									correntes_desenho_sub_abaixo[i][j].forward((len(matriz_trocadores_abaixo)+1)*55)
									temperatura.sety(y_abaixo + 1)
									temperatura.setx((len(matriz_trocadores_abaixo)+1)*55 + len(str(round(temp_misturador_abaixo[i], 1)))*3.5)
									temperatura.write(str(round(temp_misturador_abaixo[i], 1)), align="left", font=("Arial", 8, "normal"))
								else:
									correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 140)
							correntes_desenho_sub_abaixo[i][j].left(90)
							correntes_desenho_sub_abaixo[i][j].forward(40*(j+1))
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(20)
							y_abaixo -= 40
						temp.sety(y_abaixo - 8)
						temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]*fracoes_quentes_abaixo[i][quantidade_quente_abaixo[i]-1]))), align="left", font=("Arial", 10, "normal"))
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
						y_acima -= 40 * (quantidade_quente_abaixo[i] - quantidade_quente[i])
				elif dividida_quente_abaixo[i]:
					y_acima -= 40 * (quantidade_quente_abaixo[i] - 1)
			elif onde == "below":
				if dividida_quente[i] and dividida_quente_abaixo[i]:
					if quantidade_quente[i] > quantidade_quente_abaixo[i]:
						y_abaixo -= 40 * (quantidade_quente[i] - quantidade_quente_abaixo[i])
				elif dividida_quente[i]:
					y_abaixo -= 40 * (quantidade_quente[i] - 1)
			y_acima -= 40
			y_abaixo -= 40

	def frias(onde, correntes_desenho, presente):
		global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo
		distancia_x = 500
		for i in range(len(correntes_desenho)):
			if presente[i]:
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].speed(1000)
				if e_utilidade_fria[i]:
					correntes_desenho[i].color("#7FFFD4")
				else:
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
						temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]))), align="left", font=("Arial", 10, "normal"))
					else:
						correntes_desenho_sub_acima[i] = [0] * (quantidade_fria[i] - 1)
						for j in range(quantidade_fria[i] - 1):
							temp.sety(y_acima - 8)
							temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]*fracoes_frias[i][j]))), align="left", font=("Arial", 10, "normal"))
							correntes_desenho_sub_acima[i][j] = turtle.Turtle()
							correntes_desenho_sub_acima[i][j].color("blue")
							correntes_desenho_sub_acima[i][j].pensize(3)
							correntes_desenho_sub_acima[i][j].shapesize(0.001, 0.001, 0.001)
							correntes_desenho_sub_acima[i][j].penup()
							correntes_desenho_sub_acima[i][j].sety(y_acima)
							if Tc0_acima[i] == pinchf:
								correntes_desenho_sub_acima[i][j].setx(-24)
								correntes_desenho_sub_acima[i][j].pendown()
								correntes_desenho_sub_acima[i][j].right(90)
								correntes_desenho_sub_acima[i][j].forward(40)
								correntes_desenho_sub_acima[i][j].right(90)
								if fechar_corrente[i]:
									correntes_desenho_sub_acima[i][j].forward((len(matriz_armazenada)+1)*55)
									temperatura.sety(y_acima + 1)
									temperatura.setx(-(len(matriz_armazenada)+1)*55 - len(str(round(temp_misturador[i], 1))*7))
									temperatura.write(str(round(temp_misturador[i], 1)), align="left", font=("Arial", 8, "normal"))
								else:
									correntes_desenho_sub_acima[i][j].forward(distancia_x - 44)
							else:
								correntes_desenho_sub_acima[i][j].setx(-120)
								correntes_desenho_sub_acima[i][j].pendown()
								correntes_desenho_sub_acima[i][j].right(90)
								correntes_desenho_sub_acima[i][j].forward(40)
								correntes_desenho_sub_acima[i][j].right(90)
								if fechar_corrente[i]:
									correntes_desenho_sub_acima[i][j].forward((len(matriz_armazenada)+1)*55)
									temperatura.sety(y_acima + 1)
									temperatura.setx(-(len(matriz_armazenada)+1)*55 - len(str(round(temp_misturador[i], 1))*7))
									temperatura.write(str(round(temp_misturador[i], 1)), align="left", font=("Arial", 8, "normal"))
								else:
									correntes_desenho_sub_acima[i][j].forward(distancia_x - 140)
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(40*(j+1))
							correntes_desenho_sub_acima[i][j].left(90)
							correntes_desenho_sub_acima[i][j].forward(20)
							y_acima -= 40
						temp.sety(y_acima - 8)
						temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]*fracoes_frias[i][quantidade_fria[i]-1]))), align="left", font=("Arial", 10, "normal"))
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
						temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]))), align="left", font=("Arial", 10, "normal"))
					else:
						correntes_desenho_sub_abaixo[i] = [0] * (quantidade_fria_abaixo[i] - 1)
						for j in range(quantidade_fria_abaixo[i]-1):
							temp.sety(y_abaixo - 8)
							temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]*fracoes_frias_abaixo[i][j]))), align="left", font=("Arial", 10, "normal"))
							correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
							if e_utilidade_fria[i]:
								correntes_desenho_sub_abaixo[i][j].color("#7FFFD4")
							else:
								correntes_desenho_sub_abaixo[i][j].color("blue")
							correntes_desenho_sub_abaixo[i][j].pensize(3)
							correntes_desenho_sub_abaixo[i][j].shapesize(0.001, 0.001, 0.001)
							correntes_desenho_sub_abaixo[i][j].penup()
							correntes_desenho_sub_abaixo[i][j].setx(distancia_x - 20)
							correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
							correntes_desenho_sub_abaixo[i][j].pendown()
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(40)
							correntes_desenho_sub_abaixo[i][j].right(90)
							if Tcf_abaixo[i] == pinchf:
								correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 44)
							else:
								correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 140)
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(40*(j+1))
							correntes_desenho_sub_abaixo[i][j].left(90)
							correntes_desenho_sub_abaixo[i][j].forward(20)
							y_abaixo -= 40
						temp.sety(y_abaixo - 8)
						temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]*fracoes_frias_abaixo[i][quantidade_fria_abaixo[i]-1]))), align="left", font=("Arial", 10, "normal"))
					if Tcf_abaixo[i] == pinchf:
						correntes_desenho[i].forward(distancia_x - 4)
					else:
						correntes_desenho[i].forward(distancia_x - 100)
			if onde == "above":
				if dividida_fria_abaixo[i] and dividida_fria[i]:
					if quantidade_fria_abaixo[i] > quantidade_fria[i]:
						y_acima -= 40 * (quantidade_fria_abaixo[i] - quantidade_fria[i])
				elif dividida_fria_abaixo[i]:
					y_acima -= 40 * (quantidade_fria_abaixo[i] - 1)
			elif onde == "below":
				if dividida_fria[i] and dividida_fria_abaixo[i]:
					if quantidade_fria[i] > quantidade_fria_abaixo[i]:
						y_abaixo -= 40 * (quantidade_fria[i] - quantidade_fria_abaixo[i])
				elif dividida_fria[i]:
					y_abaixo -= 40 * (quantidade_fria[i] - 1)

			y_acima -= 40
			y_abaixo -= 40

	def pinch(tamanho):
		pinch = turtle.Turtle()
		pinch.speed(1000)
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

	def inserir_trocador_desenho(onde, corrente_quente, corrente_fria, subestagio, trocadorr, trocador_atual):
		trocador = turtle.Turtle()
		trocador.speed(1000)
		trocador.pensize(1.5)
		if e_utilidade_quente[trocadorr[0]-1]:
			trocador.color("black", "orange")
		elif e_utilidade_fria[trocadorr[1]-1]:
			trocador.color("black", "#7FFFD4")
		else:
			trocador.color("black", "white")
		trocador.shapesize(0.001, 0.001, 0.001)
		trocador.penup()
		if onde == "above":
			trocador.setx(-subestagio*55)
			temp.setx(-subestagio*55 - len(str(float('{:.3f}'.format(trocadorr[6]))))*3)
			if dividida_quente[trocadorr[0]-1]:
				trocador.sety(corrente_quente.pos()[1] - 10 - 40*(trocadorr[2]-1))
				temp.sety(corrente_quente.pos()[1] + 10 - 40*(trocadorr[2]-1))
				temperatura.sety(corrente_quente.pos()[1] - 14 - 40*(trocadorr[2]-1))
				ident.sety(corrente_quente.pos()[1] - 5 - 40*(trocadorr[2]-1))
			else:
				trocador.sety(corrente_quente.pos()[1]-10)
				temp.sety(corrente_quente.pos()[1]+10)
				temperatura.sety(corrente_quente.pos()[1] - 14)
				ident.sety(corrente_quente.pos()[1] - 5)
			temperatura.setx(-subestagio*55 - 8 - len(str(round(trocadorr[7], 1)))*6)
			temperatura.write(str(round(trocadorr[7], 1)), align="left", font=("Arial", 8, "normal"))
			trocador.pendown()
			trocador.begin_fill()
			trocador.circle(10)
			trocador.end_fill()
			ident.setx(-subestagio*55 + 1)
			ident.write("T" + str(trocador_atual), align="center", font=("Arial", 10, "bold"))
			if dividida_fria[trocadorr[1]-1]:
				trocador.sety(corrente_fria.pos()[1] - 10 - 40*(trocadorr[3]-1))
				temperatura.sety(corrente_fria.pos()[1] - 14 - 40*(trocadorr[3]-1))
				ident.sety(corrente_fria.pos()[1] - 5 - 40*(trocadorr[3]-1))
			else:
				trocador.sety(corrente_fria.pos()[1] - 10)
				temperatura.sety(corrente_fria.pos()[1] - 14)
				ident.sety(corrente_fria.pos()[1] - 5)
			temperatura.setx(-subestagio*55 - 8 - len(str(round(trocadorr[8],1)))*6)
			temperatura.write(str(round(trocadorr[8], 1)), align="left", font=("Arial", 8, "normal"))
			trocador.begin_fill()
			trocador.circle(10)
			trocador.end_fill()
			ident.write("T" + str(trocador_atual), align="center", font=("Arial", 10, "bold"))
		elif onde == "below":
			trocador.setx(subestagio*55)
			temp.setx(subestagio*55 - len(str(trocadorr[6]))*3)
			if dividida_quente_abaixo[trocadorr[0]-1]:
				trocador.sety(corrente_quente.pos()[1] - 10 - 40*(trocadorr[2]-1))
				temp.sety(corrente_quente.pos()[1] + 10 - 40*(trocadorr[2]-1))
				temperatura.sety(corrente_quente.pos()[1] - 14 - 40*(trocadorr[2]-1))
				ident.sety(corrente_quente.pos()[1] - 5 - 40*(trocadorr[2]-1))
			else:
				trocador.sety(corrente_quente.pos()[1]-10)
				temp.sety(corrente_quente.pos()[1]+10)
				temperatura.sety(corrente_quente.pos()[1] - 14)
				ident.sety(corrente_quente.pos()[1] - 5)
			temperatura.setx(subestagio*55 + 13)
			temperatura.write(str(round(trocadorr[7], 1)), align="left", font=("Arial", 8, "normal"))
			trocador.pendown()
			trocador.begin_fill()
			trocador.circle(10)
			trocador.end_fill()
			ident.setx(subestagio*55 + 1)
			ident.write("T" + str(trocador_atual), align="center", font=("Arial", 10, "bold"))
			if dividida_fria_abaixo[trocadorr[1]-1]:
				trocador.sety(corrente_fria.pos()[1] - 10 - 40*(trocadorr[3]-1))
				temperatura.sety(corrente_fria.pos()[1] - 14 - 40*(trocadorr[3]-1))
				ident.sety(corrente_fria.pos()[1] - 5 - 40*(trocadorr[3] - 1))
			else:
				trocador.sety(corrente_fria.pos()[1] - 10)
				temperatura.sety(corrente_fria.pos()[1] - 14 - 40*(trocadorr[3]-1))
				ident.sety(corrente_fria.pos()[1] - 5)
			temperatura.setx(subestagio*55 + 13)
			temperatura.write(str(round(trocadorr[8], 1)), align="left", font=("Arial", 8, "normal"))
			trocador.begin_fill()
			trocador.circle(10)
			trocador.end_fill()
			ident.write("T" + str(trocador_atual), align="center", font=("Arial", 10, "bold"))

		temp.write(str(float('{:.3f}'.format(trocadorr[6]))), align="left", font=("Arial", 10, "bold"))

	def utilidade_desenho(onde, corrente, subestagio, calor, primeiro, utilidade_atual):
		utilidade = turtle.Turtle()
		utilidade.speed(1000)
		utilidade.pensize(1.5)
		utilidade.shapesize(0.001, 0.001, 0.001)
		utilidade.penup()
		if onde == "above":
			utilidade.color("black", "orange")
			if primeiro == 0:
				utilidade.setx(-(subestagio+1)*55)
				temp.setx(-(subestagio+1)*55 - len(str(round(calor, 2)))*3)
				ident.setx(-(subestagio+1)*55 + 1)
			else:
				utilidade.setx(-(subestagio+1)*55 + primeiro*25)
				temp.setx(-(subestagio+1)*55 + primeiro*25 - len(str(round(calor, 2)))*3)
				ident.setx(-(subestagio+1)*55 + primeiro*25 + 1)
		elif onde == "below":
			utilidade.color("black", "#7FFFD4")
			if primeiro == 0:
				utilidade.setx((subestagio+1)*55)
				temp.setx((subestagio+1)*55 - len(str(round(calor, 2)))*3)
				ident.setx((subestagio+1)*55 + 1)
			else:
				utilidade.setx((subestagio+1)*55 - primeiro*25)
				temp.setx((subestagio+1)*55 - primeiro*25 - len(str(round(calor, 2)))*3)
				ident.setx((subestagio+1)*55 - primeiro*25 + 1)
		utilidade.sety(corrente.pos()[1]-10)
		utilidade.pendown()
		utilidade.begin_fill()
		utilidade.circle(10)
		utilidade.end_fill()
		temp.sety(corrente.pos()[1]+10)
		temp.write(str(round(calor, 2)), align="left", font=("Arial", 10, "bold"))
		ident.sety(corrente.pos()[1] - 5)
		if onde == "above":
			ident.write("H" + str(utilidade_atual), align="center", font=("Arial", 10, "bold"))
		if onde == "below":
			ident.write("C" + str(utilidade_atual), align="center", font=("Arial", 10, "bold"))


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

	trocador_atual = 1

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
			inserir_trocador_desenho("above", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr, trocador_atual)
			trocador_atual += 1

		if len(utilidades) > 0:
			primeiro = 0
			util = 1
			for utilidadee in utilidades:
				subestagio += 1
				utilidade_desenho("above", correntes_frias[utilidadee[0]-1], subestagio, utilidadee[1], primeiro, util)
				primeiro += 1
				util += 1

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
			inserir_trocador_desenho("below", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr, trocador_atual)
			trocador_atual += 1

		if len(utilidades_abaixo) > 0:
			primeiro = 0
			util = 1
			for utilidadee in utilidades_abaixo:
				subestagio += 1
				utilidade_desenho("below", correntes_quentes[utilidadee[0]-1], subestagio, utilidadee[1], primeiro, util)
				primeiro += 1
				util += 1

	if teste:
		salvar_rede(teste)
	else:
		salvar_rede(teste)

def salvar_rede(teste):
	turtle.getscreen()
	turtle.getcanvas().postscript(file="duck.eps")
	turtle.bye()
	TARGET_BOUNDS = (1280, 720)
	pic = Image.open('duck.eps')
	pic.load(scale=10)
	if pic.mode in ('P', '1'):
		pic = pic.convert("RGB")
	ratio = min(TARGET_BOUNDS[0] / pic.size[0],
				TARGET_BOUNDS[1] / pic.size[1])
	new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))
	pic = pic.resize(new_size, Image.ANTIALIAS)
	imagem = pic.crop((0, 100, 1280, 500))
	imagem.save("image.png")
	dlg.rede = QPixmap("image.png")
	dlg.label_teste = QtWidgets.QLabel(dlg)
	dlg.label_teste.setPixmap(dlg.rede)
	dlg.label_teste.setAlignment(QtCore.Qt.AlignCenter)

	if not teste:
		dlg.rede_teste.addWidget(dlg.label_teste)
		dlg.tabWidget.setCurrentIndex(5)
	else:
		dlg.tela_rede = uic.loadUi("tela_rede.ui")
		dlg.tela_rede.showMaximized()
		# dlg.label_teste.setScaledContents(True)
		dlg.label_teste.setAlignment(Qt.AlignCenter)
		dlg.tela_rede.so_mostrar.addWidget(dlg.label_teste)




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
		global subestagio_trocador
		indice = len(matriz_armazenada) - 1
		remover_trocador(dlg, dados_do_trocador, indice, matriz_armazenada)
		printar()
		checaresgotadosacima()
		dlg.dtmin.close()
		subestagio_trocador = indice

	def below(dados_do_trocacdor):
		global subestagio_trocador_abaixo
		indice = len(matriz_trocadores_abaixo) - 1
		remover_trocador_abaixo(dlg, dados_do_trocador, indice, matriz_trocadores_abaixo)
		printar_abaixo()
		checaresgotadosabaixo()
		dlg.dtmin.close()
		subestagio_trocador_abaixo = indice

def dividir_corrente(divisao, onde):
	global divtype
	divtype = divisao
	dlg.DivisaoQuente = uic.loadUi("DivisaoQuente.ui")
	dlg.DivisaoFria = uic.loadUi("DivisaoQuente.ui")
	if divtype == "Q":
		for i in range(nhot):
			dlg.DivisaoQuente.comboBox_2.addItem(str(i+1))
		for i in range(ncold):
			dlg.DivisaoQuente.comboBox_3.addItem(str(i+1))
		dlg.DivisaoQuente.show()
	elif divtype == "F":
		dlg.DivisaoFria.label_5.setText("Split Cold Stream")
		for i in range(ncold):
			dlg.DivisaoFria.comboBox_2.addItem(str(i+1))
		for i in range(nhot):
			dlg.DivisaoFria.comboBox_3.addItem(str(i+1))
		dlg.DivisaoFria.show()


	def confirm():
		global caixa_fracao, quantidade, corrente, estagio
		if divtype == "Q":
			quantidade = int(dlg.DivisaoQuente.comboBox_3.currentText())
			estagio = 1
			corrente = int(dlg.DivisaoQuente.comboBox_2.currentText())
		if divtype == "F":
			quantidade = int(dlg.DivisaoFria.comboBox_3.currentText())
			estagio = 1
			corrente = int(dlg.DivisaoFria.comboBox_2.currentText())

		if verificar_trocador_estagio(estagio, corrente, divtype) and onde == "above":
			QMessageBox.about(dlg, "Error!", "There is already a heat exchanger in this position, remove it before making the division.")
			return

		if verificar_trocador_estagio_abaixo(estagio, corrente, divtype) and onde == "below":
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
			caixa_fracao[i].setValue(round(1/quantidade, 2))
			caixa_corrente[i].setText("Substream {}".format(i+1))
			caixa_corrente[i].setAlignment(Qt.AlignCenter)
			caixa_fracao[i].setAlignment(Qt.AlignCenter)
		x = caixa_fracao[-1].value()
		if x * quantidade > 1:
			sobrou = x*quantidade - 1
			caixa_fracao[-1].setValue(x - sobrou)
		if x * quantidade < 1:
			faltou = 1 - x*quantidade
			caixa_fracao[-1].setValue(x + faltou)

	def split(onde):
		soma = 0
		fracao = [0] * quantidade
		for i in range(quantidade):
			soma += round(float(caixa_fracao[i].value()), 2)
			fracao[i] = round(float(caixa_fracao[i].value()), 2)
		if soma != 1:
			QMessageBox.about(dlg, "Error!", "The sum of the fractions must be equals 1.")
			return

		if onde == "above":
			divisao_de_correntes(divtype, estagio, corrente, quantidade, fracao)
			if divtype == "F":
				testar_correntes(dlg, True)
				dlg.comboBox_51.setEnabled(True)
			else:
				testar_correntes(dlg)
				dlg.comboBox_50.setEnabled(True)
		elif onde == "below":
			divisao_de_correntes_abaixo(divtype, estagio, corrente, quantidade, fracao)
			if divtype == "Q":
				testar_correntes_abaixo(dlg, True)
				dlg.comboBox_53.setEnabled(True)
			else:
				testar_correntes_abaixo(dlg)
				dlg.comboBox_54.setEnabled(True)

		if divtype == "Q":
			dlg.DivisaoQuente.close()
		if divtype == "F":
			dlg.DivisaoFria.close()

		printar()
		printar_abaixo()

	dlg.DivisaoQuente.pushButton.clicked.connect(lambda: confirm())
	dlg.DivisaoQuente.pushButton_3.clicked.connect(lambda: split(onde))
	dlg.DivisaoQuente.pushButton_2.clicked.connect(lambda: dlg.DivisaoQuente.close())
	dlg.DivisaoFria.pushButton.clicked.connect(lambda: confirm())
	dlg.DivisaoFria.pushButton_3.clicked.connect(lambda: split(onde))
	dlg.DivisaoFria.pushButton_2.clicked.connect(lambda: dlg.DivisaoFria.close())

def evolucao(matriz_acima_naomuda, matriz_abaixo_naomuda, nivel):
	def criar_matriz(matriz_acima, matriz_abaixo):
		global trocadores_uteis
		util = 1
		trocadores_uteis = []
		for i in range(len(matriz_acima)):
			if len(matriz_acima[i]) == 2:
				calor = matriz_acima[i][1]
				corrente_fria = matriz_acima[i][0]
				matriz_acima[i] = [nhot+util, corrente_fria, calor]
				trocadores_uteis.append([True, util])
				util += 1
			else:
				trocadores_uteis.append([False, False])

		for trocador in matriz_acima:
			trocador[0] -= 1
			trocador[1] += (nhot + util - 2)

		util_fria = 1
		for i in range(len(matriz_abaixo)):
			if len(matriz_abaixo[i]) == 2:
				calor = matriz_abaixo[i][1]
				corrente_quente = matriz_abaixo[i][0]
				matriz_abaixo[i] = [corrente_quente, ncold+util_fria, calor]
				trocadores_uteis.append([True, util_fria])
				util_fria += 1
			else:
				trocadores_uteis.append([False, False])

		for trocador in matriz_abaixo:
			trocador[0] -= 1
			trocador[1] += (nhot + util - 2)


		print(trocadores_uteis)
		return matriz_acima + matriz_abaixo, nhot+util-1, ncold+util_fria-1

	def criar_incidencia(matriz_nova, nhot, ncold):
		incidencia = []
		for i in range(nhot + ncold):
			incidencia.append([])
		for i in range(nhot):
			for trocador in matriz_nova:
				if trocador[0] == i:
					incidencia[i].append(1)
				else:
					incidencia[i].append(0)
		for j in range(nhot, ncold + nhot):
			for trocador in matriz_nova:
				if trocador[1] == j:
					incidencia[j].append(-1)
				else:
					incidencia[j].append(0)
		return incidencia

	def achar_trocador(incidencia, matriz_trocadores, correntee, excecao, comecar, nivel, n, trocador_inicial):
		i = incidencia[correntee][excecao]
		for correntes in range(len(incidencia)):
			if incidencia[correntes][excecao] == -i:
				c = correntes
		if n == 0:
			if incidencia[c][comecar] == -i and comecar != excecao:
				t = comecar
				return c, t
		elif n == nivel*2 - 1:
			if incidencia[c][trocador_inicial] == -i and trocador_inicial != excecao:
				t = trocador_inicial
				return c, t
		else:
			for trocadores in range(len(matriz_trocadores)):
				if incidencia[c][trocadores] == -i and trocadores != excecao:
					t = trocadores
					return c, t
		return "o", "o"

	def lacos(incidencia, matriz_trocadores, nivel):
		for trocadores in range(len(matriz_trocadores)):
			trocador_inicial = trocadores
			trocador = trocadores
			for c in range(len(incidencia)):
				if incidencia[c][trocadores] == 1:
					corrente_inicial = c
					corrente = c
			for comecar in range(len(matriz_trocadores)):
				corrente = corrente_inicial
				trocador = trocador_inicial
				trocadores_laco = []
				tenta_dnv = True
				for n in range(nivel*2):
					if tenta_dnv:
						corrente, trocador = achar_trocador(incidencia, matriz_trocadores, corrente, trocador, comecar, nivel, n, trocador_inicial)
						if corrente == "o":
							tenta_dnv = False
						else:
							trocadores_laco.append(trocador+1)
							if corrente == corrente_inicial and trocador == trocador_inicial:
								return trocadores_laco

		return ["None"]

	# def criar_rede_completa(matriz_acima, matriz_abaixo):
	# 	receber_pinch_completo(Th0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, Thf_acima, Tc0_acima)

	matriz_acima = []
	matriz_abaixo = []
	for i in range(len(matriz_acima_naomuda)):
		trocador = []
		for j in range(len(matriz_acima_naomuda)):
			try:
				trocador.append(matriz_acima_naomuda[i][j])
			except:
				pass
		matriz_acima.append(trocador)
	for i in range(len(matriz_abaixo_naomuda)):
		trocador = []
		for j in range(len(matriz_abaixo_naomuda)):
			try:
				trocador.append(matriz_abaixo_naomuda[i][j])
			except:
				pass
		matriz_abaixo.append(trocador)

	trocadores, n_quentes, n_frias = criar_matriz(matriz_acima, matriz_abaixo)
	incidencia = criar_incidencia(trocadores, n_quentes, n_frias)
	print(np.matrix(incidencia))
	trocadores_laco = sorted(lacos(incidencia, trocadores, nivel))
	print(trocadores_laco)
	text = ""
	for i in range(len(trocadores_laco)):
		if trocadores_laco[i] != "None":
			if not trocadores_uteis[trocadores_laco[i]-1][0]:
				if trocadores_laco[i] >= len(matriz_acima_naomuda):
					text += ("T" + str(trocadores_laco[i] - len(utilidades)) + ", ")
				else:
					text += ("T" + str(trocadores_laco[i]) + ", ")
			elif trocadores_laco[i] < len(matriz_acima_naomuda):
				text += ("H" + str(trocadores_uteis[trocadores_laco[i]-1][1]) + ", ")
			else:
				text += ("C" + str(trocadores_uteis[trocadores_laco[i]-1][1]) + ", ")
		else:
			text = trocadores_laco[i] + "."

	text = text[:len(text)-2]
	text += "."
	dlg.trocadores_loop.setText(text)





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
					if corrente_fria_presente_acima[corrente]:
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
	global subestagio_trocador
	subestagio_trocador += 1
	dados_do_trocador = ler_dados(dlg, subestagio_trocador)
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
	global subestagio_trocador
	indice_remover = dlg.tableWidget_2.currentRow()
	if indice_remover == -1:
		QMessageBox.about(dlg, "Error!", "Select the line of the Heat Exchanger that you want to remove")
		return
	if indice_remover <= len(matriz_armazenada) - 1:
		if len(utilidades) > 0:
			for i in range(len(utilidades)-1, -1, -1):
				try:
					remover_utilidade(utilidades[i][0], i, utilidades)
				except:
					print("deu nao")
		dlg.comboBox_10.setEnabled(False)
		dlg.pushButton_8.setEnabled(False)
		for i in range(len(matriz_armazenada)-1, indice_remover-1, -1):
			trocador_remover = matriz_armazenada[i]
			remover_trocador(dlg, trocador_remover, i, matriz_armazenada)
			atualizar_matriz(matriz_armazenada)
		subestagio_trocador = indice_remover
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

	dlg.TempLoadAbove.comboBox.setCurrentText(str(dlg.comboBox_2.currentText()))
	dlg.TempLoadAbove.comboBox_2.setCurrentText(str(dlg.comboBox_5.currentText()))
	dlg.TempLoadAbove.comboBox_3.setCurrentText(str(dlg.comboBox_50.currentText()))
	dlg.TempLoadAbove.comboBox_4.setCurrentText(str(dlg.comboBox_51.currentText()))

	dlg.TempLoadAbove.pushButton_2.clicked.connect(lambda: dlg.TempLoadAbove.close())
	dlg.TempLoadAbove.pushButton.clicked.connect(lambda: caixa_de_temperatura(dlg, len(matriz_armazenada)))

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
	global subestagio_trocador_abaixo
	subestagio_trocador_abaixo += 1
	dados_do_trocador = ler_dados_abaixo(dlg, subestagio_trocador_abaixo)
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
	global subestagio_trocador_abaixo
	indice_remover = dlg.tableWidget_14.currentRow()
	if indice_remover == -1:
		QMessageBox.about(dlg, "Error!", "Select the line of the Heat Exchanger that you want to remove")
		return
	if indice_remover <= len(matriz_trocadores_abaixo) - 1:
		if len(utilidades_abaixo) > 0:
			for i in range(len(utilidades_abaixo)-1, -1, -1):
				try:
					remover_utilidade_abaixo(utilidades_abaixo[i][0], i, utilidades_abaixo)
				except:
					print("deu nao")
		dlg.comboBox_43.setEnabled(False)
		dlg.pushButton_20.setEnabled(False)
		for i in range(len(matriz_trocadores_abaixo)-1, indice_remover-1, -1):
			trocador_remover = matriz_trocadores_abaixo[i]
			remover_trocador_abaixo(dlg, trocador_remover, i, matriz_trocadores_abaixo)
			atualizar_matriz_abaixo(matriz_trocadores_abaixo)
		subestagio_trocador_abaixo = indice_remover
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

	dlg.TempLoadBelow.comboBox.setCurrentText(str(dlg.comboBox_35.currentText()))
	dlg.TempLoadBelow.comboBox_2.setCurrentText(str(dlg.comboBox_36.currentText()))
	dlg.TempLoadBelow.comboBox_3.setCurrentText(str(dlg.comboBox_53.currentText()))
	dlg.TempLoadBelow.comboBox_4.setCurrentText(str(dlg.comboBox_54.currentText()))


	dlg.TempLoadBelow.pushButton.clicked.connect(lambda: caixa_de_temperatura_abaixo(dlg, len(matriz_trocadores_abaixo)))
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



#inutilidades porem depende
def suprir_9_correntes():

	if nhot == 2 and ncold == 2:
		acima = [[1, 1, 1, 1, 1, 1, 300], [2, 2, 1, 1, 2, 1, 120], [1], [2]]
		abaixo = [[1, 2, 1, 1, 1, 1, 30], [2, 2, 1, 1, 2, 1, 10], [2]]
	else:
		acima = [[3, 2, 1, 2, 1, 1, 674.632], [2, 2, 1, 1, 2, 1, 220.32], [3, 2, 1, 1, 3, 1, 309.768], [2]]
		abaixo = [[1, 2, 1, 1, 1, 1, 411.81], [2, 1, 1, 1, 2, 1, 31.3], [3, 1, 1, 1, 3, 1, 195.2], [1, 1, 1, 1, 4, 1, 715.83], [1], [2], [3]]

		divisao_de_correntes("F", 1, 2, 2, [0.56, 0.44])

	for trocador in acima:
		if len(trocador) > 1:
			nova_matriz, violou, trocador_violado = inserir_trocador(dlg, trocador)
			matriz_armazenada.append(nova_matriz[-1])
		else:
			utilidadee = adicionar_utilidade(dlg, trocador[0])
			utilidades.append(utilidadee[-1])
			utilidades.sort()

	for trocador in abaixo:
		if len(trocador) > 1:
			nova_matriz, violou, trocador_violado = inserir_trocador_abaixo(dlg, trocador)
			matriz_trocadores_abaixo.append(nova_matriz[-1])
		else:
			utilidadee = adicionar_utilidade_abaixo(dlg, trocador[0])
			utilidades_abaixo.append(utilidadee[-1])
			utilidades_abaixo.sort()

	printar()
	printar_abaixo()

	desenhar_rede(correntes_quentes, correntes_frias)

def centralizar_combobox_teste(x):
	x.setEditable(True)
	x.lineEdit().setReadOnly(True)
	x.lineEdit().setAlignment(Qt.AlignCenter)
	x.setStyleSheet("QComboBox { background-color: #e1e1e1 }")
	for i in range(x.count()):
		x.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

def mostrar():
	dlg.rede = QPixmap("image.png")
	dlg.label_teste = QtWidgets.QLabel(dlg)
	dlg.label_teste.setPixmap(dlg.rede)
	dlg.label_teste.setAlignment(QtCore.Qt.AlignCenter)
	dlg.rede_teste.addWidget(dlg.label_teste)



#streams
dlg.botao_addstream.clicked.connect(apertaradd) #add stream
dlg.botao_addutility.clicked.connect(add_utilidade)
dlg.actionOpen.triggered.connect(lambda: os.execl(sys.executable, os.path.abspath(__file__), *sys.argv))
dlg.actionOpen_2.triggered.connect(openfile_teste) #file > open
dlg.donebutton.clicked.connect(done_teste) #done
dlg.pinchbutton.clicked.connect(pinch_teste) #pinch
#dlg.tableWidget.itemChanged.connect(itemedited)
dlg.sistema_unidades.currentIndexChanged.connect(lambda: unidades(False))
dlg.temp_unidade.currentIndexChanged.connect(unidades)
dlg.cp_unidade.currentIndexChanged.connect(unidades)
dlg.pelicula_unidade.currentIndexChanged.connect(unidades)
dlg.temp_unidade_util.currentIndexChanged.connect(unidades)
dlg.pelicula_unidade_util.currentIndexChanged.connect(unidades)

#above
dlg.radioButton.toggled.connect(lambda: dlg.lineEdit_5.setEnabled(True)) #quando marca o heat load libera a linha pra digitar
dlg.radioButton_4.toggled.connect(lambda: dlg.lineEdit_5.setEnabled(False)) #block o heat load quando max heat ta ativado
dlg.radioButton_4.setChecked(True) #por padrao abre o prog com max heat selecionado
dlg.pushButton_9.clicked.connect(lambda: dividir_corrente("Q", "above"))
dlg.pushButton_13.clicked.connect(lambda: dividir_corrente("F", "above"))
dlg.checkBox.stateChanged.connect(printar) #show splited streams printa tudo dnv
dlg.checkBox_2.stateChanged.connect(printar) #show splited streams printa tudo dnv
dlg.pushButton_6.clicked.connect(inserir_teste) #add heat exchanger
dlg.pushButton_10.clicked.connect(remover_teste) #remove heat exchanger
dlg.pushButton_14.clicked.connect(calcular_calor_teste) #choose stream temperature to calculate heat
dlg.pushButton_8.clicked.connect(utilidade_teste_acima) #add cold utility
dlg.pushButton_16.clicked.connect(lambda: desenhar_rede(correntes_quentes, correntes_frias, True))
dlg.pushButton_22.clicked.connect(suprir_9_correntes) #aaaaaaaa botao quebra de laços acima

#below
dlg.radioButton_17.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(True)) #quando marca o heat load libera a linha pra digitar
dlg.radioButton_20.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(False)) #block o heat load quando max heat ta ativado
dlg.radioButton_20.setChecked(True) #por padrao abre o prog com max heat selecionado
dlg.pushButton_12.clicked.connect(lambda: dividir_corrente("F", "below"))
dlg.pushButton_11.clicked.connect(lambda: dividir_corrente("Q", "below"))
dlg.checkBox_9.stateChanged.connect(printar_abaixo) #show splited streams printa tudo dnv
dlg.checkBox_10.stateChanged.connect(printar_abaixo) #show splited streams printa tudo dnv
dlg.pushButton_18.clicked.connect(inserir_teste_abaixo) #add heat exchanger
dlg.pushButton_15.clicked.connect(remover_teste_abaixo) #remove heat exchanger
dlg.pushButton_17.clicked.connect(calcular_calor_abaixo) #choose stream temperature to calculate heat
dlg.pushButton_20.clicked.connect(utilidade_teste_abaixo) #add hot utility
dlg.pushButton_19.clicked.connect(lambda: desenhar_rede(correntes_quentes, correntes_frias))


#custos
dlg.otimizabotao.clicked.connect(lambda: otimizafun())



#evolução
dlg.identificar_laco.clicked.connect(lambda: evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, int(dlg.nivel.currentText())))





dlg.stream_supply.setPlaceholderText(" Ex: 273.15")
dlg.stream_target.setPlaceholderText(" Ex: 273.15")
dlg.util_inlet.setPlaceholderText(" Ex: 273.15")
dlg.util_outlet.setPlaceholderText(" Ex: 273.15")
dlg.stream_cp.setPlaceholderText(" Ex: 200.20")

header = dlg.tableWidget.horizontalHeader()
header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
for i in range(5):
	header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
header = dlg.tableWidget_5.horizontalHeader()
header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
for i in range(5):
	header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)



dlg.show()
dlg.showMaximized()
app.exec()
