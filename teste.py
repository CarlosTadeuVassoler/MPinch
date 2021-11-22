from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

app = QtWidgets.QApplication([])
dlg = uic.loadUi("MPinch.ui")

botao = [0] * 3
qual = []

a = 0

class botao():
    def __init__(self, i):
        self.botao = QtWidgets.QPushButton("oi {}".format(i+1))
        self.botao.clicked.connect(lambda: self.clicked(i))
        dlg.verticalLayout.addWidget(self.botao)

    def clicked(self, i):
        global a
        a+=1
        print(a)

botoes = []
for i in range(3):
    botao_do_momento = botao(i)
    botoes.append(botao_do_momento)

print(botoes)

































dlg.show()
app.exec()



#oi
