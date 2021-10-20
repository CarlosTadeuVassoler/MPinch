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

def VariaveisTempLoad(correntes,pinchq,pinchf,n,nhot,ncold,dlg,dTmin,estagio,chot,qsi,fracao_quente,qsj,fracao_fria,ccold,ntrocadores,nlinhas,Qtabela0):



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
    NewHeatLoad = 0

    nsi = [ncold, ncold]
    nsj = [nhot, nhot]

    nsk = nstages = 3

    Thin1 = 0
    Tcout1 = 0
    Qtabela = 0

    if ntrocadores == 0:
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
    
    #Fharr,nhotc,Qtotalh0=divisaoquente(estagio,chot,qsi,fracao_quente)    aqui são as divisões, ver isso dps

    #Fcarr,ncoldc,Qtotalc0=divisaofria(estagio,ccold,qsj,fracao_fria)

    #Impedir de trocar na mesma posição: o if abaixo pega o vetor que foi zerado e preenche dnv.
    #print("aaaaaaa",nlinhas)
    #if nlinhas >= 2:
    #    for i in range (nlinhas-1):

    #        estagio = int(float(dlg.tableWidget_2.item(i,5).text()))
    #        sestagio = int(float(dlg.tableWidget_2.item(i,4).text()))
    #        chot = int(float(dlg.tableWidget_2.item(i,0).text()))
    #        ccold = int(float(dlg.tableWidget_2.item(i,1).text()))
    #        sbhot = int(float(dlg.tableWidget_2.item(i,2).text()))
    #        sbcold = int(float(dlg.tableWidget_2.item(i,3).text()))
    #        Qtabela0=int(float(dlg.tableWidget_2.item(i,6).text()))
    #        Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]=Qtabela0

    #for si in range(ncold):
    #    if Fharr[estagio-1][chot-1][si] == 100: 
    #        Fharr[estagio-1][chot-1][si] = 0
    #for sj in range(nhot):      
    #    if Fcarr[estagio-1][ccold-1][sj] == 100:
    #        Fcarr[estagio-1][ccold-1][sj] = 0
            
    #if Fharr[estagio-1][chot-1][sbhot-1] == 0: 
    #    Fharr[estagio-1][chot-1][sbhot-1] = 100
    #if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
    #    Fcarr[estagio-1][ccold-1][sbcold-1] = 100

    chot = int(float(dlg.TempLoad.comboBox.currentText()))
    ccold = int(float(dlg.TempLoad.comboBox_2.currentText()))

    #Colocar Qmax aqui

    if dlg.TempLoad.radioButton.isChecked():                     #Inlet Hot Temperature

        tempmeta = float(dlg.TempLoad.lineEdit.text())

        print("Prints do tempload:")
        print("Qmax",Qmax)
        print("Tempmeta",tempmeta)
        print("Thski",Thski[chot-1][sbhot-1][sestagio-1][estagio-1])
        print("Cp",CPh[chot-1])
        print("Fharr",Fharr[estagio-1][chot-1][sbhot-1])



        Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = (tempmeta - Thski[chot-1][sbhot-1][sestagio-1][estagio-1])*(CPh[chot-1])#*(Fharr[estagio-1][chot-1][sbhot-1]/100))
        print("Q",Q)

        #if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] > Qmax:
        #    print('A corrente não deve chegar a esta temperatura')
        #    QMessageBox.about(dlg,"Warning!","The stream can't reach this temperature.")
        #    return

        if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] < 0:
            print('A corrente está ganhando calor')
            QMessageBox.about(dlg,"Warning!","The stream is gaining heat.")
            return

        elif Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] == 0:
            print('A temperatura continuará igual após a troca')
            QMessageBox.about(dlg,"Warning!","The temperature will be the same after the change.")
            return

    elif dlg.TempLoad.radioButton_2.isChecked():                    #OUTLET COLD TEMPERATURE
        tempmeta = float(dlg.TempLoad.lineEdit_2.text())
        Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = (tempmeta - Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1])*(CPc[ccold-1])#*(Fcarr[estagio-1][ccold-1][sbcold-1]/100))
        
        #if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] > Qmax:
        #    print('A corrente não deve chegar a esta temperatura')
        #    QMessageBox.about(dlg,"Warning!","The stream can't reach this temperature.")
        #    return

        if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] < 0:
            print('A corrente está perdendo calor')
            QMessageBox.about(dlg,"Warning!","The stream is losing heat.")
            return

        elif Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] == 0:
            print('A temperatura continuará igual após a troca')
            QMessageBox.about(dlg,"Warning!","The temperature will be the same after the change.")
            return


    #if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] != 0: 
    #    print('Já existe um trocador de calor nesta posição.')
    #    QMessageBox.about(dlg,"Error!","There is already a heat exchanger in this position!")
    #    NewHeatLoad=0
    #else:
    NewHeatLoad = Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

    return NewHeatLoad