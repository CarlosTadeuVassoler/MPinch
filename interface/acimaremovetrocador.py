from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMessageBox,QTableWidget,QTableWidgetItem
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import sys
from divisaodecorrentes import divisaoquente
from divisaodecorrentes import divisaofria
from variaveistrocador import variaveistrocador

def acimaremovetrocador(correntes,pinchq,pinchf,n,nhot,ncold,dlg,dTmin,estagio,chot,qsi,fracao_quente,qsj,fracao_fria,ccold,ntrocadores,Qtabela0,Qhot0,Qcold0,Tcout0,Thin0,nlinhas):

    Th0 = []
    Thf = []
    CPh = []

    Tc0 = []
    Tcf = []
    CPc = []

    divop = avanc = ''

    complistq = []
    complistf = []
    cont = contq = contf = compq = compf = opcao = 0
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
            if correntes[i][3] == "Hot":
                Th0.append(correntes[i][0])
                Thf.append(pinchq)
                CPh.append(correntes[i][2])
            j=0
    for i in range(n):
            if correntes[i][3] == "Cold":
                Tc0.append(pinchf)
                Tcf.append(correntes[i][1])
                CPc.append(correntes[i][2])
                j=j+1

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

    #Fharr,nhotc,Qtotalh0=divisaoquente(estagio,chot,qsi,fracao_quente)    aqui são as divisões, ver isso dps

    #Fcarr,ncoldc,Qtotalc0=divisaofria(estagio,ccold,qsj,fracao_fria)
    # ("nlinhas1",nlinhas)
    #(Tcout0)
    if nlinhas >= 2:
        for i in range (nlinhas-1):
            #("nlinhas2",nlinhas)
            estagio = int(float(dlg.tableWidget_2.item(i,5).text()))
            sestagio = int(float(dlg.tableWidget_2.item(i,4).text()))
            chot = int(float(dlg.tableWidget_2.item(i,0).text()))
            ccold = int(float(dlg.tableWidget_2.item(i,1).text()))
            sbhot = int(float(dlg.tableWidget_2.item(i,2).text()))
            sbcold = int(float(dlg.tableWidget_2.item(i,3).text()))
            Qtabela0 = int(float(dlg.tableWidget_2.item(i,6).text()))
            Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1] = int(float(dlg.tableWidget_2.item(i,8).text()))
            Thski[chot-1][sbhot-1][sestagio-1][estagio-1] = int(float(dlg.tableWidget_2.item(i,7).text()))
            Qtotalh0[chot-1][sbhot-1][estagio-1]=Qhot0
            Qtotalc0[ccold-1][sbcold-1][estagio-1]=Qcold0
            Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]=Qtabela0


    #("Tcout e Thin",Tcskf,Thski)

    #REMOVER TROCADOR DE CALOR
    #rows = sorted(set(index.row() for index in dlg.tableWidget_2.selectedIndexes()))
    #for row in rows:
    #   nlinhas = nlinhas-1
    #("nlinhas3",nlinhas)
    estagio = int(float(dlg.tableWidget_2.item(nlinhas-2,5).text()))
    sestagio = int(float(dlg.tableWidget_2.item(nlinhas-2,4).text()))
    chot = int(float(dlg.tableWidget_2.item(nlinhas-2,0).text()))
    ccold = int(float(dlg.tableWidget_2.item(nlinhas-2,1).text()))
    sbhot = int(float(dlg.tableWidget_2.item(nlinhas-2,2).text()))
    sbcold = int(float(dlg.tableWidget_2.item(nlinhas-2,3).text()))
    #(estagio,sestagio,chot,ccold,sbhot,sbcold)

    #ADIÇÃO DE CALOR():
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
    #("Tccold0",Tcskf)
    #CÁLCULO DA SUPERESTRUTURA
    for k in range (nstages-1, -1, -1):
    	for sk in range (nsk-1, -1, -1):
    		for i in range (nhot-1, -1, -1):
    			for si in range (ncold-1, -1, -1):
    				for j in range(ncold-1, -1, -1):
    					for sj in range(nhot-1, -1, -1):
    						#("QcalorLoop",Q)
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

    							Think[i][si][j][sj][sk][k] = Thki[i][k]
    							Thoutk[i][si][j][sj][sk][k] = Think[i][si][j][sj][sk][k] + (Qestagioq[i][k]/CPh[i])

    							Tcin[i][si][j][sj][sk][k] = Tcski[j][sj][sk][k]
    							Tcout[i][si][j][sj][sk][k] = Tcin[i][si][j][sj][sk][k] + (Q[i][si][j][sj][sk][k]/(CPc[j]*(Fcarr[k][j][sj]/100)))
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


    Tcin = Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1]
    Thin = Thskf[chot-1][sbhot-1][sestagio-1][estagio-1]  #aqui conta o Thskf pq o acima inverte
    Tcout = Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1]
    Thout = Thskf[chot-1][sbhot-1][sestagio-1][estagio-1]
    #("Tccold2",Tcskf)

    Fharr1 = Fharr[estagio-1][chot-1][sbhot-1]/100
    Fcarr1 = Fcarr[estagio-1][ccold-1][sbcold-1]/100
    Qtabela = Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
    Qhot = Qtotalh0[chot-1][sbhot-1][estagio-1]
    Qcold = Qtotalc0[ccold-1][sbcold-1][estagio-1]*-1

    #("----- #S DAS VARIÁVEIS -----")
    #("Q:", Qtabela)
    #("Thin",Thin)
    #("Tcout",Tcout)
    #("Qhot",Qhot)
    #("Qcold",Qcold)

    Thin = float('{:.1f}'.format(Thin))
    Tcout = float('{:.1f}'.format(Tcout))
    Qtabela = float('{:.1f}'.format(Qtabela))
    Fharr1 = float('{:.1f}'.format(Fharr1))
    Fcarr1 = float('{:.1f}'.format(Fcarr1))
    Qhot = float('{:.1f}'.format(Qhot))
    Qcold = float('{:.1f}'.format(Qcold))

    return Thin,Tcout,Qtabela,Fharr1,Fcarr1,Qhot,Qcold
