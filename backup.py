import numpy as np

nhot = 4
ncold = 5


#BASEADO NA MATRIZ DOS TROCADORES ARMAZENADO, CRIA UMA MATRIZ PRA LIDAR CERTO COM AS CORRENTES
# for trocador in matriz:
# 	matriz_nova.append([trocador[0], trocador[1] + nhot])

#IDENTIFICAR LAÇOS
def identificar_laco(matriz_nova, nivel):
	incidencia = []

	for i in range(nhot + ncold):
		incidencia.append([])

	#CRIAR MATRIZ INCIDENCIA
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

	print(np.matrix(incidencia))
	trocadores_laco = []
	for trocador in range(len(matriz_nova)):
		soma_quente = [0] * (nhot)
		soma_fria = [0] * (ncold)
		corrente_quente, corrente_fria = 0, nhot
		trocadores_laco.append(trocador+1)

		for corrente in range(len(incidencia)):
			if incidencia[corrente][trocador] == 1:
				soma_quente[corrente] += 1
				corrente_quente = corrente
			if incidencia[corrente][trocador] == -1:
				soma_fria[corrente - nhot] -= 1
				corrente_fria = corrente

		if nivel == 1:
			for trocador_comparar in range(trocador+1, len(matriz_nova)):
				ja_colocou = False
				if incidencia[corrente_quente][trocador_comparar] == 1:
					soma_quente[corrente_quente] += 1
					if not ja_colocou:
						trocadores_laco.append(trocador_comparar+1)
						ja_colocou = True
						print("colocou quente")
				if incidencia[corrente_fria][trocador_comparar] == -1:
					soma_fria[corrente_fria - nhot] -= 1
					if not ja_colocou:
						trocadores_laco.append(trocador_comparar+1)
						ja_colocou = True
						print("colocou fria")

				print("comparando", trocador+1, trocador_comparar+1)
				print(soma_quente)
				print(soma_fria)
				print()

				soma_teste = 0
				for i in range(len(soma_quente)):
					if soma_quente[i] == 2:
						soma_teste += 2
						if nivel == 1:
							soma_quente[i] = 1
				for j in range(len(soma_fria)):
					if soma_fria[j] == -2:
						soma_teste += 2
						if nivel == 1:
							soma_fria[j] = -1
				if soma_teste == nivel*4:
					print("laço de nivel", nivel, "entre os trocadores:")
					print(trocadores_laco)
					return
				else:
					trocadores_laco.pop(-1)
		else:
			for trocador_comparar in range(trocador+1, len(matriz_nova)):
				ja_colocou = False
				for corrente in range(len(incidencia)):
					if incidencia[corrente][trocador_comparar] == 1:
						soma_quente[corrente] += 1
					if incidencia[corrente - nhot][trocador_comparar] == -1:
						soma_fria[corrente - nhot] -= 1

				print("comparando", trocador+1, trocador_comparar+1)
				print(soma_quente)
				print(soma_fria)
				print()


				proximo = False
				if soma_quente[corrente_quente] > 2:
					soma_quente[corrente_quente] = 2
					proximo = True
				if soma_fria[corrente_fria - nhot] < -2:
					soma_fria[corrente_fria - nhot] = -2
					proximo = True


				if not proximo:
					soma_teste = 0
					ja_colocou = False
					for i in range(len(soma_quente)):
						if soma_quente[i] == 2:
							soma_teste += 2
							if not ja_colocou:
								trocadores_laco.append(trocador_comparar+1)
								ja_colocou = True
					for j in range(len(soma_fria)):
						if soma_fria[j] == -2:
							soma_teste += 2
							if not ja_colocou:
								trocadores_laco.append(trocador_comparar+1)
								ja_colocou = True
					if soma_teste == nivel*4:
						print("laço de nivel", nivel, "entre os trocadores:")
						print(trocadores_laco)
						return




matriz_nova1 = [[2, 5], [1, 5], [2, 5], [0, 5], [1, 4], [2, 4], [0,4], [0, 6], [1, 7], [2, 8], [3, 5]]
matriz_nova2 = [[2, 5], [1, 5], [0, 5], [1, 4], [2, 4], [0,4], [0, 6], [1, 7], [2, 8], [3, 5]]
matriz_nova3 = [[2, 5], [1, 5], [0, 5], [2, 4], [0, 4], [0, 6], [1, 7], [2, 8], [3, 5]]

# identificar_laco(matriz_nova1, 1)
# identificar_laco(matriz_nova2, 2)
identificar_laco(matriz_nova3, 2)







#oi
