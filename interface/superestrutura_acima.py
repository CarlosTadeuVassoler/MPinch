from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMessageBox
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import threading

nstages = 1
subestagios = []
quentes_usadas = []
frias_usadas = []
subq_usadas = []
subf_usadas = []
linha_interface = []
utilidades = []

#VARIÁVEIS DE CALOR
Qtotalh01 = []
Qtotalc01 = []
calor_atual_quente = []
calor_atual_frio = []
calor_atual_quente_sub = []
calor_atual_frio_sub = []
calor_sub_sem_utilidade = []

#VARIÁVEIS DE TEMPERATURAS QUENTES
temperatura_atual_quente = []
temperatura_atual_quente_mesclada = []

#VARIÁVEIS DE TEMPERATURAS FRIAS
temperatura_atual_fria = []
temperatura_atual_fria_mesclada = []
temp_misturador = []

#VARIÁVEIS DE DIVISÃO
dividida_quente = []
dividida_fria = []
quantidade_quente = []
quantidade_fria = []
fracoes_quentes = []
fracoes_frias = []
fechar_corrente = []



def declarar_np(*args):
	x = np.array([0.0])
	x.resize(args)
	return x

def preparar_dados_e_rede(sk):
	global Qtotalh01, Qtotalc01, Qtotalh0, Qtotalc0
	global Thski, Thki, Thskf, Thkf, Tcski, Tcki, Tcskf, Tckf
	global Fharr, Fcarr, Q

	Thski = declarar_np(nhot, ncold, nsk, nstages)
	Thskf = declarar_np(nhot, ncold, nsk, nstages)
	Tcski = declarar_np(ncold, nhot, nsk, nstages)
	Tcskf = declarar_np(ncold, nhot, nsk, nstages)
	Q = declarar_np(nhot, ncold, ncold, nhot, nsk, nstages)

	if sk == 4:
		linha_interface.clear()
		utilidades.clear()

	else:
		Qtotalh0 = declarar_np(nhot, ncold, nstages)
		Qtotalc0 = declarar_np(ncold, nhot, nstages)
		Thki = declarar_np(nhot, nstages)
		Thkf = declarar_np(nhot, nstages)
		Tckf = declarar_np(ncold, nstages)
		Tcki = declarar_np(ncold, nstages)
		Fharr = declarar_np(nstages, nhot, ncold)
		Fcarr = declarar_np(nstages, ncold, nhot)

		for quente in range(nhot):
			temperatura_atual_quente.append([])
			temperatura_atual_quente_mesclada.append(Thf[quente])
			calor_atual_quente_sub.append([])
			dividida_quente.append(False)
			quantidade_quente.append(1)
			fracoes_quentes.append([])
			subq_usadas.append([])
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
			fechar_corrente.append(False)
			temp_misturador.append(0)
			calor_sub_sem_utilidade.append([])
			subf_usadas.append([])
			for sub in range(nhot):
				calor_atual_frio_sub[fria].append(0)
				temperatura_atual_fria[fria].append(Tc0[fria])

		#calores totais
		for i in range(nhot):
			if Th0[i] <= Thf[i]:
				CPh[i] = 0
			Qtotalh01.append(CPh[i] * (Th0[i] - Thf[i]))
			calor_atual_quente.append(CPh[i] * (Th0[i] - Thf[i]))
			calor_atual_quente_sub[i][0] = CPh[i] * (Th0[i] - Thf[i])
		for j in range(ncold):
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

	#prepara rede
	for i in range(nhot):
		for si in range(ncold):
			for sk in range(nsk):
				for k in range(nstages):
					Thski[i][si][sk][k] = Thf[i]
					Thskf[i][si][sk][k] = Thf[i]
		for k in range(nstages):
			Thki[i][k] = Thf[i]
			Thkf[i][k] = Thf[i]

	for j in range(ncold):
		for sj in range(nhot):
			for sk in range(nsk-1, -1, -1):
				for k in range(nstages-1, -1, -1):
					Tcski[j][sj][sk][k] = Tc0[j]
					Tcskf[j][sj][sk][k] = Tc0[j]
		for k in range(nstages-1, -1, -1):
			Tcki[j][k] = Tc0[j]
			Tckf[j][k] = Tc0[j]

def receber_pinch(matriz_quente, matriz_fria, nquentes, nfrias, CPquente, CPfrio, deltaTmin, pinch_quente, pinch_frio, matriz_quente_in, matriz_fria_in, sk=2):
	global Th0, Thf, Tc0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, nsk
	Th0, Thf, Tc0, Tcf, CPh, CPc = [], [], [], [], [], []
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
	nsk = sk*max(nhot, ncold)
	preparar_dados_e_rede(sk)

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
		for si in range(ncold): #max de subcorrentes quentes é igual ao numero de correntes frias
			for j in range(ncold):
				for sj in range(nhot): #max de subcorrentes frias é igual ao numero de correntes quentes
					for sk in range(nsk):
						if Q[corrente-1][si][j][sj][sk][estagio-1] != 0:
							return True
	elif tipo == "F":
		for i in range(nhot):
			for si in range(ncold): #max de subcorrentes quentes é igual ao numero de correntes frias
				for sj in range(nhot): #max de subcorrentes frias é igual ao numero de correntes quentes
					for sk in range(nsk):
						if Q[i][si][corrente-1][sj][sk][estagio-1] != 0:
							return True

def calcular_superestrutura(dlg, acao, chot, ccold, sbhot, sbcold, sestagio, estagio):
	for si in range(ncold):
		for sk in range(nsk):
			for k in range(nstages):
				Thski[chot-1][si][sk][k] = Thf[chot-1]
				Thskf[chot-1][si][sk][k] = Thf[chot-1]

	for k in range(nstages):
		Thki[chot-1][k] = Thf[chot-1]
		Thkf[chot-1][k] = Thf[chot-1]

	for sj in range(nhot):
		for sk in range(nsk-1, -1, -1):
			for k in range(nstages-1, -1, -1):
				Tcski[ccold-1][sj][sk][k] = Tc0[ccold-1]
				Tcskf[ccold-1][sj][sk][k] = Tc0[ccold-1]
	for k in range(nstages-1, -1, -1):
		Tcki[ccold-1][k] = Tc0[ccold-1]
		Tckf[ccold-1][k] = Tc0[ccold-1]

	violou = False
	trocador_violado = False

	#CÁLCULO DE TODA A SUPERESTRUTURA quente
	for k in range(nstages):
		for sk in sorted(subestagios):
			for si in sorted(subq_usadas[chot-1]):
				for j in sorted(frias_usadas):
					for sj in sorted(subf_usadas[j]):

						if Q[chot-1][si][j][sj][sk][k] != 0:

							#CALORES DOS ESTÁGIOS
							Qestagioq = 0
							for si1 in range(ncold):
								for j1 in range(ncold):
									for sj1 in range(nhot):
										for sk1 in range(nsk):
											Qestagioq += Q[chot-1][si1][j1][sj1][sk1][k]

							if Fharr[k][chot-1][si] == 0:
								Fharr[k][chot-1][si] = 100

							Thin = Thski[chot-1][si][sk][k]
							Thout = Thin + (Q[chot-1][si][j][sj][sk][k]/(CPh[chot-1]*Fharr[k][chot-1][si]/100))

							Think = Thki[chot-1][k]
							Thoutk = Think + (Qestagioq/CPh[chot-1])

							if dividida_quente[chot-1]:
								temperatura_atual_quente[chot-1][si] = Thout
							temperatura_atual_quente_mesclada[chot-1] = Thoutk

							#Temperatura de estágios e sub-estágios
							for k1 in range(nstages):
								for sk1 in sorted(subestagios):
									if k1 > (k):
										Thki[chot-1][k1] = Thoutk
										Thkf[chot-1][k1] = Thoutk

										for sub_quente in range(ncold):
											Thski[chot-1][sub_quente][sk1][k1] = Thoutk
											Thskf[chot-1][sub_quente][sk1][k1] = Thoutk

									if k1 == (k):
										if sk1 >= (sk):
											if sk1 > sk:
												Thski[chot-1][si][sk1][k1] = Thout
											Thskf[chot-1][si][sk1][k1] = Thout
										Thkf[chot-1][k1] = Thoutk

							if Fharr[k][chot-1][si] == 100:
								Fharr[k][chot-1][si] = 0

	for k in range(nstages):
		for sk in sorted(subestagios):
			for i in sorted(quentes_usadas):
				for si in sorted(subq_usadas[i]):
					for sj in sorted(subf_usadas[ccold-1]):

						if Q[i][si][ccold-1][sj][sk][k] != 0:

							Qestagiof = 0
							for sj1 in range(nhot):
								for i1 in range(nhot):
									for si1 in range(ncold):
										for sk1 in range(nsk):
											Qestagiof += Q[i1][si1][ccold-1][sj1][sk1][k]

							if Fcarr[k][ccold-1][sj] == 0:
								Fcarr[k][ccold-1][sj] = 100

							Tcin = Tcski[ccold-1][sj][sk][k]
							Tcout = Tcin + (Q[i][si][ccold-1][sj][sk][k]/(CPc[ccold-1]*Fcarr[k][ccold-1][sj]/100))

							Tcink = Tcki[ccold-1][k]
							Tcoutk = Tcink + (Qestagiof/CPc[ccold-1])

							# tempdif = Thout - Tcout
							# tempdif_terminal_frio = Thin - Tcin
							#
							# if tempdif < 0 or tempdif_terminal_frio < 0:
							# 	if acao:
							# 		QMessageBox.about(dlg, "Error!", "Thermodynamics Violation. The temperature of the cold stream will be greater thant the temperature of the hot stream")
							# 		Q[i][si][ccold-1][sj][sk][k] = 0
							# 		return True, "termo"
							# 	else:
							# 		QMessageBox.about(dlg, "Warning!", "Removing this Heat Exchanger resulted in a Thermodynamics Violation (E{})".format(sk+1))
							if True:
								if dividida_fria[ccold-1]:
									temperatura_atual_fria[ccold-1][sj] = Tcout
								temperatura_atual_fria_mesclada[ccold-1] = Tcoutk

							#Temperatura de estágios e sub-estágios
							for k1 in range(nstages):
								for sk1 in sorted(subestagios):
									if k1 > (k):
										Tcki[ccold-1][k1] = Tcoutk
										Tckf[ccold-1][k1] = Tcoutk

										for sub_fria in range(nhot):
											Tcski[ccold-1][sub_fria][sk1][k1] = Tcoutk
											Tcskf[ccold-1][sub_fria][sk1][k1] = Tcoutk

									if k1 == (k):
										if sk1 >= (sk):
											if sk1 > sk:
												Tcski[ccold-1][sj][sk1][k1] = Tcout
											Tcskf[ccold-1][sj][sk1][k1] = Tcout
										Tckf[ccold-1][k1] = Tcoutk

							if Fcarr[k][ccold-1][sj] == 100:
								Fcarr[k][ccold-1][sj] = 0

	return violou, trocador_violado

def divisao_de_correntes(divtype, estagio, corrente, quantidade, fracao):
	qsi = quantidade
	qsj = quantidade
	if divtype.upper() == 'Q':
		#desfaz divisoes anteriores da corrente no estagio
		for si in range(1, ncold):
			Qtotalh0[corrente-1][0][estagio-1] += Qtotalh0[corrente-1][si][estagio-1]
		for si in range(ncold-1, qsi-1, -1):#ex: antes 3 divisoes porem agora 2, zera a 3
			Fharr[estagio-1][corrente-1][si] = 0
			Qtotalh0[corrente-1][si][estagio-1] = 0
		#faz a nova divisao
		if qsi <= ncold:
			fracoes_quentes[corrente-1] = []
			for si in range(qsi):
				Fharr[estagio-1][corrente-1][si] = 100 * fracao[si]
				fracoes_quentes[corrente-1].append(fracao[si])
			for si in range(ncold-1, -1, -1):
				if Fharr[estagio-1][corrente-1][si] != 0:
					Qtotalh0[corrente-1][si][estagio-1] = Qtotalh0[corrente-1][0][estagio-1]*(Fharr[estagio-1][corrente-1][si]/100)
					calor_atual_quente_sub[corrente-1][si] = Qtotalh0[corrente-1][si][estagio-1]
		if fracoes_quentes[corrente-1][0] != 1:
			dividida_quente[corrente-1] = True
		else:
			dividida_quente[corrente-1] = False
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
			fracoes_frias[corrente-1] = []
			for sj in range(qsj):
				Fcarr[estagio-1][corrente-1][sj] = 100 * fracao[sj]
				fracoes_frias[corrente-1].append(fracao[sj])
			for sj in range(nhot-1, -1, -1):
				if Fcarr[estagio-1][corrente-1][sj] != 0:
					Qtotalc0[corrente-1][sj][estagio-1] = Qtotalc0[corrente-1][0][estagio-1]*(Fcarr[estagio-1][corrente-1][sj]/100)
					calor_atual_frio_sub[corrente-1][sj] = Qtotalc0[corrente-1][sj][estagio-1]
		if fracoes_frias[corrente-1][0] != 1:
			dividida_fria[corrente-1] = True
		else:
			dividida_fria[corrente-1] = False
		quantidade_fria[corrente-1] = qsj

def ler_dados(dlg, subestagio_trocador):
	i = int(dlg.comboBox_2.currentIndex()+1)
	j = int(dlg.comboBox_5.currentIndex()+1)
	si = int(dlg.comboBox_50.currentText())
	sj = int(dlg.comboBox_51.currentText())
	k = 1
	sk = subestagio_trocador

	if ((Qtotalh0[i-1][si-1][k-1]) > (Qtotalc0[j-1][sj-1][k-1])):
		Qmax = Qtotalc0[j-1][sj-1][k-1]
	else:
		Qmax = Qtotalh0[i-1][si-1][k-1]
	if dlg.radioButton_4.isChecked():   #MAXIMUM HEAT
		q = Qmax
	elif dlg.radioButton.isChecked():     #HEATLOAD
		q = float(dlg.lineEdit_5.text().replace(",", ".")) #botão HEATLOAD

	return [i, j, si, sj, sk, k, q]

def inserir_trocador(dlg, vetor, verificar_termo=True, ignora=False):
	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] != 0:
		QMessageBox.about(dlg,"Error!","There is already a heat exchanger in this position!")
		return linha_interface, False

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = vetor[6]

	if ((Qtotalh0[chot-1][sbhot-1][estagio-1]) > (Qtotalc0[ccold-1][sbcold-1][estagio-1])):
		Qmax = Qtotalc0[ccold-1][sbcold-1][estagio-1]
	else:
		Qmax = Qtotalh0[chot-1][sbhot-1][estagio-1]

	if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] > Qmax:
		if not ignora:
			QMessageBox.about(dlg,"Error!","The inputed heat is greater than the available heat.")
			Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0
			return linha_interface, False
		else:
			QMessageBox.about(dlg,"Carreful!","The inputed heat is greater than the available heat. \nYou will use more than the utility duty.")

	elif Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] < 0:
		QMessageBox.about(dlg,"Error!","It is not possible to change a negative amount of heat.")
		Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0
		return linha_interface, False

	elif Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] == 0:
		QMessageBox.about(dlg,"Error!","The inputed heat must be greater than 0.")
		return linha_interface, False

	if chot-1 not in quentes_usadas:
		quentes_usadas.append(chot-1)
	if ccold-1 not in frias_usadas:
		frias_usadas.append(ccold-1)
	if sbhot-1 not in subq_usadas[chot-1]:
		subq_usadas[chot-1].append(sbhot-1)
	if sbcold-1 not in subf_usadas[ccold-1]:
		subf_usadas[ccold-1].append(sbcold-1)
	if sestagio-1 not in subestagios:
		subestagios.append(sestagio-1)

	violou, trocador_violado = calcular_superestrutura(dlg, verificar_termo, chot, ccold, sbhot, sbcold, sestagio, estagio)
	if violou and trocador_violado == "termo":
		return linha_interface, False

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
	calor_atual_quente_sub[chot-1][sbhot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
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
							Thski[chot-1][sbhot-1][sestagio-1][estagio-1],
							Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1],
							fracao_quente,
							fracao_fria])

	for trocador in linha_interface:
		trocador[7] = Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[8] = Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]

	return linha_interface, True

def remover_trocador(dlg, vetor, indice, linha_interface):
	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	adicao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0

	if sestagio == 1:
		subestagios.clear()
		quentes_usadas.clear()
		frias_usadas.clear()
		for i in range(len(subq_usadas)):
			subq_usadas[i].clear()
		for j in range(len(subf_usadas)):
			subf_usadas[j].clear()

	calcular_superestrutura(dlg, "remocao", chot, ccold, sbhot, sbcold, sestagio, estagio)

	if Fharr[estagio-1][chot-1][sbhot-1] == 0:
		fracao_quente = 1
	if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
		fracao_fria = 1

	calor_atual_quente[chot-1] += vetor[6]
	calor_atual_frio[ccold-1] += vetor[6]
	calor_atual_quente_sub[chot-1][sbhot-1] += vetor[6]
	calor_atual_frio_sub[ccold-1][sbcold-1] += vetor[6]

	if calor_atual_quente[chot-1] == Qtotalh01[chot-1]:
		temperatura_atual_quente_mesclada[chot-1] = pinchq
	if calor_atual_frio[ccold-1] == Qtotalc01[ccold-1]:
		temperatura_atual_fria_mesclada[ccold-1] = pinchf

	if calor_atual_quente_sub[chot-1][sbhot-1] == Qtotalh01[chot-1] * Fharr[estagio-1][chot-1][sbhot-1]/100:
		temperatura_atual_quente[chot-1][sbhot-1] = pinchq
	if calor_atual_frio_sub[ccold-1][sbcold-1] == Qtotalc01[ccold-1] * Fcarr[estagio-1][ccold-1][sbcold-1]/100:
		temperatura_atual_fria[ccold-1][sbcold-1] = pinchf

	linha_interface.pop(indice)

def atualizar_matriz(matriz):
	for trocador in matriz:
		trocador[7] = Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[8] = Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]

def adicionar_utilidade(dlg, corrente):
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

def remover_utilidade(corrente, indice_remover, utilidades):
	if dividida_fria[corrente-1]:
		for sj in range(quantidade_fria[corrente-1]):
			calor_atual_frio_sub[corrente-1][sj] = calor_sub_sem_utilidade[corrente-1][sj]
			temperatura_atual_fria[corrente-1][sj] = -calor_atual_frio_sub[corrente-1][sj]/(CPc[corrente-1]*Fcarr[0][corrente-1][sj]/100) + Tcf[corrente-1]
	calor_atual_frio[corrente-1] = utilidades[indice_remover][1]
	temperatura_atual_fria_mesclada[corrente-1] = -calor_atual_frio[corrente-1] / CPc[corrente-1] + Tcf[corrente-1]
	utilidades.pop(indice_remover)
	fechar_corrente[corrente-1] = False

def caixa_de_temperatura(dlg, sk):
	chot = int(float(dlg.TempLoadAbove.comboBox.currentText()))
	ccold = int(float(dlg.TempLoadAbove.comboBox_2.currentText()))
	sbhot = int(dlg.TempLoadAbove.comboBox_3.currentText())
	sbcold = int(dlg.TempLoadAbove.comboBox_4.currentText())
	estagio = 1
	sestagio = sk + 1

	if dlg.TempLoadAbove.radioButton_2.isChecked():
		inlethot = float(dlg.TempLoadAbove.lineEdit_2.text().replace(",", "."))
		q = round(CPh[chot-1] * (inlethot - Thski[chot-1][sbhot-1][sestagio-1][estagio-1]), 2)
	if dlg.TempLoadAbove.radioButton.isChecked():
		outletcold = float(dlg.TempLoadAbove.lineEdit.text().replace(",", "."))
		q = round(CPc[ccold-1] * (outletcold - Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1]), 2)

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
	dlg.comboBox_50.setCurrentText(str(dlg.TempLoadAbove.comboBox_3.currentText())) #si
	dlg.comboBox_51.setCurrentText(str(dlg.TempLoadAbove.comboBox_4.currentText())) #sj
	dlg.TempLoadAbove.close()

def testar_correntes(dlg, primeira=False):
	nhotc = 0
	ncoldc = 0
	somaCPh = 0
	somaCPc = 0

	for quente in range(nhot):
		if Thf[quente] == pinchq:
			somaCPh += CPh[quente]
			if CPh[quente] != 0:
				if dividida_quente[quente]:
					nhotc += quantidade_quente[quente]
				else:
					nhotc += 1

	for fria in range(ncold):
		if Tc0[fria] == pinchf:
			somaCPc += CPc[fria]
			if CPc[fria] != 0:
				if dividida_fria[fria]:
					ncoldc += quantidade_fria[fria]
				else:
					ncoldc += 1

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

def remover_todos_acima():
	for i in range(len(linha_interface)-1, -1, -1):
		remover_trocador("oi", linha_interface[i], i, linha_interface)
	for i in range(len(utilidades)-1, -1, -1):
		remover_utilidade(utilidades[i][0], i, utilidades)
