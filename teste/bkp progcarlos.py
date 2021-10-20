from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMessageBox
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys

Th0 = [170, 150]
map(float, Th0)
Thf = [70, 70]
map(float, Thf)
CPh = [3, 1.5]
map(float, CPh)

Tc0 = [60, 60]
map(float, Tc0)
Tcf = [140, 170]
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
linha_interface = []
linha_pra_procurar = []
trocadores_adicionados = 0
estagio = 0
sestagio = 0
temperatura_atual_quentearr = np.array([0])
temperatura_atual_quentearr.resize(nhot)
temperatura_atual_quente = temperatura_atual_quentearr.tolist()
map(float, temperatura_atual_quente)

temperatura_atual_friaarr = np.array([0])
temperatura_atual_friaarr.resize(ncold)
temperatura_atual_fria = temperatura_atual_friaarr.tolist()
map(float, temperatura_atual_fria)

calor_atual_quentearr = np.array([0])
calor_atual_quentearr.resize(nhot)
calor_atual_quente = calor_atual_quentearr.tolist()

calor_atual_frioarr = np.array([0])
calor_atual_frioarr.resize(ncold)
calor_atual_frio = calor_atual_frioarr.tolist()



complistq = []
complistf = []
cont = contq = contf = compq = compf = opcao = 0
chot = ccold = sbhot = sbcold = nhotc = ncoldc = qsi = qsj = ccoldutil = 0
Qtotalestagio = Qtotalestagiof = Qmax = Qtotalhaux = Qtotalcaux = 0
somaCPh = somaCPc = 0
tempdif = tempmeta = 0

nsi = [ncold, ncold]
nsj = [nhot, nhot]

nsk = nstages = 2

#VARIÁVEIS DE CALOR
Qutilcold = np.array([0])
Qutilcold.resize(ncold)
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

#CÁLCULOS DOS CALORES TOTAIS
for i in range (nhot):
	Qtotalh1 = 0
	Qtotalh1 = CPh[i] * (Th0[i] - Thf[i])
	Qtotalh01.append(Qtotalh1)
	Qtotalh01[i] = float('{:.2f}'.format(Qtotalh01[i]))
	calor_atual_quente[i] = Qtotalh01[i]
for j in range (ncold):
	Qtotalc1 = 0
	Qtotalc1 = CPc[j] * (Tcf[j] - Tc0[j])
	Qtotalc01.append(Qtotalc1)
	Qtotalc01[j] = float('{:.2f}'.format(Qtotalc01[j]))
	calor_atual_frio[j] = Qtotalc01[j]

for i in range(nhot):
	for j in range(ncold):
		for k in range(nstages):
			Qtotalh0[i][0][k] = Qtotalh01[i]
			Qtotalc0[j][0][k] = Qtotalc01[j]

map(float, Qtotalh01)
map(float, Qtotalc01)

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

#teste so calma
for quente in range(nhot):
	temperatura_atual_quente[quente] = pinchq

for fria in range(ncold):
	temperatura_atual_fria[fria] = pinchf


def linha():
	print('-'*42)

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

def consultar_correntes():
	pass

def divisao_de_correntes():
	global nhotc, ncoldc
	cont = 0
	divtype = input("Deseja dividir correntes quentes, frias ou ambas? ").strip().upper()[0]
	estagio = int(input('Em qual estágio ocorrerá a divisão? '))
	for i in range (nhot):
		for si in range (ncold): #max de subcorrentes quentes é igual ao numero de correntes frias
			for j in range(ncold):
				for sj in range(nhot): #max de subcorrentes frias é igual ao numero de correntes quentes
					for sk in range (nsk):
						if Q[i][si][j][sj][sk][estagio-1] != 0:
							print('Já existe um trocador neste estágio. Remova-o primeiro antes de dividir correntes!')
							cont = 1
							input()
							break
	if cont == 0:
		if divtype == 'A': #ambas quente e fria
			chot = int(input('Qual corrente quente será dividida? '))
			qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? '))
			for k in range(nstages):
				for si in range(ncold):
					if si == 0:								#fixa a corrente quente e acha a si e k que tem o Q trocador
						continue							#salvando esse valor na si 0 pra fazer as contas depois
					else:
						Qtotalh0[chot-1][0][k] += Qtotalh0[chot-1][si][k]
			for si in range(ncold-1, qsi-1, -1):
				Fharr[estagio-1][chot-1][si] = 0			#caso houvesse dividido a corrente anteriormente, zera tudo pra poder
				Qtotalh0[chot-1][si][estagio-1] = 0			#dividir novamente
			while qsi > nsi[chot-1]:
				print('Erro! O número de divisões é muito grande.')
				qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? '))
			if qsi <= nsi[chot-1]:
				for si in range(qsi-1, -1, -1):
					Fharr[estagio-1][chot-1][si] = float(input(f'Qual a fração da sub-corrente quente {si+1}? '))
				for si in range(ncold-1, -1, -1):
					for k in range(nstages-1, -1, -1):		#varre as frações de todas as si e k e quando acha
						if Fharr[k][chot-1][si] == 0:		#a corrente que foi dividida multiplica o calor total
							continue						#pela fração que vai ser dividida, obtendo o calor da subcorrente no k
						else:
							Qtotalh0[chot-1][si][k] = Qtotalh0[chot-1][0][k]*(Fharr[k][chot-1][si]/100)
			ccold = int(input('Qual corrente fria será dividida? '))
			qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? '))
			for k in range(nstages):
				for sj in range(nhot):
					if sj == 0:								#fixa a corrente fria e acha a sj e o k que tem o Q trocador
						continue							#salvando esse valor na sj 0 pra fazer as contas depois
					else:
						Qtotalc0[ccold-1][0][k] += Qtotalc0[ccold-1][sj][k]
			for sj in range(nhot-1, qsj-1, -1):
				Fcarr[estagio-1][ccold-1][sj] = 0			#caso houvesse dividido a corrente anteriormente, zera tudo pra poder
				Qtotalc0[ccold-1][sj][estagio-1] = 0		#dividir novamente
			while qsj > nsj[ccold-1]:
				print('Erro! O número de divisões é muito grande.')
				qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? '))
			if qsj <= nsj[ccold-1]:
				for sj in range(qsj-1, -1, -1):
					Fcarr[estagio-1][ccold-1][sj] = float(input(f'Qual a fração da sub-corrente fria {j+1}? '))
				for sj in range(nhot-1, -1, -1):
					for k in range(nstages-1, -1, -1):		#varre as frações de todas as sj e os k e quando acha
						if Fcarr[k][ccold-1][sj] == 0:		#a corrente que foi dividida, multiplica o calor total
							continue						#pela fração que vai ser dividida, obtendo o calor da subcorrente no k
						else:
							Qtotalc0[ccold-1][sj][k] = Qtotalc0[ccold-1][0][k]*(Fcarr[k][ccold-1][sj]/100)
			nhotc = qsi + (nhot - 1)						#arruma a quantidade de correntes pois morre uma pra adicionar a
			ncoldc = qsj + (ncold - 1)						#quantidade que foi dividida

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

def ler_dados(dlg):
	k = int(dlg.comboBox_8.currentText())
	sk = int(dlg.comboBox_7.currentText())
	i = int(dlg.comboBox_2.currentText())
	j = int(dlg.comboBox_5.currentText())
	si = int(dlg.comboBox_50.currentText())
	sj = int(dlg.comboBox_51.currentText())
	print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	print(Qtotalh0[i-1][si-1][k-1], "quente")
	print(Qtotalc0[j-1][sj-1][k-1], "frio")
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

	if ((Qtotalh0[chot-1][sbhot-1][estagio-1]) > (Qtotalc0[ccold-1][sbcold-1][estagio-1])):
		Qmax = Qtotalc0[ccold-1][sbcold-1][estagio-1]
	else:
		Qmax = Qtotalh0[chot-1][sbhot-1][estagio-1]

	if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] > Qmax:
		print('A quantidade de calor requerido é maior que a quantidade de calor disponível')
		QMessageBox.about(dlg,"Error!","calor grande")
		Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0
		return

	elif Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] < 0:
		print('Não é possível trocar uma quantidade negativa de calor')
		QMessageBox.about(dlg,"Error!","calor negativo")
		Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0
		return

	elif Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] == 0:					#calor igual a 0 (pq é valido?), ve se o
		print('A quantidade de calor trocada foi 0.')
		QMessageBox.about(dlg,"Error!","0 de calor")									#usuário quer continuar. Se quiser, descarta
		return


	for i in range (nhot):
		for si in range (ncold):
			for sk in range (nsk):																#iguala as temperaturas dos subestágios
				for k in range (nstages):														#a temperatura da corrente antes da troca
					Thski[i][si][sk][k] = Thf[i]
					Thskf[i][si][sk][k] = Thf[i]

		for k in range (nstages):																#iguala as temperaturas dos estágios a
			Thki[i][k] = Thf[i]																	#temperatura da corrente antes da troca
			Thkf[i][k] = Thf[i]

	for j in range (ncold):
		for sj in range (nhot):
			for sk in range(nsk-1, -1, -1):														#mesma coisa de cima soq pra corrente fria
				for k in range(nstages-1, -1, -1):
					Tcski[j][sj][sk][k] = Tc0[j]
					Tcskf[j][sj][sk][k] = Tc0[j]
		for k in range (nstages-1, -1, -1):
			Tcki[j][k] = Tc0[j]																	#mesma coisa de cima soq pra corrente fria
			Tckf[j][k] = Tc0[j]

	# CÁLCULO DE TODA A SUPERESTRUTURA
	for k in range (nstages-1, -1, -1):
		for sk in range (nsk-1, -1, -1):
			for i in range (nhot-1, -1, -1):
				for si in range (ncold-1, -1, -1):
					for j in range(ncold-1, -1, -1):
						for sj in range(nhot-1, -1, -1):

							Qaux[i][si][j][sj][sk][k] = Q[i][si][j][sj][sk][k]								#acha a posição que tem trocador
																											#e quando encontrada, executa o if
							if Qaux[i][si][j][sj][sk][k] != 0:

								#CALORES DOS ESTÁGIOS
								Qtotalhaux = 0
								for si1 in range (ncold):
									for j1 in range(ncold):
										for sj1 in range(nhot):												#um estágio pode ter mais de um trocador, entao
											for sk1 in range (nsk):											#pra obter as temperaturas de entrada e saída dele
												Qtotalhaux += Qaux[chot-1][si1][j1][sj1][sk1][estagio-1]	#tem que ter o qtotal do estagio tanto para
								Qtotalcaux = 0																#as correntes quentes quando para as correntes
								for sj1 in range (nhot):													#frias
									for i1 in range(nhot):
										for si1 in range(ncold):
											for sk1 in range (nsk):
												Qtotalcaux += Qaux[i1][si1][ccold-1][sj1][sk1][estagio-1]

								Qestagioq[chot-1][estagio-1] = Qtotalhaux									#salva Q em uma variável de estágio
								Qestagiof[ccold-1][estagio-1] = Qtotalcaux									#pra calcular depois com o Cp as temperaturas
																												#dos estágios (entrada saída essas coisas)
								if Fharr[k][i][si] == 0:
									Fharr[k][i][si] = 100
								if Fcarr[k][j][sj] == 0:													#volta as frações que estavam 0 (False) pra 100
									Fcarr[k][j][sj] = 100


								#Temp quente de saída do trocador recebe T quente de saída do subestágio
								Thin[i][si][j][sj][sk][k] = Thski[i][si][sk][k]
								#Temp quente de entrada do trocador é calculada
								Thout[i][si][j][sj][sk][k] = Thin[i][si][j][sj][sk][k] + (Q[i][si][j][sj][sk][k]/(CPh[i]*(Fharr[k][i][si]/100)))
								temperatura_atual_quente[i] = Thout[i][si][j][sj][sk][k]

								#Temp quente de saída do estágio recebe T quente de entrada do estágio
								Think[i][si][j][sj][sk][k] = Thki[i][k]
								#Temp quente de entrada do estágio é calculada com Q estágio
								Thoutk[i][si][j][sj][sk][k] = Think[i][si][j][sj][sk][k] + (Qestagioq[i][k]/CPh[i])

								#Temp fria entrada do trocador
								Tcin[i][si][j][sj][sk][k] = Tcski[j][sj][sk][k]
								#Temp fria saída do trocador
								Tcout[i][si][j][sj][sk][k] = Tcin[i][si][j][sj][sk][k] + (Q[i][si][j][sj][sk][k]/(CPc[j]*(Fcarr[k][j][sj]/100)))
								temperatura_atual_fria[j] = Tcout[i][si][j][sj][sk][k]
								#Temp fria entrada do estágio
								Tcink[i][si][j][sj][sk][k] = Tcki[j][k]
								#Temp fria saída do estágio
								Tcoutk[i][si][j][sj][sk][k] = Tcink[i][si][j][sj][sk][k] + (Qestagiof[j][k]/CPc[j])

								#tempdif = (Thin[i][si][j][sj][sk][k] - Tcin[i][si][j][sj][sk][k])
								#print("Delta T terminal frio:", tempdif)
								#tempdif2 = (Thout[i][si][j][sj][sk][k] - Tcout[i][si][j][sj][sk][k])
								#print("Delta T terminal quente:", tempdif2)
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
											if k1 < (k):
												Tcki[j][k1] = Tcfinal01k[j][k]
												Tcski[j][sj][sk1][k1] = Tcfinal01k[j][k]
												Thki[i][k1] = Thfinal01k[i][k]
												Thski[i][si][sk1][k1] = Thfinal01k[i][k]
											if k1 == (k):
												if sk1 < (sk):
													Tcski[j][sj][sk1][k1] = Tcfinal01[j][sj]
													Thski[i][si][sk1][k1] = Thfinal01[i][si]

									#Temperatura final dos estágios e sub-estágios
									for k1 in range(nstages):
										for sk1 in range(nsk):
											if k1 < (k):
												Tckf[j][k1] = Tcfinal01k[j][k]
												Tcskf[j][sj][sk1][k1] = Tcfinal01k[j][k]
												Thkf[i][k1] = Thfinal01k[i][k]
												Thskf[i][si][sk1][k1] = Thfinal01k[i][k]
											if k1 == (k):
												if sk1 <= (sk):
													Tcskf[j][sj][sk1][k1] = Tcfinal01[j][sj]
													Thskf[i][si][sk1][k1] = Thfinal01[i][si]
												Tckf[j][k1] = Tcfinal01k[j][k]
												Thkf[i][k1] = Thfinal01k[i][k]

								else:
									print('Erro! A diferença mínima de temperatura não está sendo respeitada: ', tempdif)
									avanc = str(input('Deseja continuar mesmo assim? ')).strip().upper()[0]
									if avanc == 'Y':
										Tcfinal01[j][sj] = Tcout[i][si][j][sj][sk][k]
										Thfinal01[i][si] = Thout[i][si][j][sj][sk][k]
										Thfinal01k[i][k] = Thoutk[i][si][j][sj][sk][k]
										Tcfinal01k[j][k] = Tcoutk[i][si][j][sj][sk][k]

										#Temperatura inicial de estágios e sub-estágios
										for k1 in range(nstages):
											for sk1 in range(nsk):
												if k1 < (k):
													Tcki[j][k1] = Tcfinal01k[j][k]
													Tcski[j][sj][sk1][k1] = Tcfinal01k[j][k]
													Thki[i][k1] = Thfinal01k[i][k]
													Thski[i][si][sk1][k1] = Thfinal01k[i][k]
												if k1 == (k):
													if sk1 < (sk):
														Tcski[j][sj][sk1][k1] = Tcfinal01[j][sj]
														Thski[i][si][sk1][k1] = Thfinal01[i][si]

										#Temperatura final dos estágios e sub-estágios
										for k1 in range(nstages):
											for sk1 in range(nsk):
												if k1 < (k):
													Tckf[j][k1] = Tcfinal01k[j][k]
													Tcskf[j][sj][sk1][k1] = Tcfinal01k[j][k]
													Thkf[i][k1] = Thfinal01k[i][k]
													Thskf[i][si][sk1][k1] = Thfinal01k[i][k]
												if k1 == (k):
													if sk1 <= (sk):
														Tcskf[j][sj][sk1][k1] = Tcfinal01[j][sj]
														Thskf[i][si][sk1][k1] = Thfinal01[i][si]
													Tckf[j][k1] = Tcfinal01k[j][k]
													Thkf[i][k1] = Thfinal01k[i][k]
									else:
										print('A troca de calor não ocorreu!')
										Q[i][si][j][sj][sk][k] = 0
										cont = 1

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

	print()


	#for k in range(nstages):
	#	print('ESTÁGIO ', k+1)
		#	print('Temperatura de entrada quente no estagio')
		#	print(Thki[chot-1][k])
		#	print('Temperatura de saída quente no estagio')
		#	print(Thkf[chot-1][k])
		#	print('Temperatura de entrada fria no estagio')
		#	print(Tcki[ccold-1][k])
		#	print('Temperatura de saída fria no estagio')
		#	print(Tckf[ccold-1][k])
		#	print()

	#	for sk in range(nsk):
	#		print('SUB-ESTÁGIO ', sk+1)
	#		print('Temperatura de entrada quente')
	#		print(Thski[chot-1][sbhot-1][sk][k])
	#		print('Temperatura de saída quente')
	#		print(Thskf[chot-1][sbhot-1][sk][k])
	#		print('Temperatura de entrada fria')
	#		print(Tcski[ccold-1][sbcold-1][sk][k])
	#		print('Temperatura de saída fria')
	#		print(Tcskf[ccold-1][sbcold-1][sk][k])
	#		print()

	if Fharr[estagio-1][chot-1][sestagio-1] == 0:
		fracao_quente = 1
	if Fharr[estagio-1][ccold-1][sestagio-1] == 0:
		fracao_fria = 1


	calor_atual_quente[chot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
	calor_atual_frio[ccold-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

	temp_quente = float('{:.1f}'.format(Thskf[chot-1][sbhot-1][sestagio-1][estagio-1]))
	temp_fria = float('{:.1f}'.format(Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1]))
	temperatura_atual_quente[chot-1] = float('{:.1f}'.format(temperatura_atual_quente[chot-1]))
	temperatura_atual_fria[ccold-1] = float('{:.1f}'.format(temperatura_atual_fria[ccold-1]))
	calor_atual_quente[chot-1] = float('{:.1f}'.format(calor_atual_quente[chot-1]))
	calor_atual_frio[ccold-1] = float('{:.1f}'.format(calor_atual_frio[ccold-1]))

	linha_interface.append([chot,
							ccold,
							sbhot,
							sbcold,
							sestagio,
							estagio,
							Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1],
							temp_quente,
							temp_fria,
							fracao_quente,
							fracao_fria])

	for trocador in linha_interface:
		trocador[7] = float('{:.1f}'.format(Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]))
		trocador[8] = float('{:.1f}'.format(Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]))


	return linha_interface

def remover_trocador(vetor, indice, linha_interface):
	estagio = vetor[5]
	sestagio = vetor[4]
	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]

	if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] == 0:
		print('Não há trocador nessa posição!')
		input()

	adicao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0

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

	#CÁLCULO DA SUPERESTRUTURA
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
								Thout[i][si][j][sj][sk][k] = Thin[i][si][j][sj][sk][k] + (Q[i][si][j][sj][sk][k]/(CPh[i]*(Fharr[k][i][si]/100)))
								temperatura_atual_quente[i] = Thout[i][si][j][sj][sk][k]

								Think[i][si][j][sj][sk][k] = Thki[i][k]
								Thoutk[i][si][j][sj][sk][k] = Think[i][si][j][sj][sk][k] + (Qestagioq[i][k]/CPh[i])

								Tcin[i][si][j][sj][sk][k] = Tcski[j][sj][sk][k]
								Tcout[i][si][j][sj][sk][k] = Tcin[i][si][j][sj][sk][k] + (Q[i][si][j][sj][sk][k]/(CPc[j]*(Fcarr[k][j][sj]/100)))
								temperatura_atual_fria[j] = Tcout[i][si][j][sj][sk][k]

								Tcink[i][si][j][sj][sk][k] = Tcki[j][k]
								Tcoutk[i][si][j][sj][sk][k] = Tcink[i][si][j][sj][sk][k] + (Qestagiof[j][k]/CPc[j])


								Thfinal01[i][si] = Thout[i][si][j][sj][sk][k]
								Tcfinal01[j][sj] = Tcout[i][si][j][sj][sk][k]
								Thfinal01k[i][k] = Thoutk[i][si][j][sj][sk][k]
								Tcfinal01k[j][k] = Tcoutk[i][si][j][sj][sk][k]

								#Temperatura inicial de estágios e sub-estágios
								for k1 in range(nstages):
									for sk1 in range(nsk):
										if k1 < (k):
											Tcki[j][k1] = Tcfinal01k[j][k]
											Tcski[j][sj][sk1][k1] = Tcfinal01k[j][k]
											Thki[i][k1] = Thfinal01k[i][k]
											Thski[i][si][sk1][k1] = Thfinal01k[i][k]
										if k1 == (k):
											if sk1 < (sk):
												Tcski[j][sj][sk1][k1] = Tcfinal01[j][sj]
												Thski[i][si][sk1][k1] = Thfinal01[i][si]

										#Temperatura final dos estágios e sub-estágios
								for k1 in range(nstages):
									for sk1 in range(nsk):
										if k1 < (k):
											Tckf[j][k1] = Tcfinal01k[j][k]
											Tcskf[j][sj][sk1][k1] = Tcfinal01k[j][k]
											Thkf[i][k1] = Thfinal01k[i][k]
											Thskf[i][si][sk1][k1] = Thfinal01k[i][k]
										if k1 == (k):
											if sk1 <= (sk):
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

	print()
	for k in range(nstages):
		print('ESTÁGIO ', k+1)
	#	print('Temperatura de entrada quente no estagio')
	#	print(Thki[chot-1][k])
	#	print('Temperatura de entrada fria no estagio')
	#	print(Tcki[ccold-1][k])
	#	print('Temperatura de saída quente no estagio')
	#	print(Thkf[chot-1][k])
	#	print('Temperatura de saída fria no estagio')
	#	print(Tckf[ccold-1][k])
	#	print()

		for sk in range(nsk):
			print('SUB-ESTÁGIO ', sk+1)
			print('Temperatura de entrada quente')
			print(Thski[chot-1][sbhot-1][sk][k])
			print('Temperatura de entrada fria')
			print(Tcski[ccold-1][sbcold-1][sk][k])
	#		print('Temperatura de saída fria')
	#		print(Tcskf[ccold-1][sbcold-1][sk][k])
	#		print('Temperatura de saída quente')
	#		print(Thskf[chot-1][sbhot-1][sk][k])
			print()

	if Fharr[estagio-1][chot-1][sestagio-1] == 0:
		fracao_quente = 1
	if Fharr[estagio-1][ccold-1][sestagio-1] == 0:
		fracao_fria = 1

	if len(linha_interface) == 0:
		temperatura_atual_quente[chot-1] = pinchq
		temperatura_atual_fria[ccold-1] = pinchf

	Thski[chot-1][sbhot-1][sestagio-1][estagio-1] = float('{:.1f}'.format(Thski[chot-1][sbhot-1][sestagio-1][estagio-1]))
	Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1] = float('{:.1f}'.format(Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1]))
	temperatura_atual_quente[chot-1] = float('{:.1f}'.format(temperatura_atual_quente[chot-1]))
	temperatura_atual_fria[ccold-1] = float('{:.1f}'.format(temperatura_atual_fria[ccold-1]))
	calor_atual_quente[chot-1] = float('{:.1f}'.format(calor_atual_quente[chot-1]))
	calor_atual_frio[ccold-1] = float('{:.1f}'.format(calor_atual_frio[ccold-1]))

	try:
		linha_interface.pop(indice)
	except:
		print("num acho")  #fazer a caixinha de erro nao foi achaaaado trocadorrrr

	return linha_interface

def atualizar_matriz(matriz):
	for trocador in matriz:
		trocador[7] = float('{:.1f}'.format(Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]))
		trocador[8] = float('{:.1f}'.format(Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]))

def adicionar_utilidade():
	ccoldutil = int(input('Qual corrente fria recebe utilidade? '))
	Qutilcold[ccoldutil-1] = Qtotalc0[ccoldutil-1][0][0]					#estabelece um calor arbitrário pra comparar depois
	for sj in range(nhot):
		for k in range(nstages):											#ve qual o maior calor de todas as sj e estagios
			if Qutilcold[ccoldutil-1] < Qtotalc0[ccoldutil-1][sj][k]:		#e faz com que o calor util seja igual a esse
				Qutilcold[ccoldutil-1] = Qtotalc0[ccoldutil-1][sj][k]
			Qtotalc0[ccoldutil-1][sj][k] = 0								#remove o calor que tinha na posição pq ele foi suprido
	Tcfinal0[ccoldutil-1] = Tcf[ccoldutil-1]								#temperatura final é atingida
	print('Quantidade de Calor no Aquecedor: ', Qutilcold[ccoldutil-1])


for i in CPh:
	somaCPh += i

for j in CPc:
	somaCPc += j

for i in range(nhot):
	compq = Thf[i] - pinchq
	complistq.append(compq)

for j in range(ncold):
	compf = Tc0[j] - pinchf
	complistf.append(compf)

for i in complistq:
	if i == 0:
		nhotc += 1

for j in complistf:
	if j == 0:
		ncoldc += 1

while nhotc > ncoldc or somaCPh >= somaCPc:
	print('Erro')
	if somaCPh >= somaCPc:
		sys.exit('A somatória dos CPs das correntes quentes é maior que a somatória dos CPs das correntes frias!')

	elif nhotc > ncoldc:
		divop = str(input('A quantidade de correntes quentes é maior do que a quantidade de correntes frias. Você gostaria de dividir correntes? ')).strip().upper()[0]
		if divop == 'Y':
			divtype = input("Deseja dividir correntes quentes, frias ou ambas? ").strip().upper()[0]
			estagio = int(input('Em qual estágio ocorrerá a divisão? '))
			divisao_de_correntes()
		else:
			break
