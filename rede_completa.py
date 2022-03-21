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
chot = ccold = sbhot = sbcold = qsi = qsj = ccoldutiila = 0
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
calor_sub_sem_utilidade = []
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
temp_misturador = []

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
fechar_corrente = []



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
		temp_misturador.append(0)
		calor_atual_frio_sub.append([])
		calor_sub_sem_utilidade.append([])
		dividida_fria.append(False)
		fechar_corrente.append(False)
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

def receber_pinch_completo(matriz_quente, matriz_fria, nquentes, nfrias, CPquente, CPfrio, deltaTmin, pinch_quente, pinch_frio, matriz_quente_in, matriz_fria_in):
	global Th0, Thf, Tc0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf
	Th0, Thf, Tc0, Tcf = [], [], [], []
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

def verificar_trocador_estagio(estagio, corrente, tipo):
	if tipo == "Q":
		for si in range (ncold): #max de subcorrentes quentes é igual ao numero de correntes frias
			for j in range(ncold):
				for sj in range(nhot): #max de subcorrentes frias é igual ao numero de correntes quentes
					for sk in range (nsk):
						if Q[corrente-1][si][j][sj][sk][estagio-1] != 0:
							return True
	elif tipo == "F":
		for i in range(nhot):
			for si in range (ncold): #max de subcorrentes quentes é igual ao numero de correntes frias
				for sj in range(nhot): #max de subcorrentes frias é igual ao numero de correntes quentes
					for sk in range (nsk):
						if Q[i][si][corrente-1][sj][sk][estagio-1] != 0:
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
										if k1 > (k): #para estágios mais a esqueda do atual da superestrutura, todas as temperaturas recebem a temperatura pós troca
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
											if sk1 >= (sk): #para os subestagios a esquerda ou atual da superestrutura, depende se entra ou sai
												if sk1 > sk: #para os a esquerda, entra recebe após troca
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

def inserir_trocador_completo(dlg, vetor):
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

def remover_trocador_completo(dlg, vetor, indice, linha_interface):
	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	adicao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0

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

def adicionar_utilidade_completo(dlg, corrente):
	if calor_atual_frio[corrente-1] == 0:
		QMessageBox.about(dlg, "Error!", "The heat of this stream has already been supplied")
		return
	utilidades.append([corrente, calor_atual_frio[corrente-1]])
	calor_sub_sem_utilidade[corrente-1] = calor_atual_frio_sub[corrente-1][:]
	if dividida_fria[corrente-1]:
		for sj in range(quantidade_fria[corrente-1]):
			temperatura_atual_fria[corrente-1][sj] = Tcf[corrente-1]
			calor_atual_frio_sub[corrente-1][sj] = 0.0
	temp_misturador[corrente-1] = temperatura_atual_fria_mesclada[corrente-1]
	temperatura_atual_fria_mesclada[corrente-1] = Tcf[corrente-1]
	calor_atual_frio[corrente-1] = 0.0
	fechar_corrente[corrente-1] = True
	return utilidades

def remover_utilidade_completo(corrente, indice_remover, utilidades):
	if dividida_fria[corrente-1]:
		for sj in range(quantidade_fria[corrente-1]):
			calor_atual_frio_sub[corrente-1][sj] = calor_sub_sem_utilidade[corrente-1][sj]
			temperatura_atual_fria[corrente-1][sj] = -calor_atual_frio_sub[corrente-1][sj]/(CPc[corrente-1]*Fcarr[0][corrente-1][sj]/100) + Tcf[corrente-1]
	calor_atual_frio[corrente-1] = utilidades[indice_remover][1]
	temperatura_atual_fria_mesclada[corrente-1] = -calor_atual_frio[corrente-1] / CPc[corrente-1] + Tcf[corrente-1]
	utilidades.pop(indice_remover)
	fechar_corrente[corrente-1] = False
