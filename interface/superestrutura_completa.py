from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMessageBox
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import threading

dTmin = 0
nhot = 0
ncold = 0
pinchq = 0
pinchf = 0

cont = 0
chot = ccold = sbhot = sbcold = estagio = sestagio = qsi = qsj = 0
tempdif = 0

nstages = 2
nsk = 10

linha_interface_ev = []
utilidades = []
utilidades_abaixo = []


#VARIÁVEIS DE CALOR
Qtotalh01 = []
Qtotalc01 = []
Qtotalh0 = []
Qtotalc0 = []
Qestagioq = []
Qestagiof = []
calor_atual_quente_ev = []
calor_atual_frio_ev = []
calor_atual_quente_ev_sub = []
calor_atual_frio_ev_sub = []
calor_sub_sem_utilidade_ev = []
Qtotalestagio = Qtotalestagiof = Qmax = Qtotalhaux = Qtotalcaux = 0


#VARIÁVEIS DE TEMPERATURAS QUENTES
Thski = []
Thki = []
Thskf = []
Thkf = []
Thfinal01 = []
Thfinal01k = []
temperatura_atual_quente_ev = []
temperatura_atual_quente_ev_mesclada = []
temp_misturador_quente = []

#VARIÁVEIS DE TEMPERATURAS FRIAS
Tcski = []
Tcki = []
Tcskf = []
Tckf = []
Tcfinal01 = []
Tcfinal01k = []
temperatura_atual_fria_ev = []
temperatura_atual_fria_ev_mesclada = []
temp_misturador_frio = []

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
dividida_quente_ev_acima = []
dividida_quente_ev_abaixo = []
dividida_fria_ev_acima = []
dividida_fria_ev_abaixo = []
quantidade_quente_ev_acima = []
quantidade_quente_ev_abaixo = []
quantidade_fria_ev_acima = []
quantidade_fria_ev_abaixo = []
fracoes_quentes_ev_acima = []
fracoes_quentes_ev_abaixo = []
fracoes_frias_ev_acima = []
fracoes_frias_ev_abaixo = []
fechar_corrente_ev = []
fechar_corrente_ev_abaixo = []

def preparar_dados_e_rede():
	global Qtotalh01, Qtotalc01, Qtotalh0, Qtotalc0, Qestagioq, Qestagiof
	global Thski, Thki, Thskf, Thkf, Thfinal01, Thfinal01k
	global Tcski, Tcki, Tcskf, Tckf, Tcfinal01, Tcfinal01k
	global Thin, Thout, Tcin, Tcout, Think, Thoutk, Tcink, Tcoutk
	global Fharr, Fcarr, Qarr, Q, Qaux
	global linha_interface_ev, utilidades, utilidades_abaixo
	global calor_atual_frio_ev, calor_atual_quente_ev, calor_atual_quente_ev_sub, calor_atual_frio_ev_sub, calor_sub_sem_utilidade_ev
	global temperatura_atual_quente_ev,	temperatura_atual_quente_ev_mesclada, temp_misturador_ev_abaixo, temperatura_atual_fria_ev,	temperatura_atual_fria_ev_mesclada,	temp_misturador_quente, temp_misturador_frio
	global dividida_quente_ev_acima, dividida_quente_ev_abaixo, dividida_fria_ev_acima, dividida_fria_ev_abaixo, quantidade_quente_ev_acima, quantidade_quente_ev_abaixo, quantidade_fria_ev_acima, quantidade_fria_ev_abaixo, fracoes_quentes_ev, fracoes_frias_ev, fechar_corrente_ev, fechar_corrente_ev_abaixo

	Qtotalh0arr = np.array([0])
	Qtotalh0arr.resize(nhot, ncold+2, nstages)
	Qtotalh0 = Qtotalh0arr.tolist()
	map(float, Qtotalh0)
	Qtotalc0arr = np.array([0])
	Qtotalc0arr.resize(ncold, nhot+2, nstages)
	Qtotalc0 = Qtotalc0arr.tolist()
	map(float, Qtotalc0)
	Qestagioq = np.array([0])
	Qestagioq.resize(nhot, nstages)
	Qestagioq = Qestagioq.tolist()
	map(float, Qestagioq)
	Qestagiof = np.array([0])
	Qestagiof.resize(ncold, nstages)
	Qestagiof = Qestagiof.tolist()
	map(float, Qestagiof)

	Thskiarr = np.array ([0])
	Thskiarr.resize(nhot, ncold+2, nsk, nstages)
	Thski = Thskiarr.tolist()
	map(float, Thski)
	Thkiarr = np.array ([0])
	Thkiarr.resize(nhot, nstages)
	Thki = Thkiarr.tolist()
	map(float, Thki)
	Thskfarr = np.array ([0])
	Thskfarr.resize(nhot, ncold+2, nsk, nstages)
	Thskf = Thskfarr.tolist()
	map(float, Thskf)
	Thkfarr = np.array ([0])
	Thkfarr.resize(nhot, nstages)
	Thkf = Thkfarr.tolist()
	map(float, Thkf)
	Thfinal01arr = np.array ([0])
	Thfinal01arr.resize(nhot, ncold+2)
	Thfinal01 = Thfinal01arr.tolist()
	map(float, Thfinal01)
	Thfinal01karr = np.array ([0])
	Thfinal01karr.resize(nhot, nstages)
	Thfinal01k = Thfinal01karr.tolist()
	map(float, Thfinal01k)

	Tcskiarr = np.array ([0])
	Tcskiarr.resize(ncold, nhot+2, nsk, nstages)
	Tcski = Tcskiarr.tolist()
	map(float, Tcski)
	Tckiarr = np.array ([0])
	Tckiarr.resize(ncold, nstages)
	Tcki = Tckiarr.tolist()
	map(float, Tcki)
	Tcskfarr = np.array ([0])
	Tcskfarr.resize(ncold, nhot+2, nsk, nstages)
	Tcskf = Tcskfarr.tolist()
	map(float, Tcskf)
	Tckfarr = np.array ([0])
	Tckfarr.resize(ncold, nstages)
	Tckf = Tckfarr.tolist()
	map(float, Tckf)
	Tcfinal01arr = np.array ([0])
	Tcfinal01arr.resize(ncold, nhot+2)
	Tcfinal01 = Tcfinal01arr.tolist()
	map(float, Tcfinal01)
	Tcfinal01karr = np.array ([0])
	Tcfinal01karr.resize(ncold, nstages)
	Tcfinal01k = Tcfinal01karr.tolist()
	map(float, Tcfinal01k)

	Thinarr = np.array ([0])
	Thinarr.resize(nhot, ncold, ncold+2, nhot+2, nsk, nstages)  #Temperatura de entrada quente de um trocador
	Thin = Thinarr.tolist()
	map(float, Thin)
	Tcinarr = np.array ([0])
	Tcinarr.resize(nhot, ncold, ncold+2, nhot+2, nsk, nstages)  #Temperatura de entrada fria de um trocador
	Tcin = Tcinarr.tolist()
	map(float, Tcin)
	Thoutarr = np.array ([0])
	Thoutarr.resize(nhot, ncold, ncold+2, nhot+2, nsk, nstages)  #Temperatura de saída quente de um trocador
	Thout = Thoutarr.tolist()
	map(float, Thout)
	Tcoutarr = np.array ([0])
	Tcoutarr.resize(nhot, ncold, ncold+2, nhot+2, nsk, nstages) #Temperatura de saída fria de um trocador
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
	Fharr.resize(nstages, nhot, ncold+2)
	Fharr = Fharr.tolist()
	Fcarr = np.array ([0])
	Fcarr.resize(nstages, ncold, nhot+2)
	Fcarr = Fcarr.tolist()
	Qarr = np.array ([0])
	Qarr.resize(nhot, ncold+2, ncold, nhot+2, nsk, nstages)  #Q[i][si][j][sj][sk][k]
	Q = Qarr.tolist()
	Qaux = Qarr.tolist()
	map(float, Q)
	map(float, Qaux)

	for quente in range(nhot):
		temperatura_atual_quente_ev.append([])
		temperatura_atual_quente_ev_mesclada.append(Th0[quente])
		temp_misturador_quente.append(0)
		calor_atual_quente_ev_sub.append([])
		dividida_quente_ev_acima.append(False)
		dividida_quente_ev_abaixo.append(False)
		fechar_corrente_ev_abaixo.append(False)
		quantidade_quente_ev_acima.append(1)
		quantidade_quente_ev_abaixo.append(1)
		fracoes_quentes_ev_acima.append([])
		fracoes_quentes_ev_abaixo.append([])
		for sub in range(ncold+2):
			calor_atual_quente_ev_sub[quente].append(0)
			temperatura_atual_quente_ev[quente].append(Th0[quente])
	for fria in range(ncold):
		temperatura_atual_fria_ev.append([])
		temperatura_atual_fria_ev_mesclada.append(Tc0[fria])
		temp_misturador_frio.append(0)
		calor_atual_frio_ev_sub.append([])
		calor_sub_sem_utilidade_ev.append([])
		dividida_fria_ev_acima.append(False)
		dividida_fria_ev_abaixo.append(False)
		fechar_corrente_ev.append(False)
		quantidade_fria_ev_acima.append(1)
		quantidade_fria_ev_abaixo.append(1)
		fracoes_frias_ev_acima.append([])
		fracoes_frias_ev_abaixo.append([])
		for sub in range(nhot+2):
			calor_atual_frio_ev_sub[fria].append(0)
			temperatura_atual_fria_ev[fria].append(Tc0[fria])

	#CÁLCULOS DOS CALORES TOTAIS
	for i in range (nhot):
		Qtotalh01.append(CPh[i] * (Th0[i] - Thf[i]))
		calor_atual_quente_ev.append(CPh[i] * (Th0[i] - Thf[i]))
		calor_atual_quente_ev_sub[i][0] = CPh[i] * (Th0[i] - Thf[i])
	for j in range (ncold):
		Qtotalc01.append(CPc[j] * (Tcf[j] - Tc0[j]))
		calor_atual_frio_ev.append(CPc[j] * (Tcf[j] - Tc0[j]))
		calor_atual_frio_ev_sub[j][0] = CPc[j] * (Tcf[j] - Tc0[j])

	for i in range(nhot):
		for j in range(ncold):
			for k in range(nstages):
				Qtotalh0[i][0][k] = Qtotalh01[i]
				Qtotalc0[j][0][k] = Qtotalc01[j]

	#Prepara rede
	for i in range (nhot):
		#Este loop iguala as temperaturas iniciais de todos os SUB-ESTÁGIOS à temperatura inicial da corrente
		for si in range (ncold+2):
			for sk in range (nsk):
				for k in range (nstages):
					Thski[i][si][sk][k] = Th0[i]
					Thskf[i][si][sk][k] = Th0[i] #Thsk é a temperatura inicial do sub-estágio
		#Este loop iguala as temperaturas iniciais de todos os ESTÁGIOS à temperatura inicial da corrente
		for k in range (nstages):
			Thki[i][k] = Th0[i]
			Thkf[i][k] = Th0[i] #Thk é a temperatura inicial do estágio

	for j in range (ncold):
		for sj in range (nhot+2):
			for sk in range(nsk-1, -1, -1):
				for k in range(nstages-1, -1, -1):
					Tcski[j][sj][sk][k] = Tcf[j]
					Tcskf[j][sj][sk][k] = Tcf[j]
		for k in range (nstages-1, -1, -1):
			Tcki[j][k] = Tcf[j]
			Tckf[j][k] = Tcf[j]

def receber_pinch_ev(matriz_quente, matriz_fria, nquentes, nfrias, CPquente, CPfrio, deltaTmin, pinch_quente, pinch_frio, matriz_quente_in, matriz_fria_in):
	global Th0, Thf, Tc0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, nsk
	Th0, Thf, Tc0, Tcf = [], [], [], []
	CPh, CPc = [], []
	for corrente in range(nquentes):
		Th0.append(matriz_quente_in[corrente])
		Thf.append(matriz_quente[corrente])
		CPh.append(CPquente[corrente])
	for corrente in range(nfrias):
		Tc0.append(matriz_fria_in[corrente])
		Tcf.append(matriz_fria[corrente])
		CPc.append(CPfrio[corrente])
	pinchq = pinch_quente
	pinchf = pinch_frio
	nhot = nquentes
	ncold = nfrias
	dTmin = deltaTmin
	#nsk = 2*nhot*ncold
	preparar_dados_e_rede()

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

def calcular_superestrutura(dlg, acao, chot, ccold, sbhot, sbcold, sestagio, estagio, ultima):
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
					Tcski[j][sj][sk][k] = Tc0[j]
					Tcskf[j][sj][sk][k] = Tc0[j]
		for k in range (nstages-1, -1, -1):
			Tcki[j][k] = Tc0[j]
			Tckf[j][k] = Tc0[j]

	violou = False
	trocador_violado = []

	#CÁLCULO DE TODA A SUPERESTRUTURA QUENTE
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

								Qestagioq[chot-1][estagio-1] = Qtotalhaux

								if Fharr[k][i][si] == 0:
									Fharr[k][i][si] = 100

								Thin[i][si][j][sj][sk][k] = Thski[i][si][sk][k]
								Thout[i][si][j][sj][sk][k] = Thin[i][si][j][sj][sk][k] - (Q[i][si][j][sj][sk][k]/(CPh[i]*Fharr[k][i][si]/100))

								Think[i][si][j][sj][sk][k] = Thki[i][k]
								Thoutk[i][si][j][sj][sk][k] = Think[i][si][j][sj][sk][k] - (Qestagioq[i][k]/CPh[i])

								temperatura_atual_quente_ev_mesclada[i] = Thoutk[i][si][j][sj][sk][k]

								Thfinal01[i][si] = Thout[i][si][j][sj][sk][k]
								Thfinal01k[i][k] = Thoutk[i][si][j][sj][sk][k]

								#Temperatura de estágios e sub-estágios
								for k1 in range(nstages):
									for sk1 in range(nsk):
										if k1 > (k): #para estágios mais a esqueda do atual da superestrutura, todas as temperaturas recebem a temperatura pós troca
											#entrada
											Thki[i][k1] = Thfinal01k[i][k]

											#saida
											Thkf[i][k1] = Thfinal01k[i][k]

											for sub_quente in range(ncold):
												Thski[i][sub_quente][sk1][k1] = Thfinal01k[i][k]
												Thskf[i][sub_quente][sk1][k1] = Thfinal01k[i][k]

										if k1 == (k): #para o estágio atual da superestrutura, depende de qual subestagio
											if sk1 >= (sk): #para os subestagios a esquerda ou atual da superestrutura, depende se entra ou sai
												if sk1 > sk: #para os a esquerda, entra recebe após troca
													Thski[i][si][sk1][k1] = Thfinal01[i][si]
												Thskf[i][si][sk1][k1] = Thfinal01[i][si]

											Thkf[i][k1] = Thfinal01k[i][k]

								if Fharr[k][i][si] == 100:
									Fharr[k][i][si] = 0

	#CÁLCULO DE TODA A SUPERESTRUTURA FRIA
	for k in range (nstages-1, -1, -1):
		for sk in range (nsk-1, -1, -1):
			for i in range (nhot):
				for si in range (ncold):
					for j in range(ncold):
						for sj in range(nhot):

							Qaux[i][si][j][sj][sk][k] = Q[i][si][j][sj][sk][k]

							if Qaux[i][si][j][sj][sk][k] != 0:

								#CALORES DOS ESTÁGIOS
								Qtotalcaux = 0
								for sj1 in range (nhot):
									for i1 in range(nhot):
										for si1 in range(ncold):
											for sk1 in range (nsk):
												Qtotalcaux += Qaux[i1][si1][ccold-1][sj1][sk1][estagio-1]

								Qestagiof[ccold-1][estagio-1] = Qtotalcaux

								if Fcarr[k][j][sj] == 0:
									Fcarr[k][j][sj] = 100


								Tcin[i][si][j][sj][sk][k] = Tcski[j][sj][sk][k]
								Tcout[i][si][j][sj][sk][k] = Tcin[i][si][j][sj][sk][k] + (Q[i][si][j][sj][sk][k]/(CPc[j]*Fcarr[k][j][sj]/100))

								Tcink[i][si][j][sj][sk][k] = Tcki[j][k]
								Tcoutk[i][si][j][sj][sk][k] = Tcink[i][si][j][sj][sk][k] + (Qestagiof[j][k]/CPc[j])

								tempdif = Thin[i][si][j][sj][sk][k] - Tcout[i][si][j][sj][sk][k]
								tempdif_terminal_frio = Thout[i][si][j][sj][sk][k] - Tcin[i][si][j][sj][sk][k]

								temperatura_atual_fria_ev_mesclada[j] = Tcoutk[i][si][j][sj][sk][k]

								Tcfinal01[j][sj] = Tcout[i][si][j][sj][sk][k]
								Tcfinal01k[j][k] = Tcoutk[i][si][j][sj][sk][k]

								#Temperatura de estágios e sub-estágios
								for k1 in range(nstages):
									for sk1 in range(nsk):
										if k1 < (k): #para estágios mais a esqueda do atual da superestrutura, todas as temperaturas recebem a temperatura pós troca
											#entrada
											Tcki[j][k1] = Tcfinal01k[j][k]

											#saida
											Tckf[j][k1] = Tcfinal01k[j][k]

											for sub_fria in range(nhot):
												Tcski[j][sub_fria][sk1][k1] = Tcfinal01k[j][k]
												Tcskf[j][sub_fria][sk1][k1] = Tcfinal01k[j][k]

										if k1 == (k): #para o estágio atual da superestrutura, depende de qual subestagio
											if sk1 <= (sk): #para os subestagios a esquerda ou atual da superestrutura, depende se entra ou sai
												if sk1 < sk: #para os a esquerda, entra recebe após troca
													Tcski[j][sj][sk1][k1] = Tcfinal01[j][sj]
												Tcskf[j][sj][sk1][k1] = Tcfinal01[j][sj] #atual e a esquerda, final recebe após troca

											Tckf[j][k1] = Tcfinal01k[j][k]

								if Fcarr[k][j][sj] == 100:
									Fcarr[k][j][sj] = 0



	for k in range (nstages):
		for sk in range (nsk):
			for i in range (nhot):
				for si in range (ncold):
					for j in range(ncold):
						for sj in range(nhot):
							Qaux[i][si][j][sj][sk][k] = 0
	# print()
	# print()
	# print()
	# print("_____________________________________________________________")
	# for k in range(nstages):
	# 	print('ESTÁGIO ', k+1)
	# 	print('Tentra:', Thki[chot-1][k])
	# 	print('Tsai:', Thkf[chot-1][k])
	# 	print()
	#
	# 	for sk in range(nsk):
	# 		print('SUB-ESTÁGIO ', sk+1)
	# 		for sub in range(ncold):
	# 			print("SUB", sub+1)
	# 			print('Tentra:', Thski[chot-1][sub][sk][k])
	# 			print('Tsai:', Thskf[chot-1][sub][sk][k])
	# 		print()
	# 	print()


	return violou, trocador_violado

def divisao_de_correntes_ev(divtype, estagio, corrente, quantidade, fracao):
	qsi = quantidade
	qsj = quantidade
	cont = 0
	if cont == 0:
		if divtype.upper() == 'Q':
			#desfaz divisoes anteriores da corrente no estagio
			for si in range(1, ncold):
				Qtotalh0[corrente-1][0][estagio-1] += Qtotalh0[corrente-1][si][estagio-1]
			for si in range(ncold-1, qsi-1, -1):#ex: antes 3 divisoes porem agora 2, zera a 3
				Fharr[estagio-1][corrente-1][si] = 0
				Qtotalh0[corrente-1][si][estagio-1] = 0
			#faz a nova divisao
			if qsi <= ncold:
				for si in range(qsi):
					Fharr[estagio-1][corrente-1][si] = 100 * fracao[si]
				for si in range(ncold-1, -1, -1):
					if Fharr[estagio-1][corrente-1][si] != 0:
						Qtotalh0[corrente-1][si][estagio-1] = Qtotalh0[corrente-1][0][estagio-1]*(Fharr[estagio-1][corrente-1][si]/100)
						calor_atual_quente_ev_sub[corrente-1][si] = Qtotalh0[corrente-1][si][estagio-1]
			if estagio == 1:
				if fracao[0] != 1:
					dividida_quente_ev_acima[corrente-1] = True
				else:
					dividida_quente_ev_acima[corrente-1] = False
				quantidade_quente_ev_acima[corrente-1] = qsi
				fracoes_quentes_ev_acima[corrente-1] = fracao[:]
			else:
				if fracao[0] != 1:
					dividida_quente_ev_abaixo[corrente-1] = True
				else:
					dividida_quente_ev_abaixo[corrente-1] = False
				quantidade_quente_ev_abaixo[corrente-1] = qsi
				fracoes_quentes_ev_abaixo[corrente-1] = fracao[:]

		if divtype.upper() == 'F':
			#desfaz divisoes anteriores da corrente no estagio
			for sj in range(1, nhot):
				Qtotalc0[corrente-1][0][estagio-1] += Qtotalc0[corrente-1][sj][estagio-1]
			for sj in range(nhot-1, qsj-1, -1):
				Fcarr[estagio-1][corrente-1][sj] = 0
				Qtotalc0[corrente-1][sj][estagio-1] = 0
			#faz a nova divisao
			if qsj <= nhot:
				for sj in range(qsj):
					Fcarr[estagio-1][corrente-1][sj] = 100 * fracao[sj]
				for sj in range(nhot-1, -1, -1):
					if Fcarr[estagio-1][corrente-1][sj] != 0:
						Qtotalc0[corrente-1][sj][estagio-1] = Qtotalc0[corrente-1][0][estagio-1]*(Fcarr[estagio-1][corrente-1][sj]/100)
						calor_atual_frio_ev_sub[corrente-1][sj] = Qtotalc0[corrente-1][sj][estagio-1]
			if estagio == 1:
				if fracao[0] != 1:
					dividida_fria_ev_acima[corrente-1] = True
				else:
					dividida_fria_ev_acima[corrente-1] = False
				quantidade_fria_ev_acima[corrente-1] = qsj
				fracoes_frias_ev_acima[corrente-1] = fracao[:]
			else:
				if fracao[0] != 1:
					dividida_fria_ev_abaixo[corrente-1] = True
				else:
					dividida_fria_ev_abaixo[corrente-1] = False
				quantidade_fria_ev_abaixo[corrente-1] = qsj
				fracoes_frias_ev_abaixo[corrente-1] = fracao[:]

def inserir_trocador_ev(dlg, vetor, ultima=False):
	cont = 0

	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = vetor[6]

	# CÁLCULO DE TODA A SUPERESTRUTURA
	violou, trocador_violado = calcular_superestrutura(dlg, "adicao", chot, ccold, sbhot, sbcold, sestagio, estagio, ultima)
	if violou and trocador_violado == "termo":
		print("viola termo")
		# return

	remocao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	if Fharr[estagio-1][chot-1][sbhot-1] == 0:
		fracao_quente = 1
	else:
		fracao_quente = Fharr[estagio-1][chot-1][sbhot-1]/100
	if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
		fracao_fria = 1
	else:
		fracao_fria = Fcarr[estagio-1][ccold-1][sbcold-1]/100

	calor_atual_quente_ev[chot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
	calor_atual_frio_ev[ccold-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
	temp_misturador_quente[chot-1] = Thkf[chot-1][estagio-1]
	temp_misturador_frio[ccold-1] = Tckf[ccold-1][estagio-1]

	linha_interface_ev.append([chot,
							ccold,
							sbhot,
							sbcold,
							sestagio,
							estagio,
							Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1],
							Thski[chot-1][sbhot-1][sestagio-1][estagio-1],
							Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1],
							Thskf[chot-1][sbhot-1][sestagio-1][estagio-1],
							Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1],
							fracao_quente,
							fracao_fria])

	for trocador in linha_interface_ev:
		trocador[7] = Thski[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[8] = Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]
		trocador[9] = Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[10] = Tcski[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]

	return linha_interface_ev, violou, trocador_violado

def remover_trocador_ev(dlg, vetor, indice, linha_interface_ev, ultima=False):
	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	adicao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0

	calcular_superestrutura(dlg, "remocao", chot, ccold, sbhot, sbcold, sestagio, estagio, ultima)

	if Fharr[estagio-1][chot-1][sbhot-1] == 0:
		fracao_quente = 1
	if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
		fracao_fria = 1

	calor_atual_quente_ev[chot-1] += vetor[6]
	calor_atual_frio_ev[ccold-1] += vetor[6]

	if calor_atual_quente_ev[chot-1] == Qtotalh01[chot-1]:
		temperatura_atual_quente_ev_mesclada[chot-1] = pinchq
	if calor_atual_frio_ev[ccold-1] == Qtotalc01[ccold-1]:
		temperatura_atual_fria_ev_mesclada[ccold-1] = pinchf

	linha_interface_ev.pop(indice)

def adicionar_utilidade_ev(dlg, corrente, tipo):
	if tipo == "aquecedor":
		utilidades.append([corrente, calor_atual_frio_ev[corrente-1]])
		calor_atual_frio_ev[corrente-1] = 0
		fechar_corrente_ev[corrente-1] = True
		return utilidades
	else:
		utilidades_abaixo.append([corrente, calor_atual_quente_ev[corrente-1]])
		calor_atual_quente_ev[corrente-1] = 0
		fechar_corrente_ev_abaixo[corrente-1] = True
		return utilidades_abaixo

def remover_utilidade_ev(corrente, indice_remover, tipo):
	if tipo == "aquecedor":
		calor_atual_frio_ev[corrente-1] = utilidades[indice_remover][1]
		utilidades.pop(indice_remover)
		fechar_corrente_ev[corrente-1] = False
	else:
		calor_atual_quente_ev[corrente-1] = utilidades_abaixo[indice_remover][1]
		utilidades_abaixo.pop(indice_remover)
		fechar_corrente_ev_abaixo[corrente-1] = False

def remover_todos_ev():
	for i in range(len(linha_interface_ev)-1, -1, -1):
		remover_trocador_ev("oi", linha_interface_ev[i], i, linha_interface_ev)
	for i in range(len(utilidades)-1, -1, -1):
		remover_utilidade_ev(utilidades[i][0], i, "aquecedor")
	for i in range(len(utilidades_abaixo)-1, -1, -1):
		remover_utilidade_ev(utilidades_abaixo[i][0], i, "resf")

def calcular_recomendado_violacao(dlg, trocador):
	if Fharr[trocador[5]-1][trocador[0]-1][trocador[2]-1] == 0:
		fracao_quente = 1
	else:
		fracao_quente = Fharr[trocador[5]-1][trocador[0]-1][trocador[2]-1] / 100
	if Fcarr[trocador[5]-1][trocador[1]-1][trocador[3]-1] == 0:
		fracao_fria = 1
	else:
		fracao_fria = Fcarr[trocador[5]-1][trocador[1]-1][trocador[3]-1] / 100
	cpquente = CPh[trocador[0]-1] * fracao_quente
	cpfrio = CPc[trocador[1]-1] * fracao_fria
	tqin = trocador[7]
	tfout = trocador[8]
	tqout = trocador[9]
	tfin = trocador[10]
	calor = original = trocador[6]
	x = ["None", "None"]
	if tqin - tfout < dTmin or tqout - tfin < dTmin:
		if tqin - tfout >= 0 and tqout - tfin >= 0:
			x[0] = str(0.00)
		while calor > 0:
			calor -= 1
			tqout = -calor / cpquente + tqin
			tfout = calor / cpfrio + tfin
			dtquente = tqin - tfout
			dtfrio = tqout - tfin
			if dtquente > 0 and dtfrio > 0 and x[0] == "None":
				calor1 = original - calor
				x[0] = str('{:.2f}'.format(round(calor1, 2)))
				x[1] = str('{:.2f}'.format(round(calor1, 2)))
			if dtquente > dTmin and dtfrio > dTmin:
				calor2 = original - calor
				x[1] =  str('{:.2f}'.format(round(calor2, 2)))
				break
	dlg.calor_path.clear()
	dlg.calor_path.setPlaceholderText("ΔT > 0: " + x[0] + ", ΔT > ΔTmin: " + x[1])
