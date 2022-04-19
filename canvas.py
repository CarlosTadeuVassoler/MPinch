from tkinter import *
import turtle
from PyQt5 import uic, QtWidgets, QtGui, QtQuick
from PIL import Image

app = QtWidgets.QApplication([])
dlg = uic.loadUi("teste_canvas.ui")


class myCanvas2(FigureCanvas):
	def __init__(self):
		self.fig=Figure()
		FigureCanvas.__init__(self,self.fig)

	def desenha(self):
		seta = turtle.RawTurtle(desenho)
		seta.speed(1000)
		seta.forward(980)

janela = Tk()
janela.geometry("1280x600")
desenho = turtle.ScrolledCanvas(janela, width=1280, height=600)
desenho.pack()

tela = turtle.TurtleScreen(desenho)
tela.screensize(2000, 2000)

seta = turtle.RawTurtle(desenho)
seta.speed(1000)
seta.forward(980)

imagem = tela.getcanvas()
QtQuick.canvas(imagem)
# dlg.label.setCanvas)#








dlg.showMaximized()
app.exec()
