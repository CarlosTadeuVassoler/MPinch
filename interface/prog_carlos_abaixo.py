from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMessageBox
from PyQt5 import QtWidgets , uic, QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import threading

Th0 = []
Thf = []
CPh = []

Tc0 = []
Tcf = []
CPc = []

divop = avanc = ''
dTmin = 0
nhot = 0
ncold = 0
pinchq = 0
pinchf = 0

linha_interface_abaixo = []
utilidades_abaixo = []
estagio = 0
sestagio = 0

complistq = []
complistf = []
cont = compq = compf = opcao = 0
chot = ccold = sbhot = sbcold = nhotc = ncoldc = qsi = qsj = chotutil = 0
somaCPh = somaCPc = 0
tempdif = tempmeta = 0

nsk = nstages = 2

#VARIÁVEIS DO CALOR
Qtotalh01 = []
Qtotalc01 = []
Qtotalh0 = []
Qtotalc0 = []
Qestagioq = []
Qestagiof = []
calor_atual_quente_abaixo = []
calor_atual_frio_abaixo = []
Qtotalestagio = Qtotalestagiof = Qmax = Qtotalhaux = Qtotalcaux = 0


#VARIÁVEIS DE TEMPERATURAS QUENTES
Thski = []
Thki = []
Thskf = []
Thkf = []
Thfinal01 = []
Thfinal01k = []
temperatura_atual_quente_abaixo = []
temperatura_atual_quente_mesclada_abaixo = []

#VARIÁVEIS DE TEMPERATURAS FRIAS
Tcski = []
Tcki = []
Tcskf = []
Tckf = []
Tcfinal01 = []
Tcfinal01k = []
temperatura_atual_fria_abaixo = []
temperatura_atual_fria_mesclada_abaixo = []

#VARIÁVEIS DE TEMPERATURAS "GERAIS"
Thin = []
Thout = []
Tcin = []
Tcout = []
Think = []
Thoutk = []
Tcink = []
Tcoutk = []

#OUTRAS VARIÁVEIS
Fharr = []
Fcarr = []
Qarr = []
Q = []
Qaux = []

def limpar_lista(lista):
	for i in range(len(lista)):
		lista.pop(-1)

def preparar_dados_e_rede2():
	global Qtotalh01, Qtotalc01, Qtotalh0, Qtotalc0, Qestagioq, Qestagiof
	global Thski, Thki, Thskf, Thkf, Thfinal01, Thfinal01k
	global Tcski, Tcki, Tcskf, Tckf, Tcfinal01, Tcfinal01k
	global Thin, Thout, Tcin, Tcout, Think, Thoutk, Tcink, Tcoutk
	global Fharr, Fcarr, Qarr, Q, Qaux

	limpar_lista(temperatura_atual_quente_abaixo)
	limpar_lista(temperatura_atual_fria_abaixo)
	limpar_lista(calor_atual_quente_abaixo)
	limpar_lista(calor_atual_frio_abaixo)
	limpar_lista(Qtotalh01)
	limpar_lista(Qtotalc01)

	Qtotalh0arr = np.array([0])
	Qtotalh0arr.resize(nhot, ncold, nstages)
	Qtotalh0 = Qtotalh0arr.tolist()
	map(float, Qtotalh0)
	Qtotalc0arr = np.array([0])
	Qtotalc0arr.resize(ncold, nhot, nstages)
	Qtotalc0 = Qtotalc0arr.tolist()
	map(float, Qtotalc0)
	Qestagioq = np.array([0])
	Qestagioq.resize(nhot, nstages)
	Qestagiof = np.array([0])
	Qestagiof.resize(ncold, nstages)

	Thskiarr = np.array ([0])
	Thskiarr.resize(nhot, ncold, nsk, nstages)
	Thski = Thskiarr.tolist()
	map(float, Thski)
	Thkiarr = np.array ([0])
	Thkiarr.resize(nhot, nstages)
	Thki = Thkiarr.tolist()
	map(float, Thki)
	Thskfarr = np.array ([0])
	Thskfarr.resize(nhot, ncold, nsk, nstages)
	Thskf = Thskfarr.tolist()
	map(float, Thskf)
	Thkfarr = np.array ([0])
	Thkfarr.resize(nhot, nstages)
	Thkf = Thkfarr.tolist()
	map(float, Thkf)
	Thfinal01arr = np.array ([0])
	Thfinal01arr.resize(nhot, ncold)
	Thfinal01 = Thfinal01arr.tolist()
	map(float, Thfinal01)
	Thfinal01karr = np.array ([0])
	Thfinal01karr.resize(nhot, nstages)
	Thfinal01k = Thfinal01karr.tolist()
	map(float, Thfinal01k)

	Tcskiarr = np.array ([0])
	Tcskiarr.resize(ncold, nhot, nsk, nstages)
	Tcski = Tcskiarr.tolist()
	map(float, Tcski)
	Tckiarr = np.array ([0])
	Tckiarr.resize(ncold, nstages)
	Tcki = Tckiarr.tolist()
	map(float, Tcki)
	Tcskfarr = np.array ([0])
	Tcskfarr.resize(ncold, nhot, nsk, nstages)
	Tcskf = Tcskfarr.tolist()
	map(float, Tcskf)
	Tckfarr = np.array ([0])
	Tckfarr.resize(ncold, nstages)
	Tckf = Tckfarr.tolist()
	map(float, Tckf)
	Tcfinal01arr = np.array ([0])
	Tcfinal01arr.resize(ncold, nhot)
	Tcfinal01 = Tcfinal01arr.tolist()
	map(float, Tcfinal01)
	Tcfinal01karr = np.array ([0])
	Tcfinal01karr.resize(ncold, nstages)
	Tcfinal01k = Tcfinal01karr.tolist()
	map(float, Tcfinal01k)

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

	Think = Thinarr.tolist()
	map(float, Think)
	Tcink = Tcinarr.tolist()
	map(float, Tcin)
	Thoutk = Thoutarr.tolist()
	map(float, Thout)
	Tcoutk = Tcoutarr.tolist()
	map(float, Tcout)

	Fharr = np.array ([0])
	Fharr.resize(nstages, nhot, ncold)
	Fcarr = np.array ([0])
	Fcarr.resize(nstages, ncold, nhot)
	Qarr = np.array ([0])
	Qarr.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Q[i][si][j][sj][sk][k]
	Q = Qarr.tolist()
	Qaux = Qarr.tolist()
	map(float, Q)
	map(float, Qaux)

	for quente in range(nhot):
		temperatura_atual_quente_abaixo.append(pinchq)
		temperatura_atual_quente_mesclada_abaixo.append(pinchq)
	for fria in range(ncold):
		temperatura_atual_fria_abaixo.append(pinchf)
		temperatura_atual_fria_mesclada_abaixo.append(pinchf)

	#CÁLCULOS DOS CALORES TOTAIS
	for i in range (nhot):
		Qtotalh01.append(CPh[i] * (Th0[i] - Thf[i]))
		calor_atual_quente_abaixo.append(CPh[i] * (Th0[i] - Thf[i]))
	for j in range (ncold):
		Qtotalc01.append(CPc[j] * (Tcf[j] - Tc0[j]))
		calor_atual_frio_abaixo.append(CPc[j] * (Tcf[j] - Tc0[j]))

	for i in range(nhot):
		for j in range(ncold):
			for k in range(nstages):
				Qtotalh0[i][0][k] = Qtotalh01[i]
				Qtotalc0[j][0][k] = Qtotalc01[j]

	#Prepara rede
	for i in range (nhot):
		#Este loop iguala as temperaturas iniciais de todos os SUB-ESTÁGIOS à temperatura inicial da corrente
		for si in range (ncold):
			for sk in range (nsk):
				for k in range (nstages):
					Thski[i][si][sk][k] = Th0[i]
					Thskf[i][si][sk][k] = Th0[i] #Thsk é a temperatura inicial do sub-estágio
		#Este loop iguala as temperaturas iniciais de todos os ESTÁGIOS à temperatura inicial da corrente
		for k in range (nstages):
			Thki[i][k] = Th0[i]
			Thkf[i][k] = Th0[i] #Thk é a temperatura inicial do estágio

	for j in range (ncold):
		for sj in range (nhot):
			for sk in range(nsk-1, -1, -1):
				for k in range(nstages-1, -1, -1):
					Tcski[j][sj][sk][k] = Tcf[j]
					Tcskf[j][sj][sk][k] = Tcf[j]
		for k in range (nstages-1, -1, -1):
			Tcki[j][k] = Tcf[j]
			Tckf[j][k] = Tcf[j]

def receber_pinch_abaixo(matriz_quente, matriz_fria, nquentes, nfrias, CPquente, CPfrio, deltaTmin, pinch_quente, pinch_frio):
	global Th0, Thf, Tc0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, nsi, nsj
	Th0, Thf, Tc0, Tcf = [], [], [], []
	limpar_lista(CPh)
	limpar_lista(CPc)
	for corrente in range(nquentes):
		Thf.append(matriz_quente[corrente])
		Th0.append(pinch_quente)
		CPh.append(CPquente[corrente])
	for corrente in range(nfrias):
		Tc0.append(matriz_fria[corrente])
		Tcf.append(pinch_frio)
		CPc.append(CPfrio[corrente])
	pinchq = pinch_quente
	pinchf = pinch_frio
	nhot = nquentes
	ncold = nfrias
	nsi = [ncold, ncold]
	nsj = [nhot, nhot]
	dTmin = deltaTmin
	preparar_dados_e_rede2()

def remocao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio):
	Qtotalestagioq = Qtotalestagiof = 0
	if Fharr[estagio-1][chot-1][sbhot-1] == 0:
		Qtotalh0[chot-1][sbhot-1][estagio-1] = Qtotalh0[chot-1][sbhot-1][estagio-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagioq = 0
			if k == (estagio-1):
				continue
			else:
				if Fharr[k][chot-1][sbhot-1] == 0:
					Qtotalh0[chot-1][sbhot-1][k] = Qtotalh0[chot-1][sbhot-1][k] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for si in range(ncold):
						Qtotalestagioq += Qtotalh0[chot-1][si][k]
					Qtotalestagioq = Qtotalestagioq - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for si in range(ncold):
						Qtotalh0[chot-1][si][k] = Qtotalestagioq*(Fharr[k][chot-1][si]/100)
	else:
		Qtotalh0[chot-1][sbhot-1][estagio-1] = Qtotalh0[chot-1][sbhot-1][estagio-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagioq = 0
			if k == (estagio-1):
				continue
			else:
				if Fharr[k][chot-1][sbhot-1] == 0:
					Qtotalh0[chot-1][0][k] = Qtotalh0[chot-1][0][k] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for si in range(ncold):
						Qtotalestagioq += Qtotalh0[chot-1][si][k]
					Qtotalestagioq = Qtotalestagioq - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for si in range(ncold):
						Qtotalh0[chot-1][si][k] = Qtotalestagioq*(Fharr[k][chot-1][si]/100)

	if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
		Qtotalc0[ccold-1][sbcold-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1][estagio-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagiof = 0
			if k == (estagio-1):
				continue
			else:
				if Fcarr[k][ccold-1][sbcold-1] == 0:
					Qtotalc0[ccold-1][sbcold-1][k] = Qtotalc0[ccold-1][sbcold-1][k] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for sj in range(nhot):
						Qtotalestagiof += Qtotalc0[ccold-1][sj][k]
					Qtotalestagiof = Qtotalestagiof - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for sj in range(nhot):
						Qtotalc0[ccold-1][sj][k] = Qtotalestagiof*(Fcarr[k][ccold-1][sj]/100)
	else:
		Qtotalc0[ccold-1][sbcold-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1][estagio-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagiof = 0
			if k == (estagio-1):
				continue
			else:
				if Fcarr[k][ccold-1][sbcold-1] == 0:
					Qtotalc0[ccold-1][0][k] = Qtotalc0[ccold-1][0][k] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for sj in range(nhot):
						Qtotalestagiof += Qtotalc0[ccold-1][sj][k]
					Qtotalestagiof = Qtotalestagiof - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for sj in range(nhot):
						Qtotalc0[ccold-1][sj][k] = Qtotalestagiof*(Fcarr[k][ccold-1][sj]/100)

def adicao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio):
	Qtotalestagioq = Qtotalestagiof = 0
	if Fharr[estagio-1][chot-1][sbhot-1] == 0:
		Qtotalh0[chot-1][sbhot-1][estagio-1] = Qtotalh0[chot-1][sbhot-1][estagio-1] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagioq = 0
			if k == (estagio-1):
				continue
			else:
				if Fharr[k][chot-1][sbhot-1] == 0:
					Qtotalh0[chot-1][sbhot-1][k] = Qtotalh0[chot-1][sbhot-1][k] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for si in range(ncold):
						Qtotalestagioq += Qtotalh0[chot-1][si][k]
					Qtotalestagioq = Qtotalestagioq + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for si in range(ncold):
						Qtotalh0[chot-1][si][k] = Qtotalestagioq*(Fharr[k][chot-1][si]/100)
	else:
		Qtotalh0[chot-1][sbhot-1][estagio-1] = Qtotalh0[chot-1][sbhot-1][estagio-1] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagioq = 0
			if k == (estagio-1):
				continue
			else:
				if Fharr[k][chot-1][sbhot-1] == 0:
					Qtotalh0[chot-1][0][k] = Qtotalh0[chot-1][0][k] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for si in range(ncold):
						Qtotalestagioq += Qtotalh0[chot-1][si][k]
					Qtotalestagioq = Qtotalestagioq + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for si in range(ncold):
						Qtotalh0[chot-1][si][k] = Qtotalestagioq*(Fharr[k][chot-1][si]/100)

	if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
		Qtotalc0[ccold-1][sbcold-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1][estagio-1] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagiof = 0
			if k == (estagio-1):
				continue
			else:
				if Fcarr[k][ccold-1][sbcold-1] == 0:
					Qtotalc0[ccold-1][sbcold-1][k] = Qtotalc0[ccold-1][sbcold-1][k] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for sj in range(nhot):
						Qtotalestagiof += Qtotalc0[ccold-1][sj][k]
					Qtotalestagiof = Qtotalestagiof + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for sj in range(nhot):
						Qtotalc0[ccold-1][sj][k] = Qtotalestagiof*(Fcarr[k][ccold-1][sj]/100)
	else:
		Qtotalc0[ccold-1][sbcold-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1][estagio-1] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagiof = 0
			if k == (estagio-1):
				continue
			else:
				if Fcarr[k][ccold-1][sbcold-1] == 0:
					Qtotalc0[ccold-1][0][k] = Qtotalc0[ccold-1][0][k] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for sj in range(nhot):
						Qtotalestagiof += Qtotalc0[ccold-1][sj][k]
					Qtotalestagiof = Qtotalestagiof + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for sj in range(nhot):
						Qtotalc0[ccold-1][sj][k] = Qtotalestagiof*(Fcarr[k][ccold-1][sj]/100)

def verificar_trocador_estagio_abaixo(estagio):
	for i in range (nhot):
		for si in range (ncold): #max de subcorrentes quentes é igual ao numero de correntes frias
			for j in range(ncold):
				for sj in range(nhot): #max de subcorrentes frias é igual ao numero de correntes quentes
					for sk in range (nsk):
						if Q[i][si][j][sj][sk][estagio-1] != 0:
							return True

def divisao_de_correntes_abaixo(divtype, estagio, corrente, quantidade, fracao):
	global nhot, ncold
	cont = 0
	qsi = quantidade
	qsj = quantidade
	if cont == 0:
		if divtype.upper() == 'Q':
			#desfaz divisoes anteriores
			for si in range(1, ncold):
				Qtotalh0[corrente-1][0][estagio-1] += Qtotalh0[corrente-1][si][estagio-1]
			for si in range(ncold-1, qsi-1, -1):#ex: antes 3 divisoes porem agora 2, zera a 3
				Fharr[estagio-1][corrente-1][si] = 0
				Qtotalh0[corrente-1][si][estagio-1] = 0

			#faz a nova divisao
			if qsi > nsi[corrente-1]:
				print('Erro! O número de divisões é muito grande.')
				return
			if qsi <= nsi[corrente-1]:
				for si in range(qsi):
					Fharr[estagio-1][corrente-1][si] = 100 * fracao[si]
				for si in range(ncold-1, -1, -1):
					if Fharr[estagio-1][corrente-1][si] != 0:
						Qtotalh0[corrente-1][si][estagio-1] = Qtotalh0[corrente-1][0][estagio-1]*(Fharr[estagio-1][corrente-1][si]/100)

			nhotc = qsi + (nhot - 1)

		if divtype.upper() == 'F':
			#desfaz divisoes anteriores
			for sj in range(1, nhot):
				Qtotalc0[corrente-1][0][estagio-1] += Qtotalc0[corrente-1][sj][estagio-1]
			for sj in range(nhot-1, qsj-1, -1):
				Fcarr[estagio-1][corrente-1][sj] = 0
				Qtotalc0[corrente-1][sj][estagio-1] = 0
			if qsj > nsj[corrente-1]:
				print('Erro! O número de divisões é muito grande.')
				return
			if qsj <= nsj[corrente-1]:
				for sj in range(qsj):
					Fcarr[estagio-1][corrente-1][sj] = 100 * fracao[sj]
				for sj in range(nhot-1, -1, -1):
					if Fcarr[estagio-1][corrente-1][sj] != 0:
						Qtotalc0[corrente-1][sj][estagio-1] = Qtotalc0[corrente-1][0][estagio-1]*(Fcarr[estagio-1][corrente-1][sj]/100)

			ncoldc = qsj + (ncold - 1)

def ler_dados_abaixo(dlg):
	i = int(dlg.comboBox_35.currentText())
	j = int(dlg.comboBox_36.currentText())
	si = int(dlg.comboBox_53.currentText())
	sj = int(dlg.comboBox_54.currentText())
	sk = int(dlg.comboBox_40.currentText())
	k = int(dlg.comboBox_39.currentText())

	if ((Qtotalh0[i-1][si-1][k-1]) > (Qtotalc0[j-1][sj-1][k-1])):
		Qmax = Qtotalc0[j-1][sj-1][k-1]
	else:
		Qmax = Qtotalh0[i-1][si-1][k-1]
	if dlg.radioButton_20.isChecked():
		q = Qmax
	elif dlg.radioButton_17.isChecked():
		q = float(dlg.lineEdit_25.text())

	return [i, j, si, sj, sk, k, q]


	#radioButton_17 é o heat load
	#radioButton_20 é o max heat
	#lineEdit_25 é o heat load
	pass

def inserir_trocador_abaixo(dlg, vetor):
	cont = 0

	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] != 0:
		QMessageBox.about(dlg,"Error!","There is already a heat exchanger in this position!")
		return

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = vetor[6]

	if ((Qtotalh0[chot-1][sbhot-1][estagio-1]) > (Qtotalc0[ccold-1][sbcold-1][estagio-1])):
		Qmax = Qtotalc0[ccold-1][sbcold-1][estagio-1]
	else:
		Qmax = Qtotalh0[chot-1][sbhot-1][estagio-1]

	if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] > Qmax:
		QMessageBox.about(dlg,"Error!","The inputed heat is greater than the available heat.")
		Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0
		return

	elif Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] < 0:
		QMessageBox.about(dlg,"Error!","It is not possible to change a negative amount of heat.")
		Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0
		return

	elif Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] == 0:
		QMessageBox.about(dlg,"Error!","The inputed heat must be greater than 0.")
		return


	for i in range (nhot):
		for si in range (ncold):
			for sk in range (nsk):
				for k in range (nstages):
					Thski[i][si][sk][k] = Th0[i]
					Thskf[i][si][sk][k] = Th0[i]

		for k in range (nstages):
			Thki[i][k] = Th0[i]
			Thkf[i][k] = Th0[i]

	for j in range (ncold):
		for sj in range (nhot):
			for sk in range(nsk-1, -1, -1):
				for k in range(nstages-1, -1, -1):
					Tcski[j][sj][sk][k] = Tcf[j]
					Tcskf[j][sj][sk][k] = Tcf[j]
		for k in range (nstages-1, -1, -1):
			Tcki[j][k] = Tcf[j]
			Tckf[j][k] = Tcf[j]

	# CÁLCULO DE TODA A SUPERESTRUTURA
	for k in range (nstages):
		for sk in range (nsk):
			for i in range (nhot):
				for si in range (ncold):
					for j in range(ncold):
						for sj in range(nhot):

							Qaux[i][si][j][sj][sk][k] = Q[i][si][j][sj][sk][k]

							if Qaux[i][si][j][sj][sk][k] != 0:

								#CALORES DOS ESTÁGIOS
								Qtotalhaux = 0
								for si1 in range (ncold):
									for j1 in range(ncold):
										for sj1 in range(nhot):
											for sk1 in range (nsk):
												Qtotalhaux += Qaux[chot-1][si1][j1][sj1][sk1][estagio-1]
								Qtotalcaux = 0
								for sj1 in range (nhot):
									for i1 in range(nhot):
										for si1 in range(ncold):
											for sk1 in range (nsk):
												Qtotalcaux += Qaux[i1][si1][ccold-1][sj1][sk1][estagio-1]

								Qestagioq[chot-1][estagio-1] = Qtotalhaux
								Qestagiof[ccold-1][estagio-1] = Qtotalcaux

								if Fharr[k][i][si] == 0:
									Fharr[k][i][si] = 100
								if Fcarr[k][j][sj] == 0:
									Fcarr[k][j][sj] = 100

								Thin[i][si][j][sj][sk][k] = Thski[i][si][sk][k]
								Thout[i][si][j][sj][sk][k] = Thin[i][si][j][sj][sk][k] - (Qaux[i][si][j][sj][sk][k]/(CPh[i]*(Fharr[k][i][si]/100)))
								temperatura_atual_quente_abaixo[i] = Thout[i][si][j][sj][sk][k]

								Think[i][si][j][sj][sk][k] = Thki[i][k]
								Thoutk[i][si][j][sj][sk][k] = Think[i][si][j][sj][sk][k] - (Qestagioq[i][k]/CPh[i])
								temperatura_atual_quente_mesclada_abaixo[i] = Thoutk[i][si][j][sj][sk][k]

								Tcin[i][si][j][sj][sk][k] = Tcski[j][sj][sk][k]
								Tcout[i][si][j][sj][sk][k] = Tcin[i][si][j][sj][sk][k] - (Qaux[i][si][j][sj][sk][k]/(CPc[j]*(Fcarr[k][j][sj]/100)))
								temperatura_atual_fria_abaixo[j] = Tcout[i][si][j][sj][sk][k]

								Tcink[i][si][j][sj][sk][k] = Tcki[j][k]
								Tcoutk[i][si][j][sj][sk][k] = Tcink[i][si][j][sj][sk][k] - (Qestagiof[j][k]/CPc[j])
								temperatura_atual_fria_mesclada_abaixo[j] = Tcoutk[i][si][j][sj][sk][k]

								tempdif = (Thin[i][si][j][sj][sk][k] - Tcin[i][si][j][sj][sk][k])
								tempdif_terminal_frio = Thout[i][si][j][sj][sk][k] - Tcout[i][si][j][sj][sk][k]
								violou = False
								violou_termo = False

								if tempdif < 0 or tempdif_terminal_frio < 0:
									QMessageBox.about(dlg, "Error!", "Thermodynamics Violation. The temperature of the cold stream will be greater thant the temperature of the hot stream")
									violou_termo = True
								elif tempdif >= dTmin and tempdif_terminal_frio >= dTmin:
									violou = False
								else:
									violou = True

								Thfinal01[i][si] = Thout[i][si][j][sj][sk][k]
								Tcfinal01[j][sj] = Tcout[i][si][j][sj][sk][k]
								Thfinal01k[i][k] = Thoutk[i][si][j][sj][sk][k]
								Tcfinal01k[j][k] = Tcoutk[i][si][j][sj][sk][k]

								#Temperatura inicial de estágios e sub-estágios
								for k1 in range(nstages):
									for sk1 in range(nsk):
										if k1 > (k):
											Tcki[j][k1] = Tcfinal01k[j][k]
											Tcski[j][sj][sk1][k1] = Tcfinal01k[j][k]
											Thki[i][k1] = Thfinal01k[i][k]
											Thski[i][si][sk1][k1] = Thfinal01k[i][k]
										if k1 == (k):
											if sk1 > (sk):
												Tcski[j][sj][sk1][k1] = Tcfinal01[j][sj]
												Thski[i][si][sk1][k1] = Thfinal01[i][si]

								#Temperatura final dos estágios e sub-estágios
								for k1 in range(nstages):
									for sk1 in range(nsk):
										if k1 > (k):
											Tckf[j][k1] = Tcfinal01k[j][k]
											Tcskf[j][sj][sk1][k1] = Tcfinal01k[j][k]
											Thkf[i][k1] = Thfinal01k[i][k]
											Thskf[i][si][sk1][k1] = Thfinal01k[i][k]
										if k1 == (k):
											if sk1 >= (sk):
												Tcskf[j][sj][sk1][k1] = Tcfinal01[j][sj]
												Thskf[i][si][sk1][k1] = Thfinal01[i][si]
											Tckf[j][k1] = Tcfinal01k[j][k]
											Thkf[i][k1] = Thfinal01k[i][k]

								if Fharr[k][i][si] == 100:
									Fharr[k][i][si] = 0
								if Fcarr[k][j][sj] == 100:
									Fcarr[k][j][sj] = 0

	remocao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	for k in range (nstages):
		for sk in range (nsk):
			for i in range (nhot):
				for si in range (ncold):
					for j in range(ncold):
						for sj in range(nhot):
							Qaux[i][si][j][sj][sk][k] = 0

	if Fharr[estagio-1][chot-1][sestagio-1] == 0:
		fracao_quente = 1
	else:
		fracao_quente = Fharr[estagio-1][chot-1][sbhot-1]/100
	if Fharr[estagio-1][ccold-1][sestagio-1] == 0:
		fracao_fria = 1
	else:
		fracao_fria = Fcarr[estagio-1][ccold-1][sbcold-1]/100

	calor_atual_quente_abaixo[chot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
	calor_atual_frio_abaixo[ccold-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

	linha_interface_abaixo.append([chot,
							ccold,
							sbhot,
							sbcold,
							sestagio,
							estagio,
							Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1],
							Thskf[chot-1][sbhot-1][sestagio-1][estagio-1],
							Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1],
							fracao_quente,
							fracao_fria])

	for trocador in linha_interface_abaixo:
		trocador[7] = Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[8] = Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]

	return linha_interface_abaixo, violou, violou_termo, tempdif, tempdif_terminal_frio

def remover_trocador_abaixo(dlg, vetor, indice, linha_interface_abaixo):
	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] == 0:
		QMessageBox.about(dlg,"Error!","There is no heat exchanger in this position.")
		return

	adicao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0

	for i in range (nhot):
		#Este loop iguala as temperaturas iniciais de todos os SUB-ESTÁGIOS à temperatura inicial da corrente
		for si in range (ncold):
			for sk in range (nsk):
				for k in range (nstages):
					Thski[i][si][sk][k] = Th0[i]
					Thskf[i][si][sk][k] = Th0[i] #Thsk é a temperatura inicial do sub-estágio
		#Este loop iguala as temperaturas iniciais de todos os ESTÁGIOS à temperatura inicial da corrente
		for k in range (nstages):
			Thki[i][k] = Th0[i]
			Thkf[i][k] = Th0[i] #Thk é a temperatura inicial do estágio

	for j in range (ncold):
		for sj in range (nhot):
			for sk in range(nsk-1, -1, -1):
				for k in range(nstages-1, -1, -1):
					Tcski[j][sj][sk][k] = Tcf[j]
					Tcskf[j][sj][sk][k] = Tcf[j]
		for k in range (nstages-1, -1, -1):
			Tcki[j][k] = Tcf[j]
			Tckf[j][k] = Tcf[j]

	#CÁLCULO DA SUPERESTRUTURA
	for k in range (nstages):
		for sk in range (nsk):
			for i in range (nhot):
				for si in range (ncold):
					for j in range(ncold):
						for sj in range(nhot):

							Qaux[i][si][j][sj][sk][k] = Q[i][si][j][sj][sk][k]

							if Qaux[i][si][j][sj][sk][k] != 0:

								#CALORES DOS ESTÁGIOS
								Qtotalhaux = 0
								for si1 in range (ncold):
									for j1 in range(ncold):
										for sj1 in range(nhot):
											for sk1 in range (nsk):
												Qtotalhaux += Qaux[chot-1][si1][j1][sj1][sk1][estagio-1]
								Qtotalcaux = 0
								for sj1 in range (nhot):
									for i1 in range(nhot):
										for si1 in range(ncold):
											for sk1 in range (nsk):
												Qtotalcaux += Qaux[i1][si1][ccold-1][sj1][sk1][estagio-1]

								Qestagioq[chot-1][estagio-1] = Qtotalhaux
								Qestagiof[ccold-1][estagio-1] = Qtotalcaux

								if Fharr[k][i][si] == 0:
									Fharr[k][i][si] = 100
								if Fcarr[k][j][sj] == 0:
									Fcarr[k][j][sj] = 100

								Thin[i][si][j][sj][sk][k] = Thski[i][si][sk][k]
								Thout[i][si][j][sj][sk][k] = Thin[i][si][j][sj][sk][k] - (Q[i][si][j][sj][sk][k]/(CPh[i]*(Fharr[k][i][si]/100)))
								temperatura_atual_quente_abaixo[i] = Thout[i][si][j][sj][sk][k]

								Think[i][si][j][sj][sk][k] = Thki[i][k]
								Thoutk[i][si][j][sj][sk][k] = Think[i][si][j][sj][sk][k] - (Qestagioq[i][k]/CPh[i])
								temperatura_atual_quente_mesclada_abaixo[i] = Thoutk[i][si][j][sj][sk][k]

								Tcin[i][si][j][sj][sk][k] = Tcski[j][sj][sk][k]
								Tcout[i][si][j][sj][sk][k] = Tcin[i][si][j][sj][sk][k] - (Q[i][si][j][sj][sk][k]/(CPc[j]*(Fcarr[k][j][sj]/100)))
								temperatura_atual_fria_abaixo[j] = Tcout[i][si][j][sj][sk][k]

								Tcink[i][si][j][sj][sk][k] = Tcki[j][k]
								Tcoutk[i][si][j][sj][sk][k] = Tcink[i][si][j][sj][sk][k] - (Qestagiof[j][k]/CPc[j])
								temperatura_atual_fria_mesclada_abaixo[j] = Tcoutk[i][si][j][sj][sk][k]

								Thfinal01[i][si] = Thout[i][si][j][sj][sk][k]
								Tcfinal01[j][sj] = Tcout[i][si][j][sj][sk][k]
								Thfinal01k[i][k] = Thoutk[i][si][j][sj][sk][k]
								Tcfinal01k[j][k] = Tcoutk[i][si][j][sj][sk][k]

								#Temperatura inicial de estágios e sub-estágios
								for k1 in range(nstages):
									for sk1 in range(nsk):
										if k1 > (k):
											Tcki[j][k1] = Tcfinal01k[j][k]
											Tcski[j][sj][sk1][k1] = Tcfinal01k[j][k]
											Thki[i][k1] = Thfinal01k[i][k]
											Thski[i][si][sk1][k1] = Thfinal01k[i][k]
										if k1 == (k):
											if sk1 > (sk):
												Tcski[j][sj][sk1][k1] = Tcfinal01[j][sj]
												Thski[i][si][sk1][k1] = Thfinal01[i][si]

										#Temperatura final dos estágios e sub-estágios
								for k1 in range(nstages):
									for sk1 in range(nsk):
										if k1 > (k):
											Tckf[j][k1] = Tcfinal01k[j][k]
											Tcskf[j][sj][sk1][k1] = Tcfinal01k[j][k]
											Thkf[i][k1] = Thfinal01k[i][k]
											Thskf[i][si][sk1][k1] = Thfinal01k[i][k]
										if k1 == (k):
											if sk1 >= (sk):
												Tcskf[j][sj][sk1][k1] = Tcfinal01[j][sj]
												Thskf[i][si][sk1][k1] = Thfinal01[i][si]
											Tckf[j][k1] = Tcfinal01k[j][k]
											Thkf[i][k1] = Thfinal01k[i][k]

								if Fharr[k][i][si] == 100:
									Fharr[k][i][si] = 0
								if Fcarr[k][j][sj] == 100:
									Fcarr[k][j][sj] = 0

	for k in range (nstages):
		for sk in range (nsk):
			for i in range (nhot):
				for si in range (ncold):
					for j in range(ncold):
						for sj in range(nhot):
							Qaux[i][si][j][sj][sk][k] = 0

	if Fharr[estagio-1][chot-1][sestagio-1] == 0:
		fracao_quente = 1
	if Fharr[estagio-1][ccold-1][sestagio-1] == 0:
		fracao_fria = 1

	calor_atual_quente_abaixo[chot-1] += vetor[6]
	calor_atual_frio_abaixo[ccold-1] += vetor[6]

	if calor_atual_quente_abaixo[chot-1] == Qtotalh01[chot-1]:
		temperatura_atual_quente_abaixo[chot-1] = pinchq
		temperatura_atual_quente_mesclada_abaixo[chot-1] = pinchq
	if calor_atual_frio_abaixo[ccold-1] == Qtotalc01[ccold-1]:
		temperatura_atual_fria_abaixo[ccold-1] = pinchf
		temperatura_atual_fria_mesclada_abaixo[ccold-1] = pinchf

	try:
		linha_interface_abaixo.pop(indice)
	except:
		QMessageBox.about(dlg, "Error!", "There is no heat exchanger in this position.")

	return linha_interface_abaixo

def atualizar_matriz_abaixo(matriz):
	for trocador in matriz:
		trocador[7] = Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[8] = Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]

def adicionar_utilidade_abaixo(dlg, corrente):
	chotutil = corrente
	q = Qtotalh0[chotutil-1][0][0]
	for si in range(ncold):
		for k in range(nstages):
			if q < Qtotalh0[chotutil-1][si][k]:
				q = Qtotalh0[chotutil-1][si][k]
			Qtotalh0[chotutil-1][si][k] = 0
	if q == 0:
		QMessageBox.about(dlg, "Error!", "The heat of this stream has already been supplied")
		return
	temperatura_atual_quente_abaixo[chotutil-1] = Thf[chotutil-1]
	calor_atual_quente_abaixo[chotutil-1] = 0.0
	utilidades_abaixo.append([chotutil, q])
	return utilidades_abaixo

def remover_utilidade_abaixo(corrente, indice_remover, utilidades_abaixo):
	Qtotalh0[corrente-1][0][0] = utilidades_abaixo[indice_remover][1]
	calor_atual_quente_abaixo[corrente-1] = Qtotalh0[corrente-1][0][0]
	temperatura_atual_quente_abaixo[corrente-1] = calor_atual_quente_abaixo[corrente-1] / CPh[corrente-1] + Thf[corrente-1]
	utilidades_abaixo.pop(indice_remover)

def caixa_de_temperatura_abaixo(dlg):
	chot = int(dlg.TempLoadBelow.comboBox.currentText())
	ccold = int(dlg.TempLoadBelow.comboBox_2.currentText())
	sbhot = int(dlg.TempLoadBelow.comboBox_3.currentText())
	sbcold = int(dlg.TempLoadBelow.comboBox_4.currentText())
	estagio = int(dlg.TempLoadBelow.comboBox_5.currentText())
	sestagio = int(dlg.TempLoadBelow.comboBox_6.currentText())

	if dlg.TempLoadBelow.radioButton_2.isChecked():                     #Inlet Hot Temperature
		outlethot = float(dlg.TempLoadBelow.lineEdit_2.text())
		q = -CPh[chot-1] * (outlethot - Thski[chot-1][sbhot-1][sestagio-1][estagio-1])
	if dlg.TempLoadBelow.radioButton.isChecked():
		inletcold = float(dlg.TempLoadBelow.lineEdit.text())
		q = -CPc[ccold-1] * (inletcold - Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1])

	if ((Qtotalh0[chot-1][sbhot-1][estagio-1]) > (Qtotalc0[ccold-1][sbcold-1][estagio-1])):
		Qmax = Qtotalc0[ccold-1][sbcold-1][estagio-1]
	else:
		Qmax = Qtotalh0[chot-1][sbhot-1][estagio-1]

	if q > Qmax:
		QMessageBox.about(dlg, "Error!", "The calculated heat is greater than the available heat.")
		return
	if q < 0:
		QMessageBox.about(dlg, "Error!", "The calculated heat is negative.")
		return
	if q == 0:
		QMessageBox.about(dlg, "Error!", "The calculated heat is equals 0.")
		return

	dlg.lineEdit_25.setText(str(float('{:.1f}'.format(q))))
	dlg.radioButton_17.setChecked(True)
	dlg.comboBox_35.setCurrentText(str(dlg.TempLoadBelow.comboBox.currentText()))  #hot strem
	dlg.comboBox_36.setCurrentText(str(dlg.TempLoadBelow.comboBox_2.currentText()))  #cold stream
	dlg.comboBox_40.setCurrentText(str(dlg.TempLoadBelow.comboBox_6.currentText())) #sk
	dlg.comboBox_39.setCurrentText(str(dlg.TempLoadBelow.comboBox_5.currentText())) #k
	dlg.comboBox_53.setCurrentText(str(dlg.TempLoadBelow.comboBox_3.currentText())) #si
	dlg.comboBox_54.setCurrentText(str(dlg.TempLoadBelow.comboBox_4.currentText())) #sj
	dlg.TempLoadBelow.close()

def testar_correntes():
	for i in CPh:
		somaCPh += i

	for j in CPc:
		somaCPc += j

	for i in range(nhot):
		compq = Th0[i] - pinchq
		complistq.append(compq)

	for j in range(ncold):
		compf = Tcf[j] - pinchf
		complistf.append(compf)

	for i in complistq:
		if i == 0:
			nhotc += 1

	for j in complistf:
		if j == 0:
			ncoldc += 1

	while ncoldc > nhotc or somaCPc >= somaCPh:
		print('Erro')
		if somaCPc >= somaCPh:
			sys.exit('A somatória dos CPs das correntes frias é maior que a somatória dos CPs das correntes quentes!')

		elif ncoldc > nhotc:
			divop = str(input('A quantidade de correntes frias é maior do que a quantidade de correntes quentes. Você gostaria de dividir correntes? ')).strip().upper()[0]
			if divop == 'Y':
				divtype = input("Deseja dividir correntes quentes, frias ou ambas? ").strip().upper()[0]
				estagio = int(input('Em qual estágio ocorrerá a divisão? '))
				divisao_de_correntes()
			else:
				break
