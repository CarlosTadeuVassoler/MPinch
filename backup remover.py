def removertrocadoracima():
	global nlinhas, correntestrocador, ntrocadores, Qtabela0, Qhot0, Qcold0, Tcout0, Thin0, opcao, alternativa,chot,ccold
	opcao = 4
	if dlg.tableWidget_2.rowCount() == 0:
	    QMessageBox.about(dlg,"Error!","You do not have any heat exchangers in your network to remove.")
	    return

	elif dlg.tableWidget_2.rowCount() > 0:
		if bool(dlg.tableWidget_2.selectedIndexes()) == False:
			QMessageBox.about(dlg,"Error!","Select a heat exchanger to remove.")
			return
	print("correntes inicial", correntestrocador)
	ntrocadores[int(float(dlg.comboBox_2.currentText()))-1]=ntrocadores[int(float(dlg.comboBox_2.currentText()))-1]-1
	ntrocadores[int(float(dlg.comboBox_5.currentText()))+nhot-1]=ntrocadores[int(float(dlg.comboBox_5.currentText()))+nhot-1]-1

	Thin,Tcout,Qtabela,Fharr1,Fcarr1,Qhot,Qcold,chot,ccold=acima(correntesncorrigidas,correntestrocador,ntrocadores,pinchq,pinchf,n,nhot,ncold,dlg,dTmin,chot,ccold,nlinhas,opcao,Qtabela0)
	#ntrocadores=ntrocadores+1
	chot1 = int(float(dlg.comboBox_2.currentText()))
	ccold1 = int(float(dlg.comboBox_5.currentText()))
	correntestrocador[chot1-1][1]=Thin
	correntestrocador[ccold1-1+nhot][0]=Tcout

	dlg.tableWidget_3.setItem(chot-1, 1, QTableWidgetItem(str(Thin)))
	dlg.tableWidget_4.setItem(ccold-1, 1, QTableWidgetItem(str(Tcout)))
	dlg.tableWidget_3.setItem(chot-1, 3, QTableWidgetItem(str(Qhot))) #heat duty hot
	dlg.tableWidget_4.setItem(ccold-1, 3, QTableWidgetItem(str(Qcold)))   #heat duty cold

	Qtabela0=Qtabela
	Qhot0=Qhot
	Qcold0=Qcold
	Tcout0=Tcout
	Thin0=Thin


	nlinhas=nlinhas-1

	checaresgotadosacima()

	if dlg.tableWidget_2.rowCount() > 0:
	    dlg.tableWidget_2.removeRow(dlg.tableWidget_2.currentRow())

def adicionartrocadoracima():
	global nlinhas, correntestrocador, ntrocadores, Qtabela0,opcao
	opcao = 3
	print("correntes inicial", correntestrocador)

	Thin,Tcout,Qtabela,Fharr1,Fcarr1,Qhot,Qcold=acima(correntesncorrigidas,correntestrocador,ntrocadores,pinchq,pinchf,n,nhot,ncold,dlg,dTmin,chot,ccold,nlinhas,opcao,Qtabela0)

	inserir_teste()

	ntrocadores[int(float(dlg.comboBox_2.currentText()))-1]=ntrocadores[int(float(dlg.comboBox_2.currentText()))-1]+1
	ntrocadores[int(float(dlg.comboBox_5.currentText()))+nhot-1]=ntrocadores[int(float(dlg.comboBox_5.currentText()))+nhot-1]+1
	chot1 = int(float(dlg.comboBox_2.currentText()))
	ccold1 = int(float(dlg.comboBox_5.currentText()))
	correntestrocador[chot1-1][1]=Thin
	correntestrocador[ccold1-1+nhot][0]=Tcout
	dlg.tableWidget_3.setItem(float(dlg.comboBox_2.currentText())-1, 1, QTableWidgetItem(str(Thin))) #só da certo se tiver tudo quente depois tudo frio
	dlg.tableWidget_4.setItem(float(dlg.comboBox_5.currentText())-1, 1, QTableWidgetItem(str(Tcout)))
	dlg.tableWidget_3.setItem(float(dlg.comboBox_2.currentText())-1, 3, QTableWidgetItem(str(Qhot)))  #heat duty hot
	dlg.tableWidget_4.setItem(float(dlg.comboBox_2.currentText())-1, 3, QTableWidgetItem(str(Qcold)))   #heat duty cold
	dlg.tableWidget_2.setRowCount(nlinhas)
	printar()
	dlg.lineEdit_5.setText(str("0"))
	dlg.tableWidget_2.setItem(nlinhas-1,7,QTableWidgetItem(str((float(dlg.tableWidget_3.item(float(dlg.comboBox_2.currentText())-1,1).text())))))
	dlg.tableWidget_2.setItem(nlinhas-1,8,QTableWidgetItem(str((float(dlg.tableWidget_4.item(float(dlg.comboBox_5.currentText())-1,1).text())))))
	nlinhas=nlinhas+1
	Qtabela0=Qtabela



	checaresgotadosacima()
