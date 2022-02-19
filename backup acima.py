from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMessageBox
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
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

linha_interface = []
utilidades = []
estagio = 0
sestagio = 0

complistq = []
complistf = []
cont = opcao = 0
chot = ccold = sbhot = sbcold = qsi = qsj = ccoldutil = 0
tempdif = 0

nstages = 1
nsk = 20

#VARIÁVEIS DE CALOR
Qtotalh01 = []
Qtotalc01 = []
Qtotalh0 = []
Qtotalc0 = []
Qestagioq = []
Qestagiof = []
calor_atual_quente = []
calor_atual_frio = []
calor_atual_quente_sub = []
calor_atual_frio_sub = []
Qtotalestagio = Qtotalestagiof = Qmax = Qtotalhaux = Qtotalcaux = 0


#VARIÁVEIS DE TEMPERATURAS QUENTES
Thski = []
Thki = []
Thskf = []
Thkf = []
Thfinal01 = []
Thfinal01k = []
temperatura_atual_quente = []
temperatura_atual_quente_mesclada = []

#VARIÁVEIS DE TEMPERATURAS FRIAS
Tcski = []
Tcki = []
Tcskf = []
Tckf = []
Tcfinal01 = []
Tcfinal01k = []
temperatura_atual_fria = []
temperatura_atual_fria_mesclada = []

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
dividida_quente = []
dividida_fria = []
quantidade_quente = []
quantidade_fria = []
fracoes_quentes = []
fracoes_frias = []



def preparar_dados_e_rede():
	global Qtotalh01, Qtotalc01, Qtotalh0, Qtotalc0, Qestagioq, Qestagiof
	global Thski, Thki, Thskf, Thkf, Thfinal01, Thfinal01k
	global Tcski, Tcki, Tcskf, Tckf, Tcfinal01, Tcfinal01k
	global Thin, Thout, Tcin, Tcout, Think, Thoutk, Tcink, Tcoutk
	global Fharr, Fcarr, Qarr, Q, Qaux

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
	Fharr = Fharr.tolist()
	Fcarr = np.array ([0])
	Fcarr.resize(nstages, ncold, nhot)
	Fcarr = Fcarr.tolist()
	Qarr = np.array ([0])
	Qarr.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Q[i][si][j][sj][sk][k]
	Q = Qarr.tolist()
	Qaux = Qarr.tolist()
	map(float, Q)
	map(float, Qaux)

	for quente in range(nhot):
		temperatura_atual_quente.append([])
		temperatura_atual_quente_mesclada.append(Thf[quente])
		calor_atual_quente_sub.append([])
		dividida_quente.append(False)
		quantidade_quente.append(1)
		fracoes_quentes.append([])
		for sub in range(ncold):
			calor_atual_quente_sub[quente].append(0)
			temperatura_atual_quente[quente].append(Thf[quente])
	for fria in range(ncold):
		temperatura_atual_fria.append([])
		temperatura_atual_fria_mesclada.append(Tc0[fria])
		calor_atual_frio_sub.append([])
		dividida_fria.append(False)
		quantidade_fria.append(1)
		fracoes_frias.append([])
		for sub in range(nhot):
			calor_atual_frio_sub[fria].append(0)
			temperatura_atual_fria[fria].append(Tc0[fria])

	#CÁLCULOS DOS CALORES TOTAIS
	for i in range (nhot):
		if Th0[i] <= Thf[i]:
			CPh[i] = 0
		Qtotalh01.append(CPh[i] * (Th0[i] - Thf[i]))
		calor_atual_quente.append(CPh[i] * (Th0[i] - Thf[i]))
		calor_atual_quente_sub[i][0] = CPh[i] * (Th0[i] - Thf[i])
	for j in range (ncold):
		if Tcf[j] <= Tc0[j]:
			CPc[j] = 0
		Qtotalc01.append(CPc[j] * (Tcf[j] - Tc0[j]))
		calor_atual_frio.append(CPc[j] * (Tcf[j] - Tc0[j]))
		calor_atual_frio_sub[j][0] = CPc[j] * (Tcf[j] - Tc0[j])

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
					Thski[i][si][sk][k] = Thf[i]
					Thskf[i][si][sk][k] = Thf[i] #Thsk é a temperatura inicial do sub-estágio
		#Este loop iguala as temperaturas iniciais de todos os ESTÁGIOS à temperatura inicial da corrente
		for k in range (nstages):
			Thki[i][k] = Thf[i]
			Thkf[i][k] = Thf[i] #Thk é a temperatura inicial do estágio

	for j in range (ncold):
		for sj in range (nhot):
			for sk in range(nsk-1, -1, -1):
				for k in range(nstages-1, -1, -1):
					Tcski[j][sj][sk][k] = Tc0[j]
					Tcskf[j][sj][sk][k] = Tc0[j]
		for k in range (nstages-1, -1, -1):
			Tcki[j][k] = Tc0[j]
			Tckf[j][k] = Tc0[j]

def receber_pinch(matriz_quente, matriz_fria, nquentes, nfrias, CPquente, CPfrio, deltaTmin, pinch_quente, pinch_frio, matriz_quente_in, matriz_fria_in):
	global Th0, Thf, Tc0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf
	Th0, Thf, Tc0, Tcf = [], [], [], []
	CPh.clear()
	CPc.clear()
	for corrente in range(nquentes):
		Th0.append(matriz_quente[corrente])
		Thf.append(matriz_quente_in[corrente])
		CPh.append(CPquente[corrente])
	for corrente in range(nfrias):
		Tcf.append(matriz_fria[corrente])
		Tc0.append(matriz_fria_in[corrente])
		CPc.append(CPfrio[corrente])
	pinchq = pinch_quente
	pinchf = pinch_frio
	nhot = nquentes
	ncold = nfrias
	dTmin = deltaTmin
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

def verificar_trocador_estagio(estagio):
	for i in range (nhot):
		for si in range (ncold): #max de subcorrentes quentes é igual ao numero de correntes frias
			for j in range(ncold):
				for sj in range(nhot): #max de subcorrentes frias é igual ao numero de correntes quentes
					for sk in range (nsk):
						if Q[i][si][j][sj][sk][estagio-1] != 0:
							return True

def calcular_superestrutura(dlg, acao, chot, ccold, sbhot, sbcold, sestagio, estagio):
	for i in range (nhot):
		for si in range (ncold):
			for sk in range (nsk):
				for k in range (nstages):
					Thski[i][si][sk][k] = Thf[i]
					Thskf[i][si][sk][k] = Thf[i]

		for k in range (nstages):
			Thki[i][k] = Thf[i]
			Thkf[i][k] = Thf[i]

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

	#CÁLCULO DE TODA A SUPERESTRUTURA
	for k in range (nstages-1, -1, -1):
		for sk in range (nsk-1, -1, -1):
			for i in range (nhot-1, -1, -1):
				for si in range (ncold-1, -1, -1):
					for j in range(ncold-1, -1, -1):
						for sj in range(nhot-1, -1, -1):

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
								Thout[i][si][j][sj][sk][k] = Thin[i][si][j][sj][sk][k] + (Q[i][si][j][sj][sk][k]/(CPh[i]*Fharr[k][i][si]/100))

								Think[i][si][j][sj][sk][k] = Thki[i][k]
								Thoutk[i][si][j][sj][sk][k] = Think[i][si][j][sj][sk][k] + (Qestagioq[i][k]/CPh[i])

								Tcin[i][si][j][sj][sk][k] = Tcski[j][sj][sk][k]
								Tcout[i][si][j][sj][sk][k] = Tcin[i][si][j][sj][sk][k] + (Q[i][si][j][sj][sk][k]/(CPc[j]*Fcarr[k][j][sj]/100))

								Tcink[i][si][j][sj][sk][k] = Tcki[j][k]
								Tcoutk[i][si][j][sj][sk][k] = Tcink[i][si][j][sj][sk][k] + (Qestagiof[j][k]/CPc[j])

								tempdif = Thout[i][si][j][sj][sk][k] - Tcout[i][si][j][sj][sk][k]
								tempdif_terminal_frio = Thin[i][si][j][sj][sk][k] - Tcin[i][si][j][sj][sk][k]

								if tempdif < 0 or tempdif_terminal_frio < 0:
									QMessageBox.about(dlg, "Error!", "Thermodynamics Violation. The temperature of the cold stream will be greater thant the temperature of the hot stream")
									Q[i][si][j][sj][sk][k] = 0
									return True, "termo"
								else:
									if not (tempdif >= dTmin and tempdif_terminal_frio >= dTmin):
										violou = True
										trocador_violado = [i+1, j+1, si+1, sj+1, sk+1, k+1, tempdif, tempdif_terminal_frio]

									if dividida_quente[i]:
										temperatura_atual_quente[i][si] = Thout[i][si][j][sj][sk][k]
									if dividida_fria[j]:
										temperatura_atual_fria[j][sj] = Tcout[i][si][j][sj][sk][k]
									temperatura_atual_quente_mesclada[i] = Thoutk[i][si][j][sj][sk][k]
									temperatura_atual_fria_mesclada[j] = Tcoutk[i][si][j][sj][sk][k]

								Thfinal01[i][si] = Thout[i][si][j][sj][sk][k]
								Tcfinal01[j][sj] = Tcout[i][si][j][sj][sk][k]
								Thfinal01k[i][k] = Thoutk[i][si][j][sj][sk][k]
								Tcfinal01k[j][k] = Tcoutk[i][si][j][sj][sk][k]

								#Temperatura de estágios e sub-estágios
								for k1 in range(nstages):
									for sk1 in range(nsk):
										if k1 < (k): #para estágios mais a esqueda do atual da superestrutura, todas as temperaturas recebem a temperatura pós troca
											#entrada
											Tcki[j][k1] = Tcfinal01k[j][k]
											Thki[i][k1] = Thfinal01k[i][k]

											#saida
											Tckf[j][k1] = Tcfinal01k[j][k]
											Thkf[i][k1] = Thfinal01k[i][k]

											for sub_fria in range(nhot):
												Tcski[j][sub_fria][sk1][k1] = Tcfinal01k[j][k]
												Tcskf[j][sub_fria][sk1][k1] = Tcfinal01k[j][k]
											for sub_quente in range(ncold):
												Thski[i][sub_quente][sk1][k1] = Thfinal01k[i][k]
												Thskf[i][sub_quente][sk1][k1] = Thfinal01k[i][k]

										if k1 == (k): #para o estágio atual da superestrutura, depende de qual subestagio
											if sk1 <= (sk): #para os subestagios a esquerda ou atual da superestrutura, depende se entra ou sai
												if sk1 < sk: #para os a esquerda, entra recebe após troca
													Tcski[j][sj][sk1][k1] = Tcfinal01[j][sj]
													Thski[i][si][sk1][k1] = Thfinal01[i][si]
												Tcskf[j][sj][sk1][k1] = Tcfinal01[j][sj] #atual e a esquerda, final recebe após troca
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

def divisao_de_correntes(divtype, estagio, corrente, quantidade, fracao):
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
					fracoes_quentes[corrente-1].append(fracao[si])
				for si in range(ncold-1, -1, -1):
					if Fharr[estagio-1][corrente-1][si] != 0:
						Qtotalh0[corrente-1][si][estagio-1] = Qtotalh0[corrente-1][0][estagio-1]*(Fharr[estagio-1][corrente-1][si]/100)
						calor_atual_quente_sub[corrente-1][si] = Qtotalh0[corrente-1][si][estagio-1]
			dividida_quente[corrente-1] = True
			quantidade_quente[corrente-1] = qsi

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
					fracoes_frias[corrente-1].append(fracao[sj])
				for sj in range(nhot-1, -1, -1):
					if Fcarr[estagio-1][corrente-1][sj] != 0:
						Qtotalc0[corrente-1][sj][estagio-1] = Qtotalc0[corrente-1][0][estagio-1]*(Fcarr[estagio-1][corrente-1][sj]/100)
						calor_atual_frio_sub[corrente-1][sj] = Qtotalc0[corrente-1][sj][estagio-1]
			dividida_fria[corrente-1] = True
			quantidade_fria[corrente-1] = qsj

def ler_dados(dlg):
	i = int(dlg.comboBox_2.currentText())
	j = int(dlg.comboBox_5.currentText())
	si = int(dlg.comboBox_50.currentText())
	sj = int(dlg.comboBox_51.currentText())
	k = int(dlg.comboBox_8.currentText())
	sk = int(dlg.comboBox_7.currentText())

	if ((Qtotalh0[i-1][si-1][k-1]) > (Qtotalc0[j-1][sj-1][k-1])):
		Qmax = Qtotalc0[j-1][sj-1][k-1]
	else:
		Qmax = Qtotalh0[i-1][si-1][k-1]
	if dlg.radioButton_4.isChecked():   #MAXIMUM HEAT
		q = Qmax
	elif dlg.radioButton.isChecked():     #HEATLOAD
		q = float(dlg.lineEdit_5.text()) #botão HEATLOAD

	return [i, j, si, sj, sk, k, q]

def inserir_trocador(dlg, vetor):
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
	calor_frio = 0
	calor_quente = 0
	for si in range(ncold):
		calor_quente += Qtotalh0[chot-1][si][estagio-1]
	for sj in range(nhot):
		calor_frio += Qtotalc0[ccold-1][sj][estagio-1]

	if calor_quente > calor_frio:
		Qmax = calor_frio
	else:
		Qmax = calor_quente

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

	# CÁLCULO DE TODA A SUPERESTRUTURA
	violou, trocador_violado = calcular_superestrutura(dlg, "adicao", chot, ccold, sbhot, sbcold, sestagio, estagio)
	if violou and trocador_violado == "termo":
		return

	remocao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	if Fharr[estagio-1][chot-1][sbhot-1] == 0:
		fracao_quente = 1
	else:
		fracao_quente = Fharr[estagio-1][chot-1][sbhot-1]/100
	if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
		fracao_fria = 1
	else:
		fracao_fria = Fcarr[estagio-1][ccold-1][sbcold-1]/100

	calor_atual_quente[chot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
	calor_atual_frio[ccold-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

	if dividida_quente[chot-1]:
		calor_atual_quente_sub[chot-1][sbhot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
	if dividida_fria[ccold-1]:
		calor_atual_frio_sub[ccold-1][sbcold-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

	linha_interface.append([chot,
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

	for trocador in linha_interface:
		trocador[7] = Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[8] = Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]

	return linha_interface, violou, trocador_violado

def remover_trocador(dlg, vetor, indice, linha_interface):
	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	adicao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0

	#CÁLCULO DA SUPERESTRUTURA
	calcular_superestrutura(dlg, "remocao", chot, ccold, sbhot, sbcold, sestagio, estagio)

	for k in range (nstages):
		for sk in range (nsk):
			for i in range (nhot):
				for si in range (ncold):
					for j in range(ncold):
						for sj in range(nhot):
							Qaux[i][si][j][sj][sk][k] = 0

	if Fharr[estagio-1][chot-1][sbhot-1] == 0:
		fracao_quente = 1
	if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
		fracao_fria = 1

	calor_atual_quente[chot-1] += vetor[6]
	calor_atual_frio[ccold-1] += vetor[6]
	if dividida_quente[chot-1]:
		calor_atual_quente_sub[chot-1][sbhot-1] += vetor[6]
	if dividida_fria[ccold-1]:
		calor_atual_frio_sub[ccold-1][sbcold-1] += vetor[6]

	if calor_atual_quente[chot-1] == Qtotalh01[chot-1]:
		temperatura_atual_quente_mesclada[chot-1] = pinchq
	if calor_atual_frio[ccold-1] == Qtotalc01[ccold-1]:
		temperatura_atual_fria_mesclada[ccold-1] = pinchf

	if dividida_quente[chot-1]:
		if calor_atual_quente_sub[chot-1][sbhot-1] == Qtotalh01[chot-1] * Fharr[estagio-1][chot-1][sbhot-1]/100:
			temperatura_atual_quente[chot-1][sbhot-1] = pinchq
	if dividida_fria[ccold-1]:
		if calor_atual_frio_sub[ccold-1][sbcold-1] == Qtotalc01[ccold-1] * Fcarr[estagio-1][ccold-1][sbcold-1]/100:
			temperatura_atual_fria[ccold-1][sbcold-1] = pinchf

	linha_interface.pop(indice)

def atualizar_matriz(matriz):
	for trocador in matriz:
		trocador[7] = Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[8] = Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]

def adicionar_utilidade(dlg, corrente):
	ccoldutil = corrente
	q = Qtotalc0[ccoldutil-1][0][0]
	for sj in range(nhot):
		for k in range(nstages):
			if q < Qtotalc0[ccoldutil-1][sj][k]:
				q = Qtotalc0[ccoldutil-1][sj][k]
			Qtotalc0[ccoldutil-1][sj][k] = 0
	if q == 0:
		QMessageBox.about(dlg, "Error!", "The heat of this stream has already been supplied")
		return
	temperatura_atual_fria[ccoldutil-1] = Tcf[ccoldutil-1]
	calor_atual_frio[ccoldutil-1] = 0.0
	utilidades.append([ccoldutil, q])
	return utilidades

def remover_utilidade(corrente, indice_remover, utilidades):
	Qtotalc0[corrente-1][0][0] = utilidades[indice_remover][1]
	calor_atual_frio[corrente-1] = Qtotalc0[corrente-1][0][0]
	temperatura_atual_fria[corrente-1] = -calor_atual_frio[corrente-1] / CPc[corrente-1] + Tcf[corrente-1]
	utilidades.pop(indice_remover)

def caixa_de_temperatura(dlg):
	chot = int(float(dlg.TempLoadAbove.comboBox.currentText()))
	ccold = int(float(dlg.TempLoadAbove.comboBox_2.currentText()))
	sbhot = int(dlg.TempLoadAbove.comboBox_3.currentText())
	sbcold = int(dlg.TempLoadAbove.comboBox_4.currentText())
	estagio = int(dlg.TempLoadAbove.comboBox_5.currentText())
	sestagio = int(dlg.TempLoadAbove.comboBox_6.currentText())

	if dlg.TempLoadAbove.radioButton_2.isChecked():
		inlethot = float(dlg.TempLoadAbove.lineEdit_2.text())
		q = CPh[chot-1] * (inlethot - Thski[chot-1][sbhot-1][sestagio-1][estagio-1])
	if dlg.TempLoadAbove.radioButton.isChecked():
		outletcold = float(dlg.TempLoadAbove.lineEdit.text())
		q = CPc[ccold-1] * (outletcold - Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1])

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

	dlg.lineEdit_5.setText(str(q))
	dlg.radioButton.setChecked(True)
	dlg.comboBox_2.setCurrentText(str(dlg.TempLoadAbove.comboBox.currentText()))  #hot strem
	dlg.comboBox_5.setCurrentText(str(dlg.TempLoadAbove.comboBox_2.currentText()))  #cold stream
	dlg.comboBox_7.setCurrentText(str(dlg.TempLoadAbove.comboBox_6.currentText())) #sk
	dlg.comboBox_8.setCurrentText(str(dlg.TempLoadAbove.comboBox_5.currentText())) #k
	dlg.comboBox_50.setCurrentText(str(dlg.TempLoadAbove.comboBox_3.currentText())) #si
	dlg.comboBox_51.setCurrentText(str(dlg.TempLoadAbove.comboBox_4.currentText())) #sj
	dlg.TempLoadAbove.close()

def testar_correntes(dlg, primeira=False):
	nhotc = 0
	ncoldc = 0
	somaCPh = 0
	somaCPc = 0

	for quente in range(nhot):
		if Thf[quente] == pinchq: #se tocar o pinch
			somaCPh += CPh[quente]
			if CPh[quente] != 0:
				if dividida_quente[quente]:
					nhotc += quantidade_quente[quente]
				else:
					nhotc += 1
					# if quente == 0:
					# 	nhotc += 1

	for fria in range(ncold):
		if Tc0[fria] == pinchf: #se tocar o pinch
			somaCPc += CPc[fria]
			if CPc[fria] != 0:
				if dividida_fria[fria]:
					ncoldc += quantidade_fria[fria]
				else:
					ncoldc += 1

	# print("nhot toca pinch acima: ", nhotc)
	# print("ncold toca pinch acima: ", ncoldc)
	# print("soma cpquente acima: ", somaCPh)
	# print("soma cpfrio acima: ", somaCPc)

	if somaCPh > somaCPc:
		dlg.label_24.setStyleSheet("QLabel {color: red}")
	else:
		dlg.label_24.setStyleSheet("QLabel {color: green}")

	if nhotc > ncoldc:
		dlg.label_23.setStyleSheet("QLabel {color: red}")
		if not primeira:
			QMessageBox.about(dlg,"Be Carreful","With this Split, you went against the Pinch Recomendations")
	else:
		dlg.label_23.setStyleSheet("QLabel {color: green}")

	if somaCPh <= somaCPc and ncoldc >= nhotc:
		dlg.label_26.setText("Respected")
		dlg.label_26.setStyleSheet("QLabel {color: green}")
	else:
		dlg.label_26.setText("Not Respected")
		dlg.label_26.setStyleSheet("QLabel {color: red}")


	# return respeitando