from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys

Th0 = [150, 150]
map(float, Th0)
Thf = [40, 40]
map(float, Thf)
CPh = [20, 40]
map(float, CPh)

Tc0 = [60, 30]
map(float, Tc0)
Tcf = [140, 130]
map(float, Tcf)
CPc = [30, 22]
map(float, CPc)
Thk = []

dTmin = 10
nhot = 2
ncold = 2
complistq = []
complistf = []
pinchf = 140
pinchq = 150
chot = ccold = sbhot = sbcold = opcao = qsi = qsj = tempdif = ncoldc = nhotc = compq = compf = somaCPh = somaCPc = 0

nsi = [ncold, ncold]
nsj = [nhot, nhot]

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
	Qtotalh1 = CPh[i] * (Th0[i] - Thf[i])
	Qtotalh01.append(Qtotalh1)
	Qtotalh01[i] = float('{:.2f}'.format(Qtotalh01[i]))
for j in range (ncold):
	Qtotalc1 = 0
	Qtotalc1 = CPc[j] * (Tcf[j] - Tc0[j])
	Qtotalc01.append(Qtotalc1)
	Qtotalc01[j] = float('{:.2f}'.format(Qtotalc01[j]))

for i in range(nhot):
	for j in range(ncold):
		Qtotalh0[i][0] = Qtotalh01[i]
		Qtotalc0[j][0] = Qtotalc01[j]

map(float, Qtotalh01)
map(float, Qtotalc01)

nsk = nstages = nhot

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

Fharr = np.array ([0])
Fharr.resize(nstages, nhot, ncold)
Fcarr = np.array ([0])
Fcarr.resize(nstages, ncold, nhot)
Qarr = np.array ([0])
Qarr.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Q[i][si][j][sj][sk][k]
Q = Qarr.tolist()
map(float, Q)

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

def linha():
	#('-'*42)

def divisao_de_correntes():
	global nhotc, ncoldc
	divtype = input("Deseja dividir correntes quentes, frias ou ambas? ").strip().upper()[0]

	if divtype == 'A':
		estagio = int(input('Em qual estágio ocorrerá a divisão? '))
		chot = int(input('Qual corrente quente será dividida? '))
		qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? '))
		while qsi > nsi[chot-1]:
			#('Erro! O número de divisões é muito grande.')
			qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? '))
		if qsi <= nsi[chot-1]:
			for i in range(qsi):
				Fharr[estagio-1][chot-1][i] = float(input(f'Qual a fração da sub-corrente quente {i+1}? '))
				Qtotalh0[chot-1][i] = Qtotalh01[chot-1]*(Fharr[estagio-1][chot-1][i]/100)
				#(Qtotalh0)
		ccold = int(input('Qual corrente fria será dividida? '))
		qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? '))
		while qsj > nsj[ccold-1]:
			#('Erro! O número de divisões é muito grande.')
			qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? '))
		if qsj <= nsj[ccold-1]:
			for j in range(qsj):
				Fcarr[estagio-1][ccold-1][j] = float(input(f'Qual a fração da sub-corrente quente {j+1}? '))
				Qtotalc0[ccold-1][j] = Qtotalc01[ccold-1]*(Fcarr[estagio-1][ccold-1][j]/100)
				#(Qtotalc0)
		nhotc = qsi + (nhot - 1)
		ncoldc = qsj + (ncold - 1)
		#(nhotc)
		#(ncoldc)
		#(Fharr)
		#(Fcarr)

	if divtype == 'Q':
		estagio = int(input('Em qual estágio ocorrerá a divisão? '))
		chot = int(input('Qual corrente quente será dividida? '))
		qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? '))
		while qsi > nsi[chot-1]:
			#('Erro! O número de divisões é muito grande.')
			qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? '))
		if qsi <= nsi[chot-1]:
			for i in range(qsi):
				Fharr[estagio-1][chot-1][i] = float(input(f'Qual a fração da sub-corrente quente {i+1}? '))
				Qtotalh0[chot-1][i] = Qtotalh01[chot-1]*(Fharr[estagio-1][chot-1][i]/100)
				#(Qtotalh0)
		nhotc = qsi + (nhot - 1)
		#(nhotc)
		#(Fharr)

	if divtype == 'F':
		estagio = int(input('Em qual estágio ocorrerá a divisão? '))
		ccold = int(input('Qual corrente fria será dividida? '))
		qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? '))
		while qsj > nsj[ccold-1]:
			#('Erro! O número de divisões é muito grande.')
			qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? '))
		if qsj <= nsj[ccold-1]:
			for j in range(qsj):
				Fcarr[estagio-1][ccold-1][j] = float(input(f'Qual a fração da sub-corrente quente {j+1}? '))
				Qtotalc0[ccold-1][j] = Qtotalc01[ccold-1]*(Fcarr[estagio-1][ccold-1][j]/100)
				#(Qtotalc0)
		ncoldc = qsj + (ncold - 1)
		#(ncoldc)
		#(Fcarr)


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
#(nhotc)

for j in complistf:
	if j == 0:
		ncoldc += 1
#(ncoldc)

while ncoldc > nhotc or somaCPc >= somaCPh:
	#('Erro')
	if ncoldc > nhotc:
		#('Você deve dividir correntes quentes!')
		divisao_de_correntes()

	elif somaCPc >= somaCPh:
		sys.exit('A somatória dos CPs das correntes frias é maior que a somatória dos CPs das correntes quentes!')

#('Temperatura Entrada Quente')
#(Th0)
#('Temperatura Final Quente')
#(Thf)
#('Temperatura Entrada Fria')
#(Tcf)
#('Temperatura Final Fria')
#(Tc0)
#('Calor Disponível Quentes:')
#(Qtotalh0)
#('Calor Disponível Frias:')
#(Qtotalc0)

while opcao != 5:
	linha()
	#('{:^42}'.format('MENU DE OPÇÕES'))
	linha()
	#('1 - Consultar correntes')
	#('2 - Dividir correntes')
	#('3 - Inserir trocador de calor')
	#('4 - Inserir utilidades')
	#('5 - Sair')
	linha()
	opcao = int(input('Qual opção você deseja? '))
	#()

	if opcao == 1:
		linha()
		#('CONSULTA DE CORRENTES')
		linha()
		#('Temperatura Entrada Quente')
		#(Thf)
		#('Temperatura Final Quente')
		#(Th0)
		#('Temperatura Entrada Fria')
		#(Tc0)
		#('Temperatura Final Fria')
		#(Tcf)
		#('Calor Disponível Quentes:')
		#(Qtotalh0)
		#('Calor Disponível Frias:')
		#(Qtotalc0)


	elif opcao == 2:
		divisao_de_correntes()

	elif opcao == 3:

		estagio = int(input('Em qual estágio ocorrerá a troca? '))
		sestagio = int(input('Em qual sub-estágio ocorrerá a troca? '))
		chot = int(input('Qual corrente quente trocará calor? '))
		ccold = int(input('Qual corrente fria trocará calor? '))

		if Fharr[estagio-1][chot-1].any() == False and Fcarr[estagio-1][ccold-1].any() == False:
			sbhot = sbcold = 1

		elif Fharr[estagio-1][chot-1].any() == False and Fcarr[estagio-1][ccold-1].any() == True:
			sbcold = int(input('Qual sub-corrente fria trocará calor? '))
			sbhot = 1

		elif Fharr[estagio-1][chot-1].any() == True and Fcarr[estagio-1][ccold-1].any() == False:
			sbhot = int(input('Qual sub-corrente quente trocará calor? '))
			sbcold = 1

		elif Fharr[estagio-1][chot-1].any() == True and Fcarr[estagio-1][ccold-1].any() == True:
			sbhot = int(input('Qual sub-corrente quente trocará calor? '))
			sbcold = int(input('Qual sub-corrente fria trocará calor? '))

		if Fharr[estagio-1][chot-1][sbhot-1] == 0:
			Fharr[estagio-1][chot-1][sbhot-1] = 100
		if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
			Fcarr[estagio-1][ccold-1][sbcold-1] = 100

		if ((Qtotalh0[chot-1][sbhot-1]) > (Qtotalc0[ccold-1][sbcold-1])):
			#('Calor Máximo a ser trocado: ', Qtotalc0[ccold-1][sbcold-1])
			Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1]
		else:
			#('Calor Máximo a ser trocado: ', Qtotalh0[chot-1][sbhot-1])
			Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalh0[chot-1][sbhot-1]
		trocamax = input('Deseja trocar o calor Máximo? ').strip().upper()[0]
		if trocamax == 'N':
			Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = float(input('Quanto calor será trocado: '))

		Thin[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Thski[chot-1][sbhot-1][sestagio-1][estagio-1]
		Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Thski[chot-1][sbhot-1][sestagio-1][estagio-1] - (Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] / (CPh[chot-1]*(Fharr[estagio-1][chot-1][sbhot-1]/100)))
		#(Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1])
		Tcin[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1]
		Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1] - (Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] / (CPc[ccold-1]*(Fcarr[estagio-1][ccold-1][sbcold-1]/100)))
		#(Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1])
		tempdif = (Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] - Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1])
		if tempdif < 0:
			tempdif = - tempdif
		if tempdif >= dTmin:
			Thfinal01[chot-1][sbhot-1] = Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
			Tcfinal01[ccold-1][sbcold-1] = Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

            #Temperatura inicial de estágios e sub-estágios
			for k in range(nstages):
				for sk in range(nsk):
					if k > (estagio-1):
						Thki[chot-1][k] = Thfinal01[chot-1][sbhot-1]
						Thski[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]
						Tcki[ccold-1][k] = Tcfinal01[ccold-1][sbcold-1]
						Tcski[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]
					if k == (estagio-1):
						if sk > (sestagio-1):
							Thski[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]
							Tcski[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]

		  	#Temperatura final dos estágios e sub-estágios
			for k in range(nstages):
				for sk in range(nsk):
					if k > (estagio-1):
						Thkf[chot-1][k] = Thfinal01[chot-1][sbhot-1]
						Thskf[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]
						Tckf[ccold-1][k] = Tcfinal01[ccold-1][sbcold-1]
						Tcskf[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]
					if k == (estagio-1):
						if sk >= (sestagio-1):
							Thskf[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]
							Tcskf[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]
						Tckf[ccold-1][k] = Tcfinal01[ccold-1][sbcold-1]
						Thkf[chot-1][k] = Thfinal01[chot-1][sbhot-1]


			Qtotalh0[chot-1][sbhot-1] = Qtotalh0[chot-1][sbhot-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
			Qtotalc0[ccold-1][sbcold-1]= Qtotalc0[ccold-1][sbcold-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]



			#()
			for k in range(nstages):
				#('ESTÁGIO ', k+1)
				for sk in range(nsk):
					#('SUB-ESTÁGIO ', sk+1)
					#('Temperatura de entrada fria')
					#(Tcski[ccold-1][sbcold-1][sk][k])
					#('Temperatura de entrada quente')
					#(Thski[chot-1][sbhot-1][sk][k])
					#('Temperatura de saída fria')
					#(Tcskf[ccold-1][sbcold-1][sk][k])
					#('Temperatura de saída quente')
					#(Thskf[chot-1][sbhot-1][sk][k])
					#()

		else:
			#('Erro! A diferença mínima de temperatura não está sendo respeitada.')

		if Fharr[estagio-1][chot-1][sbhot-1] == 100:
			Fharr[estagio-1][chot-1][sbhot-1] = 0
		if Fcarr[estagio-1][ccold-1][sbcold-1] == 100:
			Fcarr[estagio-1][ccold-1][sbcold-1] = 0

	elif opcao == 4:
		chotutil = int(input('Qual corrente quente recebe utilidade? '))
		Qtotalh01[chotutil-1] = 0
		Qtotalh0[chotutil-1] = 0
		Thfinal0[chotutil-1] = Thf[chotutil-1]
