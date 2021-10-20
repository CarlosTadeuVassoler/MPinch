import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pylab as P
import numpy as np

import random


def acima(correntes,pinchq,pinchf,n,nhot,ncold,dlg):
	Th0 = [] #Temperaturas quentes no pinch #perguntar o que entra aqui
	Thf = []
	CPh = []
	Thm = []
	#hh = [0.2, 0.2]

	Tc0 = []
	Tcf = [] #Temperaturas frias no pinch
	CPc = []
	Tcm = []
	#hc = [0.2, 0.2]
	for i in range(n):
		if correntes[i][3] == "Hot":
			Thm.append(float(dlg.tableWidget_3.item(i,1).text()))
			Th0.append(correntes[i][0])
			Thf.append(pinchq)
			CPh.append(correntes[i][2])
	j=0
	for i in range(n):
		if correntes[i][3] == "Cold":
			Tc0.append(pinchf)
			Tcf.append(correntes[i][1])
			CPc.append(correntes[i][2])
			Tcm.append(float(dlg.tableWidget_4.item(j,1).text())) #tablewidget
			j=j+1
	map(float, Th0)
	map(float, Thf)
	map(float, CPh)
	#hh = [0.2, 0.2]
	#map(float, hh)

	map(float, Tc0)
	map(float, Tcf)
	map(float, CPc)
	#hc = [0.2, 0.2]
	#map(float, hc)
	Thk = []
	#(len(correntes))
	for i in range (len(correntes)):
		if correntes[i][3] == "Hot":
			CPh.append(correntes[i][2])
		elif correntes[i][3] == "Cold":
			CPc.append(correntes[i][2])



	if ncold > nhot:
		#("Error")
	else:
		somacphot = 0
		somacpcold = 0
		for i in range(nhot):
			somacphot = CPh[i] + somacphot
		for j in range(ncold):
			somacpcold = CPc[j] + somacpcold

		Qtotalh01 = []
		Qtotalc01 = []
		Qtotalh0arr = np.array([0])
		Qtotalh0arr.resize(nhot, ncold)
		Qtotalh0 = Qtotalh0arr.tolist()
		map(float, Qtotalh0)
		Qtotalc0arr = np.array([0])
		Qtotalc0arr.resize(ncold, nhot)
		Qtotalc0 = Qtotalc0arr.tolist()
		map(float, Qtotalc0)

		#CÁLCULOS DOS CALORES TOTAIS
		for i in range (nhot):
			Qtotalh1 = 0
			Qtotalh1 = CPh[i] * (Th0[i] - Thm[i])
			Qtotalh01.append(Qtotalh1)
			Qtotalh01[i] = float("{:.2f}".format(Qtotalh01[i]))
		for j in range (ncold):
			Qtotalc1 = 0
			Qtotalc1 = CPc[j] * (Tcf[j] - Tcm[j])
			Qtotalc01.append(Qtotalc1)
			Qtotalc01[j] = float("{:.2f}".format(Qtotalc01[j]))

		map(float, Qtotalh01)
		map(float, Qtotalc01)
		#("Temperatura Entrada Quente")
		#(Th0)
		#("Temperatura Final Quente")
		#(Thf)
		#("CP da corrente Quente")
		#(CPh)
		#("Temperatura Entrada Fria")
		#(Tc0)
		#("Temperatura Final Fria")
		#(Tcf)
		#("CP da corrente Fria")
		#(CPc)
		#("Calor Disponível Quentes:")
		#(Qtotalh01)
		#("Calor Disponível Frias:")
		#(Qtotalc01)


		nsi = [ncold, ncold] #número de divisões por corrente quente
		nsj = [nhot, nhot] #número de divisões por corrente fria
		if(nhot>ncold):
			nsk = ncold #número de sub-estagios
			nstages = ncold #número de estágios
		else:
			nsk = nhot
			nstages = nhot

		Thskarr = np.array ([0])
		Thskarr.resize(nhot, ncold, nsk, nstages)
		Thsk = Thskarr.tolist()
		map(float, Thsk)
		Thkarr = np.array ([0])
		Thkarr.resize(nhot, nstages)
		Thk = Thkarr.tolist()
		map(float, Thk)
		Thsfinal0arr = np.array ([0])
		Thsfinal0arr.resize(nhot, ncold, nstages)
		Thsfinal0 = Thsfinal0arr.tolist()
		map(float, Thsfinal0)
		Thfinal0arr = np.array ([0])
		Thfinal0arr.resize(nhot)
		Thfinal0 = Thfinal0arr.tolist()
		map(float, Thfinal0)

		Tcskarr = np.array ([0])
		Tcskarr.resize(ncold, nhot, nsk, nstages)
		Tcsk = Tcskarr.tolist()
		map(float, Tcsk)
		Tckarr = np.array ([0])
		Tckarr.resize(ncold, nstages)
		Tck = Tckarr.tolist()
		map(float, Tck)
		Tcsfinal0arr = np.array ([0])
		Tcsfinal0arr.resize(ncold, nhot, nstages)
		Tcsfinal0 = Tcsfinal0arr.tolist()
		map(float, Tcsfinal0)
		Tcfinal0arr = np.array ([0])
		Tcfinal0arr.resize(ncold)
		Tcfinal0 = Tcfinal0arr.tolist()
		map(float, Tcfinal0)

		Thinarr = np.array ([0])
		Thinarr.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Temperatura de entrada quente de um trocador
		Thin = Thinarr.tolist()
		map(float, Thin)
		Tcinarr = np.array ([0])
		Tcinarr.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Temperatura de entrada fria de um trocador
		Tcin = Tcinarr.tolist()
		map(float, Tcin)
		Thoutarr = np.array ([0])
		Thoutarr.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Temperatura de saída quente de um trocador
		Thout = Thoutarr.tolist()
		map(float, Thout)
		Tcoutarr = np.array ([0])
		Tcoutarr.resize(nhot, ncold, ncold, nhot, nsk, nstages) #Temperatura de saída fria de um trocador
		Tcout = Tcoutarr.tolist()
		map(float, Tcout)

		AreaCosts = 0 #Custo relativo a área
		UtilCosts = 0 #Custo relativo às utilidades
		TotalQhu = 0 #Total em utilidades quentes (hot utilities)
		TotalQcu = 0 #Total em utilidades frias (cold utilities)
		Qmin = 0.0001 #Esta é a quantidade mínima de carga para a existência de um trocador de calor
		Frmin = 0.0001 #Esta é a fração mínima para a existência de uma divisão

		sumQThskarr = np.array ([0])
		sumQThskarr.resize(nhot, ncold, nsk, nstages)  #Variáveis auxiliares: somatórias dos calores
		sumQThsk = sumQThskarr.tolist()
		map(float, sumQThsk)
		sumQThkarr = np.array ([0])
		sumQThkarr.resize(nhot, nstages)
		sumQThk = sumQThkarr.tolist()
		map(float, sumQThk)
		Qtotalharr = np.array([0])
		Qtotalharr.resize(nhot)
		Qtotalh = Qtotalharr.tolist()
		map(float, Qtotalh)

		sumQTcskarr = np.array ([0])
		sumQTcskarr.resize(ncold, nhot, nsk, nstages)
		sumQTcsk = sumQTcskarr.tolist()
		map(float, sumQTcsk)
		sumQTckarr = np.array ([0])
		sumQTckarr.resize(ncold, nstages)
		sumQTck = sumQTckarr.tolist()
		map(float, sumQTck)
		Qtotalcarr = np.array([0])
		Qtotalcarr.resize(ncold)
		Qtotalc = Qtotalcarr.tolist()
		map(float, Qtotalc)
		# PARA CORRENTES QUENTES =====================================================================================================

		for i in range (nhot):
			#Este loop iguala as temperaturas iniciais de todos os SUB-ESTÁGIOS à temperatura inicial da corrente
			for si in range (nsi[i]):
				for sk in range (nsk):
					for k in range (nstages) :
						Thsk[i][si][sk][k] = Thf[i] #Thsk é a temperatura inicial do sub-estágio

			#Este loop iguala as temperaturas iniciais de todos os ESTÁGIOS à temperatura inicial da corrente
			for k in range (nstages):
				Thk[i][k] = Thf[i] #Thk é a temperatura inicial do estágio

		for j in range (ncold) :
			for sj in range (nsj[j]) :
				for sk in range(nsk-1, -1, -1) :
					for k in range(nstages-1, -1, -1) :
						Tcsk[j][sj][sk][k] = Tc0[j]
			for k in range (nstages-1, -1, -1) :
				Tck[j][k] = Tc0[j]
		Fharr = np.array ([0])
		Fharr.resize(nhot, ncold, nsk, nstages)  #Fh[i][si][sk][k]
		Fh = Fharr.tolist()
		map(float, Fh)
		Fcarr = np.array ([0])
		Fcarr.resize(ncold, nhot, nsk, nstages)  #Fc[j][sj][sk][k]
		Fc = Fcarr.tolist()
		map(float, Fc)
		fim = 'yes'
		no = 'no'
		divisao="yes"
		if str(dlg.comboBox_6.currentText())!="do not split stream":
			sbhot=int(dlg.comboBox_6.currentText())
		if str(dlg.comboBox_4.currentText())!="do not split stream": #criar aviso de dividir as duas com uma sendo 100
			sbcold=int(dlg.comboBox_4.currentText())
		#(str(dlg.comboBox_6.currentText()))
		if str(dlg.comboBox_4.currentText())=="do not split stream" and str(dlg.comboBox_6.currentText())=="do not split stream":
			divisao="no"
		#if divisao=="yes": criar nova linha, criar divisao antes de colocar um trocador

		sestagio = 1
		estagio = 1
		while fim != no:
			if fim == "utilidade":
				ccoldutil = int(input("Qual corrente fria recebe utilidade: "))
				Qtotalc01[ccoldutil-1] = 0
				Tcfinal0[ccoldutil-1] = Tcf[ccoldutil-1]
			else:
				Qarr = np.array ([0])
				Qarr.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Q[i][si][j][sj][sk][k]
				Q = Qarr.tolist()
				map(float, Q)
				for i in range (nhot):
				#Este loop iguala as temperaturas iniciais de todos os SUB-ESTÁGIOS à temperatura inicial da corrente
					for si in range (nsi[i]):
						for sk in range (nsk):
							for k in range (nstages) :
								Thsk[i][si][sk][k] = Thf[i] #Thsk é a temperatura inicial do sub-estágio

				#Este loop iguala as temperaturas iniciais de todos os ESTÁGIOS à temperatura inicial da corrente
					for k in range (nstages):
						Thk[i][k] = Thf[i] #Thk é a temperatura inicial do estágio

				for j in range (ncold) :
					for sj in range (nsj[j]) :
						for sk in range(nsk-1, -1, -1) :
							for k in range(nstages-1, -1, -1) :
								Tcsk[j][sj][sk][k] = Tc0[j]
					for k in range (nstages-1, -1, -1) :
						Tck[j][k] = Tc0[j]
				if(divisao == 'yes'):
					chot = int((dlg.comboBox_2.currentText()))
					ccold = int(dlg.comboBox_5.currentText())
					if(Fh[chot-1][sbhot-1][sestagio-1][estagio-1]==0):
						Fh[chot-1][sbhot-1][sestagio-1][estagio-1] = float((dlg.lineEdit_3.text()))
						Qtotalh0[chot-1][sbhot-1] = Qtotalh01[chot-1]*Fh[chot-1][sbhot-1][sestagio-1][estagio-1]/100
					if(Fc[ccold-1][sbcold-1][sestagio-1][estagio-1]==0):
						Fc[ccold-1][sbcold-1][sestagio-1][estagio-1] = float((dlg.lineEdit_4.text()))
						Qtotalc0[ccold-1][sbcold-1] = Qtotalc01[ccold-1]*(Fc[ccold-1][sbcold-1][sestagio-1][estagio-1]/100)
					if ((Qtotalh0[chot-1][sbhot-1]) > (Qtotalc0[ccold-1][sbcold-1])):
						Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1]
					else:
						Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalh0[chot-1][sbhot-1]
					for sk in range(nsk-1):
						for k in range(nstages-1):
							Fh[chot-1][sbhot-1][sk+1][k+1] = Fh[chot-1][sbhot-1][sk][k]
							Fc[ccold-1][sbcold-1][sk+1][k+1] = Fc[ccold-1][sbcold-1][sk][k]

				else:
					chot = int(dlg.comboBox_2.currentText())
					ccold = int(dlg.comboBox_5.currentText())
					sbhot = 1
					sbcold = 1
					Fh[chot-1][sbhot-1][sestagio-1][estagio-1] = 100
					Fc[ccold-1][sbcold-1][sestagio-1][estagio-1] = 100
					if ((Qtotalh01[chot-1]) > (Qtotalc01[ccold-1])):
						#("Calor Máximo a ser trocado: ", Qtotalc01[ccold-1])
						Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalc01[ccold-1]
					else:
						#("Calor Máximo a ser trocado: ", Qtotalh01[chot-1])
						Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalh01[chot-1]
					if dlg.radioButton_4.isChecked() == True:
						trocamax="yes"
					else:
						trocamax="no"
					if trocamax == 'no':
						Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = float((dlg.lineEdit_5.text()))
						#(Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1],"test para troca limitada")
			#percebam que acima do Pinch, os balanços são realizados da "direita para a esquerda". Logo, os loops de estágios "rodam" ao contrário (subtraindo 1, k--, sk--):

				for k in range(nstages-1, -1, -1) :
					for sk in range(nsk-1, -1, -1) :
						for j in range(ncold) :
							for sj in range(nsj[j]) :
								for i in range(nhot) :
									for si in range(nsi[i]) :
										if Q[i][si][j][sj][sk][k] > Qmin  and Fh[i][si][sk][k] > Frmin and Fc[j][sj][sk][k] > Frmin :
											#Se um dado trocador tiver carga térmica e frações maiores que zero
											#Calcular a temperatura de entrada quente desse trocador como segue:
											Thout[i][si][j][sj][sk][k] = Thsk[i][si][sk][k] #Sabe-se a temperatura de saída
											Thin[i][si][j][sj][sk][k] = Thout[i][si][j][sj][sk][k] + Q[i][si][j][sj][sk][k] / ((Fh[i][si][sk][k]/100) * CPh[i])#Calcula-se a de entrada

											#Esta é uma variável auxiliar que soma o calor total para um dado SUB-ESTÁGIO, em uma dada SUB-CORRENTE quente
											sumQThsk[i][si][sk][k] = sumQThsk[i][si][sk][k] + Q[i][si][j][sj][sk][k]

											#Esta é uma variável auxiliar que soma o calor total para um dado ESTÁGIO, em uma dada CORRENTE quente
											sumQThk[i][k] = sumQThk[i][k] + Q[i][si][j][sj][sk][k]

											#Esta é uma variável auxiliar que soma o calor total trocado em uma corrente quente
											Qtotalh[i] = float(Qtotalh[i]) + float(Q[i][si][j][sj][sk][k])


											#Calcular a temperatura de saída fria desse trocador como segue:
											Tcin[i][si][j][sj][sk][k] = Tcsk[j][sj][sk][k] #Sabe-se a temperatura de entrada
											Tcout[i][si][j][sj][sk][k] = Tcin[i][si][j][sj][sk][k] + Q[i][si][j][sj][sk][k] / ((Fc[j][sj][sk][k]/100) * CPc[j]) #Calcula-se a de saída

											#Esta é uma variável auxiliar que soma o calor total para um dado SUB-ESTÁGIO, em uma dada SUB-CORRENTE fria
											sumQTcsk[j][sj][sk][k] = sumQTcsk[j][sj][sk][k] + Q[i][si][j][sj][sk][k]

											#Esta é uma variável auxiliar que soma o calor total para um dado ESTÁGIO, em uma dada CORRENTE fria
											sumQTck[j][k] = sumQTck[j][k] + Q[i][si][j][sj][sk][k]

											#Esta é uma variável auxiliar que soma o calor total trocado em uma corrente fria
											Qtotalc[j] = float(Qtotalc[j]) + float(Q[i][si][j][sj][sk][k])
								if (Fh[i][si][sk][k]/100) > Frmin :
									#Aqui, a temperatura do próximo sub-estágio é calculada (note que o sumQThsk é utilizado)
									if sk > 0 :
										#Se sk não for o último sub-estágio (neste caso, zero)
										Thsk[i][si][sk - 1][k] = Thsk[i][si][sk][k] + sumQThsk[i][si][sk][k] / (Fh[i][si][sk][k] * CPh[i])
									else :
										Thsfinal0[i][si][k] = Thsk[i][si][sk][k] + sumQThsk[i][si][sk][k] / (Fh[i][si][sk][k] * CPh[i])
								if (Fc[j][sj][sk][k]/100) > Frmin :
									if sk > 0 :
										#Se sk não for o último sub-estágio (neste caso, zero)
										Tcsk[j][sj][sk - 1][k] = Tcsk[j][sj][sk][k] + sumQTcsk[j][sj][sk][k] / (Fc[j][sj][sk][k] * CPc[j])
									else :
										Tcsfinal0[j][sj][k] = Tcsk[j][sj][sk][k] + sumQTcsk[j][sj][sk][k] / (Fc[j][sj][sk][k] * CPc[j])

					#Realizados todos os cálculos para todas as sub-correntes e sub-estágios de um estágio, os balanços nos misturadores de todas as correntes quentes (i) desse estágio (k) são calculados:

					for i in range(nhot) :
						if k > 0 :
							Thk[i][k] = Thk[i][k] + sumQThk[i][k] / CPh[i]
							for k in range(nstages-1, -1, -1) :
								Thk[i][k-1] = Thk[i][k]
						else :
							Thfinal0[i] = Thk[i][k] + sumQThk[i][k] / CPh[i]
							Thfinal0[i] = float("{:.2f}".format(Thfinal0[i]))
							Thf[i] = Thfinal0[i]
					for j in range(ncold) :
						if k > 0 :
							Tck[j][k] = Tck[j][k] + sumQTck[j][k] / CPc[j]
							for k in range(nstages-1, -1, -1) :
								Tck[j][k-1] = Tck[j][k]
						else :
							Tcfinal0[j] = Tck[j][k] + sumQTck[j][k] / CPc[j]
							Tcfinal0[j] = float("{:.2f}".format(Tcfinal0[j]))
							Tc0[j] = Tcfinal0[j]
					for i in range(nhot):
						for k in range(nstages):
							sumQThk[i][k] = 0
					for j in range(ncold):
						for k in range(nstages):
							sumQTck[j][k] = 0
				#calculo do excesso/falta de calor nas correntes quentes/frias
				#(Qtotalh)
				#(Qtotalc)
				if(divisao == 'yes'):
					for i in range(nhot) :
						Qtotalh0[i][sbhot-1] = Qtotalh0[i][sbhot-1] - Qtotalh[i]
						Qtotalh0[i][sbhot-1] = float("{:.2f}".format(Qtotalh0[i][sbhot-1]))
						Qtotalh[i] = 0
					for j in range(ncold) :
						Qtotalc0[j][sbcold-1] = Qtotalc0[j][sbcold-1] - Qtotalc[j]
						Qtotalc0[j][sbhot-1] = float("{:.2f}".format(Qtotalc0[j][sbhot-1]))
						Qtotalc[j] = 0
					#(Qtotalh0)
					#(Qtotalc0)
				else:
					for i in range(nhot) :
						Qtotalh01[i] = Qtotalh01[i] - Qtotalh[i]
						Qtotalh01[i] = float("{:.2f}".format(Qtotalh01[i]))
						Qtotalh[i] = 0
					for j in range(ncold) :
						Qtotalc01[j]= Qtotalc01[j] - Qtotalc[j]
						Qtotalc01[j] = float("{:.2f}".format(Qtotalc01[j]))
						Qtotalc[j] = 0
					#(Qtotalh01)
					#(Qtotalc01)
			#(Thfinal0)
			#(Tcfinal0)
			if divisao== "yes":
				return(Thfinal0[chot-1],Tcfinal0[ccold-1],Qtotalh0[chot-1][sbhot-1],Qtotalc0[ccold-1][sbcold-1])
			else:
				return(Thfinal0[chot-1],Tcfinal0[ccold-1],Qtotalh01[chot-1],Qtotalc01[ccold-1])
			fim = "no"
			sestagio = sestagio + 1
			if (sestagio == nsk+1):
				estagio = estagio + 1
				sestagio = 1
