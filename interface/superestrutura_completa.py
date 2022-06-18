import numpy as np
import time

nstages = 2
subestagios = [[], []]
quentes_usadas = []
frias_usadas = []
subq_usadas = []
subf_usadas = []
linha_interface_ev = []

#VARIÁVEIS DE CALOR
Qtotalh01 = []
Qtotalc01 = []
calor_atual_quente_ev = []
calor_atual_frio_ev = []
calor_atual_quente_ev_sub = []
calor_atual_frio_ev_sub = []
calor_sub_sem_utilidade_ev = []

#VARIÁVEIS DE TEMPERATURAS QUENTES
temperatura_atual_quente_ev = []
temperatura_atual_quente_ev_mesclada = []
temp_misturador_quente = []

#VARIÁVEIS DE TEMPERATURAS FRIAS
temperatura_atual_fria_ev = []
temperatura_atual_fria_ev_mesclada = []
temp_misturador_frio = []

#OUTRAS VARIÁVEIS
dividida_quente_ev_acima = []
dividida_quente_ev_abaixo = []
dividida_fria_ev_acima = []
dividida_fria_ev_abaixo = []
quantidade_quente_ev_acima = []
quantidade_quente_ev_abaixo = []
quantidade_fria_ev_acima = []
quantidade_fria_ev_abaixo = []
fracoes_quentes_ev_acima = []
fracoes_quentes_ev_abaixo = []
fracoes_frias_ev_acima = []
fracoes_frias_ev_abaixo = []
fechar_corrente_ev = []
fechar_corrente_ev_abaixo = []

def declarar_np(*args):
	x = np.array([0.0])
	x.resize(args)
	return x

def preparar_dados_e_rede(sk=2):
	global Qtotalh01, Qtotalc01, Qtotalh0, Qtotalc0
	global Thski, Thki, Thskf, Thkf, Tcski, Tcki, Tcskf, Tckf
	global Fharr, Fcarr, Q

	Thski = declarar_np(nhot, ncold+2, nsk, nstages)
	Thskf = declarar_np(nhot, ncold+2, nsk, nstages)
	Tcski = declarar_np(ncold, nhot+2, nsk, nstages)
	Tcskf = declarar_np(ncold, nhot+2, nsk, nstages)
	Q = declarar_np(nhot, ncold+2, ncold, nhot+2, nsk, nstages)

	subestagios[0].clear()
	subestagios[1].clear()
	quentes_usadas.clear()
	frias_usadas.clear()
	for i in range(len(subq_usadas)):
		subq_usadas[i].clear()
		for j in range(len(subf_usadas)):
			subf_usadas[j].clear()
	if sk == 4:
		linha_interface_ev.clear()

	else:
		Qtotalh0 = declarar_np(nhot, ncold+2, nstages)
		Qtotalc0 = declarar_np(ncold, nhot+2, nstages)
		Thki = declarar_np(nhot, nstages)
		Thkf = declarar_np(nhot, nstages)
		Tckf = declarar_np(ncold, nstages)
		Tcki = declarar_np(ncold, nstages)
		Fharr = declarar_np(nstages, nhot, ncold+2)
		Fcarr = declarar_np(nstages, ncold, nhot+2)

		for quente in range(nhot):
			temperatura_atual_quente_ev.append([])
			temperatura_atual_quente_ev_mesclada.append(Th0[quente])
			temp_misturador_quente.append(0)
			calor_atual_quente_ev_sub.append([])
			dividida_quente_ev_acima.append(False)
			dividida_quente_ev_abaixo.append(False)
			fechar_corrente_ev_abaixo.append(False)
			quantidade_quente_ev_acima.append(1)
			quantidade_quente_ev_abaixo.append(1)
			fracoes_quentes_ev_acima.append([])
			fracoes_quentes_ev_abaixo.append([])
			subq_usadas.append([])
			for sub in range(ncold+2):
				calor_atual_quente_ev_sub[quente].append(0)
				temperatura_atual_quente_ev[quente].append(Th0[quente])
		for fria in range(ncold):
			temperatura_atual_fria_ev.append([])
			temperatura_atual_fria_ev_mesclada.append(Tc0[fria])
			temp_misturador_frio.append(0)
			calor_atual_frio_ev_sub.append([])
			calor_sub_sem_utilidade_ev.append([])
			dividida_fria_ev_acima.append(False)
			dividida_fria_ev_abaixo.append(False)
			fechar_corrente_ev.append(False)
			quantidade_fria_ev_acima.append(1)
			quantidade_fria_ev_abaixo.append(1)
			fracoes_frias_ev_acima.append([])
			fracoes_frias_ev_abaixo.append([])
			subf_usadas.append([])
			for sub in range(nhot+2):
				calor_atual_frio_ev_sub[fria].append(0)
				temperatura_atual_fria_ev[fria].append(Tc0[fria])

		#calores totais
		for i in range(nhot):
			Qtotalh01.append(CPh[i] * (Th0[i] - Thf[i]))
			calor_atual_quente_ev.append(CPh[i] * (Th0[i] - Thf[i]))
			calor_atual_quente_ev_sub[i][0] = CPh[i] * (Th0[i] - Thf[i])
		for j in range(ncold):
			Qtotalc01.append(CPc[j] * (Tcf[j] - Tc0[j]))
			calor_atual_frio_ev.append(CPc[j] * (Tcf[j] - Tc0[j]))
			calor_atual_frio_ev_sub[j][0] = CPc[j] * (Tcf[j] - Tc0[j])

		for i in range(nhot):
			for j in range(ncold):
				for k in range(nstages):
					Qtotalh0[i][0][k] = Qtotalh01[i]
					Qtotalc0[j][0][k] = Qtotalc01[j]

	for i in range(nhot):
		for si in range(ncold+2):
			for sk in range(nsk):
				for k in range(nstages):
					Thski[i][si][sk][k] = Th0[i]
					Thskf[i][si][sk][k] = Th0[i]
		for k in range(nstages):
			Thki[i][k] = Th0[i]
			Thkf[i][k] = Th0[i]

	for j in range(ncold):
		for sj in range(nhot+2):
			for sk in range(nsk-1, -1, -1):
				for k in range(nstages-1, -1, -1):
					Tcski[j][sj][sk][k] = Tc0[j]
					Tcskf[j][sj][sk][k] = Tc0[j]
		for k in range(nstages-1, -1, -1):
			Tcki[j][k] = Tc0[j]
			Tckf[j][k] = Tc0[j]

def receber_pinch_ev(matriz_quente, matriz_fria, nquentes, nfrias, CPquente, CPfrio, deltaTmin, pinch_quente, pinch_frio, matriz_quente_in, matriz_fria_in, nska):
	global Th0, Thf, Tc0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, nsk
	Th0, Thf, Tc0, Tcf = [], [], [], []
	CPh, CPc = [], []
	for corrente in range(nquentes):
		Th0.append(matriz_quente_in[corrente])
		Thf.append(matriz_quente[corrente])
		CPh.append(CPquente[corrente])
	for corrente in range(nfrias):
		Tc0.append(matriz_fria_in[corrente])
		Tcf.append(matriz_fria[corrente])
		CPc.append(CPfrio[corrente])
	pinchq = pinch_quente
	pinchf = pinch_frio
	nhot = nquentes
	ncold = nfrias
	dTmin = deltaTmin
	nsk = nska
	preparar_dados_e_rede()

def remocao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio):
	Qtotalestagioq = Qtotalestagiof = 0
	if Fharr[estagio-1][chot-1][sbhot-1] == 0:
		Qtotalh0[chot-1][sbhot-1][estagio-1] = Qtotalh0[chot-1][sbhot-1][estagio-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagioq = 0
			if k == (estagio-1):
				continue
			else:
				if Fharr[k][chot-1][sbhot-1] == 0:
					Qtotalh0[chot-1][sbhot-1][k] = Qtotalh0[chot-1][sbhot-1][k] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for si in range(ncold+2):
						Qtotalestagioq += Qtotalh0[chot-1][si][k]
					Qtotalestagioq = Qtotalestagioq - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for si in range(ncold+2):
						Qtotalh0[chot-1][si][k] = Qtotalestagioq*(Fharr[k][chot-1][si]/100)
	else:
		Qtotalh0[chot-1][sbhot-1][estagio-1] = Qtotalh0[chot-1][sbhot-1][estagio-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagioq = 0
			if k == (estagio-1):
				continue
			else:
				if Fharr[k][chot-1][sbhot-1] == 0:
					Qtotalh0[chot-1][0][k] = Qtotalh0[chot-1][0][k] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for si in range(ncold+2):
						Qtotalestagioq += Qtotalh0[chot-1][si][k]
					Qtotalestagioq = Qtotalestagioq - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for si in range(ncold+2):
						Qtotalh0[chot-1][si][k] = Qtotalestagioq*(Fharr[k][chot-1][si]/100)

	if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
		Qtotalc0[ccold-1][sbcold-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1][estagio-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagiof = 0
			if k == (estagio-1):
				continue
			else:
				if Fcarr[k][ccold-1][sbcold-1] == 0:
					Qtotalc0[ccold-1][sbcold-1][k] = Qtotalc0[ccold-1][sbcold-1][k] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for sj in range(nhot+2):
						Qtotalestagiof += Qtotalc0[ccold-1][sj][k]
					Qtotalestagiof = Qtotalestagiof - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for sj in range(nhot+2):
						Qtotalc0[ccold-1][sj][k] = Qtotalestagiof*(Fcarr[k][ccold-1][sj]/100)
	else:
		Qtotalc0[ccold-1][sbcold-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1][estagio-1] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagiof = 0
			if k == (estagio-1):
				continue
			else:
				if Fcarr[k][ccold-1][sbcold-1] == 0:
					Qtotalc0[ccold-1][0][k] = Qtotalc0[ccold-1][0][k] - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for sj in range(nhot+2):
						Qtotalestagiof += Qtotalc0[ccold-1][sj][k]
					Qtotalestagiof = Qtotalestagiof - Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for sj in range(nhot+2):
						Qtotalc0[ccold-1][sj][k] = Qtotalestagiof*(Fcarr[k][ccold-1][sj]/100)

def adicao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio):
	Qtotalestagioq = Qtotalestagiof = 0
	if Fharr[estagio-1][chot-1][sbhot-1] == 0:
		Qtotalh0[chot-1][sbhot-1][estagio-1] = Qtotalh0[chot-1][sbhot-1][estagio-1] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagioq = 0
			if k == (estagio-1):
				continue
			else:
				if Fharr[k][chot-1][sbhot-1] == 0:
					Qtotalh0[chot-1][sbhot-1][k] = Qtotalh0[chot-1][sbhot-1][k] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for si in range(ncold+2):
						Qtotalestagioq += Qtotalh0[chot-1][si][k]
					Qtotalestagioq = Qtotalestagioq + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for si in range(ncold+2):
						Qtotalh0[chot-1][si][k] = Qtotalestagioq*(Fharr[k][chot-1][si]/100)
	else:
		Qtotalh0[chot-1][sbhot-1][estagio-1] = Qtotalh0[chot-1][sbhot-1][estagio-1] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagioq = 0
			if k == (estagio-1):
				continue
			else:
				if Fharr[k][chot-1][sbhot-1] == 0:
					Qtotalh0[chot-1][0][k] = Qtotalh0[chot-1][0][k] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for si in range(ncold+2):
						Qtotalestagioq += Qtotalh0[chot-1][si][k]
					Qtotalestagioq = Qtotalestagioq + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for si in range(ncold+2):
						Qtotalh0[chot-1][si][k] = Qtotalestagioq*(Fharr[k][chot-1][si]/100)

	if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
		Qtotalc0[ccold-1][sbcold-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1][estagio-1] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagiof = 0
			if k == (estagio-1):
				continue
			else:
				if Fcarr[k][ccold-1][sbcold-1] == 0:
					Qtotalc0[ccold-1][sbcold-1][k] = Qtotalc0[ccold-1][sbcold-1][k] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for sj in range(nhot+2):
						Qtotalestagiof += Qtotalc0[ccold-1][sj][k]
					Qtotalestagiof = Qtotalestagiof + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for sj in range(nhot+2):
						Qtotalc0[ccold-1][sj][k] = Qtotalestagiof*(Fcarr[k][ccold-1][sj]/100)
	else:
		Qtotalc0[ccold-1][sbcold-1][estagio-1] = Qtotalc0[ccold-1][sbcold-1][estagio-1] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		for k in range(nstages):
			Qtotalestagiof = 0
			if k == (estagio-1):
				continue
			else:
				if Fcarr[k][ccold-1][sbcold-1] == 0:
					Qtotalc0[ccold-1][0][k] = Qtotalc0[ccold-1][0][k] + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
				else:
					for sj in range(nhot+2):
						Qtotalestagiof += Qtotalc0[ccold-1][sj][k]
					Qtotalestagiof = Qtotalestagiof + Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
					for sj in range(nhot+2):
						Qtotalc0[ccold-1][sj][k] = Qtotalestagiof*(Fcarr[k][ccold-1][sj]/100)

def calcular_superestrutura():
	for i in sorted(quentes_usadas):
		for si in sorted(subq_usadas[i]):
			for k in range(nstages):
				for sk in sorted(subestagios[k]):
					Thski[i][si][sk][k] = Th0[i]
					Thskf[i][si][sk][k] = Th0[i]

		for k in range(nstages):
			Thki[i][k] = Th0[i]
			Thkf[i][k] = Th0[i]

	for j in sorted(frias_usadas):
		for sj in sorted(subf_usadas[j]):
			for k in range(nstages-1, -1, -1):
				for sk in reversed(sorted(subestagios[k])):
					Tcski[j][sj][sk][k] = Tc0[j]
					Tcskf[j][sj][sk][k] = Tc0[j]
		for k in range(nstages-1, -1, -1):
			Tcki[j][k] = Tc0[j]
			Tckf[j][k] = Tc0[j]

	#CÁLCULO DE TODA A SUPERESTRUTURA QUENTE
	for k in range(nstages):
		for sk in sorted(subestagios[k]):
			for i in sorted(quentes_usadas):
				for si in sorted(subq_usadas[i]):
					for j in sorted(frias_usadas):
						for sj in sorted(subf_usadas[j]):

							if Q[i][si][j][sj][sk][k] != 0:
								# print("achou", time.time())

								Qestagioq = 0
								for si1 in sorted(subq_usadas[i]):
									for j1 in sorted(frias_usadas):
										for sj1 in sorted(subf_usadas[j1]):
											for sk1 in sorted(subestagios[k]):
												Qestagioq += Q[i][si1][j1][sj1][sk1][k]

								if Fharr[k][i][si] == 0:
									Fharr[k][i][si] = 100

								Thin = Thski[i][si][sk][k]
								Thout = Thin - (Q[i][si][j][sj][sk][k]/(CPh[i]*Fharr[k][i][si]/100))

								Think = Thki[i][k]
								Thoutk = Think - (Qestagioq/CPh[i])

								temperatura_atual_quente_ev_mesclada[i] = Thoutk

								#Temperatura de estágios e sub-estágios
								for k1 in range(nstages):
									for sk1 in sorted(subestagios[k1]):
										if k1 > (k):
											Thki[i][k1] = Thoutk
											Thkf[i][k1] = Thoutk

											for sub_quente in range(ncold+2):
												Thski[i][sub_quente][sk1][k1] = Thoutk
												Thskf[i][sub_quente][sk1][k1] = Thoutk

										if k1 == (k):
											if sk1 >= (sk):
												if sk1 > sk:
													Thski[i][si][sk1][k1] = Thout
												Thskf[i][si][sk1][k1] = Thout
											Thkf[i][k1] = Thoutk

								if Fharr[k][i][si] == 100:
									Fharr[k][i][si] = 0

	#CÁLCULO DE TODA A SUPERESTRUTURA FRIA
	for k in range(nstages-1, -1, -1):
		for sk in reversed(sorted(subestagios[k])):
			for i in sorted(quentes_usadas):
				for si in sorted(subq_usadas[i]):
					for j in sorted(frias_usadas):
						for sj in sorted(subf_usadas[j]):

							if Q[i][si][j][sj][sk][k] != 0:

								Qestagiof = 0
								for sj1 in sorted(subf_usadas[j]):
									for i1 in sorted(quentes_usadas):
										for si1 in sorted(subq_usadas[i1]):
											for sk1 in sorted(subestagios[k]):
												Qestagiof += Q[i1][si1][j][sj1][sk1][k]

								if Fcarr[k][j][sj] == 0:
									Fcarr[k][j][sj] = 100

								Tcin = Tcski[j][sj][sk][k]
								Tcout = Tcin + (Q[i][si][j][sj][sk][k]/(CPc[j]*Fcarr[k][j][sj]/100))

								Tcink = Tcki[j][k]
								Tcoutk = Tcink + (Qestagiof/CPc[j])

								tempdif = Thin - Tcout
								tempdif_terminal_frio = Thout - Tcin

								temperatura_atual_fria_ev_mesclada[j] = Tcoutk

								#Temperatura de estágios e sub-estágios
								for k1 in range(nstages-1, -1, -1):
									for sk1 in reversed(sorted(subestagios[k1])):
										if k1 < (k):
											Tcki[j][k1] = Tcoutk
											Tckf[j][k1] = Tcoutk

											for sub_fria in range(nhot+2):
												Tcski[j][sub_fria][sk1][k1] = Tcoutk
												Tcskf[j][sub_fria][sk1][k1] = Tcoutk

										if k1 == (k):
											if sk1 <= (sk):
												if sk1 < sk:
													Tcski[j][sj][sk1][k1] = Tcout
												Tcskf[j][sj][sk1][k1] = Tcout
											Tckf[j][k1] = Tcoutk

								if Fcarr[k][j][sj] == 100:
									Fcarr[k][j][sj] = 0

def divisao_de_correntes_ev(divtype, estagio, corrente, quantidade, fracao):
	qsi = quantidade
	qsj = quantidade
	cont = 0
	if cont == 0:
		if divtype.upper() == 'Q':
			#desfaz divisoes anteriores da corrente no estagio
			for si in range(1, ncold):
				Qtotalh0[corrente-1][0][estagio-1] += Qtotalh0[corrente-1][si][estagio-1]
			for si in range(ncold-1, qsi-1, -1):#ex: antes 3 divisoes porem agora 2, zera a 3
				Fharr[estagio-1][corrente-1][si] = 0
				Qtotalh0[corrente-1][si][estagio-1] = 0
			#faz a nova divisao
			if qsi <= ncold:
				for si in range(qsi):
					Fharr[estagio-1][corrente-1][si] = 100 * fracao[si]
				for si in range(ncold-1, -1, -1):
					if Fharr[estagio-1][corrente-1][si] != 0:
						Qtotalh0[corrente-1][si][estagio-1] = Qtotalh0[corrente-1][0][estagio-1]*(Fharr[estagio-1][corrente-1][si]/100)
						calor_atual_quente_ev_sub[corrente-1][si] = Qtotalh0[corrente-1][si][estagio-1]
			if estagio == 1:
				if fracao[0] != 1:
					dividida_quente_ev_acima[corrente-1] = True
				else:
					dividida_quente_ev_acima[corrente-1] = False
				quantidade_quente_ev_acima[corrente-1] = qsi
				fracoes_quentes_ev_acima[corrente-1] = fracao[:]
			else:
				if fracao[0] != 1:
					dividida_quente_ev_abaixo[corrente-1] = True
				else:
					dividida_quente_ev_abaixo[corrente-1] = False
				quantidade_quente_ev_abaixo[corrente-1] = qsi
				fracoes_quentes_ev_abaixo[corrente-1] = fracao[:]

		if divtype.upper() == 'F':
			#desfaz divisoes anteriores da corrente no estagio
			for sj in range(1, nhot):
				Qtotalc0[corrente-1][0][estagio-1] += Qtotalc0[corrente-1][sj][estagio-1]
			for sj in range(nhot-1, qsj-1, -1):
				Fcarr[estagio-1][corrente-1][sj] = 0
				Qtotalc0[corrente-1][sj][estagio-1] = 0
			#faz a nova divisao
			if qsj <= nhot:
				for sj in range(qsj):
					Fcarr[estagio-1][corrente-1][sj] = 100 * fracao[sj]
				for sj in range(nhot-1, -1, -1):
					if Fcarr[estagio-1][corrente-1][sj] != 0:
						Qtotalc0[corrente-1][sj][estagio-1] = Qtotalc0[corrente-1][0][estagio-1]*(Fcarr[estagio-1][corrente-1][sj]/100)
						calor_atual_frio_ev_sub[corrente-1][sj] = Qtotalc0[corrente-1][sj][estagio-1]
			if estagio == 1:
				if fracao[0] != 1:
					dividida_fria_ev_acima[corrente-1] = True
				else:
					dividida_fria_ev_acima[corrente-1] = False
				quantidade_fria_ev_acima[corrente-1] = qsj
				fracoes_frias_ev_acima[corrente-1] = fracao[:]
			else:
				if fracao[0] != 1:
					dividida_fria_ev_abaixo[corrente-1] = True
				else:
					dividida_fria_ev_abaixo[corrente-1] = False
				quantidade_fria_ev_abaixo[corrente-1] = qsj
				fracoes_frias_ev_abaixo[corrente-1] = fracao[:]

def inserir_trocador_ev(matriz):
	for trocador in matriz:
		chot = trocador[0]
		ccold = trocador[1]
		sbhot = trocador[2]
		sbcold = trocador[3]
		sestagio = trocador[4]
		estagio = trocador[5]
		Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = trocador[6]

		if chot-1 not in quentes_usadas:
			quentes_usadas.append(chot-1)
		if ccold-1 not in frias_usadas:
			frias_usadas.append(ccold-1)
		if sbhot-1 not in subq_usadas[chot-1]:
			subq_usadas[chot-1].append(sbhot-1)
		if sbcold-1 not in subf_usadas[ccold-1]:
			subf_usadas[ccold-1].append(sbcold-1)
		if sestagio-1 not in subestagios[estagio-1]:
			subestagios[estagio-1].append(sestagio-1)

	calcular_superestrutura()

	for trocadorr in matriz:
		chot = trocadorr[0]
		ccold = trocadorr[1]
		sbhot = trocadorr[2]
		sbcold = trocadorr[3]
		sestagio = trocadorr[4]
		estagio = trocadorr[5]

		remocao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

		if Fharr[estagio-1][chot-1][sbhot-1] == 0:
			fracao_quente = 1
		else:
			fracao_quente = Fharr[estagio-1][chot-1][sbhot-1]/100
		if Fcarr[estagio-1][ccold-1][sbcold-1] == 0:
			fracao_fria = 1
		else:
			fracao_fria = Fcarr[estagio-1][ccold-1][sbcold-1]/100

		calor_atual_quente_ev[chot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		calor_atual_frio_ev[ccold-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		calor_atual_quente_ev_sub[chot-1][sbhot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		calor_atual_frio_ev_sub[ccold-1][sbcold-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		temp_misturador_quente[chot-1] = Thkf[chot-1][estagio-1]
		temp_misturador_frio[ccold-1] = Tckf[ccold-1][estagio-1]

		linha_interface_ev.append([chot,
								ccold,
								sbhot,
								sbcold,
								sestagio,
								estagio,
								Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1],
								Thski[chot-1][sbhot-1][sestagio-1][estagio-1],
								Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1],
								Thskf[chot-1][sbhot-1][sestagio-1][estagio-1],
								Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1],
								fracao_quente,
								fracao_fria])

		for trocador in linha_interface_ev:
			trocador[7] = Thski[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
			trocador[8] = Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]
			trocador[9] = Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
			trocador[10] = Tcski[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]

	return linha_interface_ev

def remover_todos_ev():
	for vetorr in linha_interface_ev:
		chot = vetorr[0]
		ccold = vetorr[1]
		sbhot = vetorr[2]
		sbcold = vetorr[3]
		sestagio = vetorr[4]
		estagio = vetorr[5]

		adicao_de_calor(chot, ccold, sbhot, sbcold, sestagio, estagio)

		Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0

		calor_atual_quente_ev[chot-1] += vetorr[6]
		calor_atual_frio_ev[ccold-1] += vetorr[6]

	subestagios[0].clear()
	subestagios[1].clear()
	quentes_usadas.clear()
	frias_usadas.clear()
	for i in range(len(subq_usadas)):
		subq_usadas[i].clear()
	for j in range(len(subf_usadas)):
		subf_usadas[j].clear()

	linha_interface_ev.clear()

def calcular_recomendado_violacao(dlg, trocador):
	if Fharr[trocador[5]-1][trocador[0]-1][trocador[2]-1] == 0:
		fracao_quente = 1
	else:
		fracao_quente = Fharr[trocador[5]-1][trocador[0]-1][trocador[2]-1] / 100
	if Fcarr[trocador[5]-1][trocador[1]-1][trocador[3]-1] == 0:
		fracao_fria = 1
	else:
		fracao_fria = Fcarr[trocador[5]-1][trocador[1]-1][trocador[3]-1] / 100
	cpquente = CPh[trocador[0]-1] * fracao_quente
	cpfrio = CPc[trocador[1]-1] * fracao_fria
	tqin = trocador[7]
	tfout = trocador[8]
	tqout = trocador[9]
	tfin = trocador[10]
	calor = original = trocador[6]
	x = ["None", "None"]
	if tqin - tfout < dTmin or tqout - tfin < dTmin:
		if tqin - tfout >= 0 and tqout - tfin >= 0:
			x[0] = str(0.00)
		while calor > 0:
			calor -= 1
			tqout = -calor / cpquente + tqin
			tfout = calor / cpfrio + tfin
			dtquente = tqin - tfout
			dtfrio = tqout - tfin
			if dtquente > 0 and dtfrio > 0 and x[0] == "None":
				calor1 = original - calor
				x[0] = str('{:.2f}'.format(round(calor1, 2)))
				x[1] = str('{:.2f}'.format(round(calor1, 2)))
			if dtquente > dTmin and dtfrio > dTmin:
				calor2 = original - calor
				x[1] =  str('{:.2f}'.format(round(calor2, 2)))
				break
	dlg.calor_path.clear()
	dlg.calor_path.setPlaceholderText("ΔT > 0: " + x[0] + ", ΔT > ΔTmin: " + x[1])
