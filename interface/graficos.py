import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib.ticker import AutoMinorLocator

def grande_curva_composta(n, dlg, Tdecre, menor, cascat2, unidadeusada):
	plt.close("all")
	plt.style.use('default')
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	cascat3 = []
	cascat3.append(menor)
	for i in range(2*n-1):
	    cascat3.append(cascat2[i])
	for i in range(2*n-1):
	    ax.plot([cascat3[i], cascat3[i+1]], [Tdecre[i], Tdecre[i+1]], color = 'k')

	ax.grid(axis="x", color="0.75", linewidth=1, linestyle="--")
	ax.grid(axis="y", color="0.75", linewidth=1, linestyle="--")
	ax.set_xlabel("Enthalpy ({})".format(unidadeusada[2]))
	ax.set_ylabel("Temperature ({})".format(unidadeusada[0]))
	plt.title('Grand Composite Curve')
	return fig

def curva_composta_balanceada(Grafico, dtmin, tf, tq, unidades):
	pinch = []
	pinchx = []
	pinch.append(tf)
	pinch.append(tq)
	for i in range(0,len(Grafico[0])):
		if(Grafico[1][i]==tf):
			pinchx.append(Grafico[2][i])
			pinchx.append(Grafico[2][i])

	plt.close("all")
	plt.style.use('default')
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	temp = unidades[0]
	energia = unidades[2]

	ax.xaxis.set_minor_locator(AutoMinorLocator())
	ax.yaxis.set_minor_locator(AutoMinorLocator())
	ax.plot(Grafico[2],Grafico[1], label='Cold balanced composite curves', color='b')
	ax.plot(pinchx, pinch, label='Pinch: '+ str(dtmin) + ' {}'.format(temp), color='k')
	ax.set_xlabel('H ({})'.format(energia))
	ax.set_ylabel('T ({})'.format(temp))

	ax.plot(Grafico[2],Grafico[0], label='Hot balanced composite curves', color='r')
	ax.grid(axis="x", color="k", alpha=.3, linewidth=2, linestyle=":")
	ax.grid(axis="y", color="k", alpha=.5, linewidth=.5)
	ax.legend()

	return fig

def curva_composta(corrente, dtmin, pinchf, pinchq, tf, tq, unidades):
	plt.close("all")
	plt.style.use('default')
	fig = plt.figure()

	cfria=[]
	cquente=[]

	for i in range(0,len(corrente)):
		if corrente[i][3]=='Cold':
			cfria.append(corrente[i])
		else:
			cquente.append(corrente[i])

	auxf = [tf]
	auxq = [tq]

	for i in range(0,len(cfria)):
		auxf.append(cfria[i][0])
		auxf.append(cfria[i][1])
	for i in range(0, len(cquente)):
		auxq.append(cquente[i][0])
		auxq.append(cquente[i][1])

	auxq=list(dict.fromkeys(auxq))
	auxf=list(dict.fromkeys(auxf))

	auxf = sorted(auxf)
	auxq = sorted(auxq)
	somacpq = np.zeros(len(auxq)-1,dtype=float)
	somacpf = np.zeros(len(auxf)-1, dtype=float)

	hf=[]
	hq=[]

	for i in range(0,len(auxf)-1):
		for j in range(0,len(cfria)):
			if(cfria[j][0]>=auxf[i+1] and cfria[j][1]>=auxf[i+1]):
				c=0
			elif(cfria[j][0]<=auxf[i] and cfria[j][1]<=auxf[i]):
				c=0
			else:
				somacpf[i]+=cfria[j][2]
		hf.append(somacpf[i] * (auxf[i + 1] - auxf[i]))

	for i in range(0,len(auxq)-1):
		for j in range(0,len(cquente)):
			if(cquente[j][0]>=auxq[i+1] and cquente[j][1]>=auxq[i+1]):
				c=0
			elif(cquente[j][0]<=auxq[i] and cquente[j][1]<=auxq[i]):
				c=0
			else:
				somacpq[i]+=cquente[j][2]
		hq.append(somacpq[i]*(auxq[i+1]-auxq[i]))

	hf.insert(0, pinchf)
	hq.insert(0, 0)
	for i in range(0,len(hq)-1):
		hq[i+1]=hq[i]+hq[i+1]
	for i in range(0,len(hf)-1):
		hf[i+1]=hf[i]+hf[i+1]
	pinchx=[]
	pinchx.append(hq[auxq.index(tq)])
	pinchx.append(hf[auxf.index(tf)])
	pinchy=[tq,tf]
	futy=[auxf[0],auxf[0]]
	futx=[0,pinchf]
	huty=[max(auxq),max(auxq)]
	hutx=[max(hq),pinchq+max(hq)]

	temp = unidades[0]
	energia = unidades[2]

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	ax.xaxis.set_minor_locator(AutoMinorLocator())
	ax.yaxis.set_minor_locator(AutoMinorLocator())
	plt.title(label='Hot pinch temperature: '+ str(round(tq,5)) + ' ' + str(temp) + ';  Cold pinch temperature: ' + str(round(tf,5)) + ' ' + str(temp) + '\n', loc='center')

	ax.plot(hq,auxq, label='Hot composite curves', color='r')
	ax.plot(hf,auxf, label='Cold composite curves', color='b')
	ax.plot(pinchx,pinchy, label='Pinch: ' + str(dtmin) + ' ' + str(temp), color='k')
	ax.set_xlabel('H ({})'.format(energia))
	ax.set_ylabel('T ({})'.format(temp))
	ax.plot(hutx, huty, label='Hot utility: '+str(round(pinchq,2))+' {}'.format(energia), color='orange')
	ax.plot(futx, futy, label='Cold utility: '+str(round(pinchf,2))+' {}'.format(energia), color='c')
	ax.grid(axis="x", color="k", linewidth=1, linestyle=":")
	ax.grid(axis="y", color="k", linewidth=1, linestyle=":")
	ax.legend()

	return fig

def cascata(corrente, dtmin, unidades):
	correntegrid = []
	for i in range(0,len(corrente)):
		if (corrente[i][3]=='Cold'):
			correntegrid.append(float(corrente[i][0]) + dtmin/2)
			correntegrid.append(float(corrente[i][1]) + dtmin/2)
		else:
			correntegrid.append(float(corrente[i][0]) - dtmin/2)
			correntegrid.append(float(corrente[i][1]) - dtmin/2)

	sortc = np.unique(correntegrid).tolist()
	plt.close("all")
	plt.style.use('default')
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	temp = unidades[0]
	energia = unidades[2]

	ax.set_ylabel('T({})'.format(temp),fontsize=20)
	ax.set_xticks([])
	ax.set_xlim(-1, len(corrente))
	ax.set_ylim(-1.5, len(sortc) + 0.5)

	k=0.5

	for i in range(len(corrente)):
		param = [i, i]
		if (corrente[i][3] == 'Hot'):
			param2 = [sortc.index(corrente[i][0]-dtmin/2), sortc.index(corrente[i][1]-dtmin/2)]
			ax.plot(param,param2, color='r')
			ax.plot(i, (param2[0]), 'ro', ms=12, markeredgecolor='r')
			ax.annotate(str(i+1), xy=(i, param2[0]+k), color='k',fontsize="large", weight='heavy',
						horizontalalignment='center',
						verticalalignment='center')
			ax.plot([i], param2[1], marker=7, ms=10, color='r')
		else:
			param2 = [sortc.index(corrente[i][0] + dtmin / 2), sortc.index(corrente[i][1] + dtmin / 2)]
			ax.plot(param,param2, color='b')
			ax.plot(i, (param2[0]), 'bo', ms=10, markeredgecolor='b')
			ax.annotate(str(i+1), xy=(i, param2[0]-k), color='k',fontsize="large", weight='heavy',
						horizontalalignment='center',
						verticalalignment='center')
			ax.plot([i], param2[1], marker=6,ms=10,color='b')

	sortc = [round(num, 5) for num in sortc]
	ax.set_yticks(np.arange(0, len(sortc), step=1))
	ax.set_yticklabels(sortc,fontsize=20)
	ax.grid(axis="y", color="k", alpha=.5, linewidth=.5, linestyle="-")
	op=len(corrente)

	if(op<15):
		op=25
	opy=len(sortc)

	if opy>10:
		opy=15*opy
	else:
		opy=len(correntegrid)

	fig.set_size_inches(0.4*op, 5.3+0.015*opy)
	return fig
