from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMessageBox,QTableWidget,QTableWidgetItem
from PyQt5 import QtWidgets , uic
import numpy as np
import sys
from variaveistrocador import variaveis

def VariaveisTempLoad(correntes,n,nhot,ncold,dlg,chot,ccold):

    CPh = []
    CPc = []

    for i in range(n):
            if correntes[i][3] == "Hot":
                CPh.append(correntes[i][2])
            j=0
    for i in range(n):
            if correntes[i][3] == "Cold":
                CPc.append(correntes[i][2])
                j=j+1

    chot = ccold = 0
    tempmeta = 0
    NewHeatLoad = 0

    chot = int(float(dlg.TempLoad.comboBox.currentText()))
    ccold = int(float(dlg.TempLoad.comboBox_2.currentText()))

    i = chot-1
    Thin1 = int(float(dlg.tableWidget_3.item(i,1).text()))
    j = ccold-1
    Tcin1 = int(float(dlg.tableWidget_4.item(j,1).text()))

    if dlg.TempLoad.radioButton.isChecked():                     #Inlet Hot Temperature

        tempmeta = float(dlg.TempLoad.lineEdit.text())
        NewHeatLoad = (tempmeta - Thin1)*(CPh[chot-1])#*(Fharr[estagio-1][chot-1][sbhot-1]/100))

    elif dlg.TempLoad.radioButton_2.isChecked():                    #OUTLET COLD TEMPERATURE
        tempmeta = float(dlg.TempLoad.lineEdit_2.text())
        NewHeatLoad = (tempmeta - Tcin1)*(CPc[ccold-1])#*(Fcarr[estagio-1][ccold-1][sbcold-1]/100))
        

    return NewHeatLoad