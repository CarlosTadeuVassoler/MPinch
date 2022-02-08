import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets , uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pylab as P

import random


def plotargrafico1(correntes,n,caixinha,dlg,Tmin,Tmax,dTmin,dT,Tdecre,pinch,unidadeusada,plotou):

	# a figure instance to plot on
	dlg.figure = plt.figure(1)



	# this is the Canvas Widget that displays the `figure`
	# it takes the `figure` instance as a parameter to __init__
	dlg.canvas = FigureCanvas(dlg.figure)


	# this is the Navigation widget
	# it takes the Canvas widget and a parent
	dlg.toolbar = NavigationToolbar(dlg.canvas, dlg)

	if plotou == 0:
		caixinha=dlg.caixinha
		caixinha.addWidget(dlg.canvas)
		caixinha.addWidget(dlg.toolbar)
	else:
		dlg.figure.clear()


	Eixo = []
	for i in range(n):
	    Eixo.append(i+1)
	for i in range(2*n):
	     P.plot([0, 2*n], [Tdecre[i], Tdecre[i]], color = 'gray', linestyle = '--')
	for i in range(n):
	    if correntes[i][3] == 'Hot':
	        P.arrow(i + 1, correntes[i][0], 0.0, -dT[i]+4, fc="r", ec="r", head_width=0.08, head_length=4)
	    if correntes[i][3] == 'Cold':
	        P.arrow(i + 1, correntes[i][0], 0.0, -dT[i]-4, fc="b", ec="b", head_width=0.08, head_length=4)
	P.xlim([0, n + 1])
	P.ylim([Tmin-dTmin, Tmax+dTmin])
	P.xlabel('Stream')
	P.ylabel(unidadeusada[0])
	P.xticks(Eixo)
	P.yticks(Tdecre)
	P.matplotlib.pyplot.grid(which='major', axis='y')




	# Just some button connected to `plot` method
	dlg.canvas.draw()
	dlg.figure.axes.clear()










def plotargrafico2(correntes,n,caixinha3,dlg,Tmin,Tmax,dTmin,dT,Tdecre,pinch, cascat2certo,cascat,utilidadesquente,pinchf,pinchq,unidadeusada):
	# a figure instance to plot on
	#("pokkpkopkopkopkopkopkpkopkopkop",dTmin)
	dlg.figure2 = plt.figure(2)



	# this is the Canvas Widget that displays the `figure`
	# it takes the `figure` instance as a parameter to __init__
	dlg.canvas2 = FigureCanvas(dlg.figure2)


	# this is the Navigation widget
	# it takes the Canvas widget and a parent
	dlg.toolbar = NavigationToolbar(dlg.canvas2, dlg)

	def plot2():
		#("pqppppppppp ", pinchq)
		dlg.figure2.clear()
		Temperatura = Tdecre[2*n-1]
		#("232323  ",Temperatura)
		newcorrentesq = []
		newcorrentesf = []
		dHq = []
		dHf = []
		while Temperatura < Tdecre[0]:
		    Intdetemp = Temperatura + 1
		    x = []
		    x.append(Temperatura)
		    x.append(Intdetemp)
		    somacpq = 0
		    somacpf = 0
		    for i in range(n):
		        if correntes[i][3] == 'Hot':
		            if correntes[i][0] >= Intdetemp and correntes[i][1] <= Temperatura:
		                somacpq = somacpq + correntes[i][2]
		        if correntes[i][3] == 'Cold':
		            if correntes[i][1] >= Intdetemp and correntes[i][0] <= Temperatura:
		                somacpf = somacpf + correntes[i][2]
		    if somacpq != 0:
		    	auxq = somacpq * 1
		    	dHq.append(auxq)
		    	newcorrentesq.append(x)
		    if somacpf != 0:
		    	auxf = somacpf * 1
		    	dHf.append(auxf)
		    	newcorrentesf.append(x)
		    Temperatura = Temperatura + 1
		#("opopopopopopopop", somacpf,somacpq)
		intervalosq = len(dHq)
		intervalosf = len(dHf)
		#("okkokokokokkoko",dHq)
		#(newcorrentesq[0][0])
		somaq = 0
		somaf = 0
		somadH = 0
		#("n sabe fazer conta poha", pinchq, newcorrentesq[0][0], dTmin/2)
		#("2222222222222 ",pinchq - newcorrentesq[0][0] - (dTmin/2))
		for i in range(int(pinchq - newcorrentesq[0][0] - (dTmin/2))):
		    somadH = somadH + dHq[i]
		    #("kiikikkikikki",somadH)
		P.plot([0,0],[0,0],color = 'black')
		P.plot([0,0],[0,0],color = 'black')
		P.plot([0,0],[0,0],color = 'black')
		P.plot([0, somadH], [pinchq, pinchq], color = 'gray', linestyle = '--')
		P.plot([0, somadH], [pinchf, pinchf], color = 'gray', linestyle = '--')
		P.plot([somadH, somadH], [0, pinchf], color = 'gray', linestyle = '--')
		P.plot([somadH, somadH], [pinchf, pinchq], color = 'black')
		P.plot([0, 0], [0, newcorrentesq[0][0] + (dTmin/2)], color = 'gray', linestyle = '--')
		P.plot([float(cascat2certo[2*n-2]), float(cascat2certo[2*n-2])], [0, newcorrentesf[0][0] - (dTmin/2)], color = 'gray', linestyle = '--')
		for i in range(int(intervalosq)):
		    if i == 0:
		        if dHq[i] != 0:
		            P.plot([0, dHq[i]], [newcorrentesq[i][0] + (dTmin/2), newcorrentesq[i][1] + (dTmin/2)], color = 'r')
		            somaq = dHq[i]
		    else:
		        if dHq[i] != 0:
		            somaq = somaq + dHq[i]
		            P.plot([(somaq - dHq[i]), somaq], [newcorrentesq[i][0] + (dTmin/2), newcorrentesq[i][1] + (dTmin/2)], color = 'r')
		for i in range(int(intervalosf)):
		    if i == 0:
		        if dHf[i] != 0:
		           P.plot([float(cascat2certo[2*n-2]), float(cascat2certo[2*n-2]) + dHf[i]], [newcorrentesf[i][0] - (dTmin/2), newcorrentesf[i][1] - (dTmin/2)], color = 'b')
		           somaf = float(cascat2certo[2*n-2]) + dHf[i]
		    else:
		        if dHf[i] != 0:
		           somaf = somaf + dHf[i]
		           P.plot([(somaf - dHf[i]), somaf], [newcorrentesf[i][0] - (dTmin/2), newcorrentesf[i][1] - (dTmin/2)], color = 'b')
		if(newcorrentesf[int(intervalosf) - 1][1] > newcorrentesq[int(intervalosq) - 1][1]):
		    P.plot([somaq, somaf], [newcorrentesf[int(intervalosf) - 1][1] - (dTmin/2), newcorrentesf[int(intervalosf) - 1][1] - (dTmin/2)], color = 'k')
		else:
		    P.plot([somaq, somaf], [newcorrentesq[int(intervalosq) - 1][1] + (dTmin/2), newcorrentesq[int(intervalosq) - 1][1] + (dTmin/2)], color = 'k')
		P.plot([somaq, somaq], [0, newcorrentesq[int(intervalosq) - 1][1] + (dTmin/2)], color = 'gray', linestyle = '--')
		P.plot([somaf, somaf], [0, newcorrentesq[int(intervalosq) - 1][1] + (dTmin/2)], color = 'gray', linestyle = '--')
		P.plot([0, somaq], [newcorrentesq[int(intervalosq) - 1][1] + (dTmin/2), newcorrentesq[int(intervalosq) - 1][1] + (dTmin/2)], color = 'gray', linestyle = '--')
		P.plot([0, somaf], [newcorrentesf[int(intervalosf) - 1][1] - (dTmin/2), newcorrentesf[int(intervalosf) - 1][1] - (dTmin/2)], color = 'gray', linestyle = '--')
		P.plot([0, float(cascat2certo[2*n-2])], [newcorrentesf[0][0] - (dTmin/2), newcorrentesf[0][0] - (dTmin/2)], color = 'k')
		P.ylim([Tmin-dTmin, Tmax+dTmin])
		if(somaq > somaf):
		    P.xlim([0, somaq + 0.05*somaq])
		else:
		    P.xlim([0, somaf + 0.05*somaf])
		P.xlabel(unidadeusada[2])
		P.ylabel(unidadeusada[0])
		P.title('TH Diagram')
		# if (dlg.tempcombo1.currentText()) == 'SI':
		utilidadesquenteleg=(str(utilidadesquente)[0:] + ' kW')
		utilidadesquenteleg2=(str(cascat2certo[2*n-2])[0:] + ' kW')
		utilidadesquenteleg3=(str(dTmin)[0:] + ' K')
		# if (dlg.tempcombo1.currentText()) == 'Imperial units':
		# 	utilidadesquenteleg=(str(utilidadesquente)[0:] + ' btu/h')
		# 	utilidadesquenteleg2=(str(cascat2certo[2*n-2])[0:] + ' btu/h')
		# 	utilidadesquenteleg3=(str(dTmin)[0:] + ' ºF')


		P.gca().legend((("hot utilities: {}".format(utilidadesquenteleg)), ("cold utilities: {}".format(utilidadesquenteleg2)),("$\Delta Tmin$: {}".format(utilidadesquenteleg3))))
		EixoY = []
		EixoY.append(pinchq)
		EixoY.append(pinchf)
		EixoY.append(newcorrentesf[0][0] - dTmin/2)
		EixoY.append(newcorrentesf[intervalosf-1][1] - dTmin/2)
		EixoY.append(newcorrentesq[0][0] + dTmin/2)
		EixoY.append(newcorrentesq[intervalosq-1][1] + dTmin/2)
		EixoX = []
		EixoX.append(0)
		EixoX.append(float(cascat2certo[2*n-2]))
		EixoX.append(somadH)
		EixoX.append(somaf)
		EixoX.append(somaq)
		#("opqepoqiopwi",somadH,somaq,somaf)
		P.yticks(EixoY)
		P.xticks(EixoX)
		dlg.canvas2.draw()



	# Just some button connected to `plot` method
	plot2()

	# set the layout
	caixinha3=dlg.caixinha3
	caixinha3.addWidget(dlg.canvas2)
	caixinha3.addWidget(dlg.toolbar)


def plotargrafico3(correntes, n, caixinha4,dlg,Tmin,Tmax,dTmin,dT,Tdecre,pinch, cascat2certo,cascat,utilidadesquente,pinchf,pinchq,menor,cascat2,unidadeusada):
	# a figure instance to plot on
	dlg.figure3 = plt.figure(3)



	# this is the Canvas Widget that displays the `figure`
	# it takes the `figure` instance as a parameter to __init__
	dlg.canvas3 = FigureCanvas(dlg.figure3)


	# this is the Navigation widget
	# it takes the Canvas widget and a parent
	dlg.toolbar = NavigationToolbar(dlg.canvas3, dlg)

	def plot3():
		cascat3 = []
		cascat3.append(menor)
		#("sijdsoij", menor)
		for i in range(2*n-1):
		    cascat3.append(cascat2[i])
		#("hmm kkk bjs",cascat3)
		for i in range(2*n-1):
		    P.plot([cascat3[i], cascat3[i+1]], [Tdecre[i], Tdecre[i+1]], color = 'k')
		for i in range(2*n):
		    P.plot([0, cascat3[i]], [Tdecre[i], Tdecre[i]], color = 'gray', linestyle = '--')
		    P.plot([cascat3[i] , cascat3[i]], [0, Tdecre[i]], color = 'gray', linestyle = '--')
		P.ylim([0, Tdecre[0]+10])
		P.xlim(0)
		P.yticks(Tdecre)
		P.xticks(cascat3)
		P.xlabel(unidadeusada[1])
		P.ylabel(unidadeusada[0])
		P.title('Grand Composite Curve')
		dlg.canvas3.draw()



	# Just some button connected to `plot` method
	plot3()

	# set the layout
	caixinha4=dlg.caixinha4
	caixinha4.addWidget(dlg.canvas3)
	caixinha4.addWidget(dlg.toolbar)
