import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pylab as P
import numpy as np

import random

def abaixo(correntes,pinchq,pinchf,n,nhot,ncold) :
	AreaCosts = 0;
	UtilCosts = 0;
	TotalQhu = 0;
	TotalQcu = 0;
	Th0 = [] #Temperaturas quentes no pinch
	Thf = []
	CPh = []
	hh = []

	Tc0 = []
	Tcf = [] #Temperaturas frias no pinch
	CPc = []
	hc = []
	for i in range(n):
		if correntes[i][3] == "Hot":
			Th0.append(pinchq)
			Thf.append(correntes[i][1])
			CPh.append(correntes[i][2])
		if correntes[i][3] == "Cold":
			Tc0.append(correntes[i][0])
			Tcf.append(pinchf)
			CPc.append(correntes[i][2])
	#Th0 = [correntes[] 160] #Temperaturas quentes no pinch
	#Thf = [40, 120]
	#CPh = [0.15, 0.25]
	#hh = [0.2, 0.2]

	#Tc0 = [40, 20]
	#Tcf = [140, 140] #Temperaturas frias no pinch
	#CPc = [0.3, 0.2]
	#hc = [0.2, 0.2]
	Thk = []

	#nhot = 2 #número de correntes
	#ncold = 2

	Qtotalh0 = []
	Qtotalc0 = []

	#CÁLCULOS DOS CALORES TOTAIS
	#print(Tc0,Tcf,Th0,Thf,CPh,CPc)
	for i in range (nhot):
		Qtotal0 = 0
		Qtotal0 = CPh[i] * (Th0[i] - Thf[i])
		Qtotalh0.append(Qtotal0)
	for j in range (ncold):
		Qtotal1 = 0
		Qtotal1 = CPc[j] * (Tcf[j] - Tc0[j])
		Qtotalc0.append(Qtotal1)
	#print(Qtotalh0)
	#print(Qtotalc0)
	nsi = [ncold, ncold] #número de divisões por corrente quente
	nsj = [nhot, nhot] #número de divisões por corrente fria
	if(nhot>ncold):
		nsk = ncold #número de sub-estagios
		nstages = ncold #número de estágios
	else:
		nsk = nhot
		nstages = nhot

	Thsk = np.array ([0])
	Thsk.resize(nhot, ncold, nsk, nstages)
	Thk = np.array ([0])
	Thk.resize(nhot, nstages)
	Thsfinal0 = np.array ([0])
	Thsfinal0.resize(nhot, ncold, nstages)
	Thfinal0 = np.array ([0])
	Thfinal0.resize(nhot)

	Tcsk = np.array ([0])
	Tcsk.resize(ncold, nhot, nsk, nstages)
	Tck = np.array ([0])
	Tck.resize(ncold, nstages)
	Tcsfinal0 = np.array ([0])
	Tcsfinal0.resize(ncold, nhot, nstages)
	Tcfinal0 = np.array ([0])
	Tcfinal0.resize(ncold)

	Thin = np.array ([0])
	Thin.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Temperatura de entrada quente de um trocador
	Tcin = np.array ([0])
	Tcin.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Temperatura de entrada fria de um trocador
	Thout = np.array ([0])
	Thout.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Temperatura de saída quente de um trocador
	Tcout = np.array ([0])
	Tcout.resize(nhot, ncold, ncold, nhot, nsk, nstages) #Temperatura de saída fria de um trocador

	AreaCosts = 0 #Custo relativo a área
	UtilCosts = 0 #Custo relativo às utilidades
	TotalQhu = 0 #Total em utilidades quentes (hot utilities)
	TotalQcu = 0 #Total em utilidades frias (cold utilities)

	Qmin = 0.0001 #Esta é a quantidade mínima de carga para a existência de um trocador de calor
	Frmin = 0.0001 #Esta é a fração mínima para a existência de uma divisão

	sumQThsk = np.array ([0])
	sumQThsk.resize(nhot, ncold, nsk, nstages)  #Variáveis auxiliares: somatórias dos calores
	sumQThk = np.array ([0])
	sumQThk.resize(nhot, nstages)
	Qtotalh = np.array([0])
	Qtotalh.resize(nhot)

	sumQTcsk = np.array ([0])
	sumQTcsk.resize(ncold, nhot, nsk, nstages)
	sumQTck = np.array ([0])
	sumQTck.resize(ncold, nstages)
	Qtotalc = np.array([0])
	Qtotalc.resize(ncold)
	# PARA CORRENTES QUENTES =====================================================================================================

	for i in range (nhot):
		#Este loop iguala as temperaturas iniciais de todos os SUB-ESTÁGIOS à temperatura inicial da corrente
		for si in range (nsi[i]):
			for sk in range (nsk):
				for k in range (nstages) :
					Thsk[i][si][sk][k] = Th0[i] #Thsk é a temperatura inicial do sub-estágio

		#Este loop iguala as temperaturas iniciais de todos os ESTÁGIOS à temperatura inicial da corrente
		for k in range (nstages):
			Thk[i][k] = Th0[i] #Thk é a temperatura inicial do estágio

	for j in range (ncold) :
		for sj in range (nsj[j]) :
			for sk in range(nsk-1, -1, -1) :
				for k in range(nstages-1, -1, -1) :
					Tcsk[j][sj][sk][k] = Tc0[j]
		for k in range (nstages-1, -1, -1) :
			Tck[j][k] = Tc0[j]
	#print(Tc0,Tcf,Th0,Thf,CPh,CPc)
	fim = 'y'
	no = 'n'
	while fim != no:
		Q = np.array ([0])
		Q.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Q[i][si][j][sj][sk][k]
		Fh = np.array ([0])
		Fh.resize(nhot, ncold, nsk, nstages)  #Fh[i][si][sk][k]
		Fc = np.array ([0])
		Fc.resize(ncold, nhot, nsk, nstages)  #Fc[j][sj][sk][k]
		if Qtotalh0[chot-1] > Qtotalc0[ccold-1]:
			Q[chot-1][0][ccold-1][0][0][0] = Qtotalc0[ccold-1]
			Fh[chot-1][0][0][0] = 1
			Fc[ccold-1][0][0][0] = 1
		else:
			Q[chot-1][0][ccold-1][0][0][0] = Qtotalh0[chot-1]
			Fh[chot-1][0][0][0] = 1
			Fc[ccold-1][0][0][0] = 1

	#percebam que abaixo do Pinch, os balanços são realizados da "esquerda para a direita". Logo, os loops de estágios "rodam" somando +1 (k++, sk++):

		for k in range(nstages) :
			for sk in range(nsk) :
				for j in range(ncold) :
					for sj in range(nsj[j]) :
						for i in range(nhot) :
							for si in range(nsi[i]) :
								if Q[i][si][j][sj][sk][k] > Qmin  and Fh[i][si][sk][k] > Frmin and Fc[j][sj][sk][k] > Frmin:
									#Se um dado trocador tiver carga térmica e frações maiores que zero
									#Calcular a temperatura de entrada quente desse trocador como segue:
									Thin[i][si][j][sj][sk][k] = Thsk[i][si][sk][k] #Sabe-se a temperatura de entrada
									Thout[i][si][j][sj][sk][k] = Thout[i][si][j][sj][sk][k] - Q[i][si][j][sj][sk][k] / (Fh[i][si][sk][k] * CPh[i]) #Calcula-se a de saída

									#Esta é uma variável auxiliar que soma o calor total para um dado SUB-ESTÁGIO, em uma dada SUB-CORRENTE quente
									sumQThsk[i][si][sk][k] = sumQThsk[i][si][sk][k] + Q[i][si][j][sj][sk][k]

									#Esta é uma variável auxiliar que soma o calor total para um dado ESTÁGIO, em uma dada CORRENTE quente
									sumQThk[i][k] = sumQThk[i][k] + Q[i][si][j][sj][sk][k]

									#Esta é uma variável auxiliar que soma o calor total trocado em uma corrente quente
									Qtotalh[i] = Qtotalh[i] + Q[i][si][j][sj][sk][k]


									#Calcular a temperatura de saída fria desse trocador como segue:
									Tcout[i][si][j][sj][sk][k] = Tcsk[j][sj][sk][k] #Sabe-se a temperatura de entrada
									Tcin[i][si][j][sj][sk][k] = Thin[i][si][j][sj][sk][k] - Q[i][si][j][sj][sk][k] / (Fc[j][sj][sk][k] * CPc[j]) #Calcula-se a de saída

									#Esta é uma variável auxiliar que soma o calor total para um dado SUB-ESTÁGIO, em uma dada SUB-CORRENTE fria
									sumQTcsk[j][sj][sk][k] = sumQTcsk[j][sj][sk][k] + Q[i][si][j][sj][sk][k]

									#Esta é uma variável auxiliar que soma o calor total para um dado ESTÁGIO, em uma dada CORRENTE fria
									sumQTck[j][k] = sumQTck[j][k] + Q[i][si][j][sj][sk][k]

									#Esta é uma variável auxiliar que soma o calor total trocado em uma corrente fria
									Qtotalc[j] = Qtotalc[j] + Q[i][si][j][sj][sk][k]
						if Fh[i][si][sk][k] > Frmin :
							#Aqui, a temperatura do próximo sub-estágio é calculada (note que o sumQThsk é utilizado)
							if sk < nsk :
								#Se sk não for o último sub-estágio (neste caso, nsk)
								Thsk[i][si][sk][k] = Thsk[i][si][sk][k] + sumQThsk[i][si][sk][k] / (Fh[i][si][sk][k] * CPh[i])
							else :
								Thsfinal0[i][si][k] = Thsk[i][si][sk][k] + sumQThsk[i][si][sk][k] / (Fh[i][si][sk][k] * CPh[i])
						if Fc[j][sj][sk][k] > Frmin :
							if sk < nsk :
								#Se sk não for o último sub-estágio (neste caso, nsk)
								Tcsk[j][sj][sk][k] = Tcsk[j][sj][sk][k] + sumQTcsk[j][sj][sk][k] / (Fc[j][sj][sk][k] * CPc[j])
							else :
								Tcsfinal0[j][sj][k] = Tcsk[j][sj][sk][k] + sumQTcsk[j][sj][sk][k] / (Fc[j][sj][sk][k] * CPc[j])

		#Realizados todos os cálculos para todas as sub-correntes e sub-estágios de um estágio, os balanços nos misturadores de todas as correntes quentes (i) desse estágio (k) são calculados:

			for i in range(nhot):
				if k < (nstages-1):
					Thk[i][k] = Thk[i][k] - sumQThk[i][k] / CPh[i]
					for k in range (nstages-1):
						Thk[i][k+1] = Thk[i][k]
				else:
					Thfinal0[i] = Thk[i][k] - sumQThk[i][k] / CPh[i]
			for j in range(ncold):
				if k < (nstages-1):
					Tck[j][k] = Tck[j][k] + sumQTck[j][k] / CPc[j]
					for k in range (nstages-1):
						Tck[j][k+1] = Tck[j][k]
				else:
					Tcfinal0[j] = Tck[j][k] + sumQTck[j][k] / CPc[j]
			for i in range(nhot):
				for k in range(nstages):
					sumQThk[i][k] = 0
			for j in range(ncold):
				for k in range(nstages):
					sumQTck[j][k] = 0
		#calculo do excesso/falta de calor nas correntes quentes/frias
		#print(Qtotalh)
		#print(Qtotalc)
		for i in range(nhot) :
			Qtotalh0[i] = Qtotalh0[i] - Qtotalh[i]
			Qtotalh[i] = 0
		for j in range(ncold) :
			Qtotalc0[j] = Qtotalc0[j] - Qtotalc[j]
			Qtotalc[j] = 0
		#print(Thfinal0)
		#print(Tcfinal0)
		#print(Qtotalh0)
		#print(Qtotalc0)
