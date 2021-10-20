from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys

def acima():

	Th0 = [180, 180]                      #Puxar da planilha as correntes
	map(float, Th0)
	Thf = [150, 150]
	map(float, Thf) 
	CPh = [20, 2]
	map(float, CPh)

	Tc0 = [140]
	map(float, Tc0) 
	Tcf = [180]
	map(float, Tcf)
	CPc = [30]
	map(float, CPc)
	Thk = [] 

	divop = ''
	dTmin = 10
	nhot = 2
	ncold = 2
	pinchq = 150
	pinchf = 140  #puxar do pinch calcuulado, como fazer isso? buscar no maisrecenteMpinch
	complistq = []
	complistf = []
	chot = ccold = sbhot = sbcold = opcao = qsi = qsj = tempdif = nhotc = ncoldc = compq = compf = somaCPh = somaCPc = 0

	nsi = [ncold, ncold] #listas: []
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
		Qtotalh1 = CPh[i] * (Th0[i] - Thf[i]) #resulta em um número
		Qtotalh01.append(Qtotalh1)         #append coloca o número na lista    #lista com todos os calores das correntes quentes
		Qtotalh01[i] = float('{:.2f}'.format(Qtotalh01[i]))  #formata variável: float com 2 casas após vírgula
	for j in range (ncold):
		Qtotalc1 = 0
		Qtotalc1 = CPc[j] * (Tcf[j] - Tc0[j])
		Qtotalc01.append(Qtotalc1)
		Qtotalc01[j] = float('{:.2f}'.format(Qtotalc01[j]))
		
	for i in range(nhot):
		for j in range(ncold):
			Qtotalh0[i][0] = Qtotalh01[i]   #[j][0] pq é variável de duas dimensões
			Qtotalc0[j][0] = Qtotalc01[j]

	map(float, Qtotalh01) #transforma pra float
	map(float, Qtotalc01)

	if nhot >= ncold:
		nsk = nstages = ncold   #pode deixar nstages = 3
	else:
		nsk = nstages = ncold

	Thskiarr = np.array ([0])                    #quando tem sk é substagio, k é estágio
	Thskiarr.resize(nhot, ncold, nsk, nstages)
	Thski = Thskiarr.tolist()    #converte matriz pra lista
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
	Fharr.resize(nstages, nhot, ncold) #fração e´a mesma do estágio inteiro
	Fcarr = np.array ([0])
	Fcarr.resize(nstages, ncold, nhot)
	Qarr = np.array ([0])
	Qarr.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Q[i][si][j][sj][sk][k]
	Q = Qarr.tolist()      #calor a ser trocado em cada trocador
	map(float, Q)	


	for i in range (nhot):
		#Este loop iguala as temperaturas iniciais de todos os SUB-ESTÁGIOS à temperatura inicial da corrente 
		for si in range (ncold):
			for sk in range (nsk):
				for k in range (nstages):
					Thski[i][si][sk][k] = Thf[i]   #temperatura do pinch
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
			Tcki[j][k] = Tc0[j] #temperatura do pinch
			Tckf[j][k] = Tc0[j]

	def linha():
		print('-'*42)

	def divisao_de_correntes():
		global nhotc, ncoldc

		divtype = input("Deseja dividir correntes quentes, frias ou ambas? ").strip().upper()[0]    #Ambas nao tem na interface
				                                                                                   
		if divtype == 'A':
			estagio = int(input('Em qual estágio ocorrerá a divisão? ')) #stage 1a janela
			chot = int(input('Qual corrente quente será dividida? ')) #hot stream 1a janela
			qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? ')) # split 1a janela
			while qsi > nsi[chot-1]:
				print('Erro! O número de divisões é muito grande.') 
				qsi = int(input('Em quantas sub-correntes quentes essa corrente irá se dividir? '))
			if qsi <= nsi[chot-1]:
				for i in range(qsi):
					Fharr[estagio-1][chot-1][i] = float(input(f'Qual a fração da sub-corrente quente {i+1}? ')) #Fharr = 2a janela, frações sub quentes
					Qtotalh0[chot-1][i] = Qtotalh01[chot-1]*(Fharr[estagio-1][chot-1][i]/100)
					print(Qtotalh0)
			ccold = int(input('Qual corrente fria será dividida? ')) #cold stream 1a janela
			qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? ')) #stage 1a janela
			while qsj > nsj[ccold-1]:
				print('Erro! O número de divisões é muito grande.')
				qsj = int(input('Em quantas sub-correntes frias essa corrente irá se dividir? ')) #split 1a janela
			if qsj <= nsj[ccold-1]:
				for j in range(qsj):
					Fcarr[estagio-1][ccold-1][j] = float(input(f'Qual a fração da sub-corrente quente {j+1}? ')) #Fcarr = 2a janela, frações sub frias
					Qtotalc0[ccold-1][j] = Qtotalc01[ccold-1]*(Fcarr[estagio-1][ccold-1][j]/100)
					print(Qtotalc0)
			nhotc = qsi + (nhot - 1)
			ncoldc = qsj + (ncold - 1)
			print(nhotc)
			print(ncoldc)
			print(Fharr)
			print(Fcarr)
		


		def divisao_quente(estagio,chot,qsi,fracao_quente):   # if divtype == 'Q'
			while qsi > nsi[chot-1]:
				print('Erro! O número de divisões é muito grande.')                    #se numero de divisões for maior, aparecer uma janela de erro
				qsi = int(float(dlg.divisaotrocador3.comboBox_2.currentText()))        #aí o usuário tem que entrar dnv com o número de divisões
			if qsi <= nsi[chot-1]:
				for i in range(qsi):
					Fharr[estagio-1][chot-1][i] = float(fracao_quente)
					Qtotalh0[chot-1][i] = Qtotalh01[chot-1]*(Fharr[estagio-1][chot-1][i]/100)
					print(Qtotalh0)
			nhotc = qsi + (nhot - 1) 
			print(nhotc)
			print(Fharr)

		def divisao_fria(estagio,ccold,qsj,fracao_fria):     #if divtype == 'F'
			while qsj > nsj[ccold-1]:
				print('Erro! O número de divisões é muito grande.')
				qsj = int(float(dlg.divisaotrocador.comboBox_2.currentText()))
			if qsj <= nsj[ccold-1]:
				for j in range(qsj):
					Fcarr[estagio-1][ccold-1][j] = float(fracao_fria)
					Qtotalc0[ccold-1][j] = Qtotalc01[ccold-1]*(Fcarr[estagio-1][ccold-1][j]/100)
					print(Qtotalc0)
			ncoldc = qsj + (ncold - 1)
			print(ncoldc)
			print(Fcarr)


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
	print(nhotc)

	for j in complistf:
		if j == 0:
			ncoldc += 1
	print(ncoldc)

	while nhotc > ncoldc or somaCPh >= somaCPc:
		print('Erro')
		if somaCPh >= somaCPc:
			sys.exit('A somatória dos CPs das correntes quentes é maior que a somatória dos CPs das correntes frias!')

		elif nhotc > ncoldc:
			divop = str(input('A quantidade de correntes quentes é maior do que a quantidade de correntes frias. Você gostaria de dividir correntes? ')).strip().upper()[0]
			if divop == 'Y':
				divisao_de_correntes()                   #criar janela de erro aqui
			else:
				break

	print('Temperatura Entrada Quente')
	print(Thf)
	print('Temperatura Final Quente')
	print(Th0)
	print('Temperatura Entrada Fria')
	print(Tc0)
	print('Temperatura Final Fria')
	print(Tcf)
	print('Calor Disponível Quentes:')
	print(Qtotalh0)
	print('Calor Disponível Frias:')
	print(Qtotalc0)

	while opcao != 5:
		linha()
		print('{:^42}'.format('MENU DE OPÇÕES'))
		linha()
		print('1 - Consultar correntes')
		print('2 - Dividir correntes')
		print('3 - Inserir trocador de calor')
		print('4 - Inserir utilidades')
		print('5 - Sair')
		linha()
		opcao = int(input('Qual opção você deseja? '))
		print()

		if opcao == 1:
			linha()
			print('CONSULTA DE CORRENTES')
			linha()
			print('Temperatura Entrada Quente')
			print(Thf)
			print('Temperatura Final Quente')
			print(Th0)
			print('Temperatura Entrada Fria')
			print(Tc0)
			print('Temperatura Final Fria')
			print(Tcf)
			print('Calor Disponível Quentes:')
			print(Qtotalh0)
			print('Calor Disponível Frias:')
			print(Qtotalc0)


		elif opcao == 2:
			divisao_de_correntes()


		elif opcao == 3:

			estagio = int(float(dlg.comboBox_8.currentText()))
			sestagio = int(float(dlg.comboBox_7.currentText()))
			chot = int(float(dlg.comboBox_2.currentText()))
			ccold = int(float(dlg.comboBox_5.currentText()))

			if Fharr[estagio-1][chot-1].any() == False and Fcarr[estagio-1][ccold-1].any() == False: # testa se houve divisão das corrente
				sbhot = sbcold = 1   #se corrente fria e corrente quente nao tiver dividida, quem troca é a corrente normal

			elif Fharr[estagio-1][chot-1].any() == False and Fcarr[estagio-1][ccold-1].any() == True:
				sbcold = int(input('Qual sub-corrente fria trocará calor? '))                     #aqui fazer hot stream 1.1, 2.3 etc, alinhar corrente com subcorrente
				sbhot = 1

			elif Fharr[estagio-1][chot-1].any() == True and Fcarr[estagio-1][ccold-1].any() == False:
				sbhot = int(input('Qual sub-corrente quente trocará calor? '))                       #colocar na interface subhot e coldstream
				sbcold = 1
					
			elif Fharr[estagio-1][chot-1].any() == True and Fcarr[estagio-1][ccold-1].any() == True:
				sbhot = int(input('Qual sub-corrente quente trocará calor? '))
				sbcold = int(input('Qual sub-corrente fria trocará calor? '))

			if Fharr[estagio-1][chot-1][sbhot-1] == 0: 
				Fharr[estagio-1][chot-1][sbhot-1] = 100  #se não tá dividido, a fração é 100
			if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
				Fcarr[estagio-1][ccold-1][sbcold-1] = 100

			if ((Qtotalh0[chot-1][sbhot-1]) > (Qtotalc0[ccold-1][sbcold-1])):
				#ve qual corrente, fria ou quente, é o maior calor
				print('Calor Máximo a ser trocado: ', Qtotalc0[ccold-1][sbcold-1])
				Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1]
			else:
				print('Calor Máximo a ser trocado: ', Qtotalh0[chot-1][sbhot-1])
				Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalh0[chot-1][sbhot-1]
			trocamax = input('Deseja trocar o calor Máximo? ').strip().upper()[0]

				#Q é o calor que EFETIVAMENTE vai ser trocado

			if trocamax == 'N':
				Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = float(input('Quanto calor será trocado: ')) #heatload

			Thin[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Thski[chot-1][sbhot-1][sestagio-1][estagio-1]
			Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Thski[chot-1][sbhot-1][sestagio-1][estagio-1] + (Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] / (CPh[chot-1]*(Fharr[estagio-1][chot-1][sbhot-1]/100)))
			print(Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1])
			Tcin[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1]
			Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1] + (Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] / (CPc[ccold-1]*(Fcarr[estagio-1][ccold-1][sbcold-1]/100)))
			print(Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1])
			tempdif = (Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] - Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1])
			
			#temperaturas de entrada e saída do trocador

			if tempdif < 0:
				tempdif = - tempdif
			if tempdif >= dTmin:
				Thfinal01[chot-1][sbhot-1] = Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				Tcfinal01[ccold-1][sbcold-1] = Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
	                   
	            #Temperatura inicial de estágios e sub-estágios
				for k in range(nstages):
					for sk in range(nsk):
						if k < (estagio-1):
							Tcki[ccold-1][k] = Tcfinal01[ccold-1][sbcold-1]
							Tcski[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]
							Thki[chot-1][k] = Thfinal01[chot-1][sbhot-1]
							Thski[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]								
						if k == (estagio-1):
							if sk < (sestagio-1):
								Tcski[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]
								Thski[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]

			    #Temperatura final dos estágios e sub-estágios
				for k in range(nstages):
					for sk in range(nsk):
						if k < (estagio-1):
							Tckf[ccold-1][k] = Tcfinal01[ccold-1][sbcold-1]
							Tcskf[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]
							Thkf[chot-1][k] = Thfinal01[chot-1][sbhot-1]
							Thskf[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]
						if k == (estagio-1):
							if sk <= (sestagio-1):
								Tcskf[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]
								Thskf[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]
							Tckf[ccold-1][k] = Tcfinal01[ccold-1][sbcold-1]
							Thkf[chot-1][k] = Thfinal01[chot-1][sbhot-1]

				Qtotalh0[chot-1][sbhot-1] = Qtotalh0[chot-1][sbhot-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				Qtotalc0[ccold-1][sbcold-1]= Qtotalc0[ccold-1][sbcold-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

					

				print()
				for k in range(nstages):
					print('ESTÁGIO ', k+1)
					for sk in range(nsk):
						print('SUB-ESTÁGIO ', sk+1)
						print('Temperatura de entrada fria')
						print(Tcski[ccold-1][sbcold-1][sk][k])
						print('Temperatura de entrada quente')
						print(Thski[chot-1][sbhot-1][sk][k])
						print('Temperatura de saída fria')
						print(Tcskf[ccold-1][sbcold-1][sk][k])
						print('Temperatura de saída quente')
						print(Thskf[chot-1][sbhot-1][sk][k])
						print()

			else:
				print('Erro! A diferença mínima de temperatura não está sendo respeitada.') #janela de erro

			if Fharr[estagio-1][chot-1][sbhot-1] == 100: 
				Fharr[estagio-1][chot-1][sbhot-1] = 0
			if Fcarr[estagio-1][ccold-1][sbcold-1] == 100:
				Fcarr[estagio-1][ccold-1][sbcold-1] = 0
		
		elif opcao == 4:
			ccoldutil = int(float(dlg.comboBox_43.currentText())) #corrente da utilidade, fazer um connect clicked do add cold
			Qtotalc01[ccoldutil-1] = 0
			Qtotalc0[ccoldutil-1] = 0
			Tcfinal0[ccoldutil-1] = Tcf[ccoldutil-1]
acima()