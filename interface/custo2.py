import numpy as np
import funchpinchcerto as fp2
import testesoriginal as tt
import matplotlib.pyplot as plt

def varia(inicio,passo,fim,corrente,nnn):
	variadt = np.arange(inicio, fim + passo, passo)

	a = 6600
	b = 600
	c = 0.63

	ncorrentes = len(corrente) - 2
	nut=2 #nutilidades
	yplot=[]
	custocapital=[]
	i=3#taxa de juros/periodo
	periodo=2#n de periodos
	Fatoranual= 1#(i*(i+1)**periodo)/(-1+(i+1)**periodo)
	custocapitalanual=[]
	precoufano=20
	precouqano=120
	custototanual=[]
	custoopano=[]
	uflista=[]
	uqlista=[]
	# print(Fatoranual)
	for n in range(0,len(variadt)):

		uf,uq,_,_=fp2.pontopinch(corrente,ncorrentes,variadt[n])
		uflista.append(uf)
		uqlista.append(uq)
		# print(uq,uf)
		# print(corrente)
		# print(corrente[4][1])
		if corrente[-1][3] == "Hot":
			corrente[-1][2] = uq / (corrente[-1][0] - corrente[-1][1])
		else:
			corrente[-1][2] = uf / (corrente[-1][1] - corrente[-1][0])

		if corrente[-2][3] == "Hot":
			corrente[-2][2] = uq / (corrente[-2][0] - corrente[-2][1])
		else:
			corrente[-2][2] = uf / (corrente[-2][1] - corrente[-2][0])

		#dar um jeito de tirar os append, criar uma matriz de n elementos de correntes+n de ut

		areat,nareas,ajuste,_,_,_,_ = tt.CUSTO(corrente, ncorrentes + nut)
		yplot.append(areat)

		if nnn==-1:
			custoopano.append((precoufano*uf*1000)+(precouqano*uq*1000))
			custocapital.append(nareas*(a+b*(areat/nareas)**c))
			custocapitalanual.append(Fatoranual*nareas*(a+b*(areat/nareas)**c))
			custototanual.append(custoopano[n]+custocapitalanual[n])
		elif nnn==-2:
			custoopano.append((precoufano*uf*1000)+(precouqano*uq*1000))
			custocapital.append((ncorrentes+nut-1)*(a+b*(areat/(ncorrentes+nut-1))**c))
			custocapitalanual.append(Fatoranual*(ncorrentes+nut-1)*(a+b*(areat/(ncorrentes+nut-1))**c))
			custototanual.append(custoopano[n]+custocapitalanual[n])
		else:
			custoopano.append((precoufano*uf*1000)+(precouqano*uq*1000))
			custocapital.append((nnn)*(a+b*(areat/(nnn))**c))
			custocapitalanual.append(Fatoranual*(nnn)*(a+b*(areat/(nnn))**c))
			custototanual.append(custoopano[n]+custocapitalanual[n])





	return uflista,uqlista,variadt,yplot,custoopano,custocapital,custocapitalanual,custototanual

"""
figura=plt.figure(figsize=(20,20))
figura.suptitle('Graficos ΔTmin')

figura.add_subplot(121)
plt.plot(variadt,custoopano, label='C.Operacional x ΔTmin', color='r')
plt.plot(variadt,custocapitalanual, label='C.Capital x ΔTmin')
plt.plot(variadt,custototanual, label='C.Total x ΔTmin')
plt.xlabel('ΔTmin')
plt.ylabel('Custo')

figura.add_subplot(122)
plt.plot(variadt,yplot, label='Area x ΔTmin')

plt.xlabel('ΔTmin')
plt.ylabel('Area')


plt.show()

"""
