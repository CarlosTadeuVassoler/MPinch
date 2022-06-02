import numpy as np
import math
import funchpinchcerto as fp2
import matplotlib.pyplot as plt

def CUSTO(correntes, n) :
	cfria = []
	cquente = []
	tfria = []
	tquente = []

	cp=1
	ncorrentefria=0
	ncorrentequente = 0

	for i in range(0,n):
		if correntes[i][3]=="Cold":
			cfria.append(correntes[i])
			ncorrentefria +=1
		else:
			cquente.append(correntes[i])
			ncorrentequente += 1

	for n in range(0,ncorrentefria):
		tfria.append(cfria[n][0])
		tfria.append(cfria[n][1])

	tfria=sorted(set(tfria))
	somacp = np.zeros(len(tfria),dtype=float)
	hentalpia = np.zeros(len(tfria),dtype=float)

	for n in range(0,len(tfria)-1):
		for i in range(0,len(cfria)):
				if (cfria[i][0] <= tfria[n] and cfria[i][1] <= tfria[n]):
					c = 0
				elif (cfria[i][0] >= tfria[n+1] and cfria[i][1] >= tfria[n+1]):
					c = 0
				else:
					somacp[n]+=cfria[i][2]

	cont=int(len(hentalpia))
	for n in range(cont-1,0,-1):
		if n==len(hentalpia)-1:
			for i in range(0,ncorrentefria):
				hentalpia[n]+=(cfria[i][1]-cfria[i][0])*cfria[i][2]
		else:
			hentalpia[n]=hentalpia[n+1]-(tfria[n+1]-tfria[n])*somacp[n]

################################################################################
	for n in range(0, ncorrentequente):
		tquente.append(cquente[n][0])
		tquente.append(cquente[n][1])

	tquente = sorted(set(tquente))
	somacpquente = np.zeros(len(tquente), dtype=float)
	hentalpiaquente = np.zeros(len(tquente), dtype=float)

	for n in range(0, len(tquente) - 1):
		for i in range(0, len(cquente)):
			if (cquente[i][0] <= tquente[n] and cquente[i][1] <= tquente[n]):
					# simplesmente n tem nada aqui oq importa é o else
					c = 0
			elif (cquente[i][0] >= tquente[n+1] and cquente[i][1] >= tquente[n+1]):
					c = 0
			else:
				somacpquente[n] += cquente[i][2]

	cont = int(len(hentalpiaquente))
	for n in range(cont - 1, 0, -1):
		if n == len(hentalpiaquente) - 1:
			for i in range(0, ncorrentequente):
				hentalpiaquente[n] += (cquente[i][0] - cquente[i][1]) * cquente[i][2]
		else:
			hentalpiaquente[n] = hentalpiaquente[n + 1] - (tquente[n + 1] - tquente[n]) * somacpquente[n]

	ajusteF = np.full((1, len(tfria)), '-999')
	ajusteQ = np.full((1, len(tquente)), '-999')

	ajusteF=np.vstack((ajusteF,tfria,hentalpia))
	ajusteQ = np.vstack((tquente,ajusteQ, hentalpiaquente))
	ajuste= np.hstack((ajusteF,ajusteQ))
	ajuste=np.asarray(ajuste, dtype=np.float64)

	for i in range(0,len(ajuste[2])):
		ajuste[2][i]=round(ajuste[2][i],5)

	for n in range(0, len(ajuste[0])):
		for i in range(0, len(ajuste[0])):

			if(ajuste[2][n]==ajuste[2][i]):
				if(ajuste[0][i]=='-999'):
					ajuste[0][i]=ajuste[0][n]
				else:
					ajuste[1][i]=ajuste[1][n]

	b2=[]
	b3=[]
	c=1
	ajuste2=[]

	for n in range(0, len(ajuste[2])):
		for i in range(0, len(ajuste[2])):
			if ajuste[2][n]==ajuste[2][i] and i!=n:
				if ajuste[2][n] not in b3:
					b3.append(ajuste[2][n])
					b2.append(n)

	for n in range(0, len(b2)):
		ajuste = np.delete(ajuste, b2[n], 1)
		b2=list(np.asarray(b2) - 1)

	ajuste = sorted(ajuste.T, key=lambda l: l[2])

	for n in range(0,len(ajuste)):
		for i in range(0,2):
			if(ajuste[n][i] == -999 and ajuste[n+1][i] != ajuste[n][i]):
				ajuste[n][i]=ajuste[n-1][i]+(ajuste[n-1][i]-ajuste[n+1][i])*(ajuste[n][2]-ajuste[n-1][2])/(ajuste[n-1][2]-ajuste[n+1][2])
			if(ajuste[n][i]==-999 and ajuste[n+1][i]==ajuste[n][i]):
				b=n
				c=n
				while(ajuste[n][i]==-999 and ajuste[n+1][i]==ajuste[n][i]):
					n=c
					c+=1
				ajuste[b][i]=ajuste[b-1][i]+(ajuste[b-1][i]-ajuste[c][i])*(ajuste[b][2]-ajuste[b-1][2])/(ajuste[b-1][2]-ajuste[c][2])
				n=b

	ajuste=np.transpose(ajuste)

	cphquente=[]
	cphfrio = []
	somador=0
	c=0

	for n in range(0,len(ajuste[0])-1):
		for i in range(0,len(cquente)):
			if (cquente[i][0] <= ajuste[0][n] and cquente[i][1] <= ajuste[0][n]):
				#simplesmente n tem nada aqui oq importa é o else
				c=0
			elif (cquente[i][0] >= ajuste[0][n + 1] and cquente[i][1] >= ajuste[0][n + 1]):
				c = 0
			else:
				somador+=(cquente[i][2]/cquente[i][4])
		cphquente.append((ajuste[0][n+1]-ajuste[0][n])*somador)
		somador=0

	for n in range(0,len(ajuste[1])-1):
		for i in range(0,len(cfria)):
			if (cfria[i][0] <= ajuste[1][n] and cfria[i][1] <= ajuste[1][n]):
				c = 0
			elif(cfria[i][0] >= ajuste[1][n+1] and cfria[i][1] >= ajuste[1][n+1]):
				c = 0
			else:
				somador += (cfria[i][2] / cfria[i][4])
		cphfrio.append((ajuste[1][n+1]-ajuste[1][n])*somador)
		somador=0

	deltalmnk=[]
	areak=[]
	for n in range(0,len(cphfrio)):
		try:
			deltalmnk.append(((ajuste[0][n]-ajuste[1][n])-(ajuste[0][n+1]-ajuste[1][n+1]))/math.log((ajuste[0][n]-ajuste[1][n])/(ajuste[0][n+1]-ajuste[1][n+1])))
		except:
			deltalmnk.append((ajuste[0][n]-ajuste[1][n]))
		areak.append((cphfrio[n]+cphquente[n])/deltalmnk[n])


	p=len(areak)
	areatotal=sum(areak)
	return areatotal,p,ajuste,cphfrio,cphquente,areak,deltalmnk

def varia(inicio, passo, fim, corrente, nnn):
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

	for n in range(0,len(variadt)):
		uf,uq,_,_=fp2.pontopinch(corrente,ncorrentes,variadt[n])
		uflista.append(uf)
		uqlista.append(uq)

		if corrente[-1][3] == "Hot":
			corrente[-1][2] = uq / (corrente[-1][0] - corrente[-1][1])
		else:
			corrente[-1][2] = uf / (corrente[-1][1] - corrente[-1][0])

		if corrente[-2][3] == "Hot":
			corrente[-2][2] = uq / (corrente[-2][0] - corrente[-2][1])
		else:
			corrente[-2][2] = uf / (corrente[-2][1] - corrente[-2][0])

		areat,nareas,ajuste,_,_,_,_ = CUSTO(corrente, ncorrentes + nut)
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

def formatando(valor,index):
    if valor>=1_000_000:
        fomatador = '{:1.1f}M'.format(valor*0.000_001)
    else:
        fomatador = '{:1.0f}k'.format(valor * 0.001)
    return fomatador

def grafico_custo(x, y, variadt, custoopano, custocapitalanual, custototanual):
	plt.close("all")
	plt.style.use('bmh')
	fig = plt.figure()

	ax = fig.add_subplot(111)
	ax.yaxis.set_major_formatter(formatando)
	ax.plot(variadt,custoopano, label='Operational Cost x ΔTmin')
	ax.plot(variadt,custocapitalanual, label='Capital Cost x ΔTmin', color='k')
	ax.plot(variadt, custototanual, label='Total Cost x ΔTmin', color='r')
	ax.set_xlabel('ΔTmin')
	ax.set_ylabel('Cost')
	ax.legend()
	ax.grid(axis="x", color="black", alpha=.3, linewidth=2, linestyle=":")
	ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
	return fig

def grafico_area(x, y, variadt, yplot):
	plt.close("all")
	plt.style.use('bmh')
	fig = plt.figure()

	ax= fig.add_subplot(111)
	ax.yaxis.set_major_formatter(formatando)

	ax.plot(variadt,yplot, label='Area x ΔTmin', color='r')
	ax.set_xlabel('ΔTmin')
	ax.set_ylabel('Area')
	ax.legend()
	ax.grid(axis="x", color="black", alpha=.3, linewidth=2, linestyle=":")
	ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
	return fig

def grafico_utilidade(x, y, variadt, uq, uf):
	plt.close("all")
	plt.style.use('bmh')
	fig = plt.figure()

	ax = fig.add_subplot(111)
	#self.ax.yaxis.set_major_formatter(formatando)
	ax.plot(variadt,uq, label='Hot utility x ΔTmin', color='r')
	ax.plot(variadt, uf, label='Cold utility x ΔTmin', color='b')
	ax.set_xlabel('ΔTmin')
	ax.set_ylabel('Utility')
	ax.legend()
	ax.grid(axis="x", color="black", alpha=.3, linewidth=2, linestyle=":")
	ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
	return fig
