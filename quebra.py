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

	# print(incidencia)
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
				if incidencia[corrente_fria][trocador_comparar] == -1:
					soma_fria[corrente_fria - nhot] -= 1

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
					trocadores_laco = [trocador+1, trocador_comparar+1]
					print("laço de nivel", nivel, "entre os trocadores:")
					print(trocadores_laco)
					return
				else:
					trocadores_laco.pop(-1)
		else:
			contador_quente, contador_frio = 1, 1
			for trocador_comparar in range(trocador+1, 6):
				ja_colocou = False
				proximo = False
				print(contador_quente)
				print(contador_frio)

				for corrente in range(len(incidencia)):
					if incidencia[corrente][trocador_comparar] == 1 and contador_quente != nivel:
						soma_quente[corrente] += 1
						if soma_quente[corrente] > 2:
							soma_quente[corrente] = 2
							proximo = True
							for i in range(len(incidencia)):
								if incidencia[i][trocador_comparar] == -1:
									soma_fria[i - nhot] += 1
						elif soma_quente[corrente] == 2 and not ja_colocou:
							trocadores_laco.append(trocador_comparar+1)
							ja_colocou = True
							contador_quente += 1
					if incidencia[corrente][trocador_comparar] == -1 and contador_frio != nivel:
						soma_fria[corrente - nhot] -= 1
						if soma_fria[corrente - nhot] < -2:
							soma_fria[corrente - nhot] = -2
							proximo = True
							for i in range(len(incidencia)):
								if incidencia[i][trocador_comparar] == 1:
									soma_quente[i] -= 1
						elif soma_fria[corrente - nhot] and not ja_colocou:
							trocadores_laco.append(trocador_comparar+1)
							ja_colocou = True
							contador_frio += 1


				# print(np.matrix(incidencia))
				print("comparando", trocador+1, trocador_comparar+1)
				print(soma_quente)
				print(soma_fria)
				print()

				if not proximo:
					soma_teste = 0
					ja_colocou = False
					# trocadores_laco.append(trocador_comparar+1)
					for i in range(len(soma_quente)):
						if soma_quente[i] == 2:
							soma_teste += 2
							# if not ja_colocou:
							# 	trocadores_laco.append(trocador_comparar+1)
							# 	ja_colocou = True
					for j in range(len(soma_fria)):
						if soma_fria[j] == -2:
							soma_teste += 2
							# if not ja_colocou:
							# 	trocadores_laco.append(trocador_comparar+1)
							# 	ja_colocou = True
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
