from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMessageBox
from PyQt5 import QtWidgets , uic, QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import threading

nstages = 1
linha_interface_abaixo = []
utilidades_abaixo = []

#VARIÁVEIS DO CALOR
Qtotalh01 = []
Qtotalc01 = []
calor_atual_quente_abaixo = []
calor_atual_frio_abaixo = []
calor_atual_quente_sub_abaixo = []
calor_atual_frio_sub_abaixo = []
calor_sub_sem_utilidade = []

#VARIÁVEIS DE TEMPERATURAS QUENTES
temperatura_atual_quente_abaixo = []
temperatura_atual_quente_mesclada_abaixo = []

#VARIÁVEIS DE TEMPERATURAS FRIAS
temperatura_atual_fria_abaixo = []
temperatura_atual_fria_mesclada_abaixo = []
temp_misturador_abaixo = []

#VARIÁVEIS DE DIVISÃO
dividida_quente_abaixo = []
dividida_fria_abaixo = []
quantidade_quente_abaixo = []
quantidade_fria_abaixo = []
fracoes_quentes_abaixo = []
fracoes_frias_abaixo = []
fechar_corrente_abaixo = []



def declarar_np(*args):
	x = np.array([0.0])
	x.resize(args)
	return x

def preparar_dados_e_rede2(sk):
	global Qtotalh01, Qtotalc01, Qtotalh0, Qtotalc0
	global Thski, Thki, Thskf, Thkf, Tcski, Tcki, Tcskf, Tckf
	global Fharr, Fcarr, Q

	Thski = declarar_np(nhot, ncold, nsk, nstages)
	Thskf = declarar_np(nhot, ncold, nsk, nstages)
	Tcski = declarar_np(ncold, nhot, nsk, nstages)
	Tcskf = declarar_np(ncold, nhot, nsk, nstages)
	Q = declarar_np(nhot, ncold, ncold, nhot, nsk, nstages)

	if sk == 4:
		linha_interface_abaixo.clear()
		utilidades_abaixo.clear()

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
			temperatura_atual_quente_abaixo.append([])
			temperatura_atual_quente_mesclada_abaixo.append(Th0[quente])
			calor_atual_quente_sub_abaixo.append([])
			dividida_quente_abaixo.append(False)
			quantidade_quente_abaixo.append(1)
			fracoes_quentes_abaixo.append([])
			fechar_corrente_abaixo.append(False)
			temp_misturador_abaixo.append(0)
			calor_sub_sem_utilidade.append([])
			for sub in range(ncold):
				calor_atual_quente_sub_abaixo[quente].append(0)
				temperatura_atual_quente_abaixo[quente].append(Th0[quente])
		for fria in range(ncold):
			temperatura_atual_fria_abaixo.append([])
			temperatura_atual_fria_mesclada_abaixo.append(Tcf[fria])
			calor_atual_frio_sub_abaixo.append([])
			dividida_fria_abaixo.append(False)
			quantidade_fria_abaixo.append(1)
			fracoes_frias_abaixo.append([])
			for sub in range(nhot):
				calor_atual_frio_sub_abaixo[fria].append(0)
				temperatura_atual_fria_abaixo[fria].append(Tcf[fria])

		#calores totais
		for i in range (nhot):
			if Th0[i] <= Thf[i]:
				CPh[i] = 0
			Qtotalh01.append(CPh[i] * (Th0[i] - Thf[i]))
			calor_atual_quente_abaixo.append(CPh[i] * (Th0[i] - Thf[i]))
			calor_atual_quente_sub_abaixo[i][0] = CPh[i] * (Th0[i] - Thf[i])
		for j in range (ncold):
			if Tcf[j] <= Tc0[j]:
				CPc[j] = 0
			Qtotalc01.append(CPc[j] * (Tcf[j] - Tc0[j]))
			calor_atual_frio_abaixo.append(CPc[j] * (Tcf[j] - Tc0[j]))
			calor_atual_frio_sub_abaixo[j][0] = CPc[j] * (Tcf[j] - Tc0[j])

		for i in range(nhot):
			for j in range(ncold):
				for k in range(nstages):
					Qtotalh0[i][0][k] = Qtotalh01[i]
					Qtotalc0[j][0][k] = Qtotalc01[j]

	#prepara rede
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

def receber_pinch_abaixo(matriz_quente, matriz_fria, nquentes, nfrias, CPquente, CPfrio, deltaTmin, pinch_quente, pinch_frio, matriz_quente_in, matriz_fria_in, sk=2):
	global Th0, Thf, Tc0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, nsk
	Th0, Thf, Tc0, Tcf, CPh, CPc = [], [], [], [], [], []
	for corrente in range(nquentes):
		Thf.append(matriz_quente[corrente])
		Th0.append(matriz_quente_in[corrente])
		CPh.append(CPquente[corrente])
	for corrente in range(nfrias):
		Tc0.append(matriz_fria[corrente])
		Tcf.append(matriz_fria_in[corrente])
		CPc.append(CPfrio[corrente])
	pinchq = pinch_quente
	pinchf = pinch_frio
	nhot = nquentes
	ncold = nfrias
	dTmin = deltaTmin
	nsk = sk*max(nhot, ncold)
	preparar_dados_e_rede2(sk)

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

def verificar_trocador_estagio_abaixo(estagio, corrente, tipo):
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

def calcular_superestrutura_abaixo(dlg, acao, chot, ccold, sbhot, sbcold, sestagio, estagio):
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

	violou = False
	trocador_violado = False

	#CÁLCULO DE TODA A SUPERESTRUTURA
	for k in range (nstages):
		for sk in range (nsk):
			for i in range (nhot):
				for si in range (ncold):
					for j in range(ncold):
						for sj in range(nhot):

							if Q[i][si][j][sj][sk][k] != 0:

								#CALORES DOS ESTÁGIOS
								Qestagioq = 0
								for si1 in range (ncold):
									for j1 in range(ncold):
										for sj1 in range(nhot):
											for sk1 in range (nsk):
												Qestagioq += Q[i][si1][j1][sj1][sk1][k]
								Qestagiof = 0
								for sj1 in range (nhot):
									for i1 in range(nhot):
										for si1 in range(ncold):
											for sk1 in range (nsk):
												Qestagiof += Q[i1][si1][j][sj1][sk1][k]

								if Fharr[k][i][si] == 0:
									Fharr[k][i][si] = 100
								if Fcarr[k][j][sj] == 0:
									Fcarr[k][j][sj] = 100

								Thin = Thski[i][si][sk][k]
								Thout = Thin - (Q[i][si][j][sj][sk][k]/(CPh[i]*Fharr[k][i][si]/100))

								Think = Thki[i][k]
								Thoutk = Think - (Qestagioq/CPh[i])

								Tcin = Tcski[j][sj][sk][k]
								Tcout = Tcin - (Q[i][si][j][sj][sk][k]/(CPc[j]*Fcarr[k][j][sj]/100))

								Tcink = Tcki[j][k]
								Tcoutk = Tcink - (Qestagiof/CPc[j])

								tempdif = Thin - Tcin
								tempdif_terminal_frio = Thout - Tcout

								if tempdif < 0 or tempdif_terminal_frio < 0:
									if acao:
										QMessageBox.about(dlg, "Error!", "Thermodynamics Violation. The temperature of the cold stream will be greater thant the temperature of the hot stream")
										Q[i][si][j][sj][sk][k] = 0
										return True, "termo"
									else:
										QMessageBox.about(dlg, "Warning!", "Removing this Heat Exchanger resulted in a Thermodynamics Violation (E{})".format(sk+1))
								else:
									if dividida_quente_abaixo[i]:
										temperatura_atual_quente_abaixo[i][si] = Thout
									if dividida_fria_abaixo[j]:
										temperatura_atual_fria_abaixo[j][sj] = Tcout
									temperatura_atual_quente_mesclada_abaixo[i] = Thoutk
									temperatura_atual_fria_mesclada_abaixo[j] = Tcoutk

								#Temperatura de estágios e sub-estágios
								for k1 in range(nstages):
									for sk1 in range(nsk):
										if k1 > (k):
											#entrada
											Tcki[j][k1] = Tcoutk
											Thki[i][k1] = Thoutk

											#saída
											Tckf[j][k1] = Tcoutk
											Thkf[i][k1] = Thoutk

											for sub_fria in range(nhot):
												Tcski[j][sub_fria][sk1][k1] = Tcoutk
												Tcskf[j][sub_fria][sk1][k1] = Tcoutk
											for sub_quente in range(ncold):
												Thski[i][sub_quente][sk1][k1] = Thoutk
												Thskf[i][sub_quente][sk1][k1] = Thoutk

										if k1 == (k):
											if sk1 >= (sk):
												if sk1 > sk:
													Tcski[j][sj][sk1][k1] = Tcout
													Thski[i][si][sk1][k1] = Thout
												Tcskf[j][sj][sk1][k1] = Tcout
												Thskf[i][si][sk1][k1] = Thout

											Tckf[j][k1] = Tcoutk
											Thkf[i][k1] = Thoutk

								if Fharr[k][i][si] == 100:
									Fharr[k][i][si] = 0
								if Fcarr[k][j][sj] == 100:
									Fcarr[k][j][sj] = 0

	return violou, trocador_violado

def divisao_de_correntes_abaixo(divtype, estagio, corrente, quantidade, fracao):
	qsi = quantidade
	qsj = quantidade
	if divtype.upper() == 'Q':
		#desfaz divisoes anteriores
		for si in range(1, ncold):
			Qtotalh0[corrente-1][0][estagio-1] += Qtotalh0[corrente-1][si][estagio-1]
		for si in range(ncold-1, qsi-1, -1):#ex: antes 3 divisoes porem agora 2, zera a 3
			Fharr[estagio-1][corrente-1][si] = 0
			Qtotalh0[corrente-1][si][estagio-1] = 0
		#faz a nova divisao
		if qsi <= ncold:
			fracoes_quentes_abaixo[corrente-1] = []
			for si in range(qsi):
				Fharr[estagio-1][corrente-1][si] = 100 * fracao[si]
				fracoes_quentes_abaixo[corrente-1].append(fracao[si])
			for si in range(ncold-1, -1, -1):
				if Fharr[estagio-1][corrente-1][si] != 0:
					Qtotalh0[corrente-1][si][estagio-1] = Qtotalh0[corrente-1][0][estagio-1]*(Fharr[estagio-1][corrente-1][si]/100)
					calor_atual_quente_sub_abaixo[corrente-1][si] = Qtotalh0[corrente-1][si][estagio-1]
		if fracoes_quentes_abaixo[corrente-1][0] != 1:
			dividida_quente_abaixo[corrente-1] = True
		else:
			dividida_quente_abaixo[corrente-1] = False
		quantidade_quente_abaixo[corrente-1] = qsi

	if divtype.upper() == 'F':
		#desfaz divisoes anteriores
		for sj in range(1, nhot):
			Qtotalc0[corrente-1][0][estagio-1] += Qtotalc0[corrente-1][sj][estagio-1]
		for sj in range(nhot-1, qsj-1, -1):
			Fcarr[estagio-1][corrente-1][sj] = 0
			Qtotalc0[corrente-1][sj][estagio-1] = 0
		#faz a nova divisao
		if qsj <= nhot:
			fracoes_frias_abaixo[corrente-1] = []
			for sj in range(qsj):
				Fcarr[estagio-1][corrente-1][sj] = 100 * fracao[sj]
				fracoes_frias_abaixo[corrente-1].append(fracao[sj])
			for sj in range(nhot-1, -1, -1):
				if Fcarr[estagio-1][corrente-1][sj] != 0:
					Qtotalc0[corrente-1][sj][estagio-1] = Qtotalc0[corrente-1][0][estagio-1]*(Fcarr[estagio-1][corrente-1][sj]/100)
					calor_atual_frio_sub_abaixo[corrente-1][sj] = Qtotalc0[corrente-1][sj][estagio-1]
		if fracoes_frias_abaixo[corrente-1][0] != 1:
			dividida_fria_abaixo[corrente-1] = True
		else:
			dividida_fria_abaixo[corrente-1] = False
		quantidade_fria_abaixo[corrente-1] = qsj

def ler_dados_abaixo(dlg, subestagio_trocador_abaixo):
	i = int(dlg.comboBox_35.currentIndex()+1)
	j = int(dlg.comboBox_36.currentIndex()+1)
	si = int(dlg.comboBox_53.currentText())
	sj = int(dlg.comboBox_54.currentText())
	k = 1
	sk = subestagio_trocador_abaixo

	if ((Qtotalh0[i-1][si-1][k-1]) > (Qtotalc0[j-1][sj-1][k-1])):
		Qmax = Qtotalc0[j-1][sj-1][k-1]
	else:
		Qmax = Qtotalh0[i-1][si-1][k-1]
	if dlg.radioButton_20.isChecked():
		q = Qmax
	elif dlg.radioButton_17.isChecked():
		q = float(dlg.lineEdit_25.text().replace(",", "."))

	return [i, j, si, sj, sk, k, q]

def inserir_trocador_abaixo(dlg, vetor, verificar_termo=True, ignora=False):
	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] != 0:
		QMessageBox.about(dlg,"Error!","There is already a heat exchanger in this position!")
		return linha_interface_abaixo, False

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = vetor[6]

	if ((Qtotalh0[chot-1][sbhot-1][estagio-1]) > (Qtotalc0[ccold-1][sbcold-1][estagio-1])):
		Qmax = Qtotalc0[ccold-1][sbcold-1][estagio-1]
	else:
		Qmax = Qtotalh0[chot-1][sbhot-1][estagio-1]

	if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] > Qmax:
		if not ignora:
			QMessageBox.about(dlg,"Error!","The inputed heat is greater than the available heat.")
			Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0
			return linha_interface_abaixo, False
		else:
			QMessageBox.about(dlg,"Carreful!","The inputed heat is greater than the available heat. \nYou will use more than the utility duty.")

	elif Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] < 0:
		QMessageBox.about(dlg,"Error!","It is not possible to change a negative amount of heat.")
		Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0
		return linha_interface_abaixo, False

	elif Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] == 0:
		QMessageBox.about(dlg,"Error!","The inputed heat must be greater than 0.")
		return linha_interface_abaixo, False

	violou, trocador_violado = calcular_superestrutura_abaixo(dlg, verificar_termo, chot, ccold, sbhot, sbcold, sestagio, estagio)
	if violou and trocador_violado == "termo":
		return linha_interface_abaixo, False

	remocao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	if Fharr[estagio-1][chot-1][sbhot-1] == 0:
		fracao_quente = 1
	else:
		fracao_quente = Fharr[estagio-1][chot-1][sbhot-1]/100
	if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
		fracao_fria = 1
	else:
		fracao_fria = Fcarr[estagio-1][ccold-1][sbcold-1]/100

	calor_atual_quente_abaixo[chot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
	calor_atual_frio_abaixo[ccold-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
	calor_atual_quente_sub_abaixo[chot-1][sbhot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
	calor_atual_frio_sub_abaixo[ccold-1][sbcold-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

	linha_interface_abaixo.append([chot,
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

	for trocador in linha_interface_abaixo:
		trocador[7] = Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[8] = Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]

	return linha_interface_abaixo, True

def remover_trocador_abaixo(dlg, vetor, indice, linha_interface_abaixo):
	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	adicao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0

	calcular_superestrutura_abaixo(dlg, "remocao", chot, ccold, sbhot, sbcold, sestagio, estagio)

	if Fharr[estagio-1][chot-1][sbhot-1] == 0:
		fracao_quente = 1
	if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
		fracao_fria = 1

	calor_atual_quente_abaixo[chot-1] += vetor[6]
	calor_atual_frio_abaixo[ccold-1] += vetor[6]
	calor_atual_quente_sub_abaixo[chot-1][sbhot-1] += vetor[6]
	calor_atual_frio_sub_abaixo[ccold-1][sbcold-1] += vetor[6]

	if calor_atual_quente_abaixo[chot-1] == Qtotalh01[chot-1]:
		temperatura_atual_quente_mesclada_abaixo[chot-1] = pinchq
	if calor_atual_frio_abaixo[ccold-1] == Qtotalc01[ccold-1]:
		temperatura_atual_fria_mesclada_abaixo[ccold-1] = pinchf

	if calor_atual_quente_sub_abaixo[chot-1][sbhot-1] == Qtotalh01[chot-1] * Fharr[estagio-1][chot-1][sbhot-1]/100:
		temperatura_atual_quente_abaixo[chot-1][sbhot-1] = pinchq
	if calor_atual_frio_sub_abaixo[ccold-1][sbcold-1] == Qtotalc01[ccold-1] * Fcarr[estagio-1][ccold-1][sbcold-1]/100:
		temperatura_atual_fria_abaixo[ccold-1][sbcold-1] = pinchf

	linha_interface_abaixo.pop(indice)

def atualizar_matriz_abaixo(matriz):
	for trocador in matriz:
		trocador[7] = Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[8] = Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]

def adicionar_utilidade_abaixo(dlg, corrente):
	if calor_atual_quente_abaixo[corrente-1] == 0:
		QMessageBox.about(dlg, "Error!", "The heat of this stream has already been supplied")
		return
	utilidades_abaixo.append([corrente, calor_atual_quente_abaixo[corrente-1]])
	calor_sub_sem_utilidade[corrente-1] = calor_atual_quente_sub_abaixo[corrente-1][:]
	if dividida_quente_abaixo[corrente-1]:
		for si in range(quantidade_quente_abaixo[corrente-1]):
			temperatura_atual_quente_abaixo[corrente-1][si] = Thf[corrente-1]
			calor_atual_quente_sub_abaixo[corrente-1][si] = 0.0
	temp_misturador_abaixo[corrente-1] = temperatura_atual_quente_mesclada_abaixo[corrente-1]
	temperatura_atual_quente_mesclada_abaixo[corrente-1] = Thf[corrente-1]
	calor_atual_quente_abaixo[corrente-1] = 0.0
	fechar_corrente_abaixo[corrente-1] = True
	return utilidades_abaixo

def remover_utilidade_abaixo(corrente, indice_remover, utilidades_abaixo):
	if dividida_quente_abaixo[corrente-1]:
		for si in range(quantidade_quente_abaixo[corrente-1]):
			calor_atual_quente_sub_abaixo[corrente-1][si] = calor_sub_sem_utilidade[corrente-1][si]
			temperatura_atual_quente_abaixo[corrente-1][si] = calor_atual_quente_sub_abaixo[corrente-1][si]/(CPh[corrente-1]*Fharr[0][corrente-1][si]/100) + Thf[corrente-1]
	calor_atual_quente_abaixo[corrente-1] = utilidades_abaixo[indice_remover][1]
	temperatura_atual_quente_mesclada_abaixo[corrente-1] = calor_atual_quente_abaixo[corrente-1] / CPh[corrente-1] + Thf[corrente-1]
	utilidades_abaixo.pop(indice_remover)
	fechar_corrente_abaixo[corrente-1] = False

def caixa_de_temperatura_abaixo(dlg, sk):
	chot = int(dlg.TempLoadBelow.comboBox.currentText())
	ccold = int(dlg.TempLoadBelow.comboBox_2.currentText())
	sbhot = int(dlg.TempLoadBelow.comboBox_3.currentText())
	sbcold = int(dlg.TempLoadBelow.comboBox_4.currentText())
	estagio = 1
	sestagio = sk + 1

	if dlg.TempLoadBelow.radioButton_2.isChecked():                     #Inlet Hot Temperature
		outlethot = float(dlg.TempLoadBelow.lineEdit_2.text().replace(",", "."))
		q = round(-CPh[chot-1] * (outlethot - Thski[chot-1][sbhot-1][sestagio-1][estagio-1]), 2)
	if dlg.TempLoadBelow.radioButton.isChecked():
		inletcold = float(dlg.TempLoadBelow.lineEdit.text().replace(",", "."))
		q = round(-CPc[ccold-1] * (inletcold - Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1]), 2)

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
	dlg.comboBox_53.setCurrentText(str(dlg.TempLoadBelow.comboBox_3.currentText())) #si
	dlg.comboBox_54.setCurrentText(str(dlg.TempLoadBelow.comboBox_4.currentText())) #sj
	dlg.TempLoadBelow.close()

def testar_correntes_abaixo(dlg, primeira=False):
	nhotc = 0
	ncoldc = 0
	somaCPh = 0
	somaCPc = 0

	for quente in range(nhot):
		if Th0[quente] == pinchq:
			somaCPh += CPh[quente]
			if CPh[quente] != 0:
				if dividida_quente_abaixo[quente]:
					nhotc += quantidade_quente_abaixo[quente]
				else:
					nhotc += 1

	for fria in range(ncold):
		if Tcf[fria] == pinchf:
			somaCPc += CPc[fria]
			if CPc[fria] != 0:
				if dividida_fria_abaixo[fria]:
					ncoldc += quantidade_fria_abaixo[fria]
				else:
					ncoldc += 1

	if somaCPc > somaCPh:
		dlg.label_25.setStyleSheet("QLabel {color: red}")
	else:
		dlg.label_25.setStyleSheet("QLabel {color: green}")

	if ncoldc > nhotc:
		dlg.label_22.setStyleSheet("QLabel {color: red}")
		if not primeira:
			QMessageBox.about(dlg,"Be Carreful","With this Split, you went against the Pinch Recomendations")
	else:
		dlg.label_22.setStyleSheet("QLabel {color: green}")

	if somaCPh >= somaCPc and ncoldc <= nhotc:
		dlg.label_27.setText("Respected")
		dlg.label_27.setStyleSheet("QLabel {color: green}")
	else:
		dlg.label_27.setText("Not Respected")
		dlg.label_27.setStyleSheet("QLabel {color: red}")

def remover_todos_abaixo():
	for i in range(len(linha_interface_abaixo)-1, -1, -1):
		remover_trocador_abaixo("oi", linha_interface_abaixo[i], i, linha_interface_abaixo)
	for i in range(len(utilidades_abaixo)-1, -1, -1):
		remover_utilidade_abaixo(utilidades_abaixo[i][0], i, utilidades_abaixo)
