from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMessageBox
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys

Th0 = [70, 70]
map(float, Th0)
Thf = [60, 30]
map(float, Thf)
CPh = [3, 1.5]
map(float, CPh)

Tc0 = [60, 40]
map(float, Tc0)
Tcf = [60, 60]
map(float, Tcf)
CPc = [4, 2]
map(float, CPc)

divop = avanc = ''
dTmin = 10
nhot = 2
ncold = 2
pinchq = 70
pinchf = 60

#variaveis do carlos
linha_interface_abaixo = []
utilidades_abaixo = []
estagio = 0
sestagio = 0
temperatura_atual_quente_abaixoarr = np.array([0])
temperatura_atual_quente_abaixoarr.resize(nhot)
temperatura_atual_quente_abaixo = temperatura_atual_quente_abaixoarr.tolist()
map(float, temperatura_atual_quente_abaixo)

temperatura_atual_fria_abaixoarr = np.array([0])
temperatura_atual_fria_abaixoarr.resize(ncold)
temperatura_atual_fria_abaixo = temperatura_atual_fria_abaixoarr.tolist()
map(float, temperatura_atual_fria_abaixo)

calor_atual_quente_abaixoarr = np.array([0])
calor_atual_quente_abaixoarr.resize(nhot)
calor_atual_quente_abaixo = calor_atual_quente_abaixoarr.tolist()

calor_atual_frio_abaixoarr = np.array([0])
calor_atual_frio_abaixoarr.resize(ncold)
calor_atual_frio_abaixo = calor_atual_frio_abaixoarr.tolist()

Q_quente_da_corrente_sem_troca_abaixoarr = np.array([0])
Q_quente_da_corrente_sem_troca_abaixoarr.resize(nhot)
Q_quente_da_corrente_sem_troca_abaixo = Q_quente_da_corrente_sem_troca_abaixoarr.tolist()

Q_frio_da_corrente_sem_troca_abaixoarr = np.array([0])
Q_frio_da_corrente_sem_troca_abaixoarr.resize(ncold)
Q_frio_da_corrente_sem_troca_abaixo = Q_frio_da_corrente_sem_troca_abaixoarr.tolist()

complistq = []
complistf = []
cont = contq = contf = compq = compf = opcao = 0
chot = ccold = sbhot = sbcold = nhotc = ncoldc = qsi = qsj = chotutil = 0
Qtotalestagio = Qtotalestagiof = Qmax = Qtotalhaux = Qtotalcaux = 0
somaCPh = somaCPc = 0
tempdif = tempmeta = 0

nsi = [ncold, ncold]
nsj = [nhot, nhot]

nsk = nstages = 2

#VARIÁVEIS DO CALOR
Qtotalh01 = []
Qtotalc01 = []
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


#VARIÁVEIS DE TEMPERATURAS QUENTES
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
Thsfinal0arr = np.array ([0])
Thsfinal0arr.resize(nhot, ncold, nstages)
Thsfinal0 = Thsfinal0arr.tolist()
map(float, Thsfinal0)
Thfinal0arr = np.array ([0])
Thfinal0arr.resize(nhot)
Thfinal0 = Thfinal0arr.tolist()
map(float, Thfinal0)
Thfinal01arr = np.array ([0])
Thfinal01arr.resize(nhot, ncold)
Thfinal01 = Thfinal01arr.tolist()
map(float, Thfinal01)

Thfinal01karr = np.array ([0])
Thfinal01karr.resize(nhot, nstages)
Thfinal01k = Thfinal01karr.tolist()
map(float, Thfinal01k)

#VARIÁVEIS DE TEMPERATURAS FRIAS
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
Tcsfinal0arr = np.array ([0])
Tcsfinal0arr.resize(ncold, nhot, nstages)
Tcsfinal0 = Tcsfinal0arr.tolist()
map(float, Tcsfinal0)
Tcfinal0arr = np.array ([0])
Tcfinal0arr.resize(ncold)
Tcfinal0 = Tcfinal0arr.tolist()
map(float, Tcfinal0)
Tcfinal01arr = np.array ([0])
Tcfinal01arr.resize(ncold, nhot)
Tcfinal01 = Tcfinal01arr.tolist()
map(float, Tcfinal01)

Tcfinal01karr = np.array ([0])
Tcfinal01karr.resize(ncold, nstages)
Tcfinal01k = Tcfinal01karr.tolist()
map(float, Tcfinal01k)

#VARIÁVEIS DE TEMPERATURAS "GERAIS"
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

#OUTRAS VARIÁVEIS
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

def limpar_lista(lista):
	for i in range(len(lista)):
		lista.pop(-1)

def preparar_dados_e_rede2():
	#CÁLCULOS DOS CALORES TOTAIS
	for i in range (nhot):
		Qtotalh1 = 0
		Qtotalh1 = CPh[i] * (Th0[i] - Thf[i])
		Qtotalh01.append(Qtotalh1)
		Qtotalh01[i] = Qtotalh01[i]
		calor_atual_quente_abaixo[i] = Qtotalh01[i]
		Q_quente_da_corrente_sem_troca_abaixo[i] = Qtotalh01[i]
	for j in range (ncold):
		Qtotalc1 = 0
		Qtotalc1 = CPc[j] * (Tcf[j] - Tc0[j])
		Qtotalc01.append(Qtotalc1)
		Qtotalc01[j] = Qtotalc01[j]
		calor_atual_frio_abaixo[j] = Qtotalc01[j]
		Q_frio_da_corrente_sem_troca_abaixo[j] = Qtotalc01[j]

	for i in range(nhot):
		for j in range(ncold):
			for k in range(nstages):
				Qtotalh0[i][0][k] = Qtotalh01[i]
				Qtotalc0[j][0][k] = Qtotalc01[j]

	map(float, Qtotalh01)
	map(float, Qtotalc01)

	#Preparar rede
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

	#variaveis de printar
	for quente in range(nhot):
		temperatura_atual_quente_abaixo[quente] = pinchq

	for fria in range(ncold):
		temperatura_atual_fria_abaixo[fria] = pinchf

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
					print(Qtotalestagioq)
					for si in range(ncold):
						Qtotalh0[chot-1][si][k] = Qtotalestagioq*(Fharr[k][chot-1][si]/100)
						print(Qtotalh0)

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

def divisao_de_correntes():
	global nhotc, ncoldc
	cont = 0
	divtype = input("Deseja dividir correntes quentes, frias ou ambas? ").strip().upper()[0]
	estagio = int(input('Em qual estágio ocorrerá a divisão? '))
	for i in range (nhot):
		for si in range (ncold):
			for j in range(ncold):
				for sj in range(nhot):
					for sk in range (nsk):
						if Q[i][si][j][sj][sk][estagio-1] != 0:
							print('Já existe um trocador neste estágio. Remova-o primeiro antes de dividir correntes!')
							cont = 1
							input()
							break
	if cont == 0:
		if divtype == 'A':
			chot = int(input('Qual corrente quente será dividida? '))
			qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? '))
			for k in range(nstages):
				for si in range(ncold):
					if si == 0:
						continue
					else:
						Qtotalh0[chot-1][0][k] += Qtotalh0[chot-1][si][k]
			for si in range(ncold-1, qsi-1, -1):
				Fharr[estagio-1][chot-1][si] = 0
				Qtotalh0[chot-1][si][estagio-1] = 0
			while qsi > nsi[chot-1]:
				print('Erro! O número de divisões é muito grande.')
				qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? '))
			if qsi <= nsi[chot-1]:
				for si in range(qsi-1, -1, -1):
					Fharr[estagio-1][chot-1][si] = float(input(f'Qual a fração da sub-corrente quente {si+1}? '))
				for si in range(ncold-1, -1, -1):
					for k in range(nstages-1, -1, -1):
						if Fharr[k][chot-1][si] == 0:
							continue
						else:
							Qtotalh0[chot-1][si][k] = Qtotalh0[chot-1][0][k]*(Fharr[k][chot-1][si]/100)
			ccold = int(input('Qual corrente fria será dividida? '))
			qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? '))
			for k in range(nstages):
				for sj in range(nhot):
					if sj == 0:
						continue
					else:
						Qtotalc0[ccold-1][0][k] += Qtotalc0[ccold-1][sj][k]
			for sj in range(nhot-1, qsj-1, -1):
				Fcarr[estagio-1][ccold-1][sj] = 0
				Qtotalc0[ccold-1][sj][estagio-1] = 0
			while qsj > nsj[ccold-1]:
				print('Erro! O número de divisões é muito grande.')
				qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? '))
			if qsj <= nsj[ccold-1]:
				for j in range(qsj-1, -1, -1):
					Fcarr[estagio-1][ccold-1][j] = float(input(f'Qual a fração da sub-corrente fria {j+1}? '))
				for sj in range(nhot-1, -1, -1):
					for k in range(nstages-1, -1, -1):
						if Fcarr[k][ccold-1][sj] == 0:
							continue
						else:
							Qtotalc0[ccold-1][sj][k] = Qtotalc0[ccold-1][0][k]*(Fcarr[k][ccold-1][sj]/100)
			nhotc = qsi + (nhot - 1)
			ncoldc = qsj + (ncold - 1)

		if divtype == 'Q':
			chot = int(input('Qual corrente quente será dividida? '))
			qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? '))
			for k in range(nstages):
				for si in range(ncold):
					if si == 0:
						continue
					else:
						Qtotalh0[chot-1][0][k] += Qtotalh0[chot-1][si][k]
			for si in range(ncold-1, qsi-1, -1):
				Fharr[estagio-1][chot-1][si] = 0
				Qtotalh0[chot-1][si][estagio-1] = 0
			while qsi > nsi[chot-1]:
				print('Erro! O número de divisões é muito grande.')
				qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? '))
			if qsi <= nsi[chot-1]:
				for si in range(qsi-1, -1, -1):
					Fharr[estagio-1][chot-1][si] = float(input(f'Qual a fração da sub-corrente quente {si+1}? '))
				for si in range(ncold-1, -1, -1):
					for k in range(nstages-1, -1, -1):
						if Fharr[k][chot-1][si] == 0:
							continue
						else:
							Qtotalh0[chot-1][si][k] = Qtotalh0[chot-1][0][k]*(Fharr[k][chot-1][si]/100)

			nhotc = qsi + (nhot - 1)
		if divtype == 'F':
			ccold = int(input('Qual corrente fria será dividida? '))
			qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? '))
			for k in range(nstages):
				for sj in range(nhot):
					if sj == 0:
						continue
					else:
						Qtotalc0[ccold-1][0][k] += Qtotalc0[ccold-1][sj][k]
			for sj in range(nhot-1, qsj-1, -1):
				Fcarr[estagio-1][ccold-1][sj] = 0
				Qtotalc0[ccold-1][sj][estagio-1] = 0
			while qsj > nsj[ccold-1]:
				print('Erro! O número de divisões é muito grande.')
				qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? '))
			if qsj <= nsj[ccold-1]:
				for sj in range(qsj-1, -1, -1):
					Fcarr[estagio-1][ccold-1][sj] = float(input(f'Qual a fração da sub-corrente quente {sj+1}? '))
				for sj in range(nhot-1, -1, -1):
					for k in range(nstages-1, -1, -1):
						if Fcarr[k][ccold-1][sj] == 0:
							continue
						else:
							Qtotalc0[ccold-1][sj][k] = Qtotalc0[ccold-1][0][k]*(Fcarr[k][ccold-1][sj]/100)
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

								Tcin[i][si][j][sj][sk][k] = Tcski[j][sj][sk][k]
								Tcout[i][si][j][sj][sk][k] = Tcin[i][si][j][sj][sk][k] - (Qaux[i][si][j][sj][sk][k]/(CPc[j]*(Fcarr[k][j][sj]/100)))
								temperatura_atual_fria_abaixo[j] = Tcout[i][si][j][sj][sk][k]

								Tcink[i][si][j][sj][sk][k] = Tcki[j][k]
								Tcoutk[i][si][j][sj][sk][k] = Tcink[i][si][j][sj][sk][k] - (Qestagiof[j][k]/CPc[j])

								tempdif = (Thout[i][si][j][sj][sk][k] - Tcout[i][si][j][sj][sk][k])

								if tempdif < 0:
									tempdif = - tempdif
								if tempdif >= dTmin:
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

								else:
									print('Erro! A diferença mínima de temperatura não está sendo respeitada: ', tempdif)
									return
									#avanc = str(input('Deseja continuar mesmo assim? ')).strip().upper()[0]
									#if avanc == 'Y':
									#	Thfinal01[i][si] = Thout[i][si][j][sj][sk][k]
									#	Tcfinal01[j][sj] = Tcout[i][si][j][sj][sk][k]
									#	Thfinal01k[i][k] = Thoutk[i][si][j][sj][sk][k]
									#	Tcfinal01k[j][k] = Tcoutk[i][si][j][sj][sk][k]

									#	for k1 in range(nstages):
									#		for sk1 in range(nsk):
									#			if k1 > (k):
									#				Tcki[j][k1] = Tcfinal01k[j][k]
									#				Tcski[j][sj][sk1][k1] = Tcfinal01k[j][k]
									#				Thki[i][k1] = Thfinal01k[i][k]
									#				Thski[i][si][sk1][k1] = Thfinal01k[i][k]
									#			if k1 == (k):
									#				if sk1 > (sk):
									#					Tcski[j][sj][sk1][k1] = Tcfinal01[j][sj]
									#					Thski[i][si][sk1][k1] = Thfinal01[i][si]

									#	#Temperatura final dos estágios e sub-estágios
									#	for k1 in range(nstages):
									#		for sk1 in range(nsk):
									#			if k1 > (k):
									#				Tckf[j][k1] = Tcfinal01k[j][k]
									#				Tcskf[j][sj][sk1][k1] = Tcfinal01k[j][k]
									#				Thkf[i][k1] = Thfinal01k[i][k]
									#				Thskf[i][si][sk1][k1] = Thfinal01k[i][k]
									#			if k1 == (k):
									#				if sk1 >= (sk):
									#					Tcskf[j][sj][sk1][k1] = Tcfinal01[j][sj]
									#					Thskf[i][si][sk1][k1] = Thfinal01[i][si]
									#				Tckf[j][k1] = Tcfinal01k[j][k]
									#				Thkf[i][k1] = Thfinal01k[i][k]
									#else:
									#	print('A troca de calor não ocorreu!')
									#	Q[i][si][j][sj][sk][k] = 0
									#	cont = 1

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
	if cont != 1:
		remocao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	if Fharr[estagio-1][chot-1][sestagio-1] == 0:
		fracao_quente = 1
	if Fharr[estagio-1][ccold-1][sestagio-1] == 0:
		fracao_fria = 1

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


	return linha_interface_abaixo

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

								Tcin[i][si][j][sj][sk][k] = Tcski[j][sj][sk][k]
								Tcout[i][si][j][sj][sk][k] = Tcin[i][si][j][sj][sk][k] - (Q[i][si][j][sj][sk][k]/(CPc[j]*(Fcarr[k][j][sj]/100)))
								temperatura_atual_fria_abaixo[j] = Tcout[i][si][j][sj][sk][k]

								Tcink[i][si][j][sj][sk][k] = Tcki[j][k]
								Tcoutk[i][si][j][sj][sk][k] = Tcink[i][si][j][sj][sk][k] - (Qestagiof[j][k]/CPc[j])

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

	if calor_atual_quente_abaixo[chot-1] == Q_quente_da_corrente_sem_troca_abaixo[chot-1]:
		temperatura_atual_quente_abaixo[chot-1] = pinchq
	if calor_atual_frio_abaixo[ccold-1] == Q_frio_da_corrente_sem_troca_abaixo[ccold-1]:
		temperatura_atual_fria_abaixo[ccold-1] = pinchf

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
	Thfinal0[chotutil-1] = Thf[chotutil-1]
	temperatura_atual_quente_abaixo[chotutil-1] = Thf[chotutil-1]
	calor_atual_quente_abaixo[chotutil-1] = 0.0
	utilidades_abaixo.append([chotutil, q])
	print(utilidades_abaixo)
	return utilidades_abaixo

def remover_utilidade_abaixo(corrente, indice_remover, utilidades_abaixo):
	Qtotalh0[corrente-1][0][0] = utilidades_abaixo[indice_remover][1]
	calor_atual_quente_abaixo[corrente-1] = Qtotalh0[corrente-1][0][0]
	temperatura_atual_quente_abaixo[corrente-1] = -calor_atual_quente_abaixo[corrente-1] / CPh[corrente-1] + Thf[corrente-1]
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
