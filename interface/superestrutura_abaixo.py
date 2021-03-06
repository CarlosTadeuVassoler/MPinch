from PyQt5.QtWidgets import QMessageBox
import numpy as np

nstages = 1
subestagios = []
quentes_usadas = []
frias_usadas = []
quentesxfrias = []
friasxquentes = []
subq_usadas = []
subf_usadas = []
linha_interface_abaixo = []
utilidades_abaixo = []

#VARIÁVEIS DO CALOR
Qtotalh01 = []
Qtotalc01 = []
calor_atual_quente_abaixo = []
calor_atual_frio_abaixo = []
calor_atual_quente_sub_abaixo = []
calor_atual_frio_sub_abaixo = []
calor_sub_sem_utilidade = []

#VARIÁVEIS DE TEMPERATURAS QUENTES
temperatura_atual_quente_abaixo = []
temperatura_atual_quente_mesclada_abaixo = []

#VARIÁVEIS DE TEMPERATURAS FRIAS
temperatura_atual_fria_abaixo = []
temperatura_atual_fria_mesclada_abaixo = []
temp_misturador_abaixo = []

#VARIÁVEIS DE DIVISÃO
dividida_quente_abaixo = []
dividida_fria_abaixo = []
quantidade_quente_abaixo = []
quantidade_fria_abaixo = []
fracoes_quentes_abaixo = []
fracoes_frias_abaixo = []
fechar_corrente_abaixo = []

def mensagem_err(texto, titulo="Error"):
	msg = QMessageBox()
	msg.setIcon(QMessageBox.Warning)
	msg.setStyleSheet("font-weight: bold")
	msg.setStyleSheet("text-align: center")
	msg.setText(texto)
	msg.setWindowTitle(titulo)
	msg.setStandardButtons(QMessageBox.Ok)
	msg.exec_()
	return

def declarar_np(*args):
	x = np.array([0.0])
	x.resize(args)
	return x

def preparar_dados_e_rede2():
	global Qtotalh01, Qtotalc01, Qtotalh0, Qtotalc0
	global Thski, Thki, Thskf, Thkf, Tcski, Tcki, Tcskf, Tckf
	global Fharr, Fcarr, Q

	Thski = declarar_np(nhot, ncold, nsk, nstages)
	Thskf = declarar_np(nhot, ncold, nsk, nstages)
	Tcski = declarar_np(ncold, nhot, nsk, nstages)
	Tcskf = declarar_np(ncold, nhot, nsk, nstages)
	Q = declarar_np(nhot, ncold, ncold, nhot, nsk, nstages)

	Qtotalh0 = declarar_np(nhot, ncold, nstages)
	Qtotalc0 = declarar_np(ncold, nhot, nstages)
	Thki = declarar_np(nhot, nstages)
	Thkf = declarar_np(nhot, nstages)
	Tckf = declarar_np(ncold, nstages)
	Tcki = declarar_np(ncold, nstages)
	Fharr = declarar_np(nstages, nhot, ncold)
	Fcarr = declarar_np(nstages, ncold, nhot)

	for est in range(nstages):
		for q in range(nhot):
			for sq in range(ncold):
				Fharr[est][q][sq] = 100
		for f in range(ncold):
			for sf in range(nhot):
				Fcarr[est][f][sf] = 100

	for quente in range(nhot):
		temperatura_atual_quente_abaixo.append([])
		temperatura_atual_quente_mesclada_abaixo.append(Th0[quente])
		calor_atual_quente_sub_abaixo.append([])
		dividida_quente_abaixo.append(False)
		quantidade_quente_abaixo.append(1)
		fracoes_quentes_abaixo.append([])
		fechar_corrente_abaixo.append(False)
		temp_misturador_abaixo.append(0)
		calor_sub_sem_utilidade.append([])
		quentesxfrias.append([])
		subq_usadas.append([])
		for sub in range(ncold):
			calor_atual_quente_sub_abaixo[quente].append(0)
			temperatura_atual_quente_abaixo[quente].append(Th0[quente])
	for fria in range(ncold):
		temperatura_atual_fria_abaixo.append([])
		temperatura_atual_fria_mesclada_abaixo.append(Tcf[fria])
		calor_atual_frio_sub_abaixo.append([])
		dividida_fria_abaixo.append(False)
		quantidade_fria_abaixo.append(1)
		fracoes_frias_abaixo.append([])
		friasxquentes.append([])
		subf_usadas.append([])
		for sub in range(nhot):
			calor_atual_frio_sub_abaixo[fria].append(0)
			temperatura_atual_fria_abaixo[fria].append(Tcf[fria])

	#calores totais
	for i in range(nhot):
		if Th0[i] <= Thf[i]:
			CPh[i] = 0
		Qtotalh01.append(CPh[i] * (Th0[i] - Thf[i]))
		calor_atual_quente_abaixo.append(CPh[i] * (Th0[i] - Thf[i]))
		calor_atual_quente_sub_abaixo[i][0] = CPh[i] * (Th0[i] - Thf[i])
	for j in range(ncold):
		if Tcf[j] <= Tc0[j]:
			CPc[j] = 0
		Qtotalc01.append(CPc[j] * (Tcf[j] - Tc0[j]))
		calor_atual_frio_abaixo.append(CPc[j] * (Tcf[j] - Tc0[j]))
		calor_atual_frio_sub_abaixo[j][0] = CPc[j] * (Tcf[j] - Tc0[j])

	for i in range(nhot):
		for j in range(ncold):
			for k in range(nstages):
				Qtotalh0[i][0][k] = Qtotalh01[i]
				Qtotalc0[j][0][k] = Qtotalc01[j]

	#prepara rede
	for i in range(nhot):
		for si in range(ncold):
			for sk in range(nsk):
				for k in range(nstages):
					Thski[i][si][sk][k] = Th0[i]
					Thskf[i][si][sk][k] = Th0[i]
		for k in range(nstages):
			Thki[i][k] = Th0[i]
			Thkf[i][k] = Th0[i]

	for j in range(ncold):
		for sj in range(nhot):
			for sk in range(nsk-1, -1, -1):
				for k in range(nstages-1, -1, -1):
					Tcski[j][sj][sk][k] = Tcf[j]
					Tcskf[j][sj][sk][k] = Tcf[j]
		for k in range(nstages-1, -1, -1):
			Tcki[j][k] = Tcf[j]
			Tckf[j][k] = Tcf[j]

def receber_pinch_abaixo(matriz_quente, matriz_fria, nquentes, nfrias, CPquente, CPfrio, deltaTmin, pinch_quente, pinch_frio, matriz_quente_in, matriz_fria_in):
	global Th0, Thf, Tc0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, nsk
	Th0, Thf, Tc0, Tcf, CPh, CPc = [], [], [], [], [], []
	for corrente in range(nquentes):
		Thf.append(matriz_quente[corrente])
		Th0.append(matriz_quente_in[corrente])
		CPh.append(CPquente[corrente])
	for corrente in range(nfrias):
		Tc0.append(matriz_fria[corrente])
		Tcf.append(matriz_fria_in[corrente])
		CPc.append(CPfrio[corrente])
	pinchq = pinch_quente
	pinchf = pinch_frio
	nhot = nquentes
	ncold = nfrias
	dTmin = deltaTmin
	nsk = 5*max(nhot, ncold)
	preparar_dados_e_rede2()

def verificar_trocador_estagio_abaixo(estagio, corrente, tipo):
	if tipo == "Q":
		for si in range(ncold): #max de subcorrentes quentes é igual ao numero de correntes frias
			for j in range(ncold):
				for sj in range(nhot): #max de subcorrentes frias é igual ao numero de correntes quentes
					for sk in range(nsk):
						if Q[corrente-1][si][j][sj][sk][estagio-1] != 0:
							return True
	elif tipo == "F":
		for i in range(nhot):
			for si in range(ncold): #max de subcorrentes quentes é igual ao numero de correntes frias
				for sj in range(nhot): #max de subcorrentes frias é igual ao numero de correntes quentes
					for sk in range(nsk):
						if Q[i][si][corrente-1][sj][sk][estagio-1] != 0:
							return True

def calcular_superestrutura_abaixo(acao, chot, ccold, sbhot, sbcold, sestagio, estagio):
	ultimo = -1
	sai = False
	for sk in range(sestagio-2, -1, -1):
		for j in sorted(quentesxfrias[chot-1]):
			for sj in sorted(subf_usadas[j]):
				if Q[chot-1][sbhot-1][j][sj][sk][estagio-1] != 0:
					ultimo = sk
					sai = True
					break
			if sai:
				break
		if sai:
			break

	ultimof = -1
	sai = False
	for sk in range(sestagio-2, -1, -1):
		for i in sorted(friasxquentes[ccold-1]):
			for si in sorted(subq_usadas[i]):
				if Q[i][si][ccold-1][sbcold-1][sk][estagio-1] != 0:
					ultimof = sk
					sai = True
					break
			if sai:
				break
		if sai:
			break

	if ultimo != -1:
		Thski[chot-1][sbhot-1][sestagio-1][estagio-1] = Thskf[chot-1][sbhot-1][ultimo][estagio-1]
	else:
		Thski[chot-1][sbhot-1][sestagio-1][estagio-1] = Th0[chot-1]

	if ultimof != -1:
		Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1] = Tcskf[ccold-1][sbcold-1][ultimof][estagio-1]
	else:
		Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1] = Tcf[ccold-1]

	Qestagioq = 0
	for si1 in subq_usadas[chot-1]:
		for j1 in quentesxfrias[chot-1]:
			for sj1 in subf_usadas[j1]:
				for sk1 in subestagios:
					Qestagioq += Q[chot-1][si1][j1][sj1][sk1][estagio-1]

	Qestagiof = 0
	for sj1 in subf_usadas[ccold-1]:
		for i1 in friasxquentes[ccold-1]:
			for si1 in subq_usadas[i1]:
				for sk1 in subestagios:
					Qestagiof += Q[i1][si1][ccold-1][sj1][sk1][estagio-1]

	Thskf[chot-1][sbhot-1][sestagio-1][estagio-1] = Thski[chot-1][sbhot-1][sestagio-1][estagio-1] - (Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]/(CPh[chot-1]*Fharr[estagio-1][chot-1][sbhot-1]/100))
	Thkf[chot-1][estagio-1] = Th0[chot-1] - (Qestagioq/CPh[chot-1])

	temperatura_atual_quente_abaixo[chot-1][sbhot-1] = Thskf[chot-1][sbhot-1][sestagio-1][estagio-1]
	temperatura_atual_quente_mesclada_abaixo[chot-1] = Thkf[chot-1][estagio-1]

	Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1] = Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1] - (Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]/(CPc[ccold-1]*Fcarr[estagio-1][ccold-1][sbcold-1]/100))
	Tckf[ccold-1][estagio-1] = Tcf[ccold-1] - (Qestagiof/CPc[ccold-1])

	temperatura_atual_fria_abaixo[ccold-1][sbcold-1] = Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1]
	temperatura_atual_fria_mesclada_abaixo[ccold-1] = Tckf[ccold-1][estagio-1]

	if acao == "inserir":
		Qtotalh0[chot-1][sbhot-1][estagio-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		Qtotalc0[ccold-1][sbcold-1][estagio-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		calor_atual_quente_abaixo[chot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		calor_atual_frio_abaixo[ccold-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		calor_atual_quente_sub_abaixo[chot-1][sbhot-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		calor_atual_frio_sub_abaixo[ccold-1][sbcold-1] -= Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

	elif acao == "remover":
		Qtotalh0[chot-1][sbhot-1][estagio-1] += Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		Qtotalc0[ccold-1][sbcold-1][estagio-1] += Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		calor_atual_quente_abaixo[chot-1] += Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		calor_atual_frio_abaixo[ccold-1] += Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		calor_atual_quente_sub_abaixo[chot-1][sbhot-1] += Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]
		calor_atual_frio_sub_abaixo[ccold-1][sbcold-1] += Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1]

def divisao_de_correntes_abaixo(divtype, estagio, corrente, quantidade, fracao):
	qsi = quantidade
	qsj = quantidade
	if divtype.upper() == 'Q':
		#desfaz divisoes anteriores
		for si in range(1, ncold):
			Qtotalh0[corrente-1][0][estagio-1] += Qtotalh0[corrente-1][si][estagio-1]
		for si in range(ncold-1, qsi-1, -1):#ex: antes 3 divisoes porem agora 2, zera a 3
			Fharr[estagio-1][corrente-1][si] = 0
			Qtotalh0[corrente-1][si][estagio-1] = 0
		#faz a nova divisao
		if qsi <= ncold:
			fracoes_quentes_abaixo[corrente-1] = []
			for si in range(qsi):
				Fharr[estagio-1][corrente-1][si] = 100 * fracao[si]
				fracoes_quentes_abaixo[corrente-1].append(fracao[si])
			for si in range(ncold-1, -1, -1):
				if Fharr[estagio-1][corrente-1][si] != 100:
					Qtotalh0[corrente-1][si][estagio-1] = Qtotalh0[corrente-1][0][estagio-1]*(Fharr[estagio-1][corrente-1][si]/100)
					calor_atual_quente_sub_abaixo[corrente-1][si] = Qtotalh0[corrente-1][si][estagio-1]
		if fracoes_quentes_abaixo[corrente-1][0] != 1:
			dividida_quente_abaixo[corrente-1] = True
		else:
			dividida_quente_abaixo[corrente-1] = False
		quantidade_quente_abaixo[corrente-1] = qsi

	if divtype.upper() == 'F':
		#desfaz divisoes anteriores
		for sj in range(1, nhot):
			Qtotalc0[corrente-1][0][estagio-1] += Qtotalc0[corrente-1][sj][estagio-1]
		for sj in range(nhot-1, qsj-1, -1):
			Fcarr[estagio-1][corrente-1][sj] = 0
			Qtotalc0[corrente-1][sj][estagio-1] = 0
		#faz a nova divisao
		if qsj <= nhot:
			fracoes_frias_abaixo[corrente-1] = []
			for sj in range(qsj):
				Fcarr[estagio-1][corrente-1][sj] = 100 * fracao[sj]
				fracoes_frias_abaixo[corrente-1].append(fracao[sj])
			for sj in range(nhot-1, -1, -1):
				if Fcarr[estagio-1][corrente-1][sj] != 100:
					Qtotalc0[corrente-1][sj][estagio-1] = Qtotalc0[corrente-1][0][estagio-1]*(Fcarr[estagio-1][corrente-1][sj]/100)
					calor_atual_frio_sub_abaixo[corrente-1][sj] = Qtotalc0[corrente-1][sj][estagio-1]
		if fracoes_frias_abaixo[corrente-1][0] != 1:
			dividida_fria_abaixo[corrente-1] = True
		else:
			dividida_fria_abaixo[corrente-1] = False
		quantidade_fria_abaixo[corrente-1] = qsj

def ler_dados_abaixo(dlg, subestagio_trocador_abaixo):
	i = int(dlg.comboBox_35.currentIndex()+1)
	j = int(dlg.comboBox_36.currentIndex()+1)
	si = int(dlg.comboBox_53.currentText())
	sj = int(dlg.comboBox_54.currentText())
	k = 1
	sk = subestagio_trocador_abaixo

	if ((Qtotalh0[i-1][si-1][k-1]) > (Qtotalc0[j-1][sj-1][k-1])):
		Qmax = Qtotalc0[j-1][sj-1][k-1]
	else:
		Qmax = Qtotalh0[i-1][si-1][k-1]
	if dlg.radioButton_20.isChecked():
		q = Qmax
	elif dlg.radioButton_17.isChecked():
		q = float(dlg.lineEdit_25.text().replace(",", "."))

	return [i, j, si, sj, sk, k, q]

def inserir_trocador_abaixo(dlg, vetor, verificar_termo=True, ignora=False, ultimo=False):
	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] != 0:
		mensagem_err("There is already a heat exchanger in this position!")
		return linha_interface_abaixo, False

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = vetor[6]

	if ((Qtotalh0[chot-1][sbhot-1][estagio-1]) > (Qtotalc0[ccold-1][sbcold-1][estagio-1])):
		Qmax = Qtotalc0[ccold-1][sbcold-1][estagio-1]
	else:
		Qmax = Qtotalh0[chot-1][sbhot-1][estagio-1]

	if Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] > Qmax:
		if not ignora:
			mensagem_err("The input heat is greater than the available heat.")
			Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0
			return linha_interface_abaixo, False
		elif ultimo:
			mensagem_err("The input heat is greater than the available heat. \nYou will use more than the utility duty.", titulo="Be Carreful")

	matrizes("inserir", chot, ccold, sbhot, sbcold, sestagio, estagio)

	calcular_superestrutura_abaixo("inserir", chot, ccold, sbhot, sbcold, sestagio, estagio)

	linha_interface_abaixo.append([chot,
							ccold,
							sbhot,
							sbcold,
							sestagio,
							estagio,
							Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1],
							Thskf[chot-1][sbhot-1][sestagio-1][estagio-1],
							Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1],
							Thski[chot-1][sbhot-1][sestagio-1][estagio-1],
							Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1],
							Fharr[estagio-1][chot-1][sbhot-1]/100,
							Fcarr[estagio-1][ccold-1][sbcold-1]/100])

	atualizar_matriz_abaixo(linha_interface_abaixo)

	return linha_interface_abaixo, True

def remover_trocador_abaixo(dlg, vetor, indice, linha_interface_abaixo):
	chot = vetor[0]
	ccold = vetor[1]
	sbhot = vetor[2]
	sbcold = vetor[3]
	sestagio = vetor[4]
	estagio = vetor[5]

	Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0

	calcular_superestrutura_abaixo("remover", chot, ccold, sbhot, sbcold, sestagio, estagio)

	linha_interface_abaixo.pop(indice)
	atualizar_matriz_abaixo(linha_interface_abaixo)

def atualizar_matriz_abaixo(matriz):
	for trocador in matriz:
		trocador[7] = Thskf[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[8] = Tcskf[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]
		trocador[9] = Thski[trocador[0]-1][trocador[2]-1][trocador[4]-1][trocador[5]-1]
		trocador[10] = Tcski[trocador[1]-1][trocador[3]-1][trocador[4]-1][trocador[5]-1]

def matrizes(acao, chot, ccold, sbhot, sbcold, sestagio, estagio):
	global quentes_usadas, frias_usadas, quentesxfrias, friasxquentes, subq_usadas, subf_usadas, subestagios

	def verificar(variavel, matriz):
		if variavel not in matriz:
			matriz.append(variavel)
			matriz.sort()

	if acao == "inserir":
		verificar(chot-1, quentes_usadas)
		verificar(ccold-1, frias_usadas)
		verificar(sbhot-1, subq_usadas[chot-1])
		verificar(sbcold-1, subf_usadas[ccold-1])
		verificar(ccold-1, quentesxfrias[chot-1])
		verificar(chot-1, friasxquentes[ccold-1])
		verificar(sestagio-1, subestagios)

	else:
		quentes_usadas = []
		frias_usadas = []
		subq_usadas = []
		subf_usadas = []
		quentesxfrias = []
		friasxquentes = []
		subestagios = []

		for i in range(nhot):
			subq_usadas.append([])
			quentesxfrias.append([])
		for j in range(ncold):
			subf_usadas.append([])
			friasxquentes.append([])

		for trocador in linha_interface_abaixo:
			verificar(trocador[0]-1, quentes_usadas)
			verificar(trocador[1]-1, frias_usadas)
			verificar(trocador[2]-1, subq_usadas[trocador[0]-1])
			verificar(trocador[3]-1, subf_usadas[trocador[1]-1])
			verificar(trocador[1]-1, quentesxfrias[trocador[0]-1])
			verificar(trocador[0]-1, friasxquentes[trocador[1]-1])
			verificar(trocador[4]-1, subestagios)

		for i in range(nhot):
			if i not in quentes_usadas:
				for si in range(ncold):
					temperatura_atual_quente_abaixo[i][si] = Th0[i]
				temperatura_atual_quente_mesclada_abaixo[i] = Th0[i]
			else:
				for si in range(ncold):
					if si not in subq_usadas[i]:
						temperatura_atual_quente_abaixo[i][si] = Th0[i]
		for j in range(ncold):
			if j not in frias_usadas:
				for sj in range(nhot):
					temperatura_atual_fria_abaixo[j][sj] = Tcf[j]
				temperatura_atual_fria_mesclada_abaixo[j] = Tcf[j]
			else:
				for sj in range(nhot):
					if sj not in subf_usadas[j]:
						temperatura_atual_fria_abaixo[j][sj] = Tcf[j]

def adicionar_utilidade_abaixo(dlg, corrente):
	if calor_atual_quente_abaixo[corrente-1] == 0:
		mensagem_err("The duty of this stream has already been supplied")
		return
	utilidades_abaixo.append([corrente, calor_atual_quente_abaixo[corrente-1]])
	calor_sub_sem_utilidade[corrente-1] = calor_atual_quente_sub_abaixo[corrente-1][:]
	if dividida_quente_abaixo[corrente-1]:
		for si in range(quantidade_quente_abaixo[corrente-1]):
			temperatura_atual_quente_abaixo[corrente-1][si] = Thf[corrente-1]
			calor_atual_quente_sub_abaixo[corrente-1][si] = 0.0
	temp_misturador_abaixo[corrente-1] = temperatura_atual_quente_mesclada_abaixo[corrente-1]
	temperatura_atual_quente_mesclada_abaixo[corrente-1] = Thf[corrente-1]
	calor_atual_quente_abaixo[corrente-1] = 0.0
	fechar_corrente_abaixo[corrente-1] = True
	return utilidades_abaixo

def remover_utilidade_abaixo(corrente, indice_remover, utilidades_abaixo):
	if dividida_quente_abaixo[corrente-1]:
		for si in range(quantidade_quente_abaixo[corrente-1]):
			calor_atual_quente_sub_abaixo[corrente-1][si] = calor_sub_sem_utilidade[corrente-1][si]
			temperatura_atual_quente_abaixo[corrente-1][si] = calor_atual_quente_sub_abaixo[corrente-1][si]/(CPh[corrente-1]*Fharr[0][corrente-1][si]/100) + Thf[corrente-1]
	calor_atual_quente_abaixo[corrente-1] = utilidades_abaixo[indice_remover][1]
	temperatura_atual_quente_mesclada_abaixo[corrente-1] = calor_atual_quente_abaixo[corrente-1] / CPh[corrente-1] + Thf[corrente-1]
	utilidades_abaixo.pop(indice_remover)
	fechar_corrente_abaixo[corrente-1] = False

def caixa_de_temperatura_abaixo(dlg, sk):
	chot = int(dlg.TempLoadBelow.comboBox.currentText())
	ccold = int(dlg.TempLoadBelow.comboBox_2.currentText())
	sbhot = int(dlg.TempLoadBelow.comboBox_3.currentText())
	sbcold = int(dlg.TempLoadBelow.comboBox_4.currentText())
	estagio = 1
	sestagio = sk + 1

	if dlg.TempLoadBelow.radioButton_2.isChecked():                     #Inlet Hot Temperature
		outlethot = float(dlg.TempLoadBelow.lineEdit_2.text().replace(",", "."))
		q = round(-CPh[chot-1] * (outlethot - Thski[chot-1][sbhot-1][sestagio-1][estagio-1]), 2)
	if dlg.TempLoadBelow.radioButton.isChecked():
		inletcold = float(dlg.TempLoadBelow.lineEdit.text().replace(",", "."))
		q = round(-CPc[ccold-1] * (inletcold - Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1]), 2)

	if ((Qtotalh0[chot-1][sbhot-1][estagio-1]) > (Qtotalc0[ccold-1][sbcold-1][estagio-1])):
		Qmax = Qtotalc0[ccold-1][sbcold-1][estagio-1]
	else:
		Qmax = Qtotalh0[chot-1][sbhot-1][estagio-1]

	if q > Qmax:
		mensagem_err("The calculated heat is greater than the available heat.")
		return
	if q < 0:
		mensagem_err("The calculated heat is negative.")
		return
	if q == 0:
		mensagem_err("The calculated heat is equals 0.")
		return

	dlg.lineEdit_25.setText(str(float('{:.1f}'.format(q))))
	dlg.radioButton_17.setChecked(True)
	dlg.comboBox_35.setCurrentText(str(dlg.TempLoadBelow.comboBox.currentText()))  #hot strem
	dlg.comboBox_36.setCurrentText(str(dlg.TempLoadBelow.comboBox_2.currentText()))  #cold stream
	dlg.comboBox_53.setCurrentText(str(dlg.TempLoadBelow.comboBox_3.currentText())) #si
	dlg.comboBox_54.setCurrentText(str(dlg.TempLoadBelow.comboBox_4.currentText())) #sj
	dlg.TempLoadBelow.close()

def testar_correntes_abaixo(dlg, primeira=False):
	nhotc = 0
	ncoldc = 0
	somaCPh = 0
	somaCPc = 0

	for quente in range(nhot):
		if Th0[quente] == pinchq:
			somaCPh += CPh[quente]
			if CPh[quente] != 0:
				if dividida_quente_abaixo[quente]:
					nhotc += quantidade_quente_abaixo[quente]
				else:
					nhotc += 1

	for fria in range(ncold):
		if Tcf[fria] == pinchf:
			somaCPc += CPc[fria]
			if CPc[fria] != 0:
				if dividida_fria_abaixo[fria]:
					ncoldc += quantidade_fria_abaixo[fria]
				else:
					ncoldc += 1

	if somaCPc > somaCPh:
		dlg.label_25.setStyleSheet("QLabel {color: red}")
	else:
		dlg.label_25.setStyleSheet("QLabel {color: green}")

	if ncoldc > nhotc:
		dlg.label_22.setStyleSheet("QLabel {color: red}")
		if not primeira:
			mensagem_err("With this Split, you went against the Pinch Recomendations", titulo="Be Carreful")
	else:
		dlg.label_22.setStyleSheet("QLabel {color: green}")

	if somaCPh >= somaCPc and ncoldc <= nhotc:
		dlg.label_27.setText("Respected")
		dlg.label_27.setStyleSheet("QLabel {color: green}")
	else:
		dlg.label_27.setText("Not Respected")
		dlg.label_27.setStyleSheet("QLabel {color: red}")

def inserir_todos_abaixo(matriz, coloca=True, atualiza=False, novo=True):
	if len(matriz) == 0:
		for i in range(nhot):
			for si in range(ncold):
				temperatura_atual_quente_abaixo[i][si] = Th0[i]
			temperatura_atual_quente_mesclada_abaixo[i] = Th0[i]
		for j in range(ncold):
			for sj in range(nhot):
				temperatura_atual_fria_abaixo[j][sj] = Tcf[j]
			temperatura_atual_fria_mesclada_abaixo[j] = Tcf[j]

	for trocador in matriz:
		chot = trocador[0]
		ccold = trocador[1]
		sbhot = trocador[2]
		sbcold = trocador[3]
		sestagio = trocador[4]
		estagio = trocador[5]
		Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = trocador[6]

		matrizes("inserir", chot, ccold, sbhot, sbcold, sestagio, estagio)

		calcular_superestrutura_abaixo("inserir", chot, ccold, sbhot, sbcold, sestagio, estagio)

		if coloca:
			linha_interface_abaixo.append([chot,
									ccold,
									sbhot,
									sbcold,
									sestagio,
									estagio,
									Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1],
									Thskf[chot-1][sbhot-1][sestagio-1][estagio-1],
									Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1],
									Thski[chot-1][sbhot-1][sestagio-1][estagio-1],
									Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1],
									Fharr[estagio-1][chot-1][sbhot-1]/100,
									Fcarr[estagio-1][ccold-1][sbcold-1]/100])

		if atualiza:
			if matriz.index(trocador) != len(matriz)-1 or not novo:
				linha_interface_abaixo[sestagio-1] = [chot,
											   ccold,
											   sbhot,
											   sbcold,
											   sestagio,
											   estagio,
											   Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1],
											   Thskf[chot-1][sbhot-1][sestagio-1][estagio-1],
											   Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1],
											   Thski[chot-1][sbhot-1][sestagio-1][estagio-1],
											   Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1],
											   Fharr[estagio-1][chot-1][sbhot-1]/100,
											   Fcarr[estagio-1][ccold-1][sbcold-1]/100]
			elif novo:
				linha_interface_abaixo.append([chot,
										ccold,
										sbhot,
										sbcold,
										sestagio,
										estagio,
										Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1],
										Thskf[chot-1][sbhot-1][sestagio-1][estagio-1],
										Tcskf[ccold-1][sbcold-1][sestagio-1][estagio-1],
										Thski[chot-1][sbhot-1][sestagio-1][estagio-1],
										Tcski[ccold-1][sbcold-1][sestagio-1][estagio-1],
										Fharr[estagio-1][chot-1][sbhot-1]/100,
										Fcarr[estagio-1][ccold-1][sbcold-1]/100])

	atualizar_matriz_abaixo(linha_interface_abaixo)

	return linha_interface_abaixo

def remover_todos_abaixo(ate=0, temps=False):
	for i in range(len(linha_interface_abaixo)-1, ate-1, -1):
		chot = linha_interface_abaixo[i][0]
		ccold = linha_interface_abaixo[i][1]
		sbhot = linha_interface_abaixo[i][2]
		sbcold = linha_interface_abaixo[i][3]
		sestagio = linha_interface_abaixo[i][4]
		estagio = linha_interface_abaixo[i][5]
		calor = linha_interface_abaixo[i][6]

		Qtotalh0[chot-1][sbhot-1][estagio-1] += calor
		Qtotalc0[ccold-1][sbcold-1][estagio-1] += calor
		calor_atual_quente_abaixo[chot-1] += calor
		calor_atual_frio_abaixo[ccold-1] += calor
		calor_atual_quente_sub_abaixo[chot-1][sbhot-1] += calor
		calor_atual_frio_sub_abaixo[ccold-1][sbcold-1] += calor

		Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0

		linha_interface_abaixo.pop(-1)

	matrizes("remover", 0, 0, 0, 0, 0, 0)

	if temps:
		for trocador in linha_interface_abaixo:
			calcular_superestrutura_abaixo("nada", trocador[0], trocador[1], trocador[2], trocador[3], trocador[4], trocador[5])
		atualizar_matriz_abaixo(linha_interface_abaixo)

def preparar_corrente_abaixo(corrente, indice=1):
	trocadores = []
	for i in range(len(linha_interface_abaixo)-1, -1, -1):
		if linha_interface_abaixo[i][indice] == corrente:
			chot = linha_interface_abaixo[i][0]
			ccold = linha_interface_abaixo[i][1]
			sbhot = linha_interface_abaixo[i][2]
			sbcold = linha_interface_abaixo[i][3]
			sestagio = linha_interface_abaixo[i][4]
			estagio = linha_interface_abaixo[i][5]
			calor = linha_interface_abaixo[i][6]
			trocadores.append([chot, ccold, sbhot, sbcold, sestagio, estagio, calor, i])

			Q[chot-1][sbhot-1][ccold-1][sbcold-1][sestagio-1][estagio-1] = 0
			Qtotalh0[chot-1][sbhot-1][estagio-1] += calor
			Qtotalc0[ccold-1][sbcold-1][estagio-1] += calor
			calor_atual_quente_abaixo[chot-1] += calor
			calor_atual_frio_abaixo[ccold-1] += calor
			calor_atual_quente_sub_abaixo[chot-1][sbhot-1] += calor
			calor_atual_frio_sub_abaixo[ccold-1][sbcold-1] += calor
	return trocadores

def calcular_fracoes_abaixo(corrente, calores, tipo):
	fracoes = []
	for i in range(len(calores)):
		if tipo == "quente":
			fracoes.append(calores[i]/Qtotalh01[corrente-1])
		elif tipo == "fria":
			fracoes.append(calores[i]/Qtotalc01[corrente-1])

	return fracoes
