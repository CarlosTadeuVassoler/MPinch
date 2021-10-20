from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

Th0 = []
Thf = []
CPh = []
Thm = []

Tc0 = []
Tcf = []
CPc = []
Thk = []
Tcm = []

dTmin = 10.2
nhot = 2
ncold = 2

chot=int(dlg.comboBox_35.currentText())
ccold=int(dlg.comboBox_36.currentText())
divisao="yes"

for i in range(n):
		if correntes[i][3] == "Hot":
			Thm.append(float(dlg.tableWidget_15.item(i,1).text()))
			Th0.append(correntes[i][0])
			Thf.append(pinchq)
			CPh.append(correntes[i][2])
	j=0
	for i in range(n):
		if correntes[i][3] == "Cold":
			Tc0.append(pinchf)
			Tcf.append(correntes[i][1])
			CPc.append(correntes[i][2])
			Tcm.append(float(dlg.tableWidget_17.item(j,1).text())) #tablewidget
			j=j+1

	if str(dlg.comboBox_37.currentText())!="do not split stream":
		sbhot=float(dlg.comboBox_37.currentText())
	if str(dlg.comboBox_38.currentText())!="do not split stream":
		sbcold=float(dlg.comboBox_38.currentText())
	if str(dlg.comboBox_38.currentText())=="do not split stream" and str(dlg.comboBox_37.currentText())=="do not split stream":
		divisao="no"

if ncold > nhot:
	#("Error")

else:
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
		Qtotalh01[i] = float("{:.2f}".format(Qtotalh01[i]))
	for j in range (ncold):
		Qtotalc1 = 0
		Qtotalc1 = CPc[j] * (Tcf[j] - Tc0[j])
		Qtotalc01.append(Qtotalc1)
		Qtotalc01[j] = float("{:.2f}".format(Qtotalc01[j]))

	nsi = [ncold, ncold] #número de divisões por corrente quente
	nsj = [nhot, nhot] #número de divisões por corrente fria

	for i in range(nhot):
		for j in range(ncold):
			Qtotalh0[i][0] = Qtotalh01[i]
			Qtotalc0[j][0] = Qtotalc01[j]

	map(float, Qtotalh01)
	map(float, Qtotalc01)
	#("Temperatura Entrada Quente")
	#(Th0)
	#("Temperatura Final Quente")
	#(Thf)
	#("Temperatura Entrada Fria")
	#(Tcf)
	#("Temperatura Final Fria")
	#(Tc0)
	#("Calor Disponível Quentes:")
	#(Qtotalh01)
	#("Calor Disponível Frias:")
	#(Qtotalc01)

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

	#Igualando as temperaturas de Estágios e Sub-estágios

	for i in range (nhot):
		#Este loop iguala as temperaturas iniciais de todos os SUB-ESTÁGIOS à temperatura inicial da corrente
		for si in range (nsi[i]):
			for sk in range (nsk):
				for k in range (nstages):
					Thski[i][si][sk][k] = Th0[i]
					Thskf[i][si][sk][k] = Th0[i]
		#Este loop iguala as temperaturas iniciais de todos os ESTÁGIOS à temperatura inicial da corrente
		for k in range (nstages):
			Thki[i][k] = Th0[i]
			Thkf[i][k] = Th0[i] #Thk é a temperatura inicial do estágio

	for j in range (ncold):
		for sj in range (nsj[j]):
			for sk in range(nsk-1, -1, -1):
				for k in range(nstages-1, -1, -1):
					Tcski[j][sj][sk][k] = Tc0[j]
					Tcskf[j][sj][sk][k] = Tc0[j]
		for k in range (nstages-1, -1, -1):
			Tcki[j][k] = Tc0[j]
			Tckf[j][k] = Tc0[j]

	Qarr = np.array ([0])
	Qarr.resize(nhot, ncold, ncold, nhot, nsk, nstages)  #Q[i][si][j][sj][sk][k]
	Q = Qarr.tolist()
	map(float, Q)
	Fharr = np.array ([0])
	Fharr.resize(nhot, ncold, nsk, nstages)  #Fh[i][si][sk][k]
	Fh = Fharr.tolist()
	map(float, Fh)
	Fcarr = np.array ([0])
	Fcarr.resize(ncold, nhot, nsk, nstages)  #Fc[j][sj][sk][k]
	Fc = Fcarr.tolist()
	map(float, Fc)
	fim = 'Y'
	deseja = 'Y'
	chot=0
	ccold=0
	sbhot=0
	sbcold=0

	while fim != 'N':

		if fim == 'U':
			ccoldutil = int(input("Qual corrente fria recebe utilidade: "))
			Qtotalc01[ccoldutil-1] = 0
			Tcfinal0[ccoldutil-1] = Tcf[ccoldutil-1]

		else:
			divisao.strip().upper()[0]
			if(divisao == 'Y'):
				if str(dlg.comboBox_37.currentText())!="do not split stream":
					divtype="Q"
				if str(dlg.comboBox_38.currentText())!="do not split stream":
					divtype="F"
				if str(dlg.comboBox_38.currentText())!="do not split stream" and str(dlg.comboBox_37.currentText())!="do not split stream":
					divtype="A"

				if divtype == 'A':
					estagio = int(float(dlg.comboBox_40.currentText()))
					sestagio = int(float(dlg.comboBox_39.currentText()))
					if(Fh[chot-1][sbhot-1][sestagio-1][estagio-1]==0):
						Fh[chot-1][sbhot-1][sestagio-1][estagio-1] = float((dlg.lineEdit_23.text()))
						Qtotalh0[chot-1][sbhot-1] = Qtotalh01[chot-1]*Fh[chot-1][sbhot-1][sestagio-1][estagio-1]/100
						for i in range(nsi[chot-1]):
							if i != (sbhot-1):
								Fh[chot-1][i][sestagio-1][estagio-1] = 100 - Fh[chot-1][sbhot-1][sestagio-1][estagio-1]
								Qtotalh0[chot-1][i] = Qtotalh01[chot-1]*Fh[chot-1][i][sestagio-1][estagio-1]/100
					if(Fc[ccold-1][sbcold-1][sestagio-1][estagio-1]==0):
						Fc[ccold-1][sbcold-1][sestagio-1][estagio-1] = float(input("Qual a fração da sub corrente fria: "))
						Qtotalc0[ccold-1][sbcold-1] = Qtotalc01[ccold-1]*(Fc[ccold-1][sbcold-1][sestagio-1][estagio-1]/100)
						for j in range(nsj[ccold-1]):
							if j != (sbcold-1):
								Fc[ccold-1][j][sestagio-1][estagio-1] = 100 - Fc[ccold-1][sbcold-1][sestagio-1][estagio-1]
								Qtotalc0[ccold-1][j] = Qtotalc01[ccold-1]*Fc[ccold-1][j][sestagio-1][estagio-1]/100

				if divtype == 'Q':
					sbcold = 1
					estagio = int(float(dlg.comboBox_40.currentText()))
					sestagio = int(float(dlg.comboBox_39.currentText()))
					if(Fh[chot-1][sbhot-1][sestagio-1][estagio-1]==0):
						Fh[chot-1][sbhot-1][sestagio-1][estagio-1] = float((dlg.lineEdit_23.text()))
						Qtotalh0[chot-1][sbhot-1] = Qtotalh01[chot-1]*Fh[chot-1][sbhot-1][sestagio-1][estagio-1]/100
						for i in range(nsi[chot-1]):
							if i != (sbhot-1):
								Fh[chot-1][i][sestagio-1][estagio-1] = 100 - Fh[chot-1][sbhot-1][sestagio-1][estagio-1]
								Qtotalh0[chot-1][i] = Qtotalh01[chot-1]*Fh[chot-1][i][sestagio-1][estagio-1]/100
					if(Fc[ccold-1][sbcold-1][sestagio-1][estagio-1]==0):
						Fc[ccold-1][sbcold-1][sestagio-1][estagio-1] = float(100)
						Qtotalc0[ccold-1][sbcold-1] = Qtotalc01[ccold-1]*Fc[ccold-1][sbcold-1][sestagio-1][estagio-1]/100

				if divtype == 'F':
					sbhot = 1
					estagio = int(float(dlg.comboBox_40.currentText()))
					sestagio = int(float(dlg.comboBox_39.currentText()))
					if(Fh[chot-1][sbhot-1][sestagio-1][estagio-1]==0):
						Fh[chot-1][sbhot-1][sestagio-1][estagio-1] = float(100)
						Qtotalh0[chot-1][sbhot-1] = Qtotalh01[chot-1]*Fh[chot-1][sbhot-1][sestagio-1][estagio-1]/100
					if(Fc[ccold-1][sbcold-1][sestagio-1][estagio-1]==0):
						Fc[ccold-1][sbcold-1][sestagio-1][estagio-1] = float((dlg.lineEdit_24.text()))
						Qtotalc0[ccold-1][sbcold-1] = Qtotalc01[ccold-1]*(Fc[ccold-1][sbcold-1][sestagio-1][estagio-1]/100)
						for j in range(nsj[ccold-1]):
							if j != (sbcold-1):
								Fc[ccold-1][j][sestagio-1][estagio-1] = 100 - Fc[ccold-1][sbcold-1][sestagio-1][estagio-1]
								Qtotalc0[ccold-1][j] = Qtotalc01[ccold-1]*Fc[ccold-1][j][sestagio-1][estagio-1]/100

				if ((Qtotalh0[chot-1][sbhot-1]) > (Qtotalc0[ccold-1][sbcold-1])):
					#("Calor Máximo a ser trocado: ", Qtotalc0[ccold-1][sbcold-1])
					Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1]
				else:
					#("Calor Máximo a ser trocado: ", Qtotalh0[chot-1][sbhot-1])
					Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalh0[chot-1][sbhot-1]
				if dlg.radioButton_20.isChecked() == True:
					trocamax="yes"
				else:
					trocamax="no"
				trocamax.strip().upper()[0]
				if trocamax == 'N':
					Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = float((dlg.lineEdit_25.text()))

			else:
				estagio = int(float(dlg.comboBox_40.currentText()))
				sestagio = int(float(dlg.comboBox_39.currentText()))
				sbhot = 1
				sbcold = 1
				Fh[chot-1][sbhot-1][sestagio-1][estagio-1] = 100
				Fc[ccold-1][sbcold-1][sestagio-1][estagio-1] = 100
				if ((Qtotalh01[chot-1]) > (Qtotalc01[ccold-1])):
					#("Calor Máximo a ser trocado: ", Qtotalc01[ccold-1])
					Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalc01[ccold-1]
				else:
					#("Calor Máximo a ser trocado: ", Qtotalh01[chot-1])
					Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Qtotalh01[chot-1]

				if dlg.radioButton_20.isChecked() == True:
					trocamax="yes"
				else:
					trocamax="no"
				trocamax.strip().upper()[0]
				if trocamax == 'N':
					Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = float(input("Quanto calor será trocado: "))

			if divisao == 'Y':
				#Temperaturas de entrada e saída dos trocadores
				Thin[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Thski[chot-1][sbhot-1][sestagio-1][estagio-1]
				Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Thski[chot-1][sbhot-1][sestagio-1][estagio-1] - (Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] / (CPh[chot-1]*(Fh[chot-1][sbhot-1][sestagio-1][estagio-1]/100)))
				Tcin[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1]
				Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1] + (Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] / (CPc[ccold-1]*(Fc[ccold-1][sbcold-1][sestagio-1][estagio-1]/100)))

				if Thin[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] - Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] >= dTmin:
					Thfinal01[chot-1][sbhot-1] = Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					Tcfinal01[ccold-1][sbcold-1] = Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

                    #Temperatura inicial de estágios e sub-estágios
					for k in range(nstages):
						for sk in range(nsk):
							if k < (estagio-1):
								Tcki[ccold-1][k] = Tcfinal01[ccold-1][sbcold-1]
								Tcski[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]
							if k == (estagio-1):
								if sk < (sestagio-1):
									Tcski[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]

					for k in range(nstages):
						for sk in range(nsk):
							if k > (estagio-1):
								Thki[chot-1][k] = Thfinal01[chot-1][sbhot-1]
								Thski[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]
							if k == (estagio-1):
								if sk > (sestagio-1):
									Thski[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]

					#Temperatura final dos estágios e sub-estágios
					for k in range(nstages):
						for sk in range(nsk):
							if k < (estagio-1):
								Tckf[ccold-1][k] = Tcfinal01[ccold-1][sbcold-1]
								Tcskf[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]
							if k == (estagio-1):
								if sk <= (sestagio-1):
									Tcskf[ccold-1][sbcold-1][sk][k] = Tcfinal01[ccold-1][sbcold-1]
								Tckf[ccold-1][k] = Tcfinal01[ccold-1][sbcold-1]

					for k in range(nstages):
						for sk in range(nsk):
							if k > (estagio-1):
								Thkf[chot-1][k] = Thfinal01[chot-1][sbhot-1]
								Thskf[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]
							if k == (estagio-1):
								if sk >= (sestagio-1):
									Thskf[chot-1][sbhot-1][sk][k] = Thfinal01[chot-1][sbhot-1]
								Thkf[chot-1][k] = Thfinal01[chot-1][sbhot-1]
 				else:
 					dlg.conv=uic.loadUi("caixinhamanter.ui")
 					dlg.conv.show()
 					def yesmanter ():
 						deseja = "yes"
 						dlg.conv.close()
 					def nomanter ():
 						deseja = "no"
 						dlg.conv.close()
 					deseja.strip().upper()[0]

				## dos dados
				if divtype == 'Q':
					#("Temperatura da sub-corrente quente após a troca térmica")
					#(Thfinal01[chot-1][sbhot-1])
					#('Temperatura da corrente fria após a troca térmica')
					#(Tcfinal01[ccold-1][sbcold-1])
				if divtype == 'F':
					#("Temperatura da corrente quente após a troca térmica")
					#(Thfinal01[chot-1][sbhot-1])
					#('Temperatura da sub-corrente fria após a troca térmica')
					#(Tcfinal01[ccold-1][sbcold-1])
				if divtype == 'A':
					#("Temperatura da sub-corrente quente após a troca térmica")
					#(Thfinal01[chot-1][sbhot-1])
					#('Temperatura da sub-corrente fria após a troca térmica')
					#(Tcfinal01[ccold-1][sbcold-1])
				#calculo do excesso/falta de calor nas correntes quentes/frias
				#Calor das Quentes
				Qtotalh0[chot-1][sbhot-1] = Qtotalh0[chot-1][sbhot-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				Qtotalh0[chot-1][sbhot-1] = float("{:.2f}".format(Qtotalh0[chot-1][sbhot-1]))
				#Calor das Frias
				Qtotalc0[ccold-1][sbcold-1] = Qtotalc0[ccold-1][sbcold-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				Qtotalc0[ccold-1][sbhot-1] = float("{:.2f}".format(Qtotalc0[ccold-1][sbhot-1]))
				## dos dados
				#("Carga térmica do trocador")
				#(Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1])
				#("Energia disponível das correntes após a troca")
				#(Qtotalh0)
				#(Qtotalc0)

			else:
				#Temperaturas de Entrada e saída do trocador
				Thin[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Thski[chot-1][sbhot-1][sestagio-1][estagio-1]
				Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Thski[chot-1][sbhot-1][sestagio-1][estagio-1] - (Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] / CPh[chot-1])
				Tcin[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1]
				Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1] + (Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] / CPc[ccold-1])

				if Thin[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] - Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] >= dTmin:
					Thfinal0[chot-1] = Thout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					Tcfinal0[ccold-1] = Tcout[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

                    #Temperatura inicial de estágios e sub-estágios
					for k in range(nstages):
						for sk in range(nsk):
							if k < (estagio-1):
								Tcki[ccold-1][k] = Tcfinal0[ccold-1]
								Tcski[ccold-1][sbcold-1][sk][k] = Tcfinal0[ccold-1]
							if k == (estagio-1):
								if sk < (sestagio-1):
									Tcski[ccold-1][sbcold-1][sk][k] = Tcfinal0[ccold-1]

					for k in range(nstages):
						for sk in range(nsk):
							if k > (estagio-1):
								Thki[chot-1][k] = Thfinal0[chot-1]
								Thski[chot-1][sbhot-1][sk][k] = Thfinal0[chot-1]
							if k == (estagio-1):
								if sk > (sestagio-1):
									Thski[chot-1][sbhot-1][sk][k] = Thfinal0[chot-1]

					#Temperatura final dos estágios e sub-estágios
					for k in range(nstages):
						for sk in range(nsk):
							if k < (estagio-1):
								Tckf[ccold-1][k] = Tcfinal0[ccold-1]
								Tcskf[ccold-1][sbcold-1][sk][k] = Tcfinal0[ccold-1]
							if k == (estagio-1):
								if sk <= (sestagio-1):
									Tcskf[ccold-1][sbcold-1][sk][k] = Tcfinal0[ccold-1]
								Tckf[ccold-1][k] = Tcfinal0[ccold-1]

					for k in range(nstages):
						for sk in range(nsk):
							if k > (estagio-1):
								Thkf[chot-1][k] = Thfinal0[chot-1]
								Thskf[chot-1][sbhot-1][sk][k] = Thfinal0[chot-1]
							if k == (estagio-1):
								if sk >= (sestagio-1):
									Thskf[chot-1][sbhot-1][sk][k] = Thfinal0[chot-1]
								Thkf[chot-1][k] = Thfinal0[chot-1]

					## dos dados
					#("Temperatura da corrente quente após a troca:")
					#(f'{Thfinal0[chot-1]:.2f}')
					#("Temperatura da corrente fria após a troca:")
					#(f'{Tcfinal0[ccold-1]:.2f}')
					#Calor das Quentes
					Qtotalh0[chot-1][sbhot-1] = Qtotalh0[chot-1][sbhot-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					Qtotalh0[chot-1][sbhot-1] = float("{:.2f}".format(Qtotalh0[chot-1][sbhot-1]))
					#Calor das Frias
					Qtotalc0[ccold-1][sbcold-1]= Qtotalc0[ccold-1][sbcold-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					Qtotalc0[ccold-1][sbcold-1] = float("{:.2f}".format(Qtotalc0[ccold-1][sbcold-1]))
					## dos dados
					#("Carga térmica do trocador:")
					#(f'{Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]:.2f}')
					#("Energia disponível nas correntes quentes após a troca:")
					#(f'{Qtotalh0:.2f}')
					#("Energia requerida pelas correntes frias após a troca:")
					#(f'{Qtotalc0:.2f}')

				else:
					dlg.conv=uic.loadUi("caixinhamanter.ui")
					dlg.conv.show()
					def yesmanter ():
						deseja = "yes"
						dlg.conv.close()
					def nomanter ():
						deseja = "no"
						dlg.conv.close()
					deseja.strip().upper()[0]

		if deseja == 'Y':
			#()
			for k in range(nstages):
				#('ESTÁGIO ', k+1)
				for sk in range(nsk):
					#('SUB-ESTÁGIO ', sk+1)
					#('Temperatura de entrada fria')
					#(f'{Tcski[ccold-1][sbcold-1][sk][k]:.2f}')
					#('Temperatura de entrada quente')
					#(f'{Thski[chot-1][sbhot-1][sk][k]:.2f}')
					#('Temperatura de saída fria')
					#(f'{Tcskf[ccold-1][sbcold-1][sk][k]:.2f}')
					#('Temperatura de saída quente')
					#(f'{Thskf[chot-1][sbhot-1][sk][k]:.2f}')
					#()

			fim = "N"
