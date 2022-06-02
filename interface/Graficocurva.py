from funchpinchcerto import pontopinch
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter

def plotgrafcurva(corrente,dtmin,pinchf,pinchq,tf,tq, unidades):
	plt.close("all")
	# PLT.CLOSE("ALL") PRA NÃO COMER TODA A MEMORIA DO SEU PC PELO AMOR DE DEUS NÃO ESQUECE DISSO
	plt.style.use('default')
	fig = plt.figure()


	cfria=[]
	cquente=[]
	for i in range(0,len(corrente)):
		if corrente[i][3]=='Cold':
			cfria.append(corrente[i])
		else:
			cquente.append(corrente[i])


	auxf=[tf]
	auxq=[tq]

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
	ax.grid(axis="x", color="black", linewidth=1, linestyle=":")
	ax.grid(axis="y", color="black", linewidth=1, linestyle=":")
	ax.legend()

	# fig.savefig("curvadt1.png",bbox_inches="tight", pad_inches=0.5)
	return fig

def plotgrafcurva2(corrente,dtmin,pinchf,pinchq,tf,tq, unidades):
	plt.close("all")
	# PLT.CLOSE("ALL") PRA NÃO COMER TODA A MEMORIA DO SEU PC PELO AMOR DE DEUS NÃO ESQUECE DISSO
	plt.style.use('default')
	cfria=[]
	cquente=[]
	for i in range(0,len(corrente)):
		if corrente[i][3]=='Cold':
			cfria.append(corrente[i])
		else:
			cquente.append(corrente[i])


	auxf=[tf]
	auxq=[tq]

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
	plt.title(label='Hot pinch temperature: ' + str(round(tq,5)) + ' ' + str(temp) + ';  Cold pinch temperature: ' + str(round(tf,5)) + ' ' + str(temp) + '\n', loc='center')

	ax.xaxis.set_minor_locator(AutoMinorLocator())
	ax.yaxis.set_minor_locator(AutoMinorLocator())
	ax.plot(hq,auxq, label='Hot composite curves', color='r')
	ax.plot(hf,auxf, label='Cold composite curves', color='b')
	ax.plot(pinchx,pinchy, label='Pinch: '+ str(dtmin) + ' ' + str(temp), color='k')
	ax.set_xlabel('H ({})'.format(energia))
	ax.set_ylabel('T ({})'.format(temp))
	ax.plot(hutx, huty, label='Hot utility: '+str(round(pinchq,2))+' {}'.format(energia), color='orange')
	ax.plot(futx, futy, label='Cold utility: '+str(round(pinchf,2))+' {}'.format(energia), color='c')
	ax.grid(axis="x", color="black", linewidth=1, linestyle=":")
	ax.grid(axis="y", color="black", linewidth=1, linestyle=":")
	ax.legend()

	# fig.savefig("curvadt2.png",bbox_inches="tight", pad_inches=0.5)
	return fig
