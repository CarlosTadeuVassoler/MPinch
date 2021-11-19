def printar():
	dlg.tableWidget_3.clearContents()
	dlg.tableWidget_4.clearContents()

	if dlg.checkBox.isChecked():
		linha = 0
		linhas = 0
		for i in quantidade_quente:
			linhas += i
		dlg.tableWidget_3.setRowCount(linhas)
		for corrente in range(nhot):
			if dividida_quente[corrente]:
				for sub in range(quantidade_quente[corrente]):
					text = str(corrente+1) + "." + str(sub+1)
					dlg.tableWidget_3.setItem(linha, 0, QTableWidgetItem(text))
					dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente[corrente][sub])))))
					dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(Th0[corrente])))))
					dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente_sub[corrente][sub])))))
					linha += 1
			else:
				dlg.tableWidget_3.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_mesclada[corrente])))))
				dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(Th0[corrente])))))
				dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente[corrente])))))
				linha += 1
	else:
		dlg.tableWidget_3.setRowCount(nhot)
		for corrente in range(nhot):
			dlg.tableWidget_3.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
			dlg.tableWidget_3.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_quente_mesclada[corrente])))))
			dlg.tableWidget_3.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(Th0[corrente])))))
			dlg.tableWidget_3.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_quente[corrente])))))

	if dlg.checkBox_2.isChecked():
		linha = 0
		linhas = 0
		for i in quantidade_fria:
			linhas += i
		dlg.tableWidget_4.setRowCount(linhas)
		for corrente in range(ncold):
			if dividida_fria[corrente]:
				for sub in range(quantidade_fria[corrente]):
					text = str(corrente+1) + "." + str(sub+1)
					dlg.tableWidget_4.setItem(linha, 0, QTableWidgetItem(text))
					dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria[corrente][sub])))))
					dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(Tcf[corrente])))))
					dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio_sub[corrente][sub])))))
					linha += 1
			else:
				dlg.tableWidget_4.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_mesclada[corrente])))))
				dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem(str(float('{:.1f}'.format(Tcf[corrente])))))
				dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio[corrente])))))
				linha += 1
	else:
		dlg.tableWidget_4.setRowCount(ncold)
		for corrente in range(ncold):
			dlg.tableWidget_4.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
			dlg.tableWidget_4.setItem(corrente, 1, QTableWidgetItem(str(float('{:.1f}'.format(temperatura_atual_fria_mesclada[corrente])))))
			dlg.tableWidget_4.setItem(corrente, 2, QTableWidgetItem(str(float('{:.1f}'.format(Tcf[corrente])))))
			dlg.tableWidget_4.setItem(corrente, 3, QTableWidgetItem(str(float('{:.1f}'.format(calor_atual_frio[corrente])))))


	dlg.tableWidget_2.setRowCount(len(matriz_armazenada))
	if len(matriz_armazenada) > 0:
		for trocador in range(0, len(matriz_armazenada)):
			dlg.tableWidget_2.setItem(trocador, 0, QTableWidgetItem(str(matriz_armazenada[trocador][0]))) #chot
			dlg.tableWidget_2.setItem(trocador, 1, QTableWidgetItem(str(matriz_armazenada[trocador][1]))) #ccold
			dlg.tableWidget_2.setItem(trocador, 2, QTableWidgetItem(str(matriz_armazenada[trocador][2]))) #sbhot
			dlg.tableWidget_2.setItem(trocador, 3, QTableWidgetItem(str(matriz_armazenada[trocador][3]))) #sbcold
			dlg.tableWidget_2.setItem(trocador, 4, QTableWidgetItem(str(matriz_armazenada[trocador][4]))) #sk
			dlg.tableWidget_2.setItem(trocador, 5, QTableWidgetItem(str(matriz_armazenada[trocador][5]))) #k
			dlg.tableWidget_2.setItem(trocador, 6, QTableWidgetItem(str(float('{:.1f}'.format(matriz_armazenada[trocador][6]))))) # calor trocado
			dlg.tableWidget_2.setItem(trocador, 7, QTableWidgetItem(str(float('{:.1f}'.format(matriz_armazenada[trocador][7]))))) #Thin
			dlg.tableWidget_2.setItem(trocador, 8, QTableWidgetItem(str(float('{:.1f}'.format(matriz_armazenada[trocador][8]))))) #Tcout
			dlg.tableWidget_2.setItem(trocador, 9, QTableWidgetItem(str(matriz_armazenada[trocador][9]))) #fração hot
			dlg.tableWidget_2.setItem(trocador, 10, QTableWidgetItem(str(matriz_armazenada[trocador][10]))) #fraçao cold
		dlg.lineEdit_5.setText(str("0"))

	if len(utilidades) > 0:
		dlg.tableWidget_2.setRowCount(len(matriz_armazenada) + len(utilidades))
		for utilidade in range(0, len(utilidades)):
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 0, QTableWidgetItem(str("Hot Utility")))
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 1, QTableWidgetItem(str(utilidades[utilidade][0])))
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 6, QTableWidgetItem(str(float('{:.1f}'.format(utilidades[utilidade][1])))))
