import numpy as np

def estruturas (correntes, n,dlg,Tmin,Tmax,dTmin,dT,Tdecre,flagplot,pinch, cascat2certo,cascat,utilidadesquente,estagios) :
	quentes=[]
	frias=[]
	nquentes=0
	nfrias=0
	subnfrias=0
	subnquentes=0
	nestagio=0
	nsubestagio=0
	x=0
	for i in range (n):
		if correntes[i][3] == 'Hot':
			quentes.append(correntes[i])
			nquentes=nquentes+1
		else:
			frias.append(correntes[i])
			nfrias=nfrias+1
	subnquentes=nquentes
	subnfrias=nfrias
	if nquentes >= nfrias:
		nsubestagio=nquentes
		nestagio=nfrias
	else:
		nsubestagio=nfrias
		nsubestagio=nfrias
	estagios=np.array ([0])
	estagios.resize(nquentes,subnquentes,nfrias,subnfrias,nsubestagio,nestagio)
	##(estagios)
	estagios[1][0][1][0][0][0]=1
	estagios[0][0][0][0][1][1]=1
	estagios[0][1][1][0][1][1]=1
	##(estagios)
	int(estagios[1][0][0][1][1][0])
	##(type(estagios[1][0][0][1][1][0]))
	return(estagios)
