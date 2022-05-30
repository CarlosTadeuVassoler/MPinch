from PyQt5 import QtWidgets , uic, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
import numpy as np
import funchpinchcerto as fp2
from funcPPinch import pontopinch
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pylab as P
from Graficocurva import plotgrafcurva,plotgrafcurva2
from Graficocurvabalanceada import cc1,cc2
import testesoriginal as tt
import xlsxwriter
from canvas import Gc1,Gc2
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
from CORRENTEGRAPH import cascata,cascata2
from prog_carlos import *
from prog_carlos_abaixo import *
from converter_unidades import *
from matplotlib.figure import Figure
from PIL import Image
import turtle
from exportaa import export
from svg_turtle import SvgTurtle
import os
from custo2 import varia
from superestrutura_completa import *
from tkinter import Tk

workbook = xlsxwriter.Workbook('testevv.xlsx')
worksheet = workbook.add_worksheet()

app=QtWidgets.QApplication([])
dlg=uic.loadUi("MPinch.ui")


matriz = []
matriz_armazenada = []
matriz_trocadores_abaixo = []
matriz_evolucao = []
utilidades = []
utilidades_abaixo = []
dTmin = 10
donee=0
done = False
cascat=[]
nstages=1
subestagio_trocador = 0
subestagio_trocador_abaixo = 0
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
correntes=[]
primeira_vez = True
divisoes = []
primeiro_laco = True
desenho_em_dia = False
desenho_em_dia_abaixo = False
desenho_em_dia_ambas = False
violados_acima = []
violados_abaixo = []
ja_mostrou = False
unidadeusada=["Temperature (K)","Enthalpy (kJ)","Enthalpy (kJ)"]
perguntar = True
remover_todos = False


#######################
def formatando(valor,index):
	if valor>=1_000_000:
		fomatador = '{:1.1f}M'.format(valor*0.000_001)
	else:
		fomatador = '{:1.0f}k'.format(valor * 0.001)
	return fomatador

def eq():
	start=float(dlg.dtstart.text())
	step=float(dlg.dtstep.text())
	asch=dlg.dtstep.text()
	asch = asch.split(".")
	try:
		if len(asch[1])>4:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setStyleSheet("font-weight: bold")
			msg.setStyleSheet("text-align:center")
			msg.setText("The limit is 4 digits after the separator.\nChange the step value and try again.")
			msg.setWindowTitle("Error")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
			return 0
	except:
		pass

	bsch=dlg.dtstart.text()
	bsch = bsch.split(".")

	try:
		if len(bsch[1])>4:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setStyleSheet("font-weight: bold")
			msg.setStyleSheet("text-align:center")
			msg.setText("The limit is 4 digits after the separator.\nChange the start value and try again.")
			msg.setWindowTitle("Error")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
			return 0
	except:
		pass



	stop=float(dlg.dtstop.text())
	csch=dlg.dtstop.text()
	csch = csch.split(".")

	try:
		if len(csch[1])>4:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setStyleSheet("font-weight: bold")
			msg.setStyleSheet("text-align:center")
			msg.setText("The limit is 4 digits after the separator.\nChange the stop value and try again.")
			msg.setWindowTitle("Error")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
			return 0
	except:
		pass

	if stop<start:
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Warning)
		msg.setStyleSheet("font-weight: bold")
		msg.setStyleSheet("text-align:center")
		msg.setText("The stop value needs to be higher than start value.\nChange the start or stop value and try again.")
		msg.setWindowTitle("Error")
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec_()
		return 0

	if len(np.arange(start, stop + step, step))>500:
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setWindowTitle("This may take some time")
		msgBox.setText("You will run about "+ str(len(np.arange(start, stop + step, step))) +" iteractions\nDo you want to proceed?")
		msgBox.setStyleSheet("font-weight: bold")
		msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

		returnValue = msgBox.exec()
		if returnValue == QMessageBox.Cancel:
			return 0

	dlg.equation = uic.loadUi("Select.ui")
	dlg.equation.show()

	def z3():
		if (dlg.equation.nareas.isChecked() == True):
			nnn=-1
			otimizafun(nnn)
		elif(dlg.equation.us1.isChecked() == True):
			nnn=-2
			otimizafun(nnn)
		elif(dlg.equation.esp.isChecked() == True):
			nnn=float(dlg.equation.lineesp.text())
			otimizafun(nnn)
		dlg.equation.close()


	dlg.equation.otimizarun.clicked.connect(lambda: z3())

def otimizafun(nnn):
	start=float(dlg.dtstart.text())

	step=float(dlg.dtstep.text())

	stop=float(dlg.dtstop.text())




	global variadt, yplot, custoopano, custocapital, custocapitalanual, custototanual,uf,uq,dtopt
	uf,uq,variadt, yplot, custoopano, custocapital, custocapitalanual, custototanual=varia(start,step,stop,correntes,nnn)
	changedv=[]
	print(uf,uq)
	changedv.append(variadt[0])
	for i in range(0,len(custocapitalanual)):
		try:
			changedv.append(variadt[i+1])
			if not(custocapitalanual[i]>custocapitalanual[i+1] and custocapitalanual[i+2]<custocapitalanual[i+1]):
				"""changedv.pop()"""
				"""custocapitalanual[i+1]=((custocapitalanual[i+2]-custocapitalanual[i])*(variadt[i+1]-variadt[i+2])/(variadt[i+2]-variadt[i]))+custocapitalanual[i+2]
				changedv.append(str(str(round(variadt[i+1],3))+"*"))"""
				"""custototanual[i+1]=custoopano[i+1]+custocapitalanual[i+1]"""
			else:
				pass
		except:
			pass


	Custoopotimizado=custoopano[custototanual.index(min(custototanual))]
	cccapitalanualopt=custocapitalanual[custototanual.index(min(custototanual))]
	dtopt=variadt[custototanual.index(min(custototanual))]
	print(dtopt)
	cccapitalopt=custocapital[custototanual.index(min(custototanual))]
	areaopt = yplot[custototanual.index(min(custototanual))]
	custototanualopt=min(custototanual)

	dlg.label_46.setText("Operating Cost : "+str(round(Custoopotimizado,2)))
	dlg.label_46.setFont(QFont('Arial', 10))
	dlg.label_46.setStyleSheet("font-weight: bold")
	try:
		dlg.label_45.setText("ΔTmin : "+str(round(dtopt,5))) #preciso prestar atenção nisso quanto ao passo
	except:
		dlg.label_45.setText("ΔTmin : "+str(dtopt)) #preciso prestar atenção nisso quanto ao passo

	dlg.label_45.setFont(QFont('Arial', 10))
	dlg.label_45.setStyleSheet("font-weight: bold")
	dlg.label_50.setText("Capital Cost : "+str(round(cccapitalopt,2)))
	dlg.label_50.setFont(QFont('Arial', 10))
	dlg.label_50.setStyleSheet("font-weight: bold")
	dlg.label_52.setText("Anualized Capital Cost : "+str(round(cccapitalanualopt,2)))
	dlg.label_52.setFont(QFont('Arial', 10))
	dlg.label_52.setStyleSheet("font-weight: bold")
	dlg.label_49.setText("Total Cost: "+str(round(custototanualopt,2)))
	dlg.label_49.setFont(QFont('Arial', 10))
	dlg.label_49.setStyleSheet("font-weight: bold")
	dlg.label_53.setText("Area: "+str(round(areaopt,2)))
	dlg.label_53.setFont(QFont('Arial', 10))
	dlg.label_53.setStyleSheet("font-weight: bold")



	row = 0
	valorbonito = np.round(variadt, 5)
	dlg.TABELA.setRowCount(len(valorbonito))

	p=0

	for data in range(0, len(valorbonito)):
		try:
			dlg.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(np.round(changedv[data], 5))))

		except:
			dlg.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(changedv[data])))
		dlg.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(np.round(yplot[data], 2))))
		dlg.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(np.round(custoopano[data], 2))))
		dlg.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(np.round(custocapitalanual[data], 2))))
		dlg.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(np.round(custototanual[data], 2))))
		row += 1

	# print(variadt)
	dlg.sc = myCanvas()
	y=[0]
	x=[0]
	dlg.sc.plot(x, y)


	dlg.sc2 = myCanvas2()
	dlg.sc2.plot(x, y)


	dlg.sc3 = myCanvas3()
	dlg.sc3.plot(x, y)
	dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva1.png"))


def mostra3():
	dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva1.png"))

def mostra2():
	dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva3.png"))

def mostra1():
	dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva2.png"))


class myCanvas(FigureCanvas):
	def __init__(self):
		self.fig=Figure()
		FigureCanvas.__init__(self,self.fig)

	def plot(self,x,y):
		# PLT.CLOSE("ALL") PRA NÃO COMER TODA A MEMORIA DO SEU PC PELO AMOR DE DEUS NÃO ESQUECE DISSO
		plt.close("all")

		plt.style.use('bmh')
		self.ax= self.fig.add_subplot(111)
		self.ax.yaxis.set_major_formatter(formatando)
		self.ax.plot(variadt,custoopano, label='Operational Cost x ΔTmin')
		self.ax.plot(variadt,custocapitalanual, label='Capital Cost x ΔTmin', color='k')
		self.ax.plot(variadt, custototanual, label='Total Cost x ΔTmin', color='r')
		self.ax.set_xlabel('ΔTmin')
		self.ax.set_ylabel('Cost')
		self.ax.legend()
		self.ax.grid(axis="x", color="black", alpha=.3, linewidth=2, linestyle=":")
		self.ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
		self.draw()
		self.fig.savefig("canva1.png",bbox_inches="tight", pad_inches=0.5)

class myCanvas2(FigureCanvas):
	def __init__(self):
		self.fig=Figure()
		FigureCanvas.__init__(self,self.fig)

	def plot(self,x,y):
		# PLT.CLOSE("ALL") PRA NÃO COMER TODA A MEMORIA DO SEU PC PELO AMOR DE DEUS NÃO ESQUECE DISSO
		plt.close("all")
		plt.style.use('bmh')

		self.ax= self.fig.add_subplot(111)
		self.ax.yaxis.set_major_formatter(formatando)

		# print(variadt)
		self.ax.plot(variadt,yplot, label='Area x ΔTmin', color='r')
		self.ax.set_xlabel('ΔTmin')
		self.ax.set_ylabel('Area')
		self.ax.legend()
		self.ax.grid(axis="x", color="black", alpha=.3, linewidth=2, linestyle=":")
		self.ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
		self.draw()
		self.fig.savefig("canva2.png",bbox_inches="tight", pad_inches=0.5)

class myCanvas3(FigureCanvas):
	def __init__(self):
		self.fig=Figure()
		FigureCanvas.__init__(self,self.fig)

	def plot(self,x,y):
		# PLT.CLOSE("ALL") PRA NÃO COMER TODA A MEMORIA DO SEU PC PELO AMOR DE DEUS NÃO ESQUECE DISSO
		plt.close("all")
		plt.style.use('bmh')
		self.ax= self.fig.add_subplot(111)
		#self.ax.yaxis.set_major_formatter(formatando)
		self.ax.plot(variadt,uq, label='Hot utility x ΔTmin', color='r')
		self.ax.plot(variadt, uf, label='Cold utility x ΔTmin', color='b')
		self.ax.set_xlabel('ΔTmin')
		self.ax.set_ylabel('Utility')
		self.ax.legend()
		self.ax.grid(axis="x", color="black", alpha=.3, linewidth=2, linestyle=":")
		self.ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
		self.draw()
		self.fig.savefig("canva3.png",bbox_inches="tight", pad_inches=0.5)
########################


def plotgraficocurva():

	try:
		dlg.labe1.hide()
		dlg.scrola1.hide()
		dlg.horizontalLayout_37.removeWidget(dlg.scrola1)
		dlg.graficodt1.show()
		dlg.graficodt2.show()
		dlg.linicio.show()
		dlg.lmeio.show()
		dlg.lfim.show()
	except:
		None
	try:
		dlg.labe2.hide()
		dlg.scrola2.hide()
		dlg.horizontalLayout_37.removeWidget(dlg.scrola2)
		dlg.graficodt1.show()
		dlg.graficodt2.show()
		dlg.linicio.show()
		dlg.lmeio.show()
		dlg.lfim.show()
	except:
		None

	try:
		asch = dlg.DTMIN1.text()
		asch = asch.split(".")
		try:
			if len(asch[1]) > 4:
				dlg.graficodt1.setText('Waiting for ΔTmin1 data...')
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setStyleSheet("font-weight: bold")
				msg.setStyleSheet("text-align:center")
				msg.setText(
					"The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT ONE} value and try again.")
				msg.setWindowTitle("Error")
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()
				return 0
		except:
			pass
		pinchf1,pinchq1,uq1,uf1,_=pontopinch(correntes,len(correntes),float(dlg.DTMIN1.text()))

		plotgrafcurva(correntes, float(dlg.DTMIN1.text()),uf1,uq1,pinchf1,pinchq1)

		dlg.graficodt1.setPixmap(QtGui.QPixmap("curvadt1.png"))

	except:
		dlg.graficodt1.setText('Waiting for ΔTmin1 data...')

	try:
		asch = dlg.DTMIN2.text()
		asch = asch.split(".")
		try:
			if len(asch[1]) > 4:
				dlg.graficodt2.setText('Waiting for ΔTmin2 data...')
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setStyleSheet("font-weight: bold")
				msg.setStyleSheet("text-align:center")
				msg.setText(
					"The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT TWO} value and try again.")
				msg.setWindowTitle("Error")
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()

				return 0
		except:
			pass
		pinchf2, pinchq2, uq2, uf2,_ = pontopinch(correntes, len(correntes),float(dlg.DTMIN2.text()))

		plotgrafcurva2(correntes, float(dlg.DTMIN2.text()), uf2, uq2, pinchf2, pinchq2)

		dlg.graficodt2.setPixmap(QtGui.QPixmap("curvadt2.png"))

	except:
		dlg.graficodt2.setText('Waiting for ΔTmin2 data...')

def plotgraficocurvacomp():
	try:
		dlg.labe1.hide()
		dlg.scrola1.hide()
		dlg.horizontalLayout_37.removeWidget(dlg.scrola1)
		dlg.graficodt1.show()
		dlg.graficodt2.show()
		dlg.linicio.show()
		dlg.lmeio.show()
		dlg.lfim.show()
	except:
		None
	try:
		dlg.labe2.hide()
		dlg.scrola2.hide()
		dlg.horizontalLayout_37.removeWidget(dlg.scrola2)
		dlg.graficodt1.show()
		dlg.graficodt2.show()
		dlg.linicio.show()
		dlg.lmeio.show()
		dlg.lfim.show()
	except:
		None

	try:
		try:
			asch = dlg.DTMIN1.text()
			asch = asch.split(".")
			if len(asch[1]) > 4:
				dlg.graficodt1.setText('Waiting for ΔTmin1 data...')
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setStyleSheet("font-weight: bold")
				msg.setStyleSheet("text-align:center")
				msg.setText(
					"The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT ONE} value and try again.")
				msg.setWindowTitle("Error")
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()
				return 0
		except:
			pass
		contador=0
		correntecomp = correntes
		tf1,tq1,uq1, uf1,_ = pontopinch(correntes, len(correntes), float(dlg.DTMIN1.text()))
		uf1, uq1,_,_ = fp2.pontopinch(correntes, len(correntes), float(dlg.DTMIN1.text()))
		for i in range(0,len(ccopi)):
			if ccopi[i][3]=='Cold':
				ccopi[i][2]=uf1/(ccopi[i][1]-ccopi[i][0])
				correntecomp.append(ccopi[i])
				contador+=1
			else:
				ccopi[i][2] = uq1 / (ccopi[i][0] - ccopi[i][1])
				correntecomp.append(ccopi[i])
				contador+=1

		_,_,datagraph,_,_,_,_ = tt.CUSTO(correntecomp, len(correntecomp))
		for i in range(0,contador):
			correntecomp.pop()
		cc1(datagraph,float(dlg.DTMIN1.text()),round(tf1,6),round(tq1,6))
		dlg.graficodt1.setPixmap(QtGui.QPixmap("cc1.png"))
	except:
		dlg.graficodt1.setText('Waiting for ΔTmin1 data...')
	try:
		try:
			asch = dlg.DTMIN2.text()
			asch = asch.split(".")
			if len(asch[1]) > 4:
				dlg.graficodt2.setText('Waiting for ΔTmin2 data...')
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setStyleSheet("font-weight: bold")
				msg.setStyleSheet("text-align:center")
				msg.setText(
					"The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT TWO} value and try again.")
				msg.setWindowTitle("Error")
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()
				return 0
		except:
			pass
		contador=0
		tf2,tq2,uq2, uf2,_ = pontopinch(correntes, len(correntes), float(dlg.DTMIN2.text()))
		uf2, uq2,_,_ = fp2.pontopinch(correntes, len(correntes), float(dlg.DTMIN2.text()))
		for i in range(0,len(ccopi)):
			if ccopi[i][3]=='Cold':
				ccopi[i][2]=uf2/(ccopi[i][1]-ccopi[i][0])
				correntecomp.append(ccopi[i])
				contador+=1
			else:
				ccopi[i][2] = uq2 / (ccopi[i][0] - ccopi[i][1])
				correntecomp.append(ccopi[i])
				contador+=1

		_,_,datagraph,_,_,_,_  = tt.CUSTO(correntecomp, len(correntecomp))
		for i in range(0,contador):
			correntecomp.pop()
		cc2(datagraph,float(dlg.DTMIN2.text()),round(tf2,6),round(tq2,6))

		dlg.graficodt2.setPixmap(QtGui.QPixmap("cc2.png"))

	except:
		dlg.graficodt2.setText('Waiting for ΔTmin2 data...')

def GC():
	try:
		dlg.labe1.hide()
		dlg.scrola1.hide()
		dlg.horizontalLayout_37.removeWidget(dlg.scrola1)
		dlg.graficodt1.show()
		dlg.graficodt2.show()
		dlg.linicio.show()
		dlg.lmeio.show()
		dlg.lfim.show()
	except:
		print("1")
		pass
	try:
		dlg.labe2.hide()
		dlg.scrola2.hide()
		dlg.horizontalLayout_37.removeWidget(dlg.scrola2)
		dlg.graficodt1.show()
		dlg.graficodt2.show()
		dlg.linicio.show()
		dlg.lmeio.show()
		dlg.lfim.show()
	except:
		print("2")
		pass

	try:
		asch = dlg.DTMIN1.text()
		asch = asch.split(".")
		try:
			if len(asch[1]) > 4:
				dlg.graficodt1.setText('Waiting for ΔTmin1 data...')
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setStyleSheet("font-weight: bold")
				msg.setStyleSheet("text-align:center")
				msg.setText(
					"The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT ONE} value and try again.")
				msg.setWindowTitle("Error")
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()
				return 0
		except:
			print("3")
		_, _, _, _, coisas_graficos1 = pontopinch(correntes, len(correntes), float(dlg.DTMIN1.text()))
		Gc1(len(correntes),dlg,coisas_graficos1[0],coisas_graficos1[7],coisas_graficos1[5],unidadeusada)
	except:
		print("4")
		dlg.graficodt1.setText('Waiting for ΔTmin1 data...')
	try:
		asch = dlg.DTMIN2.text()
		asch = asch.split(".")
		try:
			if len(asch[1]) > 4:
				dlg.graficodt2.setText('Waiting for ΔTmin2 data...')
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setStyleSheet("font-weight: bold")
				msg.setStyleSheet("text-align:center")
				msg.setText(
					"The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT TWO} value and try again.")
				msg.setWindowTitle("Error")
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()
				return 0
		except:
			print("5")
		_, _, _, _, coisas_graficos2 = pontopinch(correntes, len(correntes), float(dlg.DTMIN2.text()))
		Gc2(len(correntes),dlg,coisas_graficos2[0],coisas_graficos2[7],coisas_graficos2[5],unidadeusada)
	except:
		print("6")
		dlg.graficodt2.setText('Waiting for ΔTmin2 data...')

def savefile():

	contador = 0
	correntecomp4 = correntes
	uf1, uq1, _, _ = fp2.pontopinch(correntes, len(correntes), float(dlg.lineEdit_2.text()))

	for i in range(0, len(ccopi)):
		if ccopi[i][3] == 'Cold':
			ccopi[i][2] = uf1 / (ccopi[i][1] - ccopi[i][0])
			correntecomp4.append(ccopi[i])
			contador += 1
		else:
			ccopi[i][2] = uq1 / (ccopi[i][0] - ccopi[i][1])
			correntecomp4.append(ccopi[i])

			contador += 1

	akt, _, ajustado, cpf, cpq, areak, deltalmnk = tt.CUSTO(correntecomp4, len(correntecomp4))
	for i in range(0, contador):
		correntecomp4.pop()
	export(correntes,ccopi, variadt, yplot, custoopano, custocapital, custocapitalanual, custototanual,uf,uq,float(dlg.lineEdit_2.text()),akt, ajustado, cpf, cpq, areak, deltalmnk)

def CASCA():

	try:
		dlg.labe1.hide()
		dlg.scrola1.hide()
		dlg.horizontalLayout_37.removeWidget(dlg.scrola1)
	except:
		None
	try:
		dlg.labe2.hide()
		dlg.scrola2.hide()
		dlg.horizontalLayout_37.removeWidget(dlg.scrola2)
	except:
		None

	dlg.labe1=QLabel()
	dlg.labe2=QLabel()
	dlg.graficodt1.hide()
	dlg.graficodt2.hide()
	dlg.linicio.hide()
	dlg.lmeio.hide()
	dlg.lfim.hide()
	try:
		asch = dlg.DTMIN1.text()
		asch = asch.split(".")
		try:
			if len(asch[1]) > 4:
				dlg.linicio.show()
				dlg.graficodt1.show()
				dlg.graficodt1.setText('Waiting for ΔTmin1 data...')  #
				dlg.lmeio.show()
				dlg.lfim.show()
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setStyleSheet("font-weight: bold")
				msg.setStyleSheet("text-align:center")
				msg.setText(
					"The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT ONE} value and try again.")
				msg.setWindowTitle("Error")
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()
			else:
				try:
					cascata(correntes, float(dlg.DTMIN1.text()))
					dlg.labe1.setPixmap(QtGui.QPixmap("EC.png"))
					dlg.scrola1 = QScrollArea()
					dlg.scrola1.setBackgroundRole(QPalette.Light)
					dlg.scrola1.setAlignment(Qt.AlignCenter)
					dlg.horizontalLayout_37.insertWidget(1, dlg.scrola1)
					dlg.scrola1.setWidget(dlg.labe1)
				except:
					pass
		except:
			cascata(correntes, float(dlg.DTMIN1.text()))
			dlg.labe1.setPixmap(QtGui.QPixmap("EC.png"))
			dlg.scrola1 = QScrollArea()
			dlg.scrola1.setBackgroundRole(QPalette.Light)
			dlg.scrola1.setAlignment(Qt.AlignCenter)
			dlg.horizontalLayout_37.insertWidget(1, dlg.scrola1)
			dlg.scrola1.setWidget(dlg.labe1)

	except:
		dlg.linicio.show()
		dlg.graficodt1.show()
		dlg.graficodt1.setText('Waiting for ΔTmin1 data...') #
		dlg.lmeio.show()
		dlg.lfim.show()
	try:
		asch = dlg.DTMIN2.text()
		asch = asch.split(".")
		try:
			if len(asch[1]) > 4:
				dlg.graficodt2.show()
				dlg.graficodt2.setText('Waiting for ΔTmin2 data...')
				dlg.lfim.show()
				dlg.lmeio.show()
				msg = QMessageBox()
				msg.setIcon(QMessageBox.Warning)
				msg.setStyleSheet("font-weight: bold")
				msg.setStyleSheet("text-align:center")
				msg.setText(
					"The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT TWO} value and try again.")
				msg.setWindowTitle("Error")
				msg.setStandardButtons(QMessageBox.Ok)
				msg.exec_()
				dlg.linicio.show()
			else:
				try:
					cascata2(correntes, float(dlg.DTMIN2.text()))
					dlg.labe2.setPixmap(QtGui.QPixmap("EC2.png"))
					dlg.scrola2 = QScrollArea()
					dlg.scrola2.setBackgroundRole(QPalette.Light)
					dlg.scrola2.setAlignment(Qt.AlignCenter)
					dlg.horizontalLayout_37.insertWidget(3, dlg.scrola2)
					dlg.scrola2.setWidget(dlg.labe2)
				except:
					pass

		except:
			cascata2(correntes, float(dlg.DTMIN2.text()))
			dlg.labe2.setPixmap(QtGui.QPixmap("EC2.png"))
			dlg.scrola2 = QScrollArea()
			dlg.scrola2.setBackgroundRole(QPalette.Light)
			dlg.scrola2.setAlignment(Qt.AlignCenter)
			dlg.horizontalLayout_37.insertWidget(3,dlg.scrola2)
			dlg.scrola2.setWidget(dlg.labe2)
	except:
		dlg.linicio.show()

		dlg.graficodt2.show()
		dlg.graficodt2.setText('Waiting for ΔTmin2 data...')
		dlg.lfim.show()
		dlg.lmeio.show()

def caxa():
	asch=dlg.DTMIN1.text()
	asch = asch.split(".")
	try:
		if len(asch[1])>4:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setStyleSheet("font-weight: bold")
			msg.setStyleSheet("text-align:center")
			msg.setText("The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT ONE} value and try again.")
			msg.setWindowTitle("Error")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
			return 0
	except:
		pass
	try:

		contador=0
		correntecomp4 = correntes
		uf1, uq1,_,_ = fp2.pontopinch(correntes, len(correntes), float(dlg.DTMIN1.text()))

		for i in range(0,len(ccopi)):
			if ccopi[i][3]=='Cold':
				ccopi[i][2]=uf1/(ccopi[i][1]-ccopi[i][0])
				correntecomp4.append(ccopi[i])
				contador+=1
			else:
				ccopi[i][2] = uq1 / (ccopi[i][0] - ccopi[i][1])
				correntecomp4.append(ccopi[i])

				contador+=1

		akt,_,ajustado,cpf,cpq,areak,deltalmnk = tt.CUSTO(correntecomp4, len(correntecomp4))




		dlg.area = uic.loadUi("Area.ui")
		dlg.area.show()
		dlg.area.label.setText("ΔTmin\N{SUBSCRIPT ONE} :  "+str(round(float(dlg.DTMIN1.text()),5)))
		dlg.area.label.setFont(QFont('Arial', 14))
		dlg.area.label.setStyleSheet("font-weight: bold")
		row = 0
		dlg.area.TABELA.setRowCount(len(areak)+1)

		for data in range(0, len(areak)):
			dlg.area.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data],2))))
			dlg.area.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data + 1],2))))
			dlg.area.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data],2))))
			dlg.area.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data + 1],2))))
			dlg.area.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(round(cpq[data],2))))
			dlg.area.TABELA.setItem(row, 5, QtWidgets.QTableWidgetItem(str(round(cpf[data],2))))
			dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str(round(deltalmnk[data],2))))
			dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round(areak[data],2))))
			row += 1
		dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str('Total Area:')))
		dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round((akt),2))))



			##################acaba aq
		for i in range(0,contador):
			correntecomp4.pop()
	except:
		try:
			f = float(dlg.DTMIN1.text())
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setStyleSheet("font-weight: bold")
			msg.setStyleSheet("text-align:center")
			msg.setText("Please input utility data in 'Streams' tab")
			msg.setWindowTitle("Error")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
		except:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setStyleSheet("font-weight: bold")
			msg.setStyleSheet("text-align:center")
			msg.setText("Please input ΔTmin₁ data")
			msg.setWindowTitle("Error")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()

def caxa2():
	asch=dlg.DTMIN2.text()
	asch = asch.split(".")
	try:
		if len(asch[1])>4:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setStyleSheet("font-weight: bold")
			msg.setStyleSheet("text-align:center")
			msg.setText("The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT TWO} value and try again.")
			msg.setWindowTitle("Error")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
			return 0
	except:
		pass
	try:
		contador = 0
		correntecomp4 = correntes
		uf1, uq1,_,_ = fp2.pontopinch(correntes, len(correntes), float(dlg.DTMIN2.text()))

		for i in range(0, len(ccopi)):
			if ccopi[i][3] == 'Cold':
				ccopi[i][2] = uf1 / (ccopi[i][1] - ccopi[i][0])

				correntecomp4.append(ccopi[i])
				contador += 1
			else:
				ccopi[i][2] = uq1 / (ccopi[i][0] - ccopi[i][1])
				correntecomp4.append(ccopi[i])
				contador += 1

		akt, _, ajustado, cpf, cpq, areak,deltalmnk = tt.CUSTO(correntecomp4, len(correntecomp4))

		dlg.area = uic.loadUi("Area.ui")
		dlg.area.show()
		dlg.area.label.setText("ΔTmin\N{SUBSCRIPT TWO} :  "+str(round(float(dlg.DTMIN2.text()),5)))
		dlg.area.label.setFont(QFont('Arial', 14))
		dlg.area.label.setStyleSheet("font-weight: bold")
		row = 0
		dlg.area.TABELA.setRowCount(len(areak) + 1)

		for data in range(0, len(areak)):
			dlg.area.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data],2))))
			dlg.area.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data + 1],2))))
			dlg.area.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data],2))))
			dlg.area.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data + 1],2))))
			dlg.area.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(round(cpq[data],2))))
			dlg.area.TABELA.setItem(row, 5, QtWidgets.QTableWidgetItem(str(round(cpf[data],2))))
			dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str(round(deltalmnk[data],2))))
			dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round(areak[data],2))))
			row += 1
		dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str('Total Area:')))
		dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round((akt),2))))

		##################acaba aq
		for i in range(0, contador):
			correntecomp4.pop()
	except:
		try:
			f=float(dlg.DTMIN2.text())
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setStyleSheet("font-weight: bold")
			msg.setStyleSheet("text-align:center")
			msg.setText("Please input utility data in 'Streams' tab")
			msg.setWindowTitle("Error")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()
		except:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Warning)
			msg.setStyleSheet("font-weight: bold")
			msg.setStyleSheet("text-align:center")
			msg.setText("Please input ΔTmin₂ data")
			msg.setWindowTitle("Error")
			msg.setStandardButtons(QMessageBox.Ok)
			msg.exec_()

def OPTA():
	contador = 0
	correntecomp4 = correntes
	uf1, uq1,_,_ = fp2.pontopinch(correntes, len(correntes), float(dtopt))
	for i in range(0, len(ccopi)):
		if ccopi[i][3] == 'Cold':
			ccopi[i][2] = uf1 / (ccopi[i][1] - ccopi[i][0])

			correntecomp4.append(ccopi[i])
			contador += 1
		else:
			ccopi[i][2] = uq1 / (ccopi[i][0] - ccopi[i][1])
			correntecomp4.append(ccopi[i])
			contador += 1

	akt, _, ajustado, cpf, cpq, areak,deltalmnk = tt.CUSTO(correntecomp4, len(correntecomp4))

	dlg.area = uic.loadUi("Area.ui")
	dlg.area.show()
	dlg.area.label.setText("Optimized ΔTmin:  " + str(round(dtopt,5)))
	dlg.area.label.setFont(QFont('Arial', 14))
	dlg.area.label.setStyleSheet("font-weight: bold")
	row = 0
	dlg.area.TABELA.setRowCount(len(areak) + 1)

	for data in range(0, len(areak)):
		dlg.area.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data],2))))
		dlg.area.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data + 1],2))))
		dlg.area.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data],2))))
		dlg.area.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data + 1],2))))
		dlg.area.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(round(cpq[data],2))))
		dlg.area.TABELA.setItem(row, 5, QtWidgets.QTableWidgetItem(str(round(cpf[data],2))))
		dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str(round(deltalmnk[data],2))))
		dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round(areak[data],2))))
		row += 1
	dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str('Total Area:')))
	dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round((akt),2))))

		##################acaba aq
	for i in range(0, contador):
		correntecomp4.pop()

kct=uic.loadUi("Select.ui")
dlg.TABELA.setColumnWidth(3,150)
#custos
dlg.CASCA.clicked.connect(lambda: CASCA())
dlg.otimizabotao.clicked.connect(lambda: eq())
kct.otimizarun.clicked.connect(lambda: otimizafun())
dlg.botaocurva.clicked.connect(lambda: plotgraficocurva())
dlg.botaocurvac.clicked.connect(lambda: plotgraficocurvacomp())
dlg.GC.clicked.connect(lambda: GC())
dlg.CUSTO.clicked.connect(lambda: mostra3())
dlg.UT.clicked.connect(lambda: mostra2())
dlg.OPTA.clicked.connect(lambda: OPTA())
dlg.AREA.clicked.connect(lambda: mostra1())
dlg.ESTIMA.clicked.connect(lambda: caxa())
dlg.ESTIMA2.clicked.connect(lambda: caxa2())
dlg.actionSave_File.triggered.connect(savefile)
########################



#inputs e coisas com eles
def openfile_teste(pergunta=True):
	global n, nhot, ncold, correntes

	#le o excel
	dlg.tableWidget.blockSignals(True)
	Tk().withdraw()
	if pergunta:
		filename = askopenfilename()
		workbook = xlrd.open_workbook(filename)
	else:
		workbook = xlrd.open_workbook("9 correntes - 20 dtmin.xls")

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
			item.setTextAlignment(Qt.AlignCenter)

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
		item.setTextAlignment(Qt.AlignCenter)

	correntes.append(dados_da_corrente)
	e_utilidade.append(False)

	dlg.tableWidget.blockSignals(False)

def add_utilidade():
	global n, n_util, ncold, nhot, correntes_util
	dlg.donebutton.setEnabled(False)
	dlg.botao_addstream.setEnabled(False)
	dlg.remover_corrente.setEnabled(False)
	# n += 1
	n_util += 1
	dados_da_corrente = []

	if float(dlg.util_inlet.text().replace(",", ".")) < float(dlg.util_outlet.text().replace(",", ".")):
		tipo = "Cold"
	else:
		tipo = "Hot"

	if len(correntes_util) > 0:
		if correntes_util[0][3] == tipo:
			if tipo == "Hot":
				QMessageBox.about(dlg, "Error!", "There's already a hot utility. You must input a cold one.")
			else:
				QMessageBox.about(dlg, "Error!", "There's already a cold utility. You must input a hot one.")
			n_util -= 1
			return

	dados_da_corrente.append(float(dlg.util_inlet.text().replace(",", ".")))
	dados_da_corrente.append(float(dlg.util_outlet.text().replace(",", ".")))
	dados_da_corrente.append(1)
	dados_da_corrente.append(tipo)
	dados_da_corrente.append(float(dlg.util_pelicula.text().replace(",", ".")))

	if dlg.utilidade.text() == "":
		texto = "Utility " + str(n_util)
	else:
		texto = dlg.utilidade.text()

	dlg.tableWidget_5.blockSignals(True)
	dlg.tableWidget_5.setRowCount(n_util)
	dlg.tableWidget_5.setItem(n_util-1, 0, QTableWidgetItem(texto))
	dlg.tableWidget_5.setItem(n_util-1, 1, QTableWidgetItem(str(dados_da_corrente[0])))
	dlg.tableWidget_5.setItem(n_util-1, 2, QTableWidgetItem(str(dados_da_corrente[1])))
	dlg.tableWidget_5.setItem(n_util-1, 3, QTableWidgetItem(dados_da_corrente[3]))
	dlg.tableWidget_5.setItem(n_util-1, 4, QTableWidgetItem(str(dados_da_corrente[4])))

	for i in range(5):
		item = dlg.tableWidget_5.item(n_util-1, i)
		item.setTextAlignment(Qt.AlignCenter)

	correntes_util.append(dados_da_corrente)
	e_utilidade.append(True)

	dlg.tableWidget_5.blockSignals(False)
	if n_util == 2:
		dlg.botao_addutility.setEnabled(False)
		dlg.pinchbutton.setEnabled(True)

def editar_corrente(correntes, tip, tabela):
	global nhot, ncold, ja_mostrou

	try:
		linha = tabela.currentItem().row()
		coluna = tabela.currentItem().column()
		coluna_comp = coluna - tip
		dado = tabela.currentItem().text()

		if coluna == 3 and dado != "Hot" and dado != "Cold":
			QMessageBox.about(dlg, "Error!", "Not allowed to change this column. Change the temperatures instead.")
			tabela.setItem(linha, coluna, QTableWidgetItem(correntes[linha][coluna]))
			tabela.currentItem().setTextAlignment(Qt.AlignCenter)
			return
		elif coluna != 3:
			correntes[linha][coluna_comp] = float(dado.replace(",", "."))

		tipo = QTableWidgetItem(correntes[linha][3])
		if coluna_comp == 0 or coluna_comp == 1:
			if correntes[linha][0] >= correntes[linha][1]:
				correntes[linha][3] = "Hot"
				tabela.setItem(linha, 3, tipo)
			else:
				correntes[linha][3] = "Cold"
				tabela.setItem(linha, 3, tipo)
			tabela.item(linha, 3).setTextAlignment(Qt.AlignCenter)

		if correntes_util[0][3] != correntes_util[1][3]:
			dlg.pinchbutton.setEnabled(True)
	except:
		pass

def remover_corrente(corrente, tabela, tipo):
	global correntes, correntes_util, n_util, ncold, nhot, n

	if corrente == -1:
		QMessageBox.about(dlg, "Error!", "Select the line of the Stream that you want to remove")
		return

	if tipo == "corrente":
		n -= 1
		if correntes[corrente][3] == "Hot":
			nhot -= 1
		elif correntes[corrente][3] == "Cold":
			ncold -= 1
		correntes.pop(corrente)
	elif tipo == "utilidade":
		n_util -= 1
		correntes_util.pop(corrente)
		dlg.botao_addutility.setEnabled(True)

	tabela.removeRow(corrente)

def done_teste(libera=False):
	global dTmin, done, correntes
	lista_cps = []

	for corrente in correntes:
		lista_cps.append(corrente[2])

	# novos_cps = unidades_compativeis(dlg.temp_unidade.currentIndex(), dlg.cp_unidade.currentIndex(), dlg.pelicula_unidade.currentIndex(), lista_cps)
	#
	# for i in range(len(correntes)):
	# 	correntes[i][2] = round(novos_cps[i], 3)

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

	def liberar_utilidades(libera):
		dlg.botao_addutility.setEnabled(True)
		dlg.remover_utilidade.setEnabled(True)
		dlg.utilidade.setEnabled(True)
		dlg.util_inlet.setEnabled(True)
		dlg.util_outlet.setEnabled(True)
		dlg.util_pelicula.setEnabled(True)
		dlg.donebutton.setEnabled(False)
		dlg.botao_addstream.setEnabled(False)
		dlg.remover_corrente.setEnabled(False)
		dlg.done.close()
		if libera:
			correntes_util.append([300, 299, 1, "Hot", 0.5])
			correntes_util.append([10, 20, 1, "Cold", 0.5])
			correntes_util.append([10, 20, 1, "Cold", 0.5])
			correntes_util.append([10, 20, 1, "Cold", 0.5])
			e_utilidade.append(True)
			e_utilidade.append(True)
			e_utilidade.append(True)
			e_utilidade.append(True)

	def pinch_sem_util():
		pinch_teste()
		dlg.done.close()

	if libera:
		liberar_utilidades(libera)
	dlg.done.cancelar.clicked.connect(cancelar)
	dlg.done.escolher_utilidades.clicked.connect(liberar_utilidades)
	dlg.done.pinch_sem_utilidades.clicked.connect(pinch_sem_util)

def pinch_teste():
	global done, Th0, Thf, CPh, Tc0, Tcf, CPc, Thf_acima, Th0_abaixo, Tc0_acima, Tcf_abaixo
	Th0, Thf, CPh, Tc0, Tcf, CPc, Thf_acima, Th0_abaixo, Tc0_acima, Tcf_abaixo = [], [], [], [], [], [], [], [], [], []
	if done:
		global correntes, correntes_util, dTmin, pinchf, pinchq, n, util_quente, util_fria, nhot, ncold

		if len(correntes_util) != 0:
			if correntes_util[0][3] == correntes_util[1][3]:
				QMessageBox.about(dlg, "Error!", "You won't be able to sinthetize the Heat Exchange Network with two " + correntes_util[0][3] + " utilities. Edit any of these to make sure you have the both types.")
				dlg.pinchbutton.setEnabled(False)
				return
			else:
				dlg.pinchbutton.setEnabled(True)


		pinchf, pinchq, util_quente, util_fria, a = pontopinch(correntes, n, dTmin)
		for util in correntes_util:
			if util[3] == "Hot":
				util[2] = util_quente/(util[0] - util[1])
				nhot += 1
			else:
				util[2] = util_fria/(util[1] - util[0])
				ncold += 1
		if len(correntes_util) == 4:
			correntes_util[1][2] = correntes_util[1][2] * 0.72185186976924193314304968313096
			correntes_util[2][2] = correntes_util[2][2] * 0.10981568380823375743795655749601
			correntes_util[3][2] = correntes_util[3][2] * 0.16833244642252430941899375937303

		ccopi = nao_sacrificar_matriz(correntes_util)
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

		global unidades_usadas, desenho_em_dia, desenho_em_dia_abaixo, desenho_em_dia_ambas
		calor = dlg.cp_unidade.currentText().split("/")
		unidades_usadas = [dlg.temp_unidade.currentText(), dlg.cp_unidade.currentText(), calor[0]]

		header = dlg.tableWidget_2.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
		for i in range(11):
			header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
		header = dlg.tableWidget_14.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
		for i in range(5):
			header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

		#manda tudo pro backend
		receber_pinch(Th0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, Thf_acima, Tc0_acima)
		receber_pinch_abaixo(Thf, Tc0, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, Th0_abaixo, Tcf_abaixo)
		printar()
		printar_abaixo()
		correntesnoscombos(nhot,ncold)
		testar_correntes(dlg, True)
		testar_correntes_abaixo(dlg)
		desenhar_rede(correntes_quentes, correntes_frias, "acima", True)
		desenhar_rede(correntes_quentes, correntes_frias, "abaixo", True)
		desenho_em_dia = desenho_em_dia_abaixo = desenho_em_dia_ambas = False

		#libera botões e coisas
		dlg.tabWidget.setTabEnabled(1,True)
		dlg.tabWidget.setTabEnabled(2,True)
		dlg.tabWidget.setTabEnabled(3,True)
		dlg.tabWidget.setTabEnabled(4,True)
		dlg.tabWidget.setCurrentIndex(2)
		dlg.pinchbutton.setEnabled(False)
		dlg.botao_addstream.setEnabled(False)
		dlg.botao_addutility.setEnabled(False)
		dlg.remover_utilidade.setEnabled(False)
		dlg.remover_corrente.setEnabled(False)
		dlg.donebutton.setEnabled(False)

def correntesnoscombos(nhot,ncold):
	for i in range(nhot):
		dlg.comboBox_9.addItem(str(i+1)) #acima   quadro de correntes quentes
		dlg.comboBox_35.addItem(str(i+1))   #abaixo   add heat ex
		dlg.comboBox_43.addItem(str(i+1))#abaixo   quadro de correntes quentes
		dlg.comboBox_51.addItem(str(i+1))	#n max de sub frias é o número de correntes quentes
		dlg.comboBox_54.addItem(str(i+1))
		dlg.corrente_abaixo.addItem("Hot " + str(i+1))
		if not e_utilidade_quente[i]:
			dlg.comboutil.addItem("Hot " + str(i+1))
			dlg.comboBox_2.addItem(str(i+1))
		else:
			dlg.comboBox_2.addItem(str(i+1) + " (utility)")
	for i in range(ncold):
		dlg.comboBox_10.addItem(str(i+1)) #acima quadro correntes frias
		dlg.comboBox_5.addItem(str(i+1)) #acima add heat ex
		dlg.comboBox_44.addItem(str(i+1)) #abaixo quadro de correntes frias
		dlg.comboBox_50.addItem(str(i+1)) #n max de sub quentes é o nomero de correntes frias
		dlg.comboBox_53.addItem(str(i+1))
		dlg.corrente_acima.addItem("Cold " + str(i+1))
		if not e_utilidade_fria[i]:
			dlg.comboBox_36.addItem(str(i+1))
			dlg.comboutil.addItem("Cold " + str(i+1))
		else:
			dlg.comboBox_36.addItem(str(i+1) + " (utility)")

	for i in range(1, min(nhot, ncold)):
		dlg.nivel.addItem(str(i+1))

def unidades(header=True, corrente=True):
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
			if corrente:
				dlg.temp_unidade_util.setCurrentIndex(dlg.temp_unidade.currentIndex())
				dlg.pelicula_unidade_util.setCurrentIndex(dlg.pelicula_unidade.currentIndex())


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




#desenhos
def desenhar_rede(correntes_quentes, correntes_frias, subrede, teste=False):

	def criar_turtle():
		nome = turtle.Turtle()
		nome.speed(1000)
		nome.hideturtle()
		nome.penup()
		return nome

	def quentes(onde, correntes_desenho, presente):
		global y_acima, y_abaixo
		ja_cp = False
		for i in range(len(correntes_desenho)):

			if onde == "above":
				ident.sety(y_acima - h_string)
				ident.setx(distancia_x/2 + distancia_cp/2)
				alinha = "left"
			elif onde == "below":
				ident.sety(y_abaixo - h_string)
				ident.setx(-distancia_x/2 - distancia_cp/2)
				alinha = "right"
			elif onde == "ambas":
				ident.sety(y_acima - h_string)
				ident.setx(distancia_x/2 + distancia_cp)
				alinha = "left"
			if e_utilidade_quente[i]:
				if onde == "below":
					ident.write("(utility) Hot " + str(i+1), align=alinha, font=("Arial", fonte_carga, "bold"))
				else:
					ident.write("Hot " + str(i+1) + " (utility)", align=alinha, font=("Arial", fonte_carga, "bold"))
			else:
				ident.write("Hot " + str(i+1), align=alinha, font=("Arial", fonte_carga, "bold"))

			if presente[i] and onde != "ambas":
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].speed(1000)
				correntes_desenho[i].shapesize(seta, seta, seta)
				if e_utilidade_quente[i]:
					correntes_desenho[i].color("orange")
				else:
					correntes_desenho[i].color("red")
				correntes_desenho[i].pensize(grossura_corrente)
				correntes_desenho[i].penup()
				correntes_desenho_sub_acima = [0] * nhot
				correntes_desenho_sub_abaixo = [0] * nhot

				if onde == "above":
					correntes_desenho[i].setx(-distancia_x/2)
					correntes_desenho[i].sety(y_acima)
					correntes_desenho[i].pendown()
					if not ja_cp:
						temp.sety(y_acima - h_string + ramo_y)
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
						temp.write("Streams CP ({})".format(unidades_usadas[1]), align="center", font=("Arial", fonte_carga, "bold"))
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
						temp.write("Streams Duty ({})".format(unidades_usadas[2]), align="center", font=("Arial", fonte_carga, "bold"))
						ja_cp = True
					temp.sety(y_acima - h_string)
					temp.setx(-distancia_x/2 - len(str('{:.2f}'.format(round(Th0[i], 2))))*tamanho_string)
					temp.write(str('{:.2f}'.format(round(Th0[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if Thf_acima[i] != pinchq:
						temp.setx(distancia_x/2 - nao_toca_pinch + 5)
						temp.write(str('{:.2f}'.format(round(Thf_acima[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if not dividida_quente[i]:
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
						temp.write(str('{:.2f}'.format(round(CPh[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_quente[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					else:
						correntes_desenho_sub_acima[i] = [0] * (quantidade_quente[i] - 1)
						for j in range(quantidade_quente[i]-1):
							temp.sety(y_acima - h_string)
							temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
							temp.write(str('{:.2f}'.format(round(CPh[i]*fracoes_quentes[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
							temp.write(str('{:.2f}'.format(round(calor_atual_quente_sub[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							correntes_desenho_sub_acima[i][j] = turtle.Turtle()
							if e_utilidade_quente[i]:
								correntes_desenho_sub_acima[i][j].color("orange")
							else:
								correntes_desenho_sub_acima[i][j].color("red")
							correntes_desenho_sub_acima[i][j].pensize(grossura_corrente)
							correntes_desenho_sub_acima[i][j].hideturtle()
							correntes_desenho_sub_acima[i][j].penup()
							correntes_desenho_sub_acima[i][j].setx(-distancia_x/2 + ramo_x)
							correntes_desenho_sub_acima[i][j].sety(y_acima)
							correntes_desenho_sub_acima[i][j].pendown()
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(ramo_y)
							correntes_desenho_sub_acima[i][j].left(90)
							if Thf_acima[i] == pinchq:
								correntes_desenho_sub_acima[i][j].forward(distancia_x - 2*ramo_x)
							else:
								correntes_desenho_sub_acima[i][j].forward(distancia_x - nao_toca_pinch - 2*ramo_x)
							correntes_desenho_sub_acima[i][j].left(90)
							correntes_desenho_sub_acima[i][j].forward(ramo_y*(j+1))
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(ramo_x)
							y_acima -= ramo_y
						temp.sety(y_acima - h_string)
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
						temp.write(str('{:.2f}'.format(round(CPh[i]*fracoes_quentes[i][quantidade_quente[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_quente_sub[i][quantidade_quente[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					if Thf_acima[i] == pinchq:
						correntes_desenho[i].forward(distancia_x)
					else:
						correntes_desenho[i].forward(distancia_x - nao_toca_pinch)

				elif onde == "below":
					correntes_desenho[i].sety(y_abaixo)
					if not ja_cp:
						temp.sety(y_abaixo - h_string + ramo_y)
						temp.setx(distancia_x/2 + distancia_cp + maior_cp)
						temp.write("Streams CP ({})".format(unidades_usadas[1]), align="center", font=("Arial", fonte_carga, "bold"))
						temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
						temp.write("Streams Duty ({})".format(unidades_usadas[2]), align="center", font=("Arial", fonte_carga, "bold"))
						ja_cp = True
					temp.sety(y_abaixo - h_string)
					temp.setx(distancia_x/2 + 6)
					temp.write(str('{:.2f}'.format(round(Thf[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if Th0_abaixo[i] != pinchq:
						temp.setx(-distancia_x/2 + nao_toca_pinch - len(str('{:.2f}'.format(round(Th0[i], 2))))*tamanho_string)
						temp.write(str('{:.2f}'.format(round(Th0_abaixo[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if not dividida_quente_abaixo[i]:
						temp.setx(distancia_x/2 + distancia_cp + maior_cp)
						temp.write(str('{:.2f}'.format(round(CPh[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_quente_abaixo[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					else:
						correntes_desenho_sub_abaixo[i] = [0] * (quantidade_quente_abaixo[i] - 1)
						for j in range(quantidade_quente_abaixo[i]-1):
							temp.sety(y_abaixo - h_string)
							temp.setx(distancia_x/2 + distancia_cp + maior_cp)
							temp.write(str('{:.2f}'.format(round(CPh[i]*fracoes_quentes_abaixo[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
							temp.write(str('{:.2f}'.format(round(calor_atual_quente_sub_abaixo[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
							correntes_desenho_sub_abaixo[i][j].color("red")
							correntes_desenho_sub_abaixo[i][j].pensize(grossura_corrente)
							correntes_desenho_sub_abaixo[i][j].hideturtle()
							correntes_desenho_sub_abaixo[i][j].penup()
							correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
							if Th0_abaixo[i] == pinchq:
								correntes_desenho_sub_abaixo[i][j].setx(-distancia_x/2 + ramo_x)
								correntes_desenho_sub_abaixo[i][j].pendown()
								correntes_desenho_sub_abaixo[i][j].right(90)
								correntes_desenho_sub_abaixo[i][j].forward(ramo_y)
								correntes_desenho_sub_abaixo[i][j].left(90)
								if fechar_corrente_abaixo[i]:
									correntes_desenho_sub_abaixo[i][j].forward((len(matriz_trocadores_abaixo)+0.5)*espaco_trocadores)
									temperatura.sety(y_abaixo + 1)
									temperatura.setx(-distancia_x/2 + (len(matriz_trocadores_abaixo)+1)*espaco_trocadores)
									temperatura.write(str('{:.2f}'.format(round(temp_misturador_abaixo[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
								else:
									correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 2*ramo_x)
							else:
								correntes_desenho_sub_abaixo[i][j].setx(-distancia_x/2 + nao_toca_pinch + ramo_x)
								correntes_desenho_sub_abaixo[i][j].pendown()
								correntes_desenho_sub_abaixo[i][j].right(90)
								correntes_desenho_sub_abaixo[i][j].forward(ramo_y)
								correntes_desenho_sub_abaixo[i][j].left(90)
								if fechar_corrente_abaixo[i]:
									correntes_desenho_sub_abaixo[i][j].forward((len(matriz_trocadores_abaixo)+0.5)*espaco_trocadores)
									temperatura.sety(y_abaixo + 1)
									temperatura.setx(-distancia_x/2 + (len(matriz_trocadores_abaixo)+1)*espaco_trocadores)
									temperatura.write(str('{:.2f}'.format(round(temp_misturador_abaixo[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
								else:
									correntes_desenho_sub_abaixo[i][j].forward(distancia_x - nao_toca_pinch - 2*ramo_x)
							correntes_desenho_sub_abaixo[i][j].left(90)
							correntes_desenho_sub_abaixo[i][j].forward(ramo_y*(j+1))
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(ramo_x)
							y_abaixo -= ramo_y
						temp.sety(y_abaixo - h_string)
						temp.setx(distancia_x/2 + distancia_cp + maior_cp)
						temp.write(str('{:.2f}'.format(round(CPh[i]*fracoes_quentes_abaixo[i][quantidade_quente_abaixo[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_quente_sub_abaixo[i][quantidade_quente_abaixo[i-1]], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					if Th0_abaixo[i] == pinchq:
						correntes_desenho[i].setx(-distancia_x/2)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x)
					else:
						correntes_desenho[i].setx(-distancia_x/2+ nao_toca_pinch)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x - nao_toca_pinch)

			if onde != "ambas":
				y_acima -= ramo_y
				y_abaixo -= ramo_y

			if onde == "ambas":
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].speed(1000)
				correntes_desenho[i].shapesize(seta, seta, seta)
				if e_utilidade_quente[i]:
					correntes_desenho[i].color("orange")
				else:
					correntes_desenho[i].color("red")
				correntes_desenho[i].pensize(grossura_corrente)
				correntes_desenho[i].penup()
				correntes_desenho_sub_acima = [0] * nhot
				correntes_desenho_sub_abaixo = [0] * nhot
				correntes_desenho[i].setx(-distancia_x/2)
				correntes_desenho[i].sety(y_acima)
				correntes_desenho[i].pendown()
				if not ja_cp:
					temp.sety(y_acima - h_string + ramo_y)
					temp.setx(-distancia_x/2 - distancia_cp - maior_duty)
					temp.write("Streams Duty ({})".format(unidades_usadas[2]), align="center", font=("Arial", fonte_carga, "bold"))
					ja_cp = True
				temp.sety(y_acima - h_string)
				temp.setx(-distancia_x/2 - distancia_cp - maior_duty)
				temp.write(str('{:.2f}'.format(round(calor_atual_quente_ev[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
				temp.setx(-distancia_x/2 - len(str('{:.2f}'.format(round(Th0[i], 2))))*tamanho_string)
				temp.write(str('{:.2f}'.format(round(Th0[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
				temp.setx(distancia_x/2 + 6)
				temp.write(str('{:.2f}'.format(round(Thf[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
				if dividida_quente_ev_acima[i]:
					correntes_desenho_sub_acima[i] = [0] * (quantidade_quente_ev_acima[i] - 1)
					for j in range(quantidade_quente_ev_acima[i]-1):
						correntes_desenho_sub_acima[i][j] = turtle.Turtle()
						if e_utilidade_quente[i]:
							correntes_desenho_sub_acima[i][j].color("orange")
						else:
							correntes_desenho_sub_acima[i][j].color("red")
						correntes_desenho_sub_acima[i][j].pensize(grossura_corrente)
						correntes_desenho_sub_acima[i][j].hideturtle()
						correntes_desenho_sub_acima[i][j].penup()
						correntes_desenho_sub_acima[i][j].setx(-distancia_x/2 + ramo_x)
						correntes_desenho_sub_acima[i][j].sety(y_acima)
						correntes_desenho_sub_acima[i][j].pendown()
						correntes_desenho_sub_acima[i][j].right(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_y)
						correntes_desenho_sub_acima[i][j].left(90)
						correntes_desenho_sub_acima[i][j].forward(distancia_x/2 - 2*ramo_x)
						correntes_desenho_sub_acima[i][j].left(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_y*(j+1))
						correntes_desenho_sub_acima[i][j].right(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_x)
						y_acima -= ramo_y
					temp.sety(y_acima - h_string)
					temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
				if dividida_quente_ev_abaixo[i]:
					correntes_desenho_sub_abaixo[i] = [0] * (quantidade_quente_ev_abaixo[i] - 1)
					for j in range(quantidade_quente_ev_abaixo[i]-1):
						correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
						correntes_desenho_sub_abaixo[i][j].color("red")
						correntes_desenho_sub_abaixo[i][j].pensize(grossura_corrente)
						correntes_desenho_sub_abaixo[i][j].hideturtle()
						correntes_desenho_sub_abaixo[i][j].penup()
						correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
						correntes_desenho_sub_abaixo[i][j].setx(ramo_x)
						correntes_desenho_sub_abaixo[i][j].pendown()
						correntes_desenho_sub_abaixo[i][j].right(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_y)
						correntes_desenho_sub_abaixo[i][j].left(90)
						if fechar_corrente_abaixo[i]:
							correntes_desenho_sub_abaixo[i][j].forward((len(matriz_trocadores_abaixo)+0.5)*espaco_trocadores)
							temperatura.sety(y_abaixo + 1)
							temperatura.setx((len(matriz_trocadores_abaixo)+1)*espaco_trocadores - 6)
							temperatura.write(str('{:.2f}'.format(round(temp_misturador_quente[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
						else:
							correntes_desenho_sub_abaixo[i][j].forward(distancia_x/2 - 2*ramo_x)
						correntes_desenho_sub_abaixo[i][j].left(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_y*(j+1))
						correntes_desenho_sub_abaixo[i][j].right(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_x)
						y_abaixo -= ramo_y
				correntes_desenho[i].forward(distancia_x)

				y_acima -= ramo_y
				y_abaixo -= ramo_y

				if y_acima < y_abaixo:
					y_abaixo = y_acima
				elif y_acima > y_abaixo:
					y_acima = y_abaixo

	def frias(onde, correntes_desenho, presente):
		global y_acima, y_abaixo
		for i in range(len(correntes_desenho)):

			if onde == "above":
				ident.sety(y_acima - h_string)
				ident.setx(distancia_x/2 + distancia_cp/2)
				alinha = "left"
			elif onde == "below":
				ident.sety(y_abaixo - h_string)
				ident.setx(-distancia_x/2 - distancia_cp/2)
				alinha = "right"
			else:
				ident.sety(y_acima - h_string)
				ident.setx(distancia_x/2 + distancia_cp)
				alinha = "left"
			if e_utilidade_fria[i]:
				if onde == "below":
					ident.write("(utility) Cold " + str(i+1), align=alinha, font=("Arial", fonte_carga, "bold"))
				else:
					ident.write("Cold " + str(i+1) + " (utility)", align=alinha, font=("Arial", fonte_carga, "bold"))
			else:
				ident.write("Cold " + str(i+1), align=alinha, font=("Arial", fonte_carga, "bold"))

			if presente[i] and onde != "ambas":
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].speed(1000)
				correntes_desenho[i].shapesize(seta, seta, seta)
				if e_utilidade_fria[i]:
					correntes_desenho[i].color("#7FFFD4")
				else:
					correntes_desenho[i].color("blue")
				correntes_desenho[i].pensize(grossura_corrente)
				correntes_desenho[i].penup()
				correntes_desenho_sub_acima = [0] * ncold
				correntes_desenho_sub_abaixo = [0] * ncold

				if onde == "above":
					correntes_desenho[i].sety(y_acima)
					correntes_desenho[i].left(180)
					temp.sety(y_acima - h_string)
					temp.setx(-distancia_x/2 - len(str('{:.2f}'.format(round(Tcf[i], 2))))*tamanho_string)
					temp.write(str('{:.2f}'.format(round(Tcf[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if Tc0_acima[i] != pinchf:
						temp.setx(distancia_x/2 - nao_toca_pinch + 5)
						temp.write(str('{:.2f}'.format(round(Tc0_acima[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if not dividida_fria[i]:
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
						temp.write(str('{:.2f}'.format(round(CPc[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_frio[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					else:
						correntes_desenho_sub_acima[i] = [0] * (quantidade_fria[i] - 1)
						for j in range(quantidade_fria[i] - 1):
							temp.sety(y_acima - h_string)
							temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
							temp.write(str('{:.2f}'.format(round(CPc[i]*fracoes_frias[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
							temp.write(str('{:.2f}'.format(round(calor_atual_frio_sub[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							correntes_desenho_sub_acima[i][j] = turtle.Turtle()
							correntes_desenho_sub_acima[i][j].color("blue")
							correntes_desenho_sub_acima[i][j].pensize(grossura_corrente)
							correntes_desenho_sub_acima[i][j].hideturtle()
							correntes_desenho_sub_acima[i][j].penup()
							correntes_desenho_sub_acima[i][j].sety(y_acima)
							if Tc0_acima[i] == pinchf:
								correntes_desenho_sub_acima[i][j].setx(distancia_x/2 - ramo_x)
								correntes_desenho_sub_acima[i][j].pendown()
								correntes_desenho_sub_acima[i][j].right(90)
								correntes_desenho_sub_acima[i][j].forward(ramo_y)
								correntes_desenho_sub_acima[i][j].right(90)
								if fechar_corrente[i]:
									correntes_desenho_sub_acima[i][j].forward((len(matriz_armazenada)+0.5)*espaco_trocadores)
									temperatura.sety(y_acima + 1)
									temperatura.setx(distancia_x/2 - (len(matriz_armazenada)+1)*espaco_trocadores)
									temperatura.write(str('{:.2f}'.format(round(temp_misturador[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
								else:
									correntes_desenho_sub_acima[i][j].forward(distancia_x - 2*ramo_x)
							else:
								correntes_desenho_sub_acima[i][j].setx(distancia_x/2 - nao_toca_pinch - ramo_x)
								correntes_desenho_sub_acima[i][j].pendown()
								correntes_desenho_sub_acima[i][j].right(90)
								correntes_desenho_sub_acima[i][j].forward(ramo_y)
								correntes_desenho_sub_acima[i][j].right(90)
								if fechar_corrente[i]:
									correntes_desenho_sub_acima[i][j].forward((len(matriz_armazenada)+0.5)*espaco_trocadores)
									temperatura.sety(y_acima + 1)
									temperatura.setx(distancia_x/2 - (len(matriz_armazenada)+1)*espaco_trocadores)
									temperatura.write(str('{:.2f}'.format(round(temp_misturador[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
								else:
									correntes_desenho_sub_acima[i][j].forward(distancia_x - nao_toca_pinch - 2*ramo_x)
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(ramo_y*(j+1))
							correntes_desenho_sub_acima[i][j].left(90)
							correntes_desenho_sub_acima[i][j].forward(ramo_x)
							y_acima -= ramo_y
						temp.sety(y_acima - h_string)
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
						temp.write(str('{:.2f}'.format(round(CPc[i]*fracoes_frias[i][quantidade_fria[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_frio_sub[i][quantidade_fria[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					if Tc0_acima[i] == pinchf:
						correntes_desenho[i].setx(distancia_x/2)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x)
					else:
						correntes_desenho[i].setx(distancia_x/2 - nao_toca_pinch)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x - nao_toca_pinch)
				elif onde == "below":
					correntes_desenho[i].sety(y_abaixo)
					correntes_desenho[i].left(180)
					correntes_desenho[i].setx(distancia_x/2)
					correntes_desenho[i].pendown()
					temp.sety(y_abaixo - h_string)
					temp.setx(distancia_x/2 + 6)
					temp.write(str('{:.2f}'.format(round(Tc0[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if Tcf_abaixo[i] != pinchf:
						temp.setx(-distancia_x/2 + nao_toca_pinch - len(str('{:.2f}'.format(round(Tcf_abaixo[i], 2))))*tamanho_string)
						temp.write(str('{:.2f}'.format(round(Tcf_abaixo[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if not dividida_fria_abaixo[i]:
						temp.setx(distancia_x/2 + distancia_cp + maior_cp)
						temp.write(str('{:.2f}'.format(round(CPc[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_frio_abaixo[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					else:
						correntes_desenho_sub_abaixo[i] = [0] * (quantidade_fria_abaixo[i] - 1)
						for j in range(quantidade_fria_abaixo[i]-1):
							temp.sety(y_abaixo - h_string)
							temp.setx(distancia_x/2 + distancia_cp + maior_cp)
							temp.write(str('{:.2f}'.format(round(CPc[i]*fracoes_frias_abaixo[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
							temp.write(str('{:.2f}'.format(round(calor_atual_frio_sub_abaixo[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
							if e_utilidade_fria[i]:
								correntes_desenho_sub_abaixo[i][j].color("#7FFFD4")
							else:
								correntes_desenho_sub_abaixo[i][j].color("blue")
							correntes_desenho_sub_abaixo[i][j].pensize(grossura_corrente)
							correntes_desenho_sub_abaixo[i][j].hideturtle()
							correntes_desenho_sub_abaixo[i][j].penup()
							correntes_desenho_sub_abaixo[i][j].setx(distancia_x/2 - ramo_x)
							correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
							correntes_desenho_sub_abaixo[i][j].pendown()
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(ramo_y)
							correntes_desenho_sub_abaixo[i][j].right(90)
							if Tcf_abaixo[i] == pinchf:
								correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 2*ramo_x)
							else:
								correntes_desenho_sub_abaixo[i][j].forward(distancia_x - nao_toca_pinch - 2*ramo_x)
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(ramo_y*(j+1))
							correntes_desenho_sub_abaixo[i][j].left(90)
							correntes_desenho_sub_abaixo[i][j].forward(ramo_x)
							y_abaixo -= ramo_y
						temp.sety(y_abaixo - h_string)
						temp.setx(distancia_x/2 + distancia_cp + maior_cp)
						temp.write(str('{:.2f}'.format(round(CPc[i]*fracoes_frias_abaixo[i][quantidade_fria_abaixo[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_frio_sub_abaixo[i][quantidade_fria_abaixo[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					if Tcf_abaixo[i] == pinchf:
						correntes_desenho[i].forward(distancia_x)
					else:
						correntes_desenho[i].forward(distancia_x - nao_toca_pinch)

			if onde != "ambas":
				y_acima -= ramo_y
				y_abaixo -= ramo_y

			if onde == "ambas":
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].speed(1000)
				correntes_desenho[i].shapesize(seta, seta, seta)
				if e_utilidade_fria[i]:
					correntes_desenho[i].color("#7FFFD4")
				else:
					correntes_desenho[i].color("blue")
				correntes_desenho[i].pensize(grossura_corrente)
				correntes_desenho[i].penup()
				correntes_desenho_sub_acima = [0] * ncold
				correntes_desenho_sub_abaixo = [0] * ncold
				correntes_desenho[i].sety(y_acima)
				correntes_desenho[i].left(180)
				temp.sety(y_acima - h_string)
				temp.setx(-distancia_x/2 - distancia_cp - maior_duty)
				temp.write(str('{:.2f}'.format(round(calor_atual_frio_ev[i]))), align="center", font=("Arial", fonte_carga, "normal"))
				temp.setx(-distancia_x/2 - len(str('{:.2f}'.format(round(Tcf[i], 2))))*tamanho_string)
				temp.write(str('{:.2f}'.format(round(Tcf[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
				temp.setx(distancia_x/2 + 6)
				temp.write(str('{:.2f}'.format(round(Tc0[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
				if dividida_fria_ev_acima[i]:
					correntes_desenho_sub_acima[i] = [0] * (quantidade_fria_ev_acima[i] - 1)
					for j in range(quantidade_fria_ev_acima[i] - 1):
						correntes_desenho_sub_acima[i][j] = turtle.Turtle()
						correntes_desenho_sub_acima[i][j].color("blue")
						correntes_desenho_sub_acima[i][j].pensize(grossura_corrente)
						correntes_desenho_sub_acima[i][j].hideturtle()
						correntes_desenho_sub_acima[i][j].penup()
						correntes_desenho_sub_acima[i][j].sety(y_acima)
						correntes_desenho_sub_acima[i][j].setx(-ramo_x)
						correntes_desenho_sub_acima[i][j].pendown()
						correntes_desenho_sub_acima[i][j].right(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_y)
						correntes_desenho_sub_acima[i][j].right(90)
						if fechar_corrente_ev[i]:
							correntes_desenho_sub_acima[i][j].forward((len(matriz_armazenada)+0.5)*espaco_trocadores)
							temperatura.sety(y_acima + 1)
							temperatura.setx(-(len(matriz_armazenada)+1)*espaco_trocadores + 6)
							temperatura.write(str('{:.2f}'.format(round(temp_misturador_frio[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
						else:
							correntes_desenho_sub_acima[i][j].forward(distancia_x/2 - 2*ramo_x)
						correntes_desenho_sub_acima[i][j].right(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_y*(j+1))
						correntes_desenho_sub_acima[i][j].left(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_x)
						y_acima -= ramo_y
				if dividida_fria_ev_abaixo[i]:
					correntes_desenho_sub_abaixo[i] = [0] * (quantidade_fria_ev_abaixo[i] - 1)
					for j in range(quantidade_fria_ev_abaixo[i]-1):
						correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
						if e_utilidade_fria[i]:
							correntes_desenho_sub_abaixo[i][j].color("#7FFFD4")
						else:
							correntes_desenho_sub_abaixo[i][j].color("blue")
						correntes_desenho_sub_abaixo[i][j].pensize(grossura_corrente)
						correntes_desenho_sub_abaixo[i][j].hideturtle()
						correntes_desenho_sub_abaixo[i][j].penup()
						correntes_desenho_sub_abaixo[i][j].setx(distancia_x/2 - ramo_x)
						correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
						correntes_desenho_sub_abaixo[i][j].pendown()
						correntes_desenho_sub_abaixo[i][j].right(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_y)
						correntes_desenho_sub_abaixo[i][j].right(90)
						correntes_desenho_sub_abaixo[i][j].forward(distancia_x/2 - 2*ramo_x)
						correntes_desenho_sub_abaixo[i][j].right(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_y*(j+1))
						correntes_desenho_sub_abaixo[i][j].left(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_x)
						y_abaixo -= ramo_y
				correntes_desenho[i].setx(distancia_x/2)
				correntes_desenho[i].pendown()
				correntes_desenho[i].forward(distancia_x)

				y_acima -= ramo_y
				y_abaixo -= ramo_y

				if y_acima < y_abaixo:
					y_abaixo = y_acima
				elif y_acima > y_abaixo:
					y_acima = y_abaixo

	def pinch(tamanho, onde):
		pinch = turtle.Turtle()
		pinch.speed(1000)
		pinch.hideturtle()
		pinch.pensize(grossura_pinch)
		pinch.right(90)
		pinch.penup()
		pinch.sety(comecar_pinch)
		if onde == "acima":
			pinch.setx(distancia_x/2 + 2)
			temp.setx(distancia_x/2 + 2)
		elif onde == "abaixo":
			pinch.setx(-distancia_x/2 - 2)
			temp.setx(-distancia_x/2 - 2)
		temp.sety(comecar_pinch + 5)
		temp.write(str('{:.2f}'.format(round(pinchq, 2))), align="center", font=("Arial", fonte_carga, "normal"))
		temp.right(90)
		tamanho = comecar_pinch - tamanho
		if str(tamanho)[-1] == 5:
			tamanho += 5

		for i in range(int(tamanho/8)+1):
			pinch.pendown()
			pinch.forward(4)
			pinch.penup()
			pinch.forward(4)
			temp.forward(8)
		temp.forward(10)
		temp.write(str('{:.2f}'.format(round(pinchf, 2))), align="center", font=("Arial", fonte_carga, "normal"))

	def inserir_trocador_desenho(onde, corrente_quente, corrente_fria, subestagio, trocadorr, trocador_atual, x, duas_temp, viola, anterior):
		trocador = criar_turtle()
		trocador.pensize(grossura_trocador)

		if e_utilidade_quente[trocadorr[0]-1]:
			trocador.color("black", "orange")
		elif e_utilidade_fria[trocadorr[1]-1]:
			trocador.color("black", "#7FFFD4")
		else:
			trocador.color("black", "white")

		y = 1.5
		"""
		QUANDO AMBAS: segue o sentido da corrente
		QUANDO ACIMA OU ABAIXO: pinch -> fora

		ACIMA
		printa sempre temperaturas da direita (tqout e tfin)
		se precisar printar as duas, ai vai as da esquerda (tqin e tfout)

		ABAIXO
		printa sempre temperaturas da esquerda (tqin e tfout)
		se precisar printa as duas, ai vai as da direita (tqout e tfin)
		"""
		if onde[:5] == "ambas":
			tq_in = trocadorr[7]
			tq_out = trocadorr[9]
			tf_in = trocadorr[10]
			tf_out = trocadorr[8]
			distancia_x = 0
			onde_temperatura_q = onde_temperatura_f_in = raio_trocador + 2
			onde_temperatura_q_in = -raio_trocador - len(str('{:.2f}'.format(round(tq_in,2))))*tamanho_string/y
			onde_temperatura_f = -raio_trocador - len(str('{:.2f}'.format(round(tf_out, 2))))*tamanho_string/y
		else:
			tq_in = trocadorr[9]
			tq_out = trocadorr[7]
			tf_in = trocadorr[10]
			tf_out = trocadorr[8]
			distancia_x = x
			if onde[6:] == "acima":
				onde_temperatura_q = -raio_trocador - len(str('{:.2f}'.format(round(tq_out, 2))))*tamanho_string/y
				onde_temperatura_f = -raio_trocador - len(str('{:.2f}'.format(round(tf_out, 2))))*tamanho_string/y
				onde_temperatura_q_in = onde_temperatura_f_in = raio_trocador + 2
			elif onde[6:] == "abaixo":
				onde_temperatura_q = onde_temperatura_f = raio_trocador + 2
				onde_temperatura_q_in = -raio_trocador - len(str('{:.2f}'.format(round(tq_in, 2))))*tamanho_string/y
				onde_temperatura_f_in = -raio_trocador - len(str('{:.2f}'.format(round(tf_in, 2))))*tamanho_string/y

		if onde[6:] == "acima":
			trocador.setx(distancia_x/2 - subestagio*espaco_trocadores)
			temp.setx(distancia_x/2 - subestagio*espaco_trocadores)
			if dividida_quente[trocadorr[0]-1]:
				trocador.sety(corrente_quente.pos()[1] - raio_trocador - ramo_y*(trocadorr[2]-1))
				temp.sety(corrente_quente.pos()[1] + raio_trocador + carga_trocador - ramo_y*(trocadorr[2]-1))
				temperatura.sety(corrente_quente.pos()[1] - h_string - grossura_corrente - 1 - ramo_y*(trocadorr[2]-1))
				ident.sety(corrente_quente.pos()[1] - raio_trocador/2 - ramo_y*(trocadorr[2]-1))
			else:
				trocador.sety(corrente_quente.pos()[1] - raio_trocador)
				temp.sety(corrente_quente.pos()[1] + raio_trocador + carga_trocador)
				temperatura.sety(corrente_quente.pos()[1] - h_string - grossura_corrente - 1)
				ident.sety(corrente_quente.pos()[1] - raio_trocador/2)
			if onde[:5] == "ambas":
				if viola[1] or anterior[0]:
					temperatura.color("red")
					if viola[3] or anterior[2]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaque = ""
				temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_q)
				temperatura.write(str('{:.2f}'.format(round(tq_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
				if duas_temp[0]:
					if viola[0]:
						temperatura.color("red")
						if viola[2]:
							estilo = "bold"
							destaque = "**"
						else:
							estilo = "normal"
							destaque = ""
					else:
						temperatura.color("black")
						estilo = "normal"
						destaque = ""
					temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_q_in)
					temperatura.write(str('{:.2f}'.format(round(tq_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			else:
				if anterior[0] or viola[1]:
					temperatura.color("red")
					if anterior[2] or viola[3]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaque = ""
				temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_q_in)
				temperatura.write(str('{:.2f}'.format(round(tq_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
				if duas_temp[0]:
					if viola[0]:
						temperatura.color("red")
						if viola[2]:
							estilo = "bold"
							destaque = "**"
						else:
							estilo = "normal"
							destaque = ""
					else:
						temperatura.color("black")
						estilo = "normal"
						destaque = ""
					temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_q)
					temperatura.write(str('{:.2f}'.format(round(tq_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			trocador.pendown()
			trocador.begin_fill()
			trocador.circle(raio_trocador)
			trocador.end_fill()
			ident.setx(distancia_x/2 - subestagio*espaco_trocadores + 1)
			ident.write("E" + str(trocador_atual), align="center", font=("Arial", fonte_carga, "bold"))
			if dividida_fria[trocadorr[1]-1]:
				trocador.sety(corrente_fria.pos()[1] - raio_trocador - ramo_y*(trocadorr[3]-1))
				temperatura.sety(corrente_fria.pos()[1] - h_string - grossura_corrente - 1 - ramo_y*(trocadorr[3]-1))
				ident.sety(corrente_fria.pos()[1] - raio_trocador/2 - ramo_y*(trocadorr[3]-1))
			else:
				trocador.sety(corrente_fria.pos()[1] - raio_trocador)
				temperatura.sety(corrente_fria.pos()[1] - h_string - grossura_corrente - 1)
				ident.sety(corrente_fria.pos()[1] - raio_trocador/2)
			if anterior[1] or viola[1]:
				temperatura.color("red")
				if anterior[3] or viola[3]:
					estilo = "bold"
					destaque = "**"
				else:
					estilo = "normal"
					destaque = ""
			else:
				temperatura.color("black")
				estilo = "normal"
				destaque = ""
			temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_f_in)
			temperatura.write(str('{:.2f}'.format(round(tf_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			if duas_temp[1]:
				if viola[0]:
					temperatura.color("red")
					if viola[2]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaque = ""
				temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_f)
				temperatura.write(str('{:.2f}'.format(round(tf_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			trocador.begin_fill()
			trocador.circle(raio_trocador)
			trocador.end_fill()
			ident.write("E" + str(trocador_atual), align="center", font=("Arial", fonte_carga, "bold"))
		elif onde[6:] == "abaixo":
			trocador.setx(-distancia_x/2 + subestagio*espaco_trocadores)
			temp.setx(-distancia_x/2 + subestagio*espaco_trocadores)
			if dividida_quente_abaixo[trocadorr[0]-1]:
				trocador.sety(corrente_quente.pos()[1] - raio_trocador - ramo_y*(trocadorr[2]-1))
				temp.sety(corrente_quente.pos()[1] + raio_trocador + carga_trocador - ramo_y*(trocadorr[2]-1))
				temperatura.sety(corrente_quente.pos()[1] - h_string - grossura_corrente - 1 - ramo_y*(trocadorr[2]-1))
				ident.sety(corrente_quente.pos()[1] - raio_trocador/2 - ramo_y*(trocadorr[2]-1))
			else:
				trocador.sety(corrente_quente.pos()[1] - raio_trocador)
				temp.sety(corrente_quente.pos()[1] + raio_trocador + carga_trocador)
				temperatura.sety(corrente_quente.pos()[1] - h_string - grossura_corrente - 1)
				ident.sety(corrente_quente.pos()[1] - raio_trocador/2)
			if anterior[0] or viola[0]:
				temperatura.color("red")
				if anterior[1] or viola[1]:
					estilo = "bold"
					destaque = "**"
				else:
					estilo = "normal"
					destaque = ""
			else:
				temperatura.color("black")
				estilo = "normal"
				destaque = ""
			temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_q_in)
			temperatura.write(str('{:.2f}'.format(round(tq_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			if duas_temp[0]:
				if viola[1]:
					temperatura.color("red")
					if viola[3]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaque = ""
				temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_q)
				temperatura.write(str('{:.2f}'.format(round(tq_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			trocador.pendown()
			trocador.begin_fill()
			trocador.circle(raio_trocador)
			trocador.end_fill()
			ident.setx(-distancia_x/2 + subestagio*espaco_trocadores + 1)
			ident.write("E" + str(trocador_atual), align="center", font=("Arial", fonte_carga, "bold"))
			if dividida_fria_abaixo[trocadorr[1]-1]:
				trocador.sety(corrente_fria.pos()[1] - raio_trocador - ramo_y*(trocadorr[3]-1))
				temperatura.sety(corrente_fria.pos()[1] - h_string - grossura_corrente - 1 - ramo_y*(trocadorr[3]-1))
				ident.sety(corrente_fria.pos()[1] - raio_trocador/2 - ramo_y*(trocadorr[3] - 1))
			else:
				trocador.sety(corrente_fria.pos()[1] - raio_trocador)
				temperatura.sety(corrente_fria.pos()[1] - h_string - grossura_corrente - 1 - ramo_y*(trocadorr[3]-1))
				ident.sety(corrente_fria.pos()[1] - raio_trocador/2)
			if onde[:5] == "ambas":
				if anterior[1] or viola[0]:
					temperatura.color("red")
					if anterior[3] or viola[1]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaeu = ""
				temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_f)
				temperatura.write(str('{:.2f}'.format(round(tf_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
				if duas_temp[1]:
					if viola[1]:
						temperatura.color("red")
						if viola[3]:
							estilo = "bold"
							destaque = "**"
						else:
							estilo = "normal"
							destaque = ""
					else:
						temperatura.color("black")
						estilo = "normal"
						destaque = ""
					temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_f_in)
					temperatura.write(str('{:.2f}'.format(round(tf_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			else:
				if anterior[1] or viola[0]:
					temperatura.color("red")
					if anterior[3] or viola[2]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaque = ""
				temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_f_in)
				temperatura.write(str('{:.2f}'.format(round(tf_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
				if duas_temp[1]:
					if viola[1]:
						temperatura.color("red")
						if viola[3]:
							estilo = "bold"
							destaque = "**"
						else:
							estilo = "normal"
							destaque = ""
					else:
						temperatura.color("black")
						estilo = "normal"
						destaque = ""
					temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_f)
					temperatura.write(str('{:.2f}'.format(round(tf_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			trocador.begin_fill()
			trocador.circle(raio_trocador)
			trocador.end_fill()
			ident.write("E" + str(trocador_atual), align="center", font=("Arial", fonte_carga, "bold"))

		temp.write(str('{:.2f}'.format(round(trocadorr[6], 2))), align="center", font=("Arial", fonte_carga, "bold"))

	def utilidade_desenho(onde, corrente, subestagio, calor, primeiro, utilidade_atual, x):
		utilidade = criar_turtle()
		utilidade.pensize(grossura_trocador)
		if onde[:5] == "ambas":
			distancia_x = 0
		else:
			distancia_x = x
		if onde[6:] == "acima":
			utilidade.color("black", "orange")
			if primeiro == 0:
				utilidade.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores)
				temp.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores)
				ident.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores + 1)
			else:
				utilidade.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores + primeiro*espaco_utilidades)
				temp.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores + primeiro*espaco_utilidades)
				ident.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores + primeiro*espaco_utilidades + 1)
		elif onde[6:] == "abaixo":
			utilidade.color("black", "#7FFFD4")
			if primeiro == 0:
				utilidade.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores)
				temp.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores)
				ident.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores + 1)
			else:
				utilidade.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores - primeiro*espaco_utilidades)
				temp.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores - primeiro*espaco_utilidades)
				ident.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores - primeiro*espaco_utilidades + 1)
		utilidade.sety(corrente.pos()[1] - raio_trocador)
		utilidade.pendown()
		utilidade.begin_fill()
		utilidade.circle(raio_trocador)
		utilidade.end_fill()
		temp.sety(corrente.pos()[1] + raio_trocador)
		temp.write(str('{:.2f}'.format(round(calor, 2))), align="center", font=("Arial", fonte_carga, "bold"))
		ident.sety(corrente.pos()[1] - raio_trocador/2)
		if onde[6:] == "acima":
			ident.write("H" + str(utilidade_atual), align="center", font=("Arial", fonte_carga, "bold"))
		if onde[6:] == "abaixo":
			ident.write("C" + str(utilidade_atual), align="center", font=("Arial", fonte_carga, "bold"))

	def legenda(onde_comecar, unidades):
		trocador = turtle.Turtle()
		trocador.hideturtle()
		trocador.color("black", "white")
		trocador.pensize(grossura_corrente)
		trocador.penup()
		trocador.speed(1000)

		corrente = turtle.Turtle()
		corrente.pensize(grossura_corrente)
		corrente.penup()
		corrente.speed(1000)

		texto = turtle.Turtle()
		texto.hideturtle()
		texto.penup()
		texto.speed(1000)

		legenda = turtle.Turtle()
		legenda.hideturtle()
		legenda.pensize(grossura_pinch)
		legenda.penup()
		legenda.speed(1000)


		legenda_comeco_corrente = onde_comecar[0]
		legenda_trocador = onde_comecar[0] + 150
		legenda_raio_trocador = 30
		caixa_horizontal = 300 + len("temperature")*4*2 + 80
		caixa_vertical = legenda_raio_trocador*2 + 100

		legenda.sety(onde_comecar[1] + caixa_vertical/2)
		legenda.setx(onde_comecar[0] - len("temperature")*4 - 40)
		legenda.pendown()
		for i in range(2):
			legenda.forward(caixa_horizontal)
			legenda.right(90)
			legenda.forward(caixa_vertical)
			legenda.right(90)


		corrente.setx(legenda_comeco_corrente)
		corrente.sety(onde_comecar[1])
		corrente.pendown()
		corrente.forward(300)
		trocador.setx(legenda_trocador)
		trocador.sety(corrente.pos()[1] - legenda_raio_trocador)
		trocador.pendown()
		trocador.begin_fill()
		trocador.circle(legenda_raio_trocador)
		trocador.end_fill()
		texto.setx(trocador.pos()[0])
		texto.sety(corrente.pos()[1] + legenda_raio_trocador + 5)
		if unidades[1] == "kW/K":
			texto.write("HEAT LOAD ({})".format(unidades[1][:2]), align="center", font=("Arial", fonte_carga, "bold"))
		else:
			texto.write("HEAT LOAD ({})".format(unidades[1][:3]), align="center", font=("Arial", fonte_carga, "bold"))
		texto.sety(corrente.pos()[1] + legenda_raio_trocador + 20)
		texto.write("LEGEND", align="center", font=("Arial", 14, "bold"))
		legenda.penup()
		legenda.sety(texto.pos()[1] - 2)
		legenda.setx(texto.pos()[0] + len("subtitle")*5)
		legenda.pendown()
		legenda.setx(texto.pos()[0] - len("subtitle")*5)

		texto.setx(trocador.pos()[0] - legenda_raio_trocador - len("temperature")*2.75)
		texto.sety(corrente.pos()[1] - 14)
		texto.write("Inlet", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(corrente.pos()[1] - 24)
		texto.write("Temperature", align="center", font=("Arial", fonte_carga, "normal"))
		texto.setx(trocador.pos()[0] + legenda_raio_trocador + len("temperature")*2.90)
		texto.write("Temperature", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(corrente.pos()[1] - 14)
		texto.write("Outlet", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(corrente.pos()[1] + 2)
		texto.setx(legenda_comeco_corrente - len("temperature")*4)
		texto.write("Supply", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(corrente.pos()[1] - 14)
		texto.write("Temperature", align="center", font=("Arial", fonte_carga, "normal"))
		texto.setx(len("temperature")*4 + corrente.pos()[0])
		texto.sety(corrente.pos()[1] + 2)
		texto.write("Target", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(corrente.pos()[1] - 14)
		texto.write("Temperature", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(trocador.pos()[1] - 40)
		texto.setx(legenda_trocador)
		texto.write("UNITS:   Temperature: {};   CP = {}".format(unidades[0], unidades[1]), align="center", font=("Arial", fonte_carga, "bold"))

	global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo, distancia_x, ramo_x, ramo_y, nao_toca_pinch, espaco_trocadores, comecar_pinch, raio_trocador, espaco_utilidades, distancia_cp, maior_cp
	global desenho_em_dia, desenho_em_dia_abaixo, desenho_em_dia_ambas, tamanho_antigo, tamanho_antigo_acima, tamanho_antigo_abaixo

	desenha = False
	if subrede == "acima" and not desenho_em_dia and not desenha:
		desenha = True
		desenho_em_dia = True

	elif subrede == "abaixo" and not desenho_em_dia_abaixo and not desenha:
		desenha = True
		desenho_em_dia_abaixo = True

	elif subrede == "ambas" and not desenho_em_dia_ambas and not desenha:
		desenha = True
		desenho_em_dia_ambas = True

	if desenha:
		turtle.TurtleScreen._RUNNING=True
		turtle.delay(0)
		turtle.hideturtle()
		turtle.speed(1000)
		turtle.hideturtle()
		temp = criar_turtle() #CP, supply/target, heat load
		temperatura = criar_turtle() #temps de troca
		ident = criar_turtle() #E1 C1 H1 hot 1 cold 1


		#obtendo arbitrarias
		tamanho_string = 2.5
		tamanhos = []
		temps = Th0 + Thf + Tc0 + Tcf
		for i in range(len(temps)):
			tamanhos.append(len(str('{:.2f}'.format(round(temps[i], 2))))*tamanho_string)
		cps = CPh + CPc

		#strings
		h_string = 2
		fonte_carga = 4
		fonte_temp = 3

		#setas e trocadores
		raio_trocador = 4.2
		grossura_corrente = 0.75
		grossura_pinch = 0.5
		grossura_trocador = 0.5
		seta = 0.4

		#espaçamentos
		carga_trocador = 0
		ramo_x = 10
		ramo_y = 3*raio_trocador + h_string
		borda = 100
		espaco_trocadores = max(tamanhos) + 5
		espaco_utilidades = espaco_trocadores/2
		nao_toca_pinch = max(tamanhos) + 5
		distancia_cp = nao_toca_pinch + 20
		maior_cp = len("Streams CP ({})".format(unidades_usadas[1]))*tamanho_string/2
		maior_duty = len("Streams Duty ({})".format(unidades_usadas[2]))*tamanho_string/2


		x = 150
		#tamanho das setas
		if subrede == "acima":
			distancia_x = espaco_trocadores * (len(matriz_armazenada) + len(utilidades) + 2)
			if distancia_x < x:
				distancia_x = x
		elif subrede == "abaixo":
			distancia_x = espaco_trocadores * (len(matriz_trocadores_abaixo) + len(utilidades_abaixo) + 2)
			if distancia_x < x:
				distancia_x = x
		elif subrede == "ambas":
			acima = abaixo = 0
			for trocador in matriz_evolucao:
				if trocador[5] == 1:
					acima += 1
				if trocador[5] == 2:
					abaixo += 1
			distancia_x = espaco_trocadores * 2 * (max(acima, abaixo) + 1)
			if distancia_x < 2*x:
				distancia_x = 2*x

		#tamanho da janela
		if subrede == "ambas":
			w = distancia_x + distancia_cp + maior_duty*2 + len("Cold 99 (utility)")*tamanho_string + borda
		else:
			w = distancia_x + 1.5*distancia_cp + maior_cp*2 + maior_duty*2 + borda + len("Cold 99 (utility)")*tamanho_string

		h = 0
		h_acima = 0
		h_abaixo = 0

		for i in range(len(correntes_quentes)):
			if quantidade_quente[i] > quantidade_quente_abaixo[i]:
				h += ramo_y * quantidade_quente[i]
			else:
				h += ramo_y * quantidade_quente_abaixo[i]
			h_acima += ramo_y * quantidade_quente[i]
			h_abaixo += ramo_y * quantidade_quente_abaixo[i]

		for i in range(len(correntes_frias)):
			if quantidade_fria[i] > quantidade_fria_abaixo[i]:
				h += ramo_y * quantidade_fria[i]
			else:
				h += ramo_y * quantidade_fria_abaixo[i]
			h_acima += ramo_y * quantidade_fria[i]
			h_abaixo += ramo_y * quantidade_fria_abaixo[i]

		if subrede == "acima":
			y_acima, y_abaixo = h_acima/2, h_acima/2
			turtle.setup(width=w, height=1.5*h_acima + 35)
			h = 1.5*h_acima + 35
		elif subrede == "abaixo":
			y_acima, y_abaixo = h_abaixo/2, h_abaixo/2
			turtle.setup(width=w, height=1.5*h_abaixo + 35)
			h = 1.5*h_abaixo + 35
		elif subrede == "ambas":
			y_acima, y_abaixo = h/2, h/2
			turtle.setup(width=w, height=1.5*h)

		y_acima_f, y_abaixo_f = y_acima, y_abaixo
		comecar_pinch = y_acima + ramo_y

		if subrede == "acima":
			tamanho_antigo_acima = [w, h]
			quentes("above", correntes_quentes, corrente_quente_presente_acima)
			frias("above", correntes_frias, corrente_fria_presente_acima)
			pinch(y_acima, "acima")

			trocador_atual = 1

			if len(matriz_armazenada) > 0:
				subestagio = 1
				for trocadorr in matriz_armazenada:
					subestagio += 1
					duas_temp_quente = True
					duas_temp_fria = True
					viola_quente, viola_frio = False, False
					termo_quente, termo_frio = False, False
					viola_anterior_quente, viola_anterior_fria = False, False
					if trocadorr[7] - trocadorr[8] < dTmin:
						viola_quente = True
						if trocadorr[7] - trocadorr[8] < 0:
							termo_quente = True
					if trocadorr[9] - trocadorr[10] < dTmin:
						viola_frio = True
						if trocadorr[9] - trocadorr[10] < 0:
							termo_frio = True
					try:
						if matriz_armazenada[matriz_armazenada.index(trocadorr)+1][0] == trocadorr[0] and matriz_armazenada[matriz_armazenada.index(trocadorr)+1][2] == trocadorr[2]:
							duas_temp_quente = False
						if matriz_armazenada[matriz_armazenada.index(trocadorr)+1][1] == trocadorr[1] and matriz_armazenada[matriz_armazenada.index(trocadorr)+1][3] == trocadorr[3]:
							duas_temp_fria = False
					except:
						pass
					try:
						termo, termo_quente_anterior, termo_fria_anterior = False, False, False
						if (matriz_armazenada[matriz_armazenada.index(trocadorr)-1][7] - matriz_armazenada[matriz_armazenada.index(trocadorr)-1][8]) < dTmin and matriz_armazenada.index(trocadorr) != 0:
							if (matriz_armazenada[matriz_armazenada.index(trocadorr)-1][7] - matriz_armazenada[matriz_armazenada.index(trocadorr)-1][8]) < 0 and matriz_armazenada.index(trocadorr) != 0:
								termo = True
							if matriz_armazenada[matriz_armazenada.index(trocadorr)-1][0] == trocadorr[0] and matriz_armazenada[matriz_armazenada.index(trocadorr)-1][2] == trocadorr[2]:
								viola_anterior_quente = True
								if termo:
									termo_quente_anterior = True
							if matriz_armazenada[matriz_armazenada.index(trocadorr)-1][1] == trocadorr[1] and matriz_armazenada[matriz_armazenada.index(trocadorr)-1][3] == trocadorr[3]:
								viola_anterior_fria = True
								if termo:
									termo_fria_anterior = True
					except:
						pass
					inserir_trocador_desenho("123456acima", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr, trocador_atual, distancia_x, [duas_temp_quente, duas_temp_fria], [viola_quente, viola_frio, termo_quente, termo_frio], [viola_anterior_quente, viola_anterior_fria, termo_fria_anterior, termo_quente_anterior])
					trocador_atual += 1

				if len(utilidades) > 0:
					primeiro = 0
					util = 1
					for utilidadee in utilidades:
						subestagio += 1
						utilidade_desenho("123456acima", correntes_frias[utilidadee[0]-1], subestagio, utilidadee[1], primeiro, util, distancia_x)
						primeiro += 1
						util += 1


		elif subrede == "abaixo":
			tamanho_antigo_abaixo = [w, h]
			quentes("below", correntes_quentes, corrente_quente_presente_abaixo)
			frias("below", correntes_frias, corrente_fria_presente_abaixo)
			pinch(y_abaixo, "abaixo")

			trocador_atual = 1

			if len(matriz_trocadores_abaixo) > 0:
				subestagio = 1
				for trocadorr in matriz_trocadores_abaixo:
					subestagio += 1
					duas_temp_quente = True
					duas_temp_fria = True
					viola_quente, viola_frio = False, False
					termo_quente, termo_frio = False, False
					viola_anterior_quente, viola_anterior_fria = False, False
					if trocadorr[7] - trocadorr[8] < dTmin:
						viola_frio = True
						if trocadorr[7] - trocadorr[8] < 0:
							termo_frio = True
					if trocadorr[9] - trocadorr[10] < dTmin:
						viola_quente = True
						if trocadorr[9] - trocadorr[10] < 0:
							termo_quente = True
					try:
						if matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)+1][0] == trocadorr[0] and matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)+1][2] == trocadorr[2]:
							duas_temp_quente = False
						if matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)+1][1] == trocadorr[1] and matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)+1][3] == trocadorr[3]:
							duas_temp_fria = False
					except:
						pass
					try:
						termo = termo_quente_anterior = termo_fria_anterior = False
						if (matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][7] - matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][8]) < dTmin and matriz_trocadores_abaixo.index(trocadorr) != 0:
							if (matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][7] - matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][8]) < 0 and matriz_trocadores_abaixo.index(trocadorr) != 0:
								termo = True
							if matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][0] == trocadorr[0] and matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][2] == trocadorr[2]:
								viola_anterior_quente = True
								if termo:
									termo_quente_anterior = True
							if matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][1] == trocadorr[1] and matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][3] == trocadorr[3]:
								viola_anterior_fria = True
								if termo:
									termo_fria_anterior = True
					except:
						pass
					inserir_trocador_desenho("123456abaixo", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr, trocador_atual, distancia_x, [duas_temp_quente, duas_temp_fria], [viola_quente, viola_frio, termo_quente, termo_frio], [viola_anterior_quente, viola_anterior_fria, termo_quente_anterior, termo_fria_anterior])
					trocador_atual += 1

				if len(utilidades_abaixo) > 0:
					primeiro = 0
					util = 1
					for utilidadee in utilidades_abaixo:
						subestagio += 1
						utilidade_desenho("123456abaixo", correntes_quentes[utilidadee[0]-1], subestagio, utilidadee[1], primeiro, util, distancia_x)
						primeiro += 1
						util += 1
		elif subrede == "ambas":
			tamanho_antigo = [w, h]
			quentes("ambas", correntes_quentes, corrente_quente_presente_acima)
			frias("ambas", correntes_frias, corrente_fria_presente_acima)

			trocador_atual = 1
			if len(matriz_evolucao) > 0:
				subestagio = 0
				subestagio_abaixo = 0
				for trocadorr in matriz_evolucao:
					if trocadorr[5] == 1:
						subestagio += 1
						duas_temp_quente = True
						duas_temp_fria = True
						viola_quente, viola_frio = False, False
						termo_quente, termo_frio = False, False
						viola_anterior_quente, viola_anterior_fria = False, False
						if trocadorr[7] - trocadorr[8] < dTmin:
							viola_quente = True
							if trocadorr[7] - trocadorr[8] < 0:
								termo_quente = True
						if trocadorr[9] - trocadorr[10] < dTmin:
							viola_frio = True
							if trocadorr[9] - trocadorr[10] < 0:
								termo_frio = True
						try:
							if matriz_evolucao[matriz_evolucao.index(trocadorr)+1][0] == trocadorr[0] and matriz_evolucao[matriz_evolucao.index(trocadorr)+1][2] == trocadorr[2]:
								duas_temp_quente = False
							if matriz_evolucao[matriz_evolucao.index(trocadorr)+1][1] == trocadorr[1] and matriz_evolucao[matriz_evolucao.index(trocadorr)+1][3] == trocadorr[3]:
								duas_temp_fria = False
							if matriz_evolucao[matriz_evolucao.index(trocadorr)+1][5] == 2:
								duas_temp_quente = True
								duas_temp_fria = True
						except:
							pass
						try:
							termo, termo_quente_anterior, termo_fria_anterior = False, False, False
							if (matriz_evolucao[matriz_evolucao.index(trocadorr)-1][7] - matriz_evolucao[matriz_evolucao.index(trocadorr)-1][8]) < dTmin and matriz_evolucao.index(trocadorr) != 0:
								if (matriz_evolucao[matriz_evolucao.index(trocadorr)-1][7] - matriz_evolucao[matriz_evolucao.index(trocadorr)-1][8]) < 0 and matriz_evolucao.index(trocadorr) != 0:
									termo = True
								if matriz_evolucao[matriz_evolucao.index(trocadorr)-1][0] == trocadorr[0] and matriz_evolucao[matriz_evolucao.index(trocadorr)-1][2] == trocadorr[2]:
									viola_anterior_quente = True
									if termo:
										termo_quente_anterior = True
								if matriz_evolucao[matriz_evolucao.index(trocadorr)-1][1] == trocadorr[1] and matriz_evolucao[matriz_evolucao.index(trocadorr)-1][3] == trocadorr[3]:
									viola_anterior_fria = True
									if termo:
										termo_fria_anterior = True
						except:
							pass
						inserir_trocador_desenho("ambas/acima", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr, trocador_atual, distancia_x, [duas_temp_quente, duas_temp_fria], [viola_quente, viola_frio, termo_quente, termo_frio], [viola_anterior_quente, viola_anterior_fria, termo_quente_anterior, termo_fria_anterior])
					elif trocadorr[5] == 2:
						subestagio_abaixo += 1
						duas_temp_quente = True
						duas_temp_fria = True
						viola_quente, viola_frio = False, False
						termo_quente, termo_frio = False, False
						viola_anterior_quente, viola_anterior_fria = False, False
						if trocadorr[7] - trocadorr[8] < dTmin:
							viola_quente = True
							if trocadorr[7] - trocadorr[8] < 0:
								termo_quente = True
						if trocadorr[9] - trocadorr[10] < dTmin:
							viola_frio = True
							if trocadorr[9] - trocadorr[10] < 0:
								termo_frio = True

						try:
							if matriz_evolucao[matriz_evolucao.index(trocadorr)+1][0] == trocadorr[0] and matriz_evolucao[matriz_evolucao.index(trocadorr)+1][2] == trocadorr[2]:
								duas_temp_quente = False
							if matriz_evolucao[matriz_evolucao.index(trocadorr)+1][1] == trocadorr[1] and matriz_evolucao[matriz_evolucao.index(trocadorr)+1][3] == trocadorr[3]:
								duas_temp_fria = False
						except:
							pass
						try:
							termo, termo_quente_anterior, termo_fria_anterior = False, False, False
							if (matriz_evolucao[matriz_evolucao.index(trocadorr)-1][9] - matriz_evolucao[matriz_evolucao.index(trocadorr)-1][10]) < dTmin:
								if (matriz_evolucao[matriz_evolucao.index(trocadorr)-1][9] - matriz_evolucao[matriz_evolucao.index(trocadorr)-1][10]) < 0:
									termo = True
								if matriz_evolucao[matriz_evolucao.index(trocadorr)-1][0] == trocadorr[0] and matriz_evolucao[matriz_evolucao.index(trocadorr)-1][2] == trocadorr[2]:
									viola_anterior_quente = True
									if termo:
										termo_quente_anterior = True
								if matriz_evolucao[matriz_evolucao.index(trocadorr)-1][1] == trocadorr[1] and matriz_evolucao[matriz_evolucao.index(trocadorr)-1][3] == trocadorr[3]:
									viola_anterior_fria = True
									if termo:
										termo_fria_anterior = True
						except:
							pass
						if matriz_evolucao[matriz_evolucao.index(trocadorr)-1][5] == 1:
							viola_anterior_quente = False
							viola_anterior_frio = False
							termo_quente_anterior = False
							termo_fria_anterior = False
						inserir_trocador_desenho("ambas/abaixo", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio_abaixo, trocadorr, trocador_atual, distancia_x, [duas_temp_quente, duas_temp_fria], [viola_quente, viola_frio, termo_quente, termo_frio], [viola_anterior_quente, viola_anterior_fria, termo_quente_anterior, termo_fria_anterior])
					trocador_atual += 1

	else:
		if subrede == "acima":
			w = tamanho_antigo_acima[0]
			h = tamanho_antigo_acima[1]
		elif subrede == "abaixo":
			w = tamanho_antigo_abaixo[0]
			h = tamanho_antigo_abaixo[1]
		else:
			w = tamanho_antigo[0]
			h = tamanho_antigo[1]

	salvar_rede(teste, subrede, desenha, [w, h])

def salvar_rede(so_ver, onde, salva, tamanho):
	global primeira_vez

	if salva:
		turtle.getscreen()
		turtle.getcanvas().postscript(file = (onde + ".eps"))
		turtle.bye()
		# turtle.done()
		TARGET_BOUNDS = [tamanho[0]*3, tamanho[1]*3]
		if TARGET_BOUNDS[0] < 1280:
			TARGET_BOUNDS[0] = 1280
		if TARGET_BOUNDS[1] < 1280:
			TARGET_BOUNDS[1] = 1280
		TARGET_BOUNDS[0] = max(TARGET_BOUNDS)
		TARGET_BOUNDS[1] = TARGET_BOUNDS[0]
		pic = Image.open(onde + '.eps')
		pic.load(scale=10)
		if pic.mode in ('P', '1'):
			pic = pic.convert("RGB")
		ratio = min(TARGET_BOUNDS[0] / pic.size[0],
					TARGET_BOUNDS[1] / pic.size[1])
		new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))
		tamanho = [int(pic.size[0]*ratio), int(pic.size[1]*ratio)]
		pic = pic.resize(new_size, Image.ANTIALIAS)
		if onde == "acima":
			imagem = pic.crop((0, 0, pic.size[0] - 200, pic.size[1]))
		elif onde == "abaixo":
			imagem = pic.crop((200, 0, pic.size[0], pic.size[1]))
		else:
			imagem = pic
		imagem.save(onde + ".png")

	dlg.rede = QPixmap(onde + ".png")
	if not so_ver:#atualizando evolução
		dlg.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
		dlg.label_teste.setPixmap(dlg.rede)
		dlg.ambasScroll.setWidgetResizable(True)
		dlg.ambasScroll.ensureVisible(int(tamanho[0]/2), 0, 10, 10)
		dlg.tabWidget.setCurrentIndex(4)
	else:#subredes
		if onde == "acima":
			dlg.lay_acima.setContentsMargins(0, 0, 0, 0)
			dlg.hen_acima.setPixmap(QtGui.QPixmap(onde + ".png"))
			dlg.scroll_acima.ensureVisible(0, int(tamanho[1]/2), 1, 1)
		if onde == "abaixo":
			dlg.lay_abaixo.setContentsMargins(0, 0, 0, 0)
			dlg.hen_abaixo.setPixmap(QtGui.QPixmap(onde + ".png"))
			dlg.scroll_abaixo.ensureVisible(int(tamanho[1])+100, int(tamanho[1]/2), 1, 1)



#outros
def violou_dtmin(trocador_violado, onde, dados_do_trocador):
	dlg.dtmin = uic.loadUi("dtmin.ui")
	dlg.dtmin.show()
	text = "ΔT = " + str('{:.2f}'.format(round(trocador_violado[6], 2)))
	textfrio = "ΔT = " + str('{:.2f}'.format(round(trocador_violado[7], 2)))

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
		global subestagio_trocador, desenho_em_dia, desenho_em_dia_ambas
		indice = len(matriz_armazenada) - 1
		remover_trocador(dlg, dados_do_trocador, indice, matriz_armazenada)
		printar()
		checaresgotadosacima()
		dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
		desenho_em_dia = False
		desenho_em_dia_ambas = False
		atualizar_desenho("acima")
		dlg.dtmin.close()
		subestagio_trocador = indice

	def below(dados_do_trocacdor):
		global subestagio_trocador_abaixo, desenho_em_dia_abaixo, desenho_em_dia_ambas
		indice = len(matriz_trocadores_abaixo) - 1
		remover_trocador_abaixo(dlg, dados_do_trocador, indice, matriz_trocadores_abaixo)
		printar_abaixo()
		checaresgotadosabaixo()
		dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
		desenho_em_dia_abaixo = False
		desenho_em_dia_ambas = False
		atualizar_desenho("abaixo")
		dlg.dtmin.close()
		subestagio_trocador_abaixo = indice

def dividir_corrente(divisao, onde):
	global divtype
	divtype = divisao
	dlg.DivisaoQuente = uic.loadUi("divisao.ui")
	dlg.DivisaoFria = uic.loadUi("divisao.ui")
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
		global desenho_em_dia, desenho_em_dia_abaixo
		soma = 0
		fracao = [0] * quantidade
		for i in range(quantidade):
			soma += round(float(caixa_fracao[i].value()), 2)
			fracao[i] = round(float(caixa_fracao[i].value()), 2)
		if soma != 1:
			QMessageBox.about(dlg, "Error!", "The sum of the fractions must be equals 1.")
			if divtype == "Q":
				dlg.DivisaoQuente.show()
			if divtype == "F":
				dlg.DivisaoFria.show()
			return

		if onde == "above":
			divisao_de_correntes(divtype, estagio, corrente, quantidade, fracao)
			divisoes.append([divtype, 1, corrente, quantidade, fracao])
			if divtype == "F":
				testar_correntes(dlg, True)
				if quantidade > 1:
					dlg.comboBox_51.setEnabled(True)
				else:
					dlg.comboBox_51.setEnabled(False)
			else:
				if quantidade == 1:
					testar_correntes(dlg, True)
					dlg.comboBox_50.setEnabled(False)
				else:
					testar_correntes(dlg)
					dlg.comboBox_50.setEnabled(True)
			desenho_em_dia = False
		elif onde == "below":
			divisao_de_correntes_abaixo(divtype, estagio, corrente, quantidade, fracao)
			divisoes.append([divtype, 2, corrente, quantidade, fracao])
			if divtype == "Q":
				testar_correntes_abaixo(dlg, True)
				if quantidade > 1:
					dlg.comboBox_53.setEnabled(True)
				else:
					dlg.comboBox_53.setEnabled(False)
			else:
				if quantidade == 1:
					testar_correntes_abaixo(dlg, True)
					dlg.comboBox_54.setEnabled(False)
				else:
					testar_correntes_abaixo(dlg)
					dlg.comboBox_54.setEnabled(True)
			desenho_em_dia_abaixo = False

		if divtype == "Q":
			dlg.DivisaoQuente.close()
		if divtype == "F":
			dlg.DivisaoFria.close()

		printar()
		printar_abaixo()
		atualizar_desenho(onde)

	dlg.DivisaoQuente.pushButton.clicked.connect(lambda: confirm())
	dlg.DivisaoQuente.pushButton_3.clicked.connect(lambda: split(onde))
	dlg.DivisaoQuente.pushButton_2.clicked.connect(lambda: dlg.DivisaoQuente.close())
	dlg.DivisaoFria.pushButton.clicked.connect(lambda: confirm())
	dlg.DivisaoFria.pushButton_3.clicked.connect(lambda: split(onde))
	dlg.DivisaoFria.pushButton_2.clicked.connect(lambda: dlg.DivisaoFria.close())

def remover_anteriores(onde, indice_remover, nem_pergunta=False):

	def remover_acima(indice_remover, tudo=True):
		global subestagio_trocador, matriz_armazenada, desenho_em_dia, desenho_em_dia_ambas
		if tudo:
			if indice_remover <= len(matriz_armazenada) - 1:
				if len(utilidades) > 0:
					for i in range(len(utilidades)-1, -1, -1):
						try:
							remover_utilidade(utilidades[i][0], i, utilidades)
							dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
						except:
							print("deu nao")
				dlg.comboBox_10.setEnabled(False)
				dlg.pushButton_8.setEnabled(False)
				for i in range(len(matriz_armazenada)-1, indice_remover-1, -1):
					trocador_remover = matriz_armazenada[i]
					remover_trocador(dlg, trocador_remover, i, matriz_armazenada)
					atualizar_matriz(matriz_armazenada)
					dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
				subestagio_trocador = indice_remover
			else:
				tabela = dlg.tableWidget_2.currentRow()
				if tabela != -1:
					indice_remover = dlg.tableWidget_2.currentRow() - len(matriz_armazenada)
				else:
					indice_remover = dlg.trocador_acima.currentIndex() - len(matriz_armazenada)
				utilidade_remover = utilidades[indice_remover]
				corrente_remover_utilidade = utilidade_remover[0]
				remover_utilidade(corrente_remover_utilidade, indice_remover, utilidades)
				dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
		else:
			if indice_remover <= len(matriz_armazenada) - 1:
				if len(utilidades) > 0:
					for i in range(len(utilidades)-1, -1, -1):
						try:
							remover_utilidade(utilidades[i][0], i, utilidades)
							dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
						except:
							print("deu nao")
				trocador_remover = matriz_armazenada[indice_remover]
				matriz = nao_sacrificar_matriz(matriz_armazenada)
				matriz.pop(indice_remover)
				remover_todos_acima()
				for trocador in matriz:
					if matriz.index(trocador) >= indice_remover:
						trocador[4] -= 1
					matriz_armazenada, oi = inserir_trocador(dlg, trocador, False)
				if len(matriz) == 0:
					matriz_armazenada = []
				dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
				subestagio_trocador = len(matriz_armazenada)
			else:
				tabela = dlg.tableWidget_2.currentRow()
				if tabela != -1:
					indice_remover = dlg.tableWidget_2.currentRow() - len(matriz_armazenada)
				else:
					indice_remover = dlg.trocador_acima.currentIndex() - len(matriz_armazenada)
				utilidade_remover = utilidades[indice_remover]
				corrente_remover_utilidade = utilidade_remover[0]
				remover_utilidade(corrente_remover_utilidade, indice_remover, utilidades)
				dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
		printar()
		checaresgotadosacima()
		desenho_em_dia = False
		desenho_em_dia_ambas = False
		atualizar_desenho("acima")

	def remover_abaixo(indice_remover, tudo=True):
		global subestagio_trocador_abaixo, matriz_trocadores_abaixo, desenho_em_dia_abaixo, desenho_em_dia_ambas
		if tudo:
			if indice_remover <= len(matriz_trocadores_abaixo) - 1:
				if len(utilidades_abaixo) > 0:
					for i in range(len(utilidades_abaixo)-1, -1, -1):
						try:
							remover_utilidade_abaixo(utilidades_abaixo[i][0], i, utilidades_abaixo)
							dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
						except:
							print("deu nao")
				dlg.comboBox_43.setEnabled(False)
				dlg.pushButton_20.setEnabled(False)
				for i in range(len(matriz_trocadores_abaixo)-1, indice_remover-1, -1):
					trocador_remover = matriz_trocadores_abaixo[i]
					remover_trocador_abaixo(dlg, trocador_remover, i, matriz_trocadores_abaixo)
					atualizar_matriz_abaixo(matriz_trocadores_abaixo)
					dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
				subestagio_trocador_abaixo = indice_remover
			else:
				tabela = dlg.tableWidget_14.currentRow()
				if tabela != -1:
					indice_remover = dlg.tableWidget_14.currentRow() - len(matriz_trocadores_abaixo)
				else:
					indice_remover = dlg.trocador_abaixo.currentIndex() - len(matriz_trocadores_abaixo)
				utilidade_remover = utilidades_abaixo[indice_remover]
				corrente_remover_utilidade = utilidade_remover[0]
				remover_utilidade_abaixo(corrente_remover_utilidade, indice_remover, utilidades_abaixo)
				dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
		else:
			if indice_remover <= len(matriz_trocadores_abaixo) - 1:
				if len(utilidades_abaixo) > 0:
					for i in range(len(utilidades_abaixo)-1, -1, -1):
						try:
							remover_utilidade_abaixo(utilidades_abaixo[i][0], i, utilidades_abaixo)
							dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
						except:
							print("deu nao")
				trocador_remover = matriz_trocadores_abaixo[indice_remover]
				matriz = nao_sacrificar_matriz(matriz_trocadores_abaixo)
				matriz.pop(indice_remover)
				remover_todos_abaixo()
				for trocador in matriz:
					if matriz.index(trocador) >= indice_remover:
						trocador[4] -= 1
					matriz_trocadores_abaixo, oi = inserir_trocador_abaixo(dlg, trocador, False)
				if len(matriz) == 0:
					matriz_trocadores_abaixo = []
				dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
				subestagio_trocador_abaixo = len(matriz_trocadores_abaixo)
			else:
				tabela = dlg.tableWidget_14.currentRow()
				if tabela != -1:
					indice_remover = dlg.tableWidget_14.currentRow() - len(matriz_trocadores_abaixo)
				else:
					indice_remover = dlg.trocador_abaixo.currentIndex() - len(matriz_trocadores_abaixo)
				utilidade_remover = utilidades_abaixo[indice_remover]
				corrente_remover_utilidade = utilidade_remover[0]
				remover_utilidade_abaixo(corrente_remover_utilidade, indice_remover, utilidades_abaixo)
				dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
		printar_abaixo()
		checaresgotadosabaixo()
		desenho_em_dia_abaixo = False
		desenho_em_dia_ambas = False
		atualizar_desenho("abaixo")

	def sim(onde, indice_remover):
		global perguntar, remover_todos
		try:
			if dlg.perguntar.lembrar.isChecked():
				perguntar = False
				remover_todos = True
			dlg.perguntar.close()
		except:
			pass
		if onde == "acima":
			remover_acima(indice_remover)
		if onde == "abaixo":
			remover_abaixo(indice_remover)

	def nao(onde, indice_remover):
		global perguntar, remover_todos
		try:
			if dlg.perguntar.lembrar.isChecked():
				perguntar = False
				remover_todos = False
			dlg.perguntar.close()
		except:
			pass
		if onde == "acima":
			remover_acima(indice_remover, False)
		if onde == "abaixo":
			remover_abaixo(indice_remover, False)

	global remover_todos, perguntar

	if perguntar and not nem_pergunta: #nem pergunta analisa se ja é o ultimo, perguntar analisa a preferencia do usuário
		dlg.perguntar = uic.loadUi("remover_anteriores.ui")
		dlg.perguntar.show()
		dlg.perguntar.sim.clicked.connect(lambda: sim(onde, indice_remover))
		dlg.perguntar.nao.clicked.connect(lambda: nao(onde, indice_remover))
	else:
		if remover_todos:
			sim(onde, indice_remover)
		else:
			nao(onde, indice_remover)

def atualizar_desenho(onde, botao=False):
	if botao:
		if onde == "acima" or onde == "above":
			dlg.tab_acima.setCurrentIndex(0)
		elif onde == "abaixo" or onde == "below":
			dlg.tab_abaixo.setCurrentIndex(0)
	if onde == "acima" or onde == "above":
		if dlg.tab_acima.currentIndex() == 0:
			desenhar_rede(correntes_quentes, correntes_frias, "acima", True)
			dlg.emdia_acima.setText("Up to date drawing.")
			dlg.emdia_acima.setStyleSheet("QLabel {color: green}")
		else:
			dlg.emdia_acima.setText("Drawing requires update.")
			dlg.emdia_acima.setStyleSheet("QLabel {color: red}")
	elif onde == "abaixo" or onde == "below":
		if dlg.tab_abaixo.currentIndex() == 0:
			desenhar_rede(correntes_quentes, correntes_frias, "abaixo", True)
			dlg.emdia_abaixo.setText("Up to date drawing.")
			dlg.emdia_abaixo.setStyleSheet("QLabel {color: green}")
		else:
			dlg.emdia_abaixo.setText("Drawing requires update.")
			dlg.emdia_abaixo.setStyleSheet("QLabel {color: red}")



#evolução
def nao_sacrificar_matriz(matriz_naomuda):
	matriz = []
	for i in range(len(matriz_naomuda)):
		trocador = []
		for j in range(len(matriz_naomuda[0])):
			try:
				trocador.append(matriz_naomuda[i][j])
			except:
				pass
		matriz.append(trocador)
	return matriz

def evolucao(matriz_acima_naomuda, matriz_abaixo_naomuda, nivel, todos=False, jogar_evolucao=False):

	def criar_matriz(matriz_acima, matriz_abaixo):
		for i in range(len(matriz_acima)-1, -1, -1):
			if len(matriz_acima[i]) == 2:
				matriz_acima.pop(i)
			else:
				matriz_acima[i][0] -= 1
				matriz_acima[i][1] += (nhot - 1)

		for i in range(len(matriz_abaixo)-1, -1, -1):
			if len(matriz_abaixo[i]) == 2:
				matriz_abaixo.pop(i)
			else:
				matriz_abaixo[i][0] -= 1
				matriz_abaixo[i][1] += (nhot - 1)

		return matriz_acima + matriz_abaixo, nhot, ncold

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

	def achar_trocador(incidencia, matriz_trocadores, correntee, excecao, comecar, nivel, n, trocador_inicial, trocadores_laco):
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
				if incidencia[c][trocadores] == -i and trocadores != excecao and not trocadores+1 in trocadores_laco:
					t = trocadores
					return c, t
		return "o", "o"

	def lacos(incidencia, matriz_trocadores, nivel, todos):
		ja_encontrado = []
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
				trocadores_laco = [trocador_inicial+1]
				tenta_dnv = True
				for n in range(nivel*2):
					if tenta_dnv:
						corrente, trocador = achar_trocador(incidencia, matriz_trocadores, corrente, trocador, comecar, nivel, n, trocador_inicial, trocadores_laco)
						if corrente == "o":
							tenta_dnv = False
						else:
							trocadores_laco.append(trocador+1)
							if corrente == corrente_inicial and trocador == trocador_inicial and n == nivel*2-1:
								trocadores_laco.pop(-1)
								if todos:
									if not sorted(trocadores_laco) in ja_encontrado:
										ja_encontrado.append(sorted(trocadores_laco))
								else:
									return trocadores_laco
		if todos:
			return ja_encontrado
		else:
			return ["None "]

	def criar_rede_completa(matriz_acima, matriz_abaixo, primeiro=False):
		ultimo_subestagio_acima = 0

		if primeiro:
			receber_pinch_ev(Thf, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, Th0, Tc0)
			for i in range(len(matriz_acima)-1, -1, -1):
				if len(matriz_acima[i]) > 2:
					ultimo_subestagio_acima = matriz_acima[i][4]
					break

			for i in range(len(matriz_acima)):
				if len(matriz_acima[i]) > 2:
					matriz_acima[i][4] = ultimo_subestagio_acima - i

			for trocador in matriz_abaixo:
				if len(trocador) > 2:
					# trocador[4] += ultimo_subestagio_acima
					trocador[5] = 2
			try:
				remover_todos_ev()
			except:
				pass
		else:
			ultimo_subestagio_acima = matriz_acima[0][4]
			remover_todos_ev()

		matriz_total = matriz_acima + matriz_abaixo

		for i in range(len(divisoes)):
			divisao_de_correntes_ev(divisoes[i][0], divisoes[i][1], divisoes[i][2], divisoes[i][3], divisoes[i][4])

		for trocador in matriz_total:
			if len(trocador) > 2:
				matriz_completa, violou, trocadores_violados = inserir_trocador_ev("oi", trocador[:7])
		try:
			return nao_sacrificar_matriz(matriz_completa)
		except:
			return []

	def coisas_interface(trocadores_laco, matriz_completa):
		text = ""
		dlg.trocador_remover.clear()
		menor_calor = []
		trocadores_combo = []
		for i in range(len(trocadores_laco)):
			if trocadores_laco[i] != "None ":
				text += ("E" + str(trocadores_laco[i]) + ", ")
				menor_calor.append(trocadores[trocadores_laco[i]-1][6])
				trocadores_combo.append(text[len(text)-4:len(text)-2])
				dlg.trocador_remover.addItem(text[len(text)-4:len(text)-2])
				dlg.trocador_remover.setEnabled(True)
				dlg.remover.setEnabled(True)
			else:
				text = trocadores_laco[i] + "."
				dlg.trocador_remover.setEnabled(False)
				dlg.remover.setEnabled(False)

		text = text[:len(text)-2]
		text += "."
		dlg.trocadores_loop.setText(text)
		try:
			menor_calorr = min(menor_calor)
			dlg.trocador_remover.setCurrentIndex(menor_calor.index(menor_calorr))
		except:
			pass
		dlg.trocador_remover.setItemText(dlg.trocador_remover.currentIndex(), dlg.trocador_remover.currentText() + " (suggested)")
		if nivel == 1:
			dlg.label_7.setText("Loop Found Between:")
		else:
			dlg.label_7.setText("Loop Found Among:")

		dlg.remover.clicked.connect(lambda: distribuir_calor(trocadores_laco, matriz_completa, dlg.trocador_remover.currentIndex()))

	def interface_todos(trocadores_laco, matriz_completa):

		class Botao():
			def __init__(self, nivel, laco):
				self.nivel = nivel
				self.laco = laco
				self.button = QtWidgets.QPushButton("  Remove  ")
				self.button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
				self.button.setStyleSheet("QPushButton {font: 1000}")
				self.combo = QtWidgets.QComboBox()
				self.combo.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
				self.combo.setMinimumWidth(100)
				self.button.clicked.connect(lambda: distribuir_calor(trocadores_laco[self.nivel][self.laco], matriz_completa, self.combo.currentIndex()))

			def botaoo(self):
				return self.button

			def comboo(self):
				return self.combo

		dlg.lista_lacos = uic.loadUi("lista_lacos.ui")

		if len(trocadores_laco) == 0:
			label_nivel = QtWidgets.QLabel("No remaining Loop")
			label_nivel.setStyleSheet("QLabel {font: 1000 12pt 'MS Shell Dlg 2'}")
			label_nivel.setAlignment(Qt.AlignCenter)
			dlg.lista_lacos.lista.addWidget(label_nivel)
		else:
			lay_nivel = [0] * len(trocadores_laco)
			lay_laco = [0] * len(trocadores_laco)
			label_nivel = [0] * len(trocadores_laco)
			label_trocador = [0] * len(trocadores_laco)
			botao_remover = [0] * len(trocadores_laco)


			for nivel in range(len(trocadores_laco)):
				lay_nivel[nivel] = QtWidgets.QVBoxLayout()
				linha = QtWidgets.QFrame()
				linha.setGeometry(QRect(60, 110, 751, 20))
				linha.setFrameShape(QtWidgets.QFrame.HLine)
				linha.setFrameShadow(QtWidgets.QFrame.Sunken)
				if nivel != 0:
					lay_nivel[nivel].addWidget(linha)
				lay_laco[nivel] = [0] * len(trocadores_laco[nivel])
				label_trocador[nivel] = [0] * len(trocadores_laco[nivel])
				botao_remover[nivel] = [0] * len(trocadores_laco[nivel])
				for laco in range(len(trocadores_laco[nivel])):
					if laco == 0:
						label_nivel[nivel] = QtWidgets.QLabel("Level " + str(int(len(trocadores_laco[nivel][laco])/2)) + " Loops")
						label_nivel[nivel].setStyleSheet("QLabel {font: 1000 12pt 'MS Shell Dlg 2'}")
						label_nivel[nivel].setAlignment(Qt.AlignCenter)
						lay_nivel[nivel].addWidget(label_nivel[nivel])
					lay_laco[nivel][laco] = QtWidgets.QHBoxLayout()
					botao_remover[nivel][laco] = Botao(nivel, laco)
					texto = "Loop " + str(laco+1) + ": "
					menor_calor = []
					for trocador in range(len(trocadores_laco[nivel][laco])):
						texto += "E" + str(trocadores_laco[nivel][laco][trocador]) + ", "
						botao_remover[nivel][laco].comboo().addItem("E" + str(trocadores_laco[nivel][laco][trocador]))
						menor_calor.append(matriz_completa[trocadores_laco[nivel][laco][trocador]-1][6])
					botao_remover[nivel][laco].comboo().setCurrentIndex(menor_calor.index(min(menor_calor)))
					botao_remover[nivel][laco].comboo().setItemText(botao_remover[nivel][laco].comboo().currentIndex(), botao_remover[nivel][laco].comboo().currentText() + " (suggested)")
					texto = texto[:len(texto)-2]
					texto += "."
					label_trocador[nivel][laco] = QtWidgets.QLabel(texto)
					label_trocador[nivel][laco].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
					label_trocador[nivel][laco].setStyleSheet("QLabel {font: 10pt 'MS Shell Dlg 2'}")
					lay_laco[nivel][laco].addWidget(label_trocador[nivel][laco])
					lay_laco[nivel][laco].addWidget(botao_remover[nivel][laco].comboo())
					lay_laco[nivel][laco].addWidget(botao_remover[nivel][laco].botaoo())
					lay_nivel[nivel].addLayout(lay_laco[nivel][laco])
				dlg.lista_lacos.lista.addLayout(lay_nivel[nivel])

		dlg.lista_lacos.show()

	def distribuir_calor(trocadores_laco, matriz_completa, trocador_removido):
		dlg.dividir_calor = uic.loadUi("distribuir_calor.ui")

		corrente_quente_vai_remover = matriz_completa[trocadores_laco[trocador_removido]-1][0]
		corrente_fria_vai_remover = matriz_completa[trocadores_laco[trocador_removido]-1][1]
		calor_trocador_removido = matriz_completa[trocadores_laco[trocador_removido]-1][6]
		valores = []
		valores_recomendados = []
		placeholders = [[], []]

		label_trocador = [0] * len(trocadores_laco)
		set_calor = [0] * len(trocadores_laco)
		add_calor = [0] * len(trocadores_laco)
		dtquente = [0] * len(trocadores_laco)
		dtfrio = [0] * len(trocadores_laco)
		lay = [0] * len(trocadores_laco)

		dlg.dividir_calor.trocador_remover.setText("E" + str(trocadores_laco[trocador_removido]) + " Heat Load: " + str(round(calor_trocador_removido, 2)))
		dlg.dividir_calor.horizontalLayout_3.setAlignment(Qt.AlignCenter)
		dlg.dividir_calor.horizontalLayout_4.setAlignment(Qt.AlignCenter)

		for i in range(len(trocadores_laco)):
			if i != trocador_removido:
				label_trocador[i] = QtWidgets.QLabel(dlg.dividir_calor)
				label_trocador[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				label_trocador[i].setAlignment(Qt.AlignCenter)
				set_calor[i] = QtWidgets.QLineEdit(dlg.dividir_calor)
				set_calor[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				set_calor[i].setAlignment(Qt.AlignCenter)
				set_calor[i].setEnabled(False)
				add_calor[i] = QtWidgets.QLineEdit(dlg.dividir_calor)
				add_calor[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				add_calor[i].setAlignment(Qt.AlignCenter)
				add_calor[i].setEnabled(False)
				dtquente[i] = QtWidgets.QLabel(dlg.dividir_calor)
				dtquente[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				dtquente[i].setAlignment(Qt.AlignCenter)
				dtfrio[i] = QtWidgets.QLabel(dlg.dividir_calor)
				dtfrio[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				dtfrio[i].setAlignment(Qt.AlignCenter)
				label_trocador[i].setText("E" + str(trocadores_laco[i]))
				label_trocador[i].setMinimumWidth(95)
				label_trocador[i].setMaximumWidth(95)
				label_trocador[i].setStyleSheet("QLabel {font: 1000 10pt 'MS Shell Dlg 2'}")
				dtquente[i].setText("-")
				dtquente[i].setFont(QFont("Arial", 10))
				dtquente[i].setStyleSheet("QLabel {font: 1000 10pt 'MS Shell Dlg 2'}")
				dtfrio[i].setText("-")
				dtfrio[i].setFont(QFont("Arial", 10))
				dtfrio[i].setStyleSheet("QLabel {font: 1000 10pt 'MS Shell Dlg 2'}")
				lay[i] = QtWidgets.QHBoxLayout()
				lay[i].addWidget(label_trocador[i])
				lay[i].addWidget(set_calor[i])
				lay[i].addWidget(add_calor[i])
				lay[i].addWidget(dtquente[i])
				lay[i].addWidget(dtfrio[i])
				dlg.dividir_calor.trocadores.addLayout(lay[i])
				if matriz_completa[trocadores_laco[i]-1][0] == corrente_quente_vai_remover or matriz_completa[trocadores_laco[i]-1][1] == corrente_fria_vai_remover:
					calor_recomendado = matriz_completa[trocadores_laco[i]-1][6] + calor_trocador_removido
					placeholders[1].append("Ex: " + str(round(calor_trocador_removido, 2)))
				else:
					calor_recomendado = matriz_completa[trocadores_laco[i]-1][6] - calor_trocador_removido
					placeholders[1].append("Ex: -" + str(round(calor_trocador_removido, 2)))
				placeholders[0].append(str(round(calor_recomendado, 2)) + " (suggested)")
				valores.append(calor_recomendado)
				valores_recomendados.append(calor_recomendado)
			else:
				valores.append(0)
				valores_recomendados.append(0)
				placeholders[0].append(0)
				placeholders[1].append(0)

		for i in range(len(set_calor)):
			dlg.dividir_calor.radio_add.toggled.connect(lambda: liberar_bloquear([set_calor, add_calor], "add", trocador_removido, placeholders))
			dlg.dividir_calor.radio_set.toggled.connect(lambda: liberar_bloquear([set_calor, add_calor], "setar", trocador_removido, placeholders))
			dlg.dividir_calor.padrao.toggled.connect(lambda: liberar_bloquear([set_calor, add_calor], "padrão", trocador_removido, placeholders))

		dlg.dividir_calor.show()
		dlg.dividir_calor.prever.clicked.connect(lambda: distribuiu([set_calor, add_calor], valores, valores_recomendados, trocadores_laco, matriz_completa, trocador_removido, dtquente, dtfrio))

		def distribuiu(valor_trocador, valores, valores_recomendados, trocadores_laco, matriz_completa_naomuda, trocador_removido, dtquente, dtfrio):
			global ja_violava, layh, novas_violacoes, dt_quente_novo, dt_frio_novo
			for i in range(len(trocadores_laco)):
				try:
					if dlg.dividir_calor.padrao.isChecked():
						valores[i] = valores_recomendados[i]
					elif dlg.dividir_calor.radio_set.isChecked():
						if i != trocador_removido:
							valores[i] = float(valor_trocador[0][i].text().replace(",", "."))
						else:
							valores[i] = 0
					elif dlg.dividir_calor.radio_add.isChecked():
						if i != trocador_removido:
							valores[i] = float(valor_trocador[1][i].text().replace(",", ".")) + matriz_completa_naomuda[trocadores_laco[i]-1][6]
						else:
							valores[i] = 0
				except:
					QMessageBox.about(dlg, "Error!", "Specify all the values or select the standard method.")
					return

			matriz_completa = nao_sacrificar_matriz(matriz_completa_naomuda)

			corrente_quente = matriz_completa[trocadores_laco[trocador_removido]-1][0]
			corrente_fria = matriz_completa[trocadores_laco[trocador_removido]-1][1]
			ramo_quente = matriz_completa[trocadores_laco[trocador_removido]-1][2]
			ramo_frio = matriz_completa[trocadores_laco[trocador_removido]-1][3]
			estagio = matriz_completa[trocadores_laco[trocador_removido]-1][5]

			novas_divisoes = remover_ramo(matriz_completa, corrente_quente, corrente_fria, ramo_quente, ramo_frio, estagio, excecao=(trocadores_laco[trocador_removido]-1))

			for i in range(len(trocadores_laco)):
				matriz_completa[trocadores_laco[i]-1][6] = valores[i]

			for trocador in matriz_completa:
				if trocador[6] == 0:
					estagio = trocador[5]
					partir_estagio = trocador[4]
					matriz_completa.pop(matriz_completa.index(trocador))

			for trocador in matriz_completa:
				if trocador[4] > partir_estagio and trocador[5] == estagio:
					trocador[4] -= 1

			for trocador in matriz_completa:
				matriz_teste, violou, trocadores_violados = inserir_trocador_ev("oi", trocador[:7])

			matriz_completa = nao_sacrificar_matriz(matriz_teste)

			viola_agora = []
			for trocador in matriz_completa:
				if trocador[7] - trocador[8] < dTmin or trocador[9] - trocador[10] < dTmin:
					if not matriz_completa.index(trocador)+1 in trocadores_laco:
						viola_agora.append(matriz_completa.index(trocador))

			dlg.dividir_calor.botaodone.setEnabled(True)
			for i in range(len(trocadores_laco)):
				if i != trocador_removido:
					if i < trocador_removido:
						dt_quente = matriz_completa[trocadores_laco[i]-1][7]-matriz_completa[trocadores_laco[i]-1][8]
						dt_frio = matriz_completa[trocadores_laco[i]-1][9]-matriz_completa[trocadores_laco[i]-1][10]
					else:
						dt_quente = matriz_completa[trocadores_laco[i]-2][7]-matriz_completa[trocadores_laco[i]-2][8]
						dt_frio = matriz_completa[trocadores_laco[i]-2][9]-matriz_completa[trocadores_laco[i]-2][10]
					dtquente[i].setText(str('{:.2f}'.format(round(dt_quente, 2))))
					dtfrio[i].setText(str('{:.2f}'.format(round(dt_frio, 2))))
					if dt_quente < 0 or dt_frio < 0:
						# dlg.dividir_calor.botaodone.setEnabled(False)
						pass
					if dt_quente < dTmin:
						dtquente[i].setStyleSheet("QLabel {color: red; font: 1000 10pt 'MS Shell Dlg 2'}")
					else:
						dtquente[i].setStyleSheet("QLabel {color: black; font: 1000 10pt 'MS Shell Dlg 2'}")
					if dt_frio < dTmin:
						dtfrio[i].setStyleSheet("QLabel {color: red; font: 1000 10pt 'MS Shell Dlg 2'}")
					else:
						dtfrio[i].setStyleSheet("QLabel {color: black; font: 1000 10pt 'MS Shell Dlg 2'}")

			try:
				if ja_violava[0] != "None.":
					for lay in range(len(ja_violava)-1, -1, -1):
						layh[lay].removeWidget(novas_violacoes[lay])
						layh[lay].removeWidget(dt_quente_novo[lay])
						layh[lay].removeWidget(dt_frio_novo[lay])
						novas_violacoes[lay].setParent(None)
						dt_quente_novo[lay].setParent(None)
						dt_frio_novo[lay].setParent(None)
						dlg.dividir_calor.outras_violacoes.removeItem(layh[lay])
				else:
					dlg.dividir_calor.outras_violacoes.removeWidget(novas_violacoes)
					novas_violacoes.setParent(None)
			except:
				pass

			if len(viola_agora) != 0:
				novas_violacoes = [0] * len(viola_agora)
				dt_quente_novo = [0] * len(viola_agora)
				dt_frio_novo = [0] * len(viola_agora)
				layh = [0] * len(viola_agora)
				for i in range(len(viola_agora)):
					novas_violacoes[i] = QtWidgets.QLabel("E" + str(viola_agora[i]+1))
					novas_violacoes[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
					novas_violacoes[i].setAlignment(Qt.AlignCenter)
					novas_violacoes[i].setStyleSheet("QLabel {font: 1000 10pt 'MS Shell Dlg 2'}")
					dt_quente_novo[i] = QtWidgets.QLabel(str('{:.2f}'.format(round(matriz_completa[viola_agora[i]][7] - matriz_completa[viola_agora[i]][8], 2))))
					dt_quente_novo[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
					dt_quente_novo[i].setAlignment(Qt.AlignCenter)
					if matriz_completa[viola_agora[i]][7] - matriz_completa[viola_agora[i]][8] < dTmin:
						dt_quente_novo[i].setStyleSheet("QLabel {color: red; font: 1000 10pt 'MS Shell Dlg 2'}")
					else:
						dt_quente_novo[i].setStyleSheet("QLabel {color: black; font: 1000 10pt 'MS Shell Dlg 2'}")
					dt_frio_novo[i] = QtWidgets.QLabel(str('{:.2f}'.format(round(matriz_completa[viola_agora[i]][9] - matriz_completa[viola_agora[i]][10], 2))))
					dt_frio_novo[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
					dt_frio_novo[i].setAlignment(Qt.AlignCenter)
					if matriz_completa[viola_agora[i]][9] - matriz_completa[viola_agora[i]][10] < dTmin:
						dt_frio_novo[i].setStyleSheet("QLabel {color: red; font: 1000 10pt 'MS Shell Dlg 2'}")
					else:
						dt_frio_novo[i].setStyleSheet("QLabel {color: black; font: 1000 10pt 'MS Shell Dlg 2'}")
					layh[i] = QtWidgets.QHBoxLayout()
					layh[i].addWidget(novas_violacoes[i])
					layh[i].addWidget(dt_quente_novo[i])
					layh[i].addWidget(dt_frio_novo[i])
					dlg.dividir_calor.outras_violacoes.addLayout(layh[i])
			else:
				novas_violacoes = QtWidgets.QLabel("None.")
				novas_violacoes.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				novas_violacoes.setAlignment(Qt.AlignCenter)
				novas_violacoes.setStyleSheet("QLabel {font: 1000 10pt 'MS Shell Dlg 2'}")
				dlg.dividir_calor.outras_violacoes.addWidget(novas_violacoes)
				viola_agora.append("None.")

			ja_violava = []
			for i in range(len(viola_agora)):
				ja_violava.append(viola_agora[i])

			dlg.dividir_calor.botaodone.clicked.connect(lambda: done(matriz_completa, novas_divisoes))
			dlg.dividir_calor.botaoundone.clicked.connect(lambda: undone(matriz_completa_naomuda, divisoes))

			def done(matriz_completa_done, novas_divisoes):
				global matriz_evolucao, desenho_em_dia_ambas, divisoes_ev
				matriz_evolucao = nao_sacrificar_matriz(matriz_completa_done)
				divisoes_ev = nao_sacrificar_matriz(novas_divisoes)
				dlg.dividir_calor.close()
				desenho_em_dia_ambas = False
				desenhar_rede(correntes_quentes, correntes_frias, "ambas")
				dlg.trocador_editar.removeItem(dlg.trocador_editar.count()-1)
				dlg.trocador_path.removeItem(dlg.trocador_path.count()-1)
				if todos:
					evolucao([], [], "todos", True)
				else:
					evolucao([], [], nivel)

			def undone(matriz_completa_undone, novas_divisoes):
				global matriz_evolucao, divisoes_ev
				remover_todos_ev()
				for trocador in matriz_completa_undone:
					matriz_completa, violou, trocadores_violados = inserir_trocador_ev("oi", trocador[:7])
				matriz_evolucao = nao_sacrificar_matriz(matriz_completa)
				divisoes_ev = nao_sacrificar_matriz(novas_divisoes)
				dlg.dividir_calor.close()

		def liberar_bloquear(valor_trocador, acao, trocador_removido, placeholders):
			for i in range(len(valor_trocador[0])):
				if i != trocador_removido:
					if acao == "setar":
						valor_trocador[1][i].setEnabled(False)
						valor_trocador[0][i].setEnabled(True)
						valor_trocador[0][i].setPlaceholderText(placeholders[0][i])
						valor_trocador[1][i].setPlaceholderText("")
					elif acao == "add":
						valor_trocador[1][i].setEnabled(True)
						valor_trocador[0][i].setEnabled(False)
						valor_trocador[1][i].setPlaceholderText(placeholders[1][i])
						valor_trocador[0][i].setPlaceholderText("")
					else:
						valor_trocador[1][i].setEnabled(False)
						valor_trocador[0][i].setEnabled(False)
						valor_trocador[0][i].setPlaceholderText("")
						valor_trocador[1][i].setPlaceholderText("")

	global matriz_evolucao, n_quentes, n_frias, desenho_em_dia_ambas, divisoes_ev

	if jogar_evolucao:
		matriz_acima = nao_sacrificar_matriz(matriz_acima_naomuda)
		matriz_abaixo = nao_sacrificar_matriz(matriz_abaixo_naomuda)
		matriz = criar_rede_completa(matriz_acima, matriz_abaixo, primeiro=True)
		matriz_evolucao = nao_sacrificar_matriz(matriz)
		trocadores, n_quentes, n_frias = criar_matriz(matriz_acima, matriz_abaixo)
		desenho_em_dia_ambas = False
		divisoes_ev = nao_sacrificar_matriz(divisoes)
		desenhar_rede(correntes_quentes, correntes_frias, "ambas")
		if dlg.trocador_editar.count() > 0:
			dlg.trocador_editar.clear()
			dlg.trocador_path.clear()
		for i in range(len(matriz_evolucao)):
			dlg.trocador_editar.addItem("E" + str(i+1))
			dlg.trocador_path.addItem("E" + str(i+1))
	else:
		matriz_acima_nm = []
		matriz_abaixo_nm = []
		for trocador in matriz_evolucao:
			if trocador[5] == 1:
				matriz_acima_nm.append(trocador)
			elif trocador[5] == 2:
				matriz_abaixo_nm.append(trocador)
		matriz_acima = nao_sacrificar_matriz(matriz_acima_nm)
		matriz_abaixo = nao_sacrificar_matriz(matriz_abaixo_nm)
		matriz = criar_rede_completa(matriz_acima, matriz_abaixo)
		matriz_evolucao = nao_sacrificar_matriz(matriz)
		trocadores, n_quentes, n_frias = criar_matriz(matriz_acima, matriz_abaixo)
	incidencia = criar_incidencia(trocadores, n_quentes, n_frias)
	dlg.sugerir_path.clicked.connect(lambda: calcular_recomendado_violacao(dlg, matriz_evolucao[dlg.trocador_path.currentIndex()]))
	if todos:
		trocadores_laco = []
		for n in range(min(nhot, ncold)):
			trocadores_laco.append(sorted(lacos(incidencia, trocadores, n, todos)))
			if len(trocadores_laco[-1]) == 0:
				trocadores_laco.pop(-1)
	else:
		trocadores_laco = sorted(lacos(incidencia, trocadores, nivel, todos))
	if todos:
		interface_todos(trocadores_laco, matriz_evolucao)
	else:
		coisas_interface(trocadores_laco, matriz_evolucao)
		if trocadores_laco == ["None "] and nivel+1 <= min(n_quentes, n_frias):
			dlg.nivel.setCurrentIndex(nivel)
			evolucao([], [], nivel+1)

def editar_calor(matriz_naomuda, trocador, calor, path=False):
	global desenho_em_dia_ambas, matriz_evolucao, n_quentes, n_frias, divisoes_ev
	if calor == 0 and path:
		QMessageBox.about(dlg, "Error!", "You must Specify a Heat Load greater than 0")
		return
	matriz = nao_sacrificar_matriz(matriz_naomuda)
	remover_todos_ev()
	ramo = [False, False]
	if (calor == 0 and not path) or ((matriz_naomuda[trocador][6] - calor == 0) and path):
		corrente_quente = matriz_naomuda[trocador][0]
		corrente_fria = matriz_naomuda[trocador][1]
		ramo_quente = matriz_naomuda[trocador][2]
		ramo_frio = matriz_naomuda[trocador][3]
		estagio = matriz_naomuda[trocador][5]
		dlg.trocadores_loop.setText("Requires new search")
		dlg.remover.setEnabled(False)
		divisoes_ev, ramo = remover_ramo(matriz, corrente_quente, corrente_fria, ramo_quente, ramo_frio, estagio, excecao=trocador)
	desenho_em_dia_ambas = False
	if not path:
		if calor == 0:
			for i in range(len(matriz)):
				if matriz[trocador][4] < matriz[i][4] and matriz[trocador][5] == matriz[i][5]:
					matriz[i][4] -= 1
			matriz.pop(trocador)
			dlg.trocador_editar.removeItem(dlg.trocador_editar.count()-1)
			dlg.trocador_path.removeItem(dlg.trocador_path.count()-1)
		else:
			matriz[trocador][6] = calor
		for trocadorr in matriz:
			matriz_teste, violou, trocadores_violados = inserir_trocador_ev("oi", trocadorr[:7])
		matriz_evolucao = nao_sacrificar_matriz(matriz_teste)
	else:
		matriz_evolucao = nao_sacrificar_matriz(utilidade(matriz_naomuda, [trocador, calor], path=True, ramo=ramo))
		for i in range(2):
			dlg.trocador_path.addItem("E" + str(dlg.trocador_path.count()+1))
			dlg.trocador_editar.addItem("E" + str(dlg.trocador_editar.count()+1))

	desenhar_rede(correntes_quentes, correntes_frias, "ambas")

def utilidade(matriz_naomuda, dados, path=False, ramo=[False, False]):
	global matriz_evolucao, n_quentes, n_frias, desenho_em_dia_ambas
	matriz = nao_sacrificar_matriz(matriz_naomuda)
	if path:
		trocador = dados[0]
		calor = dados[1]
		corrente_quente = matriz_naomuda[trocador][0]
		corrente_fria = matriz_naomuda[trocador][1]
		if ramo[0]:
			sub_quente = 1
		else:
			sub_quente = matriz_naomuda[trocador][2]
		if ramo[1]:
			sub_fria = 1
		else:
			sub_fria = matriz_naomuda[trocador][3]
		matriz[trocador][6] = matriz_naomuda[trocador][6] - calor
		if round(matriz[trocador][6], 2) == 0:
			matriz.pop(trocador)
			dlg.trocador_path.removeItem(dlg.trocador_path.count()-1)
			dlg.trocador_editar.removeItem(dlg.trocador_editar.count()-1)
		tipo = ""
		dlg.calor_path.clear()
		dlg.calor_path.setPlaceholderText("-")
	else:
		oi = dlg.comboutil.currentText().split(" ")
		corrente = int(oi[1])
		if oi[0] == "Hot":
			tipo = "Cold"
			calor = calor_atual_quente_ev[corrente-1]
		else:
			tipo = "Hot"
			calor = calor_atual_frio_ev[corrente-1]
	if tipo == "Hot" or path:
		for trocadorr in matriz:
			if trocadorr[5] == 2:
				parar = matriz.index(trocadorr)
				break
			else:
				trocadorr[4] += 1
		matriz_reserva = nao_sacrificar_matriz(matriz[parar:])
		for i in range(parar, len(matriz)):
			matriz.pop(-1)
		if path:
			matriz.append([n_quentes, corrente_fria, 1, sub_fria, 1, 1, calor])
		else:
			matriz.append([n_quentes, corrente, 1, 1, 1, 1, calor])
		for reserva in matriz_reserva:
			matriz.append(reserva)
	else:
		matriz.append([corrente, n_frias, 1, 1, matriz[-1][4]+1, 2, calor])
	if path:
		matriz.append([corrente_quente, n_frias, sub_quente, 1, matriz[-1][4]+1, 2, calor])
	else:
		remover_todos_ev()
	for trocadorr in matriz:
		matriz_teste, violou, trocadores_violados = inserir_trocador_ev("oi", trocadorr[:7])
	if path:
		return matriz_teste
	else:
		desenho_em_dia_ambas = False
		matriz_evolucao = nao_sacrificar_matriz(matriz_teste)
		desenhar_rede(correntes_quentes, correntes_frias, "ambas")

def remover_ramo(matriz_completa, corrente_quente, corrente_fria, ramo_quente, ramo_frio, estagio, excecao=-1):
	ainda_tem_quente = False
	ainda_tem_frio = False
	ramoo = [True, True]
	for trocador in matriz_completa:
		if matriz_completa.index(trocador) != excecao and trocador[5] == estagio:
			if ramo_quente == trocador[2] and corrente_quente == trocador[0]:
				ainda_tem_quente = True
				ramoo[0] = False
			if ramo_frio == trocador[3] and corrente_fria == trocador[1]:
				ainda_tem_frio = True
				ramoo[1] = False

	remover_todos_ev()

	novas_divisoes = nao_sacrificar_matriz(divisoes_ev)

	if not ainda_tem_quente:
		for divisao in novas_divisoes:
			if divisao[0] == "Q" and divisao[1] == estagio and divisao[2] == corrente_quente:
				total = 0
				for ramo in range(divisao[3]):
					if ramo+1 != ramo_quente:
						total += divisao[4][ramo]
				fracao = []
				for ramo in range(divisao[3]):
					if ramo+1 != ramo_quente:
						proporcao = divisao[4][ramo] / total
						fracao.append(divisao[4][ramo] + proporcao * divisao[4][ramo_quente-1])
						if ramo+1 > ramo_quente:
							for trocador in matriz_completa:
								if trocador[0] == corrente_quente and trocador[2] == ramo+1 and trocador[5] == estagio:
									trocador[2] -= 1
				divisao_de_correntes_ev("Q", estagio, corrente_quente, len(fracao), fracao)
				divisao = ["Q", estagio, corrente_fria, len(fracao), fracao]

	if not ainda_tem_frio:
		for divisao in novas_divisoes:
			if divisao[0] == "F" and divisao[1] == estagio and divisao[2] == corrente_fria:
				total = 0
				for ramo in range(divisao[3]):
					if ramo+1 != ramo_frio:
						total += divisao[4][ramo]
				fracao = []
				for ramo in range(divisao[3]):
					if ramo+1 != ramo_frio:
						proporcao = divisao[4][ramo] / total
						fracao.append(divisao[4][ramo] + proporcao * divisao[4][ramo_frio-1])
						if ramo+1 > ramo_frio:
							for trocador in matriz_completa:
								if trocador[1] == corrente_fria and trocador[3] == ramo+1 and trocador[5] == estagio:
									trocador[3] -= 1
				divisao_de_correntes_ev("F", estagio, corrente_fria, len(fracao), fracao)
				divisao = ["F", estagio, corrente_fria, len(fracao), fracao]

	return novas_divisoes, ramoo


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
					dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0[corrente], 2)))))
					if corrente_quente_presente_acima[corrente]:
						dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente[corrente][sub], 2)))))
						dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf_acima[corrente], 2)))))
						dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente_sub[corrente][sub], 2)))))
					else:
						dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_3.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0[corrente], 2)))))
				if corrente_quente_presente_acima[corrente]:
					dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente_mesclada[corrente], 2)))))
					dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf_acima[corrente], 2)))))
					dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente[corrente], 2)))))
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
			dlg.tableWidget_3.setItem(corrente, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0[corrente], 2)))))
			if corrente_quente_presente_acima[corrente]:
				dlg.tableWidget_3.setItem(corrente, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente_mesclada[corrente], 2)))))
				dlg.tableWidget_3.setItem(corrente, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf_acima[corrente], 2)))))
				dlg.tableWidget_3.setItem(corrente, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente[corrente], 2)))))
			else:
				dlg.tableWidget_3.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_3.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_3.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_3.setItem(corrente, 4, QTableWidgetItem("-"))

	try:
		for corrente in range(nhot*ncold):
			for j in range(5):
				item = dlg.tableWidget_3.item(corrente, j)
				item.setTextAlignment(Qt.AlignCenter)
	except:
		pass

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
					dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf[corrente], 2)))))
					if corrente_fria_presente_acima[corrente]:
						dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria[corrente][sub], 2)))))
						dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0_acima[corrente], 2)))))
						dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio_sub[corrente][sub], 2)))))
					else:
						dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_4.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf[corrente], 2)))))
				if corrente_fria_presente_acima[corrente]:
					dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria_mesclada[corrente], 2)))))
					dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0_acima[corrente], 2)))))
					dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio[corrente], 2)))))
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
			dlg.tableWidget_4.setItem(corrente, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf[corrente], 2)))))
			if corrente_fria_presente_acima[corrente]:
				dlg.tableWidget_4.setItem(corrente, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria_mesclada[corrente], 2)))))
				dlg.tableWidget_4.setItem(corrente, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0_acima[corrente], 2)))))
				dlg.tableWidget_4.setItem(corrente, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio[corrente], 2)))))
			else:
				dlg.tableWidget_4.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_4.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_4.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_4.setItem(corrente, 4, QTableWidgetItem("-"))

	try:
		for corrente in range(nhot*ncold):
			for j in range(5):
				item = dlg.tableWidget_4.item(corrente, j)
				item.setTextAlignment(Qt.AlignCenter)
	except:
		pass

	dlg.tableWidget_2.setRowCount(len(matriz_armazenada))
	if len(matriz_armazenada) > 0:
		for trocador in range(0, len(matriz_armazenada)):
			dlg.tableWidget_2.setItem(trocador, 0, QTableWidgetItem(str(matriz_armazenada[trocador][0]))) #chot
			dlg.tableWidget_2.setItem(trocador, 1, QTableWidgetItem(str(matriz_armazenada[trocador][1]))) #ccold
			dlg.tableWidget_2.setItem(trocador, 2, QTableWidgetItem(str(matriz_armazenada[trocador][2]))) #sbhot
			dlg.tableWidget_2.setItem(trocador, 3, QTableWidgetItem(str(matriz_armazenada[trocador][3]))) #sbcold
			dlg.tableWidget_2.setItem(trocador, 4, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][6], 2))))) #calor trocador
			dlg.tableWidget_2.setItem(trocador, 5, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][7], 2))))) #thin
			dlg.tableWidget_2.setItem(trocador, 6, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][8], 2))))) #tcout
			dlg.tableWidget_2.setItem(trocador, 7, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][9], 2))))) #Thout
			dlg.tableWidget_2.setItem(trocador, 8, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][10], 2))))) #Tcin
			dlg.tableWidget_2.setItem(trocador, 9, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][11], 2))))) #fração hot
			dlg.tableWidget_2.setItem(trocador, 10, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][12], 2))))) #fraçao cold
			for j in range(11):
				item = dlg.tableWidget_2.item(trocador, j)
				item.setTextAlignment(Qt.AlignCenter)

	if len(utilidades) > 0:
		dlg.tableWidget_2.setRowCount(len(matriz_armazenada) + len(utilidades))
		for utilidade in range(0, len(utilidades)):
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 0, QTableWidgetItem(str("Hot Utility")))
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 1, QTableWidgetItem(str(utilidades[utilidade][0])))
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 4, QTableWidgetItem(str('{:.2f}'.format(round(utilidades[utilidade][1], 2)))))
			for j in range(11):
				if j == 0 or j == 1 or j == 4:
					item = dlg.tableWidget_2.item(utilidade + len(matriz_armazenada), j)
					item.setTextAlignment(Qt.AlignCenter)

def inserir_teste():
	global subestagio_trocador, desenho_em_dia, desenho_em_dia_ambas, violados_acima, matriz_armazenada
	subestagio_trocador += 1
	dados_do_trocador = ler_dados(dlg, subestagio_trocador)
	matriz_armazenada, inseriu = inserir_trocador(dlg, dados_do_trocador)
	if inseriu:
		if (matriz_armazenada[-1][7] - matriz_armazenada[-1][8]) < dTmin or (matriz_armazenada[-1][9] - matriz_armazenada[-1][10]) < dTmin:
			trocador_violado = matriz_armazenada[-1][:6]
			trocador_violado.append(matriz_armazenada[-1][7] - matriz_armazenada[-1][8])
			trocador_violado.append(matriz_armazenada[-1][9] - matriz_armazenada[-1][10])
			violou_dtmin(trocador_violado, "above", dados_do_trocador)
			violados_acima.append(subestagio_trocador)
		printar()
		checaresgotadosacima()
		dlg.trocador_acima.addItem("E" + str(subestagio_trocador))
		dlg.trocador_acima.setCurrentIndex(dlg.trocador_acima.count()-1)
		desenho_em_dia = False
		desenho_em_dia_ambas = False
		atualizar_desenho("acima")
	else:
		subestagio_trocador -= 1
		return

def remover_teste():
	global subestagio_trocador, desenho_em_dia, desenho_em_dia_ambas
	indice_remover = dlg.tableWidget_2.currentRow()
	if indice_remover == -1:
		indice_remover = dlg.trocador_acima.currentIndex()
	if indice_remover >= len(matriz_armazenada) - 1:
		remover_anteriores("acima", indice_remover, True)
	else:
		remover_anteriores("acima", indice_remover)

def utilidade_teste_acima():
	global desenho_em_dia, desenho_em_dia_ambas, utilidades
	if dlg.tab_acima.currentIndex() == 1:
		corrente = int(dlg.comboBox_10.currentText())
	else:
		corrente = int(dlg.corrente_acima.currentIndex()+1)
	try:
		utilidades = adicionar_utilidade(dlg, corrente)
		utilidades.sort()
	except:
		print("erro utilidade teste acima")
	printar()
	checaresgotadosacima()
	dlg.trocador_acima.addItem("H" + str(len(utilidades)))
	dlg.trocador_acima.setCurrentIndex(dlg.trocador_acima.count()-1)
	desenho_em_dia = False
	desenho_em_dia_ambas = False
	if dlg.tab_acima.currentIndex() == 0:
		desenhar_rede(correntes_quentes, correntes_frias, "acima", True)

def calcular_calor_teste():
	dlg.TempLoadAbove=uic.loadUi("TempLoad.ui")
	dlg.TempLoadAbove.show()
	dlg.TempLoadAbove.radioButton_2.setText("Inlet Hot Temperature")
	dlg.TempLoadAbove.radioButton.setText("Outlet Cold Temperature")

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
		dlg.corrente_acima.setEnabled(True)
		dlg.addutil_acima.setEnabled(True)
	else:
		dlg.comboBox_10.setEnabled(False)
		dlg.pushButton_8.setEnabled(False)
		dlg.corrente_acima.setEnabled(False)
		dlg.addutil_acima.setEnabled(False)

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
		dlg.corrente_acima.setEnabled(False)
		dlg.addutil_acima.setEnabled(False)

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
					dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0_abaixo[corrente], 2)))))
					if corrente_quente_presente_abaixo[corrente]:
						dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente_abaixo[corrente][sub], 2)))))
						dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf[corrente], 2)))))
						dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente_sub_abaixo[corrente][sub], 2)))))
					else:
						dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_15.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0_abaixo[corrente], 2)))))
				if corrente_quente_presente_abaixo[corrente]:
					dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente_mesclada_abaixo[corrente], 2)))))
					dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf[corrente], 2)))))
					dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente_abaixo[corrente], 2)))))
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
			dlg.tableWidget_15.setItem(corrente, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0_abaixo[corrente], 2)))))
			if corrente_quente_presente_abaixo[corrente]:
				dlg.tableWidget_15.setItem(corrente, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente_mesclada_abaixo[corrente], 2)))))
				dlg.tableWidget_15.setItem(corrente, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf[corrente], 2)))))
				dlg.tableWidget_15.setItem(corrente, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente_abaixo[corrente], 2)))))
			else:
				dlg.tableWidget_15.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_15.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_15.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_15.setItem(corrente, 4, QTableWidgetItem("-"))

	try:
		for corrente in range(nhot*ncold):
			for j in range(5):
				item = dlg.tableWidget_15.item(corrente, j)
				item.setTextAlignment(Qt.AlignCenter)
	except:
		pass

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
					dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf_abaixo[corrente], 2)))))
					if corrente_fria_presente_abaixo[corrente]:
						dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria_abaixo[corrente][sub], 2)))))
						dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0[corrente], 2)))))
						dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio_sub_abaixo[corrente][sub], 2)))))
					else:
						dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_17.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf_abaixo[corrente], 2)))))
				if corrente_fria_presente_abaixo[corrente]:
					dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria_mesclada_abaixo[corrente], 2)))))
					dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0[corrente], 2)))))
					dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio_abaixo[corrente], 2)))))
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
			dlg.tableWidget_17.setItem(corrente, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf_abaixo[corrente], 2)))))
			if corrente_fria_presente_abaixo[corrente]:
				dlg.tableWidget_17.setItem(corrente, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria_mesclada_abaixo[corrente], 2)))))
				dlg.tableWidget_17.setItem(corrente, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0[corrente], 2)))))
				dlg.tableWidget_17.setItem(corrente, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio_abaixo[corrente], 2)))))
			else:
				dlg.tableWidget_17.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_17.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_17.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_17.setItem(corrente, 4, QTableWidgetItem("-"))

	try:
		for corrente in range(nhot*ncold):
			for j in range(5):
				item = dlg.tableWidget_17.item(corrente, j)
				item.setTextAlignment(Qt.AlignCenter)
	except:
		pass

	dlg.tableWidget_14.setRowCount(len(matriz_trocadores_abaixo))
	if len(matriz_trocadores_abaixo) > 0:
		for trocador in range(0, len(matriz_trocadores_abaixo)):
			dlg.tableWidget_14.setItem(trocador, 0, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][0]))) #chot
			dlg.tableWidget_14.setItem(trocador, 1, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][1]))) #ccold
			dlg.tableWidget_14.setItem(trocador, 2, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][2]))) #sbhot
			dlg.tableWidget_14.setItem(trocador, 3, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][3]))) #sbcold
			dlg.tableWidget_14.setItem(trocador, 4, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][6], 2))))) # calor trocado
			dlg.tableWidget_14.setItem(trocador, 5, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][9], 2))))) #Thin
			dlg.tableWidget_14.setItem(trocador, 6, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][10], 2))))) #Tcout
			dlg.tableWidget_14.setItem(trocador, 7, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][7], 2))))) #Thout
			dlg.tableWidget_14.setItem(trocador, 8, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][8], 2))))) #Tcin
			dlg.tableWidget_14.setItem(trocador, 9, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][11], 2))))) #fração hot
			dlg.tableWidget_14.setItem(trocador, 10, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][12], 2))))) #fraçao cold
			for j in range(11):
				item = dlg.tableWidget_14.item(trocador, j)
				item.setTextAlignment(Qt.AlignCenter)

	if len(utilidades_abaixo) > 0:
		dlg.tableWidget_14.setRowCount(len(matriz_trocadores_abaixo) + len(utilidades_abaixo))
		for utilidade in range(0, len(utilidades_abaixo)):
			dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 1, QTableWidgetItem(str("Cold Utility")))
			dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 0, QTableWidgetItem(str(utilidades_abaixo[utilidade][0])))
			dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 4, QTableWidgetItem(str('{:.2f}'.format(round(utilidades_abaixo[utilidade][1], 2)))))
			for j in range(11):
				if j == 0 or j == 1 or j == 4:
					item = dlg.tableWidget_14.item(utilidade + len(matriz_trocadores_abaixo), j)
					item.setTextAlignment(Qt.AlignCenter)

def inserir_teste_abaixo():
	global subestagio_trocador_abaixo, desenho_em_dia_abaixo, desenho_em_dia_ambas, violados_abaixo, matriz_trocadores_abaixo
	subestagio_trocador_abaixo += 1
	dados_do_trocador = ler_dados_abaixo(dlg, subestagio_trocador_abaixo)
	matriz_trocadores_abaixo, inseriu = inserir_trocador_abaixo(dlg, dados_do_trocador)
	if inseriu:
		if (matriz_trocadores_abaixo[-1][7] - matriz_trocadores_abaixo[-1][8]) < dTmin or (matriz_trocadores_abaixo[-1][9] - matriz_trocadores_abaixo[-1][10]) < dTmin:
			trocador_violado = matriz_trocadores_abaixo[-1][:6]
			trocador_violado.append(matriz_trocadores_abaixo[-1][7] - matriz_trocadores_abaixo[-1][8])
			trocador_violado.append(matriz_trocadores_abaixo[-1][9] - matriz_trocadores_abaixo[-1][10])
			violou_dtmin(trocador_violado, "below", dados_do_trocador)
			violados_abaixo.append(subestagio_trocador_abaixo)
		printar_abaixo()
		checaresgotadosabaixo()
		dlg.trocador_abaixo.addItem("E" + str(subestagio_trocador_abaixo))
		dlg.trocador_abaixo.setCurrentIndex(dlg.trocador_abaixo.count()-1)
		desenho_em_dia_abaixo = False
		desenho_em_dia_ambas = False
		atualizar_desenho("abaixo")
	else:
		subestagio_trocador_abaixo -= 1
		return

def remover_teste_abaixo():
	global subestagio_trocador_abaixo, desenho_em_dia_abaixo, desenho_em_dia_ambas, matriz_trocadores_abaixo
	indice_remover = dlg.tableWidget_14.currentRow()
	if indice_remover == -1:
		indice_remover = dlg.trocador_abaixo.currentIndex()
	if indice_remover >= len(matriz_trocadores_abaixo) - 1:
		remover_anteriores("abaixo", indice_remover, True)
	else:
		remover_anteriores("abaixo", indice_remover)

def utilidade_teste_abaixo():
	global desenho_em_dia_abaixo, desenho_em_dia_ambas, utilidades_abaixo
	if dlg.tab_abaixo.currentIndex() == 1:
		corrente = int(dlg.comboBox_43.currentText())
	else:
		corrente = int(dlg.corrente_abaixo.currentIndex()+1)
	try:
		utilidades_abaixo = adicionar_utilidade_abaixo(dlg, corrente)
		utilidades_abaixo.sort()
	except:
		print("utilidade teste abaixo")
	printar_abaixo()
	checaresgotadosabaixo()
	dlg.trocador_abaixo.addItem("C" + str(len(utilidades_abaixo)))
	dlg.trocador_abaixo.setCurrentIndex(dlg.trocador_abaixo.count()-1)
	desenho_em_dia_abaixo = False
	desenho_em_dia_ambas = False
	if dlg.tab_abaixo.currentIndex() == 0:
		desenhar_rede(correntes_quentes, correntes_frias, "abaixo", True)

def calcular_calor_abaixo():
	dlg.TempLoadBelow = uic.loadUi("TempLoad.ui")
	dlg.TempLoadBelow.show()
	dlg.TempLoadBelow.radioButton_2.setText("Outlet Hot Temperature")
	dlg.TempLoadBelow.radioButton.setText("Inlet Cold Temperature")

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
		if calor_atual_quente_abaixo[corrente] == 0:
			contadordutyhot += 1
	for corrente in range(ncold):
		if calor_atual_frio_abaixo[corrente] == 0:
			contadordutycold += 1

	objetivo_quente = nhot
	objetivo_frio = ncold

	if contadordutyhot == objetivo_quente:
		dlg.comboBox_44.setEnabled(True)
		dlg.pushButton_21.setEnabled(True)
	else:
		dlg.comboBox_44.setEnabled(False)
		dlg.pushButton_21.setEnabled(False)

	if contadordutycold == objetivo_frio:
		dlg.comboBox_43.setEnabled(True)
		dlg.pushButton_20.setEnabled(True)
		dlg.corrente_abaixo.setEnabled(True)
		dlg.addutil_abaixo.setEnabled(True)
	else:
		dlg.comboBox_43.setEnabled(False)
		dlg.pushButton_20.setEnabled(False)
		dlg.corrente_abaixo.setEnabled(False)
		dlg.addutil_abaixo.setEnabled(False)

	if contadordutyhot == objetivo_quente and contadordutycold == objetivo_frio:
		dlg.comboBox_43.setEnabled(False)
		dlg.comboBox_44.setEnabled(False)
		dlg.pushButton_20.setEnabled(False)
		dlg.pushButton_21.setEnabled(False)
		dlg.corrente_abaixo.setEnabled(False)
		dlg.addutil_abaixo.setEnabled(False)



#inutilidades porem depende
def suprir_9_correntes():
	global matriz_armazenada, matriz_trocadores_abaixo

	if nhot == 2 and ncold == 2:
		acima = [[1, 1, 1, 1, 1, 1, 150], [1, 1, 2, 2, 2, 1, 150], [2, 2, 2, 2, 4, 1, 60], [2, 2, 1, 1, 3, 1, 60], [1], [2]]
		abaixo = [[1, 2, 1, 1, 1, 1, 15], [1, 2, 2, 2, 2, 1, 15], [2, 2, 2, 2, 4, 1, 5], [2, 2, 1, 1, 3, 1, 5], [2]]
		#divtype, estagio, corrente, quantidade, fracao
		divisao_de_correntes("Q", 1, 1, 2, [0.5, 0.5])
		divisao_de_correntes("Q", 1, 2, 2, [0.5, 0.5])
		divisao_de_correntes("F", 1, 1, 2, [0.5, 0.5])
		divisao_de_correntes("F", 1, 2, 2, [0.5, 0.5])
		divisao_de_correntes_abaixo("Q", 1, 1, 2, [0.5, 0.5])
		divisao_de_correntes_abaixo("Q", 1, 2, 2, [0.5, 0.5])
		divisao_de_correntes_abaixo("F", 1, 2, 2, [0.5, 0.5])
	else:
		# acima = []
		# abaixo = []
		# for i in range(10):
		# 	acima.append([3, 2, 1, 2, i+1, 1, 1])
		# 	abaixo.append([1, 2, 1, 1, i+1, 1, 1])

		#viola termo util
		# acima = [[3, 2, 1, 2, 1, 1, 677.9], [2, 2, 1, 1, 2, 1, 220.3], [3, 2, 1, 1, 3, 1, 306.5], [4, 2, 1, 1, 4, 1, "max"], [4, 2, 1, 2, 5, 1, "max"]]
		# abaixo = [[1, 2, 1, 1, 1, 1, 411.8], [2, 1, 1, 1, 2, 1, 31.3], [3, 1, 1, 1, 3, 1, 195.2], [1, 1, 1, 1, 4, 1, 715.8], [1, 3, 1, 1, 5, 1, "max"], [2, 4, 1, 1, 6, 1, 111.5], [3, 5, 1, 1, 7, 1, 170.9]]

		#sem viola term util
		acima = [[3, 2, 1, 2, 1, 1, "max"], [2, 2, 1, 1, 2, 1, "max"], [3, 2, 1, 1, 3, 1, "max"], [4, 2, 1, 1, 4, 1, "max"]]
		abaixo = [[1, 2, 1, 1, 1, 1, 411.8], [2, 1, 1, 1, 2, 1, 31.3], [3, 1, 1, 1, 3, 1, 195.2], [1, 1, 1, 1, 4, 1, "max"], [1, 3, 1, 1, 5, 1, "max"], [2, 4, 1, 1, 6, 1, "max"], [3, 5, 1, 1, 7, 1, "max"]]

		divisao_de_correntes("F", 1, 2, 2, [0.72, 0.28])
		divisoes.append(["F", 1, 2, 2, [0.72, 0.28]])

	for trocador in acima:
		if len(trocador) > 1:
			if trocador[6] == "max":
				trocador[6] = min(calor_atual_frio_sub[trocador[1]-1][trocador[3]-1], calor_atual_quente_sub[trocador[0]-1][trocador[2]-1])
			matriz_armazenada, oi = inserir_trocador(dlg, trocador)
			if matriz_armazenada[-1][7] - matriz_armazenada[-1][8] < dTmin or matriz_armazenada[-1][9] - matriz_armazenada[-1][10] < dTmin:
				violados_acima.append(len(matriz_armazenada))
		else:
			utilidadee = adicionar_utilidade(dlg, trocador[0])
			utilidades.append(utilidadee[-1])
			utilidades.sort()

	for trocador in abaixo:
		if len(trocador) > 1:
			if trocador[6] == "max":
				trocador[6] = min(calor_atual_quente_sub_abaixo[trocador[0]-1][trocador[2]-1], calor_atual_frio_sub_abaixo[trocador[1]-1][trocador[3]-1])
			matriz_trocadores_abaixo, oi = inserir_trocador_abaixo(dlg, trocador)
			if matriz_trocadores_abaixo[-1][7] - matriz_trocadores_abaixo[-1][8] < dTmin or matriz_trocadores_abaixo[-1][9] - matriz_trocadores_abaixo[-1][10] < dTmin:
				violados_abaixo.append(len(matriz_trocadores_abaixo))
		else:
			utilidadee = adicionar_utilidade_abaixo(dlg, trocador[0])
			utilidades_abaixo.append(utilidadee[-1])
			utilidades_abaixo.sort()

	printar()
	printar_abaixo()
	testar_correntes(dlg)
	testar_correntes_abaixo(dlg)
	global desenho_em_dia, desenho_em_dia_abaixo, desenho_em_dia_ambas
	desenho_em_dia = False
	desenho_em_dia_abaixo = False
	desenho_em_dia_ambas = False
	evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, 1, jogar_evolucao=True)
	desenhar_rede(correntes_quentes, correntes_frias, "ambas")

def centralizar_combobox_teste(x):
	x.setEditable(True)
	x.lineEdit().setReadOnly(True)
	x.lineEdit().setAlignment(Qt.AlignCenter)
	x.setStyleSheet("QComboBox { background-color: #e1e1e1 }")
	for i in range(x.count()):
		x.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

def jogar_evolucao():
	acima = [[1, 2, 1, 1, 1, 1, 50], [2, 1, 1, 1, 2, 1, 90], [1, 1, 1, 1, 3, 1, 230], [1, 2, 1, 1, 4, 1, 20], [2, 2, 1, 1, 5, 1, 30]]
	abaixo = [[2, 2, 1, 1, 1, 1, 20], [1, 2, 1, 1, 2, 1, 1], [2, 2, 1, 1, 3, 1, 19]]

	for trocador in acima:
		if len(trocador) > 1:
			nova_matriz = inserir_trocador(dlg, trocador)
			matriz_armazenada.append(nova_matriz[-1])
			if nova_matriz[-1][7] - nova_matriz[-1][8] < dTmin or nova_matriz[-1][9] - nova_matriz[-1][10] < dTmin:
				violados_acima.append(len(matriz_armazenada))
		else:
			utilidadee = adicionar_utilidade(dlg, trocador[0])
			utilidades.append(utilidadee[-1])
			utilidades.sort()

	for trocador in abaixo:
		if len(trocador) > 1:
			nova_matriz = inserir_trocador_abaixo(dlg, trocador)
			matriz_trocadores_abaixo.append(nova_matriz[-1])
			if nova_matriz[-1][7] - nova_matriz[-1][8] < dTmin or nova_matriz[-1][9] - nova_matriz[-1][10] < dTmin:
				violados_abaixo.append(len(matriz_trocadores_abaixo))
		else:
			utilidadee = adicionar_utilidade_abaixo(dlg, trocador[0])
			utilidades_abaixo.append(utilidadee[-1])
			utilidades_abaixo.sort()

	printar()
	printar_abaixo()
	testar_correntes(dlg)
	testar_correntes_abaixo(dlg)
	global desenho_em_dia, desenho_em_dia_abaixo, desenho_em_dia_ambas
	desenho_em_dia = False
	desenho_em_dia_abaixo = False
	desenho_em_dia_ambas = False
	evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, 1)
	desenhar_rede(correntes_quentes, correntes_frias, "ambas")


#streams
dlg.tableWidget.itemChanged.connect(lambda: editar_corrente(correntes, 0, dlg.tableWidget))
dlg.tableWidget_5.itemChanged.connect(lambda: editar_corrente(correntes_util, 1, dlg.tableWidget_5))
dlg.botao_addstream.clicked.connect(apertaradd) #add stream
dlg.botao_addutility.clicked.connect(add_utilidade)
dlg.remover_corrente.clicked.connect(lambda: remover_corrente(dlg.tableWidget.currentRow(), dlg.tableWidget, "corrente"))
dlg.remover_utilidade.clicked.connect(lambda: remover_corrente(dlg.tableWidget_5.currentRow(), dlg.tableWidget_5, "utilidade"))
dlg.actionOpen.triggered.connect(lambda: os.execl(sys.executable, os.path.abspath(__file__), *sys.argv))
dlg.actionOpen_2.triggered.connect(lambda: openfile_teste(True)) #file > open
dlg.donebutton.clicked.connect(lambda: done_teste(False)) #done
dlg.pinchbutton.clicked.connect(pinch_teste) #pinch
dlg.sistema_unidades.currentIndexChanged.connect(lambda: unidades(False))
dlg.temp_unidade.currentIndexChanged.connect(unidades)
dlg.cp_unidade.currentIndexChanged.connect(unidades)
dlg.pelicula_unidade.currentIndexChanged.connect(unidades)
dlg.temp_unidade_util.currentIndexChanged.connect(lambda: unidades(corrente=False))
dlg.pelicula_unidade_util.currentIndexChanged.connect(lambda: unidades(corrente=False))

#above
dlg.radioButton.toggled.connect(lambda: dlg.lineEdit_5.setEnabled(True)) #quando marca o heat load libera a linha pra digitar
dlg.radioButton_4.toggled.connect(lambda: dlg.lineEdit_5.setEnabled(False)) #block o heat load quando max heat ta ativado
dlg.radioButton_4.setChecked(True) #por padrao abre o prog com max heat selecionado
dlg.pushButton_9.clicked.connect(lambda: dividir_corrente("Q", "above"))
dlg.pushButton_13.clicked.connect(lambda: dividir_corrente("F", "above"))
dlg.divq_acima.clicked.connect(lambda: dividir_corrente("Q", "above"))
dlg.divf_acima.clicked.connect(lambda: dividir_corrente("F", "above"))
dlg.checkBox.stateChanged.connect(printar) #show splited streams printa tudo dnv
dlg.checkBox_2.stateChanged.connect(printar) #show splited streams printa tudo dnv
dlg.pushButton_6.clicked.connect(inserir_teste) #add heat exchanger
dlg.pushButton_10.clicked.connect(remover_teste) #remove heat exchanger
dlg.pushButton_14.clicked.connect(calcular_calor_teste) #choose stream temperature to calculate heat
dlg.pushButton_8.clicked.connect(utilidade_teste_acima) #add cold utility
dlg.addutil_acima.clicked.connect(utilidade_teste_acima)
dlg.pushButton_16.clicked.connect(lambda: atualizar_desenho("acima", True))

#below
dlg.radioButton_17.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(True)) #quando marca o heat load libera a linha pra digitar
dlg.radioButton_20.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(False)) #block o heat load quando max heat ta ativado
dlg.radioButton_20.setChecked(True) #por padrao abre o prog com max heat selecionado
dlg.pushButton_11.clicked.connect(lambda: dividir_corrente("Q", "below"))
dlg.pushButton_12.clicked.connect(lambda: dividir_corrente("F", "below"))
dlg.divq_abaixo.clicked.connect(lambda: dividir_corrente("Q", "below"))
dlg.divf_abaixo.clicked.connect(lambda: dividir_corrente("F", "below"))
dlg.checkBox_9.stateChanged.connect(printar_abaixo) #show splited streams printa tudo dnv
dlg.checkBox_10.stateChanged.connect(printar_abaixo) #show splited streams printa tudo dnv
dlg.pushButton_18.clicked.connect(inserir_teste_abaixo) #add heat exchanger
dlg.pushButton_15.clicked.connect(remover_teste_abaixo) #remove heat exchanger
dlg.pushButton_17.clicked.connect(calcular_calor_abaixo) #choose stream temperature to calculate heat
dlg.pushButton_20.clicked.connect(utilidade_teste_abaixo) #add hot utility
dlg.addutil_abaixo.clicked.connect(utilidade_teste_abaixo)
dlg.pushButton_19.clicked.connect(lambda: atualizar_desenho("abaixo", True))

#custos
dlg.otimizabotao.clicked.connect(lambda: otimizafun())



#evolução
dlg.trocador_path.currentIndexChanged.connect(lambda: dlg.calor_path.setPlaceholderText("-"))
dlg.botao_evolucao.clicked.connect(lambda: evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, 1, jogar_evolucao=True))
dlg.identificar_laco.clicked.connect(lambda: evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, int(dlg.nivel.currentText()), jogar_evolucao=False))
dlg.identificar_todos.clicked.connect(lambda: evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, "todos", todos=True))
dlg.botao_editar.clicked.connect(lambda: editar_calor(matriz_evolucao, dlg.trocador_editar.currentIndex(), float(dlg.calor_editar.text().replace(",", "."))))
dlg.botao_path.clicked.connect(lambda: editar_calor(matriz_evolucao, dlg.trocador_path.currentIndex(), float(dlg.calor_path.text().replace(",", ".")), path=True))
dlg.add_util.clicked.connect(lambda: utilidade(matriz_evolucao, []))





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



openfile_teste(False)
done_teste(True)
pinch_teste()
suprir_9_correntes()



dlg.show()
dlg.showMaximized()
app.exec()
