def recriar_rede(matriz_inputs, matriz_armazenada):
	matriz_armazenada = []
	linha_interface = []
	for i in range (nhot):
		for si in range (ncold):
			for sk in range (nsk):
				for k in range (nstages):
					Thski[i][si][sk][k] = Thf[i]
					Thskf[i][si][sk][k] = Thf[i]
		for k in range (nstages):
			Thki[i][k] = Thf[i]
			Thkf[i][k] = Thf[i]

	for j in range (ncold):
		for sj in range (nhot):
			for sk in range(nsk-1, -1, -1):
				for k in range(nstages-1, -1, -1):
					Tcski[j][sj][sk][k] = Tc0[j]
					Tcskf[j][sj][sk][k] = Tc0[j]
		for k in range (nstages-1, -1, -1):
			Tcki[j][k] = Tc0[j]
			Tckf[j][k] = Tc0[j]

	for quente in range(nhot):
		temperatura_atual_quente[quente] = pinchq

	for fria in range(ncold):
		temperatura_atual_fria[fria] = pinchf


	for trocador in matriz_inputs:
		matriz_armazenada = inserir_trocador(trocador)
