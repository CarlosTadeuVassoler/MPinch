from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys
from divisaodecorrentes import divisaoquente
from divisaodecorrentes import divisaofria
#from testeconvertdumpnovo import adicionartrocadoracima
#from testeconvertdumpnovo import removertrocadoracima

def variaveis(nhot,ncold,n,nstages,correntestrocador,pinchq,pinchf,dlg,nlinhas):

	Th0 = [] 
	Thf = [] 
	CPh = []

	Tc0 = []
	Tcf = []
	CPc = []

	divop = avanc = ''

	complistq = []
	complistf = []
	cont = contq = contf = compq = compf = 0
	chot = ccold = sbhot = sbcold = nhotc = ncoldc = qsi = qsj = ccoldutil = 0
	Qtotalestagio = Qtotalestagiof = Qmax = Qtotalhaux = Qtotalcaux = 0
	somaCPh = somaCPc = 0
	tempdif = tempmeta = 0

	nsi = [ncold, ncold]
	nsj = [nhot, nhot]

	nsk = nstages = 3

	Thin1 = 0
	Tcout1 = 0
	Qtabela = 0

	for i in range(n):
	        if correntestrocador[i][3] == "Hot":
	            Th0.append(correntestrocador[i][0])
	            Thf.append(pinchq) 
	            CPh.append(correntestrocador[i][2])
	        j=0
	for i in range(n):
	        if correntestrocador[i][3] == "Cold":
	            Tc0.append(pinchf)         
	            Tcf.append(correntestrocador[i][1])
	            CPc.append(correntestrocador[i][2])
	            j=j+1
	#elif ntrocadores > 0:
	#    for i in range(n):
	#            if correntestrocador[i][3] == "Hot":
	#                Th0.append(correntestrocador[i][0])
	#                Thf.append(correntestrocador[i][1]) 
	#                CPh.append(correntestrocador[i][2])
	#            j=0
	#    for i in range(n):
	#            if correntestrocador[i][3] == "Cold":
	#                Tc0.append(correntestrocador[i][0])         
	#                Tcf.append(correntestrocador[i][1])
	#                CPc.append(correntestrocador[i][2])
	#                j=j+1

	Qutilcold = np.array([0])
	Qutilcold.resize(ncold)
	Qtotalh01 = []
	Qtotalc01 = []
	Qtotalh0arr = np.array([0])
	Qtotalh0arr.resize(nhot, ncold,nstages)
	Qtotalh0 = Qtotalh0arr.tolist()
	map(float, Qtotalh0)
	Qtotalc0arr = np.array([0])
	Qtotalc0arr.resize(ncold, nhot,nstages)
	Qtotalc0 = Qtotalc0arr.tolist()
	map(float, Qtotalc0)
	Qestagioq = np.array([0])
	Qestagioq.resize(nhot, nstages)
	Qestagiof = np.array([0])
	Qestagiof.resize(ncold, nstages)

	#CÁLCULOS DOS CALORES TOTAIS
	for i in range (nhot):
	    Qtotalh1 = 0
	    Qtotalh1 = int(float(dlg.tableWidget_3.item(i,3).text()))
	    Qtotalh01.append(Qtotalh1)
	    Qtotalh01[i] = float('{:.2f}'.format(Qtotalh01[i]))
	for j in range (ncold):
	    Qtotalc1 = 0
	    Qtotalc1 = int(float(dlg.tableWidget_4.item(j,3).text()))*-1
	    Qtotalc01.append(Qtotalc1)
	    Qtotalc01[j] = float('{:.2f}'.format(Qtotalc01[j]))
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
	Fharr = np.array ([])
	Fharr.resize(nstages, nhot, ncold)
	Fcarr = np.array ([0])
	Fcarr.resize(nstages, ncold, nhot)
	Qarr = np.array([0])
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


	return Thf,Th0,CPc,CPh,Tc0,Tcf,Qtotalh0,Qtotalc0,Q,Fharr,Fcarr,Thout,Thin,Tcout,Tcin,somaCPh,somaCPc,compq,compf,complistq,complistf,nhotc,ncoldc,nsk,Thski,Thskf,Tcski,Tcskf,Thki,Thkf,Tcki,Tckf,Qaux,Qestagioq,Qestagiof,Think,Thoutk,Tcink,Tcoutk,Thfinal01,Tcfinal01,Thfinal01k,Tcfinal01k


		

def variaveis2(nhot,ncold,n,nstages,correntestrocador,pinchq,pinchf,dlg):		

	Thf,Th0,CPc,CPh,Tc0,Tcf,Qtotalh0,Qtotalc0,Q,Fharr,Fcarr,Thout,Thin,Tcout,Tcin,somaCPh,somaCPc,compq,compf,complistq,complistf,nhotc,ncoldc,nsk,Thski,Thskf,Tcski,Tcskf,Thki,Thkf,Tcki,Tckf,Qaux,Qestagioq,Qestagiof,Think,Thoutk,Tcink,Tcoutk,Thfinal01,Tcfinal01,Thfinal01k,Tcfinal01k=adicionartrocadoracima(correntestrocador,ntrocadores,pinchq,pinchf,n,nhot,ncold,dlg,dTmin,chot,ccold,nlinhas,opcao,nstages)