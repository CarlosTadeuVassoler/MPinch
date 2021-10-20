while opcao != 6:
	linha()
	print('{:^42}'.format('MENU DE OPÇÕES'))
	linha()
	print('1 - Consultar correntes')
	print('2 - Dividir correntes')
	print('3 - Inserir trocador de calor')
	print('4 - Remover um trocador de calor')
	print('5 - Inserir utilidades')
	print('6 - Finalizar')
	linha()
	opcao = int(input('Qual opção você deseja? '))
	print()

	if opcao == 1:   #num vo faze função pq nao vai usa
		linha()
		print('CONSULTA DE CORRENTES')
		linha()
		print('Temperatura Entrada Quente')
		print(Thf)
		print('Temperatura Final Quente')
		print(Th0)
		print('Temperatura Entrada Fria')
		print(Tc0)
		print('Temperatura Final Fria')
		print(Tcf)
		print('Calor Disponível Quentes:')
		print(Qtotalh0)
		print('Calor Disponível Frias:')
		print(Qtotalc0)


	elif opcao == 2:
		divisao_de_correntes()

	elif opcao == 3:
		print(recriar_rede(matriz))

	elif opcao == 4:
		print(recriar_rede(matriz))
		print(remover_trocador(vetor))

	elif opcao == 5:
		adicionar_utilidade()
