import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def cascata(corrente,dtmin, unidades):
	correntegrid = []
	for i in range(0,len(corrente)):
		if (corrente[i][3]=='Cold'):
			correntegrid.append(float(corrente[i][0])+dtmin/2)
			correntegrid.append(float(corrente[i][1]) + dtmin / 2)
		else:
			correntegrid.append(float(corrente[i][0])-dtmin/2)
			correntegrid.append(float(corrente[i][1]) - dtmin / 2)

	sortc=np.unique(correntegrid).tolist()
	plt.close("all")
	plt.style.use('default')
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	temp = unidades[0]
	energia = unidades[2]

	ax.set_ylabel('T({})'.format(temp),fontsize=20)
	ax.set_xticks([])
	ax.set_xlim(-1, len(corrente))
	ax.set_ylim(-1.5,len(sortc)+0.5)

	if(len(corrente)>10):
		k=0.5
	else:
		k=0.5

	for i in range(0, len(corrente)):
		param=[i,i]
		if (corrente[i][3]=='Hot'):
			param2 = [sortc.index(corrente[i][0]-dtmin/2), sortc.index(corrente[i][1]-dtmin/2)]
			ax.plot(param,param2, color='red')
			ax.plot(i, (param2[0]), 'ro', ms=12, markeredgecolor='red')
			ax.annotate(str(i+1), xy=(i, param2[0]+k), color='black',fontsize="large", weight='heavy',
						horizontalalignment='center',
						verticalalignment='center')
			ax.plot([i], param2[1], marker=7, ms=10, color='red')
		else:
			param2 = [sortc.index(corrente[i][0] + dtmin / 2), sortc.index(corrente[i][1] + dtmin / 2)]
			ax.plot(param,param2, color='blue')
			ax.plot(i, (param2[0]), 'bo', ms=10, markeredgecolor='blue')
			ax.annotate(str(i+1), xy=(i, param2[0]-k), color='black',fontsize="large", weight='heavy',
						horizontalalignment='center',
						verticalalignment='center')
			ax.plot([i], param2[1], marker=6,ms=10,color='blue')

	sortc = [round(num, 5) for num in sortc]
	ax.set_yticks(np.arange(0, len(sortc), step=1))
	ax.set_yticklabels(sortc,fontsize=20)
	ax.grid(axis="y", color="black", alpha=.5, linewidth=.5, linestyle="-")
	op=len(corrente)

	if(op<15):
		op=25
	opy=len(sortc)

	if opy>10:
		opy=15*opy
	else:
		opy=len(correntegrid)

	fig.set_size_inches(0.4*op, 5.3+0.015*opy)
	# fig.savefig("EC.png", bbox_inches='tight')
	return fig

def cascata2(corrente,dtmin, unidades):
	correntegrid = []
	for i in range(0,len(corrente)):
		if (corrente[i][3]=='Cold'):
			correntegrid.append(float(corrente[i][0])+dtmin/2)
			correntegrid.append(float(corrente[i][1]) + dtmin / 2)
		else:
			correntegrid.append(float(corrente[i][0])-dtmin/2)
			correntegrid.append(float(corrente[i][1]) - dtmin / 2)

	sortc=np.unique(correntegrid).tolist()
	plt.close("all")
	plt.style.use('default')
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	temp = unidades[0]
	energia = unidades[2]

	ax.set_ylabel('T({})'.format(temp),fontsize=20)
	ax.set_xticks([])
	ax.set_xlim(-1, len(corrente))
	ax.set_ylim(-1.5,len(sortc)+0.5)

	if(len(corrente)>10):
		k=0.5
	else:
		k=0.5

	for i in range(0, len(corrente)):
		param=[i,i]
		if (corrente[i][3]=='Hot'):
			param2 = [sortc.index(corrente[i][0]-dtmin/2), sortc.index(corrente[i][1]-dtmin/2)]

			ax.plot(param,param2, color='red')
			ax.plot(i, (param2[0]), 'ro', ms=12, markeredgecolor='red')
			ax.annotate(str(i+1), xy=(i, param2[0]+k), color='black',fontsize="large", weight='heavy',
						horizontalalignment='center',
						verticalalignment='center')
			ax.plot([i], param2[1], marker=7, ms=10, color='red')
		else:
			param2 = [sortc.index(corrente[i][0] + dtmin / 2), sortc.index(corrente[i][1] + dtmin / 2)]

			ax.plot(param,param2, color='blue')
			ax.plot(i, (param2[0]), 'bo', ms=10, markeredgecolor='blue')
			ax.annotate(str(i+1), xy=(i, param2[0]-k), color='black',fontsize="large", weight='heavy',
						horizontalalignment='center',
						verticalalignment='center')
			ax.plot([i], param2[1], marker=6,ms=10,color='blue')

	sortc = [round(num, 5) for num in sortc]
	ax.set_yticks(np.arange(0, len(sortc), step=1))
	ax.set_yticklabels(sortc,fontsize=20)

	ax.grid(axis="y", color="black", alpha=.5, linewidth=.5, linestyle="-")
	op=len(corrente)

	if(op<15):
		op=25
	opy=len(sortc)

	if opy>10:
		opy=15*opy
	else:
		opy=len(correntegrid)

	fig.set_size_inches(0.4*op, 5.3+0.015*opy)
	# fig.savefig("EC2.png", bbox_inches='tight')
	return fig
