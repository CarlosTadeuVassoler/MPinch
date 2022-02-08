import xlrd
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
def pontopinch (correntes, n, dTmin, mudar=False) :
	#(n)
	correntes_calculo = []
	if not mudar:
		for corrente in range(len(correntes)):
			correntes_calculo.append([])
			for i in range(4):
				correntes_calculo[corrente].append(correntes[corrente][i])
	else:
		correntes_calculo = correntes
	for i in range (n): #correção das temperaturas
		if correntes_calculo[i][3] == "Hot":
			correntes_calculo[i][0] -= (dTmin)/2
			correntes_calculo[i][1] -= (dTmin)/2
		if correntes_calculo[i][3] == "Cold":
			correntes_calculo[i][0] += (dTmin)/2
			correntes_calculo[i][1] += (dTmin)/2
	Tdecre=[] #recebeu as temperaturas corrigidas
	for i in range (n):
		for j in range (2):
			Tdecre.append(correntes_calculo[i][j])
	Tdecre.sort(reverse = True) #temperaturas decrescentes
	#("correntes_calculo:")
	#(correntes_calculo)
	#("temperaturas corrigidas:")
	#(Tdecre)
	dTdecre=[]
	dT=[]
	for i in range(n): #encontrando a variação das temperaturas
		x2=correntes_calculo[i][0]-correntes_calculo[i][0+1]
		dT.append(x2)
	for i in range(2*n-1): #encontrando a variação das temperaturas
		x2=Tdecre[i]-Tdecre[i+1]
		dTdecre.append(x2)
	#('sdsd',dT,'sssss')
	#("intervalo de temperaturas:")
	#(dTdecre)
	quaiscp=[]
	v=[]
	for k in range (2*n-1): #escolha dos cps
		v=[]
		for i in range (n):
			for j in range (1):
				if correntes_calculo[i][3]=="Hot":
					if (correntes_calculo[i][j] > Tdecre[k+1]) and (correntes_calculo[i][j+1] < Tdecre [k]):
						cptq=correntes_calculo[i][2]
						cptq=float(cptq)
						cptq=-cptq
						v.append(cptq)
						break
				if correntes_calculo[i][3]=="Cold":
					if (correntes_calculo[i][j+1] > Tdecre[k+1]) and (correntes_calculo[i][j] < Tdecre [k]):
						cptf=correntes_calculo[i][2]
						v.append(cptf)
						break
			if i==3:
				quaiscp.append(v)
	#("cps das correntes_calculo quentes e frias:")
	#(quaiscp) #escolha dos cps com base nos dT 'flechinhas'
	somacps=[]
	soma=0
	tamanhocps=len(quaiscp)
	for i in range (len(quaiscp)):
		soma2=0
		for j in range (len(quaiscp[i])):
			soma=quaiscp[i][j]
			soma=float(soma)
			soma2=float(soma+soma2)
		somacps.append(soma2)
	somacpscerto = [ '%.2f' % elem for elem in somacps]
	#("somatorios dos cps:")
	#(somacpscerto) #arredondamento dos cps
	dH=[]
	for i in range (2*n-1): #achando a variação da entalpia
		mult=somacps[i]*dTdecre[i]
		dH.append(mult)
	dHcerto = ([ '%.2f' % elem for elem in dH])
	#("intervalo de entalpia:")
	#(dHcerto)
	cascat=[0-dH[0]]
	for i in range (2*n-2): #primeira cascata de energia
		sub2=dH[i+1]
		sub3=cascat[i]-sub2
		cascat.append(sub3)
	cascatcerto= ([ '%.2f' % elem for elem in cascat])
	#("primeira cascata de energia:")
	#(cascatcerto)
	menor = min(float(s) for s in cascat) #encontrando a maior demanda de energia
	cascat2=[-menor-dH[0]]
	for i in range (2*n-2): #segunda cascata
		sub2=dH[i+1]
		sub3=cascat2[i]-sub2
		cascat2.append(sub3)
	cascat2certo = [ '%.2f' % elem for elem in cascat2]
	for i in range (len(cascat2)): #arredondar para encontrar o 0
		x=round(cascat2[i], 2)
		cascat2[i]=x
	#("segunda cascata de energia:")
	#(cascat2)
	# print(cascat2)
	# print(dH)
	# print(dH[0]+cascat2[0])
	util_quente = dH[0] + cascat2[0]
	util_fria = cascat2[-1]
	ponto0=min(float(s) for s in cascat2)
	for i in range (len(cascat2)):  #encontrar temperatura no ponto pinch
		if ponto0 == cascat2[i]:
			pinch=Tdecre[i+1]
	#("ponto de estrangulamento energético")
	#(pinch)
	pinchq=pinch+(dTmin/2) #arrumando as temperatura das correntes_calculo quentes e frias
	pinchf=pinch-(dTmin/2)
	#("pinch da temperatura da corrente quente:")
	#(pinchq)
	#("pinch da temperatura da corrente fria:")
	#(pinchf)
	Tmax = 0
	Tmin = 99999
	for i in range(n):
	    for j in range(2):
	        if Tmax < correntes_calculo[i][j]:
	            Tmax = correntes_calculo[i][j]
	        if Tmin > correntes_calculo[i][j]:
	            Tmin = correntes_calculo[i][j]
	#('sdsd',Tdecre,'sssss')
	menor = min(float(s) for s in cascat)  # encontrando a maior demanda de energia
	menor = menor*(-1)
	menorc = ['%.2f' % menor]
	utilidadesquente = menorc[0]
	coisas_graficos = [Tdecre, Tmin, Tmax, cascat2certo, dT, cascat2, utilidadesquente, menor, pinch]
	return pinchf, pinchq, util_quente, util_fria, coisas_graficos
