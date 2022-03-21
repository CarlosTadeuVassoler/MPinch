import numpy as np

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

def achar_trocador(incidencia, matriz_trocadores, correntee, excecao, comecar, nivel, n, trocador_inicial):
	i = incidencia[correntee][excecao]
	for correntes in range(len(incidencia)):
		if incidencia[correntes][excecao] == -i:
			c = correntes
	if n == 0:
		if incidencia[c][comecar] == -i and comecar != excecao:
			t = comecar
			return c, t
	elif n == nivel*2 - 1:
		if incidencia[c][trocador_inicial] == -i and trocador_inicial != excecao:
			t = trocador_inicial
			return c, t
	else:
		for trocadores in range(len(matriz_trocadores)):
			if incidencia[c][trocadores] == -i and trocadores != excecao:
				t = trocadores
				return c, t
	return "o", "o"

def lacos(incidencia, matriz_trocadores, nivel):
	for trocadores in range(len(matriz_trocadores)):
		trocador_inicial = trocadores
		trocador = trocadores
		for c in range(len(incidencia)):
			if incidencia[c][trocadores] == 1:
				corrente_inicial = c
				corrente = c
		for comecar in range(len(matriz_trocadores)):
			corrente = corrente_inicial
			trocador = trocador_inicial
			trocadores_laco = []
			tenta_dnv = True
			for n in range(nivel*2):
				if tenta_dnv:
					corrente, trocador = achar_trocador(incidencia, matriz_trocadores, corrente, trocador, comecar, nivel, n, trocador_inicial)
					if corrente == "o":
						tenta_dnv = False
					else:
						trocadores_laco.append(trocador+1)
						if corrente == corrente_inicial and trocador == trocador_inicial:
							print("laço entre os trocadores:")
							print(trocadores_laco)
							print()
							return

matriz_nova1 = [[2, 5], [1, 5], [2, 5], [0, 5], [1, 4], [2, 4], [0, 4], [0, 6], [1, 7], [2, 8], [3, 5]]
matriz_nova2 = [[2, 5], [1, 5], [0, 5], [1, 4], [2, 4], [0, 4], [0, 6], [1, 7], [2, 8], [3, 5]]
matriz_nova3 = [[2, 5], [1, 5], [0, 5], [2, 4], [0, 4], [0, 6], [1, 7], [2, 8], [3, 5]]
matriz_nova4 = [[0, 6], [2, 5], [1, 5], [0, 5], [2, 4], [0, 4], [1, 7], [2, 8], [3, 5]]
laco3_certo = [[1, 8], [5, 9], [4, 7], [4, 8], [5, 8], [0, 7], [1, 10], [2,  10], [6, 9], [6, 10], [0, 11], [3, 11]]

# nhot = 4
# ncold = 5

# a = criar_incidencia(matriz_nova1)
# print(np.matrix(a))
# lacos(a, matriz_nova1, 1)

# b = criar_incidencia(matriz_nova2)
# print(np.matrix(b))
# lacos(b, matriz_nova2, 2)
#
# c = criar_incidencia(matriz_nova3)
# print(np.matrix(c))
# lacos(c, matriz_nova3, 2)
#
# d = criar_incidencia(matriz_nova4)
# print(np.matrix(d))
# lacos(d, matriz_nova4, 2)


# nhot = 7
# ncold = 5
# e = criar_incidencia(laco3_certo)
# print(np.matrix(e))
# lacos(e, laco3_certo, 3)
