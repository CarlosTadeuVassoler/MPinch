import numpy as np

nhot = 4
ncold = 5



def criar_incidencia(matriz_nova):
	incidencia = []
	for i in range(nhot + ncold):
		incidencia.append([])

	for i in range(nhot):
		for trocador in matriz_nova:
			if trocador[0] == i:
				incidencia[i].append(1)
			else:
				incidencia[i].append(0)

	for j in range(nhot, ncold + nhot):
		for trocador in matriz_nova:
			if trocador[1] == j:
				incidencia[j].append(-1)
			else:
				incidencia[j].append(0)

	return incidencia

def achar_trocador(incidencia, matriz_trocadores, correntee, excecao, pular, nivel):
	i = incidencia[correntee][excecao]
	# print("recebe corrente", correntee+1, "no trocador", excecao+1)
	for correntes in range(len(incidencia)):
		if incidencia[correntes][excecao] == -i:
			c = correntes
			# print("acha a outra corrente", correntes+1)
	for trocadores in range(len(matriz_trocadores)):
		if incidencia[c][trocadores] == -i and trocadores != excecao:
			t = trocadores
			# print("que também esta no trocador", trocadores+1)
			# print()
			return c, t

def lacos(incidencia, matriz_trocadores, nivel):
	for trocadores in range(len(matriz_trocadores)):
		trocador_inicial = trocadores
		trocador = trocadores
		for c in range(len(incidencia)):
			if incidencia[c][trocadores] == 1:
				corrente_inicial = c
				corrente = c
		trocadores_laco = []
		for n in range(nivel*2):
			try:
				corrente, trocador = achar_trocador(incidencia, matriz_trocadores, corrente, trocador, None, nivel)
				trocadores_laco.append(trocador+1)
			except:
				break
		if corrente == corrente_inicial and trocador == trocador_inicial:
			print("laço entre os trocadores:")
			print(trocadores_laco)
			print()
			return
		else:
			# print("nao achou, proximo")
			# print(np.matrix(incidencia))
			# print()
			pass


matriz_nova1 = [[2, 5], [1, 5], [2, 5], [0, 5], [1, 4], [2, 4], [0,4], [0, 6], [1, 7], [2, 8], [3, 5]]
matriz_nova2 = [[2, 5], [1, 5], [0, 5], [1, 4], [2, 4], [0,4], [0, 6], [1, 7], [2, 8], [3, 5]]
matriz_nova3 = [[2, 5], [1, 5], [0, 5], [2, 4], [0, 4], [0, 6], [1, 7], [2, 8], [3, 5]]

a = criar_incidencia(matriz_nova1)
print(np.matrix(a))
lacos(a, matriz_nova1, 1)

b = criar_incidencia(matriz_nova2)
print(np.matrix(b))
lacos(b, matriz_nova2, 2)
#
c = criar_incidencia(matriz_nova3)
print(np.matrix(c))
lacos(c, matriz_nova3, 2)










#oi
