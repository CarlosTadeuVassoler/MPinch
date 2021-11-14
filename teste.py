from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

app = QtWidgets.QApplication([])
dlg = uic.loadUi("teste.ui")

temperatura = [[70], [70]]
pinchq = 70
objetivo = [170, 150]
calor = [[300], [120]]
calor_mesclado = [300, 120]
nhot = 2
divisao = [False, False]
quantidade = [1, 1]

def printar():
    dlg.tableWidget.clearContents()
    if dlg.checkBox.isChecked():
        linha = 0
        linhas = 0
        for i in quantidade:
            linhas += i
        dlg.tableWidget.setRowCount(linhas)
        for corrente in range(nhot):
            if divisao[corrente]:
                for sub in range(quantidade[corrente]):
                    text = str(corrente+1) + "." + str(sub+1)
                    dlg.tableWidget.setItem(linha, 0, QTableWidgetItem(text))
                    dlg.tableWidget.setItem(linha, 1, QTableWidgetItem(str(pinchq)))
                    dlg.tableWidget.setItem(linha, 2, QTableWidgetItem(str(temperatura[corrente][sub])))
                    dlg.tableWidget.setItem(linha, 3, QTableWidgetItem(str(objetivo[corrente])))
                    dlg.tableWidget.setItem(linha, 4, QTableWidgetItem(str(calor[corrente][sub])))
                    linha += 1
            else:
                dlg.tableWidget.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
                dlg.tableWidget.setItem(linha, 1, QTableWidgetItem(str(pinchq)))
                dlg.tableWidget.setItem(linha, 2, QTableWidgetItem(str(temperatura[corrente][0])))
                dlg.tableWidget.setItem(linha, 3, QTableWidgetItem(str(objetivo[corrente])))
                dlg.tableWidget.setItem(linha, 4, QTableWidgetItem(str(calor[corrente][0])))
                linha += 1
    else:
        dlg.tableWidget.setRowCount(nhot)
        for corrente in range(nhot):
            dlg.tableWidget.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
            dlg.tableWidget.setItem(corrente, 1, QTableWidgetItem(str(pinchq)))
            dlg.tableWidget.setItem(corrente, 2, QTableWidgetItem(str(temperatura[corrente][0])))
            dlg.tableWidget.setItem(corrente, 3, QTableWidgetItem(str(objetivo[corrente])))
            dlg.tableWidget.setItem(corrente, 4, QTableWidgetItem(str(calor_mesclado[corrente])))

def dividir(corrente):
    temperatura[corrente-1].append(70)
    if corrente == 1:
        calor[corrente-1][0] = 140
        calor[corrente-1].append(160)
    if corrente == 2:
        calor[corrente-1][0] = 10
        calor[corrente-1].append(110)
    divisao[corrente-1] = True
    quantidade[corrente-1] += 1

printar()

dlg.pushButton.clicked.connect(lambda: dividir(1))
#dlg.pushButton.clicked.connect(lambda: dividir(2))
dlg.checkBox.stateChanged.connect(printar)

































dlg.show()
app.exec()



#oi
