import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter

import numpy as np

def cc1(Grafico,dtmin,tf,tq, unidades):
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
	ax.grid(axis="x", color="black", alpha=.3, linewidth=2, linestyle=":")
	ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
	ax.legend()

	# fig.savefig("cc1.png",bbox_inches="tight", pad_inches=0.5)
	return fig


def cc2(Grafico,dtmin,tf,tq, unidades):
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
	ax.plot(pinchx, pinch, label='Pinch: ' + str(dtmin)+ ' {}'.format(temp), color='k')
	ax.set_xlabel('H ({})'.format(energia))
	ax.set_ylabel('T ({})'.format(temp))

	ax.plot(Grafico[2],Grafico[0], label='Hot balanced composite curves', color='r')
	ax.grid(axis="x", color="black", alpha=.3, linewidth=2, linestyle=":")
	ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
	ax.legend()

	# fig.savefig("cc2.png",bbox_inches="tight", pad_inches=0.5)
	return fig
