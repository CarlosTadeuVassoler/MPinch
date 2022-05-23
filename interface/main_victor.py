from PyQt5 import QtWidgets , uic, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
import numpy as np
import funchpinchcerto as fp2
from funcPPinch import pontopinch
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pylab as P
from Graficocurva import plotgrafcurva,plotgrafcurva2
from Graficocurvabalanceada import cc1,cc2
import testesoriginal as tt
import xlsxwriter
from canvas import Gc1,Gc2
from tkinter.filedialog import askopenfilename
import xlrd
import re
import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from CORRENTEGRAPH import cascata,cascata2
from prog_carlos import *
from prog_carlos_abaixo import *
from converter_unidades import *
from matplotlib.figure import Figure
from PIL import Image
import turtle
from exportaa import export
from svg_turtle import SvgTurtle
import os
from custo2 import varia
from superestrutura_completa import *
from tkinter import Tk

workbook = xlsxwriter.Workbook('testevv.xlsx')
worksheet = workbook.add_worksheet()

app=QtWidgets.QApplication([])
dlg=uic.loadUi("MPinch2.ui")
dlg.stream_supply.setPlaceholderText(" Ex: 273.15")
dlg.stream_target.setPlaceholderText(" Ex: 273.15")
dlg.util_inlet.setPlaceholderText(" Ex: 273.15")
dlg.util_outlet.setPlaceholderText(" Ex: 273.15")
dlg.stream_cp.setPlaceholderText(" Ex: 200.20")


matriz = []
matriz_armazenada = []
matriz_trocadores_abaixo = []
matriz_evolucao = []
utilidades = []
utilidades_abaixo = []
dTmin = 10
donee=0
done = False
cascat=[]
nstages=1
subestagio_trocador = 0
subestagio_trocador_abaixo = 0
alreadypinched=0
plotou=0
ccopi=[]
corrente_quente_presente_acima = []
corrente_fria_presente_acima = []
corrente_quente_presente_abaixo = []
corrente_fria_presente_abaixo = []
correntes_quentes = []
correntes_frias = []
n = nhot = ncold = n_util = 0
correntes = []
e_utilidade = []
e_utilidade_quente = []
e_utilidade_fria = []
correntes_util = []
correntenutilidade=[]
#


#######################
def formatando(valor,index):
    if valor>=1_000_000:
        fomatador = '{:1.1f}M'.format(valor*0.000_001)
    else:
        fomatador = '{:1.0f}k'.format(valor * 0.001)
    return fomatador

def eq():
    start=float(dlg.dtstart.text())
    step=float(dlg.dtstep.text())
    asch=dlg.dtstep.text()
    asch = asch.split(".")
    try:
        if len(asch[1])>4:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("font-weight: bold")
            msg.setStyleSheet("text-align:center")
            msg.setText("The limit is 4 digits after the separator.\nChange the step value and try again.")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return 0
    except:
        pass

    bsch=dlg.dtstart.text()
    bsch = bsch.split(".")

    try:
        if len(bsch[1])>4:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("font-weight: bold")
            msg.setStyleSheet("text-align:center")
            msg.setText("The limit is 4 digits after the separator.\nChange the start value and try again.")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return 0
    except:
        pass



    stop=float(dlg.dtstop.text())
    csch=dlg.dtstop.text()
    csch = csch.split(".")

    try:
        if len(csch[1])>4:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("font-weight: bold")
            msg.setStyleSheet("text-align:center")
            msg.setText("The limit is 4 digits after the separator.\nChange the stop value and try again.")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return 0
    except:
        pass

    if stop<start:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setStyleSheet("font-weight: bold")
        msg.setStyleSheet("text-align:center")
        msg.setText("The stop value needs to be higher than start value.\nChange the start or stop value and try again.")
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        return 0

    if len(np.arange(start, stop + step, step))>500:
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("This may take some time")
        msgBox.setText("You will run about "+ str(len(np.arange(start, stop + step, step))) +" iteractions\nDo you want to proceed?")
        msgBox.setStyleSheet("font-weight: bold")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Cancel:
            return 0

    dlg.equation = uic.loadUi("Select.ui")
    dlg.equation.show()

    def z3():
        if (dlg.equation.nareas.isChecked() == True):
            nnn=-1
            otimizafun(nnn)
        elif(dlg.equation.us1.isChecked() == True):
            nnn=-2
            otimizafun(nnn)
        elif(dlg.equation.esp.isChecked() == True):
            nnn=float(dlg.equation.lineesp.text())
            otimizafun(nnn)
        dlg.equation.close()


    dlg.equation.otimizarun.clicked.connect(lambda: z3())

def otimizafun(nnn):
    start=float(dlg.dtstart.text())

    step=float(dlg.dtstep.text())

    stop=float(dlg.dtstop.text())




    global variadt, yplot, custoopano, custocapital, custocapitalanual, custototanual,uf,uq,dtopt
    uf,uq,variadt, yplot, custoopano, custocapital, custocapitalanual, custototanual=varia(start,step,stop,correntes,nnn)
    changedv=[]
    print(uf,uq)
    changedv.append(variadt[0])
    for i in range(0,len(custocapitalanual)):
        try:
            changedv.append(variadt[i+1])
            if not(custocapitalanual[i]>custocapitalanual[i+1] and custocapitalanual[i+2]<custocapitalanual[i+1]):
                """changedv.pop()"""
                """custocapitalanual[i+1]=((custocapitalanual[i+2]-custocapitalanual[i])*(variadt[i+1]-variadt[i+2])/(variadt[i+2]-variadt[i]))+custocapitalanual[i+2]
                changedv.append(str(str(round(variadt[i+1],3))+"*"))"""
                """custototanual[i+1]=custoopano[i+1]+custocapitalanual[i+1]"""
            else:
                pass
        except:
            pass


    Custoopotimizado=custoopano[custototanual.index(min(custototanual))]
    cccapitalanualopt=custocapitalanual[custototanual.index(min(custototanual))]
    dtopt=variadt[custototanual.index(min(custototanual))]
    print(dtopt)
    cccapitalopt=custocapital[custototanual.index(min(custototanual))]
    areaopt = yplot[custototanual.index(min(custototanual))]
    custototanualopt=min(custototanual)

    dlg.label_46.setText("Operating Cost : "+str(round(Custoopotimizado,2)))
    dlg.label_46.setFont(QFont('Arial', 10))
    dlg.label_46.setStyleSheet("font-weight: bold")
    try:
        dlg.label_45.setText("ΔTmin : "+str(round(dtopt,5))) #preciso prestar atenção nisso quanto ao passo
    except:
        dlg.label_45.setText("ΔTmin : "+str(dtopt)) #preciso prestar atenção nisso quanto ao passo

    dlg.label_45.setFont(QFont('Arial', 10))
    dlg.label_45.setStyleSheet("font-weight: bold")
    dlg.label_50.setText("Capital Cost : "+str(round(cccapitalopt,2)))
    dlg.label_50.setFont(QFont('Arial', 10))
    dlg.label_50.setStyleSheet("font-weight: bold")
    dlg.label_52.setText("Anualized Capital Cost : "+str(round(cccapitalanualopt,2)))
    dlg.label_52.setFont(QFont('Arial', 10))
    dlg.label_52.setStyleSheet("font-weight: bold")
    dlg.label_49.setText("Total Cost: "+str(round(custototanualopt,2)))
    dlg.label_49.setFont(QFont('Arial', 10))
    dlg.label_49.setStyleSheet("font-weight: bold")
    dlg.label_53.setText("Area: "+str(round(areaopt,2)))
    dlg.label_53.setFont(QFont('Arial', 10))
    dlg.label_53.setStyleSheet("font-weight: bold")



    row = 0
    valorbonito = np.round(variadt, 5)
    dlg.TABELA.setRowCount(len(valorbonito))

    p=0

    for data in range(0, len(valorbonito)):
        try:
            dlg.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(np.round(changedv[data], 5))))

        except:
            dlg.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(changedv[data])))
        dlg.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(np.round(yplot[data], 2))))
        dlg.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(np.round(custoopano[data], 2))))
        dlg.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(np.round(custocapitalanual[data], 2))))
        dlg.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(np.round(custototanual[data], 2))))
        row += 1

    # print(variadt)
    dlg.sc = myCanvas()
    y=[0]
    x=[0]
    dlg.sc.plot(x, y)


    dlg.sc2 = myCanvas2()
    dlg.sc2.plot(x, y)


    dlg.sc3 = myCanvas3()
    dlg.sc3.plot(x, y)
    dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva1.png"))


def mostra3():
    dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva1.png"))

def mostra2():
    dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva3.png"))

def mostra1():
    dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva2.png"))


class myCanvas(FigureCanvas):
    def __init__(self):
        self.fig=Figure()
        FigureCanvas.__init__(self,self.fig)

    def plot(self,x,y):
        # PLT.CLOSE("ALL") PRA NÃO COMER TODA A MEMORIA DO SEU PC PELO AMOR DE DEUS NÃO ESQUECE DISSO
        plt.close("all")

        plt.style.use('bmh')
        self.ax= self.fig.add_subplot(111)
        self.ax.yaxis.set_major_formatter(formatando)
        self.ax.plot(variadt,custoopano, label='Operational Cost x ΔTmin')
        self.ax.plot(variadt,custocapitalanual, label='Capital Cost x ΔTmin', color='k')
        self.ax.plot(variadt, custototanual, label='Total Cost x ΔTmin', color='r')
        self.ax.set_xlabel('ΔTmin')
        self.ax.set_ylabel('Cost')
        self.ax.legend()
        self.ax.grid(axis="x", color="black", alpha=.3, linewidth=2, linestyle=":")
        self.ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
        self.draw()
        self.fig.savefig("canva1.png",bbox_inches="tight", pad_inches=0.5)

class myCanvas2(FigureCanvas):
    def __init__(self):
        self.fig=Figure()
        FigureCanvas.__init__(self,self.fig)

    def plot(self,x,y):
        # PLT.CLOSE("ALL") PRA NÃO COMER TODA A MEMORIA DO SEU PC PELO AMOR DE DEUS NÃO ESQUECE DISSO
        plt.close("all")
        plt.style.use('bmh')

        self.ax= self.fig.add_subplot(111)
        self.ax.yaxis.set_major_formatter(formatando)

        # print(variadt)
        self.ax.plot(variadt,yplot, label='Area x ΔTmin', color='r')
        self.ax.set_xlabel('ΔTmin')
        self.ax.set_ylabel('Area')
        self.ax.legend()
        self.ax.grid(axis="x", color="black", alpha=.3, linewidth=2, linestyle=":")
        self.ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
        self.draw()
        self.fig.savefig("canva2.png",bbox_inches="tight", pad_inches=0.5)

class myCanvas3(FigureCanvas):
    def __init__(self):
        self.fig=Figure()
        FigureCanvas.__init__(self,self.fig)

    def plot(self,x,y):
        # PLT.CLOSE("ALL") PRA NÃO COMER TODA A MEMORIA DO SEU PC PELO AMOR DE DEUS NÃO ESQUECE DISSO
        plt.close("all")
        plt.style.use('bmh')
        self.ax= self.fig.add_subplot(111)
        #self.ax.yaxis.set_major_formatter(formatando)
        self.ax.plot(variadt,uq, label='Hot utility x ΔTmin', color='r')
        self.ax.plot(variadt, uf, label='Cold utility x ΔTmin', color='b')
        self.ax.set_xlabel('ΔTmin')
        self.ax.set_ylabel('Utility')
        self.ax.legend()
        self.ax.grid(axis="x", color="black", alpha=.3, linewidth=2, linestyle=":")
        self.ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
        self.draw()
        self.fig.savefig("canva3.png",bbox_inches="tight", pad_inches=0.5)
########################


def plotgraficocurva():

    try:
        dlg.labe1.hide()
        dlg.scrola1.hide()
        dlg.horizontalLayout_32.removeWidget(dlg.scrola1)
        dlg.graficodt1.show()
        dlg.graficodt2.show()
        dlg.linicio.show()
        dlg.lmeio.show()
        dlg.lfim.show()
    except:
        None
    try:
        dlg.labe2.hide()
        dlg.scrola2.hide()
        dlg.horizontalLayout_32.removeWidget(dlg.scrola2)
        dlg.graficodt1.show()
        dlg.graficodt2.show()
        dlg.linicio.show()
        dlg.lmeio.show()
        dlg.lfim.show()
    except:
        None



    print(correntenutilidade)
    try:
        asch = dlg.DTMIN1.text()
        asch = asch.split(".")
        try:
            if len(asch[1]) > 4:
                dlg.graficodt1.setText('Waiting for ΔTmin1 data...')
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setStyleSheet("font-weight: bold")
                msg.setStyleSheet("text-align:center")
                msg.setText(
                    "The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT ONE} value and try again.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return 0
        except:
            pass
        pinchf1,pinchq1,uq1,uf1,_=pontopinch(correntenutilidade,len(correntenutilidade),float(dlg.DTMIN1.text()))

        plotgrafcurva(correntenutilidade, float(dlg.DTMIN1.text()),uf1,uq1,pinchf1,pinchq1)

        dlg.graficodt1.setPixmap(QtGui.QPixmap("curvadt1.png"))

    except:
        dlg.graficodt1.setText('Waiting for ΔTmin1 data...')

    try:
        asch = dlg.DTMIN2.text()
        asch = asch.split(".")
        try:
            if len(asch[1]) > 4:
                dlg.graficodt2.setText('Waiting for ΔTmin2 data...')
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setStyleSheet("font-weight: bold")
                msg.setStyleSheet("text-align:center")
                msg.setText(
                    "The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT TWO} value and try again.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

                return 0
        except:
            pass
        pinchf2, pinchq2, uq2, uf2,_ = pontopinch(correntenutilidade, len(correntenutilidade),float(dlg.DTMIN2.text()))

        plotgrafcurva2(correntenutilidade, float(dlg.DTMIN2.text()), uf2, uq2, pinchf2, pinchq2)

        dlg.graficodt2.setPixmap(QtGui.QPixmap("curvadt2.png"))

    except:
        dlg.graficodt2.setText('Waiting for ΔTmin2 data...')

def plotgraficocurvacomp():
    try:
        dlg.labe1.hide()
        dlg.scrola1.hide()
        dlg.horizontalLayout_32.removeWidget(dlg.scrola1)
        dlg.graficodt1.show()
        dlg.graficodt2.show()
        dlg.linicio.show()
        dlg.lmeio.show()
        dlg.lfim.show()
    except:
        None
    try:
        dlg.labe2.hide()
        dlg.scrola2.hide()
        dlg.horizontalLayout_32.removeWidget(dlg.scrola2)
        dlg.graficodt1.show()
        dlg.graficodt2.show()
        dlg.linicio.show()
        dlg.lmeio.show()
        dlg.lfim.show()
    except:
        None

    try:
        try:
            asch = dlg.DTMIN1.text()
            asch = asch.split(".")
            if len(asch[1]) > 4:
                dlg.graficodt1.setText('Waiting for ΔTmin1 data...')
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setStyleSheet("font-weight: bold")
                msg.setStyleSheet("text-align:center")
                msg.setText(
                    "The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT ONE} value and try again.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return 0
        except:
            pass
        contador=0
        correntecomp = correntenutilidade
        tf1,tq1,uq1, uf1,_ = pontopinch(correntenutilidade, len(correntenutilidade), float(dlg.DTMIN1.text()))
        uf1, uq1,_,_ = fp2.pontopinch(correntenutilidade, len(correntenutilidade), float(dlg.DTMIN1.text()))
        for i in range(0,len(ccopi)):
            if ccopi[i][3]=='Cold':
                ccopi[i][2]=uf1/(ccopi[i][1]-ccopi[i][0])
                correntecomp.append(ccopi[i])
                contador+=1
            else:
                ccopi[i][2] = uq1 / (ccopi[i][0] - ccopi[i][1])
                correntecomp.append(ccopi[i])
                contador+=1

        _,_,datagraph,_,_,_,_ = tt.CUSTO(correntecomp, len(correntecomp))
        for i in range(0,contador):
            correntecomp.pop()
        cc1(datagraph,float(dlg.DTMIN1.text()),round(tf1,6),round(tq1,6))
        dlg.graficodt1.setPixmap(QtGui.QPixmap("cc1.png"))
    except:
        dlg.graficodt1.setText('Waiting for ΔTmin1 data...')
    try:
        try:
            asch = dlg.DTMIN2.text()
            asch = asch.split(".")
            if len(asch[1]) > 4:
                dlg.graficodt2.setText('Waiting for ΔTmin2 data...')
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setStyleSheet("font-weight: bold")
                msg.setStyleSheet("text-align:center")
                msg.setText(
                    "The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT TWO} value and try again.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return 0
        except:
            pass
        contador=0
        tf2,tq2,uq2, uf2,_ = pontopinch(correntenutilidade, len(correntenutilidade), float(dlg.DTMIN2.text()))
        uf2, uq2,_,_ = fp2.pontopinch(correntenutilidade, len(correntenutilidade), float(dlg.DTMIN2.text()))
        for i in range(0,len(ccopi)):
            if ccopi[i][3]=='Cold':
                ccopi[i][2]=uf2/(ccopi[i][1]-ccopi[i][0])
                correntecomp.append(ccopi[i])
                contador+=1
            else:
                ccopi[i][2] = uq2 / (ccopi[i][0] - ccopi[i][1])
                correntecomp.append(ccopi[i])
                contador+=1

        _,_,datagraph,_,_,_,_  = tt.CUSTO(correntecomp, len(correntecomp))
        for i in range(0,contador):
            correntecomp.pop()
        cc2(datagraph,float(dlg.DTMIN2.text()),round(tf2,6),round(tq2,6))

        dlg.graficodt2.setPixmap(QtGui.QPixmap("cc2.png"))

    except:
        dlg.graficodt2.setText('Waiting for ΔTmin2 data...')

def GC():
    try:
        dlg.labe1.hide()
        dlg.scrola1.hide()
        dlg.horizontalLayout_32.removeWidget(dlg.scrola1)
        dlg.graficodt1.show()
        dlg.graficodt2.show()
        dlg.linicio.show()
        dlg.lmeio.show()
        dlg.lfim.show()
    except:
        None
    try:
        dlg.labe2.hide()
        dlg.scrola2.hide()
        dlg.horizontalLayout_32.removeWidget(dlg.scrola2)
        dlg.graficodt1.show()
        dlg.graficodt2.show()
        dlg.linicio.show()
        dlg.lmeio.show()
        dlg.lfim.show()
    except:
        None

    try:
        asch = dlg.DTMIN1.text()
        asch = asch.split(".")
        try:
            if len(asch[1]) > 4:
                dlg.graficodt1.setText('Waiting for ΔTmin1 data...')
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setStyleSheet("font-weight: bold")
                msg.setStyleSheet("text-align:center")
                msg.setText(
                    "The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT ONE} value and try again.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return 0
        except:
            pass
        _, _, _, _, coisas_graficos1 = pontopinch(correntenutilidade, len(correntenutilidade), float(dlg.DTMIN1.text()))
        Gc1(len(correntenutilidade),dlg,coisas_graficos1[0],coisas_graficos1[7],coisas_graficos1[5],unidadeusada)
    except:
        dlg.graficodt1.setText('Waiting for ΔTmin1 data...')
    try:
        asch = dlg.DTMIN2.text()
        asch = asch.split(".")
        try:
            if len(asch[1]) > 4:
                dlg.graficodt2.setText('Waiting for ΔTmin2 data...')
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setStyleSheet("font-weight: bold")
                msg.setStyleSheet("text-align:center")
                msg.setText(
                    "The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT TWO} value and try again.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return 0
        except:
            pass
        _, _, _, _, coisas_graficos2 = pontopinch(correntenutilidade, len(correntenutilidade), float(dlg.DTMIN2.text()))
        Gc2(len(correntenutilidade),dlg,coisas_graficos2[0],coisas_graficos2[7],coisas_graficos2[5],unidadeusada)
    except:
        dlg.graficodt2.setText('Waiting for ΔTmin2 data...')

def savefile():

    contador = 0
    correntecomp4 = correntenutilidade
    uf1, uq1, _, _ = fp2.pontopinch(correntenutilidade, len(correntenutilidade), float(dlg.lineEdit_2.text()))

    for i in range(0, len(ccopi)):
        if ccopi[i][3] == 'Cold':
            ccopi[i][2] = uf1 / (ccopi[i][1] - ccopi[i][0])
            correntecomp4.append(ccopi[i])
            contador += 1
        else:
            ccopi[i][2] = uq1 / (ccopi[i][0] - ccopi[i][1])
            correntecomp4.append(ccopi[i])

            contador += 1

    akt, _, ajustado, cpf, cpq, areak, deltalmnk = tt.CUSTO(correntecomp4, len(correntecomp4))
    for i in range(0, contador):
        correntecomp4.pop()
    export(correntenutilidade,ccopi, variadt, yplot, custoopano, custocapital, custocapitalanual, custototanual,uf,uq,float(dlg.lineEdit_2.text()),akt, ajustado, cpf, cpq, areak, deltalmnk)

def CASCA():

    try:
        dlg.labe1.hide()
        dlg.scrola1.hide()
        dlg.horizontalLayout_32.removeWidget(dlg.scrola1)
    except:
        None
    try:
        dlg.labe2.hide()
        dlg.scrola2.hide()
        dlg.horizontalLayout_32.removeWidget(dlg.scrola2)
    except:
        None

    dlg.labe1=QLabel()
    dlg.labe2=QLabel()
    dlg.graficodt1.hide()
    dlg.graficodt2.hide()
    dlg.linicio.hide()
    dlg.lmeio.hide()
    dlg.lfim.hide()
    try:
        asch = dlg.DTMIN1.text()
        asch = asch.split(".")
        try:
            if len(asch[1]) > 4:
                dlg.linicio.show()
                dlg.graficodt1.show()
                dlg.graficodt1.setText('Waiting for ΔTmin1 data...')  #
                dlg.lmeio.show()
                dlg.lfim.show()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setStyleSheet("font-weight: bold")
                msg.setStyleSheet("text-align:center")
                msg.setText(
                    "The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT ONE} value and try again.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
            else:
                try:
                    cascata(correntenutilidade, float(dlg.DTMIN1.text()))
                    dlg.labe1.setPixmap(QtGui.QPixmap("EC.png"))
                    dlg.scrola1 = QScrollArea()
                    dlg.scrola1.setBackgroundRole(QPalette.Light)
                    dlg.scrola1.setAlignment(Qt.AlignCenter)
                    dlg.horizontalLayout_32.insertWidget(1, dlg.scrola1)
                    dlg.scrola1.setWidget(dlg.labe1)
                except:
                    pass
        except:
            cascata(correntenutilidade, float(dlg.DTMIN1.text()))
            dlg.labe1.setPixmap(QtGui.QPixmap("EC.png"))
            dlg.scrola1 = QScrollArea()
            dlg.scrola1.setBackgroundRole(QPalette.Light)
            dlg.scrola1.setAlignment(Qt.AlignCenter)
            dlg.horizontalLayout_32.insertWidget(1, dlg.scrola1)
            dlg.scrola1.setWidget(dlg.labe1)

    except:
        dlg.linicio.show()
        dlg.graficodt1.show()
        dlg.graficodt1.setText('Waiting for ΔTmin1 data...') #
        dlg.lmeio.show()
        dlg.lfim.show()
    try:
        asch = dlg.DTMIN2.text()
        asch = asch.split(".")
        try:
            if len(asch[1]) > 4:
                dlg.graficodt2.show()
                dlg.graficodt2.setText('Waiting for ΔTmin2 data...')
                dlg.lfim.show()
                dlg.lmeio.show()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setStyleSheet("font-weight: bold")
                msg.setStyleSheet("text-align:center")
                msg.setText(
                    "The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT TWO} value and try again.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                dlg.linicio.show()
            else:
                try:
                    cascata2(correntenutilidade, float(dlg.DTMIN2.text()))
                    dlg.labe2.setPixmap(QtGui.QPixmap("EC2.png"))
                    dlg.scrola2 = QScrollArea()
                    dlg.scrola2.setBackgroundRole(QPalette.Light)
                    dlg.scrola2.setAlignment(Qt.AlignCenter)
                    dlg.horizontalLayout_32.insertWidget(3, dlg.scrola2)
                    dlg.scrola2.setWidget(dlg.labe2)
                except:
                    pass

        except:
            cascata2(correntenutilidade, float(dlg.DTMIN2.text()))
            dlg.labe2.setPixmap(QtGui.QPixmap("EC2.png"))
            dlg.scrola2 = QScrollArea()
            dlg.scrola2.setBackgroundRole(QPalette.Light)
            dlg.scrola2.setAlignment(Qt.AlignCenter)
            dlg.horizontalLayout_32.insertWidget(3,dlg.scrola2)
            dlg.scrola2.setWidget(dlg.labe2)
    except:
        dlg.linicio.show()

        dlg.graficodt2.show()
        dlg.graficodt2.setText('Waiting for ΔTmin2 data...')
        dlg.lfim.show()
        dlg.lmeio.show()

def caxa():
    asch=dlg.DTMIN1.text()
    asch = asch.split(".")
    try:
        if len(asch[1])>4:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("font-weight: bold")
            msg.setStyleSheet("text-align:center")
            msg.setText("The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT ONE} value and try again.")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return 0
    except:
        pass
    try:

        contador=0
        correntecomp4 = correntenutilidade
        uf1, uq1,_,_ = fp2.pontopinch(correntenutilidade, len(correntenutilidade), float(dlg.DTMIN1.text()))

        for i in range(0,len(ccopi)):
            if ccopi[i][3]=='Cold':
                ccopi[i][2]=uf1/(ccopi[i][1]-ccopi[i][0])
                correntecomp4.append(ccopi[i])
                contador+=1
            else:
                ccopi[i][2] = uq1 / (ccopi[i][0] - ccopi[i][1])
                correntecomp4.append(ccopi[i])

                contador+=1

        akt,_,ajustado,cpf,cpq,areak,deltalmnk = tt.CUSTO(correntecomp4, len(correntecomp4))




        dlg.area = uic.loadUi("Area.ui")
        dlg.area.show()
        dlg.area.label.setText("ΔTmin\N{SUBSCRIPT ONE} :  "+str(round(float(dlg.DTMIN1.text()),5)))
        dlg.area.label.setFont(QFont('Arial', 14))
        dlg.area.label.setStyleSheet("font-weight: bold")
        row = 0
        dlg.area.TABELA.setRowCount(len(areak)+1)

        for data in range(0, len(areak)):
            dlg.area.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data],2))))
            dlg.area.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data + 1],2))))
            dlg.area.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data],2))))
            dlg.area.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data + 1],2))))
            dlg.area.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(round(cpq[data],2))))
            dlg.area.TABELA.setItem(row, 5, QtWidgets.QTableWidgetItem(str(round(cpf[data],2))))
            dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str(round(deltalmnk[data],2))))
            dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round(areak[data],2))))
            row += 1
        dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str('Total Area:')))
        dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round((akt),2))))



            ##################acaba aq
        for i in range(0,contador):
            correntecomp4.pop()
    except:
        try:
            f = float(dlg.DTMIN1.text())
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("font-weight: bold")
            msg.setStyleSheet("text-align:center")
            msg.setText("Please input utility data in 'Streams' tab")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("font-weight: bold")
            msg.setStyleSheet("text-align:center")
            msg.setText("Please input ΔTmin₁ data")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

def caxa2():
    asch=dlg.DTMIN2.text()
    asch = asch.split(".")
    try:
        if len(asch[1])>4:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("font-weight: bold")
            msg.setStyleSheet("text-align:center")
            msg.setText("The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT TWO} value and try again.")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return 0
    except:
        pass
    try:
        contador = 0
        correntecomp4 = correntenutilidade
        uf1, uq1,_,_ = fp2.pontopinch(correntenutilidade, len(correntenutilidade), float(dlg.DTMIN2.text()))

        for i in range(0, len(ccopi)):
            if ccopi[i][3] == 'Cold':
                ccopi[i][2] = uf1 / (ccopi[i][1] - ccopi[i][0])

                correntecomp4.append(ccopi[i])
                contador += 1
            else:
                ccopi[i][2] = uq1 / (ccopi[i][0] - ccopi[i][1])
                correntecomp4.append(ccopi[i])
                contador += 1

        akt, _, ajustado, cpf, cpq, areak,deltalmnk = tt.CUSTO(correntecomp4, len(correntecomp4))

        dlg.area = uic.loadUi("Area.ui")
        dlg.area.show()
        dlg.area.label.setText("ΔTmin\N{SUBSCRIPT TWO} :  "+str(round(float(dlg.DTMIN2.text()),5)))
        dlg.area.label.setFont(QFont('Arial', 14))
        dlg.area.label.setStyleSheet("font-weight: bold")
        row = 0
        dlg.area.TABELA.setRowCount(len(areak) + 1)

        for data in range(0, len(areak)):
            dlg.area.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data],2))))
            dlg.area.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data + 1],2))))
            dlg.area.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data],2))))
            dlg.area.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data + 1],2))))
            dlg.area.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(round(cpq[data],2))))
            dlg.area.TABELA.setItem(row, 5, QtWidgets.QTableWidgetItem(str(round(cpf[data],2))))
            dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str(round(deltalmnk[data],2))))
            dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round(areak[data],2))))
            row += 1
        dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str('Total Area:')))
        dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round((akt),2))))

        ##################acaba aq
        for i in range(0, contador):
            correntecomp4.pop()
    except:
        try:
            f=float(dlg.DTMIN2.text())
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("font-weight: bold")
            msg.setStyleSheet("text-align:center")
            msg.setText("Please input utility data in 'Streams' tab")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setStyleSheet("font-weight: bold")
            msg.setStyleSheet("text-align:center")
            msg.setText("Please input ΔTmin₂ data")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

def OPTA():
    contador = 0
    correntecomp4 = correntenutilidade
    uf1, uq1,_,_ = fp2.pontopinch(correntenutilidade, len(correntenutilidade), float(dtopt))
    for i in range(0, len(ccopi)):
        if ccopi[i][3] == 'Cold':
            ccopi[i][2] = uf1 / (ccopi[i][1] - ccopi[i][0])

            correntecomp4.append(ccopi[i])
            contador += 1
        else:
            ccopi[i][2] = uq1 / (ccopi[i][0] - ccopi[i][1])
            correntecomp4.append(ccopi[i])
            contador += 1

    akt, _, ajustado, cpf, cpq, areak,deltalmnk = tt.CUSTO(correntecomp4, len(correntecomp4))

    dlg.area = uic.loadUi("Area.ui")
    dlg.area.show()
    dlg.area.label.setText("Optimized ΔTmin:  " + str(round(dtopt,5)))
    dlg.area.label.setFont(QFont('Arial', 14))
    dlg.area.label.setStyleSheet("font-weight: bold")
    row = 0
    dlg.area.TABELA.setRowCount(len(areak) + 1)

    for data in range(0, len(areak)):
        dlg.area.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data],2))))
        dlg.area.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data + 1],2))))
        dlg.area.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data],2))))
        dlg.area.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data + 1],2))))
        dlg.area.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(round(cpq[data],2))))
        dlg.area.TABELA.setItem(row, 5, QtWidgets.QTableWidgetItem(str(round(cpf[data],2))))
        dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str(round(deltalmnk[data],2))))
        dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round(areak[data],2))))
        row += 1
    dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str('Total Area:')))
    dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round((akt),2))))

        ##################acaba aq
    for i in range(0, contador):
        correntecomp4.pop()

kct=uic.loadUi("Select.ui")
dlg.TABELA.setColumnWidth(3,150)
#custos
dlg.CASCA.clicked.connect(lambda: CASCA())
dlg.otimizabotao.clicked.connect(lambda: eq())
kct.otimizarun.clicked.connect(lambda: otimizafun())
dlg.botaocurva.clicked.connect(lambda: plotgraficocurva())
dlg.botaocurvac.clicked.connect(lambda: plotgraficocurvacomp())
dlg.GC.clicked.connect(lambda: GC())
dlg.CUSTO.clicked.connect(lambda: mostra3())
dlg.UT.clicked.connect(lambda: mostra2())
dlg.OPTA.clicked.connect(lambda: OPTA())
dlg.AREA.clicked.connect(lambda: mostra1())
dlg.ESTIMA.clicked.connect(lambda: caxa())
dlg.ESTIMA2.clicked.connect(lambda: caxa2())
dlg.actionSave_File.triggered.connect(savefile)





#inputs e coisas com eles
def openfile_teste():
    global n, nhot, ncold, correntes

    #le o excel
    dlg.tableWidget.blockSignals(True)
    Tk().withdraw()
    filename = askopenfilename()
    workbook = xlrd.open_workbook(filename)
    worksheet = workbook.sheet_by_index(0)
    k=0
    while k != -1:
        try:
            if (worksheet.cell(k+1, 0).value) != '':
                k=k+1
                n=n+1
        except IndexError:
            break

    #armazena as correntes e calcula a quantidade de quentes e frias
    correntes = []
    dlg.tableWidget.setRowCount(n)
    for i in range (n):
        dados_da_corrente = []
        for j in range (3):
            dados_da_corrente.append(worksheet.cell(i+1, j+1).value)
        if dados_da_corrente[0] > dados_da_corrente[1]:
            dados_da_corrente.append("Hot")
            nhot += 1
        else:
            dados_da_corrente.append("Cold")
            ncold += 1
        dados_da_corrente.append(worksheet.cell(i+1, 5).value)
        correntes.append(dados_da_corrente)
        correntenutilidade.append(dados_da_corrente)
        e_utilidade.append(False)

    #printa as correntes pro usuário na tabela de streams
    for corrente in range(len(correntes)):
        for coluna in range(5):
            dlg.tableWidget.setItem(corrente, coluna, QTableWidgetItem(str(correntes[corrente][coluna])))


    dlg.tableWidget.blockSignals(False)
    for i in range(n):
        for j in range(5):
            item = dlg.tableWidget.item(i, j)
            item.setTextAlignment(Qt.AlignHCenter)

def apertaradd() :
    global n, ncold, nhot, correntes
    n += 1
    dados_da_corrente = []
    if n == 1:
        headerrr = ["Supply Temperature ({})".format(dlg.temp_unidade.currentText()),
                    "Target Temperature ({})".format(dlg.temp_unidade.currentText()),
                    "Cp ({})".format(dlg.cp_unidade.currentText()),
                    "Stream Type",
                    "h ({})".format(dlg.pelicula_unidade.currentText())]
        dlg.tableWidget.setHorizontalHeaderLabels(headerrr)
        dlg.temp_unidade.setEnabled(False)
        dlg.cp_unidade.setEnabled(False)
        dlg.pelicula_unidade.setEnabled(False)
        dlg.temp_unidade_util.setEnabled(False)
        dlg.pelicula_unidade_util.setEnabled(False)

    if float(dlg.stream_supply.text()) < float(dlg.stream_target.text()):
        tipo = "Cold"
        ncold += 1
    else:
        tipo = "Hot"
        nhot += 1

    dados_da_corrente.append(float(dlg.stream_supply.text()))
    dados_da_corrente.append(float(dlg.stream_target.text()))
    dados_da_corrente.append(float(dlg.stream_cp.text()))
    dados_da_corrente.append(tipo)
    dados_da_corrente.append(float(dlg.stream_pelicula.text()))

    dlg.tableWidget.blockSignals(True)
    dlg.tableWidget.setRowCount(n)
    dlg.tableWidget.setItem(n-1, 0, QTableWidgetItem(str(dados_da_corrente[0])))
    dlg.tableWidget.setItem(n-1, 1, QTableWidgetItem(str(dados_da_corrente[1])))
    dlg.tableWidget.setItem(n-1, 2, QTableWidgetItem(str(dados_da_corrente[2])))
    dlg.tableWidget.setItem(n-1, 3, QTableWidgetItem(dados_da_corrente[3]))
    dlg.tableWidget.setItem(n-1, 4, QTableWidgetItem(str(dados_da_corrente[4])))

    for i in range(5):
        item = dlg.tableWidget.item(n-1, i)
        item.setTextAlignment(Qt.AlignHCenter)
    correntenutilidade.append(dados_da_corrente)
    correntes.append(dados_da_corrente)
    e_utilidade.append(False)

    dlg.tableWidget.blockSignals(False)

def add_utilidade():
    global n, n_util, ncold, nhot, correntes_util,SAVEUT
    # n += 1
    n_util += 1

    dados_da_corrente = []
    if n_util == 1:
        headerrr = ["Utility",
                    "Inlet Temperature ({})".format(dlg.temp_unidade_util.currentText()),
                    "Outlet Temperature ({})".format(dlg.temp_unidade_util.currentText()),
                    "Utility Type",
                    "h ({})".format(dlg.pelicula_unidade_util.currentText())]
        dlg.tableWidget_5.setHorizontalHeaderLabels(headerrr)
        dlg.temp_unidade_util.setEnabled(False)
        dlg.temp_unidade.setEnabled(False)
        dlg.cp_unidade.setEnabled(False)
        dlg.pelicula_unidade_util.setEnabled(False)
        dlg.pelicula_unidade.setEnabled(False)

    if float(dlg.util_inlet.text()) < float(dlg.util_outlet.text()):
        tipo = "Cold"
    else:
        tipo = "Hot"

    dados_da_corrente.append(float(dlg.util_inlet.text()))
    dados_da_corrente.append(float(dlg.util_outlet.text()))
    dados_da_corrente.append(1)
    dados_da_corrente.append(tipo)
    dados_da_corrente.append(float(dlg.util_pelicula.text()))


    dlg.tableWidget_5.blockSignals(True)
    dlg.tableWidget_5.setRowCount(n_util)
    dlg.tableWidget_5.setItem(n_util-1, 0, QTableWidgetItem(dlg.utilidade.currentText()))
    dlg.tableWidget_5.setItem(n_util-1, 1, QTableWidgetItem(str(dados_da_corrente[0])))
    dlg.tableWidget_5.setItem(n_util-1, 2, QTableWidgetItem(str(dados_da_corrente[1])))
    dlg.tableWidget_5.setItem(n_util-1, 3, QTableWidgetItem(dados_da_corrente[3]))
    dlg.tableWidget_5.setItem(n_util-1, 4, QTableWidgetItem(str(dados_da_corrente[4])))

    for i in range(5):
        item = dlg.tableWidget_5.item(n_util-1, i)
        item.setTextAlignment(Qt.AlignHCenter)

    correntes_util.append(dados_da_corrente)
    ccopi.append(dados_da_corrente)
    e_utilidade.append(True)
    SAVEUT=ccopi
    print(SAVEUT)
    dlg.tableWidget_5.blockSignals(False)

def done_teste():
    global dTmin, done, correntes

    #libera o pinch e armazena as correntes numa variável que vai ser mudada de acordo com o pinch
    done = True
    dlg.pinchbutton.setEnabled(True)
    dTmin=float(dlg.lineEdit_2.text())
    pinchf, pinchq, util_quente, util_fria, coisas_graficos = pontopinch(correntes, len(correntes), dTmin)
    dlg.done = uic.loadUi("done.ui")

    dlg.done.show()
    dlg.done.hot_temp.setText("Hot: " + str(pinchq) + " " + dlg.temp_unidade.currentText())
    dlg.done.cold_temp.setText("Cold: " + str(pinchf) + " " + dlg.temp_unidade.currentText())



def pinch_teste():
    global done, Th0, Thf, CPh, Tc0, Tcf, CPc, Thf_acima, Th0_abaixo, Tc0_acima, Tcf_abaixo
    Th0, Thf, CPh, Tc0, Tcf, CPc, Thf_acima, Th0_abaixo, Tc0_acima, Tcf_abaixo = [], [], [], [], [], [], [], [], [], []

    if done:
        global correntes, correntes_util, dTmin, pinchf, pinchq, n, util_quente, util_fria, nhot, ncold
        pinchf, pinchq, util_quente, util_fria, a = pontopinch(correntes, n, dTmin)
        for util in correntes_util:
            if util[3] == "Hot":
                util[2] = util_quente/(util[0] - util[1])
                nhot += 1
            else:
                util[2] = util_fria/(util[1] - util[0])
                ncold += 1

        correntes += correntes_util
        n += len(correntes_util)
        #arruma as temperaturas baseado no pinch
        for i in range (n): #correção das temperaturas
            if correntes[i][3] == "Hot":
                correntes_quentes.append(1)
                if e_utilidade[i]:
                    e_utilidade_quente.append(True)
                else:
                    e_utilidade_quente.append(False)
                Th0.append(correntes[i][0])
                Thf.append(correntes[i][1])
                CPh.append(correntes[i][2])
                if correntes[i][1] >= pinchq: #corrente quente nao bate no pinch acima
                    Thf_acima.append(correntes[i][1])
                    corrente_quente_presente_abaixo.append(False)
                else:
                    Thf_acima.append(pinchq)
                    corrente_quente_presente_abaixo.append(True)
                if correntes[i][0] <= pinchq: #corrente quente não bate no pinch abaixo
                    Th0_abaixo.append(correntes[i][0])
                    corrente_quente_presente_acima.append(False)
                else:
                    Th0_abaixo.append(pinchq)
                    corrente_quente_presente_acima.append(True)

            if correntes[i][3] == "Cold":
                correntes_frias.append(1)
                if e_utilidade[i]:
                    e_utilidade_fria.append(True)
                else:
                    e_utilidade_fria.append(False)
                Tc0.append(correntes[i][0])
                Tcf.append(correntes[i][1])
                CPc.append(correntes[i][2])
                if correntes[i][0] >= pinchf: #corrente fria não bate no pinch acima
                    Tc0_acima.append(correntes[i][0])
                    corrente_fria_presente_abaixo.append(False)
                else:
                    Tc0_acima.append(pinchf)
                    corrente_fria_presente_abaixo.append(True)
                if correntes[i][1] <= pinchf: #corrente fria não bate no pinch abaixo
                    Tcf_abaixo.append(correntes[i][1])
                    corrente_fria_presente_acima.append(False)
                else:
                    Tcf_abaixo.append(pinchf)
                    corrente_fria_presente_acima.append(True)
        #manda tudo pro backend
        receber_pinch(Th0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, Thf_acima, Tc0_acima)
        receber_pinch_abaixo(Thf, Tc0, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, Th0_abaixo, Tcf_abaixo)
        printar()
        printar_abaixo()
        correntesnoscombos(nhot,ncold)
        testar_correntes(dlg, True)
        testar_correntes_abaixo(dlg)


        #libera botões e coisas
        dlg.tabWidget.setTabEnabled(1,True)
        dlg.tabWidget.setTabEnabled(2,True)
        dlg.tabWidget.setTabEnabled(3,True)
        dlg.tabWidget.setTabEnabled(4,True)
        dlg.comboBox_50.setEnabled(True)
        dlg.comboBox_51.setEnabled(True)
        dlg.comboBox_53.setEnabled(True)
        dlg.comboBox_54.setEnabled(True)

def correntesnoscombos(nhot,ncold):
    nstages=1
    nsubstages=20
    for i in range (nhot):
        dlg.comboBox_2.addItem(str(i+1)) #acima   add heat ex
        dlg.comboBox_9.addItem(str(i+1)) #acima   quadro de correntes quentes
        dlg.comboBox_35.addItem(str(i+1))   #abaixo   add heat ex
        dlg.comboBox_43.addItem(str(i+1))#abaixo   quadro de correntes quentes
        dlg.comboBox_51.addItem(str(i+1))	#n max de sub frias é o número de correntes quentes
        dlg.comboBox_54.addItem(str(i+1))
    for i in range (ncold):
        dlg.comboBox_5.addItem(str(i+1))  #acima add heat ex
        dlg.comboBox_10.addItem(str(i+1)) #acima quadro correntes frias
        dlg.comboBox_36.addItem(str(i+1)) #abaixo add heat ex
        dlg.comboBox_44.addItem(str(i+1)) #abaixo quadro de correntes frias
        dlg.comboBox_50.addItem(str(i+1))	#n max de sub quentes é o nomero de correntes frias
        dlg.comboBox_53.addItem(str(i+1))



#parte de desenhos
def desenhar_rede(correntes_quentes, correntes_frias):
    global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo
    turtle.delay(0)
    turtle.setup(width=1.0, height=1.0)
    temp = turtle.Turtle()
    temp.speed(1000)
    temp.shapesize(0.001, 0.001, 0.001)
    temp.penup()
    y_acima, y_abaixo = 200, 200

    def quentes(onde, correntes_desenho, presente):
        global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo
        distancia_x = 500
        for i in range(len(correntes_desenho)):
            if presente[i]:
                correntes_desenho[i] = turtle.Turtle()
                correntes_desenho[i].speed(1000)
                if e_utilidade_quente[i]:
                    correntes_desenho[i].color("orange")
                else:
                    correntes_desenho[i].color("red")
                correntes_desenho[i].pensize(3)
                correntes_desenho[i].penup()
                correntes_desenho_sub_acima = [0] * nhot
                correntes_desenho_sub_abaixo = [0] * nhot
                if onde == "above":
                    correntes_desenho[i].setx(-distancia_x)
                    correntes_desenho[i].sety(y_acima)
                    correntes_desenho[i].pendown()
                    temp.sety(y_acima - 8)
                    temp.setx(-distancia_x - len(str(Th0[i]))*6 - 4)
                    temp.write(str(Th0[i]), align="left", font=("Arial", 10, "normal"))
                    if Thf_acima[i] != pinchq:
                        temp.setx(-94)
                        temp.write(str(Thf_acima[i]), align="left", font=("Arial", 10, "normal"))
                    if not dividida_quente[i]:
                        temp.setx(-distancia_x - 138)
                        temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]))), align="left", font=("Arial", 10, "normal"))
                    else:
                        correntes_desenho_sub_acima[i] = [0] * (quantidade_quente[i] - 1)
                        for j in range(quantidade_quente[i]-1):
                            temp.sety(y_acima - 8)
                            temp.setx(-distancia_x - 138)
                            temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]*fracoes_quentes[i][j]))), align="left", font=("Arial", 10, "normal"))
                            correntes_desenho_sub_acima[i][j] = turtle.Turtle()
                            correntes_desenho_sub_acima[i][j].color("red")
                            correntes_desenho_sub_acima[i][j].pensize(3)
                            correntes_desenho_sub_acima[i][j].shapesize(0.001, 0.001, 0.001)
                            correntes_desenho_sub_acima[i][j].penup()
                            correntes_desenho_sub_acima[i][j].setx(-distancia_x + 20)
                            correntes_desenho_sub_acima[i][j].sety(y_acima)
                            correntes_desenho_sub_acima[i][j].pendown()
                            correntes_desenho_sub_acima[i][j].right(90)
                            correntes_desenho_sub_acima[i][j].forward(30)
                            correntes_desenho_sub_acima[i][j].left(90)
                            if Thf_acima[i] == pinchq:
                                correntes_desenho_sub_acima[i][j].forward(distancia_x - 44)
                            else:
                                correntes_desenho_sub_acima[i][j].forward(distancia_x - 140)
                            correntes_desenho_sub_acima[i][j].left(90)
                            correntes_desenho_sub_acima[i][j].forward(30*(j+1))
                            correntes_desenho_sub_acima[i][j].right(90)
                            correntes_desenho_sub_acima[i][j].forward(20)
                            y_acima -= 30
                        temp.sety(y_acima - 8)
                        temp.setx(-distancia_x - 138)
                        temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]*fracoes_quentes[i][quantidade_quente[i]-1]))), align="left", font=("Arial", 10, "normal"))
                    if Thf_acima[i] == pinchq:
                        correntes_desenho[i].forward(distancia_x - 4)
                    else:
                        correntes_desenho[i].forward(distancia_x - 100)
                elif onde == "below":
                    correntes_desenho[i].sety(y_abaixo)
                    temp.sety(y_abaixo - 8)
                    temp.setx(distancia_x + 6)
                    temp.write(str(Thf[i]), align="left", font=("Arial", 10, "normal"))
                    if Th0_abaixo[i] != pinchq:
                        temp.setx(100 - len(str(Th0[i]))*6 - 4)
                        temp.write(str(Th0_abaixo[i]), align="left", font=("Arial", 10, "normal"))
                    temp.setx(distancia_x + 90)
                    if not dividida_quente_abaixo[i]:
                        temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]))), align="left", font=("Arial", 10, "normal"))
                    else:
                        correntes_desenho_sub_abaixo[i] = [0] * (quantidade_quente_abaixo[i] - 1)
                        for j in range(quantidade_quente_abaixo[i]-1):
                            temp.sety(y_abaixo - 8)
                            temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]*fracoes_quentes_abaixo[i][j]))), align="left", font=("Arial", 10, "normal"))
                            correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
                            correntes_desenho_sub_abaixo[i][j].color("red")
                            correntes_desenho_sub_abaixo[i][j].pensize(3)
                            correntes_desenho_sub_abaixo[i][j].shapesize(0.001, 0.001, 0.001)
                            correntes_desenho_sub_abaixo[i][j].penup()
                            correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
                            if Th0_abaixo[i] == pinchq:
                                correntes_desenho_sub_abaixo[i][j].setx(24)
                                correntes_desenho_sub_abaixo[i][j].pendown()
                                correntes_desenho_sub_abaixo[i][j].right(90)
                                correntes_desenho_sub_abaixo[i][j].forward(30)
                                correntes_desenho_sub_abaixo[i][j].left(90)
                                if calor_atual_quente_abaixo[i] == 0 and not any(e_utilidade_quente):
                                    correntes_desenho_sub_abaixo[i][j].forward(len(matriz_trocadores_abaixo)*50)
                                else:
                                    correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 44)
                            else:
                                correntes_desenho_sub_abaixo[i][j].setx(120)
                                correntes_desenho_sub_abaixo[i][j].pendown()
                                correntes_desenho_sub_abaixo[i][j].right(90)
                                correntes_desenho_sub_abaixo[i][j].forward(30)
                                correntes_desenho_sub_abaixo[i][j].left(90)
                                if calor_atual_quente_abaixo[i] == 0 and not any(e_utilidade_quente):
                                    correntes_desenho_sub_abaixo[i][j].forward(len(matriz_trocadores_abaixo)*50)
                                else:
                                    correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 140)
                            correntes_desenho_sub_abaixo[i][j].left(90)
                            correntes_desenho_sub_abaixo[i][j].forward(30*(j+1))
                            correntes_desenho_sub_abaixo[i][j].right(90)
                            correntes_desenho_sub_abaixo[i][j].forward(20)
                            y_abaixo -= 30
                        temp.sety(y_abaixo - 8)
                        temp.write("CP = " + str(float('{:.3f}'.format(CPh[i]*fracoes_quentes_abaixo[i][quantidade_quente_abaixo[i]-1]))), align="left", font=("Arial", 10, "normal"))
                    if Th0_abaixo[i] == pinchq:
                        correntes_desenho[i].setx(4)
                        correntes_desenho[i].pendown()
                        correntes_desenho[i].forward(distancia_x - 4)
                    else:
                        correntes_desenho[i].setx(100)
                        correntes_desenho[i].pendown()
                        correntes_desenho[i].forward(distancia_x - 100)
            if onde == "above":
                if dividida_quente[i] and dividida_quente_abaixo[i]:
                    if quantidade_quente[i] < quantidade_quente_abaixo[i]:
                        y_acima -= 30 * (quantidade_quente_abaixo[i] - quantidade_quente[i])
                elif dividida_quente_abaixo[i]:
                    y_acima -= 30 * (quantidade_quente_abaixo[i] - 1)
            elif onde == "below":
                if dividida_quente[i] and dividida_quente_abaixo[i]:
                    if quantidade_quente[i] > quantidade_quente_abaixo[i]:
                        y_abaixo -= 30 * (quantidade_quente[i] - quantidade_quente_abaixo[i])
                elif dividida_quente[i]:
                    y_abaixo -= 30 * (quantidade_quente[i] - 1)
            y_acima -= 30
            y_abaixo -= 30

    def frias(onde, correntes_desenho, presente):
        global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo
        distancia_x = 500
        for i in range(len(correntes_desenho)):
            if presente[i]:
                correntes_desenho[i] = turtle.Turtle()
                correntes_desenho[i].speed(1000)
                if e_utilidade_fria[i]:
                    correntes_desenho[i].color("#7FFFD4")
                else:
                    correntes_desenho[i].color("blue")
                correntes_desenho[i].pensize(3)
                correntes_desenho[i].penup()
                correntes_desenho_sub_acima = [0] * ncold
                correntes_desenho_sub_abaixo = [0] * ncold
                if onde == "above":
                    correntes_desenho[i].sety(y_acima)
                    correntes_desenho[i].left(180)
                    temp.sety(y_acima - 8)
                    temp.setx(-distancia_x - len(str(Tcf[i]))*6 - 4)
                    temp.write(str(Tcf[i]), align="left", font=("Arial", 10, "normal"))
                    if Tc0_acima[i] != pinchf:
                        temp.setx(-94)
                        temp.write(str(Tc0_acima[i]), align="left", font=("Arial", 10, "normal"))
                    temp.setx(-distancia_x - 138)
                    if not dividida_fria[i]:
                        temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]))), align="left", font=("Arial", 10, "normal"))
                    else:
                        correntes_desenho_sub_acima[i] = [0] * (quantidade_fria[i] - 1)
                        for j in range(quantidade_fria[i] - 1):
                            temp.sety(y_acima - 8)
                            temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]*fracoes_frias[i][j]))), align="left", font=("Arial", 10, "normal"))
                            correntes_desenho_sub_acima[i][j] = turtle.Turtle()
                            correntes_desenho_sub_acima[i][j].color("blue")
                            correntes_desenho_sub_acima[i][j].pensize(3)
                            correntes_desenho_sub_acima[i][j].shapesize(0.001, 0.001, 0.001)
                            correntes_desenho_sub_acima[i][j].penup()
                            correntes_desenho_sub_acima[i][j].sety(y_acima)
                            if Tc0_acima[i] == pinchf:
                                correntes_desenho_sub_acima[i][j].setx(-24)
                                correntes_desenho_sub_acima[i][j].pendown()
                                correntes_desenho_sub_acima[i][j].right(90)
                                correntes_desenho_sub_acima[i][j].forward(30)
                                correntes_desenho_sub_acima[i][j].right(90)
                                if calor_atual_frio[i] == 0 and not any(e_utilidade_quente):
                                    correntes_desenho_sub_acima[i][j].forward(len(matriz_armazenada)*50)
                                else:
                                    correntes_desenho_sub_acima[i][j].forward(distancia_x - 44)
                            else:
                                correntes_desenho_sub_acima[i][j].setx(-120)
                                correntes_desenho_sub_acima[i][j].pendown()
                                correntes_desenho_sub_acima[i][j].right(90)
                                correntes_desenho_sub_acima[i][j].forward(30)
                                correntes_desenho_sub_acima[i][j].right(90)
                                if calor_atual_frio[i] == 0 and not any(e_utilidade_quente):
                                    correntes_desenho_sub_acima[i][j].forward(len(matriz_armazenada)*50)
                                else:
                                    correntes_desenho_sub_acima[i][j].forward(distancia_x - 140)
                            correntes_desenho_sub_acima[i][j].right(90)
                            correntes_desenho_sub_acima[i][j].forward(30*(j+1))
                            correntes_desenho_sub_acima[i][j].left(90)
                            correntes_desenho_sub_acima[i][j].forward(20)
                            y_acima -= 30
                        temp.sety(y_acima - 8)
                        temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]*fracoes_frias[i][quantidade_fria[i]-1]))), align="left", font=("Arial", 10, "normal"))
                    if Tc0_acima[i] == pinchf:
                        correntes_desenho[i].setx(-4)
                        correntes_desenho[i].pendown()
                        correntes_desenho[i].forward(distancia_x - 4)
                    else:
                        correntes_desenho[i].setx(-100)
                        correntes_desenho[i].pendown()
                        correntes_desenho[i].forward(distancia_x - 100)
                elif onde == "below":
                    correntes_desenho[i].sety(y_abaixo)
                    correntes_desenho[i].left(180)
                    correntes_desenho[i].setx(distancia_x)
                    correntes_desenho[i].pendown()
                    temp.sety(y_abaixo - 8)
                    temp.setx(distancia_x + 6)
                    temp.write(str(Tc0[i]), align="left", font=("Arial", 10, "normal"))
                    if Tcf_abaixo[i] != pinchf:
                        temp.setx(100 - len(str(Tcf_abaixo[i]))*6 - 4)
                        temp.write(str(Tcf_abaixo[i]), align="left", font=("Arial", 10, "normal"))
                    temp.setx(distancia_x + 90)
                    if not dividida_fria_abaixo[i]:
                        temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]))), align="left", font=("Arial", 10, "normal"))
                    else:
                        correntes_desenho_sub_abaixo[i] = [0] * (quantidade_fria_abaixo[i] - 1)
                        for j in range(quantidade_fria_abaixo[i]-1):
                            temp.sety(y_abaixo - 8)
                            temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]*fracoes_frias_abaixo[i][j]))), align="left", font=("Arial", 10, "normal"))
                            correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
                            correntes_desenho_sub_abaixo[i][j].color("blue")
                            correntes_desenho_sub_abaixo[i][j].pensize(3)
                            correntes_desenho_sub_abaixo[i][j].shapesize(0.001, 0.001, 0.001)
                            correntes_desenho_sub_abaixo[i][j].penup()
                            correntes_desenho_sub_abaixo[i][j].setx(distancia_x - 20)
                            correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
                            correntes_desenho_sub_abaixo[i][j].pendown()
                            correntes_desenho_sub_abaixo[i][j].right(90)
                            correntes_desenho_sub_abaixo[i][j].forward(30)
                            correntes_desenho_sub_abaixo[i][j].right(90)
                            if Tcf_abaixo[i] == pinchf:
                                correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 44)
                            else:
                                correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 140)
                            correntes_desenho_sub_abaixo[i][j].right(90)
                            correntes_desenho_sub_abaixo[i][j].forward(30*(j+1))
                            correntes_desenho_sub_abaixo[i][j].left(90)
                            correntes_desenho_sub_abaixo[i][j].forward(20)
                            y_abaixo -= 30
                        temp.sety(y_abaixo - 8)
                        temp.write("CP = " + str(float('{:.3f}'.format(CPc[i]*fracoes_frias_abaixo[i][quantidade_fria_abaixo[i]-1]))), align="left", font=("Arial", 10, "normal"))
                    if Tcf_abaixo[i] == pinchf:
                        correntes_desenho[i].forward(distancia_x - 4)
                    else:
                        correntes_desenho[i].forward(distancia_x - 100)
            if onde == "above":
                if dividida_fria_abaixo[i] and dividida_fria[i]:
                    if quantidade_fria_abaixo[i] > quantidade_fria[i]:
                        y_acima -= 30 * (quantidade_fria_abaixo[i] - quantidade_fria[i])
                elif dividida_fria_abaixo[i]:
                    y_acima -= 30 * (quantidade_fria_abaixo[i] - 1)
            elif onde == "below":
                if dividida_fria[i] and dividida_fria_abaixo[i]:
                    if quantidade_fria[i] > quantidade_fria_abaixo[i]:
                        y_abaixo -= 30 * (quantidade_fria[i] - quantidade_fria_abaixo[i])
                elif dividida_fria[i]:
                    y_abaixo -= 30 * (quantidade_fria[i] - 1)

            y_acima -= 30
            y_abaixo -= 30

    def pinch(tamanho):
        pinch = turtle.Turtle()
        pinch.speed(1000)
        pinch.shapesize(0.001, 0.001, 0.001)
        pinch.pensize(2)
        pinch.right(90)
        pinch.penup()
        pinch.sety(235)
        temp.sety(240)
        temp.setx(-len(str(pinchq))*3)
        temp.write(str(pinchq), align="left", font=("Arial", 10, "normal"))
        temp.right(90)
        tamanho = 235 - tamanho
        if str(tamanho)[-1] == 5:
            tamanho += 5

        for i in range(int(tamanho/10)+1):
            pinch.pendown()
            pinch.forward(5)
            pinch.penup()
            pinch.forward(5)
            temp.forward(10)
        temp.forward(20)
        temp.write(str(pinchf), align="left", font=("Arial", 10, "normal"))

    def inserir_trocador_desenho(onde, corrente_quente, corrente_fria, subestagio, trocadorr):
        trocador = turtle.Turtle()
        trocador.speed(1000)
        trocador.pensize(1.5)
        if e_utilidade_quente[trocadorr[0]-1]:
            trocador.color("black", "orange")
        elif e_utilidade_fria[trocadorr[1]-1]:
            trocador.color("black", "#7FFFD4")
        else:
            trocador.color("black", "white")
        trocador.shapesize(0.001, 0.001, 0.001)
        trocador.penup()
        if onde == "above":
            trocador.setx(-subestagio*50)
            temp.setx(-subestagio*50 - len(str(float('{:.3f}'.format(trocadorr[6]))))*3)
            if dividida_quente[trocadorr[0]-1]:
                trocador.sety(corrente_quente.pos()[1] - 10 - 30*(trocadorr[2]-1))
                temp.sety(corrente_quente.pos()[1] + 10 - 30*(trocadorr[2]-1))
            else:
                trocador.sety(corrente_quente.pos()[1]-10)
                temp.sety(corrente_quente.pos()[1]+10)
            trocador.pendown()
            trocador.begin_fill()
            trocador.circle(10)
            trocador.end_fill()
            if dividida_fria[trocadorr[1]-1]:
                trocador.sety(corrente_fria.pos()[1] - 10 - 30*(trocadorr[3]-1))
            else:
                trocador.sety(corrente_fria.pos()[1] - 10)
            trocador.begin_fill()
            trocador.circle(10)
            trocador.end_fill()
        elif onde == "below":
            trocador.setx(subestagio*50)
            temp.setx(subestagio*50 - len(str(trocadorr[6]))*3)
            if dividida_quente_abaixo[trocadorr[0]-1]:
                trocador.sety(corrente_quente.pos()[1] - 10 - 30*(trocadorr[2]-1))
                temp.sety(corrente_quente.pos()[1] + 10 - 30*(trocadorr[2]-1))
            else:
                trocador.sety(corrente_quente.pos()[1]-10)
                temp.sety(corrente_quente.pos()[1]+10)
            trocador.pendown()
            trocador.begin_fill()
            trocador.circle(10)
            trocador.end_fill()
            if dividida_fria_abaixo[trocadorr[1]-1]:
                trocador.sety(corrente_fria.pos()[1] - 10 - 30*(trocadorr[3]-1))
            else:
                trocador.sety(corrente_fria.pos()[1] - 10)
            trocador.begin_fill()
            trocador.circle(10)
            trocador.end_fill()

        temp.write(str(float('{:.3f}'.format(trocadorr[6]))), align="left", font=("Arial", 10, "normal"))

    def utilidade_desenho(onde, corrente, subestagio, calor):
        utilidade = turtle.Turtle()
        utilidade.speed(1000)
        utilidade.pensize(1.5)
        utilidade.shapesize(0.001, 0.001, 0.001)
        utilidade.penup()
        if onde == "above":
            utilidade.color("black", "orange")
            utilidade.setx(-subestagio*50)
            temp.setx(-subestagio*50 - len(str(calor))*3)
        elif onde == "below":
            utilidade.color("black", "#7FFFD4")
            utilidade.setx(subestagio*50)
            temp.setx(subestagio*50 - len(str(calor))*3)
        utilidade.sety(corrente.pos()[1]-10)
        utilidade.pendown()
        utilidade.begin_fill()
        utilidade.circle(10)
        utilidade.end_fill()
        temp.sety(corrente.pos()[1]+10)
        temp.write(str(calor), align="left", font=("Arial", 10, "normal"))


    quentes("above", correntes_quentes, corrente_quente_presente_acima)
    frias("above", correntes_frias, corrente_fria_presente_acima)
    tamanho_acima = y_acima
    y_acima, y_abaixo = 200, 200
    quentes("below", correntes_quentes, corrente_quente_presente_abaixo)
    frias("below", correntes_frias, corrente_fria_presente_abaixo)
    tamanho_abaixo = y_abaixo
    if tamanho_acima > tamanho_abaixo:
        tamanho = tamanho_acima
    else:
        tamanho = tamanho_abaixo
    pinch(tamanho)

    if len(matriz_armazenada) > 0:
        subestagio = 0
        foi_pra_frente = False
        i = 0
        for trocadorr in matriz_armazenada:
            if Thf_acima[trocadorr[0]-1] != pinchq:
                if not foi_pra_frente and i < 2:
                    subestagio += 2 - i
                    foi_pra_frente = True
            if Tc0_acima[trocadorr[1]-1] != pinchf:
                if not foi_pra_frente and i < 2:
                    subestagio += 2 - i
                    foi_pra_frente = True
            subestagio += 1
            i += 1
            inserir_trocador_desenho("above", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr)

        if len(utilidades) > 0:
            for utilidadee in utilidades:
                subestagio += 1
                utilidade_desenho("above", correntes_frias[utilidadee[0]-1], subestagio, utilidadee[1])

    if len(matriz_trocadores_abaixo) > 0:
        subestagio = 0
        foi_pra_frente = False
        i = 0
        for trocadorr in matriz_trocadores_abaixo:
            if Th0_abaixo[trocadorr[0]-1] != pinchq:
                if not foi_pra_frente and i < 2:
                    subestagio += 2 - i
                    foi_pra_frente = True
            if Tcf_abaixo[trocadorr[1]-1] != pinchf:
                if not foi_pra_frente and i < 2:
                    subestagio += 2 - i
                    foi_pra_frente = True
            subestagio += 1
            i += 1
            inserir_trocador_desenho("below", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr)

        if len(utilidades_abaixo) > 0:
            for utilidadee in utilidades_abaixo:
                subestagio += 1
                utilidade_desenho("below", correntes_quentes[utilidadee[0]-1], subestagio, utilidadee[1])

    # salvar_rede()
    turtle.done()
    # turtle.bye()

    # dlg.rede_teste = uic.loadUi("tela_rede.ui")
    # dlg.rede = QPixmap("image.png")
    # dlg.label_ooi = QtWidgets.QLabel(dlg)
    # dlg.label_ooi.setPixmap(dlg.rede)
    # dlg.label_ooi.setAlignment(QtCore.Qt.AlignCenter)
    # dlg.label_ooi.setScaledContents(True)
    # dlg.rede_teste.verticalLayout_2.addWidget(dlg.label_ooi)
    # dlg.rede_teste.show()
    # dlg.rede_teste.showMaximized()

def salvar_rede():
    turtle.getscreen()
    turtle.getcanvas().postscript(file="duck.eps")
    TARGET_BOUNDS = (2000, 2000)
    pic = Image.open('duck.eps')
    pic.load(scale=10)
    if pic.mode in ('P', '1'):
        pic = pic.convert("RGB")
        ratio = min(TARGET_BOUNDS[0] / pic.size[0],
                    TARGET_BOUNDS[1] / pic.size[1])
    new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))
    pic = pic.resize(new_size, Image.ANTIALIAS)
    pic.save("image.png")



def violou_dtmin(trocador_violado, onde, dados_do_trocador):
    dlg.dtmin = uic.loadUi("dtmin.ui")
    dlg.dtmin.show()
    text = "ΔT = " + str(float('{:.1f}'.format(trocador_violado[6])))
    textfrio = "ΔT = " + str(float('{:.1f}'.format(trocador_violado[7])))

    if onde == "above":
        dlg.dtmin.label_7.setText(str(len(matriz_armazenada)))
        dlg.dtmin.pushButton.clicked.connect(lambda: above(dados_do_trocador))
    if onde == "below":
        dlg.dtmin.label_7.setText(str(len(matriz_trocadores_abaixo)))
        dlg.dtmin.pushButton.clicked.connect(lambda: below(dados_do_trocador))

    dlg.dtmin.label_3.setText(text)
    dlg.dtmin.label_4.setText(textfrio)

    if trocador_violado[6] < dTmin:
        dlg.dtmin.label_3.setStyleSheet("QLabel {color: red}")
    if trocador_violado[7] < dTmin:
        dlg.dtmin.label_4.setStyleSheet("QLabel {color: red}")

    dlg.dtmin.pushButton_2.clicked.connect(lambda: dlg.dtmin.close())


    def above(dados_do_trocador):
        global subestagio_trocador
        indice = len(matriz_armazenada) - 1
        remover_trocador(dlg, dados_do_trocador, indice, matriz_armazenada)
        printar()
        checaresgotadosacima()
        dlg.dtmin.close()
        subestagio_trocador = indice

    def below(dados_do_trocacdor):
        global subestagio_trocador_abaixo
        indice = len(matriz_trocadores_abaixo) - 1
        remover_trocador_abaixo(dlg, dados_do_trocador, indice, matriz_trocadores_abaixo)
        printar_abaixo()
        checaresgotadosabaixo()
        dlg.dtmin.close()
        subestagio_trocador_abaixo = indice

def dividir_corrente(divisao, onde):
    global divtype
    divtype = divisao
    dlg.DivisaoQuente = uic.loadUi("DivisaoQuente.ui")
    dlg.DivisaoFria = uic.loadUi("DivisaoQuente.ui")
    if divtype == "Q":
        for i in range(nhot):
            dlg.DivisaoQuente.comboBox_2.addItem(str(i+1))
        for i in range(nstages):
            dlg.DivisaoQuente.comboBox.addItem(str(i+1))
        for i in range(ncold):
            dlg.DivisaoQuente.comboBox_3.addItem(str(i+1))
        dlg.DivisaoQuente.show()
    elif divtype == "F":
        dlg.DivisaoFria.label_5.setText("Split Cold Stream")
        for i in range(ncold):
            dlg.DivisaoFria.comboBox_2.addItem(str(i+1))
        for i in range(nstages):
            dlg.DivisaoFria.comboBox.addItem(str(i+1))
        for i in range(nhot):
            dlg.DivisaoFria.comboBox_3.addItem(str(i+1))
        dlg.DivisaoFria.show()


    def confirm():
        global caixa_fracao, quantidade, corrente, estagio
        if divtype == "Q":
            quantidade = int(dlg.DivisaoQuente.comboBox_3.currentText())
            estagio = int(dlg.DivisaoQuente.comboBox.currentText())
            corrente = int(dlg.DivisaoQuente.comboBox_2.currentText())
        if divtype == "F":
            quantidade = int(dlg.DivisaoFria.comboBox_3.currentText())
            estagio = int(dlg.DivisaoFria.comboBox.currentText())
            corrente = int(dlg.DivisaoFria.comboBox_2.currentText())

        if verificar_trocador_estagio(estagio) and onde == "above":
            QMessageBox.about(dlg, "Error!", "There is already a heat exchanger in this position, remove it before making the division.")
            return

        if verificar_trocador_estagio_abaixo(estagio) and onde == "below":
            QMessageBox.about(dlg, "Error!", "There is already a heat exchanger in this position, remove it before making the division.")
            return

        if divtype == "Q":
            dlg.DivisaoQuente.pushButton_3.setEnabled(True)
            dlg.DivisaoQuente.pushButton.setEnabled(False)
        if divtype == "F":
            dlg.DivisaoFria.pushButton_3.setEnabled(True)
            dlg.DivisaoFria.pushButton.setEnabled(False)

        caixa_fracao = [0] * quantidade
        caixa_corrente = [0] * quantidade

        for i in range(quantidade):
            caixa_fracao[i] = QtWidgets.QDoubleSpinBox(dlg)
            caixa_corrente[i] = QtWidgets.QLabel(dlg)
            if divtype == "Q":
                dlg.DivisaoQuente.verticalLayout_3.addWidget(caixa_corrente[i])
                dlg.DivisaoQuente.verticalLayout_3.addWidget(caixa_fracao[i])
            if divtype == "F":
                dlg.DivisaoFria.verticalLayout_3.addWidget(caixa_corrente[i])
                dlg.DivisaoFria.verticalLayout_3.addWidget(caixa_fracao[i])
            caixa_fracao[i].setSingleStep(float(0.1))
            caixa_fracao[i].setMaximum(1)
            caixa_fracao[i].setMinimum(0)
            caixa_fracao[i].setValue(round(1/quantidade, 2))
            caixa_corrente[i].setText("Substream {}".format(i+1))
            caixa_corrente[i].setAlignment(Qt.AlignCenter)
            caixa_fracao[i].setAlignment(Qt.AlignCenter)
        x = caixa_fracao[-1].value()
        if x * quantidade > 1:
            sobrou = x*quantidade - 1
            caixa_fracao[-1].setValue(x - sobrou)
        if x * quantidade < 1:
            faltou = 1 - x*quantidade
            caixa_fracao[-1].setValue(x + faltou)


    def split(onde):
        soma = 0
        fracao = [0] * quantidade
        for i in range(quantidade):
            soma += round(float(caixa_fracao[i].value()), 2)
            fracao[i] = round(float(caixa_fracao[i].value()), 2)
        if soma != 1:
            QMessageBox.about(dlg, "Error!", "The sum of the fractions must be equals 1.")
            return

        if onde == "above":
            divisao_de_correntes(divtype, estagio, corrente, quantidade, fracao)
            if divtype == "F":
                testar_correntes(dlg, True)
            else:
                testar_correntes(dlg)
        elif onde == "below":
            divisao_de_correntes_abaixo(divtype, estagio, corrente, quantidade, fracao)
            if divtype == "Q":
                testar_correntes_abaixo(dlg, True)
            else:
                testar_correntes_abaixo(dlg)

        if divtype == "Q":
            dlg.DivisaoQuente.close()
        if divtype == "F":
            dlg.DivisaoFria.close()

        printar()

    dlg.DivisaoQuente.pushButton.clicked.connect(lambda: confirm())
    dlg.DivisaoQuente.pushButton_3.clicked.connect(lambda: split(onde))
    dlg.DivisaoQuente.pushButton_2.clicked.connect(lambda: dlg.DivisaoQuente.close())
    dlg.DivisaoFria.pushButton.clicked.connect(lambda: confirm())
    dlg.DivisaoFria.pushButton_3.clicked.connect(lambda: split(onde))
    dlg.DivisaoFria.pushButton_2.clicked.connect(lambda: dlg.DivisaoFria.close())



#above
def printar():
    dlg.tableWidget_3.clearContents()
    dlg.tableWidget_4.clearContents()

    pinch_quente_texto = "Hot Pinch Temperature: " + str(pinchq)
    pinch_frio_texto = "Cold Pinch Temperature: " + str(pinchf)

    dlg.label_15.setText(pinch_quente_texto)
    dlg.label_12.setText(pinch_frio_texto)

    if dlg.checkBox.isChecked():
        linha = 0
        linhas = 0
        for i in quantidade_quente:
            linhas += i
        dlg.tableWidget_3.setRowCount(linhas)
        for corrente in range(nhot):
            if dividida_quente[corrente]:
                for sub in range(quantidade_quente[corrente]):
                    text = str(corrente+1) + "." + str(sub+1)
                    dlg.tableWidget_3.setItem(linha, 0, QTableWidgetItem(text))
                    dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0[corrente])))))
                    if corrente_quente_presente_acima[corrente]:
                        dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente[corrente][sub])))))
                        dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf_acima[corrente])))))
                        dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente_sub[corrente][sub])))))
                    else:
                        dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem("-"))
                        dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem("-"))
                        dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem("-"))
                        dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem("-"))
                    linha += 1
            else:
                dlg.tableWidget_3.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
                dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0[corrente])))))
                if corrente_quente_presente_acima[corrente]:
                    dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_mesclada[corrente])))))
                    dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf_acima[corrente])))))
                    dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente[corrente])))))
                else:
                    dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem("-"))
                    dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem("-"))
                    dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem("-"))
                    dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem("-"))
                linha += 1
    else:
        dlg.tableWidget_3.setRowCount(nhot)
        for corrente in range(nhot):
            dlg.tableWidget_3.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
            dlg.tableWidget_3.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0[corrente])))))
            if corrente_quente_presente_acima[corrente]:
                dlg.tableWidget_3.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_mesclada[corrente])))))
                dlg.tableWidget_3.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf_acima[corrente])))))
                dlg.tableWidget_3.setItem(corrente, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente[corrente])))))
            else:
                dlg.tableWidget_3.setItem(corrente, 1, QTableWidgetItem("-"))
                dlg.tableWidget_3.setItem(corrente, 2, QTableWidgetItem("-"))
                dlg.tableWidget_3.setItem(corrente, 3, QTableWidgetItem("-"))
                dlg.tableWidget_3.setItem(corrente, 4, QTableWidgetItem("-"))

    if dlg.checkBox_2.isChecked():
        linha = 0
        linhas = 0
        for i in quantidade_fria:
            linhas += i
        dlg.tableWidget_4.setRowCount(linhas)
        for corrente in range(ncold):
            if dividida_fria[corrente]:
                for sub in range(quantidade_fria[corrente]):
                    text = str(corrente+1) + "." + str(sub+1)
                    dlg.tableWidget_4.setItem(linha, 0, QTableWidgetItem(text))
                    dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf[corrente])))))
                    if corrente_fria_presente_acima[corrente]:
                        dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria[corrente][sub])))))
                        dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0_acima[corrente])))))
                        dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio_sub[corrente][sub])))))
                    else:
                        dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem("-"))
                        dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem("-"))
                        dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem("-"))
                        dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem("-"))
                    linha += 1
            else:
                dlg.tableWidget_4.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
                dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf[corrente])))))
                if corrente_fria_presente_acima[corrente]:
                    dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_mesclada[corrente])))))
                    dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0_acima[corrente])))))
                    dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio[corrente])))))
                else:
                    dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem("-"))
                    dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem("-"))
                    dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem("-"))
                    dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem("-"))
                linha += 1
    else:
        dlg.tableWidget_4.setRowCount(ncold)
        for corrente in range(ncold):
            dlg.tableWidget_4.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
            dlg.tableWidget_4.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf[corrente])))))
            if corrente_fria_presente_acima[corrente]:
                dlg.tableWidget_4.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_mesclada[corrente])))))
                dlg.tableWidget_4.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0_acima[corrente])))))
                dlg.tableWidget_4.setItem(corrente, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio[corrente])))))
            else:
                dlg.tableWidget_4.setItem(corrente, 1, QTableWidgetItem("-"))
                dlg.tableWidget_4.setItem(corrente, 2, QTableWidgetItem("-"))
                dlg.tableWidget_4.setItem(corrente, 3, QTableWidgetItem("-"))
                dlg.tableWidget_4.setItem(corrente, 4, QTableWidgetItem("-"))


    dlg.tableWidget_2.setRowCount(len(matriz_armazenada))
    if len(matriz_armazenada) > 0:
        for trocador in range(0, len(matriz_armazenada)):
            dlg.tableWidget_2.setItem(trocador, 0, QTableWidgetItem(str(matriz_armazenada[trocador][0]))) #chot
            dlg.tableWidget_2.setItem(trocador, 1, QTableWidgetItem(str(matriz_armazenada[trocador][1]))) #ccold
            dlg.tableWidget_2.setItem(trocador, 2, QTableWidgetItem(str(matriz_armazenada[trocador][2]))) #sbhot
            dlg.tableWidget_2.setItem(trocador, 3, QTableWidgetItem(str(matriz_armazenada[trocador][3]))) #sbcold
            dlg.tableWidget_2.setItem(trocador, 4, QTableWidgetItem(str(matriz_armazenada[trocador][4]))) #sk
            dlg.tableWidget_2.setItem(trocador, 5, QTableWidgetItem(str(matriz_armazenada[trocador][5]))) #k
            dlg.tableWidget_2.setItem(trocador, 6, QTableWidgetItem(str(float('{:.1f}'.format(matriz_armazenada[trocador][6]))))) # calor trocado
            dlg.tableWidget_2.setItem(trocador, 7, QTableWidgetItem(str(float('{:.1f}'.format(matriz_armazenada[trocador][7]))))) #Thin
            dlg.tableWidget_2.setItem(trocador, 8, QTableWidgetItem(str(float('{:.1f}'.format(matriz_armazenada[trocador][8]))))) #Tcout
            dlg.tableWidget_2.setItem(trocador, 9, QTableWidgetItem(str(matriz_armazenada[trocador][9]))) #fração hot
            dlg.tableWidget_2.setItem(trocador, 10, QTableWidgetItem(str(matriz_armazenada[trocador][10]))) #fraçao cold
        dlg.lineEdit_5.setText(str("0"))

    if len(utilidades) > 0:
        dlg.tableWidget_2.setRowCount(len(matriz_armazenada) + len(utilidades))
        for utilidade in range(0, len(utilidades)):
            dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 0, QTableWidgetItem(str("Hot Utility")))
            dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 1, QTableWidgetItem(str(utilidades[utilidade][0])))
            dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 6, QTableWidgetItem(str(float('{:.1f}'.format(utilidades[utilidade][1])))))

def inserir_teste():
    global subestagio_trocador
    subestagio_trocador += 1
    dados_do_trocador = ler_dados(dlg, subestagio_trocador)
    try:
        nova_matriz, violou, trocador_violado = inserir_trocador(dlg, dados_do_trocador)
        matriz_armazenada.append(nova_matriz[-1])
    except:
        print("erro inserir teste")
        return
    if violou:
        violou_dtmin(trocador_violado, "above", dados_do_trocador)
        printar()
        checaresgotadosacima()
    else:
        printar()
        checaresgotadosacima()

def remover_teste():
    global subestagio_trocador
    indice_remover = dlg.tableWidget_2.currentRow()
    if indice_remover == -1:
        return
    if indice_remover <= len(matriz_armazenada) - 1:
        if len(utilidades) > 0:
            for i in range(ncold, -1, -1):
                for j in range(len(utilidades)):
                    if utilidades[j][0] == i+1:
                        try:
                            remover_utilidade(i+1, j, utilidades)
                        except:
                            print("erro remover teste")
        dlg.comboBox_10.setEnabled(False)
        dlg.pushButton_8.setEnabled(False)
        for i in range(len(matriz_armazenada)-1, indice_remover-1, -1):
            trocador_remover = matriz_armazenada[i]
            remover_trocador(dlg, trocador_remover, i, matriz_armazenada)
            atualizar_matriz(matriz_armazenada)
        subestagio_trocador = indice_remover
    else:
        indice_remover = dlg.tableWidget_2.currentRow() - len(matriz_armazenada)
        utilidade_remover = utilidades[indice_remover]
        corrente_remover_utilidade = utilidade_remover[0]
        remover_utilidade(corrente_remover_utilidade, indice_remover, utilidades)
    printar()

def utilidade_teste_acima():
    corrente = int(dlg.comboBox_10.currentText())
    utilidadee = adicionar_utilidade(dlg, corrente)
    try:
        utilidades.append(utilidadee[-1])
        utilidades.sort()
    except:
        print("erro utilidade teste acima")
    printar()

def calcular_calor_teste():
    dlg.TempLoadAbove=uic.loadUi("TempLoadAbove.ui")
    dlg.TempLoadAbove.show()

    for i in range (nhot):
        dlg.TempLoadAbove.comboBox.addItem(str(i+1))
    for i in range (ncold):
        dlg.TempLoadAbove.comboBox_2.addItem(str(i+1))
    for i in range(nstages):
        dlg.TempLoadAbove.comboBox_5.addItem(str(i+1))
    for i in range(nsk):
        dlg.TempLoadAbove.comboBox_6.addItem(str(i+1))

    dlg.TempLoadAbove.comboBox.setCurrentText(str(dlg.comboBox_2.currentText()))
    dlg.TempLoadAbove.comboBox_2.setCurrentText(str(dlg.comboBox_5.currentText()))
    dlg.TempLoadAbove.comboBox_3.setCurrentText(str(dlg.comboBox_50.currentText()))
    dlg.TempLoadAbove.comboBox_4.setCurrentText(str(dlg.comboBox_51.currentText()))

    dlg.TempLoadAbove.pushButton_2.clicked.connect(lambda: dlg.TempLoadAbove.close())
    dlg.TempLoadAbove.pushButton.clicked.connect(lambda: caixa_de_temperatura(dlg))

def checaresgotadosacima():
    contadordutycold = 0
    contadordutyhot = 0

    for corrente in range(nhot):
        if calor_atual_quente[corrente] == 0:
            contadordutyhot += 1
    for corrente in range(ncold):
        if calor_atual_frio[corrente] == 0:
            contadordutycold += 1

    objetivo_quente = nhot
    objetivo_frio = ncold


    if contadordutyhot == objetivo_quente:
        dlg.comboBox_10.setEnabled(True)
        dlg.pushButton_8.setEnabled(True)
    else:
        dlg.comboBox_10.setEnabled(False)
        dlg.pushButton_8.setEnabled(False)

    if contadordutycold == objetivo_frio:
        dlg.comboBox_9.setEnabled(True)
        dlg.pushButton_7.setEnabled(True)
    else:
        dlg.comboBox_9.setEnabled(False)
        dlg.pushButton_7.setEnabled(False)

    if contadordutyhot == objetivo_quente and contadordutycold == objetivo_frio:
        dlg.comboBox_9.setEnabled(False)
        dlg.comboBox_10.setEnabled(False)
        dlg.pushButton_7.setEnabled(False)
        dlg.pushButton_8.setEnabled(False)

#below
def printar_abaixo():
    dlg.tableWidget_15.clearContents()
    dlg.tableWidget_17.clearContents()

    pinch_quente_texto = "Hot Pinch Temperature: " + str(pinchq)
    pinch_frio_texto = "Cold Pinch Temperature: " + str(pinchf)

    dlg.label_17.setText(pinch_quente_texto)
    dlg.label_21.setText(pinch_frio_texto)

    if dlg.checkBox_9.isChecked():
        linha = 0
        linhas = 0
        for i in quantidade_quente_abaixo:
            linhas += i
        dlg.tableWidget_15.setRowCount(linhas)
        for corrente in range(nhot):
            if dividida_quente_abaixo[corrente]:
                for sub in range(quantidade_quente_abaixo[corrente]):
                    text = str(corrente+1) + "." + str(sub+1)
                    dlg.tableWidget_15.setItem(linha, 0, QTableWidgetItem(text))
                    dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0_abaixo[corrente])))))
                    if corrente_quente_presente_abaixo[corrente]:
                        dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_abaixo[corrente][sub])))))
                        dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf[corrente])))))
                        dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente_sub_abaixo[corrente][sub])))))
                    else:
                        dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem("-"))
                        dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem("-"))
                        dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem("-"))
                        dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem("-"))
                    linha += 1
            else:
                dlg.tableWidget_15.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
                dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0_abaixo[corrente])))))
                if corrente_quente_presente_abaixo[corrente]:
                    dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_mesclada_abaixo[corrente])))))
                    dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf[corrente])))))
                    dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente_abaixo[corrente])))))
                else:
                    dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem("-"))
                    dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem("-"))
                    dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem("-"))
                    dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem("-"))

                linha += 1
    else:
        dlg.tableWidget_15.setRowCount(nhot)
        for corrente in range(nhot):
            dlg.tableWidget_15.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
            dlg.tableWidget_15.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(Th0_abaixo[corrente])))))
            if corrente_quente_presente_abaixo[corrente]:
                dlg.tableWidget_15.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_mesclada_abaixo[corrente])))))
                dlg.tableWidget_15.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(Thf[corrente])))))
                dlg.tableWidget_15.setItem(corrente, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente_abaixo[corrente])))))
            else:
                dlg.tableWidget_15.setItem(corrente, 1, QTableWidgetItem("-"))
                dlg.tableWidget_15.setItem(corrente, 2, QTableWidgetItem("-"))
                dlg.tableWidget_15.setItem(corrente, 3, QTableWidgetItem("-"))
                dlg.tableWidget_15.setItem(corrente, 4, QTableWidgetItem("-"))

    if dlg.checkBox_10.isChecked():
        linha = 0
        linhas = 0
        for i in quantidade_fria_abaixo:
            linhas += i
        dlg.tableWidget_17.setRowCount(linhas)
        for corrente in range(ncold):
            if dividida_fria_abaixo[corrente]:
                for sub in range(quantidade_fria_abaixo[corrente]):
                    text = str(corrente+1) + "." + str(sub+1)
                    dlg.tableWidget_17.setItem(linha, 0, QTableWidgetItem(text))
                    dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf_abaixo[corrente])))))
                    if corrente_fria_presente_abaixo[corrente]:
                        dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_abaixo[corrente][sub])))))
                        dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0[corrente])))))
                        dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio_sub_abaixo[corrente][sub])))))
                    else:
                        dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem("-"))
                        dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem("-"))
                        dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem("-"))
                        dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem("-"))
                    linha += 1
            else:
                dlg.tableWidget_17.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
                dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf_abaixo[corrente])))))
                if corrente_fria_presente_abaixo[corrente]:
                    dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_mesclada_abaixo[corrente])))))
                    dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0[corrente])))))
                    dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio_abaixo[corrente])))))
                else:
                    dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem("-"))
                    dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem("-"))
                    dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem("-"))
                    dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem("-"))
                linha += 1
    else:
        dlg.tableWidget_17.setRowCount(ncold)
        for corrente in range(ncold):
            dlg.tableWidget_17.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
            dlg.tableWidget_17.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(Tcf_abaixo[corrente])))))
            if corrente_fria_presente_abaixo[corrente]:
                dlg.tableWidget_17.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_mesclada_abaixo[corrente])))))
                dlg.tableWidget_17.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(Tc0[corrente])))))
                dlg.tableWidget_17.setItem(corrente, 4, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio_abaixo[corrente])))))
            else:
                dlg.tableWidget_17.setItem(corrente, 1, QTableWidgetItem("-"))
                dlg.tableWidget_17.setItem(corrente, 2, QTableWidgetItem("-"))
                dlg.tableWidget_17.setItem(corrente, 3, QTableWidgetItem("-"))
                dlg.tableWidget_17.setItem(corrente, 4, QTableWidgetItem("-"))


    dlg.tableWidget_14.setRowCount(len(matriz_trocadores_abaixo))
    if len(matriz_trocadores_abaixo) > 0:
        for trocador in range(0, len(matriz_trocadores_abaixo)):
            dlg.tableWidget_14.setItem(trocador, 0, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][0]))) #chot
            dlg.tableWidget_14.setItem(trocador, 1, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][1]))) #ccold
            dlg.tableWidget_14.setItem(trocador, 2, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][2]))) #sbhot
            dlg.tableWidget_14.setItem(trocador, 3, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][3]))) #sbcold
            dlg.tableWidget_14.setItem(trocador, 4, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][4]))) #sk
            dlg.tableWidget_14.setItem(trocador, 5, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][5]))) #k
            dlg.tableWidget_14.setItem(trocador, 6, QTableWidgetItem(str(float('{:.1f}'.format(matriz_trocadores_abaixo[trocador][6]))))) # calor trocado
            dlg.tableWidget_14.setItem(trocador, 7, QTableWidgetItem(str(float('{:.1f}'.format(matriz_trocadores_abaixo[trocador][7]))))) #Thin
            dlg.tableWidget_14.setItem(trocador, 8, QTableWidgetItem(str(float('{:.1f}'.format(matriz_trocadores_abaixo[trocador][8]))))) #Tcout
            dlg.tableWidget_14.setItem(trocador, 9, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][9]))) #fração hot
            dlg.tableWidget_14.setItem(trocador, 10, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][10]))) #fraçao cold
        dlg.lineEdit_25.setText(str("0"))

    if len(utilidades_abaixo) > 0:
        dlg.tableWidget_14.setRowCount(len(matriz_trocadores_abaixo) + len(utilidades_abaixo))
        for utilidade in range(0, len(utilidades_abaixo)):
            dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 0, QTableWidgetItem(str("Cold Utility")))
            dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 1, QTableWidgetItem(str(utilidades_abaixo[utilidade][0])))
            dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 6, QTableWidgetItem(str(float('{:.1f}'.format(utilidades_abaixo[utilidade][1])))))

def inserir_teste_abaixo():
    global subestagio_trocador_abaixo
    subestagio_trocador_abaixo += 1
    dados_do_trocador = ler_dados_abaixo(dlg, subestagio_trocador_abaixo)
    try:
        nova_matriz, violou, trocador_violado = inserir_trocador_abaixo(dlg, dados_do_trocador)
        matriz_trocadores_abaixo.append(nova_matriz[-1])
    except:
        print("erro, inserir teste abaixo")
        return
    if violou:
        violou_dtmin(trocador_violado, "below", dados_do_trocador)
        printar_abaixo()
        checaresgotadosabaixo()
    else:
        printar_abaixo()
        checaresgotadosabaixo()

def remover_teste_abaixo():
    global subestagio_trocador_abaixo
    indice_remover = dlg.tableWidget_14.currentRow()
    if indice_remover == -1:
        return
    if indice_remover <= len(matriz_trocadores_abaixo) - 1:
        if len(utilidades_abaixo) > 0:
            for i in range(nhot-1, -1, -1):
                for j in range(len(utilidades_abaixo)):
                    if utilidades_abaixo[j][0] == i:
                        try:
                            remover_utilidade_abaixo(i, j, utilidades_abaixo)
                        except:
                            print("erro remover teste abaixo")
        dlg.comboBox_43.setEnabled(False)
        dlg.pushButton_20.setEnabled(False)
        for i in range(len(matriz_trocadores_abaixo)-1, indice_remover-1, -1):
            trocador_remover = matriz_trocadores_abaixo[i]
            remover_trocador_abaixo(dlg, trocador_remover, i, matriz_trocadores_abaixo)
            atualizar_matriz_abaixo(matriz_trocadores_abaixo)
        subestagio_trocador_abaixo = indice_remover
    else:
        indice_remover = dlg.tableWidget_14.currentRow() - len(matriz_trocadores_abaixo)
        utilidade_remover = utilidades_abaixo[indice_remover]
        corrente_remover_utilidade = utilidade_remover[0]
        remover_utilidade_abaixo(corrente_remover_utilidade, indice_remover, utilidades_abaixo)
    printar_abaixo()

def utilidade_teste_abaixo():
    corrente = int(dlg.comboBox_43.currentText())
    utilidadee = adicionar_utilidade_abaixo(dlg, corrente)
    try:
        utilidades_abaixo.append(utilidadee[-1])
        utilidades_abaixo.sort()
    except:
        print("utilidade teste abaixo")
    printar_abaixo()

def calcular_calor_abaixo():
    dlg.TempLoadBelow = uic.loadUi("TempLoadBelow.ui")
    dlg.TempLoadBelow.show()

    for i in range(nhot):
        dlg.TempLoadBelow.comboBox.addItem(str(i+1))
    for i in range(ncold):
        dlg.TempLoadBelow.comboBox_2.addItem(str(i+1))
    for i in range(nstages):
        dlg.TempLoadBelow.comboBox_5.addItem(str(i+1))
    for i in range(nsk):
        dlg.TempLoadBelow.comboBox_6.addItem(str(i+1))

    dlg.TempLoadBelow.comboBox.setCurrentText(str(dlg.comboBox_35.currentText()))
    dlg.TempLoadBelow.comboBox_2.setCurrentText(str(dlg.comboBox_36.currentText()))
    dlg.TempLoadBelow.comboBox_3.setCurrentText(str(dlg.comboBox_53.currentText()))
    dlg.TempLoadBelow.comboBox_4.setCurrentText(str(dlg.comboBox_54.currentText()))


    dlg.TempLoadBelow.pushButton.clicked.connect(lambda: caixa_de_temperatura_abaixo(dlg))
    dlg.TempLoadBelow.pushButton_2.clicked.connect(lambda: dlg.TempLoadBelow.close())

def checaresgotadosabaixo():
    contadordutyhot=0
    contadordutycold=0

    for corrente in range(nhot):
        if dividida_quente_abaixo[corrente]:
            for sub in range(quantidade_quente_abaixo[corrente]):
                if calor_atual_quente_sub_abaixo[corrente][sub] == 0:
                    contadordutyhot += 1
        else:
            if calor_atual_quente_abaixo[corrente] == 0:
                contadordutyhot += 1
    for corrente in range(ncold):
        if dividida_fria_abaixo[corrente]:
            for sub in range(quantidade_fria_abaixo[corrente]):
                if calor_atual_frio_sub_abaixo[corrente][sub] == 0:
                    contadordutycold += 1
        else:
            if calor_atual_frio_abaixo[corrente] == 0:
                contadordutycold += 1

    objetivo_quente = 0
    objetivo_frio = 0

    for i in quantidade_quente_abaixo:
        objetivo_quente += i
    for i in quantidade_fria_abaixo:
        objetivo_frio += i

    if contadordutyhot == objetivo_quente:
        dlg.comboBox_44.setEnabled(True)
        dlg.pushButton_21.setEnabled(True)
    else:
        dlg.comboBox_44.setEnabled(False)
        dlg.pushButton_21.setEnabled(False)

    if contadordutycold == objetivo_frio:
        dlg.comboBox_43.setEnabled(True)
        dlg.pushButton_20.setEnabled(True)
    else:
        dlg.comboBox_43.setEnabled(False)
        dlg.pushButton_20.setEnabled(False)

    if contadordutyhot == objetivo_quente and contadordutycold == objetivo_frio:
        dlg.comboBox_43.setEnabled(False)
        dlg.comboBox_44.setEnabled(False)
        dlg.pushButton_20.setEnabled(False)
        dlg.pushButton_21.setEnabled(False)


#streams
# dlg.pinchbutton.setEnabled(False) #block o botao pinch até apertar done
# dlg.tabWidget.setTabEnabled(1,False) #block stream diagram até fazer o pinch
# dlg.tabWidget.setTabEnabled(2,False) #block composite curver até fazer o pinch
# dlg.tabWidget.setTabEnabled(3,False) #block heat exchangers até fazer o pinch
# dlg.tabWidget.setTabEnabled(4,True) #block heat exchangers network até fazer o pinch
dlg.botao_addstream.clicked.connect(apertaradd) #add stream
dlg.botao_addutility.clicked.connect(add_utilidade)
dlg.actionOpen.triggered.connect(lambda: os.execl(sys.executable, os.path.abspath(__file__), *sys.argv))
dlg.actionOpen_2.triggered.connect(openfile_teste) #file > open
dlg.donebutton.clicked.connect(done_teste) #done
dlg.pinchbutton.clicked.connect(pinch_teste) #pinch
#dlg.tableWidget.itemChanged.connect(itemedited)
# dlg.tempcombo1.currentIndexChanged.connect(lambda i: i == 0 and SI(dlg))
# dlg.tempcombo1.currentIndexChanged.connect(lambda i: i == 1 and sistemaingles(dlg))
# dlg.comboBox.currentIndexChanged.connect(lambda i: i == 1 and celsius(dlg))
# dlg.comboBox.currentIndexChanged.connect(lambda i: i == 0 and kelvin(dlg))
# dlg.comboBox.currentIndexChanged.connect(lambda i: i == 2 and farenheit(dlg))
# dlg.comboBox.currentIndexChanged.connect(lambda i: i == 3 and rankine(dlg))
# dlg.comboBox_3.currentIndexChanged.connect(lambda i: i == 0 and btu(dlg))
# dlg.comboBox_3.currentIndexChanged.connect(lambda i: i == 1 and kW(dlg))

#above
dlg.radioButton.toggled.connect(lambda: dlg.lineEdit_5.setEnabled(True)) #quando marca o heat load libera a linha pra digitar
dlg.radioButton_4.toggled.connect(lambda: dlg.lineEdit_5.setEnabled(False)) #block o heat load quando max heat ta ativado
dlg.radioButton_4.setChecked(True) #por padrao abre o prog com max heat selecionado
dlg.pushButton_9.clicked.connect(lambda: dividir_corrente("Q", "above"))
dlg.pushButton_13.clicked.connect(lambda: dividir_corrente("F", "above"))
dlg.comboBox_9.setEnabled(False) #corrente quente que vai utilizade
dlg.comboBox_10.setEnabled(False) #corrente fria que vai utilidade
dlg.pushButton_7.setEnabled(False) #add utility hot
dlg.pushButton_8.setEnabled(False) #add utility cold
dlg.checkBox.stateChanged.connect(printar) #show splited streams printa tudo dnv
dlg.checkBox_2.stateChanged.connect(printar) #show splited streams printa tudo dnv
dlg.pushButton_6.clicked.connect(inserir_teste) #add heat exchanger
dlg.pushButton_10.clicked.connect(remover_teste) #remove heat exchanger
dlg.pushButton_14.clicked.connect(calcular_calor_teste) #choose stream temperature to calculate heat
dlg.pushButton_8.clicked.connect(utilidade_teste_acima) #add cold utility
dlg.pushButton_16.clicked.connect(lambda: desenhar_rede(correntes_quentes, correntes_frias))
#dlg.pushButton_22.clicked.connect() aaaaaaaa botao quebra de laços acima

#below
dlg.radioButton_17.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(True)) #quando marca o heat load libera a linha pra digitar
dlg.radioButton_20.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(False)) #block o heat load quando max heat ta ativado
dlg.radioButton_20.setChecked(True) #por padrao abre o prog com max heat selecionado
dlg.pushButton_12.clicked.connect(lambda: dividir_corrente("F", "below"))
dlg.pushButton_11.clicked.connect(lambda: dividir_corrente("Q", "below"))
dlg.comboBox_43.setEnabled(False) #corrente quente que vai utilizade
dlg.comboBox_44.setEnabled(False) #corrente fria que vai utilidade
dlg.pushButton_20.setEnabled(False) #add utility hot
dlg.pushButton_21.setEnabled(False) #add utility cold
dlg.checkBox_9.stateChanged.connect(printar_abaixo) #show splited streams printa tudo dnv
dlg.checkBox_10.stateChanged.connect(printar_abaixo) #show splited streams printa tudo dnv
dlg.pushButton_18.clicked.connect(inserir_teste_abaixo) #add heat exchanger
dlg.pushButton_15.clicked.connect(remover_teste_abaixo) #remove heat exchanger
dlg.pushButton_17.clicked.connect(calcular_calor_abaixo) #choose stream temperature to calculate heat
dlg.pushButton_20.clicked.connect(utilidade_teste_abaixo) #add hot utility
dlg.pushButton_19.clicked.connect(lambda: desenhar_rede(correntes_quentes, correntes_frias))


header = dlg.tableWidget.horizontalHeader()
header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
for i in range(5):
    header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
header = dlg.tableWidget_5.horizontalHeader()
header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
for i in range(5):
    header.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)



dlg.show()
dlg.showMaximized()
app.exec()
