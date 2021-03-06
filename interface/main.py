import sys #usa pra fazer new file
import os #usa pra fazer new file

import xlrd #lidar com excel
import xlsxwriter #criar excel
from tkinter import Tk #usa pra nao mostrar a aba tk
from tkinter.filedialog import askopenfilename #abrir arquivo (excel)
from tkinter.filedialog import asksaveasfilename #salvar imagem

from PyQt5 import uic, QtGui, QtWidgets #ler interface e widgets de um jeito diferente
from PyQt5.QtWidgets import * #widgets
from PyQt5.QtCore import * #alinhamentos
from PyQt5.QtGui import * #pixmaps

import funchpinchcerto as fp2 #pinch victor
from funcPPinch import pontopinch #pinch meninos

from superestrutura_acima import * #superestrutura acima
from superestrutura_abaixo import * #superestrutura abaixo
from superestrutura_completa import * #superestrutura ambas (evolucao)

from PIL import Image #usa pra manipular/salvar imagens
import turtle #usa pra criar os desenhos de rede

import numpy as np #facilita a lidar com numeros
from converter_unidades import * #nao ta usando ainda

from custos import * #calculos/graficos da aba dtmin optimization
from graficos import * #graficos da aba diagrams comparison
from exportaa import export #coisas savefile

import time



#matrizes que armazenam os trocadores inseridos
matriz_armazenada = [] #acima
matriz_trocadores_abaixo = [] #abaixo
matriz_evolucao = [] #ambas (evolucao)
subestagio_trocador = 1 #usada pra determinar qual subestagio vai inserir o trocador acima
subestagio_trocador_abaixo = 1 #usada pra determinar qual subestagio vai inserir o trocador abaixo

#quando nao sao especificadas as utilidades, armazena nessas
utilidades = [] #acima
utilidades_abaixo = [] #abaixo

#variaveis de corrente
correntes = [] #após o pinch, armazena correntes + utilidades quando especificadas
correntes_util = [] #armazena somente as utilidades
correntes_quentes = [] #utilizada para desenhar correntes quentes
correntes_frias = [] #utilizada para desenhar correntes frias
corrente_quente_presente_acima = [] #ve se a corrente ta presente na subrede
corrente_quente_presente_abaixo = [] #ve se a corrente ta presente na subrede
corrente_fria_presente_acima = [] #ve se a corrente ta presente na subrede
corrente_fria_presente_abaixo = [] #ve se a corrente ta presente na subrede
e_utilidade = [] #diferencia corrente de utilidade na matriz "correntes"
e_utilidade_quente = [] #usa pra preencher combobox e pra criar desenho
e_utilidade_fria = [] #usa pra preencher combobox e pra criar desenho
n = nhot = ncold = n_util = 0 #numero de correntes fornecidas
divisoes = [] #salva as divisoes feitas nas subredes pra quando for criar a rede completa

#remover_trocadores
perguntar = True #continuar perguntando se quer remover todos os trocadores anteriores
remover_todos = False #se perguntar = False, ele armazena a decisão do usuário sobre remover

#divisao de utilidades
dividir_padrao = False #guarda se quer dividir a utilidade sempre
nao_perguntar = False #dont ask again utilidade
primeira_util = True
primeira_util_fria = True

primeira_evolucao = True
zoom_atual = 1
zoom_atual_abaixo = 1


#streams
def openfile_teste(pergunta=True, nome=None):
	global n, nhot, ncold, correntes, arquivo

	#le o excel
	dlg.tableWidget.blockSignals(True)
	Tk().withdraw()
	if pergunta:
		filename = askopenfilename()
		workbook = xlrd.open_workbook(filename)
		arquivo = filename
	else:
		workbook = xlrd.open_workbook(nome)
		arquivo = nome
		# workbook = xlrd.open_workbook("25 correntes.xls")
		# arquivo = "25 correntes.xls"
		# workbook = xlrd.open_workbook("40 correntes - 3 dtmin.xls")
		# arquivo = "40 correntes - 3 dtmin.xls"
		# workbook = xlrd.open_workbook("50 correntes.xls")
		# arquivo = "50 correntes.xls"
		# workbook = xlrd.open_workbook("4 correntes - 10 dtmin.xls")
		# arquivo = "4 correntes - 10 dtmin.xls"

	worksheet = workbook.sheet_by_index(0)
	k=0
	while k != -1:
		try:
			if (worksheet.cell(k+1, 0).value) != '':
				k=k+1
				n=n+1
		except IndexError:
			break

	#armazena as correntes e calcula a quantidade de quentes e frias
	correntes = []
	dlg.tableWidget.setRowCount(n)
	for i in range(n):
		dados_da_corrente = []
		for j in range(3):
			dados_da_corrente.append(worksheet.cell(i+1, j+1).value)
		if dados_da_corrente[0] > dados_da_corrente[1]:
			dados_da_corrente.append("Hot")
			nhot += 1
		else:
			dados_da_corrente.append("Cold")
			ncold += 1
		try:
			dados_da_corrente.append(worksheet.cell(i+1, 5).value)
		except:
			dados_da_corrente.append(0.5)
		correntes.append(dados_da_corrente)
		e_utilidade.append(False)

	#printa as correntes pro usuário na tabela de streams
	for corrente in range(len(correntes)):
		for coluna in range(5):
			dlg.tableWidget.setItem(corrente, coluna, QTableWidgetItem(str(correntes[corrente][coluna])))


	dlg.tableWidget.blockSignals(False)
	for i in range(n):
		for j in range(5):
			item = dlg.tableWidget.item(i, j)
			item.setTextAlignment(Qt.AlignCenter)

def add_corrente() :
	global n, ncold, nhot, correntes

	if float(dlg.stream_supply.text().replace(",", ".")) < float(dlg.stream_target.text().replace(",", ".")):
		tipo = "Cold"
		ncold += 1
	elif float(dlg.stream_supply.text().replace(",", ".")) > float(dlg.stream_target.text().replace(",", ".")):
		tipo = "Hot"
		nhot += 1
	else:
		mensagem_erro("Please avoid Tin = Tout. \nIf the stream is isothermal, you may use 1 K difference and assign the heat capacity flowrate (w.Cp) with the latent heat flowrate value (w.L). \nFor more accuracy, use, for instance, 0.001 K difference and w.L/0.001 as heat capacity flowrate.")
		return

	n += 1
	dados_da_corrente = []
	if n == 1:
		dlg.sistema_unidades.setEnabled(False)
		dlg.temp_unidade.setEnabled(False)
		dlg.cp_unidade.setEnabled(False)
		dlg.pelicula_unidade.setEnabled(False)
		dlg.temp_unidade_util.setEnabled(False)
		dlg.pelicula_unidade_util.setEnabled(False)

	dados_da_corrente.append(float(dlg.stream_supply.text().replace(",",".")))
	dados_da_corrente.append(float(dlg.stream_target.text().replace(",", ".")))
	dados_da_corrente.append(float(dlg.stream_cp.text().replace(",", ".")))
	dados_da_corrente.append(tipo)
	dados_da_corrente.append(float(dlg.stream_pelicula.text().replace(",", ".")))

	dlg.tableWidget.blockSignals(True)
	dlg.tableWidget.setRowCount(n)
	dlg.tableWidget.setItem(n-1, 0, QTableWidgetItem(str(dados_da_corrente[0])))
	dlg.tableWidget.setItem(n-1, 1, QTableWidgetItem(str(dados_da_corrente[1])))
	dlg.tableWidget.setItem(n-1, 2, QTableWidgetItem(str(dados_da_corrente[2])))
	dlg.tableWidget.setItem(n-1, 3, QTableWidgetItem(dados_da_corrente[3]))
	dlg.tableWidget.setItem(n-1, 4, QTableWidgetItem(str(dados_da_corrente[4])))

	for i in range(5):
		item = dlg.tableWidget.item(n-1, i)
		item.setTextAlignment(Qt.AlignCenter)

	correntes.append(dados_da_corrente)
	e_utilidade.append(False)

	dlg.tableWidget.blockSignals(False)

def add_utilidade():
	global n, n_util, ncold, nhot, correntes_util

	if float(dlg.util_inlet.text().replace(",", ".")) < float(dlg.util_outlet.text().replace(",", ".")):
		tipo = "Cold"
	elif float(dlg.util_inlet.text().replace(",", ".")) > float(dlg.util_outlet.text().replace(",", ".")):
		tipo = "Hot"
	else:
		mensagem_erro("Please avoid Tin = Tout. \nIf the stream is isothermal, you may use 1 K difference and assign the heat capacity flowrate (w.Cp) with the latent heat flowrate value (w.L). \nFor more accuracy, use, for instance, 0.001 K difference and w.L/0.001 as heat capacity flowrate.")
		return

	if len(correntes_util) > 0:
		if correntes_util[0][3] == tipo:
			if tipo == "Hot":
				mensagem_erro("There's already a hot utility. You must input a cold one.")
			else:
				mensagem_erro("There's already a cold utility. You must input a hot one.")
			return

	dlg.donebutton.setEnabled(False)
	dlg.botao_addstream.setEnabled(False)
	dlg.remover_corrente.setEnabled(False)
	dados_da_corrente = []

	n_util += 1
	dados_da_corrente.append(float(dlg.util_inlet.text().replace(",", ".")))
	dados_da_corrente.append(float(dlg.util_outlet.text().replace(",", ".")))
	dados_da_corrente.append(1)
	dados_da_corrente.append(tipo)
	dados_da_corrente.append(float(dlg.util_pelicula.text().replace(",", ".")))

	if dlg.utilidade.text() == "":
		texto = "Utility " + str(n_util)
	else:
		texto = dlg.utilidade.text()

	dlg.tableWidget_5.blockSignals(True)
	dlg.tableWidget_5.setRowCount(n_util)
	dlg.tableWidget_5.setItem(n_util-1, 0, QTableWidgetItem(texto))
	dlg.tableWidget_5.setItem(n_util-1, 1, QTableWidgetItem(str(dados_da_corrente[0])))
	dlg.tableWidget_5.setItem(n_util-1, 2, QTableWidgetItem(str(dados_da_corrente[1])))
	dlg.tableWidget_5.setItem(n_util-1, 3, QTableWidgetItem(dados_da_corrente[3]))
	dlg.tableWidget_5.setItem(n_util-1, 4, QTableWidgetItem(str(dados_da_corrente[4])))

	for i in range(5):
		item = dlg.tableWidget_5.item(n_util-1, i)
		item.setTextAlignment(Qt.AlignCenter)

	correntes_util.append(dados_da_corrente)
	e_utilidade.append(True)

	dlg.tableWidget_5.blockSignals(False)
	if n_util == 2:
		dlg.botao_addutility.setEnabled(False)
		dlg.pinchbutton.setEnabled(True)

def editar_corrente(correntes, tip, tabela):
	global nhot, ncold

	try:
		linha = tabela.currentItem().row()
		coluna = tabela.currentItem().column()
		coluna_comp = coluna - tip
		dado = tabela.currentItem().text()
		dado_antigo = correntes[linha][3]

		if coluna == 3 and dado != dado_antigo:
			mensagem_erro("Not allowed to change this column. Change the temperatures instead.")
			tabela.setItem(linha, coluna, QTableWidgetItem(correntes[linha][coluna]))
			tabela.currentItem().setTextAlignment(Qt.AlignCenter)
			return
		elif coluna != 3:
			c = correntes[linha][:]
			c[coluna_comp] = float(dado.replace(",", "."))
			if c[0] == c[1]:
				mensagem_erro("Please avoid Tin = Tout. \nIf the stream is isothermal, you may use 1 K difference and assign the heat capacity flowrate (w.Cp) with the latent heat flowrate value (w.L). \nFor more accuracy, use, for instance, 0.001 K difference and w.L/0.001 as heat capacity flowrate.")
				tabela.setItem(linha, coluna, QTableWidgetItem(str(correntes[linha][coluna_comp])))
				tabela.currentItem().setTextAlignment(Qt.AlignCenter)
				return
			else:
				correntes[linha] = c[:]

		tipo = QTableWidgetItem(correntes[linha][3])
		if coluna_comp == 0 or coluna_comp == 1:
			if correntes[linha][0] > correntes[linha][1]:
				correntes[linha][3] = "Hot"
				tabela.setItem(linha, 3, tipo)
			elif correntes[linha][0] < correntes[linha][1]:
				correntes[linha][3] = "Cold"
				tabela.setItem(linha, 3, tipo)

			tabela.item(linha, 3).setTextAlignment(Qt.AlignCenter)

		if correntes_util[0][3] != correntes_util[1][3]:
			dlg.pinchbutton.setEnabled(True)
	except:
		pass

def remover_corrente(corrente, tabela, tipo):
	global correntes, correntes_util, n_util, ncold, nhot, n

	if corrente == -1:
		mensagem_erro("Select the line of the Stream that you want to remove")
		return

	if tipo == "corrente":
		n -= 1
		if correntes[corrente][3] == "Hot":
			nhot -= 1
		elif correntes[corrente][3] == "Cold":
			ncold -= 1
		correntes.pop(corrente)
	elif tipo == "utilidade":
		n_util -= 1
		correntes_util.pop(corrente)
		dlg.botao_addutility.setEnabled(True)

	tabela.removeRow(corrente)
	tabela.setCurrentCell(-1, -1)

def done_teste(libera=False):
	global dTmin, done, correntes
	lista_cps = []

	for corrente in correntes:
		lista_cps.append(corrente[2])

	dTmin=float(dlg.lineEdit_2.text().replace(",", "."))
	if arquivo == "40 correntes - 3 dtmin.xls":
		dTmin = 3
	pinchf, pinchq, util_quente, util_fria, coisas_graficos = pontopinch(correntes, len(correntes), dTmin)
	dlg.done = uic.loadUi("done.ui")
	# dlg.done.showMaximized()
	dlg.done.show()
	dlg.done.hot_temp.setText("Hot: " + str(pinchq) + " " + dlg.temp_unidade.currentText())
	dlg.done.cold_temp.setText("Cold: " + str(pinchf) + " " + dlg.temp_unidade.currentText())
	dlg.done.precisa_quente.setText("Hot Utility Demand: " + str(util_quente) + " " + "kW")
	dlg.done.precisa_fria.setText("Cold Utility Demand: " + str(util_fria) + " " + "kW")

	calor = dlg.cp_unidade.currentText().split("/")
	unidades_usadas = [dlg.temp_unidade.currentText(), dlg.cp_unidade.currentText(), calor[0]]

	tamanho = 400

	curva_comp = curva_composta(correntes, float(dlg.lineEdit_2.text().replace(",", ".")), util_fria, util_quente, pinchf, pinchq, unidades_usadas)
	arrumar_tamanho(curva_comp, "curva_composta", tamanho, dlg.done.curva_composta, dlg.done.scroll_composta)

	grande_curva = grande_curva_composta(len(correntes), dlg, coisas_graficos[0], coisas_graficos[7], coisas_graficos[5], unidades_usadas)
	arrumar_tamanho(grande_curva, "grande_curva", tamanho, dlg.done.grande_curva, dlg.done.scroll_grande)


	def liberar_utilidades(libera):
		dlg.botao_addutility.setEnabled(True)
		dlg.remover_utilidade.setEnabled(True)
		dlg.utilidade.setEnabled(True)
		dlg.util_inlet.setEnabled(True)
		dlg.util_outlet.setEnabled(True)
		dlg.util_pelicula.setEnabled(True)
		dlg.donebutton.setEnabled(False)
		dlg.botao_addstream.setEnabled(False)
		dlg.remover_corrente.setEnabled(False)
		dlg.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
		dlg.done.close()
		if libera:
			if arquivo == "9 correntes - 20 dtmin.xls":
				correntes_util.append([300, 299, 1, "Hot", 0.5])
				correntes_util.append([10, 20, 1, "Cold", 0.5])
			elif arquivo != "4 correntes - 10 dtmin.xls":
				correntes_util.append([600, 599, 1, "Hot", 0.5])
				correntes_util.append([0, 5, 1, "Cold", 0.5])
			e_utilidade.append(True)
			e_utilidade.append(True)

	def pinch_sem_util():
		dlg.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
		dlg.tableWidget_5.setEditTriggers(QAbstractItemView.NoEditTriggers)
		pinch_teste()
		dlg.done.close()

	if libera:
		liberar_utilidades(libera)

	dlg.done.cancelar.clicked.connect(lambda: dlg.done.close())
	dlg.done.escolher_utilidades.clicked.connect(liberar_utilidades)
	dlg.done.pinch_sem_utilidades.clicked.connect(pinch_sem_util)

def pinch_teste(desenha=True):
	global Th0, Thf, CPh, Tc0, Tcf, CPc, Thf_acima, Th0_abaixo, Tc0_acima, Tcf_abaixo
	Th0, Thf, CPh, Tc0, Tcf, CPc, Thf_acima, Th0_abaixo, Tc0_acima, Tcf_abaixo = [], [], [], [], [], [], [], [], [], []
	global correntes, correntes_util, dTmin, pinchf, pinchq, n, util_quente, util_fria, nhot, ncold, util_temporaria, correntes_temporaria
	global corrente_quente_presente_acima, corrente_quente_presente_abaixo, corrente_fria_presente_acima, corrente_fria_presente_abaixo


	if len(correntes_util) != 0:
		if correntes_util[0][3] == correntes_util[1][3]:
			mensagem_erro("You won't be able to sinthetize the Heat Exchange Network with two " + correntes_util[0][3] + " utilities. Edit any of these to make sure you have the both types.")
			dlg.pinchbutton.setEnabled(False)
			return
		else:
			dlg.pinchbutton.setEnabled(True)

	util_temporaria = nao_sacrificar_matriz(correntes_util)
	pinchf, pinchq, util_quente, util_fria, a = pontopinch(correntes, n, dTmin)

	for util in correntes_util:
		if util[3] == "Hot":
			util[2] = util_quente/(util[0] - util[1])
			nhot += 1
		else:
			util[2] = util_fria/(util[1] - util[0])
			ncold += 1


	util_temporaria = nao_sacrificar_matriz(correntes_util)
	correntes_temporaria = nao_sacrificar_matriz(correntes)
	correntes += correntes_util
	n += len(correntes_util)
	#arruma as temperaturas baseado no pinch
	for i in range(n): #correção das temperaturas
		if correntes[i][3] == "Hot":
			correntes_quentes.append(1)
			if e_utilidade[i]:
				e_utilidade_quente.append(True)
			else:
				e_utilidade_quente.append(False)
			Th0.append(correntes[i][0])
			Thf.append(correntes[i][1])
			CPh.append(correntes[i][2])
			if correntes[i][1] >= pinchq: #corrente quente nao bate no pinch acima
				Thf_acima.append(correntes[i][1])
				corrente_quente_presente_abaixo.append(False)
			else:
				Thf_acima.append(pinchq)
				corrente_quente_presente_abaixo.append(True)
			if correntes[i][0] <= pinchq: #corrente quente não bate no pinch abaixo
				Th0_abaixo.append(correntes[i][0])
				corrente_quente_presente_acima.append(False)
			else:
				Th0_abaixo.append(pinchq)
				corrente_quente_presente_acima.append(True)

		if correntes[i][3] == "Cold":
			correntes_frias.append(1)
			if e_utilidade[i]:
				e_utilidade_fria.append(True)
			else:
				e_utilidade_fria.append(False)
			Tc0.append(correntes[i][0])
			Tcf.append(correntes[i][1])
			CPc.append(correntes[i][2])
			if correntes[i][0] >= pinchf: #corrente fria não bate no pinch acima
				Tc0_acima.append(correntes[i][0])
				corrente_fria_presente_abaixo.append(False)
			else:
				Tc0_acima.append(pinchf)
				corrente_fria_presente_abaixo.append(True)
			if correntes[i][1] <= pinchf: #corrente fria não bate no pinch abaixo
				Tcf_abaixo.append(correntes[i][1])
				corrente_fria_presente_acima.append(False)
			else:
				Tcf_abaixo.append(pinchf)
				corrente_fria_presente_acima.append(True)



	global unidades_usadas
	calor = dlg.cp_unidade.currentText().split("/")
	unidades_usadas = [dlg.temp_unidade.currentText(), dlg.cp_unidade.currentText(), calor[0]]

	unidades(pinch=True)

	#manda tudo pro backend

	receber_pinch(Th0, Tcf, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, Thf_acima, Tc0_acima)
	receber_pinch_abaixo(Thf, Tc0, nhot, ncold, CPh, CPc, dTmin, pinchq, pinchf, Th0_abaixo, Tcf_abaixo)
	printar()
	printar_abaixo()
	correntesnoscombos(nhot,ncold)
	testar_correntes(dlg, True)
	testar_correntes_abaixo(dlg)

	vai()

	#libera botões e coisas
	dlg.tabWidget.setTabEnabled(1,True)
	dlg.tabWidget.setTabEnabled(2,True)
	dlg.tabWidget.setTabEnabled(3,True)
	dlg.tabWidget.setTabEnabled(4,True)
	dlg.tabWidget.setCurrentIndex(2)
	dlg.pinchbutton.setEnabled(False)
	dlg.botao_addstream.setEnabled(False)
	dlg.botao_addutility.setEnabled(False)
	dlg.remover_utilidade.setEnabled(False)
	dlg.remover_corrente.setEnabled(False)
	dlg.donebutton.setEnabled(False)
	dlg.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
	dlg.tableWidget_5.setEditTriggers(QAbstractItemView.NoEditTriggers)

def correntesnoscombos(nhot,ncold):
	for i in range(nhot):
		dlg.comboBox_9.addItem(str(i+1)) #util fria tabelas acima (corrente quente)
		dlg.comboBox_43.addItem(str(i+1)) #util fria tabelas abaixo (corrente quente)
		dlg.comboBox_51.addItem(str(i+1)) #sub cold acima
		dlg.comboBox_54.addItem(str(i+1)) #sub cold abaixo
		dlg.corrente_abaixo.addItem("Hot " + str(i+1))
		if not e_utilidade_quente[i]:
			dlg.comboutil.addItem("Hot " + str(i+1)) #util evolução
			dlg.comboBox_2.addItem(str(i+1)) #hot acima
			dlg.comboBox_35.addItem(str(i+1)) #hot abaixo
		else:
			dlg.comboBox_2.addItem(str(i+1) + " (utility)") #hot acima
	for i in range(ncold):
		dlg.comboBox_10.addItem(str(i+1)) #util quente tabelas acima (corrente fria)
		dlg.comboBox_44.addItem(str(i+1)) #util quente tabelas abaixo (corrente fria)
		dlg.comboBox_50.addItem(str(i+1)) #sub hot acima
		dlg.comboBox_53.addItem(str(i+1)) #sub hot abaixo
		dlg.corrente_acima.addItem("Cold " + str(i+1))
		if not e_utilidade_fria[i]:
			dlg.comboBox_5.addItem(str(i+1)) #cold acima
			dlg.comboBox_36.addItem(str(i+1)) #cold abaixo
			dlg.comboutil.addItem("Cold " + str(i+1)) #util evolução
		else:
			dlg.comboBox_36.addItem(str(i+1) + " (utility)") #cold abaixo

	for i in range(1, min(nhot, ncold)):
		dlg.nivel.addItem(str(i+1))

	for i in range(max(nhot, ncold)):
		dlg.comboutil_sub.addItem(str(i+1))

def unidades(header=True, corrente=True, pinch=False):
	if not header:
		if dlg.sistema_unidades.currentIndex() != 2:
			dlg.temp_unidade.setCurrentIndex(dlg.sistema_unidades.currentIndex())
			dlg.cp_unidade.setCurrentIndex(dlg.sistema_unidades.currentIndex())
			dlg.pelicula_unidade.setCurrentIndex(dlg.sistema_unidades.currentIndex())
			dlg.temp_unidade_util.setCurrentIndex(dlg.sistema_unidades.currentIndex())
			dlg.pelicula_unidade_util.setCurrentIndex(dlg.sistema_unidades.currentIndex())
			dlg.temp_unidade.setEnabled(False)
			dlg.cp_unidade.setEnabled(False)
			dlg.pelicula_unidade.setEnabled(False)
			dlg.temp_unidade_util.setEnabled(False)
			dlg.pelicula_unidade_util.setEnabled(False)
		else:
			dlg.temp_unidade.setEnabled(True)
			dlg.cp_unidade.setEnabled(True)
			dlg.pelicula_unidade.setEnabled(True)
			dlg.temp_unidade_util.setEnabled(True)
			dlg.pelicula_unidade_util.setEnabled(True)
			if corrente:
				dlg.temp_unidade_util.setCurrentIndex(dlg.temp_unidade.currentIndex())
				dlg.pelicula_unidade_util.setCurrentIndex(dlg.pelicula_unidade.currentIndex())


	headerrr = ["Supply Temperature ({})".format(dlg.temp_unidade.currentText()),
				"Target Temperature ({})".format(dlg.temp_unidade.currentText()),
				"CP ({})".format(dlg.cp_unidade.currentText()),
				"Stream Type",
				"h ({})".format(dlg.pelicula_unidade.currentText())]
	dlg.tableWidget.setHorizontalHeaderLabels(headerrr)
	headerrr = ["Utility",
				"Inlet Temperature ({})".format(dlg.temp_unidade_util.currentText()),
				"Outlet Temperature ({})".format(dlg.temp_unidade_util.currentText()),
				"Utility Type",
				"h ({})".format(dlg.pelicula_unidade_util.currentText())]
	dlg.tableWidget_5.setHorizontalHeaderLabels(headerrr)

	if pinch:
		headerrr = ["Hot Stream",
					"Cold Stream",
					"Sub Hot Stream",
					"Sub Cold Stream",
					" Heat Exchanged ({}) ".format(str(unidades_usadas[2])),
					" Inlet Hot Temp. ({}) ".format(str(unidades_usadas[0])),
					" Outlet Cold Temp. ({}) ".format(str(unidades_usadas[0])),
					" Outlet Hot Temp. ({}) ".format(str(unidades_usadas[0])),
					" Inlet Cold Temp. ({}) ".format(str(unidades_usadas[0])),
					"Hot Fraction",
					"Cold Fraction"]
		dlg.tableWidget_2.setHorizontalHeaderLabels(headerrr)
		dlg.tableWidget_14.setHorizontalHeaderLabels(headerrr)
		headerrr = ["Stream",
					" Supply Temp. ({}) (Goal) ".format(str(unidades_usadas[0])),
					" Intermediate Temp. ({}) ".format(str(unidades_usadas[0])),
					" Outlet Temp. ({}) ".format(str(unidades_usadas[0])),
					" Heat Duty ({}) ".format(str(unidades_usadas[2]))]
		dlg.tableWidget_3.setHorizontalHeaderLabels(headerrr)
		headerrr = ["Stream",
					" Outlet Temp. ({}) (Goal) ".format(str(unidades_usadas[0])),
					" Intermediate Temp. ({}) ".format(str(unidades_usadas[0])),
					" Inlet Temp. ({}) ".format(str(unidades_usadas[0])),
					" Heat Duty ({}) ".format(str(unidades_usadas[2]))]
		dlg.tableWidget_4.setHorizontalHeaderLabels(headerrr)
		headerrr = ["Stream",
					" Inlet Temp. ({}) ".format(str(unidades_usadas[0])),
					" Intermediate Temp. ({}) ".format(str(unidades_usadas[0])),
					" Outlet Temp. ({}) (Goal) ".format(str(unidades_usadas[0])),
					" Heat Duty ({}) ".format(str(unidades_usadas[2]))]
		dlg.tableWidget_15.setHorizontalHeaderLabels(headerrr)
		headerrr = ["Stream",
					" Outlet Temp. ({}) ".format(str(unidades_usadas[0])),
					" Intermediate Temp. ({}) ".format(str(unidades_usadas[0])),
					" Supply Temp. ({}) (Goal) ".format(str(unidades_usadas[0])),
					" Heat Duty ({}) ".format(str(unidades_usadas[2]))]
		dlg.tableWidget_17.setHorizontalHeaderLabels(headerrr)
		for i in range(4, 9):
			dlg.tableWidget_2.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
			dlg.tableWidget_14.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
		for i in range(5):
			dlg.tableWidget_3.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
			dlg.tableWidget_4.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
			dlg.tableWidget_15.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
			dlg.tableWidget_17.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

def unidades_compativeis(unidade_temp, unidade_cp, unidade_pelicula, cp_printar):
	#0:si
	#1:eng
	#2:si
	#3:eng
	cp_contas = []

	if (unidade_temp == 0 or unidade_temp == 2) and (unidade_cp != 0 or unidade_pelicula != 0):
		if unidade_cp != 0:
			print("cp incompativel")
			for cp in cp_printar:
				cp_contas.append(cp * 0.00052753)
		if unidade_pelicula != 0:
			#converter aqui a unidade pelicula para 0
			print("pelicula incompativel")
	elif (unidade_temp == 1 or unidade_temp == 3) and (unidade_cp != 1 or unidade_pelicula != 1):
		if unidade_cp != 1:
			print("cp incompativel 1")
			for cp in cp_printar:
				cp_contas.append(cp / 0.00052753)
		if unidade_pelicula != 1:
			#converter aqui pelicula pra 1
			print("pelicula incompativel 1")
	else:
		cp_contas = cp_printar

	return cp_contas



#diagrams comparison
def mensagem_erro(texto, titulo="Error"):
	msg = QMessageBox()
	msg.setIcon(QMessageBox.Warning)
	msg.setStyleSheet("font-weight: bold")
	msg.setStyleSheet("text-align: center")
	msg.setText(texto)
	msg.setWindowTitle(titulo)
	msg.setStandardButtons(QMessageBox.Ok)
	msg.exec_()
	return

def verificar_digitos(linha, grafico=None, qual_dt=None):
	asch = linha.text().replace(",", ".").split(".")
	if len(asch) == 2:
		if len(asch[1]) > 4:
			if qual_dt == "1" or qual_dt == "2":
				grafico.setText('Waiting for ΔTmin' + qual_dt +' data...')
				if qual_dt == "1":
					mensagem_erro("The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT ONE} value and try again.")
				elif qual_dt == "2":
					mensagem_erro("The limit is 4 digits after the separator.\nChange the ΔTmin\N{SUBSCRIPT TWO} value and try again.")
			return True
	return False

def arrumar_tamanho(fig, nome, tamanho, onde_botar, scroll, casca=False):
	tamanho -= 20
	fig.savefig(nome + ".png", bbox_inches="tight", pad_inches=0.5)
	pic = Image.open(nome + ".png")
	if not casca:
		razao = min(tamanho/pic.size[0], tamanho/pic.size[1])
	else:
		razao = tamanho/pic.size[1]
	novo_tamanho = (int(razao*pic.size[0]), int(razao*pic.size[1]))
	pic = pic.resize(novo_tamanho, Image.ANTIALIAS)
	pic.save(nome + ".png", quality=100)
	onde_botar.setPixmap(QtGui.QPixmap(nome + ".png"))

def grande_curva_comp():
	if verificar_digitos(dlg.DTMIN1, dlg.graficodt1, "1") or verificar_digitos(dlg.DTMIN2, dlg.graficodt2, "2"):
		return

	if not dlg.DTMIN1.text().replace(",", ".") and not dlg.DTMIN2.text().replace(",", "."):
		mensagem_erro("Please input any ΔTmin data")

	if dlg.DTMIN1.text().replace(",", "."):
		_, _, _, _, coisas_graficos1 = pontopinch(correntes_temporaria, len(correntes_temporaria), float(dlg.DTMIN1.text().replace(",", ".")))
		fig = grande_curva_composta(len(correntes_temporaria), dlg, coisas_graficos1[0], coisas_graficos1[7], coisas_graficos1[5], unidades_usadas)
		tamanho = dlg.graficodt1.frameGeometry().height()
		if tamanho < 550:
			tamanho = 550
		arrumar_tamanho(fig, "Gc1", tamanho, dlg.graficodt1, dlg.scroll_dt1)
	else:
		dlg.graficodt1.setText('Waiting for ΔTmin1 data...')

	if dlg.DTMIN2.text().replace(",", "."):
		_, _, _, _, coisas_graficos2 = pontopinch(correntes_temporaria, len(correntes_temporaria), float(dlg.DTMIN2.text().replace(",", ".")))
		fig = grande_curva_composta(len(correntes_temporaria), dlg, coisas_graficos2[0], coisas_graficos2[7], coisas_graficos2[5], unidades_usadas)
		tamanho = dlg.graficodt2.frameGeometry().height()
		if tamanho < 550:
			tamanho = 550
		arrumar_tamanho(fig, "Gc2", tamanho, dlg.graficodt2, dlg.scroll_dt2)
	else:
		dlg.graficodt2.setText('Waiting for ΔTmin2 data...')

def curva_comp_balanceada():
	if verificar_digitos(dlg.DTMIN1, dlg.graficodt1, "1") or verificar_digitos(dlg.DTMIN2, dlg.graficodt2, "2"):
		return

	if not dlg.DTMIN1.text().replace(",", ".") and not dlg.DTMIN2.text().replace(",", "."):
		mensagem_erro("Please input any ΔTmin data")

	if dlg.DTMIN1.text().replace(",", "."):
		contador = 0
		tf1, tq1, uq1, uf1, _ = pontopinch(correntes_temporaria, len(correntes_temporaria), float(dlg.DTMIN1.text().replace(",", ".")))
		uf1, uq1, _, _ = fp2.pontopinch(correntes_temporaria, len(correntes_temporaria), float(dlg.DTMIN1.text().replace(",", ".")))

		for i in range(0, len(util_temporaria)):
			if util_temporaria[i][3] == 'Cold':
				util_temporaria[i][2] = uf1 / (util_temporaria[i][1] - util_temporaria[i][0])
				correntes_temporaria.append(util_temporaria[i])
				contador += 1
			else:
				util_temporaria[i][2] = uq1 / (util_temporaria[i][0] - util_temporaria[i][1])
				correntes_temporaria.append(util_temporaria[i])
				contador += 1

		_,_,datagraph,_,_,_,_ = CUSTO(correntes_temporaria, len(correntes_temporaria))
		fig = curva_composta_balanceada(datagraph, float(dlg.DTMIN1.text().replace(",", ".")), round(tf1, 6), round(tq1, 6), unidades_usadas)
		tamanho = dlg.graficodt1.frameGeometry().height()
		if tamanho < 550:
			tamanho = 550
		arrumar_tamanho(fig, "cc1", tamanho, dlg.graficodt1, dlg.scroll_dt1)

		for i in range(contador):
			correntes_temporaria.pop(-1)
	else:
		dlg.graficodt1.setText('Waiting for ΔTmin1 data...')

	if dlg.DTMIN2.text().replace(",", "."):
		contador = 0
		tf2, tq2, uq2, uf2, _ = pontopinch(correntes_temporaria, len(correntes_temporaria), float(dlg.DTMIN2.text().replace(",", ".")))
		uf2, uq2, _, _ = fp2.pontopinch(correntes_temporaria, len(correntes_temporaria), float(dlg.DTMIN2.text().replace(",", ".")))

		for i in range(len(util_temporaria)):
			if util_temporaria[i][3] == 'Cold':
				util_temporaria[i][2] = uf2 / (util_temporaria[i][1] - util_temporaria[i][0])
				correntes_temporaria.append(util_temporaria[i])
				contador += 1
			else:
				util_temporaria[i][2] = uq2 / (util_temporaria[i][0] - util_temporaria[i][1])
				correntes_temporaria.append(util_temporaria[i])
				contador += 1

		_,_,datagraph,_,_,_,_  = CUSTO(correntes_temporaria, len(correntes_temporaria))

		fig = curva_composta_balanceada(datagraph, float(dlg.DTMIN2.text().replace(",", ".")), round(tf2, 6), round(tq2, 6), unidades_usadas)
		tamanho = dlg.graficodt2.frameGeometry().height()
		if tamanho < 550:
			tamanho = 550
		arrumar_tamanho(fig, "cc2", tamanho, dlg.graficodt2, dlg.scroll_dt2)

		for i in range(contador):
			correntes_temporaria.pop(-1)
	else:
		dlg.graficodt2.setText('Waiting for ΔTmin2 data...')

def curva_comp():
	if verificar_digitos(dlg.DTMIN1, dlg.graficodt1, "1") or verificar_digitos(dlg.DTMIN2, dlg.graficodt2, "2"):
		return

	if not dlg.DTMIN1.text().replace(",", ".") and not dlg.DTMIN2.text().replace(",", "."):
		mensagem_erro("Please input any ΔTmin data")

	if dlg.DTMIN1.text().replace(",", "."):
		pinchf1, pinchq1, uq1, uf1, _ = pontopinch(correntes_temporaria, len(correntes_temporaria), float(dlg.DTMIN1.text().replace(",", ".")))
		fig = curva_composta(correntes_temporaria, float(dlg.DTMIN1.text().replace(",", ".")), uf1, uq1, pinchf1, pinchq1, unidades_usadas)
		tamanho = dlg.graficodt1.frameGeometry().height()
		if tamanho < 550:
			tamanho = 550
		arrumar_tamanho(fig, "curvadt1", tamanho, dlg.graficodt1, dlg.scroll_dt1)
	else:
		dlg.graficodt1.setText('Waiting for ΔTmin1 data...')

	if dlg.DTMIN2.text().replace(",", "."):
		pinchf2, pinchq2, uq2, uf2,_ = pontopinch(correntes_temporaria, len(correntes_temporaria), float(dlg.DTMIN2.text().replace(",", ".")))
		fig = curva_composta(correntes_temporaria, float(dlg.DTMIN2.text().replace(",", ".")), uf2, uq2, pinchf2, pinchq2, unidades_usadas)
		tamanho = dlg.graficodt2.frameGeometry().height()
		if tamanho < 550:
			tamanho = 550
		arrumar_tamanho(fig, "curvadt2", tamanho, dlg.graficodt2, dlg.scroll_dt2)
		dlg.graficodt2.setPixmap(QtGui.QPixmap("curvadt2.png"))
	else:
		dlg.graficodt2.setText('Waiting for ΔTmin2 data...')

def cascataaa():
	if verificar_digitos(dlg.DTMIN1, dlg.graficodt1, "1") or verificar_digitos(dlg.DTMIN2, dlg.graficodt2, "2"):
		return

	if not dlg.DTMIN1.text().replace(",", ".") and not dlg.DTMIN2.text().replace(",", "."):
		mensagem_erro("Please input any ΔTmin data")

	if dlg.DTMIN1.text().replace(",", "."):
		fig = cascata(correntes_temporaria, float(dlg.DTMIN1.text().replace(",", ".")), unidades_usadas)
		tamanho = dlg.graficodt1.frameGeometry().height()
		arrumar_tamanho(fig, "EC", tamanho, dlg.graficodt1, dlg.scroll_dt1, casca=True)
	else:
		dlg.graficodt1.setText('Waiting for ΔTmin1 data...')


	if dlg.DTMIN2.text().replace(",", "."):
		fig = cascata(correntes_temporaria, float(dlg.DTMIN2.text().replace(",", ".")), unidades_usadas)
		tamanho = dlg.graficodt2.frameGeometry().height()
		arrumar_tamanho(fig, "EC2", tamanho, dlg.graficodt2, dlg.scroll_dt2, casca=True)
	else:
		dlg.graficodt2.setText('Waiting for ΔTmin2 data...')

def area_information(dtmin, grafico):
	if verificar_digitos(dtmin, grafico, "2"):
		return

	if len(util_temporaria) == 0:
		mensagem_erro("Please input utility data in 'Streams' tab")
		return

	if dtmin.text().replace(",", "."):
		uf1, uq1, _, _ = fp2.pontopinch(correntes_temporaria, len(correntes_temporaria), float(dtmin.text().replace(",", ".")))

		contador = 0
		for i in range(0, len(util_temporaria)):
			if util_temporaria[i][3] == 'Cold':
				util_temporaria[i][2] = uf1 / (util_temporaria[i][1] - util_temporaria[i][0])
				correntes_temporaria.append(util_temporaria[i])
				contador += 1
			else:
				util_temporaria[i][2] = uq1 / (util_temporaria[i][0] - util_temporaria[i][1])
				correntes_temporaria.append(util_temporaria[i])
				contador += 1

		akt, _, ajustado, cpf, cpq, areak,deltalmnk = CUSTO(correntes_temporaria, len(correntes_temporaria))

		for i in range(contador):
			correntes_temporaria.pop(-1)

		dlg.area = uic.loadUi("Area.ui")
		dlg.area.show()
		dlg.area.label.setText("ΔTmin\N{SUBSCRIPT TWO} :  "+str(round(float(dtmin.text().replace(",", ".")), 5)))
		dlg.area.label.setFont(QFont('Arial', 14))
		dlg.area.label.setStyleSheet("font-weight: bold")
		row = 0
		dlg.area.TABELA.setRowCount(len(areak) + 1)

		for data in range(0, len(areak)):
			dlg.area.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data], 2))))
			dlg.area.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data+1], 2))))
			dlg.area.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data], 2))))
			dlg.area.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data+1], 2))))
			dlg.area.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(round(cpq[data], 2))))
			dlg.area.TABELA.setItem(row, 5, QtWidgets.QTableWidgetItem(str(round(cpf[data], 2))))
			dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str(round(deltalmnk[data], 2))))
			dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round(areak[data], 2))))
			row += 1
		dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str('Total Area:')))
		dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round((akt), 2))))
	else:
		mensagem_erro("Please input ΔTmin₂ data")



#desenhos
def desenhar_rede(correntes_quentes, correntes_frias, subrede, subredes=False, ensure=False):

	def criar_turtle():
		nome = turtle.Turtle()
		nome.speed("fastest")
		nome.hideturtle()
		nome.penup()
		return nome

	def quentes(onde, correntes_desenho, presente):
		global y_acima, y_abaixo
		ja_cp = False
		for i in range(len(correntes_desenho)):

			if onde == "above":
				ident.sety(y_acima - h_string)
				ident.setx(distancia_x/2 + distancia_cp/2)
				alinha = "left"
			elif onde == "below":
				ident.sety(y_abaixo - h_string)
				ident.setx(-distancia_x/2 - distancia_cp/2)
				alinha = "right"
			elif onde == "ambas":
				ident.sety(y_acima - h_string)
				ident.setx(distancia_x/2 + distancia_cp)
				alinha = "left"
			if e_utilidade_quente[i]:
				if onde == "below":
					ident.write("(utility) Hot " + str(i+1), align=alinha, font=("Arial", fonte_carga, "bold"))
				else:
					ident.write("Hot " + str(i+1) + " (utility)", align=alinha, font=("Arial", fonte_carga, "bold"))
			else:
				ident.write("Hot " + str(i+1), align=alinha, font=("Arial", fonte_carga, "bold"))

			if presente[i] and onde != "ambas":
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].speed(1000)
				correntes_desenho[i].shapesize(seta, seta, seta)
				if e_utilidade_quente[i]:
					correntes_desenho[i].color("orange")
				else:
					correntes_desenho[i].color("red")
				correntes_desenho[i].pensize(grossura_corrente)
				correntes_desenho[i].penup()
				correntes_desenho_sub_acima = [0] * nhot
				correntes_desenho_sub_abaixo = [0] * nhot

				if onde == "above":
					correntes_desenho[i].setx(-distancia_x/2)
					correntes_desenho[i].sety(y_acima)
					correntes_desenho[i].pendown()
					if not ja_cp:
						temp.sety(y_acima - h_string + ramo_y)
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
						temp.write("Streams CP ({})".format(unidades_usadas[1]), align="center", font=("Arial", fonte_carga, "bold"))
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
						temp.write("Streams Duty ({})".format(unidades_usadas[2]), align="center", font=("Arial", fonte_carga, "bold"))
						ja_cp = True
					temp.sety(y_acima - h_string)
					temp.setx(-distancia_x/2 - len(str('{:.2f}'.format(round(Th0[i], 2))))*tamanho_string)
					temp.write(str('{:.2f}'.format(round(Th0[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if Thf_acima[i] != pinchq:
						temp.setx(distancia_x/2 - nao_toca_pinch + 5)
						temp.write(str('{:.2f}'.format(round(Thf_acima[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if not dividida_quente[i]:
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
						temp.write(str('{:.2f}'.format(round(CPh[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_quente[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					else:
						correntes_desenho_sub_acima[i] = [0] * (quantidade_quente[i] - 1)
						for j in range(quantidade_quente[i]-1):
							temp.sety(y_acima - h_string)
							temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
							temp.write(str('{:.2f}'.format(round(CPh[i]*fracoes_quentes[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
							temp.write(str('{:.2f}'.format(round(calor_atual_quente_sub[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							correntes_desenho_sub_acima[i][j] = turtle.Turtle()
							if e_utilidade_quente[i]:
								correntes_desenho_sub_acima[i][j].color("orange")
							else:
								correntes_desenho_sub_acima[i][j].color("red")
							correntes_desenho_sub_acima[i][j].pensize(grossura_corrente)
							correntes_desenho_sub_acima[i][j].hideturtle()
							correntes_desenho_sub_acima[i][j].penup()
							correntes_desenho_sub_acima[i][j].setx(-distancia_x/2 + ramo_x)
							correntes_desenho_sub_acima[i][j].sety(y_acima)
							correntes_desenho_sub_acima[i][j].pendown()
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(ramo_y)
							correntes_desenho_sub_acima[i][j].left(90)
							if Thf_acima[i] == pinchq:
								correntes_desenho_sub_acima[i][j].forward(distancia_x - 2*ramo_x)
							else:
								correntes_desenho_sub_acima[i][j].forward(distancia_x - nao_toca_pinch - 2*ramo_x)
							correntes_desenho_sub_acima[i][j].left(90)
							correntes_desenho_sub_acima[i][j].forward(ramo_y*(j+1))
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(ramo_x)
							y_acima -= ramo_y
						temp.sety(y_acima - h_string)
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
						temp.write(str('{:.2f}'.format(round(CPh[i]*fracoes_quentes[i][quantidade_quente[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_quente_sub[i][quantidade_quente[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					if Thf_acima[i] == pinchq:
						correntes_desenho[i].forward(distancia_x)
					else:
						correntes_desenho[i].forward(distancia_x - nao_toca_pinch)

				elif onde == "below":
					correntes_desenho[i].sety(y_abaixo)
					if not ja_cp:
						temp.sety(y_abaixo - h_string + ramo_y)
						temp.setx(distancia_x/2 + distancia_cp + maior_cp)
						temp.write("Streams CP ({})".format(unidades_usadas[1]), align="center", font=("Arial", fonte_carga, "bold"))
						temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
						temp.write("Streams Duty ({})".format(unidades_usadas[2]), align="center", font=("Arial", fonte_carga, "bold"))
						ja_cp = True
					temp.sety(y_abaixo - h_string)
					temp.setx(distancia_x/2 + 6)
					temp.write(str('{:.2f}'.format(round(Thf[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if Th0_abaixo[i] != pinchq:
						temp.setx(-distancia_x/2 + nao_toca_pinch - len(str('{:.2f}'.format(round(Th0[i], 2))))*tamanho_string)
						temp.write(str('{:.2f}'.format(round(Th0_abaixo[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if not dividida_quente_abaixo[i]:
						temp.setx(distancia_x/2 + distancia_cp + maior_cp)
						temp.write(str('{:.2f}'.format(round(CPh[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_quente_abaixo[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					else:
						correntes_desenho_sub_abaixo[i] = [0] * (quantidade_quente_abaixo[i] - 1)
						for j in range(quantidade_quente_abaixo[i]-1):
							temp.sety(y_abaixo - h_string)
							temp.setx(distancia_x/2 + distancia_cp + maior_cp)
							temp.write(str('{:.2f}'.format(round(CPh[i]*fracoes_quentes_abaixo[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
							temp.write(str('{:.2f}'.format(round(calor_atual_quente_sub_abaixo[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
							correntes_desenho_sub_abaixo[i][j].color("red")
							correntes_desenho_sub_abaixo[i][j].pensize(grossura_corrente)
							correntes_desenho_sub_abaixo[i][j].hideturtle()
							correntes_desenho_sub_abaixo[i][j].penup()
							correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
							if Th0_abaixo[i] == pinchq:
								correntes_desenho_sub_abaixo[i][j].setx(-distancia_x/2 + ramo_x)
								correntes_desenho_sub_abaixo[i][j].pendown()
								correntes_desenho_sub_abaixo[i][j].right(90)
								correntes_desenho_sub_abaixo[i][j].forward(ramo_y)
								correntes_desenho_sub_abaixo[i][j].left(90)
								if fechar_corrente_abaixo[i]:
									correntes_desenho_sub_abaixo[i][j].forward((len(matriz_trocadores_abaixo)+0.5)*espaco_trocadores)
									temperatura.sety(y_abaixo + 1)
									temperatura.setx(-distancia_x/2 + (len(matriz_trocadores_abaixo)+1)*espaco_trocadores)
									temperatura.write(str('{:.2f}'.format(round(temp_misturador_abaixo[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
								else:
									correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 2*ramo_x)
							else:
								correntes_desenho_sub_abaixo[i][j].setx(-distancia_x/2 + nao_toca_pinch + ramo_x)
								correntes_desenho_sub_abaixo[i][j].pendown()
								correntes_desenho_sub_abaixo[i][j].right(90)
								correntes_desenho_sub_abaixo[i][j].forward(ramo_y)
								correntes_desenho_sub_abaixo[i][j].left(90)
								if fechar_corrente_abaixo[i]:
									correntes_desenho_sub_abaixo[i][j].forward((len(matriz_trocadores_abaixo)+0.5)*espaco_trocadores)
									temperatura.sety(y_abaixo + 1)
									temperatura.setx(-distancia_x/2 + (len(matriz_trocadores_abaixo)+1)*espaco_trocadores)
									temperatura.write(str('{:.2f}'.format(round(temp_misturador_abaixo[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
								else:
									correntes_desenho_sub_abaixo[i][j].forward(distancia_x - nao_toca_pinch - 2*ramo_x)
							correntes_desenho_sub_abaixo[i][j].left(90)
							correntes_desenho_sub_abaixo[i][j].forward(ramo_y*(j+1))
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(ramo_x)
							y_abaixo -= ramo_y
						temp.sety(y_abaixo - h_string)
						temp.setx(distancia_x/2 + distancia_cp + maior_cp)
						temp.write(str('{:.2f}'.format(round(CPh[i]*fracoes_quentes_abaixo[i][quantidade_quente_abaixo[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_quente_sub_abaixo[i][quantidade_quente_abaixo[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					if Th0_abaixo[i] == pinchq:
						correntes_desenho[i].setx(-distancia_x/2)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x)
					else:
						correntes_desenho[i].setx(-distancia_x/2+ nao_toca_pinch)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x - nao_toca_pinch)

			if onde != "ambas":
				y_acima -= ramo_y
				y_abaixo -= ramo_y

			if onde == "ambas":
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].speed(1000)
				correntes_desenho[i].shapesize(seta, seta, seta)
				if e_utilidade_quente[i]:
					correntes_desenho[i].color("orange")
				else:
					correntes_desenho[i].color("red")
				correntes_desenho[i].pensize(grossura_corrente)
				correntes_desenho[i].penup()
				correntes_desenho_sub_acima = [0] * nhot
				correntes_desenho_sub_abaixo = [0] * nhot
				correntes_desenho[i].setx(-distancia_x/2)
				correntes_desenho[i].sety(y_acima)
				correntes_desenho[i].pendown()
				if not ja_cp:
					temp.sety(y_acima - h_string + ramo_y)
					temp.setx(-distancia_x/2 - distancia_cp - maior_duty)
					temp.write("Streams Duty ({})".format(unidades_usadas[2]), align="center", font=("Arial", fonte_carga, "bold"))
					ja_cp = True
				temp.sety(y_acima - h_string)
				temp.setx(-distancia_x/2 - distancia_cp - maior_duty)
				temp.write(str('{:.2f}'.format(round(calor_atual_quente_ev[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
				temp.setx(-distancia_x/2 - len(str('{:.2f}'.format(round(Th0[i], 2))))*tamanho_string)
				temp.write(str('{:.2f}'.format(round(Th0[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
				temp.setx(distancia_x/2 + 6)
				temp.write(str('{:.2f}'.format(round(Thf[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
				if dividida_quente_ev_acima[i]:
					correntes_desenho_sub_acima[i] = [0] * (quantidade_quente_ev_acima[i] - 1)
					for j in range(quantidade_quente_ev_acima[i]-1):
						correntes_desenho_sub_acima[i][j] = turtle.Turtle()
						if e_utilidade_quente[i]:
							correntes_desenho_sub_acima[i][j].color("orange")
						else:
							correntes_desenho_sub_acima[i][j].color("red")
						correntes_desenho_sub_acima[i][j].pensize(grossura_corrente)
						correntes_desenho_sub_acima[i][j].hideturtle()
						correntes_desenho_sub_acima[i][j].penup()
						correntes_desenho_sub_acima[i][j].setx(-distancia_x/2 + ramo_x)
						correntes_desenho_sub_acima[i][j].sety(y_acima)
						correntes_desenho_sub_acima[i][j].pendown()
						correntes_desenho_sub_acima[i][j].right(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_y)
						correntes_desenho_sub_acima[i][j].left(90)
						correntes_desenho_sub_acima[i][j].forward(distancia_x/2 - 2*ramo_x)
						correntes_desenho_sub_acima[i][j].left(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_y*(j+1))
						correntes_desenho_sub_acima[i][j].right(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_x)
						y_acima -= ramo_y
					temp.sety(y_acima - h_string)
					temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
				if dividida_quente_ev_abaixo[i]:
					correntes_desenho_sub_abaixo[i] = [0] * (quantidade_quente_ev_abaixo[i] - 1)
					for j in range(quantidade_quente_ev_abaixo[i]-1):
						correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
						correntes_desenho_sub_abaixo[i][j].color("red")
						correntes_desenho_sub_abaixo[i][j].pensize(grossura_corrente)
						correntes_desenho_sub_abaixo[i][j].hideturtle()
						correntes_desenho_sub_abaixo[i][j].penup()
						correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
						correntes_desenho_sub_abaixo[i][j].setx(ramo_x)
						correntes_desenho_sub_abaixo[i][j].pendown()
						correntes_desenho_sub_abaixo[i][j].right(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_y)
						correntes_desenho_sub_abaixo[i][j].left(90)
						if fechar_corrente_abaixo[i]:
							correntes_desenho_sub_abaixo[i][j].forward((len(matriz_trocadores_abaixo)+0.5)*espaco_trocadores)
							temperatura.sety(y_abaixo + 1)
							temperatura.setx((len(matriz_trocadores_abaixo)+1)*espaco_trocadores - 6)
							temperatura.write(str('{:.2f}'.format(round(temp_misturador_quente[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
						else:
							correntes_desenho_sub_abaixo[i][j].forward(distancia_x/2 - 2*ramo_x)
						correntes_desenho_sub_abaixo[i][j].left(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_y*(j+1))
						correntes_desenho_sub_abaixo[i][j].right(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_x)
						y_abaixo -= ramo_y
				correntes_desenho[i].forward(distancia_x)

				y_acima -= ramo_y
				y_abaixo -= ramo_y

				if y_acima < y_abaixo:
					y_abaixo = y_acima
				elif y_acima > y_abaixo:
					y_acima = y_abaixo

	def frias(onde, correntes_desenho, presente):
		global y_acima, y_abaixo
		for i in range(len(correntes_desenho)):

			if onde == "above":
				ident.sety(y_acima - h_string)
				ident.setx(distancia_x/2 + distancia_cp/2)
				alinha = "left"
			elif onde == "below":
				ident.sety(y_abaixo - h_string)
				ident.setx(-distancia_x/2 - distancia_cp/2)
				alinha = "right"
			else:
				ident.sety(y_acima - h_string)
				ident.setx(distancia_x/2 + distancia_cp)
				alinha = "left"
			if e_utilidade_fria[i]:
				if onde == "below":
					ident.write("(utility) Cold " + str(i+1), align=alinha, font=("Arial", fonte_carga, "bold"))
				else:
					ident.write("Cold " + str(i+1) + " (utility)", align=alinha, font=("Arial", fonte_carga, "bold"))
			else:
				ident.write("Cold " + str(i+1), align=alinha, font=("Arial", fonte_carga, "bold"))

			if presente[i] and onde != "ambas":
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].speed(1000)
				correntes_desenho[i].shapesize(seta, seta, seta)
				if e_utilidade_fria[i]:
					correntes_desenho[i].color("#7FFFD4")
				else:
					correntes_desenho[i].color("blue")
				correntes_desenho[i].pensize(grossura_corrente)
				correntes_desenho[i].penup()
				correntes_desenho_sub_acima = [0] * ncold
				correntes_desenho_sub_abaixo = [0] * ncold

				if onde == "above":
					correntes_desenho[i].sety(y_acima)
					correntes_desenho[i].left(180)
					temp.sety(y_acima - h_string)
					temp.setx(-distancia_x/2 - len(str('{:.2f}'.format(round(Tcf[i], 2))))*tamanho_string)
					temp.write(str('{:.2f}'.format(round(Tcf[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if Tc0_acima[i] != pinchf:
						temp.setx(distancia_x/2 - nao_toca_pinch + 5)
						temp.write(str('{:.2f}'.format(round(Tc0_acima[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if not dividida_fria[i]:
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
						temp.write(str('{:.2f}'.format(round(CPc[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_frio[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					else:
						correntes_desenho_sub_acima[i] = [0] * (quantidade_fria[i] - 1)
						for j in range(quantidade_fria[i] - 1):
							temp.sety(y_acima - h_string)
							temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
							temp.write(str('{:.2f}'.format(round(CPc[i]*fracoes_frias[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
							temp.write(str('{:.2f}'.format(round(calor_atual_frio_sub[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							correntes_desenho_sub_acima[i][j] = turtle.Turtle()
							correntes_desenho_sub_acima[i][j].color("blue")
							correntes_desenho_sub_acima[i][j].pensize(grossura_corrente)
							correntes_desenho_sub_acima[i][j].hideturtle()
							correntes_desenho_sub_acima[i][j].penup()
							correntes_desenho_sub_acima[i][j].sety(y_acima)
							if Tc0_acima[i] == pinchf:
								correntes_desenho_sub_acima[i][j].setx(distancia_x/2 - ramo_x)
								correntes_desenho_sub_acima[i][j].pendown()
								correntes_desenho_sub_acima[i][j].right(90)
								correntes_desenho_sub_acima[i][j].forward(ramo_y)
								correntes_desenho_sub_acima[i][j].right(90)
								if fechar_corrente[i]:
									correntes_desenho_sub_acima[i][j].forward((len(matriz_armazenada)+0.5)*espaco_trocadores)
									temperatura.sety(y_acima + 1)
									temperatura.setx(distancia_x/2 - (len(matriz_armazenada)+1)*espaco_trocadores)
									temperatura.write(str('{:.2f}'.format(round(temp_misturador[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
								else:
									correntes_desenho_sub_acima[i][j].forward(distancia_x - 2*ramo_x)
							else:
								correntes_desenho_sub_acima[i][j].setx(distancia_x/2 - nao_toca_pinch - ramo_x)
								correntes_desenho_sub_acima[i][j].pendown()
								correntes_desenho_sub_acima[i][j].right(90)
								correntes_desenho_sub_acima[i][j].forward(ramo_y)
								correntes_desenho_sub_acima[i][j].right(90)
								if fechar_corrente[i]:
									correntes_desenho_sub_acima[i][j].forward((len(matriz_armazenada)+0.5)*espaco_trocadores)
									temperatura.sety(y_acima + 1)
									temperatura.setx(distancia_x/2 - (len(matriz_armazenada)+1)*espaco_trocadores)
									temperatura.write(str('{:.2f}'.format(round(temp_misturador[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
								else:
									correntes_desenho_sub_acima[i][j].forward(distancia_x - nao_toca_pinch - 2*ramo_x)
							correntes_desenho_sub_acima[i][j].right(90)
							correntes_desenho_sub_acima[i][j].forward(ramo_y*(j+1))
							correntes_desenho_sub_acima[i][j].left(90)
							correntes_desenho_sub_acima[i][j].forward(ramo_x)
							y_acima -= ramo_y
						temp.sety(y_acima - h_string)
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp)
						temp.write(str('{:.2f}'.format(round(CPc[i]*fracoes_frias[i][quantidade_fria[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(-distancia_x/2 - distancia_cp - maior_cp*2 -  maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_frio_sub[i][quantidade_fria[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					if Tc0_acima[i] == pinchf:
						correntes_desenho[i].setx(distancia_x/2)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x)
					else:
						correntes_desenho[i].setx(distancia_x/2 - nao_toca_pinch)
						correntes_desenho[i].pendown()
						correntes_desenho[i].forward(distancia_x - nao_toca_pinch)
				elif onde == "below":
					correntes_desenho[i].sety(y_abaixo)
					correntes_desenho[i].left(180)
					correntes_desenho[i].setx(distancia_x/2)
					correntes_desenho[i].pendown()
					temp.sety(y_abaixo - h_string)
					temp.setx(distancia_x/2 + 6)
					temp.write(str('{:.2f}'.format(round(Tc0[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if Tcf_abaixo[i] != pinchf:
						temp.setx(-distancia_x/2 + nao_toca_pinch - len(str('{:.2f}'.format(round(Tcf_abaixo[i], 2))))*tamanho_string)
						temp.write(str('{:.2f}'.format(round(Tcf_abaixo[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
					if not dividida_fria_abaixo[i]:
						temp.setx(distancia_x/2 + distancia_cp + maior_cp)
						temp.write(str('{:.2f}'.format(round(CPc[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_frio_abaixo[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					else:
						correntes_desenho_sub_abaixo[i] = [0] * (quantidade_fria_abaixo[i] - 1)
						for j in range(quantidade_fria_abaixo[i]-1):
							temp.sety(y_abaixo - h_string)
							temp.setx(distancia_x/2 + distancia_cp + maior_cp)
							temp.write(str('{:.2f}'.format(round(CPc[i]*fracoes_frias_abaixo[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
							temp.write(str('{:.2f}'.format(round(calor_atual_frio_sub_abaixo[i][j], 2))), align="center", font=("Arial", fonte_carga, "normal"))
							correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
							if e_utilidade_fria[i]:
								correntes_desenho_sub_abaixo[i][j].color("#7FFFD4")
							else:
								correntes_desenho_sub_abaixo[i][j].color("blue")
							correntes_desenho_sub_abaixo[i][j].pensize(grossura_corrente)
							correntes_desenho_sub_abaixo[i][j].hideturtle()
							correntes_desenho_sub_abaixo[i][j].penup()
							correntes_desenho_sub_abaixo[i][j].setx(distancia_x/2 - ramo_x)
							correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
							correntes_desenho_sub_abaixo[i][j].pendown()
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(ramo_y)
							correntes_desenho_sub_abaixo[i][j].right(90)
							if Tcf_abaixo[i] == pinchf:
								correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 2*ramo_x)
							else:
								correntes_desenho_sub_abaixo[i][j].forward(distancia_x - nao_toca_pinch - 2*ramo_x)
							correntes_desenho_sub_abaixo[i][j].right(90)
							correntes_desenho_sub_abaixo[i][j].forward(ramo_y*(j+1))
							correntes_desenho_sub_abaixo[i][j].left(90)
							correntes_desenho_sub_abaixo[i][j].forward(ramo_x)
							y_abaixo -= ramo_y
						temp.sety(y_abaixo - h_string)
						temp.setx(distancia_x/2 + distancia_cp + maior_cp)
						temp.write(str('{:.2f}'.format(round(CPc[i]*fracoes_frias_abaixo[i][quantidade_fria_abaixo[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
						temp.setx(distancia_x/2 + distancia_cp + maior_cp*2 + maior_duty)
						temp.write(str('{:.2f}'.format(round(calor_atual_frio_sub_abaixo[i][quantidade_fria_abaixo[i]-1], 2))), align="center", font=("Arial", fonte_carga, "normal"))
					if Tcf_abaixo[i] == pinchf:
						correntes_desenho[i].forward(distancia_x)
					else:
						correntes_desenho[i].forward(distancia_x - nao_toca_pinch)

			if onde != "ambas":
				y_acima -= ramo_y
				y_abaixo -= ramo_y

			if onde == "ambas":
				correntes_desenho[i] = turtle.Turtle()
				correntes_desenho[i].speed(1000)
				correntes_desenho[i].shapesize(seta, seta, seta)
				if e_utilidade_fria[i]:
					correntes_desenho[i].color("#7FFFD4")
				else:
					correntes_desenho[i].color("blue")
				correntes_desenho[i].pensize(grossura_corrente)
				correntes_desenho[i].penup()
				correntes_desenho_sub_acima = [0] * ncold
				correntes_desenho_sub_abaixo = [0] * ncold
				correntes_desenho[i].sety(y_acima)
				correntes_desenho[i].left(180)
				temp.sety(y_acima - h_string)
				temp.setx(-distancia_x/2 - distancia_cp - maior_duty)
				temp.write(str('{:.2f}'.format(round(calor_atual_frio_ev[i], 2))), align="center", font=("Arial", fonte_carga, "normal"))
				temp.setx(-distancia_x/2 - len(str('{:.2f}'.format(round(Tcf[i], 2))))*tamanho_string)
				temp.write(str('{:.2f}'.format(round(Tcf[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
				temp.setx(distancia_x/2 + 6)
				temp.write(str('{:.2f}'.format(round(Tc0[i], 2))), align="left", font=("Arial", fonte_carga, "normal"))
				if dividida_fria_ev_acima[i]:
					correntes_desenho_sub_acima[i] = [0] * (quantidade_fria_ev_acima[i] - 1)
					for j in range(quantidade_fria_ev_acima[i] - 1):
						correntes_desenho_sub_acima[i][j] = turtle.Turtle()
						correntes_desenho_sub_acima[i][j].color("blue")
						correntes_desenho_sub_acima[i][j].pensize(grossura_corrente)
						correntes_desenho_sub_acima[i][j].hideturtle()
						correntes_desenho_sub_acima[i][j].penup()
						correntes_desenho_sub_acima[i][j].sety(y_acima)
						correntes_desenho_sub_acima[i][j].setx(-ramo_x)
						correntes_desenho_sub_acima[i][j].pendown()
						correntes_desenho_sub_acima[i][j].right(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_y)
						correntes_desenho_sub_acima[i][j].right(90)
						if fechar_corrente_ev[i]:
							correntes_desenho_sub_acima[i][j].forward((len(matriz_armazenada)+0.5)*espaco_trocadores)
							temperatura.sety(y_acima + 1)
							temperatura.setx(-(len(matriz_armazenada)+1)*espaco_trocadores + 6)
							temperatura.write(str('{:.2f}'.format(round(temp_misturador_frio[i], 2))), align="center", font=("Arial", fonte_temp, "normal"))
						else:
							correntes_desenho_sub_acima[i][j].forward(distancia_x/2 - 2*ramo_x)
						correntes_desenho_sub_acima[i][j].right(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_y*(j+1))
						correntes_desenho_sub_acima[i][j].left(90)
						correntes_desenho_sub_acima[i][j].forward(ramo_x)
						y_acima -= ramo_y
				if dividida_fria_ev_abaixo[i]:
					correntes_desenho_sub_abaixo[i] = [0] * (quantidade_fria_ev_abaixo[i] - 1)
					for j in range(quantidade_fria_ev_abaixo[i]-1):
						correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
						if e_utilidade_fria[i]:
							correntes_desenho_sub_abaixo[i][j].color("#7FFFD4")
						else:
							correntes_desenho_sub_abaixo[i][j].color("blue")
						correntes_desenho_sub_abaixo[i][j].pensize(grossura_corrente)
						correntes_desenho_sub_abaixo[i][j].hideturtle()
						correntes_desenho_sub_abaixo[i][j].penup()
						correntes_desenho_sub_abaixo[i][j].setx(distancia_x/2 - ramo_x)
						correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
						correntes_desenho_sub_abaixo[i][j].pendown()
						correntes_desenho_sub_abaixo[i][j].right(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_y)
						correntes_desenho_sub_abaixo[i][j].right(90)
						correntes_desenho_sub_abaixo[i][j].forward(distancia_x/2 - 2*ramo_x)
						correntes_desenho_sub_abaixo[i][j].right(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_y*(j+1))
						correntes_desenho_sub_abaixo[i][j].left(90)
						correntes_desenho_sub_abaixo[i][j].forward(ramo_x)
						y_abaixo -= ramo_y
				correntes_desenho[i].setx(distancia_x/2)
				correntes_desenho[i].pendown()
				correntes_desenho[i].forward(distancia_x)

				y_acima -= ramo_y
				y_abaixo -= ramo_y

				if y_acima < y_abaixo:
					y_abaixo = y_acima
				elif y_acima > y_abaixo:
					y_acima = y_abaixo

	def pinch(tamanho, onde):
		pinch = turtle.Turtle()
		pinch.speed(1000)
		pinch.hideturtle()
		pinch.pensize(grossura_pinch)
		pinch.right(90)
		pinch.penup()
		pinch.sety(comecar_pinch)
		if onde == "acima":
			pinch.setx(distancia_x/2 + 2)
			temp.setx(distancia_x/2 + 2)
		elif onde == "abaixo":
			pinch.setx(-distancia_x/2 - 2)
			temp.setx(-distancia_x/2 - 2)
		temp.sety(comecar_pinch + 5)
		temp.write(str('{:.2f}'.format(round(pinchq, 2))), align="center", font=("Arial", fonte_carga, "normal"))
		temp.right(90)
		tamanho = comecar_pinch - tamanho
		if str(tamanho)[-1] == 5:
			tamanho += 5

		for i in range(int(tamanho/8)+1):
			pinch.pendown()
			pinch.forward(4)
			pinch.penup()
			pinch.forward(4)
			temp.forward(8)
		temp.forward(10)
		temp.write(str('{:.2f}'.format(round(pinchf, 2))), align="center", font=("Arial", fonte_carga, "normal"))

	def inserir_trocador_desenho(onde, corrente_quente, corrente_fria, subestagio, trocadorr, trocador_atual, x, duas_temp, viola, anterior):
		trocador = criar_turtle()
		trocador.pensize(grossura_trocador)

		if e_utilidade_quente[trocadorr[0]-1]:
			trocador.color("black", "orange")
		elif e_utilidade_fria[trocadorr[1]-1]:
			trocador.color("black", "#7FFFD4")
		else:
			trocador.color("black", "white")

		y = 1.5
		"""
		QUANDO AMBAS: segue o sentido da corrente
		QUANDO ACIMA OU ABAIXO: pinch -> fora

		ACIMA
		printa sempre temperaturas da direita (tqout e tfin)
		se precisar printar as duas, ai vai as da esquerda (tqin e tfout)

		ABAIXO
		printa sempre temperaturas da esquerda (tqin e tfout)
		se precisar printa as duas, ai vai as da direita (tqout e tfin)
		"""
		if onde[:5] == "ambas":
			tq_in = trocadorr[7]
			tq_out = trocadorr[9]
			tf_in = trocadorr[10]
			tf_out = trocadorr[8]
			distancia_x = 0
			onde_temperatura_q = onde_temperatura_f_in = raio_trocador + 2
			onde_temperatura_q_in = -raio_trocador - len(str('{:.2f}'.format(round(tq_in,2))))*tamanho_string/y
			onde_temperatura_f = -raio_trocador - len(str('{:.2f}'.format(round(tf_out, 2))))*tamanho_string/y
			div_q_acima = dividida_quente_ev_acima
			div_q_abaixo = dividida_quente_ev_abaixo
			div_f_acima = dividida_fria_ev_acima
			div_f_abaixo = dividida_fria_ev_abaixo
		else:
			tq_in = trocadorr[9]
			tq_out = trocadorr[7]
			tf_in = trocadorr[10]
			tf_out = trocadorr[8]
			distancia_x = x
			if onde[6:] == "acima":
				onde_temperatura_q = -raio_trocador - len(str('{:.2f}'.format(round(tq_out, 2))))*tamanho_string/y
				onde_temperatura_f = -raio_trocador - len(str('{:.2f}'.format(round(tf_out, 2))))*tamanho_string/y
				onde_temperatura_q_in = onde_temperatura_f_in = raio_trocador + 2
				div_q_acima = dividida_quente
				div_f_acima = dividida_fria
			elif onde[6:] == "abaixo":
				onde_temperatura_q = onde_temperatura_f = raio_trocador + 2
				onde_temperatura_q_in = -raio_trocador - len(str('{:.2f}'.format(round(tq_in, 2))))*tamanho_string/y
				onde_temperatura_f_in = -raio_trocador - len(str('{:.2f}'.format(round(tf_in, 2))))*tamanho_string/y
				div_q_abaixo = dividida_quente_abaixo
				div_f_abaixo = dividida_fria_abaixo

		if onde[6:] == "acima":
			trocador.setx(distancia_x/2 - subestagio*espaco_trocadores)
			temp.setx(distancia_x/2 - subestagio*espaco_trocadores)
			if div_q_acima[trocadorr[0]-1]:
				trocador.sety(corrente_quente.pos()[1] - raio_trocador - ramo_y*(trocadorr[2]-1))
				temp.sety(corrente_quente.pos()[1] + raio_trocador + carga_trocador - ramo_y*(trocadorr[2]-1))
				temperatura.sety(corrente_quente.pos()[1] - h_string - grossura_corrente - 1 - ramo_y*(trocadorr[2]-1))
				ident.sety(corrente_quente.pos()[1] - raio_trocador/2 - ramo_y*(trocadorr[2]-1))
			else:
				trocador.sety(corrente_quente.pos()[1] - raio_trocador)
				temp.sety(corrente_quente.pos()[1] + raio_trocador + carga_trocador)
				temperatura.sety(corrente_quente.pos()[1] - h_string - grossura_corrente - 1)
				ident.sety(corrente_quente.pos()[1] - raio_trocador/2)
			if onde[:5] == "ambas":
				if viola[1] or anterior[0]:
					temperatura.color("red")
					if viola[3] or anterior[2]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaque = ""
				temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_q)
				temperatura.write(str('{:.2f}'.format(round(tq_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
				if duas_temp[0]:
					if viola[0]:
						temperatura.color("red")
						if viola[2]:
							estilo = "bold"
							destaque = "**"
						else:
							estilo = "normal"
							destaque = ""
					else:
						temperatura.color("black")
						estilo = "normal"
						destaque = ""
					temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_q_in)
					temperatura.write(str('{:.2f}'.format(round(tq_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			else:
				if anterior[0] or viola[1]:
					temperatura.color("red")
					if anterior[2] or viola[3]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaque = ""
				temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_q_in)
				temperatura.write(str('{:.2f}'.format(round(tq_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
				if duas_temp[0]:
					if viola[0]:
						temperatura.color("red")
						if viola[2]:
							estilo = "bold"
							destaque = "**"
						else:
							estilo = "normal"
							destaque = ""
					else:
						temperatura.color("black")
						estilo = "normal"
						destaque = ""
					temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_q)
					temperatura.write(str('{:.2f}'.format(round(tq_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			trocador.pendown()
			trocador.begin_fill()
			trocador.circle(raio_trocador)
			trocador.end_fill()
			ident.setx(distancia_x/2 - subestagio*espaco_trocadores + 1)
			ident.write("E" + str(trocador_atual), align="center", font=("Arial", fonte_carga, "bold"))
			if div_f_acima[trocadorr[1]-1]:
				trocador.sety(corrente_fria.pos()[1] - raio_trocador - ramo_y*(trocadorr[3]-1))
				temperatura.sety(corrente_fria.pos()[1] - h_string - grossura_corrente - 1 - ramo_y*(trocadorr[3]-1))
				ident.sety(corrente_fria.pos()[1] - raio_trocador/2 - ramo_y*(trocadorr[3]-1))
			else:
				trocador.sety(corrente_fria.pos()[1] - raio_trocador)
				temperatura.sety(corrente_fria.pos()[1] - h_string - grossura_corrente - 1)
				ident.sety(corrente_fria.pos()[1] - raio_trocador/2)
			if anterior[1] or viola[1]:
				temperatura.color("red")
				if anterior[3] or viola[3]:
					estilo = "bold"
					destaque = "**"
				else:
					estilo = "normal"
					destaque = ""
			else:
				temperatura.color("black")
				estilo = "normal"
				destaque = ""
			temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_f_in)
			temperatura.write(str('{:.2f}'.format(round(tf_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			if duas_temp[1]:
				if viola[0]:
					temperatura.color("red")
					if viola[2]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaque = ""
				temperatura.setx(distancia_x/2 - subestagio*espaco_trocadores + onde_temperatura_f)
				temperatura.write(str('{:.2f}'.format(round(tf_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			trocador.begin_fill()
			trocador.circle(raio_trocador)
			trocador.end_fill()
			ident.write("E" + str(trocador_atual), align="center", font=("Arial", fonte_carga, "bold"))
		elif onde[6:] == "abaixo":
			trocador.setx(-distancia_x/2 + subestagio*espaco_trocadores)
			temp.setx(-distancia_x/2 + subestagio*espaco_trocadores)
			if div_q_abaixo[trocadorr[0]-1]:
				trocador.sety(corrente_quente.pos()[1] - raio_trocador - ramo_y*(trocadorr[2]-1))
				temp.sety(corrente_quente.pos()[1] + raio_trocador + carga_trocador - ramo_y*(trocadorr[2]-1))
				temperatura.sety(corrente_quente.pos()[1] - h_string - grossura_corrente - 1 - ramo_y*(trocadorr[2]-1))
				ident.sety(corrente_quente.pos()[1] - raio_trocador/2 - ramo_y*(trocadorr[2]-1))
			else:
				trocador.sety(corrente_quente.pos()[1] - raio_trocador)
				temp.sety(corrente_quente.pos()[1] + raio_trocador + carga_trocador)
				temperatura.sety(corrente_quente.pos()[1] - h_string - grossura_corrente - 1)
				ident.sety(corrente_quente.pos()[1] - raio_trocador/2)
			if anterior[0] or viola[0]:
				temperatura.color("red")
				if anterior[1] or viola[1]:
					estilo = "bold"
					destaque = "**"
				else:
					estilo = "normal"
					destaque = ""
			else:
				temperatura.color("black")
				estilo = "normal"
				destaque = ""
			temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_q_in)
			temperatura.write(str('{:.2f}'.format(round(tq_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			if duas_temp[0]:
				if viola[1]:
					temperatura.color("red")
					if viola[3]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaque = ""
				temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_q)
				temperatura.write(str('{:.2f}'.format(round(tq_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			trocador.pendown()
			trocador.begin_fill()
			trocador.circle(raio_trocador)
			trocador.end_fill()
			ident.setx(-distancia_x/2 + subestagio*espaco_trocadores + 1)
			ident.write("E" + str(trocador_atual), align="center", font=("Arial", fonte_carga, "bold"))
			if div_f_abaixo[trocadorr[1]-1]:
				trocador.sety(corrente_fria.pos()[1] - raio_trocador - ramo_y*(trocadorr[3]-1))
				temperatura.sety(corrente_fria.pos()[1] - h_string - grossura_corrente - 1 - ramo_y*(trocadorr[3]-1))
				ident.sety(corrente_fria.pos()[1] - raio_trocador/2 - ramo_y*(trocadorr[3] - 1))
			else:
				trocador.sety(corrente_fria.pos()[1] - raio_trocador)
				temperatura.sety(corrente_fria.pos()[1] - h_string - grossura_corrente - 1 - ramo_y*(trocadorr[3]-1))
				ident.sety(corrente_fria.pos()[1] - raio_trocador/2)
			if onde[:5] == "ambas":
				if anterior[1] or viola[0]:
					temperatura.color("red")
					if anterior[3] or viola[1]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaeu = ""
				temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_f)
				temperatura.write(str('{:.2f}'.format(round(tf_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
				if duas_temp[1]:
					if viola[1]:
						temperatura.color("red")
						if viola[3]:
							estilo = "bold"
							destaque = "**"
						else:
							estilo = "normal"
							destaque = ""
					else:
						temperatura.color("black")
						estilo = "normal"
						destaque = ""
					temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_f_in)
					temperatura.write(str('{:.2f}'.format(round(tf_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			else:
				if anterior[1] or viola[0]:
					temperatura.color("red")
					if anterior[3] or viola[2]:
						estilo = "bold"
						destaque = "**"
					else:
						estilo = "normal"
						destaque = ""
				else:
					temperatura.color("black")
					estilo = "normal"
					destaque = ""
				temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_f_in)
				temperatura.write(str('{:.2f}'.format(round(tf_in, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
				if duas_temp[1]:
					if viola[1]:
						temperatura.color("red")
						if viola[3]:
							estilo = "bold"
							destaque = "**"
						else:
							estilo = "normal"
							destaque = ""
					else:
						temperatura.color("black")
						estilo = "normal"
						destaque = ""
					temperatura.setx(-distancia_x/2 + subestagio*espaco_trocadores + onde_temperatura_f)
					temperatura.write(str('{:.2f}'.format(round(tf_out, 2))) + destaque, align="left", font=("Arial", fonte_temp, estilo))
			trocador.begin_fill()
			trocador.circle(raio_trocador)
			trocador.end_fill()
			ident.write("E" + str(trocador_atual), align="center", font=("Arial", fonte_carga, "bold"))

		temp.write(str('{:.2f}'.format(round(trocadorr[6], 2))), align="center", font=("Arial", fonte_carga, "bold"))

	def utilidade_desenho(onde, corrente, subestagio, calor, primeiro, utilidade_atual, x):
		utilidade = criar_turtle()
		utilidade.pensize(grossura_trocador)
		if onde[:5] == "ambas":
			distancia_x = 0
		else:
			distancia_x = x
		if onde[6:] == "acima":
			utilidade.color("black", "orange")
			if primeiro == 0:
				utilidade.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores)
				temp.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores)
				ident.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores + 1)
			else:
				utilidade.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores + primeiro*espaco_utilidades)
				temp.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores + primeiro*espaco_utilidades)
				ident.setx(distancia_x/2 - (subestagio+0.5)*espaco_trocadores + primeiro*espaco_utilidades + 1)
		elif onde[6:] == "abaixo":
			utilidade.color("black", "#7FFFD4")
			if primeiro == 0:
				utilidade.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores)
				temp.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores)
				ident.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores + 1)
			else:
				utilidade.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores - primeiro*espaco_utilidades)
				temp.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores - primeiro*espaco_utilidades)
				ident.setx(-distancia_x/2 + (subestagio+0.5)*espaco_trocadores - primeiro*espaco_utilidades + 1)
		utilidade.sety(corrente.pos()[1] - raio_trocador)
		utilidade.pendown()
		utilidade.begin_fill()
		utilidade.circle(raio_trocador)
		utilidade.end_fill()
		temp.sety(corrente.pos()[1] + raio_trocador)
		temp.write(str('{:.2f}'.format(round(calor, 2))), align="center", font=("Arial", fonte_carga, "bold"))
		ident.sety(corrente.pos()[1] - raio_trocador/2)
		if onde[6:] == "acima":
			ident.write("H" + str(utilidade_atual), align="center", font=("Arial", fonte_carga, "bold"))
		if onde[6:] == "abaixo":
			ident.write("C" + str(utilidade_atual), align="center", font=("Arial", fonte_carga, "bold"))

	def legenda(onde_comecar, unidades):
		trocador = turtle.Turtle()
		trocador.hideturtle()
		trocador.color("black", "white")
		trocador.pensize(grossura_corrente)
		trocador.penup()
		trocador.speed(1000)

		corrente = turtle.Turtle()
		corrente.pensize(grossura_corrente)
		corrente.penup()
		corrente.speed(1000)

		texto = turtle.Turtle()
		texto.hideturtle()
		texto.penup()
		texto.speed(1000)

		legenda = turtle.Turtle()
		legenda.hideturtle()
		legenda.pensize(grossura_pinch)
		legenda.penup()
		legenda.speed(1000)


		legenda_comeco_corrente = onde_comecar[0]
		legenda_trocador = onde_comecar[0] + 150
		legenda_raio_trocador = 30
		caixa_horizontal = 300 + len("temperature")*4*2 + 80
		caixa_vertical = legenda_raio_trocador*2 + 100

		legenda.sety(onde_comecar[1] + caixa_vertical/2)
		legenda.setx(onde_comecar[0] - len("temperature")*4 - 40)
		legenda.pendown()
		for i in range(2):
			legenda.forward(caixa_horizontal)
			legenda.right(90)
			legenda.forward(caixa_vertical)
			legenda.right(90)


		corrente.setx(legenda_comeco_corrente)
		corrente.sety(onde_comecar[1])
		corrente.pendown()
		corrente.forward(300)
		trocador.setx(legenda_trocador)
		trocador.sety(corrente.pos()[1] - legenda_raio_trocador)
		trocador.pendown()
		trocador.begin_fill()
		trocador.circle(legenda_raio_trocador)
		trocador.end_fill()
		texto.setx(trocador.pos()[0])
		texto.sety(corrente.pos()[1] + legenda_raio_trocador + 5)
		if unidades[1] == "kW/K":
			texto.write("HEAT LOAD ({})".format(unidades[1][:2]), align="center", font=("Arial", fonte_carga, "bold"))
		else:
			texto.write("HEAT LOAD ({})".format(unidades[1][:3]), align="center", font=("Arial", fonte_carga, "bold"))
		texto.sety(corrente.pos()[1] + legenda_raio_trocador + 20)
		texto.write("LEGEND", align="center", font=("Arial", 14, "bold"))
		legenda.penup()
		legenda.sety(texto.pos()[1] - 2)
		legenda.setx(texto.pos()[0] + len("subtitle")*5)
		legenda.pendown()
		legenda.setx(texto.pos()[0] - len("subtitle")*5)

		texto.setx(trocador.pos()[0] - legenda_raio_trocador - len("temperature")*2.75)
		texto.sety(corrente.pos()[1] - 14)
		texto.write("Inlet", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(corrente.pos()[1] - 24)
		texto.write("Temperature", align="center", font=("Arial", fonte_carga, "normal"))
		texto.setx(trocador.pos()[0] + legenda_raio_trocador + len("temperature")*2.90)
		texto.write("Temperature", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(corrente.pos()[1] - 14)
		texto.write("Outlet", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(corrente.pos()[1] + 2)
		texto.setx(legenda_comeco_corrente - len("temperature")*4)
		texto.write("Supply", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(corrente.pos()[1] - 14)
		texto.write("Temperature", align="center", font=("Arial", fonte_carga, "normal"))
		texto.setx(len("temperature")*4 + corrente.pos()[0])
		texto.sety(corrente.pos()[1] + 2)
		texto.write("Target", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(corrente.pos()[1] - 14)
		texto.write("Temperature", align="center", font=("Arial", fonte_carga, "normal"))
		texto.sety(trocador.pos()[1] - 40)
		texto.setx(legenda_trocador)
		texto.write("UNITS:   Temperature: {};   CP = {}".format(unidades[0], unidades[1]), align="center", font=("Arial", fonte_carga, "bold"))

	global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo, distancia_x, ramo_x, ramo_y, nao_toca_pinch, espaco_trocadores, comecar_pinch, raio_trocador, espaco_utilidades, distancia_cp, maior_cp
	global tamanho_antigo, tamanho_antigo_acima, tamanho_antigo_abaixo

	if True:
		turtle.TurtleScreen._RUNNING=True
		turtle.delay(0)
		turtle.tracer(0, 0)
		turtle.hideturtle()
		turtle.speed("fastest")
		turtle.hideturtle()
		temp = criar_turtle() #CP, supply/target, heat load
		temperatura = criar_turtle() #temps de troca
		ident = criar_turtle() #E1 C1 H1 hot 1 cold 1


		#obtendo arbitrarias
		tamanho_string = 2.5
		tamanhos = []
		temps = Th0 + Thf + Tc0 + Tcf
		for i in range(len(temps)):
			tamanhos.append(len(str('{:.2f}'.format(round(temps[i], 2))))*tamanho_string)
		cps = CPh + CPc

		#strings
		h_string = 2
		fonte_carga = 4
		fonte_temp = 3

		#setas e trocadores
		raio_trocador = 4.2
		grossura_corrente = 0.75
		grossura_pinch = 0.5
		grossura_trocador = 0.5
		seta = 0.4

		#espaçamentos
		carga_trocador = 0
		ramo_x = 10
		ramo_y = 3*raio_trocador + h_string
		borda = 100
		espaco_trocadores = max(tamanhos) + 5
		espaco_utilidades = espaco_trocadores/2
		nao_toca_pinch = max(tamanhos) + 5
		distancia_cp = nao_toca_pinch + 20
		maior_cp = len("Streams CP ({})".format(unidades_usadas[1]))*tamanho_string/2
		maior_duty = len("Streams Duty ({})".format(unidades_usadas[2]))*tamanho_string/2


		x = 150
		#tamanho das setas
		if subrede == "acima":
			distancia_x = espaco_trocadores * (len(matriz_armazenada) + len(utilidades) + 2)
			if distancia_x < x:
				distancia_x = x
		elif subrede == "abaixo":
			distancia_x = espaco_trocadores * (len(matriz_trocadores_abaixo) + len(utilidades_abaixo) + 2)
			if distancia_x < x:
				distancia_x = x
		elif subrede == "ambas":
			acima = abaixo = 0
			for trocador in matriz_evolucao:
				if trocador[5] == 1:
					acima += 1
				if trocador[5] == 2:
					abaixo += 1
			distancia_x = espaco_trocadores * 2 * (max(acima, abaixo) + 1)
			if distancia_x < 2*x:
				distancia_x = 2*x

		#tamanho da janela
		if subrede == "ambas":
			w = distancia_x + distancia_cp + maior_duty*2 + len("Cold 99 (utility)")*tamanho_string + borda
		else:
			w = distancia_x + 1.5*distancia_cp + maior_cp*2 + maior_duty*2 + borda + len("Cold 99 (utility)")*tamanho_string

		h = 0
		h_acima = 0
		h_abaixo = 0

		if subrede != "ambas":
			for i in range(len(correntes_quentes)):
				h_acima += ramo_y * quantidade_quente[i]
				h_abaixo += ramo_y * quantidade_quente_abaixo[i]

			for i in range(len(correntes_frias)):
				h_acima += ramo_y * quantidade_fria[i]
				h_abaixo += ramo_y * quantidade_fria_abaixo[i]
		else:
			for i in range(len(correntes_quentes)):
				h += ramo_y * max(quantidade_quente_ev_acima[i], quantidade_quente_ev_abaixo[i])
			for j in range(len(correntes_frias)):
				h += ramo_y * max(quantidade_fria_ev_acima[j], quantidade_fria_ev_abaixo[j])

		if subrede == "acima":
			y_acima, y_abaixo = h_acima/2, h_acima/2
			turtle.setup(width=w, height=1.5*h_acima + 35)
			h = 1.5*h_acima + 35
		elif subrede == "abaixo":
			y_acima, y_abaixo = h_abaixo/2, h_abaixo/2
			turtle.setup(width=w, height=1.5*h_abaixo + 35)
			h = 1.5*h_abaixo + 35
		elif subrede == "ambas":
			y_acima, y_abaixo = h/2, h/2
			turtle.setup(width=w, height=1.5*h)

		y_acima_f, y_abaixo_f = y_acima, y_abaixo
		comecar_pinch = y_acima + ramo_y

		if subrede == "acima":
			tamanho_antigo_acima = [w, h]
			quentes("above", correntes_quentes, corrente_quente_presente_acima)
			frias("above", correntes_frias, corrente_fria_presente_acima)
			pinch(y_acima, "acima")

			trocador_atual = 1

			if len(matriz_armazenada) > 0:
				subestagio = 1
				for trocadorr in matriz_armazenada:
					subestagio += 1
					duas_temp_quente = True
					duas_temp_fria = True
					viola_quente, viola_frio = False, False
					termo_quente, termo_frio = False, False
					viola_anterior_quente, viola_anterior_fria = False, False
					if trocadorr[7] - trocadorr[8] < dTmin:
						viola_quente = True
						if trocadorr[7] - trocadorr[8] < 0:
							termo_quente = True
					if trocadorr[9] - trocadorr[10] < dTmin:
						viola_frio = True
						if trocadorr[9] - trocadorr[10] < 0:
							termo_frio = True
					try:
						if matriz_armazenada[matriz_armazenada.index(trocadorr)+1][0] == trocadorr[0] and matriz_armazenada[matriz_armazenada.index(trocadorr)+1][2] == trocadorr[2]:
							duas_temp_quente = False
						if matriz_armazenada[matriz_armazenada.index(trocadorr)+1][1] == trocadorr[1] and matriz_armazenada[matriz_armazenada.index(trocadorr)+1][3] == trocadorr[3]:
							duas_temp_fria = False
					except:
						pass
					try:
						termo, termo_quente_anterior, termo_fria_anterior = False, False, False
						if (matriz_armazenada[matriz_armazenada.index(trocadorr)-1][7] - matriz_armazenada[matriz_armazenada.index(trocadorr)-1][8]) < dTmin and matriz_armazenada.index(trocadorr) != 0:
							if (matriz_armazenada[matriz_armazenada.index(trocadorr)-1][7] - matriz_armazenada[matriz_armazenada.index(trocadorr)-1][8]) < 0 and matriz_armazenada.index(trocadorr) != 0:
								termo = True
							if matriz_armazenada[matriz_armazenada.index(trocadorr)-1][0] == trocadorr[0] and matriz_armazenada[matriz_armazenada.index(trocadorr)-1][2] == trocadorr[2]:
								viola_anterior_quente = True
								if termo:
									termo_quente_anterior = True
							if matriz_armazenada[matriz_armazenada.index(trocadorr)-1][1] == trocadorr[1] and matriz_armazenada[matriz_armazenada.index(trocadorr)-1][3] == trocadorr[3]:
								viola_anterior_fria = True
								if termo:
									termo_fria_anterior = True
					except:
						pass
					inserir_trocador_desenho("123456acima", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr, trocador_atual, distancia_x, [duas_temp_quente, duas_temp_fria], [viola_quente, viola_frio, termo_quente, termo_frio], [viola_anterior_quente, viola_anterior_fria, termo_fria_anterior, termo_quente_anterior])
					trocador_atual += 1

				if len(utilidades) > 0:
					primeiro = 0
					util = 1
					for utilidadee in utilidades:
						subestagio += 1
						utilidade_desenho("123456acima", correntes_frias[utilidadee[0]-1], subestagio, utilidadee[1], primeiro, util, distancia_x)
						primeiro += 1
						util += 1


		elif subrede == "abaixo":
			tamanho_antigo_abaixo = [w, h]
			quentes("below", correntes_quentes, corrente_quente_presente_abaixo)
			frias("below", correntes_frias, corrente_fria_presente_abaixo)
			pinch(y_abaixo, "abaixo")

			trocador_atual = 1

			if len(matriz_trocadores_abaixo) > 0:
				subestagio = 1
				for trocadorr in matriz_trocadores_abaixo:
					subestagio += 1
					duas_temp_quente = True
					duas_temp_fria = True
					viola_quente, viola_frio = False, False
					termo_quente, termo_frio = False, False
					viola_anterior_quente, viola_anterior_fria = False, False
					if trocadorr[7] - trocadorr[8] < dTmin:
						viola_frio = True
						if trocadorr[7] - trocadorr[8] < 0:
							termo_frio = True
					if trocadorr[9] - trocadorr[10] < dTmin:
						viola_quente = True
						if trocadorr[9] - trocadorr[10] < 0:
							termo_quente = True
					try:
						if matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)+1][0] == trocadorr[0] and matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)+1][2] == trocadorr[2]:
							duas_temp_quente = False
						if matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)+1][1] == trocadorr[1] and matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)+1][3] == trocadorr[3]:
							duas_temp_fria = False
					except:
						pass
					try:
						termo = termo_quente_anterior = termo_fria_anterior = False
						if (matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][7] - matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][8]) < dTmin and matriz_trocadores_abaixo.index(trocadorr) != 0:
							if (matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][7] - matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][8]) < 0 and matriz_trocadores_abaixo.index(trocadorr) != 0:
								termo = True
							if matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][0] == trocadorr[0] and matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][2] == trocadorr[2]:
								viola_anterior_quente = True
								if termo:
									termo_quente_anterior = True
							if matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][1] == trocadorr[1] and matriz_trocadores_abaixo[matriz_trocadores_abaixo.index(trocadorr)-1][3] == trocadorr[3]:
								viola_anterior_fria = True
								if termo:
									termo_fria_anterior = True
					except:
						pass
					inserir_trocador_desenho("123456abaixo", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr, trocador_atual, distancia_x, [duas_temp_quente, duas_temp_fria], [viola_quente, viola_frio, termo_quente, termo_frio], [viola_anterior_quente, viola_anterior_fria, termo_quente_anterior, termo_fria_anterior])
					trocador_atual += 1

				if len(utilidades_abaixo) > 0:
					primeiro = 0
					util = 1
					for utilidadee in utilidades_abaixo:
						subestagio += 1
						utilidade_desenho("123456abaixo", correntes_quentes[utilidadee[0]-1], subestagio, utilidadee[1], primeiro, util, distancia_x)
						primeiro += 1
						util += 1
		elif subrede == "ambas":
			tamanho_antigo = [w, h]
			quentes("ambas", correntes_quentes, corrente_quente_presente_acima)
			frias("ambas", correntes_frias, corrente_fria_presente_acima)

			trocador_atual = 1
			if len(matriz_evolucao) > 0:
				subestagio = 0
				subestagio_abaixo = 0
				for trocadorr in matriz_evolucao:
					if trocadorr[5] == 1:
						subestagio += 1
						duas_temp_quente = True
						duas_temp_fria = True
						viola_quente, viola_frio = False, False
						termo_quente, termo_frio = False, False
						viola_anterior_quente, viola_anterior_fria = False, False
						if trocadorr[7] - trocadorr[8] < dTmin:
							viola_quente = True
							if trocadorr[7] - trocadorr[8] < 0:
								termo_quente = True
						if trocadorr[9] - trocadorr[10] < dTmin:
							viola_frio = True
							if trocadorr[9] - trocadorr[10] < 0:
								termo_frio = True
						try:
							if matriz_evolucao[matriz_evolucao.index(trocadorr)+1][0] == trocadorr[0] and matriz_evolucao[matriz_evolucao.index(trocadorr)+1][2] == trocadorr[2]:
								duas_temp_quente = False
							if matriz_evolucao[matriz_evolucao.index(trocadorr)+1][1] == trocadorr[1] and matriz_evolucao[matriz_evolucao.index(trocadorr)+1][3] == trocadorr[3]:
								duas_temp_fria = False
							if matriz_evolucao[matriz_evolucao.index(trocadorr)+1][5] == 2:
								duas_temp_quente = True
								duas_temp_fria = True
						except:
							pass
						try:
							termo, termo_quente_anterior, termo_fria_anterior = False, False, False
							if (matriz_evolucao[matriz_evolucao.index(trocadorr)-1][7] - matriz_evolucao[matriz_evolucao.index(trocadorr)-1][8]) < dTmin and matriz_evolucao.index(trocadorr) != 0:
								if (matriz_evolucao[matriz_evolucao.index(trocadorr)-1][7] - matriz_evolucao[matriz_evolucao.index(trocadorr)-1][8]) < 0 and matriz_evolucao.index(trocadorr) != 0:
									termo = True
								if matriz_evolucao[matriz_evolucao.index(trocadorr)-1][0] == trocadorr[0] and matriz_evolucao[matriz_evolucao.index(trocadorr)-1][2] == trocadorr[2]:
									viola_anterior_quente = True
									if termo:
										termo_quente_anterior = True
								if matriz_evolucao[matriz_evolucao.index(trocadorr)-1][1] == trocadorr[1] and matriz_evolucao[matriz_evolucao.index(trocadorr)-1][3] == trocadorr[3]:
									viola_anterior_fria = True
									if termo:
										termo_fria_anterior = True
						except:
							pass
						inserir_trocador_desenho("ambas/acima", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio, trocadorr, trocador_atual, distancia_x, [duas_temp_quente, duas_temp_fria], [viola_quente, viola_frio, termo_quente, termo_frio], [viola_anterior_quente, viola_anterior_fria, termo_quente_anterior, termo_fria_anterior])
					elif trocadorr[5] == 2:
						subestagio_abaixo += 1
						duas_temp_quente = True
						duas_temp_fria = True
						viola_quente, viola_frio = False, False
						termo_quente, termo_frio = False, False
						viola_anterior_quente, viola_anterior_fria = False, False
						if trocadorr[7] - trocadorr[8] < dTmin:
							viola_quente = True
							if trocadorr[7] - trocadorr[8] < 0:
								termo_quente = True
						if trocadorr[9] - trocadorr[10] < dTmin:
							viola_frio = True
							if trocadorr[9] - trocadorr[10] < 0:
								termo_frio = True

						try:
							if matriz_evolucao[matriz_evolucao.index(trocadorr)+1][0] == trocadorr[0] and matriz_evolucao[matriz_evolucao.index(trocadorr)+1][2] == trocadorr[2]:
								duas_temp_quente = False
							if matriz_evolucao[matriz_evolucao.index(trocadorr)+1][1] == trocadorr[1] and matriz_evolucao[matriz_evolucao.index(trocadorr)+1][3] == trocadorr[3]:
								duas_temp_fria = False
						except:
							pass
						try:
							termo, termo_quente_anterior, termo_fria_anterior = False, False, False
							if (matriz_evolucao[matriz_evolucao.index(trocadorr)-1][9] - matriz_evolucao[matriz_evolucao.index(trocadorr)-1][10]) < dTmin:
								if (matriz_evolucao[matriz_evolucao.index(trocadorr)-1][9] - matriz_evolucao[matriz_evolucao.index(trocadorr)-1][10]) < 0:
									termo = True
								if matriz_evolucao[matriz_evolucao.index(trocadorr)-1][0] == trocadorr[0] and matriz_evolucao[matriz_evolucao.index(trocadorr)-1][2] == trocadorr[2]:
									viola_anterior_quente = True
									if termo:
										termo_quente_anterior = True
								if matriz_evolucao[matriz_evolucao.index(trocadorr)-1][1] == trocadorr[1] and matriz_evolucao[matriz_evolucao.index(trocadorr)-1][3] == trocadorr[3]:
									viola_anterior_fria = True
									if termo:
										termo_fria_anterior = True
						except:
							pass
						if matriz_evolucao[matriz_evolucao.index(trocadorr)-1][5] == 1:
							viola_anterior_quente = False
							viola_anterior_frio = False
							termo_quente_anterior = False
							termo_fria_anterior = False
						inserir_trocador_desenho("ambas/abaixo", correntes_quentes[trocadorr[0]-1], correntes_frias[trocadorr[1]-1], subestagio_abaixo, trocadorr, trocador_atual, distancia_x, [duas_temp_quente, duas_temp_fria], [viola_quente, viola_frio, termo_quente, termo_frio], [viola_anterior_quente, viola_anterior_fria, termo_quente_anterior, termo_fria_anterior])
					trocador_atual += 1


		turtle.update()
	else:
		if subrede == "acima":
			w = tamanho_antigo_acima[0]
			h = tamanho_antigo_acima[1]
		elif subrede == "abaixo":
			w = tamanho_antigo_abaixo[0]
			h = tamanho_antigo_abaixo[1]
		else:
			w = tamanho_antigo[0]
			h = tamanho_antigo[1]

	salvar_rede(subredes, subrede, desenha, [w, h], ensure)

def salvar_rede(subredes, onde, salva, tamanho, ensure):
	if salva:
		turtle.getscreen()
		turtle.getcanvas().postscript(file = (onde + ".eps"))
		turtle.bye()
		# turtle.done()
		TARGET_BOUNDS = [tamanho[0]*3, tamanho[1]*3]
		# TARGET_BOUNDS = [tamanho[0], tamanho[1]]
		if TARGET_BOUNDS[0] < 1280:
			TARGET_BOUNDS[0] = 1280
		if TARGET_BOUNDS[1] < 1280:
			TARGET_BOUNDS[1] = 1280
		TARGET_BOUNDS[0] = max(TARGET_BOUNDS)
		TARGET_BOUNDS[1] = TARGET_BOUNDS[0]
		pic = Image.open(onde + '.eps')
		pic.load(scale=10)
		if pic.mode in ('P', '1'):
			pic = pic.convert("RGB")
		ratio = min(TARGET_BOUNDS[0] / pic.size[0],
					TARGET_BOUNDS[1] / pic.size[1])
		new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))
		tamanho = [int(pic.size[0]*ratio), int(pic.size[1]*ratio)]
		pic = pic.resize(new_size, Image.ANTIALIAS)
		if onde == "acima":
			imagem = pic.crop((0, 0, pic.size[0] - 200, pic.size[1]))
		elif onde == "abaixo":
			imagem = pic.crop((200, 0, pic.size[0], pic.size[1]))
		else:
			imagem = pic

		imagem.save(onde + ".png")
		pic.close()
		imagem.close()

	dlg.rede = QPixmap(onde + ".png")
	if not subredes:#atualizando evolução
		dlg.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
		dlg.label_teste.setPixmap(dlg.rede)
		dlg.ambasScroll.setWidgetResizable(True)
		dlg.tabWidget.setCurrentIndex(4)
		if ensure:
			dlg.ambasScroll.ensureVisible(int(tamanho[0]/2), 0, 10, 10)
	else:#subredes
		if onde == "acima":
			dlg.lay_acima.setContentsMargins(0, 0, 0, 0)
			dlg.hen_acima.setPixmap(QtGui.QPixmap(onde + ".png"))
		if onde == "abaixo":
			dlg.lay_abaixo.setContentsMargins(0, 0, 0, 0)
			dlg.hen_abaixo.setPixmap(QtGui.QPixmap(onde + ".png"))

def vai():
	global scroll_acima, scroll_abaixo, wid_acima, wid_abaixo, wid_ambas

	wid_acima = wid_zoom([10000, 10000], "acima")
	dlg.hen_acima.addWidget(wid_acima)
	wid_abaixo = wid_zoom([10000, 10000], "abaixo")
	dlg.hen_abaixo.addWidget(wid_abaixo)

class Desenho(QWidget):
	def __init__(self, tamanho, subrede):
		super().__init__()
		self.tamanho = tamanho
		self.subrede = subrede

		self.w = 0
		self.h = 0

	def paintEvent(self, event):
		def corrente(painter, tipo, id, dividida, quantidade, comeco, fim, dados, toca):

			if tipo == "quente":
				painter.setPen(QPen(QColor("red"), grossura_seta, Qt.SolidLine))
				ponta = -valor
				ramos = 1
				localizacao = localizacao_quente
				if dividida and self.subrede != "ambas":
					dados[3] = dutyq_sub[id]
					fracoes = fracoesq[id]
				texto = "Hot " + str(id+1)
				if self.subrede == "acima":
					tin = comeco[0] - maior_temp - 2*espaco
					iden = fim[0] + 2*espaco
					if not toca:
						fim[0] -= (maior_temp + espaco)
						lugar = fim[0] + 5
				elif self.subrede == "abaixo":
					tin = fim[0] + espaco
					iden = comeco[0] - 2*espaco - int(len(texto)*w_string)
					if not toca:
						comeco[0] += (maior_temp + espaco)
						lugar = int(comeco[0] - len(dados[2])*w_string - espaco/2)
				elif self.subrede == "ambas":
					tin = comeco[0] - maior_temp - 2*espaco
					iden = fim[0] + maior_temp + 5*espaco
					lugar = fim[0] + espaco
			elif tipo == "fria":
				painter.setPen(QPen(QColor("blue"), grossura_seta, Qt.SolidLine))
				ponta = valor
				ramos = -1
				localizacao = localizacao_fria
				if dividida and self.subrede != "ambas":
					dados[3] = dutyf_sub[id]
					fracoes = fracoesf[id]
				texto = "Cold " + str(id+1)
				if self.subrede == "acima":
					tin = fim[0] - maior_temp - 2*espaco
					iden = comeco[0] + 2*espaco
					if not toca:
						comeco[0] -= (maior_temp + espaco)
						lugar = comeco[0] + 5
				elif self.subrede == "abaixo":
					tin = comeco[0] + espaco
					iden = fim[0] - 2*espaco - int(len(texto)*w_string)
					if not toca:
						fim[0] += (maior_temp + espaco)
						lugar = int(fim[0] - len(dados[2])*w_string - espaco/2)
				elif self.subrede == "ambas":
					tin = comeco[0] + espaco
					iden = comeco[0] + maior_temp + 5*espaco
					lugar = fim[0] - maior_temp - 2*espaco
			elif tipo == "quenteutil":
				painter.setPen(QPen(QColor("orange"), grossura_seta, Qt.SolidLine))
				ponta = -valor
				ramos = 1
				localizacao = localizacao_quente
				if dividida and self.subrede != "ambas":
					dados[3] = dutyq_sub[id]
					fracoes = fracoesq[id]
				if self.subrede == "acima":
					tin = comeco[0] - maior_temp - 2*espaco
					iden = fim[0] + 2*espaco
					texto = "Hot " + str(id+1) + " (utility)"
					if not toca:
						fim[0] -= (maior_temp + espaco)
						lugar = fim[0] + 5
				elif self.subrede == "abaixo":
					tin = fim[0] + espaco
					texto = "(utility) Hot " + str(id+1)
					iden = comeco[0] - 2*espaco - int(len(texto)*w_string)
					if not toca:
						comeco[0] += (maior_temp + espaco)
						lugar = int(comeco[0] - len(dados[2])*w_string - espaco/2)
				elif self.subrede == "ambas":
					tin = comeco[0] - maior_temp - 2*espaco
					iden = fim[0] + maior_temp + 5*espaco
					lugar = fim[0] + espaco
					texto = "Hot " + str(id+1) + " (utility)"
			elif tipo == "friautil":
				painter.setPen(QPen(QColor("cyan"), grossura_seta, Qt.SolidLine))
				ponta = valor
				ramos = -1
				localizacao = localizacao_fria
				if dividida and self.subrede != "ambas":
					dados[3] = dutyf_sub[id]
					fracoes = fracoesf[id]
				if self.subrede == "acima":
					tin = fim[0] - maior_temp - 2*espaco
					texto = "Cold " + str(id+1) + " (utility)"
					iden = comeco[0] + 2*espaco
					if not toca:
						comeco[0] -= (maior_temp + espaco)
						lugar = comeco[0] + 5
				elif self.subrede == "abaixo":
					tin = comeco[0] + espaco
					texto = "(utility) Cold " + str(id+1)
					iden = fim[0] - 2*espaco - int(len(texto)*w_string)
					if not toca:
						fim[0] += (maior_temp + espaco)
						lugar = int(fim[0] - len(dados[2])*w_string - espaco/2)
				elif self.subrede == "ambas":
					tin = comeco[0] + espaco
					iden = comeco[0] + maior_temp + 5*espaco
					lugar = fim[0] - maior_temp - 2*espaco
					texto = "Cold " + str(id+1) + " (utility)"
			elif tipo == "quentefora":
				painter.setPen(QPen(QColor("white"), grossura_seta, Qt.SolidLine))
				ponta = -valor
				ramos = 1
				localizacao = localizacao_quente
				tin = comeco[0] - maior_temp - espaco
				if dividida and self.subrede != "ambas":
					dados[3] = dutyq_sub[id]
					fracoes = fracoesq[id]
				if e_utilidade_quente_a[id]:
					if self.subrede == "acima":
						texto = "Hot " + str(id+1) + " (utility)"
					elif self.subrede == "abaixo":
						texto = "(utility) Hot " + str(id+1)
				else:
					texto = "Hot " + str(id+1)
				if self.subrede == "acima":
					iden = fim[0] + 2*espaco
				elif self.subrede == "abaixo":
					iden = comeco[0] - 2*espaco - int(len(texto)*w_string)
			elif tipo == "friafora":
				painter.setPen(QPen(QColor("white"), grossura_seta, Qt.SolidLine))
				ponta = valor
				ramos = -1
				localizacao = localizacao_fria
				tin = fim[0] - maior_temp - espaco
				if dividida and self.subrede != "ambas":
					dados[3] = dutyf_sub[id]
					fracoes = fracoesf[id]
				if e_utilidade_fria_a[id]:
					if self.subrede == "acima":
						texto = "Cold " + str(id+1) + " (utility)"
					elif self.subrede == "abaixo":
						texto = "(utility) Cold " + str(id+1)
				else:
					texto = "Cold " + str(id+1)
				if self.subrede == "acima":
					iden = comeco[0] + 2*espaco
				elif self.subrede == "abaixo":
					iden = fim[0] - 2*espaco - int(len(texto)*w_string)

			painter.drawLine(int(comeco[0]), int(comeco[1]), int(fim[0]), int(fim[1]))
			painter.drawLine(int(fim[0]), int(fim[1]), int(fim[0]+ponta), int(fim[1]+h_seta))
			painter.drawLine(int(fim[0]), int(fim[1]), int(fim[0]+ponta), int(fim[1]-h_seta))

			if self.subrede == "ambas":
				if tipo[0] == "q":
					tamanho_ramo = [int(meio - comeco[0] - 2*ramox), int(fim[0] - meio - 2*ramox)]
				else:
					tamanho_ramo = [int(meio - fim[0] - 2*ramox), int(comeco[0] - meio - 2*ramox)]

			ramoxx = ramox*ramos

			if self.subrede != "ambas":
				localizacao.append([comeco[1]])
				if dividida:
					for ramo in range(1, quantidade):
						painter.drawLine(int(comeco[0]+ramoxx), int(comeco[1]), int(comeco[0]+ramoxx), int(comeco[1]+ramoy*ramo))
						painter.drawLine(int(comeco[0]+ramoxx), int(comeco[1]+ramoy*ramo), int(fim[0]-ramoxx), int(comeco[1]+ramoy*ramo))
						painter.drawLine(int(fim[0]-ramoxx), int(comeco[1]+ramoy*ramo), int(fim[0]-ramoxx), int(fim[1]))
						localizacao[-1].append(int(comeco[1]+ramoy*ramo))
			else:
				localizacao[0].append([comeco[1]])
				localizacao[1].append([comeco[1]])
				if tipo[:4] == "fria":
					primeiro = 1
					segundo = 0
				else:
					primeiro = 0
					segundo = 1
				if dividida[primeiro]:
					for ramo in range(1, quantidade[primeiro]):
						painter.drawLine(int(comeco[0]+ramoxx), int(comeco[1]), int(comeco[0]+ramoxx), int(comeco[1]+ramoy*ramo))
						painter.drawLine(int(comeco[0]+ramoxx), int(comeco[1]+ramoy*ramo), int(comeco[0]+ramoxx+tamanho_ramo[primeiro]*ramos), int(comeco[1]+ramoy*ramo))
						painter.drawLine(int(comeco[0]+ramoxx+tamanho_ramo[primeiro]*ramos), int(comeco[1]+ramoy*ramo), int(comeco[0]+ramoxx+tamanho_ramo[primeiro]*ramos), int(fim[1]))
						localizacao[primeiro][-1].append(int(comeco[1]+ramoy*ramo))
				if dividida[segundo]:
					for ramo in range(1, quantidade[segundo]):
						painter.drawLine(int(comeco[0]+3*ramoxx+tamanho_ramo[primeiro]*ramos), int(comeco[1]), int(comeco[0]+3*ramoxx+tamanho_ramo[primeiro]*ramos), int(comeco[1]+ramoy*ramo))
						painter.drawLine(int(comeco[0]+3*ramoxx+tamanho_ramo[primeiro]*ramos), int(comeco[1]+ramoy*ramo), int(comeco[0]+3*ramoxx+(tamanho_ramo[primeiro]+tamanho_ramo[segundo])*ramos), int(comeco[1]+ramoy*ramo))
						painter.drawLine(int(comeco[0]+3*ramoxx+(tamanho_ramo[primeiro]+tamanho_ramo[segundo])*ramos), int(comeco[1]+ramoy*ramo), int(comeco[0]+3*ramoxx+(tamanho_ramo[primeiro]+tamanho_ramo[segundo])*ramos), int(fim[1]))
						localizacao[segundo][-1].append(int(comeco[1]+ramoy*ramo))

			fonte = painter.font()
			fonte.setBold(True)
			fonte.setFamily("Arial")
			fonte.setPointSize(fonte_calor)
			painter.setFont(fonte)
			painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
			if self.subrede == "acima":
				alinha_in = Qt.AlignRight
				alinha_toca = Qt.AlignLeft
				alinha_iden = Qt.AlignLeft
			elif self.subrede == "abaixo":
				alinha_in = Qt.AlignLeft
				alinha_toca = Qt.AlignRight
				alinha_iden = Qt.AlignRight
			elif self.subrede == "ambas":
				if tipo[0] == "q":
					alinha_in = Qt.AlignRight
					alinha_toca = Qt.AlignLeft
				else:
					alinha_in = Qt.AlignLeft
					alinha_toca = Qt.AlignRight
				alinha_iden = Qt.AlignLeft

			if self.subrede != "abaixo":
				painter.drawText(QRect(int(iden + espaco), int(comeco[1]-h_string), int(len(texto)*w_string + 2*espaco), int(h_string*3)), alinha_iden, texto)
			else:
				painter.drawText(QRect(int(iden - 2*espaco), int(comeco[1]-h_string), int(len(texto)*w_string + 2*espaco), int(h_string*3)), alinha_iden, texto)

			painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
			fonte = painter.font()
			fonte.setFamily("Arial")
			fonte.setBold(False)
			fonte.setPointSize(fonte_calor)
			painter.setFont(fonte)
			painter.drawText(QRect(int(tin), int(comeco[1]-h_string), int(w_string*len(dados[1])), int(h_string*3)), alinha_in, dados[1])
			if not toca or self.subrede == "ambas":
				painter.drawText(QRect(int(lugar), int(comeco[1]-h_string), int(w_string*len(dados[2])), int(h_string*3)), alinha_toca, dados[2])
			if self.subrede != "ambas":
				if not dividida:
					if self.subrede == "acima":
						painter.drawText(QRect(int(tin - 2*espaco - maior_cp), int(comeco[1]-h_string), int(maior_cp), int(h_string*3)), Qt.AlignHCenter, dados[0])
						painter.drawText(QRect(int(tin - 4*espaco - maior_cp - maior_duty), int(comeco[1]-h_string), int(maior_duty), int(h_string*3)), Qt.AlignHCenter, dados[3])
					elif self.subrede == "abaixo":
						painter.drawText(QRect(int(tin + maior_temp + 2*espaco), int(comeco[1]-h_string), int(maior_cp), int(h_string*3)), Qt.AlignHCenter, dados[0])
						painter.drawText(QRect(int(tin + maior_temp + 4*espaco + maior_cp), int(comeco[1]-h_string), int(maior_duty), int(h_string*3)), Qt.AlignHCenter, dados[3])

				else:
					for ramo in range(quantidade):
						if self.subrede == "acima":
							painter.drawText(QRect(int(tin - 2*espaco - maior_cp), int(comeco[1] - h_string + ramo*(ramoy - h_string)), int(maior_cp), int(h_string*3)), Qt.AlignHCenter, str('{:.2f}'.format(round(float(dados[0])*fracoes[ramo], 2))))
							painter.drawText(QRect(int(tin - 4*espaco - maior_cp - maior_duty), int(comeco[1] - h_string + ramo*(ramoy - h_string)), int(maior_duty), int(h_string*3)), Qt.AlignHCenter, str('{:.2f}'.format(round(dados[3][ramo], 2))))
						elif self.subrede == "abaixo":
							painter.drawText(QRect(int(tin + maior_temp + 2*espaco), int(comeco[1] - h_string + ramo*(ramoy - h_string)), int(maior_cp), int(h_string*3)), Qt.AlignHCenter, str('{:.2f}'.format(round(float(dados[0])*fracoes[ramo], 2))))
							painter.drawText(QRect(int(tin + maior_temp + 4*espaco + maior_cp), int(comeco[1] - h_string + ramo*(ramoy - h_string)), int(maior_duty), int(h_string*3)), Qt.AlignHCenter, str('{:.2f}'.format(round(dados[3][ramo], 2))))
			else:
				if tipo[0] == "q":
					painter.drawText(QRect(int(tin - 2*espaco - maior_duty), int(comeco[1]-h_string), int(maior_duty), int(h_string*3)), Qt.AlignHCenter, dados[3])
					if id == 0:
						fonte = painter.font()
						fonte.setBold(True)
						fonte.setPointSize(fonte_calor)
						painter.setFont(fonte)
						painter.drawText(QRect(int(tin - 3*espaco - maior_duty), int(comeco[1]-ramoy-h_string), int(maior_duty+espaco), int(h_string*3)), Qt.AlignHCenter, "Streams Duty ({})".format(unidades_usadas[2]))
				else:
					painter.drawText(QRect(int(lugar - 2*espaco - maior_duty), int(comeco[1]-h_string), int(maior_duty), int(h_string*3)), Qt.AlignHCenter, dados[3])

		def trocador(painter, id, ondeq, ondef, calor, temperaturas, regras_temp, util=False, tipo=""):
			painter.setPen(QPen(Qt.black, grossura_seta, Qt.SolidLine))
			if util:
				if tipo == "quente":
					painter.setBrush(QColor("orange"))
				elif tipo == "fria":
					painter.setBrush(QColor("cyan"))
			else:
				painter.setBrush(QColor("white"))
			painter.drawLine(int(ondeq[0] + raio_trocador/2), int(ondeq[1]), int(ondef[0] + raio_trocador/2), int(ondef[1]))
			painter.drawEllipse(int(ondeq[0]), int(ondeq[1] - raio_trocador/2), int(raio_trocador), int(raio_trocador))
			painter.drawEllipse(int(ondef[0]), int(ondef[1] - raio_trocador/2), int(raio_trocador), int(raio_trocador))
			fonte = painter.font()
			fonte.setFamily("Arial")
			fonte.setBold(False)
			fonte.setPointSize(fonte_temp)
			painter.setFont(fonte)

			duas_quente = regras_temp[0][0]
			duas_fria = regras_temp[0][1]
			viola_quente = regras_temp[1][0]
			viola_frio = regras_temp[1][1]
			termo_quente = regras_temp[1][2]
			termo_frio = regras_temp[1][3]
			anterior_quente = regras_temp[2][0]
			anterior_fria = regras_temp[2][1]
			anterior_termo_quente = regras_temp[2][2]
			anterior_termo_fria = regras_temp[2][3]

			#tqin
			#sempre abaixo e ambas, duas_temp acima
			if duas_quente or self.subrede != "acima":
				if viola_quente or (self.subrede != "acima" and anterior_quente):
					painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
				else:
					painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
				fonte = painter.font()
				if termo_quente or (self.subrede != "acima" and anterior_termo_quente):
					temp = temperaturas[0] + "**"
					fonte.setBold(True)
				else:
					temp = temperaturas[0]
					fonte.setBold(False)
				painter.setFont(fonte)
				painter.drawText(QRect(int(ondeq[0] - w_string*len(temp) - 1), int(ondeq[1] + 1), int(w_string*len(temp)), int(raio_trocador)), Qt.AlignRight, temp)

			#tqout
			#sempre acima, duas_temp abaixo e ambas
			if duas_quente or self.subrede == "acima":
				if viola_frio or (self.subrede == "acima" and anterior_quente):
					painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
				else:
					painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
				fonte = painter.font()
				if termo_frio or (self.subrede == "acima" and anterior_termo_quente):
					temp = temperaturas[1] + "**"
					fonte.setBold(True)
				else:
					temp = temperaturas[1]
					fonte.setBold(False)
				painter.setFont(fonte)
				painter.drawText(QRect(int(ondeq[0] + raio_trocador + 1), int(ondeq[1] + 1), int(len(temp)*w_string), int(raio_trocador)), Qt.AlignLeft, temp)

			#tfout
			#sempre abaixo e ambas, duas_temp acima
			if duas_fria or self.subrede != "acima":
				if viola_quente or (self.subrede != "acima" and anterior_fria):
					painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
				else:
					painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
				fonte = painter.font()
				if termo_quente or (self.subrede != "acima" and anterior_termo_fria):
					temp = temperaturas[2] + "**"
					fonte.setBold(True)
				else:
					temp = temperaturas[2]
					fonte.setBold(False)
				painter.setFont(fonte)
				painter.drawText(QRect(int(ondef[0] - w_string*len(temp) - 1), int(ondef[1] + 1), int(w_string*len(temp)), int(raio_trocador)), Qt.AlignRight, temp)

			#tfin
			#sempre acima, duas_temp abaixo e ambas
			if duas_fria or self.subrede == "acima":
				if viola_frio or (self.subrede == "acima" and anterior_fria):
					painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
				else:
					painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
				fonte = painter.font()
				if termo_frio or (self.subrede == "acima" and anterior_termo_fria):
					temp = temperaturas[3] + "**"
					fonte.setBold(True)
				else:
					temp = temperaturas[3]
					fonte.setBold(False)
				painter.setFont(fonte)
				painter.drawText(QRect(int(ondef[0] + raio_trocador + 1), int(ondef[1] + 1), int(len(temp)*w_string), int(raio_trocador)), Qt.AlignLeft, temp)

			painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
			fonte = painter.font()
			fonte.setFamily("Arial")
			fonte.setBold(True)
			fonte.setPointSize(fonte_calor)
			painter.setFont(fonte)
			painter.drawText(QRect(int(ondeq[0] + raio_trocador/2 - len(calor)*w_string), int(ondeq[1]-raio_trocador-1), int(len(calor)*2*w_string), int(h_string*3)), Qt.AlignHCenter, calor)
			painter.drawText(QRect(int(ondeq[0]), int(ondeq[1] - raio_trocador/2), int(raio_trocador), int(raio_trocador)), Qt.AlignCenter, id)
			painter.drawText(QRect(int(ondef[0]), int(ondef[1] - raio_trocador/2), int(raio_trocador), int(raio_trocador)), Qt.AlignCenter, id)

		def pinch(painter, onde, temperaturas, header):
			painter.setPen(QPen(Qt.black, grossura_seta, Qt.DotLine))
			painter.drawLine(int(onde[0]), int(onde[1]), int(onde[2]), int(onde[3]))
			fonte = painter.font()
			fonte.setFamily("Arial")
			fonte.setBold(False)
			fonte.setPointSize(fonte_calor)
			painter.setFont(fonte)
			painter.drawText(QRect(int(onde[0] - w_string*2*len(temperaturas[0])/2), int(onde[1] - 25), int(w_string*2*len(temperaturas[0])), int(h_string*3)), Qt.AlignHCenter, temperaturas[0])
			painter.drawText(QRect(int(onde[2] - w_string*2*len(temperaturas[0])/2), int(onde[3] + 10), int(w_string*2*len(temperaturas[1])), int(h_string*3)), Qt.AlignHCenter, temperaturas[1])
			fonte.setBold(True)
			fonte.setPointSize(fonte_calor)
			painter.setFont(fonte)
			if self.subrede == "acima":
				painter.drawText(QRect(int(header[0] - maior_temp - 4*espaco - maior_cp), int(header[1] - 25), int(maior_cp+espaco), int(h_string*3)), Qt.AlignHCenter, "Streams CP ({})".format(unidades_usadas[1]))
				painter.drawText(QRect(int(header[0] - maior_temp - 7*espaco - maior_cp - maior_duty), int(header[1] - 25), int(maior_duty+2*espaco), int(h_string*3)), Qt.AlignHCenter, "Streams Duty ({})".format(unidades_usadas[2]))
			elif self.subrede == "abaixo":
				painter.drawText(QRect(int(header[0] + maior_temp + 2*espaco), int(header[1] - 25), int(maior_cp+espaco), int(h_string*3)), Qt.AlignHCenter, "Streams CP ({})".format(unidades_usadas[1]))
				painter.drawText(QRect(int(header[0] + maior_temp + 4*espaco + maior_cp), int(header[1] - 25), int(maior_duty+2*espaco), int(h_string*3)), Qt.AlignHCenter, "Streams Duty ({})".format(unidades_usadas[2]))

		def utilidade(painter, onde, calor, tipo, id):
			painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
			if tipo == "quente":
				painter.setBrush(QColor("orange"))
			else:
				painter.setBrush(QColor("cyan"))

			painter.drawEllipse(int(onde[0]), int(onde[1]-raio_trocador/2), int(raio_trocador), int(raio_trocador))
			painter.drawText(QRect(int(onde[0] + raio_trocador/2 - len(calor)*w_string), int(onde[1]-raio_trocador-1), int(len(calor)*2*w_string), int(h_string*3)), Qt.AlignHCenter, calor)
			painter.drawText(QRect(int(onde[0]), int(onde[1] - raio_trocador/2), int(raio_trocador), int(raio_trocador)), Qt.AlignCenter, id)

		def legenda(painer, ondeq, ondef):

			painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
			painter.setBrush(QColor("white"))
			painter.drawRect(int(ondeq[0] - 12*espaco), int(ondeq[1] - 3*raio_trocador), int(24*espaco + raio_trocador), int(ondef[1] - ondeq[1] + 4*raio_trocador))
			painter.drawLine(int(ondeq[0] + raio_trocador/2 - w_string*len("Legend")), int(ondeq[1] - 2*raio_trocador + h_string - 1), int(ondeq[0] + raio_trocador/2 + w_string*len("Legend")), int(ondeq[1] - 2*raio_trocador + h_string - 1))

			painter.setPen(QPen(Qt.red, grossura_seta, Qt.SolidLine))
			painter.drawLine(int(ondeq[0] - 10*espaco), int(ondeq[1]), int(ondeq[0] + 10*espaco + raio_trocador), int(ondeq[1]))
			painter.drawLine(int(ondeq[0] + 10*espaco + raio_trocador), int(ondeq[1]), int(ondeq[0] + 10*espaco + raio_trocador - valor), int(ondeq[1] - h_seta))
			painter.drawLine(int(ondeq[0] + 10*espaco + raio_trocador), int(ondeq[1]), int(ondeq[0] + 10*espaco + raio_trocador - valor), int(ondeq[1] + h_seta))

			painter.setPen(QPen(Qt.blue, grossura_seta, Qt.SolidLine))
			painter.drawLine(int(ondef[0] - 10*espaco), int(ondef[1]), int(ondef[0] + 10*espaco + raio_trocador), int(ondef[1]))
			painter.drawLine(int(ondef[0] - 10*espaco), int(ondef[1]), int(ondef[0] - 10*espaco + valor), int(ondef[1] - h_seta))
			painter.drawLine(int(ondef[0] - 10*espaco), int(ondef[1]), int(ondef[0] - 10*espaco + valor), int(ondef[1] + h_seta))

			painter.setPen(QPen(Qt.black, grossura_seta, Qt.SolidLine))
			painter.drawLine(int(ondeq[0] + raio_trocador/2), int(ondeq[1]), int(ondef[0] + raio_trocador/2), int(ondef[1]))
			painter.drawEllipse(int(ondeq[0]), int(ondeq[1] - raio_trocador/2), int(raio_trocador), int(raio_trocador))
			painter.drawEllipse(int(ondef[0]), int(ondef[1] - raio_trocador/2), int(raio_trocador), int(raio_trocador))

			fonte = painter.font()
			fonte.setPointSize(fonte_calor)
			fonte.setBold(True)
			fonte.setFamily("Arial")
			painter.setFont(fonte)

			painter.drawText(QRect(int(ondeq[0]), int(ondeq[1] - raio_trocador/2), int(raio_trocador), int(raio_trocador)), Qt.AlignCenter, "Id")
			painter.drawText(QRect(int(ondef[0]), int(ondef[1] - raio_trocador/2), int(raio_trocador), int(raio_trocador)), Qt.AlignCenter, "Id")

			texto = "Heat Load ({})".format(unidades_usadas[2])
			painter.drawText(QRect(int(ondeq[0] + raio_trocador/2 - w_string*(len(texto))), int(ondeq[1] - raio_trocador - 1), int(2*w_string*(len(texto))), int(h_string*3)), Qt.AlignHCenter, texto)

			fonte = painter.font()
			fonte.setPointSize(fonte_temp)
			fonte.setBold(False)
			fonte.setFamily("Arial")
			painter.setFont(fonte)

			texto = "Thin ({})".format(unidades_usadas[0])
			painter.drawText(QRect(int(ondeq[0] - 1 - w_string*len(texto)), int(ondeq[1] + 1), int(w_string*len(texto)), int(h_string*3)), Qt.AlignRight, texto)
			texto = "Thout ({})".format(unidades_usadas[0])
			painter.drawText(QRect(int(ondeq[0] + raio_trocador + 1), int(ondeq[1]+1), int(w_string*len(texto)), int(h_string*3)), Qt.AlignLeft, texto)
			texto = "Tcout ({})".format(unidades_usadas[0])
			painter.drawText(QRect(int(ondef[0] - 1 - w_string*len(texto)), int(ondef[1] + 1), int(w_string*len(texto)), int(h_string*3)), Qt.AlignRight, texto)
			texto = "Tcin ({})".format(unidades_usadas[0])
			painter.drawText(QRect(int(ondef[0] + raio_trocador + 1), int(ondef[1]+1), int(w_string*len(texto)), int(h_string*3)), Qt.AlignLeft, texto)

			fonte = painter.font()
			fonte.setPointSize(fonte_calor + 2)
			fonte.setBold(True)
			fonte.setFamily("Arial")
			painter.setFont(fonte)

			painter.drawText(QRect(int(ondeq[0] + raio_trocador/2 - w_string*len("Legend")), int(ondeq[1] - 2.5*raio_trocador), int(2*w_string*len("Legend")), int(3*h_string)), Qt.AlignHCenter, "Legend")


		global localizacao_quente, localizacao_fria, valor, espaco, fonte_temp, fonte_calor, ramox, ramoy, meio, w_string, h_string, h_seta
		painter = QPainter(self)
		painter.setRenderHints(QPainter.Antialiasing)
		painter.setPen(QPen(Qt.white, 0, Qt.SolidLine))
		painter.setBrush(QBrush(Qt.white, Qt.SolidPattern))
		painter.drawRect(0, 0, self.tamanho[0], self.tamanho[1])

		#designando variaveis
		if self.subrede == "acima":
			trocadores = matriz_armazenada
			uteis = utilidades
			quente_presente = corrente_quente_presente_acima
			fria_presente = corrente_fria_presente_acima
			e_utilidade_quente_a, e_utilidade_fria_a = e_utilidade_quente[:], e_utilidade_fria[:]
			thtoca, tctoca = Thf_acima, Tc0_acima
			thcomeco, tccomeco = Th0, Tcf
			CPha, CPca = CPh, CPc
			correntes_quentes_a, correntes_frias_a = correntes_quentes, correntes_frias
			dutyq, dutyf = calor_atual_quente, calor_atual_frio
			dutyq_sub, dutyf_sub = calor_atual_quente_sub, calor_atual_frio_sub
			divididaq, divididaf = dividida_quente, dividida_fria
			quantidadeq, quantidadef = quantidade_quente, quantidade_fria
			fracoesq, fracoesf = fracoes_quentes, fracoes_frias
		elif self.subrede == "abaixo":
			trocadores = matriz_trocadores_abaixo
			uteis = utilidades_abaixo
			quente_presente = corrente_quente_presente_abaixo
			fria_presente = corrente_fria_presente_abaixo
			e_utilidade_quente_a, e_utilidade_fria_a = e_utilidade_quente[:], e_utilidade_fria[:]
			thtoca, tctoca = Th0_abaixo, Tcf_abaixo
			thcomeco, tccomeco = Thf, Tc0
			CPha, CPca = CPh, CPc
			correntes_quentes_a, correntes_frias_a = correntes_quentes, correntes_frias
			dutyq, dutyf = calor_atual_quente_abaixo, calor_atual_frio_abaixo
			dutyq_sub, dutyf_sub = calor_atual_quente_sub_abaixo, calor_atual_frio_sub_abaixo
			divididaq, divididaf = dividida_quente_abaixo, dividida_fria_abaixo
			quantidadeq, quantidadef = quantidade_quente_abaixo, quantidade_fria_abaixo
			fracoesq, fracoesf = fracoes_quentes_abaixo, fracoes_frias_abaixo
		elif self.subrede == "ambas":
			trocadores = matriz_evolucao
			uteis = utilidades_ev
			quente_presente, fria_presente = [[True]]*(nhot+1), [[True]]*(ncold+1)
			e_utilidade_quente_a, e_utilidade_fria_a = e_utilidade_quente[:], e_utilidade_fria[:]
			e_utilidade_quente_a.append(True)
			e_utilidade_fria_a.append(True)
			thtoca, tctoca = Thf_fake, Tcf_fake
			thcomeco, tccomeco = Th0_fake, Tc0_fake
			CPha, CPca = CPh_fake, CPc_fake
			correntes_quentes_a, correntes_frias_a = correntes_quentes_fake, correntes_frias_fake
			dutyq, dutyf = calor_atual_quente_ev, calor_atual_frio_ev
			dutyq_sub, dutyf_sub = calor_atual_quente_ev, calor_atual_frio_ev
			divq_acima, divq_abaixo, divf_acima, divf_abaixo = dividida_quente_ev_acima, dividida_quente_ev_abaixo, dividida_fria_ev_acima, dividida_fria_ev_abaixo
			quantq_acima, quantq_abaixo, quantf_acima, quantf_abaixo = quantidade_quente_ev_acima, quantidade_quente_ev_abaixo, quantidade_fria_ev_acima, quantidade_fria_ev_abaixo
			fracoesq, fracoesf = fracoes_quentes, fracoes_frias


		#determinando medidas
		tempet = []
		cpe = []
		dutye = []
		for temp in Th0:
			tempet.append(len(str(temp)))
		for temp in Thf:
			tempet.append(len(str(temp)))
		for cp in CPha:
			cpe.append(len(str(cp)))
			dutye.append(len(str('{:.2f}'.format(round(cp*(thcomeco[CPha.index(cp)]-thtoca[CPha.index(cp)]), 2)))))
		for cp in CPca:
			cpe.append(len(str(cp)))
			dutye.append(len(str('{:.2f}'.format(round(cp*(tccomeco[CPca.index(cp)]-tctoca[CPca.index(cp)]), 2)))))

		w_string = 7
		h_string = 7
		h_seta = 7
		grossura_seta = 3
		fonte_calor = 10
		fonte_temp = 8
		raio_trocador = 30
		valor = 15 #tamanho das pontas das setas
		espaco = 10
		ramox = ramoy = 45
		tamanho_minimo = 800

		dutye.append(len("Streams Duty ({})".format(unidades_usadas[2])))
		cpe.append(len("Streams CP ({})".format(unidades_usadas[1])))
		maior_temp = int(max(tempet)*w_string)
		maior_cp = int(max(cpe)*w_string)
		maior_duty = int(max(dutye)*w_string)

		espaco_trocadores = 2*maior_temp

		if self.subrede != "ambas":
			localizacao_quente = []
			localizacao_fria = []
			if self.subrede == "acima":
				t_acima = len(trocadores) + 3
				t_abaixo = 0
			else:
				t_abaixo = len(trocadores) + 3
				t_acima = 0
		else:
			localizacao_quente = [[], []]
			localizacao_fria = [[], []]
			t_acima = 4 + len(uteis[0])*2
			t_abaixo = 4 + len(uteis[1])*2
			for t in range(len(trocadores)):
				if trocadores[t][5] == 1:
					t_acima += 2
				else:
					t_abaixo += 2
		if self.subrede == "acima":
			x_esquerda = 30 + maior_temp + maior_cp + maior_duty + 4*espaco
		if self.subrede == "abaixo":
			x_esquerda  = 30 + maior_duty
		if self.subrede == "ambas":
			x_esquerda = 30 + maior_duty + maior_temp + 3*espaco
			x_direita = max(tamanho_minimo, x_esquerda + (len(trocadores)+len(uteis[0])+len(uteis[1])+4) * espaco_trocadores)
		else:
			x_direita = max(tamanho_minimo, x_esquerda + (len(trocadores)+len(uteis)+4) * espaco_trocadores)

		meio = x_esquerda + t_acima/2 * espaco_trocadores
		comecary = y = 100

		#criar correntes quentes
		for i in range(len(correntes_quentes_a)):
			if quente_presente[i]:
				if len(localizacao_quente) != 0 and self.subrede != "ambas":
					y = localizacao_quente[-1][-1]
				if self.subrede == "ambas":
					if len(localizacao_quente[0]) != 0:
						y = max(localizacao_quente[0][-1][-1], localizacao_quente[1][-1][-1])

				if e_utilidade_quente_a[i]:
					tipo = "quenteutil"
				else:
					tipo = "quente"

				if thtoca[i] != pinchq and self.subrede != "ambas":
					toca = False
				else:
					toca = True

				dados = [str('{:.2f}'.format(round(CPha[i], 2))), str('{:.2f}'.format(round(thcomeco[i], 2))), str('{:.2f}'.format(round(thtoca[i], 2))), str('{:.2f}'.format(round(dutyq[i], 2)))]
				if self.subrede != "ambas":
					corrente(painter, tipo, i, divididaq[i], quantidadeq[i], [x_esquerda, ramoy + y], [x_direita, ramoy + y], dados, toca)
				else:
					corrente(painter, tipo, i, [divq_acima[i], divq_abaixo[i]], [quantq_acima[i], quantq_abaixo[i]], [x_esquerda, ramoy + y], [x_direita, ramoy + y], dados, toca)

			else:
				if len(localizacao_quente) != 0:
					y = localizacao_quente[-1][-1]
				else:
					y = comecary

				dados = ["", "", "", ""]
				corrente(painter, "quentefora", i, False, False, [x_esquerda, ramoy + y], [x_direita, ramoy + y], dados, True)

		#criar correntes frias
		if self.subrede != "ambas":
			y = localizacao_quente[-1][-1]
		else:
			y = max(localizacao_quente[0][-1][-1], localizacao_quente[1][-1][-1])
		for j in range(len(correntes_frias_a)):
			if fria_presente[j]:
				if len(localizacao_fria) != 0 and self.subrede != "ambas":
					y = localizacao_fria[-1][-1]
				if self.subrede == "ambas":
					if len(localizacao_fria[0]) != 0:
						y = max(localizacao_fria[0][-1][-1], localizacao_fria[1][-1][-1])

				if e_utilidade_fria_a[j]:
					tipo = "friautil"
				else:
					tipo = "fria"

				if tctoca[j] != pinchf and self.subrede != "ambas":
					toca = False
				else:
					toca = True

				dados = [str('{:.2f}'.format(round(CPca[j], 2))), str('{:.2f}'.format(round(tccomeco[j], 2))), str('{:.2f}'.format(round(tctoca[j], 2))), str('{:.2f}'.format(round(dutyf[j], 2)))]
				if self.subrede != "ambas":
					corrente(painter, tipo, j, divididaf[j], quantidadef[j], [x_direita, ramoy + y], [x_esquerda, ramoy + y], dados, toca)
				else:
					corrente(painter, tipo, j, [divf_acima[j], divf_abaixo[j]], [quantf_acima[j], quantf_abaixo[j]], [x_direita, ramoy + y], [x_esquerda, ramoy + y], dados, toca)

			else:
				if len(localizacao_fria) != 0:
					y = localizacao_fria[-1][-1]
				dados = ["", "", "", ""]
				corrente(painter, "friafora", j, divididaf[j], quantidadef[j], [x_direita, ramoy + y], [x_esquerda, ramoy + y], dados, True)

		#criar a linha do pinch e cabeçalhos
		if self.subrede == "acima":
			pinch(painter, [x_direita + 1, comecary, x_direita + 1, localizacao_fria[-1][-1] + ramoy], [str('{:.2f}'.format(round(pinchq, 2))), str('{:.2f}'.format(round(pinchf, 2)))], [x_esquerda, comecary])
			legenda(painter, [x_direita + maior_duty + 14*espaco, localizacao_fria[-1][0]], [x_direita + maior_duty + 14*espaco, localizacao_fria[-1][0] + 4*espaco])
		elif self.subrede == "abaixo":
			pinch(painter, [x_esquerda - 1, comecary, x_esquerda - 1, localizacao_fria[-1][-1] + ramoy], [str('{:.2f}'.format(round(pinchq, 2))), str('{:.2f}'.format(round(pinchf, 2)))], [x_direita, comecary])
			legenda(painter, [x_direita + 30*espaco + maior_temp + maior_duty, localizacao_fria[-1][0]], [x_direita + 30*espaco + maior_temp + maior_duty, localizacao_fria[-1][0] + 4*espaco])
		elif self.subrede == "ambas":
			legenda(painter, [x_direita + 20*espaco + maior_temp + maior_duty, localizacao_fria[1][-1][0]], [x_direita + 20*espaco + maior_temp + maior_duty, localizacao_fria[1][-1][0] + 4*espaco])

		#criar os trocadores
		for t in trocadores:
			chot = t[0]-1
			ccold = t[1]-1
			sbhot = t[2]-1
			sbcold = t[3]-1
			if self.subrede != "ambas" or t[5] == 2:
				sestagio = t[4]*espaco_trocadores
			else:
				sestagio = (trocadores.index(t)+1)*espaco_trocadores

			calor = str('{:.2f}'.format(round(t[6], 2)))

			util = False
			if e_utilidade_quente_a[chot]:
				util = True
				tipo = "quente"

			if e_utilidade_fria_a[ccold]:
				util = True
				tipo = "fria"

			if self.subrede == "acima":
				tqin, tqout, tfout, tfin = t[7], t[9], t[8], t[10]
				x, y = 7, 8
				f = 1
			elif self.subrede == "abaixo":
				tqin, tqout, tfout, tfin = t[9], t[7], t[10], t[8]
				x, y = 7, 8
				f = 1
			elif self.subrede == "ambas":
				tqin, tfout, tqout, tfin = t[7], t[8], t[9], t[10]
				if t[5] == 1:
					f = -1
					x, y = 7, 8
				else:
					f = 1
					x, y = 9, 10

			duas_temp_quente = True
			duas_temp_fria = True
			viola_quente, viola_frio = False, False
			termo_quente, termo_frio = False, False
			viola_anterior_quente, viola_anterior_fria = False, False

			if tqin - tfout < dTmin:
				viola_quente = True
				if tqin - tfout < 0:
					termo_quente = True
			if tqout - tfin < dTmin:
				viola_frio = True
				if tqout - tfin < 0:
					termo_frio = True
			try:
				if trocadores[trocadores.index(t)+f][0] == t[0] and trocadores[trocadores.index(t)+f][2] == t[2]:
					duas_temp_quente = False
				if trocadores[trocadores.index(t)+f][1] == t[1] and trocadores[trocadores.index(t)+f][3] == t[3]:
					duas_temp_fria = False
				if self.subrede == "ambas":
					if trocadores[trocadores.index(t)+f][5] == 2 and t[5] == 1:
						duas_temp_quente = True
						duas_temp_fria = True
			except:
				pass
			try:
				termo, termo_quente_anterior, termo_fria_anterior = False, False, False
				if (trocadores[trocadores.index(t)-f][x] - trocadores[trocadores.index(t)-f][y]) < dTmin and trocadores.index(t) != 0:
					if (trocadores[trocadores.index(t)-f][x] - trocadores[trocadores.index(t)-f][y]) < 0 and trocadores.index(t) != 0:
						termo = True
					if trocadores[trocadores.index(t)-f][0] == t[0] and trocadores[trocadores.index(t)-f][2] == t[2]:
						viola_anterior_quente = True
						if termo:
							termo_quente_anterior = True
					if trocadores[trocadores.index(t)-f][1] == t[1] and trocadores[trocadores.index(t)-f][3] == t[3]:
						viola_anterior_fria = True
						if termo:
							termo_fria_anterior = True
			except:
				pass

			temperaturas = [str('{:.2f}'.format(round(tqin, 2))), str('{:.2f}'.format(round(tqout, 2))), str('{:.2f}'.format(round(tfout, 2))), str('{:.2f}'.format(round(tfin, 2)))]
			regras_temp = [[duas_temp_quente, duas_temp_fria], [viola_quente, viola_frio, termo_quente, termo_frio], [viola_anterior_quente, viola_anterior_fria, termo_quente_anterior, termo_fria_anterior]]
			if self.subrede == "acima":
				trocador(painter, "E" + str(trocadores.index(t)+1), [x_direita - espaco_trocadores - sestagio, localizacao_quente[chot][sbhot]], [x_direita - espaco_trocadores - sestagio, localizacao_fria[ccold][sbcold]], calor, temperaturas, regras_temp, util, tipo)
			elif self.subrede == "abaixo":
				trocador(painter, "E" + str(trocadores.index(t)+1), [x_esquerda + espaco_trocadores + sestagio, localizacao_quente[chot][sbhot]], [x_esquerda + espaco_trocadores + sestagio, localizacao_fria[ccold][sbcold]], calor, temperaturas, regras_temp, util, tipo)
			elif self.subrede == "ambas":
				if t[5] == 1:
					trocador(painter, "E" + str(trocadores.index(t)+1), [meio - sestagio - ramox, localizacao_quente[0][chot][sbhot]], [meio - sestagio - ramox, localizacao_fria[0][ccold][sbcold]], calor, temperaturas, regras_temp, util, tipo)
				else:
					trocador(painter, "E" + str(trocadores.index(t)+1), [meio + sestagio + ramox, localizacao_quente[1][chot][sbhot]], [meio + sestagio + ramox, localizacao_fria[1][ccold][sbcold]], calor, temperaturas, regras_temp, util, tipo)

		#criar utilidades em caso de subredes
		if self.subrede != "ambas":
			for u in uteis:
				corrente = u[0]-1
				calor = str('{:.2f}'.format(round(u[1], 2)))
				if self.subrede == "acima":
					tipo = "quente"
					id = "H" + str(uteis.index(u)+1)
					onde = localizacao_fria[corrente][0]
					v = -1
					x = x_direita
				elif self.subrede == "abaixo":
					tipo = "fria"
					id = "C" + str(uteis.index(u)+1)
					onde = localizacao_quente[corrente][0]
					v = 1
					x = x_esquerda

				ondex = (trocadores[-1][4] + uteis.index(u)+2) * espaco_trocadores
				utilidade(painter, [x + v*ondex, onde], calor, tipo, id)
		else:
			for u in uteis[0]:
				corrente = u[0]-1
				calor = str('{:.2f}'.format(round(u[1], 2)))
				tipo = "quente"
				id = "H" + str(uteis[0].index(u)+1)
				onde = localizacao_fria[0][corrente][0]

				ondex = (trocadores[0][4] + uteis[0].index(u)+2) * espaco_trocadores
				utilidade(painter, [meio - ondex, onde], calor, tipo, id)
			for u in uteis[1]:
				corrente = u[0]-1
				calor = str('{:.2f}'.format(round(u[1], 2)))
				tipo = "fria"
				id = "C" + str(uteis[1].index(u)+1)
				onde = localizacao_quente[1][corrente][0]

				ondex = (trocadores[-1][4] + uteis[1].index(u)+2) * espaco_trocadores
				utilidade(painter, [meio + ondex, onde], calor, tipo, id)

		painter.end()

		if self.subrede == "acima":
			self.w = x_direita + maior_duty + 30*espaco
		elif self.subrede == "abaixo":
			self.w = x_direita + maior_temp + maior_cp + maior_duty + 36*espaco
		elif self.subrede == "ambas":
			self.w = x_direita + 2*maior_duty + 30*espaco
			self.h = max(localizacao_fria[0][-1][-1], localizacao_fria[1][-1][-1]) + 10*espaco

		if self.subrede != "ambas":
			self.h = localizacao_fria[-1][-1] + 10*espaco

	def salvar(self):
		file = asksaveasfilename(
	        filetypes=[("PNG", ".png"), ("JPEG", ".JPEG")],
	        defaultextension=".png")
		self.grab(QRect(0, 0, self.w, self.h)).save(file)

class wid_zoom(QtWidgets.QMainWindow):
	factor = 1.5

	def __init__(self, tamanho, subrede, parent=None):
		super(wid_zoom, self).__init__(parent)

		self._scene = QtWidgets.QGraphicsScene(self)
		self._view = QtWidgets.QGraphicsView(self._scene)

		self.desenho = Desenho([tamanho[0], tamanho[1]], subrede)
		self.desenho.setFixedSize(tamanho[0], tamanho[1])
		self._scene.addWidget(self.desenho)

		self.setCentralWidget(self._view)

		QtWidgets.QShortcut(
			QtGui.QKeySequence(QtGui.QKeySequence.ZoomIn),
			self._view,
			context=Qt.WidgetShortcut,
			activated=self.zoom_in,
		)

		QtWidgets.QShortcut(
			QtGui.QKeySequence(QtGui.QKeySequence.ZoomOut),
			self._view,
			context=Qt.WidgetShortcut,
			activated=self.zoom_out,
		)

	@pyqtSlot()
	def zoom_in(self, fator=1.5, arruma=True):
		global zoom_atual, zoom_atual_abaixo

		scale_tr = QtGui.QTransform()
		scale_tr.scale(fator, fator)

		tr = self._view.transform() * scale_tr
		self._view.setTransform(tr)

		if dlg.tabWidget_2.currentIndex() == 0:
			zoom_atual = fator * zoom_atual
			barra = dlg.zoom_acima
			valor = zoom_atual
		elif dlg.tabWidget_2.currentIndex() == 1:
			zoom_atual_abaixo = fator * zoom_atual_abaixo
			barra = dlg.zoom_abaixo
			valor = zoom_atual_abaixo
		if arruma:
			barra.setValue(int(valor*100))

	@pyqtSlot()
	def zoom_out(self, fator=1.5, arruma=True):
		global zoom_atual, zoom_atual_abaixo

		scale_tr = QtGui.QTransform()
		scale_tr.scale(fator, fator)

		scale_inverted, invertible = scale_tr.inverted()

		if invertible:
			tr = self._view.transform() * scale_inverted
			self._view.setTransform(tr)

		if dlg.tabWidget_2.currentIndex() == 0:
			zoom_atual = zoom_atual / fator
			barra = dlg.zoom_acima
			valor = zoom_atual
		elif dlg.tabWidget_2.currentIndex() == 1:
			zoom_atual_abaixo = zoom_atual_abaixo / fator
			barra = dlg.zoom_abaixo
			valor = zoom_atual_abaixo

		if arruma:
			barra.setValue(int(valor*100))

def zoom_barra(barra, wid, atual):
	valor = barra.value()/100
	if valor != atual:
		wid.zoom_in(valor/atual, arruma=False)



#outros
def savefile():
	uf1, uq1, _, _ = fp2.pontopinch(correntes, len(correntes), float(dlg.lineEdit_2.text()))
	akt, _, ajustado, cpf, cpq, areak, deltalmnk = CUSTO(correntes, len(correntes))
	export(correntes, util_temporaria, variadt, yplot, custoopano, custocapital, custocapitalanual, custototanual,uf,uq,float(dlg.lineEdit_2.text()),akt, ajustado, cpf, cpq, areak, deltalmnk)

def violou_dtmin(trocador_violado, onde, dados_do_trocador):
	dlg.dtmin = uic.loadUi("dtmin.ui")
	dlg.dtmin.show()
	text = "ΔT = " + str('{:.2f}'.format(round(trocador_violado[6], 2)))
	textfrio = "ΔT = " + str('{:.2f}'.format(round(trocador_violado[7], 2)))

	if onde == "above":
		dlg.dtmin.label_7.setText(str(len(matriz_armazenada)))
		dlg.dtmin.pushButton.clicked.connect(lambda: above(dados_do_trocador))
	if onde == "below":
		dlg.dtmin.label_7.setText(str(len(matriz_trocadores_abaixo)))
		dlg.dtmin.pushButton.clicked.connect(lambda: below(dados_do_trocador))

	dlg.dtmin.label_3.setText(text)
	dlg.dtmin.label_4.setText(textfrio)

	if trocador_violado[6] < dTmin:
		dlg.dtmin.label_3.setStyleSheet("QLabel {color: red}")
		if trocador_violado[6] < 0:
			dlg.dtmin.label_3.setText(text + "**")
			dlg.dtmin.label_3.setStyleSheet("QLabel {font: 1000; color: red}")
	if trocador_violado[7] < dTmin:
		dlg.dtmin.label_4.setStyleSheet("QLabel {color: red}")
		if trocador_violado[7] < 0:
			dlg.dtmin.label_4.setText(textfrio + "**")
			dlg.dtmin.label_4.setStyleSheet("QLabel {font: 1000; color: red}")

	dlg.dtmin.pushButton_2.clicked.connect(lambda: dlg.dtmin.close())


	def above(dados_do_trocador):
		global subestagio_trocador
		indice = len(matriz_armazenada) - 1
		remover_trocador(dlg, dados_do_trocador, indice, matriz_armazenada)
		printar()
		checaresgotadosacima()
		dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
		wid_acima.desenho.update()
		dlg.dtmin.close()
		subestagio_trocador = indice + 1

	def below(dados_do_trocacdor):
		global subestagio_trocador_abaixo
		indice = len(matriz_trocadores_abaixo) - 1
		remover_trocador_abaixo(dlg, dados_do_trocador, indice, matriz_trocadores_abaixo)
		printar_abaixo()
		checaresgotadosabaixo()
		dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
		wid_abaixo.desenho.update()
		dlg.dtmin.close()
		subestagio_trocador_abaixo = indice + 1

def dividir_corrente(divisao, onde):
	global divtype
	divtype = divisao
	dlg.divisao = uic.loadUi("divisao.ui")
	if divtype == "Q":
		for i in range(nhot):
			if not e_utilidade_quente[i]:
				dlg.divisao.comboBox_2.addItem(str(i+1))
			else:
				dlg.divisao.comboBox_2.addItem(str(i+1) + " (utility)")
		for i in range(ncold):
			dlg.divisao.comboBox_3.addItem(str(i+1))
	elif divtype == "F":
		dlg.divisao.label_5.setText("Split Cold Stream")
		for i in range(ncold):
			if not e_utilidade_fria[i]:
				dlg.divisao.comboBox_2.addItem(str(i+1))
			else:
				dlg.divisao.comboBox_2.addItem(str(i+1) + " (utility)")
		for i in range(nhot):
			dlg.divisao.comboBox_3.addItem(str(i+1))

	dlg.divisao.show()


	def confirm(onde, muda=True):
		global caixa_fracao, quantidade, corrente, estagio, caixa_corrente, label_minimo, spacer, linha
		global minimos, ramosxtrocador

		def calcular_minimo(corrente, quantidade, matriz, i1, i2):
			calor = []
			ramosxtrocador = []
			achou = False
			for i in range(quantidade):
				calor.append(0)
				ramosxtrocador.append([])
			for trocador in matriz:
				if corrente == trocador[i1]:
					calor[trocador[i2]-1] += trocador[6]
					achou = True
					ramosxtrocador[trocador[i2]-1].append(matriz.index(trocador))

			return calor, achou, ramosxtrocador

		achou = False
		minimos = []

		quantidade = int(dlg.divisao.comboBox_3.currentText())
		estagio = 1
		corrente = dlg.divisao.comboBox_2.currentIndex() + 1
		if divtype == "Q":
			if onde == "above":
				quantidade2 = max(quantidade, quantidade_quente[corrente-1])
				if not muda:
					dlg.divisao.comboBox_3.setCurrentIndex(quantidade2-1)
				calor, achou, ramosxtrocador = calcular_minimo(corrente, quantidade2, matriz_armazenada, 0, 2)
				if achou:
					fracoes = calcular_fracoes(corrente, calor, "quente")
					minimos = fracoes[:]
				valores_atuais = fracoes_quentes[corrente-1][:]
			elif onde == "below":
				quantidade2 = max(quantidade, quantidade_quente_abaixo[corrente-1])
				if not muda:
					dlg.divisao.comboBox_3.setCurrentIndex(quantidade2-1)
				calor, achou, ramosxtrocador = calcular_minimo(corrente, quantidade2, matriz_trocadores_abaixo, 0, 2)
				if achou:
					fracoes = calcular_fracoes_abaixo(corrente, calor, "quente")
					minimos = fracoes[:]
				valores_atuais = fracoes_quentes_abaixo[corrente-1][:]
		if divtype == "F":
			if onde == "above":
				quantidade2 = max(quantidade, quantidade_fria[corrente-1])
				if not muda:
					dlg.divisao.comboBox_3.setCurrentIndex(quantidade2-1)
				calor, achou, ramosxtrocador = calcular_minimo(corrente, quantidade2, matriz_armazenada, 1, 3)
				if achou:
					fracoes = calcular_fracoes(corrente, calor, "fria")
					minimos = fracoes[:]
				valores_atuais = fracoes_frias[corrente-1][:]
			elif onde == "below":
				quantidade2 = max(quantidade, quantidade_fria_abaixo[corrente-1])
				if not muda:
					dlg.divisao.comboBox_3.setCurrentIndex(quantidade2-1)
				calor, achou, ramosxtrocador = calcular_minimo(corrente, quantidade2, matriz_trocadores_abaixo, 1, 3)
				if achou:
					fracoes = calcular_fracoes_abaixo(corrente, calor, "fria")
					minimos = fracoes[:]
				valores_atuais = fracoes_frias_abaixo[corrente-1][:]

		if len(valores_atuais) > 0 and not muda:
			valores = valores_atuais
			if len(valores_atuais) < quantidade:
				for i in range(len(valores_atuais), quantidade):
					valores.append(0)
		else:
			valores = []
			for f in range(quantidade):
				valores.append(round(1/quantidade, 4))
			x = float(valores[-1])
			if x * quantidade > 1:
				sobrou = x*quantidade - 1
				valores[-1] = round(x - sobrou, 4)
			if x * quantidade < 1:
				faltou = 1 - x*quantidade
				valores[-1] = round(x + faltou, 4)

		if not achou:
			fracoes = []
			for f in range(quantidade):
				fracoes.append("")
		else:
			quantos = 0
			for q in calor:
				if q != 0:
					quantos += 1
			if quantos > quantidade:
				quantidade = quantidade2
				dlg.divisao.comboBox_3.setCurrentIndex(quantidade-1)
				mensagem_erro("Not able to remove a branch wich has a Heat Exchanger. \nRemove it before spliting the stream.")
				return

			elif quantidade < quantidade2:
				for f in range(len(fracoes)-1, -1, -1):
					if fracoes[f] == 0:
						fracoes.pop(f)
						ramosxtrocador.pop(f)
					else:
						fracoes[f] = "(minimum: " + str(fracoes[f]) + ")"

			if quantidade >= quantidade2:
				soma = 0
				zeros = []
				for f in range(len(fracoes)):
					soma += fracoes[f]
					if fracoes[f] == 0:
						zeros.append(f)
					else:
						fracoes[f] = "(minimum: " + str(fracoes[f]) + ")"
				for z in zeros:
					fracoes[z] = ""

		dlg.divisao.pushButton_3.setEnabled(True)
		lay = dlg.divisao.verticalLayout_3


		try:
			for widget in range(len(caixa_fracao)-1, -1, -1):
				lay.removeWidget(caixa_corrente[widget])
				lay.removeWidget(caixa_fracao[widget])
				lay.removeWidget(label_minimo[widget])
				lay.removeItem(spacer[widget])
				lay.removeWidget(linha[widget])
				caixa_corrente[widget].setParent(None)
				caixa_fracao[widget].setParent(None)
				label_minimo[widget].setParent(None)
				linha[widget].setParent(None)
		except:
			pass


		caixa_fracao = [0] * quantidade
		caixa_corrente = [0] * quantidade
		label_minimo = [0] * quantidade
		spacer = [0] * quantidade
		linha = [0] * quantidade

		for i in range(quantidade):
			caixa_fracao[i] = QtWidgets.QDoubleSpinBox(dlg)
			caixa_corrente[i] = QtWidgets.QLabel(dlg)
			label_minimo[i] = QtWidgets.QLabel(dlg)
			spacer[i] = QtWidgets.QSpacerItem(1, 10, QSizePolicy.Fixed, QSizePolicy.Fixed)
			linha[i] = QtWidgets.QFrame()
			linha[i].setGeometry(QRect(60, 110, 751, 20))
			linha[i].setFrameShape(QtWidgets.QFrame.HLine)
			linha[i].setFrameShadow(QtWidgets.QFrame.Sunken)
			dlg.divisao.verticalLayout_3.addWidget(caixa_corrente[i])
			dlg.divisao.verticalLayout_3.addWidget(caixa_fracao[i])
			dlg.divisao.verticalLayout_3.addWidget(label_minimo[i])
			dlg.divisao.verticalLayout_3.addSpacerItem(spacer[i])
			dlg.divisao.verticalLayout_3.addWidget(linha[i])
			caixa_fracao[i].setDecimals(4)
			caixa_fracao[i].setSingleStep(float(0.1))
			caixa_fracao[i].setMaximum(1)
			caixa_fracao[i].setMinimum(0)
			caixa_fracao[i].setValue(round(valores[i], 4))
			caixa_corrente[i].setText("Substream {}".format(i+1))
			caixa_corrente[i].setAlignment(Qt.AlignCenter)
			caixa_fracao[i].setAlignment(Qt.AlignCenter)
			label_minimo[i].setText(fracoes[i])
			label_minimo[i].setAlignment(Qt.AlignCenter)

	def split(onde):
		if onde == "above":
			if divtype == "Q":
				if not corrente_quente_presente_acima[corrente-1]:
					mensagem_erro("Stream not present in the subnetwork.")
					return
			if divtype == "F":
				if not corrente_fria_presente_acima[corrente-1]:
					mensagem_erro("Stream not present in the subnetwork.")
					return
		elif onde == "below":
			if divtype == "Q":
				if not corrente_quente_presente_abaixo[corrente-1]:
					mensagem_erro("Stream not present in the subnetwork.")
					return
			if divtype == "F":
				if not corrente_fria_presente_abaixo[corrente-1]:
					mensagem_erro("Stream not present in the subnetwork.")
					return

		soma = 0
		fracao = [0] * quantidade
		for i in range(quantidade):
			soma += round(float(caixa_fracao[i].value()), 4)
			fracao[i] = round(float(caixa_fracao[i].value()), 4)

		if len(minimos) > 0:
			for i in range(quantidade):
				if round(fracao[i], 4) < round(minimos[i], 4):
					mensagem_erro("The specified fraction is lower than the minimum. \nOne of the branches will not have enough duty to the already existing Heat Exchangers.")
					return

		if soma != 1:
			mensagem_erro("The sum of the fractions must be equals 1.")
			dlg.divisao.show()
			return

		if onde == "above":
			if divtype == "Q":
				a = preparar_corrente_acima(corrente, indice=0)
				indice = 2
			elif divtype == "F":
				a = preparar_corrente_acima(corrente, indice=1)
				indice = 3
			trocadores = []
			for i in range(len(a)-1, -1, -1):
				trocadores.append(a[i])

			for r in ramosxtrocador:
				for t in trocadores:
					if t[7] in r:
						t[indice] = ramosxtrocador.index(r) + 1

			divisao_de_correntes(divtype, estagio, corrente, quantidade, fracao)
			divisoes.append([divtype, 1, corrente, quantidade, fracao])
			matriz_armazenada = inserir_todos_acima(trocadores, coloca=False, atualiza=True, novo=False)

			for divisao in divisoes:
				if divisao[:3] == divisoes[-1][:3] and divisoes.index(divisao) != len(divisoes) - 1:
					divisoes.pop(divisoes.index(divisao))
					break

			if divtype == "F":
				testar_correntes(dlg, True)
			else:
				if quantidade == 1:
					testar_correntes(dlg, True)
				else:
					testar_correntes(dlg)
			wid_acima.desenho.update()

		elif onde == "below":
			if divtype == "Q":
				a = preparar_corrente_abaixo(corrente, indice=0)
				indice = 2
			elif divtype == "F":
				a = preparar_corrente_abaixo(corrente, indice=1)
				indice = 3
			trocadores = []
			for i in range(len(a)-1, -1, -1):
				trocadores.append(a[i])

			for r in ramosxtrocador:
				for t in trocadores:
					if t[7] in r:
						t[indice] = ramosxtrocador.index(r) + 1

			divisao_de_correntes_abaixo(divtype, estagio, corrente, quantidade, fracao)
			divisoes.append([divtype, 2, corrente, quantidade, fracao])
			matriz_trocadores_abaixo = inserir_todos_abaixo(trocadores, coloca=False, atualiza=True, novo=False)

			for divisao in divisoes:
				if divisao[:3] == divisoes[-1][:3] and divisoes.index(divisao) != len(divisoes) - 1:
					divisoes.pop(divisoes.index(divisao))
					break

			if divtype == "Q":
				testar_correntes_abaixo(dlg, True)
			else:
				if quantidade == 1:
					testar_correntes_abaixo(dlg, True)
				else:
					testar_correntes_abaixo(dlg)
			wid_abaixo.desenho.update()

		dlg.divisao.close()

		printar()
		printar_abaixo()

	dlg.divisao.confirm.clicked.connect(lambda: confirm(onde))
	dlg.divisao.comboBox_2.currentIndexChanged.connect(lambda: confirm(onde, muda=False))
	dlg.divisao.comboBox_3.currentIndexChanged.connect(lambda: confirm(onde))
	dlg.divisao.pushButton_3.clicked.connect(lambda: split(onde))
	dlg.divisao.pushButton_2.clicked.connect(lambda: dlg.divisao.close())

def remover_anteriores(onde, indice_remover, nem_pergunta=False):

	def remover_acima(indice_remover, tudo=True):
		global subestagio_trocador, matriz_armazenada
		if tudo:
			if indice_remover <= len(matriz_armazenada) - 1:
				if len(utilidades) > 0:
					for i in range(len(utilidades)-1, -1, -1):
						try:
							remover_utilidade(utilidades[i][0], i, utilidades)
							dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
						except:
							pass
				dlg.comboBox_10.setEnabled(False)
				dlg.pushButton_8.setEnabled(False)
				for i in range(len(matriz_armazenada)-1, indice_remover-1, -1):
					dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
				remover_todos_acima(indice_remover, temps=True)
				subestagio_trocador = indice_remover + 1
			else:
				indice_remover = dlg.trocador_acima.currentIndex() - len(matriz_armazenada)
				utilidade_remover = utilidades[indice_remover]
				corrente_remover_utilidade = utilidade_remover[0]
				remover_utilidade(corrente_remover_utilidade, indice_remover, utilidades)
				dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
		else:
			if indice_remover <= len(matriz_armazenada) - 1:
				if len(utilidades) > 0:
					for i in range(len(utilidades)-1, -1, -1):
						try:
							remover_utilidade(utilidades[i][0], i, utilidades)
							dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
						except:
							pass
				trocador_remover = matriz_armazenada[indice_remover]
				matriz = nao_sacrificar_matriz(matriz_armazenada)
				matriz.pop(indice_remover)
				remover_todos_acima(indice_remover)
				for trocador in matriz:
					if matriz.index(trocador) >= indice_remover:
						trocador[4] -= 1
				matriz_armazenada = inserir_todos_acima(matriz[indice_remover:])
				if len(matriz) == 0:
					matriz_armazenada = []
				dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)
				subestagio_trocador = len(matriz_armazenada) + 1
			else:
				indice_remover = dlg.trocador_acima.currentIndex() - len(matriz_armazenada)
				utilidade_remover = utilidades[indice_remover]
				corrente_remover_utilidade = utilidade_remover[0]
				remover_utilidade(corrente_remover_utilidade, indice_remover, utilidades)
				dlg.trocador_acima.removeItem(dlg.trocador_acima.count()-1)

	def remover_abaixo(indice_remover, tudo=True):
		global subestagio_trocador_abaixo, matriz_trocadores_abaixo
		if tudo:
			if indice_remover <= len(matriz_trocadores_abaixo) - 1:
				if len(utilidades_abaixo) > 0:
					for i in range(len(utilidades_abaixo)-1, -1, -1):
						try:
							remover_utilidade_abaixo(utilidades_abaixo[i][0], i, utilidades_abaixo)
							dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
						except:
							pass
				dlg.comboBox_43.setEnabled(False)
				dlg.pushButton_20.setEnabled(False)
				for i in range(len(matriz_trocadores_abaixo)-1, indice_remover-1, -1):
					dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
				remover_todos_abaixo(indice_remover, temps=True)
				subestagio_trocador_abaixo = indice_remover + 1
			else:
				indice_remover = dlg.trocador_abaixo.currentIndex() - len(matriz_trocadores_abaixo)
				utilidade_remover = utilidades_abaixo[indice_remover]
				corrente_remover_utilidade = utilidade_remover[0]
				remover_utilidade_abaixo(corrente_remover_utilidade, indice_remover, utilidades_abaixo)
				dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
		else:
			if indice_remover <= len(matriz_trocadores_abaixo) - 1:
				if len(utilidades_abaixo) > 0:
					for i in range(len(utilidades_abaixo)-1, -1, -1):
						try:
							remover_utilidade_abaixo(utilidades_abaixo[i][0], i, utilidades_abaixo)
							dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
						except:
							pass
				trocador_remover = matriz_trocadores_abaixo[indice_remover]
				matriz = nao_sacrificar_matriz(matriz_trocadores_abaixo)
				matriz.pop(indice_remover)
				remover_todos_abaixo(indice_remover)
				for trocador in matriz:
					if matriz.index(trocador) >= indice_remover:
						trocador[4] -= 1
				matriz_trocadores_abaixo = inserir_todos_abaixo(matriz[indice_remover:])
				if len(matriz) == 0:
					matriz_trocadores_abaixo = []
				dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)
				subestagio_trocador_abaixo = len(matriz_trocadores_abaixo) + 1
			else:
				indice_remover = dlg.trocador_abaixo.currentIndex() - len(matriz_trocadores_abaixo)
				utilidade_remover = utilidades_abaixo[indice_remover]
				corrente_remover_utilidade = utilidade_remover[0]
				remover_utilidade_abaixo(corrente_remover_utilidade, indice_remover, utilidades_abaixo)
				dlg.trocador_abaixo.removeItem(dlg.trocador_abaixo.count()-1)

	def sim(onde, indice_remover):
		global perguntar, remover_todos, matriz_armazenada, matriz_trocadores_abaixo

		try:
			if dlg.perguntar.lembrar.isChecked():
				perguntar = False
				remover_todos = True
			dlg.perguntar.close()
		except:
			pass

		verifica = False
		if onde == "acima":
			if e_utilidade_quente[matriz_armazenada[indice_remover][0]-1]:
				verifica = True
			remover_acima(indice_remover)
		if onde == "abaixo":
			if e_utilidade_fria[matriz_trocadores_abaixo[indice_remover][1]-1]:
				verifica = True
			remover_abaixo(indice_remover)

		if verifica:
			verificar_uteis(onde)

		if onde == "acima":
			printar()
			checaresgotadosacima()
			wid_acima.desenho.update()
		elif onde == "abaixo":
			printar_abaixo()
			checaresgotadosabaixo()
			wid_abaixo.desenho.update()

	def nao(onde, indice_remover):
		global perguntar, remover_todo, matriz_armazenada, matriz_trocadores_abaixo

		try:
			if dlg.perguntar.lembrar.isChecked():
				perguntar = False
				remover_todos = False
			dlg.perguntar.close()
		except:
			pass

		verifica = False
		if onde == "acima":
			if indice_remover < len(matriz_armazenada):
				if e_utilidade_quente[matriz_armazenada[indice_remover][0]-1]:
					verifica = True
			if indice_remover < len(matriz_armazenada)-1:
				remover_acima(indice_remover, False)
			else:
				remover_acima(indice_remover)

		if onde == "abaixo":
			if indice_remover < len(matriz_trocadores_abaixo):
				if e_utilidade_fria[matriz_trocadores_abaixo[indice_remover][1]-1]:
					verifica = True
			if indice_remover < len(matriz_trocadores_abaixo)-1:
				remover_abaixo(indice_remover, False)
			else:
				remover_abaixo(indice_remover)

		if verifica:
			verificar_uteis(onde)

		if onde == "acima":
			printar()
			checaresgotadosacima()
			wid_acima.desenho.update()
		elif onde == "abaixo":
			printar_abaixo()
			checaresgotadosabaixo()
			wid_abaixo.desenho.update()

	def verificar_uteis(onde):
		global matriz_armazenada, matriz_trocadores_abaixo, primeira_util, primeira_util_fria

		if onde == "acima" and e_utilidade_quente[nhot-1]:
			para = False
			for trocador in matriz_armazenada:
				if e_utilidade_quente[trocador[0]-1]:
					para = True
					break
			if para:
				primeira_util = False
			else:
				primeira_util = True
				divisao_de_correntes("Q", 1, len(e_utilidade_quente), 1, [1.0])
				for divisao in divisoes:
					if divisao[:3] == ["Q", 1, len(e_utilidade_quente)]:
						divisoes.pop(divisoes.index(divisao))
						break

		elif onde == "abaixo" and e_utilidade_fria[ncold-1]:
			para = False
			for trocador in matriz_trocadores_abaixo:
				if e_utilidade_fria[trocador[1]-1]:
					para = True
					break
			if para:
				primeira_util_fria = False
			else:
				primeira_util_fria = True
				divisao_de_correntes_abaixo("F", 1, len(e_utilidade_fria), 1, [1.0])
				for divisao in divisoes:
					if divisao[:3] == ["F", 2, len(e_utilidade_fria)]:
						divisoes.pop(divisoes.index(divisao))
						break

	global remover_todos, perguntar

	if perguntar and not nem_pergunta: #nem pergunta analisa se ja é o ultimo, perguntar analisa a preferencia do usuário
		dlg.perguntar = uic.loadUi("remover_anteriores.ui")
		dlg.perguntar.show()
		dlg.perguntar.sim.clicked.connect(lambda: sim(onde, indice_remover))
		dlg.perguntar.nao.clicked.connect(lambda: nao(onde, indice_remover))
	else:
		if remover_todos:
			sim(onde, indice_remover)
		else:
			nao(onde, indice_remover)

def divisao_de_utilidades(tipo, corrente, dados_do_trocador, ambas=False, m=[]):

	def simm(tipo, corrente, dados_do_trocador, ambas=False, m=[]):
		global matriz_armazenada, matriz_trocadores_abaixo, matriz_evolucao
		global nao_perguntar, dividir_padrao, subestagio_trocador, subestagio_trocador_abaixo

		try:
			if dlg.perguntar_util.lembrar.isChecked():
				nao_perguntar = True
				dividir_padrao = True
		except:
			pass

		if not ambas:
			if tipo == "quente": #acima
				trocadores = []
				matriz_reserva = nao_sacrificar_matriz(matriz_armazenada)
				matriz_reserva.append(dados_do_trocador)
				if dados_do_trocador[6] < 0.001:
					matriz_reserva[-1][6] = calor_atual_frio_sub[matriz_reserva[-1][1]-1][matriz_reserva[-1][3]-1]
				if matriz_reserva[-1][6] < 0.001:
					mensagem_erro("This cold stream is already supplied")
					matriz_reserva.pop(-1)
					return

				quantidade = 1
				for i in range(len(matriz_reserva)):
					if matriz_reserva[i][0] == corrente:
						matriz_reserva[i][2] = quantidade
						trocadores.append(matriz_reserva[i])
						quantidade += 1

				soma = 0
				fracoes = []

				calor = 0
				for t in trocadores:
					calor += t[6]

				for i in range(quantidade-2):
					soma_trocadores = 0
					for j in range(len(trocadores)):
						if trocadores[j][2] == i + 1:
							soma_trocadores += trocadores[j][6]
					if soma_trocadores != 0:
						fracoes.append(soma_trocadores / max(util_quente, calor))
						soma += fracoes[-1]
				fracoes.append(1-soma)

				preparar_corrente_acima(corrente)
				divisao_de_correntes("Q", 1, corrente, len(fracoes), fracoes)
				divisoes.append(["Q", 1, corrente, len(fracoes), fracoes])
				matriz_armazenada = inserir_todos_acima(trocadores, coloca=False, atualiza=True)

				for divisao in divisoes:
					if divisao[:3] == divisoes[-1][:3] and divisoes.index(divisao) != len(divisoes) - 1:
						divisoes.pop(divisoes.index(divisao))
						break

				printar()
				checaresgotadosacima()
				dlg.trocador_acima.addItem("E" + str(subestagio_trocador))
				dlg.trocador_acima.setCurrentIndex(dlg.trocador_acima.count()-1)
				wid_acima.desenho.update()
				subestagio_trocador += 1

			elif tipo == "fria":
				trocadores = []
				matriz_reserva = nao_sacrificar_matriz(matriz_trocadores_abaixo)
				matriz_reserva.append(dados_do_trocador)
				if dados_do_trocador[6] < 0.001:
					matriz_reserva[-1][6] = calor_atual_quente_sub_abaixo[matriz_reserva[-1][0]-1][matriz_reserva[-1][2]-1]
				if matriz_reserva[-1][6] < 0.001:
					mensagem_erro("This hot stream is already supplied")
					matriz_reserva.pop(-1)
					return

				quantidade = 1
				for i in range(len(matriz_reserva)):
					if matriz_reserva[i][1] == corrente:
						matriz_reserva[i][3] = quantidade
						trocadores.append(matriz_reserva[i])
						quantidade += 1

				soma = 0
				fracoes = []

				calor = 0
				for t in trocadores:
					calor += t[6]

				for i in range(quantidade-2):
					soma_trocadores = 0
					for j in range(len(trocadores)):
						if trocadores[j][3] == i + 1:
							soma_trocadores += trocadores[j][6]
					if soma_trocadores != 0:
						fracoes.append(soma_trocadores / max(calor, util_fria))
						soma += fracoes[-1]
				fracoes.append(1-soma)

				preparar_corrente_abaixo(corrente)
				divisao_de_correntes_abaixo("F", 1, corrente, len(fracoes), fracoes)
				divisoes.append(["F", 2, corrente, len(fracoes), fracoes])
				matriz_trocadores_abaixo = inserir_todos_abaixo(trocadores, coloca=False, atualiza=True)

				for divisao in divisoes:
					if divisao[:3] == divisoes[-1][:3] and divisoes.index(divisao) != len(divisoes) - 1:
						divisoes.pop(divisoes.index(divisao))
						break

				printar_abaixo()
				checaresgotadosabaixo()
				dlg.trocador_abaixo.addItem("E" + str(subestagio_trocador_abaixo))
				dlg.trocador_abaixo.setCurrentIndex(dlg.trocador_abaixo.count()-1)
				wid_abaixo.desenho.update()
				subestagio_trocador_abaixo += 1

		else:
			if tipo == "quente" or tipo == "Hot":
				estagio = 1
				div = "Q"
				util = util_quente
				ramo_indice = 2
			else:
				estagio = 2
				div = "F"
				util = util_fria
				ramo_indice = 3

			trocadores = []
			matriz_reserva = nao_sacrificar_matriz(m)

			ramos = []
			for i in range(len(matriz_reserva)):
				if tipo == "quente" or tipo == "Hot":
					if matriz_reserva[i][0] == corrente and matriz_reserva[i][5] == estagio:
						trocadores.append(matriz_reserva[i])
						ramos.append(matriz_reserva[i][2])
					if matriz_reserva[i][5] == estagio and dados_do_trocador[4] == matriz_reserva[i][4]:
						parar = i
				else:
					if matriz_reserva[i][1] == corrente and matriz_reserva[i][5] == estagio:
						trocadores.append(matriz_reserva[i])
						ramos.append(matriz_reserva[i][3])

			quantidade = max(ramos) + 1

			if tipo == "quente" or tipo == "Hot":
				matriz_reserva[parar][2] = quantidade
			else:
				matriz_reserva[-1][3] = quantidade

			soma = 0
			fracoes = []

			calor = 0
			for t in trocadores:
				calor += t[6]

			for i in range(quantidade-1):
				soma_trocadores = 0
				for j in range(len(trocadores)):
					if trocadores[j][ramo_indice] == i + 1:
						soma_trocadores += trocadores[j][6]
				fracoes.append(soma_trocadores / max(calor, util))
				soma += fracoes[-1]
			fracoes.append(1 - soma)

			divisao_de_correntes_ev(div, estagio, corrente, quantidade, fracoes)
			divisoes_ev.append([div, estagio, corrente, quantidade, fracoes])

			for divisao in divisoes_ev:
				if divisao[:3] == divisoes_ev[-1][:3] and divisoes_ev.index(divisao) != len(divisoes_ev) - 1:
					divisoes_ev.pop(divisoes_ev.index(divisao))
					break

			return matriz_reserva

		dlg.perguntar_util.close()

	def naoo(tipo, dados_do_trocador):
		global nao_perguntar, dividir_padrao, subestagio_trocador, subestagio_trocador_abaixo, matriz_armazenada, matriz_trocadores_abaixo

		try:
			if dlg.perguntar_util.lembrar.isChecked():
				nao_perguntar = True
				dividir_padrao = False
		except:
			pass

		if tipo == "quente": #acima
			if dados_do_trocador[6] < 0.001:
				mensagem_erro("This cold stream is already supplied.")
				return
			if dlg.radioButton_4.isChecked():
				matriz_armazenada, inseriu = inserir_trocador(dlg, dados_do_trocador, ignora=True, ultimo=True)
			else:
				matriz_armazenada, inseriu = inserir_trocador(dlg, dados_do_trocador, ultimo=True)
			if inseriu:
				if (matriz_armazenada[-1][7] - matriz_armazenada[-1][8]) < dTmin or (matriz_armazenada[-1][9] - matriz_armazenada[-1][10]) < dTmin:
					trocador_violado = matriz_armazenada[-1][:6]
					trocador_violado.append(matriz_armazenada[-1][7] - matriz_armazenada[-1][8])
					trocador_violado.append(matriz_armazenada[-1][9] - matriz_armazenada[-1][10])
					violou_dtmin(trocador_violado, "above", dados_do_trocador)
				printar()
				checaresgotadosacima()
				dlg.trocador_acima.addItem("E" + str(subestagio_trocador))
				dlg.trocador_acima.setCurrentIndex(dlg.trocador_acima.count()-1)
				wid_acima.desenho.update()
				subestagio_trocador += 1

		elif tipo == "fria":
			if dados_do_trocador[6] < 0.001:
				mensagem_erro("This hot stream is already supplied.")
				return
			if dlg.radioButton_20.isChecked():
				matriz_trocadores_abaixo, inseriu = inserir_trocador_abaixo(dlg, dados_do_trocador, ignora=True, ultimo=True)
			else:
				matriz_trocadores_abaixo, inseriu = inserir_trocador_abaixo(dlg, dados_do_trocador, ultimo=True)
			if inseriu:
				if (matriz_trocadores_abaixo[-1][7] - matriz_trocadores_abaixo[-1][8]) < dTmin or (matriz_trocadores_abaixo[-1][9] - matriz_trocadores_abaixo[-1][10]) < dTmin:
					trocador_violado = matriz_trocadores_abaixo[-1][:6]
					trocador_violado.append(matriz_trocadores_abaixo[-1][7] - matriz_trocadores_abaixo[-1][8])
					trocador_violado.append(matriz_trocadores_abaixo[-1][9] - matriz_trocadores_abaixo[-1][10])
					violou_dtmin(trocador_violado, "below", dados_do_trocador)
				printar_abaixo()
				checaresgotadosabaixo()
				dlg.trocador_abaixo.addItem("E" + str(subestagio_trocador_abaixo))
				dlg.trocador_abaixo.setCurrentIndex(dlg.trocador_abaixo.count()-1)
				wid_abaixo.desenho.update()
				subestagio_trocador_abaixo += 1

		dlg.perguntar_util.close()

	if not nao_perguntar and not ambas:
		dlg.perguntar_util = uic.loadUi("dividir_util.ui")
		dlg.perguntar_util.show()
		dlg.perguntar_util.sim.clicked.connect(lambda: simm(tipo, corrente, dados_do_trocador))
		dlg.perguntar_util.nao.clicked.connect(lambda: naoo(tipo, dados_do_trocador))
	else:
		if not ambas:
			if dividir_padrao:
				simm(tipo, corrente, dados_do_trocador)
			else:
				naoo(tipo, dados_do_trocador)
		else:
			return simm(tipo, corrente, dados_do_trocador, ambas, m)

def botao_remover(indice, botao, onde):
	global matriz_armazenada, utilidades, matriz_trocadores_abaixo, utilidades_abaixo
	if onde == "acima":
		if indice > len(matriz_armazenada):
			botao.setText("Remove H" + str(indice - len(matriz_armazenada)))
		else:
			botao.setText("Remove E" + str(indice))
	elif onde == "abaixo":
		if indice > len(matriz_trocadores_abaixo):
			botao.setText("Remove C" + str(indice - len(matriz_trocadores_abaixo)))
		else:
			botao.setText("Remove E" + str(indice))



#evolução
def nao_sacrificar_matriz(matriz_naomuda):
	matriz = []
	for i in range(len(matriz_naomuda)):
		trocador = []
		for j in range(len(matriz_naomuda[0])):
			try:
				trocador.append(matriz_naomuda[i][j])
			except:
				pass
		matriz.append(trocador)
	return matriz

def evolucao(matriz_acima_naomuda, matriz_abaixo_naomuda, nivel, todos=False, jogar_evolucao=False, sub=False):

	def criar_matriz(matriz_acima, matriz_abaixo):
		for i in range(len(matriz_acima)-1, -1, -1):
			if len(matriz_acima[i]) == 2:
				matriz_acima.pop(i)
			else:
				matriz_acima[i][0] -= 1
				matriz_acima[i][1] += (n_quentes - 1)

		for i in range(len(matriz_abaixo)-1, -1, -1):
			if len(matriz_abaixo[i]) == 2:
				matriz_abaixo.pop(i)
			else:
				matriz_abaixo[i][0] -= 1
				matriz_abaixo[i][1] += (n_quentes - 1)

		return matriz_acima + matriz_abaixo

	def criar_incidencia(matriz_nova, nhot, ncold):
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

	def achar_trocador(incidencia, matriz_trocadores, correntee, excecao, comecar, nivel, n, trocador_inicial, trocadores_laco):
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
				if incidencia[c][trocadores] == -i and trocadores != excecao and not trocadores+1 in trocadores_laco:
					t = trocadores
					return c, t
		return "o", "o"

	def lacos(incidencia, matriz_trocadores, nivel, todos):
		ja_encontrado = []
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
				trocadores_laco = [trocador_inicial+1]
				tenta_dnv = True
				for n in range(nivel*2):
					if tenta_dnv:
						corrente, trocador = achar_trocador(incidencia, matriz_trocadores, corrente, trocador, comecar, nivel, n, trocador_inicial, trocadores_laco)
						if corrente == "o":
							tenta_dnv = False
						else:
							trocadores_laco.append(trocador+1)
							if corrente == corrente_inicial and trocador == trocador_inicial and n == nivel*2-1:
								trocadores_laco.pop(-1)
								if todos:
									if not sorted(trocadores_laco) in ja_encontrado:
										ja_encontrado.append(sorted(trocadores_laco))
								else:
									return trocadores_laco
		if todos:
			return ja_encontrado
		else:
			return ["None "]

	def criar_rede_completa(matriz_acima, matriz_abaixo, primeiro=False, sub=False):
		global Th0_fake, Thf_fake, CPh_fake, Tc0_fake, Tcf_fake, CPc_fake, correntes_quentes_fake, correntes_frias_fake, n_quentes, n_frias

		ultimo_subestagio_acima = 0

		if primeiro:
			Th0_fake = Th0[:]
			Thf_fake = Thf[:]
			CPh_fake = CPh[:]
			Tc0_fake = Tc0[:]
			Tcf_fake = Tcf[:]
			CPc_fake = CPc[:]
			n_quentes = nhot
			n_frias = ncold
			correntes_quentes_fake = correntes_quentes[:]
			correntes_frias_fake = correntes_frias[:]
			if not sub:
				if len(matriz_acima[-1]) == 2 or len(matriz_abaixo[-1]) == 2:
					n_quentes += 1
					n_frias += 1
					maior_fria = max(Tcf)
					menor_quente = min(Thf)
					c_quente = [maior_fria + 3*dTmin, maior_fria + 3*dTmin - 0.001, util_quente/0.001, "Hot", 0.05]
					c_fria = [menor_quente - 3*dTmin, menor_quente - 3*dTmin + 0.001, util_fria/0.001, "Cold", 0.05]
					Th0_fake.append(c_quente[0])
					Thf_fake.append(c_quente[1])
					CPh_fake.append(c_quente[2])
					Tc0_fake.append(c_fria[0])
					Tcf_fake.append(c_fria[1])
					CPc_fake.append(c_fria[2])
					correntes_quentes_fake.append(1)
					correntes_frias_fake.append(1)
					dlg.nivel.addItem(str(min(n_quentes, n_frias)))
			else:
				for i in range(len(matriz_acima)-1, -1, -1):
					if len(matriz_acima[i]) == 2:
						matriz_acima.pop(-1)
				for i in range(len(matriz_abaixo)-1, -1, -1):
					if len(matriz_abaixo[i]) == 2:
						matriz_abaixo.pop(-1)

			nska = max(subestagio_trocador, subestagio_trocador_abaixo) + 2*max(nhot, ncold)
			for i in range(len(matriz_acima)):
				if len(matriz_acima[i]) > 2:
					ultimo_subestagio_acima = matriz_acima[i][4]
				elif not sub:
					matriz_acima[i] = [n_quentes, matriz_acima[i][0], 1, 1, i+1, 1, matriz_acima[i][1]]
					ultimo_subestagio_acima = i + 1

			for i in range(len(matriz_acima)):
				if len(matriz_acima[i]) > 2:
					matriz_acima[i][4] = ultimo_subestagio_acima - i

			for i in range(len(matriz_abaixo)):
				if len(matriz_abaixo[i]) > 2:
					matriz_abaixo[i][5] = 2
				elif not sub:
					matriz_abaixo[i] = [matriz_abaixo[i][0], n_frias, 1, 1, i+1, 2, matriz_abaixo[i][1]]

			receber_pinch_ev(Thf_fake, Tcf_fake, n_quentes, n_frias, CPh_fake, CPc_fake, dTmin, pinchq, pinchf, Th0_fake, Tc0_fake, nska)

			try:
				remover_todos_ev()
			except:
				pass

			for quente in range(nhot):
				divisao_de_correntes_ev("Q", 1, quente+1, 1, [1])
				divisao_de_correntes_ev("Q", 2, quente+1, 1, [1])
			for fria in range(ncold):
				divisao_de_correntes_ev("F", 1, fria+1, 1, [1])
				divisao_de_correntes_ev("F", 2, fria+1, 1, [1])
			for i in range(len(divisoes)):
				divisao_de_correntes_ev(divisoes[i][0], divisoes[i][1], divisoes[i][2], divisoes[i][3], divisoes[i][4])
		else:
			remover_todos_ev()
			for i in range(len(divisoes_ev)):
				divisao_de_correntes_ev(divisoes_ev[i][0], divisoes_ev[i][1], divisoes_ev[i][2], divisoes_ev[i][3], divisoes_ev[i][4])

		matriz_total = matriz_acima + matriz_abaixo
		matriz_completa = inserir_trocador_ev(matriz_total)
		if len(utilidades) > 0 and sub:
			for i in range(len(utilidades)):
				adicionar_utilidade_ev("quente", utilidades[i][0])
		if len(utilidades_abaixo) > 0 and sub:
			for i in range(len(utilidades_abaixo)):
				adicionar_utilidade_ev("fria", utilidades[i][0])

		try:
			return nao_sacrificar_matriz(matriz_completa)
		except:
			return []

	def coisas_interface(trocadores_laco, matriz_completa):
		text = ""
		dlg.trocador_remover.clear()
		menor_calor = []
		trocadores_combo = []
		for i in range(len(trocadores_laco)):
			if trocadores_laco[i] != "None ":
				text += ("E" + str(trocadores_laco[i]) + ", ")
				menor_calor.append(trocadores[trocadores_laco[i]-1][6])
				trocadores_combo.append(text[len(text)-4:len(text)-2])
				dlg.trocador_remover.addItem(text[len(text)-4:len(text)-2])
				dlg.trocador_remover.setEnabled(True)
				dlg.remover.setEnabled(True)
			else:
				text = trocadores_laco[i] + "."
				dlg.trocador_remover.setEnabled(False)
				dlg.remover.setEnabled(False)

		text = text[:len(text)-2]
		text += "."
		dlg.trocadores_loop.setText(text)
		try:
			menor_calorr = min(menor_calor)
			dlg.trocador_remover.setCurrentIndex(menor_calor.index(menor_calorr))
		except:
			pass
		dlg.trocador_remover.setItemText(dlg.trocador_remover.currentIndex(), dlg.trocador_remover.currentText() + " (suggested)")
		if nivel == 1:
			dlg.label_7.setText("Loop Found Between:")
		else:
			dlg.label_7.setText("Loop Found Among:")

		dlg.remover.clicked.connect(lambda: distribuir_calor(trocadores_laco, matriz_completa, dlg.trocador_remover.currentIndex()))

	def interface_todos(trocadores_laco, matriz_completa):

		class Botao():
			def __init__(self, nivel, laco):
				self.nivel = nivel
				self.laco = laco
				self.button = QtWidgets.QPushButton("  Remove  ")
				self.button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
				self.button.setStyleSheet("QPushButton {font: 1000}")
				self.combo = QtWidgets.QComboBox()
				self.combo.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
				self.combo.setMinimumWidth(100)
				self.button.clicked.connect(lambda: distribuir_calor(trocadores_laco[self.nivel][self.laco], matriz_completa, self.combo.currentIndex()))

			def botaoo(self):
				return self.button

			def comboo(self):
				return self.combo

		dlg.lista_lacos = uic.loadUi("lista_lacos.ui")

		if len(trocadores_laco) == 0:
			label_nivel = QtWidgets.QLabel("No remaining Loop")
			label_nivel.setStyleSheet("QLabel {font: 1000 12pt 'MS Shell Dlg 2'}")
			label_nivel.setAlignment(Qt.AlignCenter)
			dlg.lista_lacos.lista.addWidget(label_nivel)
		else:
			lay_nivel = [0] * len(trocadores_laco)
			lay_laco = [0] * len(trocadores_laco)
			label_nivel = [0] * len(trocadores_laco)
			label_trocador = [0] * len(trocadores_laco)
			botao_remover = [0] * len(trocadores_laco)


			for nivel in range(len(trocadores_laco)):
				lay_nivel[nivel] = QtWidgets.QVBoxLayout()
				linha = QtWidgets.QFrame()
				linha.setGeometry(QRect(60, 110, 751, 20))
				linha.setFrameShape(QtWidgets.QFrame.HLine)
				linha.setFrameShadow(QtWidgets.QFrame.Sunken)
				if nivel != 0:
					lay_nivel[nivel].addWidget(linha)
				lay_laco[nivel] = [0] * len(trocadores_laco[nivel])
				label_trocador[nivel] = [0] * len(trocadores_laco[nivel])
				botao_remover[nivel] = [0] * len(trocadores_laco[nivel])
				for laco in range(len(trocadores_laco[nivel])):
					if laco == 0:
						label_nivel[nivel] = QtWidgets.QLabel("Level " + str(int(len(trocadores_laco[nivel][laco])/2)) + " Loops")
						label_nivel[nivel].setStyleSheet("QLabel {font: 1000 12pt 'MS Shell Dlg 2'}")
						label_nivel[nivel].setAlignment(Qt.AlignCenter)
						lay_nivel[nivel].addWidget(label_nivel[nivel])
					lay_laco[nivel][laco] = QtWidgets.QHBoxLayout()
					botao_remover[nivel][laco] = Botao(nivel, laco)
					texto = "Loop " + str(laco+1) + ": "
					menor_calor = []
					for trocador in range(len(trocadores_laco[nivel][laco])):
						texto += "E" + str(trocadores_laco[nivel][laco][trocador]) + ", "
						botao_remover[nivel][laco].comboo().addItem("E" + str(trocadores_laco[nivel][laco][trocador]))
						menor_calor.append(matriz_completa[trocadores_laco[nivel][laco][trocador]-1][6])
					botao_remover[nivel][laco].comboo().setCurrentIndex(menor_calor.index(min(menor_calor)))
					botao_remover[nivel][laco].comboo().setItemText(botao_remover[nivel][laco].comboo().currentIndex(), botao_remover[nivel][laco].comboo().currentText() + " (suggested)")
					texto = texto[:len(texto)-2]
					texto += "."
					label_trocador[nivel][laco] = QtWidgets.QLabel(texto)
					label_trocador[nivel][laco].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
					label_trocador[nivel][laco].setStyleSheet("QLabel {font: 10pt 'MS Shell Dlg 2'}")
					lay_laco[nivel][laco].addWidget(label_trocador[nivel][laco])
					lay_laco[nivel][laco].addWidget(botao_remover[nivel][laco].comboo())
					lay_laco[nivel][laco].addWidget(botao_remover[nivel][laco].botaoo())
					lay_nivel[nivel].addLayout(lay_laco[nivel][laco])
				dlg.lista_lacos.lista.addLayout(lay_nivel[nivel])

		dlg.lista_lacos.show()

	def distribuir_calor(trocadores_laco, matriz_completa, trocador_removido):
		dlg.dividir_calor = uic.loadUi("distribuir_calor.ui")

		corrente_quente_vai_remover = matriz_completa[trocadores_laco[trocador_removido]-1][0]
		corrente_fria_vai_remover = matriz_completa[trocadores_laco[trocador_removido]-1][1]
		calor_trocador_removido = matriz_completa[trocadores_laco[trocador_removido]-1][6]
		valores = []
		valores_recomendados = []
		placeholders = [[], []]

		label_trocador = [0] * len(trocadores_laco)
		set_calor = [0] * len(trocadores_laco)
		add_calor = [0] * len(trocadores_laco)
		dtquente = [0] * len(trocadores_laco)
		dtfrio = [0] * len(trocadores_laco)
		lay = [0] * len(trocadores_laco)

		dlg.dividir_calor.trocador_remover.setText("E" + str(trocadores_laco[trocador_removido]) + " Heat Load: " + str(round(calor_trocador_removido, 2)))
		dlg.dividir_calor.horizontalLayout_3.setAlignment(Qt.AlignCenter)
		dlg.dividir_calor.horizontalLayout_4.setAlignment(Qt.AlignCenter)

		for i in range(len(trocadores_laco)):
			if i != trocador_removido:
				label_trocador[i] = QtWidgets.QLabel(dlg.dividir_calor)
				label_trocador[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				label_trocador[i].setAlignment(Qt.AlignCenter)
				set_calor[i] = QtWidgets.QLineEdit(dlg.dividir_calor)
				set_calor[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				set_calor[i].setAlignment(Qt.AlignCenter)
				set_calor[i].setEnabled(False)
				add_calor[i] = QtWidgets.QLineEdit(dlg.dividir_calor)
				add_calor[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				add_calor[i].setAlignment(Qt.AlignCenter)
				add_calor[i].setEnabled(False)
				dtquente[i] = QtWidgets.QLabel(dlg.dividir_calor)
				dtquente[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				dtquente[i].setAlignment(Qt.AlignCenter)
				dtfrio[i] = QtWidgets.QLabel(dlg.dividir_calor)
				dtfrio[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				dtfrio[i].setAlignment(Qt.AlignCenter)
				label_trocador[i].setText("E" + str(trocadores_laco[i]))
				label_trocador[i].setMinimumWidth(95)
				label_trocador[i].setMaximumWidth(95)
				label_trocador[i].setStyleSheet("QLabel {font: 1000 10pt 'MS Shell Dlg 2'}")
				dtquente[i].setText("-")
				dtquente[i].setFont(QFont("Arial", 10))
				dtquente[i].setStyleSheet("QLabel {font: 1000 10pt 'MS Shell Dlg 2'}")
				dtfrio[i].setText("-")
				dtfrio[i].setFont(QFont("Arial", 10))
				dtfrio[i].setStyleSheet("QLabel {font: 1000 10pt 'MS Shell Dlg 2'}")
				lay[i] = QtWidgets.QHBoxLayout()
				lay[i].addWidget(label_trocador[i])
				lay[i].addWidget(set_calor[i])
				lay[i].addWidget(add_calor[i])
				lay[i].addWidget(dtquente[i])
				lay[i].addWidget(dtfrio[i])
				dlg.dividir_calor.trocadores.addLayout(lay[i])
				if matriz_completa[trocadores_laco[i]-1][0] == corrente_quente_vai_remover or matriz_completa[trocadores_laco[i]-1][1] == corrente_fria_vai_remover:
					calor_recomendado = matriz_completa[trocadores_laco[i]-1][6] + calor_trocador_removido
					placeholders[1].append("Ex: " + str(round(calor_trocador_removido, 2)))
				else:
					calor_recomendado = matriz_completa[trocadores_laco[i]-1][6] - calor_trocador_removido
					placeholders[1].append("Ex: -" + str(round(calor_trocador_removido, 2)))
				placeholders[0].append(str(round(calor_recomendado, 2)) + " (suggested)")
				valores.append(calor_recomendado)
				valores_recomendados.append(calor_recomendado)
			else:
				valores.append(0)
				valores_recomendados.append(0)
				placeholders[0].append(0)
				placeholders[1].append(0)

		for i in range(len(set_calor)):
			dlg.dividir_calor.radio_add.toggled.connect(lambda: liberar_bloquear([set_calor, add_calor], "add", trocador_removido, placeholders))
			dlg.dividir_calor.radio_set.toggled.connect(lambda: liberar_bloquear([set_calor, add_calor], "setar", trocador_removido, placeholders))
			dlg.dividir_calor.padrao.toggled.connect(lambda: liberar_bloquear([set_calor, add_calor], "padrão", trocador_removido, placeholders))

		dlg.dividir_calor.show()
		dlg.dividir_calor.prever.clicked.connect(lambda: distribuiu([set_calor, add_calor], valores, valores_recomendados, trocadores_laco, matriz_completa, trocador_removido, dtquente, dtfrio))

		def distribuiu(valor_trocador, valores, valores_recomendados, trocadores_laco, matriz_completa_naomuda, trocador_removido, dtquente, dtfrio):
			global ja_violava, layh, novas_violacoes, dt_quente_novo, dt_frio_novo
			for i in range(len(trocadores_laco)):
				try:
					if dlg.dividir_calor.padrao.isChecked():
						valores[i] = valores_recomendados[i]
					elif dlg.dividir_calor.radio_set.isChecked():
						if i != trocador_removido:
							valores[i] = float(valor_trocador[0][i].text().replace(",", "."))
						else:
							valores[i] = 0
					elif dlg.dividir_calor.radio_add.isChecked():
						if i != trocador_removido:
							valores[i] = float(valor_trocador[1][i].text().replace(",", ".")) + matriz_completa_naomuda[trocadores_laco[i]-1][6]
						else:
							valores[i] = 0
				except:
					mensagem_erro("Specify all the values or select the standard method.")
					return

			matriz_completa = nao_sacrificar_matriz(matriz_completa_naomuda)

			corrente_quente = matriz_completa[trocadores_laco[trocador_removido]-1][0]
			corrente_fria = matriz_completa[trocadores_laco[trocador_removido]-1][1]
			ramo_quente = matriz_completa[trocadores_laco[trocador_removido]-1][2]
			ramo_frio = matriz_completa[trocadores_laco[trocador_removido]-1][3]
			estagio = matriz_completa[trocadores_laco[trocador_removido]-1][5]

			novas_divisoes, h = remover_ramo(matriz_completa, corrente_quente, corrente_fria, ramo_quente, ramo_frio, estagio, excecao=(trocadores_laco[trocador_removido]-1))

			for i in range(len(trocadores_laco)):
				matriz_completa[trocadores_laco[i]-1][6] = valores[i]

			for trocador in matriz_completa:
				if trocador[6] == 0:
					estagio = trocador[5]
					partir_estagio = trocador[4]
					matriz_completa.pop(matriz_completa.index(trocador))

			for trocador in matriz_completa:
				if trocador[4] > partir_estagio and trocador[5] == estagio:
					trocador[4] -= 1

			matriz_teste = inserir_trocador_ev(matriz_completa)

			matriz_completa = nao_sacrificar_matriz(matriz_teste)

			viola_agora = []
			for trocador in matriz_completa:
				if trocador[7] - trocador[8] < dTmin or trocador[9] - trocador[10] < dTmin:
					if not matriz_completa.index(trocador)+1 in trocadores_laco:
						viola_agora.append(matriz_completa.index(trocador))

			dlg.dividir_calor.botaodone.setEnabled(True)
			for i in range(len(trocadores_laco)):
				if i != trocador_removido:
					if i < trocador_removido:
						dt_quente = matriz_completa[trocadores_laco[i]-1][7]-matriz_completa[trocadores_laco[i]-1][8]
						dt_frio = matriz_completa[trocadores_laco[i]-1][9]-matriz_completa[trocadores_laco[i]-1][10]
					else:
						dt_quente = matriz_completa[trocadores_laco[i]-2][7]-matriz_completa[trocadores_laco[i]-2][8]
						dt_frio = matriz_completa[trocadores_laco[i]-2][9]-matriz_completa[trocadores_laco[i]-2][10]
					dtquente[i].setText(str('{:.2f}'.format(round(dt_quente, 2))))
					dtfrio[i].setText(str('{:.2f}'.format(round(dt_frio, 2))))
					if dt_quente < 0 or dt_frio < 0:
						# dlg.dividir_calor.botaodone.setEnabled(False)
						pass
					if dt_quente < dTmin:
						dtquente[i].setStyleSheet("QLabel {color: red; font: 1000 10pt 'MS Shell Dlg 2'}")
					else:
						dtquente[i].setStyleSheet("QLabel {color: black; font: 1000 10pt 'MS Shell Dlg 2'}")
					if dt_frio < dTmin:
						dtfrio[i].setStyleSheet("QLabel {color: red; font: 1000 10pt 'MS Shell Dlg 2'}")
					else:
						dtfrio[i].setStyleSheet("QLabel {color: black; font: 1000 10pt 'MS Shell Dlg 2'}")

			try:
				if ja_violava[0] != "None.":
					for lay in range(len(ja_violava)-1, -1, -1):
						layh[lay].removeWidget(novas_violacoes[lay])
						layh[lay].removeWidget(dt_quente_novo[lay])
						layh[lay].removeWidget(dt_frio_novo[lay])
						novas_violacoes[lay].setParent(None)
						dt_quente_novo[lay].setParent(None)
						dt_frio_novo[lay].setParent(None)
						dlg.dividir_calor.outras_violacoes.removeItem(layh[lay])
				else:
					dlg.dividir_calor.outras_violacoes.removeWidget(novas_violacoes)
					novas_violacoes.setParent(None)
			except:
				pass

			if len(viola_agora) != 0:
				novas_violacoes = [0] * len(viola_agora)
				dt_quente_novo = [0] * len(viola_agora)
				dt_frio_novo = [0] * len(viola_agora)
				layh = [0] * len(viola_agora)
				for i in range(len(viola_agora)):
					novas_violacoes[i] = QtWidgets.QLabel("E" + str(viola_agora[i]+1))
					novas_violacoes[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
					novas_violacoes[i].setAlignment(Qt.AlignCenter)
					novas_violacoes[i].setStyleSheet("QLabel {font: 1000 10pt 'MS Shell Dlg 2'}")
					dt_quente_novo[i] = QtWidgets.QLabel(str('{:.2f}'.format(round(matriz_completa[viola_agora[i]][7] - matriz_completa[viola_agora[i]][8], 2))))
					dt_quente_novo[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
					dt_quente_novo[i].setAlignment(Qt.AlignCenter)
					if matriz_completa[viola_agora[i]][7] - matriz_completa[viola_agora[i]][8] < dTmin:
						dt_quente_novo[i].setStyleSheet("QLabel {color: red; font: 1000 10pt 'MS Shell Dlg 2'}")
					else:
						dt_quente_novo[i].setStyleSheet("QLabel {color: black; font: 1000 10pt 'MS Shell Dlg 2'}")
					dt_frio_novo[i] = QtWidgets.QLabel(str('{:.2f}'.format(round(matriz_completa[viola_agora[i]][9] - matriz_completa[viola_agora[i]][10], 2))))
					dt_frio_novo[i].setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
					dt_frio_novo[i].setAlignment(Qt.AlignCenter)
					if matriz_completa[viola_agora[i]][9] - matriz_completa[viola_agora[i]][10] < dTmin:
						dt_frio_novo[i].setStyleSheet("QLabel {color: red; font: 1000 10pt 'MS Shell Dlg 2'}")
					else:
						dt_frio_novo[i].setStyleSheet("QLabel {color: black; font: 1000 10pt 'MS Shell Dlg 2'}")
					layh[i] = QtWidgets.QHBoxLayout()
					layh[i].addWidget(novas_violacoes[i])
					layh[i].addWidget(dt_quente_novo[i])
					layh[i].addWidget(dt_frio_novo[i])
					dlg.dividir_calor.outras_violacoes.addLayout(layh[i])
			else:
				novas_violacoes = QtWidgets.QLabel("None.")
				novas_violacoes.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
				novas_violacoes.setAlignment(Qt.AlignCenter)
				novas_violacoes.setStyleSheet("QLabel {font: 1000 10pt 'MS Shell Dlg 2'}")
				dlg.dividir_calor.outras_violacoes.addWidget(novas_violacoes)
				viola_agora.append("None.")

			ja_violava = []
			for i in range(len(viola_agora)):
				ja_violava.append(viola_agora[i])

			dlg.dividir_calor.botaodone.clicked.connect(lambda: done(matriz_completa, novas_divisoes))
			dlg.dividir_calor.botaoundone.clicked.connect(lambda: undone(matriz_completa_naomuda, divisoes_ev))

			def done(matriz_completa_done, novas_divisoes):
				global matriz_evolucao, divisoes_ev
				matriz_evolucao = nao_sacrificar_matriz(matriz_completa_done)
				divisoes_ev = nao_sacrificar_matriz(novas_divisoes)
				dlg.dividir_calor.close()
				wid_ambas.desenho.update()
				dlg.trocador_editar.removeItem(dlg.trocador_editar.count()-1)
				dlg.trocador_path.removeItem(dlg.trocador_path.count()-1)
				if todos:
					evolucao([], [], 1)
					dlg.lista_lacos.close()
				else:
					evolucao([], [], nivel)

			def undone(matriz_completa_undone, novas_divisoes):
				global matriz_evolucao, divisoes_ev
				remover_todos_ev()
				matriz_evolucao = nao_sacrificar_matriz(matriz_completa_undone)
				divisoes_ev = nao_sacrificar_matriz(novas_divisoes)
				if todos:
					evolucao([], [], "todos", True)
				else:
					evolucao([], [], nivel)

				dlg.dividir_calor.close()

		def liberar_bloquear(valor_trocador, acao, trocador_removido, placeholders):
			for i in range(len(valor_trocador[0])):
				if i != trocador_removido:
					if acao == "setar":
						valor_trocador[1][i].setEnabled(False)
						valor_trocador[0][i].setEnabled(True)
						valor_trocador[0][i].setPlaceholderText(placeholders[0][i])
						valor_trocador[1][i].setPlaceholderText("")
					elif acao == "add":
						valor_trocador[1][i].setEnabled(True)
						valor_trocador[0][i].setEnabled(False)
						valor_trocador[1][i].setPlaceholderText(placeholders[1][i])
						valor_trocador[0][i].setPlaceholderText("")
					else:
						valor_trocador[1][i].setEnabled(False)
						valor_trocador[0][i].setEnabled(False)
						valor_trocador[0][i].setPlaceholderText("")
						valor_trocador[1][i].setPlaceholderText("")

	global matriz_evolucao, divisoes_ev, primeira_evolucao, wid_ambas

	if not sub:
		if jogar_evolucao:
			matriz_acima = nao_sacrificar_matriz(matriz_acima_naomuda)
			matriz_abaixo = nao_sacrificar_matriz(matriz_abaixo_naomuda)
			try:
				matriz = criar_rede_completa(matriz_acima, matriz_abaixo, primeiro=True)
			except:
				mensagem_erro("Subnetwork Error. \nOne of them may have no Heat Exchanger.")
				return
			matriz_evolucao = nao_sacrificar_matriz(matriz)
			trocadores = criar_matriz(matriz_acima, matriz_abaixo)
			divisoes_ev = nao_sacrificar_matriz(divisoes)
			if primeira_evolucao:
				wid_ambas = wid_zoom([10000, 10000], "ambas")
				dlg.hen_ambas.addWidget(wid_ambas)
				primeira_evolucao = False
			else:
				wid_ambas.desenho.update()
			if dlg.trocador_editar.count() > 0:
				dlg.trocador_editar.clear()
				dlg.trocador_path.clear()
			for i in range(len(matriz_evolucao)):
				dlg.trocador_editar.addItem("E" + str(i+1))
				dlg.trocador_path.addItem("E" + str(i+1))
		else:
			matriz_acima_nm = []
			matriz_abaixo_nm = []
			for trocador in matriz_evolucao:
				if trocador[5] == 1:
					matriz_acima_nm.append(trocador)
				elif trocador[5] == 2:
					matriz_abaixo_nm.append(trocador)
			matriz_acima = nao_sacrificar_matriz(matriz_acima_nm)
			matriz_abaixo = nao_sacrificar_matriz(matriz_abaixo_nm)
			matriz = criar_rede_completa(matriz_acima, matriz_abaixo)
			matriz_evolucao = nao_sacrificar_matriz(matriz)
			trocadores = criar_matriz(matriz_acima, matriz_abaixo)
		incidencia = criar_incidencia(trocadores, n_quentes, n_frias)
		dlg.sugerir_path.clicked.connect(lambda: calcular_recomendado_violacao(dlg, matriz_evolucao[dlg.trocador_path.currentIndex()]))
		if todos:
			trocadores_laco = []
			for n in range(1, min(nhot, ncold)+1):
				trocadores_laco.append(sorted(lacos(incidencia, trocadores, n, todos)))
				if len(trocadores_laco[-1]) == 0:
					trocadores_laco.pop(-1)
		else:
			trocadores_laco = sorted(lacos(incidencia, trocadores, nivel, todos))
		if todos:
			interface_todos(trocadores_laco, matriz_evolucao)
		else:
			coisas_interface(trocadores_laco, matriz_evolucao)
			if trocadores_laco == ["None "] and nivel+1 <= min(n_quentes, n_frias):
				dlg.nivel.setCurrentIndex(nivel)
				evolucao([], [], nivel+1)
	else:
		matriz_acima = nao_sacrificar_matriz(matriz_acima_naomuda)
		matriz_abaixo = nao_sacrificar_matriz(matriz_abaixo_naomuda)
		try:
			matriz = criar_rede_completa(matriz_acima, matriz_abaixo, primeiro=True, sub=True)
		except:
			mensagem_erro("Subnetwork Error. \nOne of the Subnetworks has no Heat Exchangers.")
			return
		matriz_evolucao = nao_sacrificar_matriz(matriz)
		dlg.completa = uic.loadUi("rede_completa.ui")
		dlg.completa.showMaximized()
		wid_completa = wid_zoom([10000, 10000], "ambas")
		dlg.completa.hen_completa.addWidget(wid_completa)

def editar_calor(matriz_naomuda, trocador, calor, path=False):
	global matriz_evolucao, n_quentes, n_frias, divisoes_ev
	if calor == 0 and path:
		mensagem_erro("You must Specify a Heat Load greater than 0.")
		return
	if calor < 0:
		mensagem_erro("You must Specify a Heat Load greater than 0.")
		return
	if matriz_naomuda[trocador][6] - calor < 0 and path:
		mensagem_erro("Not able to remove more than the Heat Exchanger Heal Load.")
		return

	matriz = nao_sacrificar_matriz(matriz_naomuda)
	remover_todos_ev()
	ramo = [False, False]
	if (calor == 0 and not path) or ((matriz_naomuda[trocador][6] - calor == 0) and path):
		corrente_quente = matriz_naomuda[trocador][0]
		corrente_fria = matriz_naomuda[trocador][1]
		ramo_quente = matriz_naomuda[trocador][2]
		ramo_frio = matriz_naomuda[trocador][3]
		estagio = matriz_naomuda[trocador][5]
		dlg.trocadores_loop.setText("Requires new search")
		dlg.remover.setEnabled(False)
		divisoes_ev, ramo = remover_ramo(matriz, corrente_quente, corrente_fria, ramo_quente, ramo_frio, estagio, excecao=trocador)
		print()
		for d in divisoes_ev:
			print(d)
	if not path:
		if calor == 0:
			for i in range(len(matriz)):
				if matriz[trocador][4] < matriz[i][4] and matriz[trocador][5] == matriz[i][5]:
					matriz[i][4] -= 1
			matriz.pop(trocador)
			dlg.trocador_editar.removeItem(dlg.trocador_editar.count()-1)
			dlg.trocador_path.removeItem(dlg.trocador_path.count()-1)
		else:
			matriz[trocador][6] = calor
		matriz_teste = inserir_trocador_ev(matriz)
		matriz_evolucao = nao_sacrificar_matriz(matriz_teste)
		for t in matriz_evolucao:
			print(t)
	else:
		matriz_evolucao = nao_sacrificar_matriz(utilidade(matriz_naomuda, [trocador, calor], path=True, ramo=ramo))
		for i in range(2):
			dlg.trocador_path.addItem("E" + str(dlg.trocador_path.count()+1))
			dlg.trocador_editar.addItem("E" + str(dlg.trocador_editar.count()+1))

	wid_ambas.desenho.update()

def utilidade(matriz_naomuda, dados, path=False, ramo=[False, False]):
	global matriz_evolucao, n_quentes, n_frias
	matriz = nao_sacrificar_matriz(matriz_naomuda)
	if path:
		trocador = dados[0]
		calor = dados[1]
		corrente_quente = matriz_naomuda[trocador][0]
		corrente_fria = matriz_naomuda[trocador][1]
		if ramo[0]:
			sub_quente = 1
		else:
			sub_quente = matriz_naomuda[trocador][2]
		if ramo[1]:
			sub_fria = 1
		else:
			sub_fria = matriz_naomuda[trocador][3]
		matriz[trocador][6] = matriz_naomuda[trocador][6] - calor
		if round(matriz[trocador][6], 2) == 0:
			matriz.pop(trocador)
			dlg.trocador_path.removeItem(dlg.trocador_path.count()-1)
			dlg.trocador_editar.removeItem(dlg.trocador_editar.count()-1)
		tipo = ""
		dlg.calor_path.clear()
		dlg.calor_path.setPlaceholderText("-")
	else:
		oi = dlg.comboutil.currentText().split(" ")
		corrente = int(oi[1])
		sub = dlg.comboutil_sub.currentIndex()+1
		if oi[0] == "Hot":
			tipo = "Cold"
			calor = calor_atual_quente_ev[corrente-1]
			if quantidade_quente_ev_abaixo[corrente-1] < sub:
				if calor > 0.001:
					mensagem_erro("This Stream has only {} branch/branches. \nThe utility will be added to the Substream 1.".format(quantidade_quente_ev_abaixo[corrente-1]), titulo="Warning")
					sub = 1
		else:
			tipo = "Hot"
			calor = calor_atual_frio_ev[corrente-1]
			if quantidade_fria_ev_acima[corrente-1] < sub:
				if calor > 0.001:
						mensagem_erro("This Stream has only {} branch/branches. \nThe utility will be added to the Substream 1.".format(quantidade_fria_ev_acima[corrente-1]), titulo="Warning")
						sub = 1
		if calor < 0.001:
			mensagem_erro("There is no duty left for this stream. \nThe utility will not be added.")
			return
	if tipo == "Hot" or path:
		for trocadorr in matriz:
			if trocadorr[5] == 2:
				parar = matriz.index(trocadorr)
				break
			else:
				trocadorr[4] += 1
		matriz_reserva = nao_sacrificar_matriz(matriz[parar:])
		for i in range(parar, len(matriz)):
			matriz.pop(-1)
		if path:
			matriz.append([n_quentes, corrente_fria, 1, sub_fria, 1, 1, calor])
			dados_do_trocador_quente = [n_quentes, corrente_fria, 1, sub_fria, 1, 1, calor]
		else:
			matriz.append([n_quentes, corrente, 1, sub, 1, 1, calor])
			dados_do_trocador = [n_quentes, corrente, 1, sub, 1, 1, calor]
		for reserva in matriz_reserva:
			matriz.append(reserva)
	else: #somente util fria
		matriz.append([corrente, n_frias, sub, 1, matriz[-1][4]+1, 2, calor])
		dados_do_trocador = [corrente, n_frias, sub, 1, matriz[-1][4]+1, 2, calor]

	if path:
		matriz.append([corrente_quente, n_frias, sub_quente, 1, matriz[-1][4]+1, 2, calor])
		dados_do_trocador_fria = [corrente_quente, n_frias, sub_quente, 1, matriz[-1][4]+1, 2, calor]
	else:
		remover_todos_ev()

	quente = fria = 0
	for trocador in matriz:
		if tipo == "Hot" or path:
			if trocador[5] == 1 and trocador[0] == n_quentes:
				quente += 1
		if tipo == "Cold" or path:
			if trocador[5] == 2 and trocador[1] == n_frias:
				fria += 1

	if not path and dlg.dividir_utilidade.isChecked():
		if tipo == "Hot" and quente > 1:
			matriz = divisao_de_utilidades(tipo, dados_do_trocador[0], dados_do_trocador, ambas=True, m=matriz)
		if tipo == "Cold" and fria > 1:
			matriz = divisao_de_utilidades(tipo, dados_do_trocador[1], dados_do_trocador, ambas=True, m=matriz)


	if path and dlg.dividir_utilidade2.isChecked():
		if quente > 1:
			matriz = divisao_de_utilidades("quente", dados_do_trocador_quente[0], dados_do_trocador_quente, ambas=True, m=matriz)
		if fria > 1:
			matriz = divisao_de_utilidades("fria", dados_do_trocador_fria[1], dados_do_trocador_fria, ambas=True, m=matriz)

	matriz_teste = inserir_trocador_ev(matriz)

	if path:
		return matriz_teste
	else:
		matriz_evolucao = nao_sacrificar_matriz(matriz_teste)
		# desenhar_rede(correntes_quentes, correntes_frias, "ambas")
		wid_ambas.desenho.update()
		dlg.trocador_editar.addItem("E" + str(dlg.trocador_editar.count()+1))
		dlg.trocador_path.addItem("E" + str(dlg.trocador_path.count()+1))

def remover_ramo(matriz_completa, corrente_quente, corrente_fria, ramo_quente, ramo_frio, estagio, excecao=-1):
	ainda_tem_quente, ainda_tem_frio = False, False
	ramoo = [True, True]
	remove_quente, remove_fria = False, False
	for trocador in matriz_completa:
		if matriz_completa.index(trocador) != excecao and trocador[5] == estagio:
			if ramo_quente == trocador[2] and corrente_quente == trocador[0]:
				ainda_tem_quente = True
				ramoo[0] = False
			if ramo_frio == trocador[3] and corrente_fria == trocador[1]:
				ainda_tem_frio = True
				ramoo[1] = False

	remover_todos_ev()

	novas_divisoes = nao_sacrificar_matriz(divisoes_ev)

	if not ainda_tem_quente:
		for divisao in novas_divisoes:
			if divisao[0] == "Q" and divisao[1] == estagio and divisao[2] == corrente_quente:
				total = 0
				for ramo in range(divisao[3]):
					if ramo+1 != ramo_quente:
						total += divisao[4][ramo]
				fracao = []
				for ramo in range(divisao[3]):
					if ramo+1 != ramo_quente:
						proporcao = divisao[4][ramo] / total
						fracao.append(divisao[4][ramo] + proporcao * divisao[4][ramo_quente-1])
						if ramo+1 > ramo_quente:
							for trocador in matriz_completa:
								if trocador[0] == corrente_quente and trocador[2] == ramo+1 and trocador[5] == estagio:
									trocador[2] -= 1
				divisao_de_correntes_ev("Q", estagio, corrente_quente, len(fracao), fracao)
				if len(fracao) != 1:
					novas_divisoes[novas_divisoes.index(divisao)] = ["Q", estagio, corrente_quente, len(fracao), fracao]
				else:
					remove_quente = True
					indice_quente = novas_divisoes.index(divisao)

	if not ainda_tem_frio:
		for divisao in novas_divisoes:
			if divisao[0] == "F" and divisao[1] == estagio and divisao[2] == corrente_fria:
				total = 0
				for ramo in range(divisao[3]):
					if ramo+1 != ramo_frio:
						total += divisao[4][ramo]
				fracao = []
				for ramo in range(divisao[3]):
					if ramo+1 != ramo_frio:
						proporcao = divisao[4][ramo] / total
						fracao.append(divisao[4][ramo] + proporcao * divisao[4][ramo_frio-1])
						if ramo+1 > ramo_frio:
							for trocador in matriz_completa:
								if trocador[1] == corrente_fria and trocador[3] == ramo+1 and trocador[5] == estagio:
									trocador[3] -= 1
				divisao_de_correntes_ev("F", estagio, corrente_fria, len(fracao), fracao)
				if len(fracao) != 1:
					novas_divisoes[novas_divisoes.index(divisao)] = ["F", estagio, corrente_fria, len(fracao), fracao]
				else:
					remove_fria = True
					indice_fria = novas_divisoes.index(divisao)

	if remove_quente:
		if remove_fria:
			if indice_fria < indice_quente:
				indice_quente -= 1
		novas_divisoes.pop(indice_quente)
	if remove_fria:
		if remove_quente:
			if indice_quente < indice_fria:
				indice_fria -= 1
		novas_divisoes.pop(indice_fria)

	return novas_divisoes, ramoo



#above
def printar():
	dlg.tableWidget_3.clearContents()
	dlg.tableWidget_4.clearContents()

	pinch_quente_texto = "Hot Pinch Temperature: " + str(pinchq)
	pinch_frio_texto = "Cold Pinch Temperature: " + str(pinchf)

	dlg.label_15.setText(pinch_quente_texto)
	dlg.label_12.setText(pinch_frio_texto)

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
					dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0[corrente], 2)))))
					if corrente_quente_presente_acima[corrente]:
						dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente[corrente][sub], 2)))))
						dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf_acima[corrente], 2)))))
						dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente_sub[corrente][sub], 2)))))
					else:
						dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_3.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0[corrente], 2)))))
				if corrente_quente_presente_acima[corrente]:
					dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente_mesclada[corrente], 2)))))
					dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf_acima[corrente], 2)))))
					dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente[corrente], 2)))))
				else:
					dlg.tableWidget_3.setItem(linha, 1, QTableWidgetItem("-"))
					dlg.tableWidget_3.setItem(linha, 2, QTableWidgetItem("-"))
					dlg.tableWidget_3.setItem(linha, 3, QTableWidgetItem("-"))
					dlg.tableWidget_3.setItem(linha, 4, QTableWidgetItem("-"))
				linha += 1
	else:
		dlg.tableWidget_3.setRowCount(nhot)
		for corrente in range(nhot):
			dlg.tableWidget_3.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
			dlg.tableWidget_3.setItem(corrente, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0[corrente], 2)))))
			if corrente_quente_presente_acima[corrente]:
				dlg.tableWidget_3.setItem(corrente, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente_mesclada[corrente], 2)))))
				dlg.tableWidget_3.setItem(corrente, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf_acima[corrente], 2)))))
				dlg.tableWidget_3.setItem(corrente, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente[corrente], 2)))))
			else:
				dlg.tableWidget_3.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_3.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_3.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_3.setItem(corrente, 4, QTableWidgetItem("-"))

	try:
		for corrente in range(nhot*ncold):
			for j in range(5):
				item = dlg.tableWidget_3.item(corrente, j)
				item.setTextAlignment(Qt.AlignCenter)
	except:
		pass

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
					dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf[corrente], 2)))))
					if corrente_fria_presente_acima[corrente]:
						dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria[corrente][sub], 2)))))
						dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0_acima[corrente], 2)))))
						dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio_sub[corrente][sub], 2)))))
					else:
						dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_4.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf[corrente], 2)))))
				if corrente_fria_presente_acima[corrente]:
					dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria_mesclada[corrente], 2)))))
					dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0_acima[corrente], 2)))))
					dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio[corrente], 2)))))
				else:
					dlg.tableWidget_4.setItem(linha, 1, QTableWidgetItem("-"))
					dlg.tableWidget_4.setItem(linha, 2, QTableWidgetItem("-"))
					dlg.tableWidget_4.setItem(linha, 3, QTableWidgetItem("-"))
					dlg.tableWidget_4.setItem(linha, 4, QTableWidgetItem("-"))
				linha += 1
	else:
		dlg.tableWidget_4.setRowCount(ncold)
		for corrente in range(ncold):
			dlg.tableWidget_4.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
			dlg.tableWidget_4.setItem(corrente, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf[corrente], 2)))))
			if corrente_fria_presente_acima[corrente]:
				dlg.tableWidget_4.setItem(corrente, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria_mesclada[corrente], 2)))))
				dlg.tableWidget_4.setItem(corrente, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0_acima[corrente], 2)))))
				dlg.tableWidget_4.setItem(corrente, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio[corrente], 2)))))
			else:
				dlg.tableWidget_4.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_4.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_4.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_4.setItem(corrente, 4, QTableWidgetItem("-"))

	try:
		for corrente in range(nhot*ncold):
			for j in range(5):
				item = dlg.tableWidget_4.item(corrente, j)
				item.setTextAlignment(Qt.AlignCenter)
	except:
		pass

	dlg.tableWidget_2.setRowCount(len(matriz_armazenada))
	if len(matriz_armazenada) > 0:
		for trocador in range(0, len(matriz_armazenada)):
			dlg.tableWidget_2.setItem(trocador, 0, QTableWidgetItem(str(matriz_armazenada[trocador][0]))) #chot
			dlg.tableWidget_2.setItem(trocador, 1, QTableWidgetItem(str(matriz_armazenada[trocador][1]))) #ccold
			dlg.tableWidget_2.setItem(trocador, 2, QTableWidgetItem(str(matriz_armazenada[trocador][2]))) #sbhot
			dlg.tableWidget_2.setItem(trocador, 3, QTableWidgetItem(str(matriz_armazenada[trocador][3]))) #sbcold
			dlg.tableWidget_2.setItem(trocador, 4, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][6], 2))))) #calor trocador
			dlg.tableWidget_2.setItem(trocador, 5, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][7], 2))))) #thin
			dlg.tableWidget_2.setItem(trocador, 6, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][8], 2))))) #tcout
			dlg.tableWidget_2.setItem(trocador, 7, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][9], 2))))) #Thout
			dlg.tableWidget_2.setItem(trocador, 8, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][10], 2))))) #Tcin
			dlg.tableWidget_2.setItem(trocador, 9, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][11], 2))))) #fração hot
			dlg.tableWidget_2.setItem(trocador, 10, QTableWidgetItem(str('{:.2f}'.format(round(matriz_armazenada[trocador][12], 2))))) #fraçao cold
			for j in range(11):
				item = dlg.tableWidget_2.item(trocador, j)
				item.setTextAlignment(Qt.AlignCenter)

	if len(utilidades) > 0:
		dlg.tableWidget_2.setRowCount(len(matriz_armazenada) + len(utilidades))
		for utilidade in range(0, len(utilidades)):
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 0, QTableWidgetItem(str("Hot Utility")))
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 1, QTableWidgetItem(str(utilidades[utilidade][0])))
			dlg.tableWidget_2.setItem(len(matriz_armazenada) + utilidade, 4, QTableWidgetItem(str('{:.2f}'.format(round(utilidades[utilidade][1], 2)))))
			for j in range(11):
				if j == 0 or j == 1 or j == 4:
					item = dlg.tableWidget_2.item(utilidade + len(matriz_armazenada), j)
					item.setTextAlignment(Qt.AlignCenter)

def inserir_teste():
	global subestagio_trocador, matriz_armazenada, primeira_util
	dados_do_trocador = ler_dados(dlg, subestagio_trocador)

	if not corrente_quente_presente_acima[dados_do_trocador[0]-1]:
		mensagem_erro("This hot stream is not present in the above subnetwork.")
		return
	if not corrente_fria_presente_acima[dados_do_trocador[1]-1]:
		mensagem_erro("This cold stream is not present in the above subnetwork.")
		return

	if dados_do_trocador[2] > quantidade_quente[dados_do_trocador[0]-1]:
		mensagem_erro("The hot stream has not this many branches.")
		return
	elif dados_do_trocador[3] > quantidade_fria[dados_do_trocador[1]-1]:
		mensagem_erro("The cold stream has not this many branches.")
		return

	if not e_utilidade_quente[dados_do_trocador[0]-1] and ((dados_do_trocador[6] <= 0 and not dlg.radioButton_4.isChecked()) or (dados_do_trocador[6] < 0.001 and dlg.radioButton_4.isChecked())):
		mensagem_erro("The input heat must be greater than 0.")
		return

	insere_sim = True
	if e_utilidade_quente[dados_do_trocador[0]-1]:
		if not primeira_util:
			if dlg.radioButton_4.isChecked():
				dados_do_trocador[6] = max(dados_do_trocador[6], calor_atual_frio_sub[dados_do_trocador[1]-1][dados_do_trocador[3]-1])
			divisao_de_utilidades("quente", dados_do_trocador[0], dados_do_trocador)
			insere_sim = False
		else:
			primeira_util = False

	if not e_utilidade_quente[dados_do_trocador[0]-1] or insere_sim:
		matriz_armazenada, inseriu = inserir_trocador(dlg, dados_do_trocador)
		if inseriu:
			if (matriz_armazenada[-1][7] - matriz_armazenada[-1][8]) < dTmin or (matriz_armazenada[-1][9] - matriz_armazenada[-1][10]) < dTmin:
				trocador_violado = matriz_armazenada[-1][:6]
				trocador_violado.append(matriz_armazenada[-1][7] - matriz_armazenada[-1][8])
				trocador_violado.append(matriz_armazenada[-1][9] - matriz_armazenada[-1][10])
				violou_dtmin(trocador_violado, "above", dados_do_trocador)
			printar()
			checaresgotadosacima()
			dlg.trocador_acima.addItem("E" + str(subestagio_trocador))
			dlg.trocador_acima.setCurrentIndex(dlg.trocador_acima.count()-1)
			wid_acima.desenho.update()
			subestagio_trocador += 1

def remover_teste():
	global subestagio_trocador
	indice_remover = dlg.trocador_acima.currentIndex()
	if indice_remover >= len(matriz_armazenada) - 1:
		remover_anteriores("acima", indice_remover, True)
	else:
		remover_anteriores("acima", indice_remover)

def utilidade_teste_acima():
	global utilidades
	if dlg.tab_acima.currentIndex() == 1:
		corrente = int(dlg.comboBox_10.currentText())
	else:
		corrente = int(dlg.corrente_acima.currentIndex()+1)
	try:
		utilidades = adicionar_utilidade(dlg, corrente)
		utilidades.sort()
	except:
		print("erro utilidade teste acima")
	printar()
	checaresgotadosacima()
	dlg.trocador_acima.addItem("H" + str(len(utilidades)))
	dlg.trocador_acima.setCurrentIndex(dlg.trocador_acima.count()-1)
	wid_acima.desenho.update()

def calcular_calor_teste():
	dlg.TempLoadAbove=uic.loadUi("TempLoad.ui")
	dlg.TempLoadAbove.show()
	dlg.TempLoadAbove.radioButton_2.setText("Inlet Hot Temperature")
	dlg.TempLoadAbove.radioButton.setText("Outlet Cold Temperature")

	for i in range(nhot):
		dlg.TempLoadAbove.comboBox.addItem(str(i+1))
	for i in range(ncold):
		dlg.TempLoadAbove.comboBox_2.addItem(str(i+1))

	dlg.TempLoadAbove.comboBox.setCurrentText(str(dlg.comboBox_2.currentText()))
	dlg.TempLoadAbove.comboBox_2.setCurrentText(str(dlg.comboBox_5.currentText()))
	dlg.TempLoadAbove.comboBox_3.setCurrentText(str(dlg.comboBox_50.currentText()))
	dlg.TempLoadAbove.comboBox_4.setCurrentText(str(dlg.comboBox_51.currentText()))

	dlg.TempLoadAbove.pushButton_2.clicked.connect(lambda: dlg.TempLoadAbove.close())
	dlg.TempLoadAbove.pushButton.clicked.connect(lambda: caixa_de_temperatura(dlg, len(matriz_armazenada)))

def checaresgotadosacima():
	contadordutycold = 0
	contadordutyhot = 0

	for corrente in range(nhot):
		if round(calor_atual_quente[corrente], 2) == 0:
			contadordutyhot += 1
	for corrente in range(ncold):
		if round(calor_atual_frio[corrente], 2) == 0:
			contadordutycold += 1

	objetivo_quente = nhot
	objetivo_frio = ncold


	if contadordutyhot == objetivo_quente:
		dlg.comboBox_10.setEnabled(True)
		dlg.pushButton_8.setEnabled(True)
		dlg.corrente_acima.setEnabled(True)
		dlg.addutil_acima.setEnabled(True)
	else:
		dlg.comboBox_10.setEnabled(False)
		dlg.pushButton_8.setEnabled(False)
		dlg.corrente_acima.setEnabled(False)
		dlg.addutil_acima.setEnabled(False)

	if contadordutycold == objetivo_frio:
		dlg.comboBox_9.setEnabled(True)
		dlg.pushButton_7.setEnabled(True)
	else:
		dlg.comboBox_9.setEnabled(False)
		dlg.pushButton_7.setEnabled(False)

	if contadordutyhot == objetivo_quente and contadordutycold == objetivo_frio:
		dlg.comboBox_9.setEnabled(False)
		dlg.comboBox_10.setEnabled(False)
		dlg.pushButton_7.setEnabled(False)
		dlg.pushButton_8.setEnabled(False)
		dlg.corrente_acima.setEnabled(False)
		dlg.addutil_acima.setEnabled(False)


#below
def printar_abaixo():
	dlg.tableWidget_15.clearContents()
	dlg.tableWidget_17.clearContents()

	pinch_quente_texto = "Hot Pinch Temperature: " + str(pinchq)
	pinch_frio_texto = "Cold Pinch Temperature: " + str(pinchf)

	dlg.label_17.setText(pinch_quente_texto)
	dlg.label_21.setText(pinch_frio_texto)

	if dlg.checkBox_9.isChecked():
		linha = 0
		linhas = 0
		for i in quantidade_quente_abaixo:
			linhas += i
		dlg.tableWidget_15.setRowCount(linhas)
		for corrente in range(nhot):
			if dividida_quente_abaixo[corrente]:
				for sub in range(quantidade_quente_abaixo[corrente]):
					text = str(corrente+1) + "." + str(sub+1)
					dlg.tableWidget_15.setItem(linha, 0, QTableWidgetItem(text))
					dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0_abaixo[corrente], 2)))))
					if corrente_quente_presente_abaixo[corrente]:
						dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente_abaixo[corrente][sub], 2)))))
						dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf[corrente], 2)))))
						dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente_sub_abaixo[corrente][sub], 2)))))
					else:
						dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_15.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0_abaixo[corrente], 2)))))
				if corrente_quente_presente_abaixo[corrente]:
					dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente_mesclada_abaixo[corrente], 2)))))
					dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf[corrente], 2)))))
					dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente_abaixo[corrente], 2)))))
				else:
					dlg.tableWidget_15.setItem(linha, 1, QTableWidgetItem("-"))
					dlg.tableWidget_15.setItem(linha, 2, QTableWidgetItem("-"))
					dlg.tableWidget_15.setItem(linha, 3, QTableWidgetItem("-"))
					dlg.tableWidget_15.setItem(linha, 4, QTableWidgetItem("-"))

				linha += 1
	else:
		dlg.tableWidget_15.setRowCount(nhot)
		for corrente in range(nhot):
			dlg.tableWidget_15.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
			dlg.tableWidget_15.setItem(corrente, 1, QTableWidgetItem(str('{:.2f}'.format(round(Th0_abaixo[corrente], 2)))))
			if corrente_quente_presente_abaixo[corrente]:
				dlg.tableWidget_15.setItem(corrente, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_quente_mesclada_abaixo[corrente], 2)))))
				dlg.tableWidget_15.setItem(corrente, 3, QTableWidgetItem(str('{:.2f}'.format(round(Thf[corrente], 2)))))
				dlg.tableWidget_15.setItem(corrente, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_quente_abaixo[corrente], 2)))))
			else:
				dlg.tableWidget_15.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_15.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_15.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_15.setItem(corrente, 4, QTableWidgetItem("-"))

	try:
		for corrente in range(nhot*ncold):
			for j in range(5):
				item = dlg.tableWidget_15.item(corrente, j)
				item.setTextAlignment(Qt.AlignCenter)
	except:
		pass

	if dlg.checkBox_10.isChecked():
		linha = 0
		linhas = 0
		for i in quantidade_fria_abaixo:
			linhas += i
		dlg.tableWidget_17.setRowCount(linhas)
		for corrente in range(ncold):
			if dividida_fria_abaixo[corrente]:
				for sub in range(quantidade_fria_abaixo[corrente]):
					text = str(corrente+1) + "." + str(sub+1)
					dlg.tableWidget_17.setItem(linha, 0, QTableWidgetItem(text))
					dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf_abaixo[corrente], 2)))))
					if corrente_fria_presente_abaixo[corrente]:
						dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria_abaixo[corrente][sub], 2)))))
						dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0[corrente], 2)))))
						dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio_sub_abaixo[corrente][sub], 2)))))
					else:
						dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem("-"))
						dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem("-"))
						dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem("-"))
						dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem("-"))
					linha += 1
			else:
				dlg.tableWidget_17.setItem(linha, 0, QTableWidgetItem(str(corrente+1)))
				dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf_abaixo[corrente], 2)))))
				if corrente_fria_presente_abaixo[corrente]:
					dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria_mesclada_abaixo[corrente], 2)))))
					dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0[corrente], 2)))))
					dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio_abaixo[corrente], 2)))))
				else:
					dlg.tableWidget_17.setItem(linha, 1, QTableWidgetItem("-"))
					dlg.tableWidget_17.setItem(linha, 2, QTableWidgetItem("-"))
					dlg.tableWidget_17.setItem(linha, 3, QTableWidgetItem("-"))
					dlg.tableWidget_17.setItem(linha, 4, QTableWidgetItem("-"))
				linha += 1
	else:
		dlg.tableWidget_17.setRowCount(ncold)
		for corrente in range(ncold):
			dlg.tableWidget_17.setItem(corrente, 0, QTableWidgetItem(str(corrente+1)))
			dlg.tableWidget_17.setItem(corrente, 1, QTableWidgetItem(str('{:.2f}'.format(round(Tcf_abaixo[corrente], 2)))))
			if corrente_fria_presente_abaixo[corrente]:
				dlg.tableWidget_17.setItem(corrente, 2, QTableWidgetItem(str('{:.2f}'.format(round(temperatura_atual_fria_mesclada_abaixo[corrente], 2)))))
				dlg.tableWidget_17.setItem(corrente, 3, QTableWidgetItem(str('{:.2f}'.format(round(Tc0[corrente], 2)))))
				dlg.tableWidget_17.setItem(corrente, 4, QTableWidgetItem(str('{:.2f}'.format(round(calor_atual_frio_abaixo[corrente], 2)))))
			else:
				dlg.tableWidget_17.setItem(corrente, 1, QTableWidgetItem("-"))
				dlg.tableWidget_17.setItem(corrente, 2, QTableWidgetItem("-"))
				dlg.tableWidget_17.setItem(corrente, 3, QTableWidgetItem("-"))
				dlg.tableWidget_17.setItem(corrente, 4, QTableWidgetItem("-"))

	try:
		for corrente in range(nhot*ncold):
			for j in range(5):
				item = dlg.tableWidget_17.item(corrente, j)
				item.setTextAlignment(Qt.AlignCenter)
	except:
		pass

	dlg.tableWidget_14.setRowCount(len(matriz_trocadores_abaixo))
	if len(matriz_trocadores_abaixo) > 0:
		for trocador in range(0, len(matriz_trocadores_abaixo)):
			dlg.tableWidget_14.setItem(trocador, 0, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][0]))) #chot
			dlg.tableWidget_14.setItem(trocador, 1, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][1]))) #ccold
			dlg.tableWidget_14.setItem(trocador, 2, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][2]))) #sbhot
			dlg.tableWidget_14.setItem(trocador, 3, QTableWidgetItem(str(matriz_trocadores_abaixo[trocador][3]))) #sbcold
			dlg.tableWidget_14.setItem(trocador, 4, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][6], 2))))) # calor trocado
			dlg.tableWidget_14.setItem(trocador, 5, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][9], 2))))) #Thin
			dlg.tableWidget_14.setItem(trocador, 6, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][10], 2))))) #Tcout
			dlg.tableWidget_14.setItem(trocador, 7, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][7], 2))))) #Thout
			dlg.tableWidget_14.setItem(trocador, 8, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][8], 2))))) #Tcin
			dlg.tableWidget_14.setItem(trocador, 9, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][11], 2))))) #fração hot
			dlg.tableWidget_14.setItem(trocador, 10, QTableWidgetItem(str('{:.2f}'.format(round(matriz_trocadores_abaixo[trocador][12], 2))))) #fraçao cold
			for j in range(11):
				item = dlg.tableWidget_14.item(trocador, j)
				item.setTextAlignment(Qt.AlignCenter)

	if len(utilidades_abaixo) > 0:
		dlg.tableWidget_14.setRowCount(len(matriz_trocadores_abaixo) + len(utilidades_abaixo))
		for utilidade in range(0, len(utilidades_abaixo)):
			dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 1, QTableWidgetItem(str("Cold Utility")))
			dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 0, QTableWidgetItem(str(utilidades_abaixo[utilidade][0])))
			dlg.tableWidget_14.setItem(len(matriz_trocadores_abaixo) + utilidade, 4, QTableWidgetItem(str('{:.2f}'.format(round(utilidades_abaixo[utilidade][1], 2)))))
			for j in range(11):
				if j == 0 or j == 1 or j == 4:
					item = dlg.tableWidget_14.item(utilidade + len(matriz_trocadores_abaixo), j)
					item.setTextAlignment(Qt.AlignCenter)

def inserir_teste_abaixo():
	global subestagio_trocador_abaixo, matriz_trocadores_abaixo, primeira_util_fria
	dados_do_trocador = ler_dados_abaixo(dlg, subestagio_trocador_abaixo)

	if not corrente_quente_presente_abaixo[dados_do_trocador[0]-1]:
		mensagem_erro("This hot stream is not present in the below subnetwork.")
		return
	if not corrente_fria_presente_abaixo[dados_do_trocador[1]-1]:
		mensagem_erro("This cold stream is not present in the below subnetwork.")
		return

	if dados_do_trocador[2] > quantidade_quente_abaixo[dados_do_trocador[0]-1]:
		mensagem_erro("The hot stream has not this many branches.")
		return
	elif dados_do_trocador[3] > quantidade_fria_abaixo[dados_do_trocador[1]-1]:
		mensagem_erro("The cold stream has not this many branches.")
		return

	if not e_utilidade_fria[dados_do_trocador[1]-1] and ((dados_do_trocador[6] <= 0 and not dlg.radioButton_20.isChecked()) or (dados_do_trocador[6] < 0.001 and dlg.radioButton_20.isChecked())):
		mensagem_erro("The input heat must be greater than 0.")
		return

	insere_sim = True
	if e_utilidade_fria[dados_do_trocador[1]-1]:
		if not primeira_util_fria:
			if dlg.radioButton_20.isChecked():
				dados_do_trocador[6] = max(dados_do_trocador[6], calor_atual_quente_sub_abaixo[dados_do_trocador[0]-1][dados_do_trocador[2]-1])
			divisao_de_utilidades("fria", dados_do_trocador[1], dados_do_trocador)
			insere_sim = False
		else:
			primeira_util_fria = False

	if not e_utilidade_fria[dados_do_trocador[1]-1] or insere_sim:
		matriz_trocadores_abaixo, inseriu = inserir_trocador_abaixo(dlg, dados_do_trocador)
		if inseriu:
			if (matriz_trocadores_abaixo[-1][7] - matriz_trocadores_abaixo[-1][8]) < dTmin or (matriz_trocadores_abaixo[-1][9] - matriz_trocadores_abaixo[-1][10]) < dTmin:
				trocador_violado = matriz_trocadores_abaixo[-1][:6]
				trocador_violado.append(matriz_trocadores_abaixo[-1][9] - matriz_trocadores_abaixo[-1][10])
				trocador_violado.append(matriz_trocadores_abaixo[-1][7] - matriz_trocadores_abaixo[-1][8])
				violou_dtmin(trocador_violado, "below", dados_do_trocador)
			printar_abaixo()
			checaresgotadosabaixo()
			dlg.trocador_abaixo.addItem("E" + str(subestagio_trocador_abaixo))
			dlg.trocador_abaixo.setCurrentIndex(dlg.trocador_abaixo.count()-1)
			wid_abaixo.desenho.update()
			subestagio_trocador_abaixo += 1

def remover_teste_abaixo():
	global subestagio_trocador_abaixo
	indice_remover = dlg.trocador_abaixo.currentIndex()
	if indice_remover >= len(matriz_trocadores_abaixo) - 1:
		remover_anteriores("abaixo", indice_remover, True)
	else:
		remover_anteriores("abaixo", indice_remover)

def utilidade_teste_abaixo():
	global utilidades_abaixo
	if dlg.tab_abaixo.currentIndex() == 1:
		corrente = int(dlg.comboBox_43.currentText())
	else:
		corrente = int(dlg.corrente_abaixo.currentIndex()+1)
	try:
		utilidades_abaixo = adicionar_utilidade_abaixo(dlg, corrente)
		utilidades_abaixo.sort()
	except:
		print("utilidade teste abaixo")
	printar_abaixo()
	checaresgotadosabaixo()
	dlg.trocador_abaixo.addItem("C" + str(len(utilidades_abaixo)))
	dlg.trocador_abaixo.setCurrentIndex(dlg.trocador_abaixo.count()-1)
	wid_abaixo.desenho.update()

def calcular_calor_abaixo():
	dlg.TempLoadBelow = uic.loadUi("TempLoad.ui")
	dlg.TempLoadBelow.show()
	dlg.TempLoadBelow.radioButton_2.setText("Outlet Hot Temperature")
	dlg.TempLoadBelow.radioButton.setText("Inlet Cold Temperature")

	for i in range(nhot):
		dlg.TempLoadBelow.comboBox.addItem(str(i+1))
	for i in range(ncold):
		dlg.TempLoadBelow.comboBox_2.addItem(str(i+1))

	dlg.TempLoadBelow.comboBox.setCurrentText(str(dlg.comboBox_35.currentText()))
	dlg.TempLoadBelow.comboBox_2.setCurrentText(str(dlg.comboBox_36.currentText()))
	dlg.TempLoadBelow.comboBox_3.setCurrentText(str(dlg.comboBox_53.currentText()))
	dlg.TempLoadBelow.comboBox_4.setCurrentText(str(dlg.comboBox_54.currentText()))


	dlg.TempLoadBelow.pushButton.clicked.connect(lambda: caixa_de_temperatura_abaixo(dlg, len(matriz_trocadores_abaixo)))
	dlg.TempLoadBelow.pushButton_2.clicked.connect(lambda: dlg.TempLoadBelow.close())

def checaresgotadosabaixo():
	contadordutyhot=0
	contadordutycold=0

	for corrente in range(nhot):
		if round(calor_atual_quente_abaixo[corrente], 2) == 0:
			contadordutyhot += 1
	for corrente in range(ncold):
		if round(calor_atual_frio_abaixo[corrente], 2) == 0:
			contadordutycold += 1

	objetivo_quente = nhot
	objetivo_frio = ncold

	if contadordutyhot == objetivo_quente:
		dlg.comboBox_44.setEnabled(True)
		dlg.pushButton_21.setEnabled(True)
	else:
		dlg.comboBox_44.setEnabled(False)
		dlg.pushButton_21.setEnabled(False)

	if contadordutycold == objetivo_frio:
		dlg.comboBox_43.setEnabled(True)
		dlg.pushButton_20.setEnabled(True)
		dlg.corrente_abaixo.setEnabled(True)
		dlg.addutil_abaixo.setEnabled(True)
	else:
		dlg.comboBox_43.setEnabled(False)
		dlg.pushButton_20.setEnabled(False)
		dlg.corrente_abaixo.setEnabled(False)
		dlg.addutil_abaixo.setEnabled(False)

	if contadordutyhot == objetivo_quente and contadordutycold == objetivo_frio:
		dlg.comboBox_43.setEnabled(False)
		dlg.comboBox_44.setEnabled(False)
		dlg.pushButton_20.setEnabled(False)
		dlg.pushButton_21.setEnabled(False)
		dlg.corrente_abaixo.setEnabled(False)
		dlg.addutil_abaixo.setEnabled(False)



#dtmin optimization
def eq():

	if verificar_digitos(dlg.dtstep):
		mensagem_erro("The limit is 4 digits after the separator.\nChange the step value and try again.")
		return
	if verificar_digitos(dlg.dtstart):
		mensagem_erro("The limit is 4 digits after the separator.\nChange the start value and try again.")
		return
	if verificar_digitos(dlg.dtstop):
		mensagem_erro("The limit is 4 digits after the separator.\nChange the stop value and try again.")
		return

	start = float(dlg.dtstart.text().replace(",", "."))
	step = float(dlg.dtstep.text().replace(",", "."))
	stop = float(dlg.dtstop.text().replace(",", "."))


	if stop < start:
		mensagem_erro("The stop value needs to be higher than the start value.\nChange one of them and try again.")
		return

	if len(np.arange(start, stop + step, step))>500:
		msgBox = QMessageBox()
		msgBox.setIcon(QMessageBox.Information)
		msgBox.setWindowTitle("This may take some time")
		msgBox.setText("You will run about "+ str(len(np.arange(start, stop + step, step))) +" iteractions\nDo you want to proceed?")
		msgBox.setStyleSheet("font-weight: bold")
		msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

		returnValue = msgBox.exec()
		if returnValue == QMessageBox.Cancel:
			return 0

	dlg.equation = uic.loadUi("Select.ui")
	dlg.equation.show()

	def z3():
		if dlg.equation.nareas.isChecked():
			nnn = -1
			otimizafun(nnn)
		elif dlg.equation.us1.isChecked():
			nnn = -2
			otimizafun(nnn)
		elif dlg.equation.esp.isChecked():
			nnn = float(dlg.equation.lineesp.text())
			otimizafun(nnn)
		dlg.equation.close()

	dlg.equation.otimizarun.clicked.connect(lambda: z3())

def otimizafun(nnn):
	start = float(dlg.dtstart.text().replace(",", "."))
	step = float(dlg.dtstep.text().replace(",", "."))
	stop = float(dlg.dtstop.text().replace(",", "."))

	global variadt, yplot, custoopano, custocapital, custocapitalanual, custototanual,uf,uq,dtopt

	contador = 0
	for i in range(len(util_temporaria)):
		if util_temporaria[i][3] == 'Cold':
			correntes_temporaria.append(util_temporaria[i])
			contador += 1
		else:
			correntes_temporaria.append(util_temporaria[i])
			contador += 1

	uf, uq, variadt, yplot, custoopano, custocapital, custocapitalanual, custototanual = varia(start, step, stop, correntes_temporaria, nnn)

	for i in range(contador):
		correntes_temporaria.pop(-1)

	changedv = []
	changedv.append(variadt[0])

	for i in range(0,len(custocapitalanual)):
		try:
			changedv.append(variadt[i+1])
		except:
			pass

	Custoopotimizado = custoopano[custototanual.index(min(custototanual))]
	cccapitalanualopt = custocapitalanual[custototanual.index(min(custototanual))]
	dtopt = variadt[custototanual.index(min(custototanual))]
	cccapitalopt = custocapital[custototanual.index(min(custototanual))]
	areaopt = yplot[custototanual.index(min(custototanual))]
	custototanualopt = min(custototanual)

	dlg.operating.setText("Operating Cost : "+str(round(Custoopotimizado,2)))
	dlg.operating.setFont(QFont('Arial', 10))
	dlg.operating.setStyleSheet("font-weight: bold")

	try:
		dlg.dtmin_op.setText("ΔTmin : "+str(round(dtopt, 5))) #preciso prestar atenção nisso quanto ao passo
	except:
		dlg.dtmin_op.setText("ΔTmin : "+str(dtopt)) #preciso prestar atenção nisso quanto ao passo

	dlg.dtmin_op.setFont(QFont('Arial', 10))
	dlg.dtmin_op.setStyleSheet("font-weight: bold")
	dlg.capital.setText("Capital Cost : " + str(round(cccapitalopt,2)))
	dlg.capital.setFont(QFont('Arial', 10))
	dlg.capital.setStyleSheet("font-weight: bold")
	dlg.capital_anual.setText("Anualized Capital Cost : " + str(round(cccapitalanualopt,2)))
	dlg.capital_anual.setFont(QFont('Arial', 10))
	dlg.capital_anual.setStyleSheet("font-weight: bold")
	dlg.custo_total.setText("Total Cost: " + str(round(custototanualopt,2)))
	dlg.custo_total.setFont(QFont('Arial', 10))
	dlg.custo_total.setStyleSheet("font-weight: bold")
	dlg.area_label.setText("Area: " + str(round(areaopt,2)))
	dlg.area_label.setFont(QFont('Arial', 10))
	dlg.area_label.setStyleSheet("font-weight: bold")

	row = 0
	p = 0
	valorbonito = np.round(variadt, 5)
	dlg.TABELA.setRowCount(len(valorbonito))

	for data in range(len(valorbonito)):
		try:
			dlg.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(np.round(changedv[data], 5))))
		except:
			dlg.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(changedv[data])))
		dlg.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(np.round(yplot[data], 2))))
		dlg.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(np.round(custoopano[data], 2))))
		dlg.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(np.round(custocapitalanual[data], 2))))
		dlg.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(np.round(custototanual[data], 2))))
		for j in range(5):
			item = dlg.TABELA.item(row, j)
			item.setTextAlignment(Qt.AlignCenter)
		row += 1


	y=[0]
	x=[0]
	tamanho = dlg.GRAFICO.frameGeometry().height()
	if tamanho < 550:
		tamanho = 550


	fig = grafico_custo(x, y, variadt, custoopano, custocapitalanual, custototanual)
	arrumar_tamanho(fig, "canva1", tamanho, dlg.GRAFICO, dlg.scroll_custo)

	fig = grafico_area(x, y, variadt, yplot)
	arrumar_tamanho(fig, "canva2", tamanho, dlg.GRAFICO, dlg.scroll_custo)

	fig = grafico_utilidade(x, y, variadt, uq, uf)
	arrumar_tamanho(fig, "canva3", tamanho, dlg.GRAFICO, dlg.scroll_custo)

	dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva1.png"))

def OPTA():
	contador = 0
	uf1, uq1,_,_ = fp2.pontopinch(correntes_temporaria, len(correntes_temporaria), float(dtopt))
	for i in range(0, len(util_temporaria)):
		if util_temporaria[i][3] == 'Cold':
			util_temporaria[i][2] = uf1 / (util_temporaria[i][1] - util_temporaria[i][0])
			correntes_temporaria.append(util_temporaria[i])
			contador += 1
		else:
			util_temporaria[i][2] = uq1 / (util_temporaria[i][0] - util_temporaria[i][1])
			correntes_temporaria.append(util_temporaria[i])
			contador += 1

	akt, _, ajustado, cpf, cpq, areak,deltalmnk = CUSTO(correntes_temporaria, len(correntes_temporaria))

	dlg.area = uic.loadUi("Area.ui")
	dlg.area.show()
	dlg.area.label.setText("Optimized ΔTmin:  " + str(round(dtopt,5)))
	dlg.area.label.setFont(QFont('Arial', 14))
	dlg.area.label.setStyleSheet("font-weight: bold")
	row = 0
	dlg.area.TABELA.setRowCount(len(areak) + 1)

	for data in range(0, len(areak)):
		dlg.area.TABELA.setItem(row, 0, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data],2))))
		dlg.area.TABELA.setItem(row, 1, QtWidgets.QTableWidgetItem(str(round(ajustado[0][data + 1],2))))
		dlg.area.TABELA.setItem(row, 2, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data],2))))
		dlg.area.TABELA.setItem(row, 3, QtWidgets.QTableWidgetItem(str(round(ajustado[1][data + 1],2))))
		dlg.area.TABELA.setItem(row, 4, QtWidgets.QTableWidgetItem(str(round(cpq[data],2))))
		dlg.area.TABELA.setItem(row, 5, QtWidgets.QTableWidgetItem(str(round(cpf[data],2))))
		dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str(round(deltalmnk[data],2))))
		dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round(areak[data],2))))
		row += 1
	dlg.area.TABELA.setItem(row, 6, QtWidgets.QTableWidgetItem(str('Total Area:')))
	dlg.area.TABELA.setItem(row, 7, QtWidgets.QTableWidgetItem(str(round((akt),2))))

		##################acaba aq
	for i in range(0, contador):
		correntes_temporaria.pop()



#inutilidades porem depende
def suprir_9_correntes():
	global matriz_armazenada, matriz_trocadores_abaixo, subestagio_trocador_abaixo, subestagio_trocador, dTmin

	if arquivo == "25 correntes.xls":
		acima = [[2, 2, 1, 1, 1, 1, 1], [3, 2, 1, 1, 2, 1, 1]]
		for i in range(2, 6):
			try:
				acima.append([acima[len(acima)-2][0]+3, i*2, 1, 1, i+1, 1, 1])
				acima.append([acima[len(acima)-2][0]+3, i*2, 1, 1, i+2, 1, 1])
			except:
				pass

		abaixo = [[1, 1, 1, 1, 1, 1, 1], [2, 2, 1, 1, 2, 1, 1], [3, 11, 1, 1, 3, 1, 1]]
		for i in range(4):
			abaixo.append([abaixo[-2][0]+2, abaixo[-2][1]+1, 1, 1, len(abaixo) + 1, 1, 1])
			abaixo.append([abaixo[-1][0]+1, abaixo[-1][1]+1, 1, 1, len(abaixo) + 1, 1, 1])
			abaixo.append([abaixo[-1][0]+1, 11, 1, 1, len(abaixo) + 1, 1, 1])

	elif arquivo == "50 correntes.xls":
		acima = [[2, 2, 1, 1, 1, 1, 1], [3, 2, 1, 1, 2, 1, 1]]
		for i in range(2, 11):
			try:
				acima.append([acima[len(acima)-2][0]+3, i*2, 1, 1, i+1, 1, 1])
				acima.append([acima[len(acima)-2][0]+3, i*2, 1, 1, i+2, 1, 1])
			except:
				pass
		abaixo = [[1, 1, 1, 1, 1, 1, 1], [2, 2, 1, 1, 2, 1, 1], [3, 11, 1, 1, 3, 1, 1]]
		for i in range(9):
			abaixo.append([abaixo[-2][0]+2, abaixo[-2][1]+1, 1, 1, len(abaixo) + 1, 1, 1])
			abaixo.append([abaixo[-1][0]+1, abaixo[-1][1]+1, 1, 1, len(abaixo) + 1, 1, 1])
			abaixo.append([abaixo[-1][0]+1, 11, 1, 1, len(abaixo) + 1, 1, 1])
	elif arquivo == "40 correntes - 3 dtmin.xls":
		divisao_de_correntes("Q", 1, 15, 3, [0.17, 0.79, 0.04])
		divisoes.append(["Q", 1, 15, 3, [0.17, 0.79, 0.04]])
		divisao_de_correntes("Q", 1, 14, 3, [0.28, 0.32, 0.40])
		divisoes.append(["Q", 1, 14, 3, [0.28, 0.32, 0.40]])
		divisao_de_correntes("F", 1, 13, 2, [0.5, 0.5])
		divisoes.append(["F", 1, 13, 2, [0.5, 0.5]])
		divisao_de_correntes("Q", 1, 17, 3, [0.03461047894321384, 0.47533989450877473, 0.49004962654801143])
		divisoes.append(["Q", 1, 17, 3, [0.03461047894321384, 0.47533989450877473, 0.49004962654801143]])

		acima = [[15, 5, 1, 1, 1, 1, 8418.576800000004],
				 [15, 7, 3, 1, 2, 1, 1721.2799999999993],
				 [15, 6, 2, 1, 3, 1, 38109.99999999783],
				 [4, 9, 1, 1, 4, 1, 2131.5],
				 [14, 14, 1, 1, 5, 1, 5081.916000000003],
				 [14, 4, 3, 1, 6, 1, 7259.880000000004],
				 [14, 4, 2, 1, 7, 1, 717.0799999999954],
				 [14, 8, 2, 1, 8, 1, 5090.824000000007],
				 [1, 16, 1, 1, 9, 1, 104.88000000000001],
				 [16, 16, 1, 1, 10, 1, 613.6],
				 [3, 13, 1, 1, 11, 1, 1318.0400000000002],
				 [7, 13, 1, 2, 12, 1, 1212.3999999999999],
				 [15, 5, 3, 1, 13, 1, 148.5831999999973],
				 [15, 8, 3, 1, 14, 1, 110.97840000000429],
				 [4, 16, 1, 1, 15, 1, 38.84999999999991],
				 [15, 14, 2, 1, 16, 1, 70.88399999999729],
				 [15, 16, 2, 1, 17, 1, 576.1100000000005],
				 [15, 8, 2, 1, 18, 1, 364.6276000021909],
				 [17, 8, 1, 1, 19, 1, 248.55999999774224],
				 [17, 13, 2, 1, 20, 1, 3413.7199999999966],
				 [17, 13, 3, 2, 21, 1, 3519.359999999997]]

		divisao_de_correntes_abaixo("Q", 1, 13, 5, [0.18, 0.10, 0.11, 0.52, 0.09])
		divisoes.append(["Q", 2, 13, 5, [0.18, 0.10, 0.11, 0.52, 0.09]])
		divisao_de_correntes_abaixo("F", 1, 18, 10, [0.04411665198623181, 0.0009617876307905618, 0.31263859862075805, 0.0414726963117882, 0.0013317286795616215, 0.21075390853650794, 0.08600612293802927, 0.08249488893347355, 0.15439135094374853, 0.06583226541911047])
		divisoes.append(["F", 2, 18, 10, [0.04411665198623181, 0.0009617876307905618, 0.31263859862075805, 0.0414726963117882, 0.0013317286795616215, 0.21075390853650794, 0.08600612293802927, 0.08249488893347355, 0.15439135094374853, 0.06583226541911047]])

		abaixo = [	[3, 1, 1, 1, 1, 1, 267.86],
					[13, 13, 1, 1, 2, 1, 373.5599999999965],
					[13, 16, 2, 1, 3, 1, 1259.3599999999994],
					[13, 3, 3, 1, 4, 1, 1795.1999999999998],
					[13, 12, 4, 1, 5, 1, 8302.0],
					[13, 15, 5, 1, 6, 1, 1525.0999999999992],
					[13, 2, 4, 1, 7, 1, 8157.34],
					[5, 10, 1, 1, 8, 1, 4949.0],
					[5, 18, 1, 1, 9, 1, 1493.0500000000002],
					[8, 11, 1, 1, 10, 1, 129.12000000000012],
					[10, 11, 1, 1, 11, 1, 64.17000000000003],
					[3, 11, 1, 1, 12, 1, 445.94000000000005],
					[6, 11, 1, 1, 13, 1, 857.9999999999998],
					[11, 11, 1, 1, 14, 1, 44.529999999999745],
					[4, 9, 1, 1, 15, 1, 597.4499999999999],
					[4, 18, 1, 2, 16, 1, 32.55000000000007],
					[9, 17, 1, 1, 17, 1, 689.71],
					[12, 17, 1, 1, 18, 1, 27.610000000000003],
					[7, 17, 1, 1, 19, 1, 544.93],
					[2, 18, 1, 3, 20, 1, 10580.699999999999],
					[7, 18, 1, 4, 21, 1, 1403.5699999999997],
					[11, 18, 1, 5, 22, 1, 45.07000000000026],
					[13, 18, 1, 6, 23, 1, 7132.593000000003],
					[13, 18, 2, 7, 24, 1, 2910.7250000000004],
					[13, 18, 3, 8, 25, 1, 2791.8935],
					[13, 18, 4, 9, 26, 1, 5225.101999999999],
					[13, 18, 5, 10, 27, 1, 2227.9765000000007]]
	elif arquivo == "9 correntes - 20 dtmin.xls":
		# viola termo util
		# # acima = [[3, 2, 1, 2, 1, 1, 677.9], [2, 2, 1, 1, 2, 1, 220.3], [3, 2, 1, 1, 3, 1, 306.5]]
		# # abaixo = [[1, 2, 1, 1, 1, 1, 411.8], [2, 1, 1, 1, 2, 1, 31.3], [3, 1, 1, 1, 3, 1, 195.2], [1, 1, 1, 1, 4, 1, "max"]]
		#
		# # utilidades
		# acima.append([4, 2, 1, 1, 4, 1, "max"])
		# acima.append([4, 2, 1, 2, 5, 1, "max"])
		# abaixo.append([1, 3, 1, 1, 5, 1, "max"])
		# abaixo.append([2, 3, 1, 2, 6, 1, "max"])
		# abaixo.append([3, 3, 1, 3, 7, 1, "max"])

		#sem viola term util
		acima = [[3, 2, 1, 2, 1, 1, 691.8408000000001], [2, 2, 1, 1, 2, 1, 220.32], [3, 2, 1, 1, 3, 1, 292.5591999999999]]
		abaixo = [[1, 2, 1, 1, 1, 1, 411.8], [2, 1, 1, 1, 2, 1, 31.3], [3, 1, 1, 1, 3, 1, 195.2], [1, 1, 1, 1, 4, 1, 715.8300000000002]]

		#util
		acima.append([4, 2, 1, 1, 4, 1, 1266.14])
		abaixo.append([1, 3, 1, 1, 5, 1, 746.0699999999999])
		abaixo.append([2, 3, 1, 2, 6, 1, 113.54])
		abaixo.append([3, 3, 1, 3, 7, 1, 173.95])


		divisao_de_correntes("F", 1, 2, 2, [0.72, 0.28])
		divisoes.append(["F", 1, 2, 2, [0.72, 0.28]])
		divisao_de_correntes_abaixo("F", 1, 3, 3, [0.72185186976924193314304968313096, 0.10981568380823375743795655749601, 0.16833244642252430941899375937303])
		divisoes.append(["F", 2, 3, 3, [0.72185186976924193314304968313096, 0.10981568380823375743795655749601, 0.16833244642252430941899375937303]])
	elif arquivo == "4 correntes - 10 dtmin.xls":
		acima = [[1, 1, 1, 1, 1, 1, 100], [1, 1, 2, 2, 2, 1, 100], [2, 2, 1, 1, 3, 1, 50.5], [2, 2, 2, 2, 4, 1, 50.5], [1, 1, 1, 1, 5, 1, 35], [1, 1, 2, 2, 6, 1, 35], [2, 2, 1, 1, 7, 1, 2], [2, 2, 2, 2, 8, 1, 2]]
		abaixo = [[1, 2, 1, 1, 1, 1, 15], [1, 2, 2, 2, 2, 1, 15], [1, 2, 1, 1, 3, 1, 5], [1, 2, 2, 2, 4, 1, 5]]

		divisao_de_correntes("Q", 1, 1, 2, [0.5, 0.5])
		divisoes.append(["Q", 1, 1, 2, [0.5, 0.5]])
		divisao_de_correntes("Q", 1, 2, 2, [0.5, 0.5])
		divisoes.append(["Q", 1, 2, 2, [0.5, 0.5]])
		divisao_de_correntes("F", 1, 1, 2, [0.5, 0.5])
		divisoes.append(["F", 1, 1, 2, [0.5, 0.5]])
		divisao_de_correntes("F", 1, 2, 2, [0.5, 0.5])
		divisoes.append(["F", 1, 2, 2, [0.5, 0.5]])

		divisao_de_correntes_abaixo("Q", 1, 1, 2, [0.5, 0.5])
		divisoes.append(["Q", 2, 1, 2, [0.5, 0.5]])
		divisao_de_correntes_abaixo("Q", 1, 2, 2, [0.5, 0.5])
		divisoes.append(["Q", 2, 2, 2, [0.5, 0.5]])
		divisao_de_correntes_abaixo("F", 1, 2, 2, [0.5, 0.5])
		divisoes.append(["F", 2, 2, 2, [0.5, 0.5]])


	for trocador in acima:
		if trocador[6] == "max":
			trocador[6] = min(calor_atual_frio_sub[trocador[1]-1][trocador[3]-1], calor_atual_quente_sub[trocador[0]-1][trocador[2]-1])
		dlg.trocador_acima.addItem("E" + str(subestagio_trocador))
		dlg.trocador_acima.setCurrentIndex(dlg.trocador_acima.count()-1)
		subestagio_trocador += 1

	for trocador in abaixo:
		if trocador[6] == "max":
			trocador[6] = min(calor_atual_quente_sub_abaixo[trocador[0]-1][trocador[2]-1], calor_atual_frio_sub_abaixo[trocador[1]-1][trocador[3]-1])
		dlg.trocador_abaixo.addItem("E" + str(subestagio_trocador_abaixo))
		dlg.trocador_abaixo.setCurrentIndex(dlg.trocador_abaixo.count()-1)
		subestagio_trocador_abaixo += 1

	matriz_trocadores_abaixo = inserir_todos_abaixo(abaixo)
	matriz_armazenada = inserir_todos_acima(acima)

	checaresgotadosacima()
	checaresgotadosabaixo()

	# printar()
	# printar_abaixo()
	# testar_correntes(dlg)
	# testar_correntes_abaixo(dlg)
	# evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, 1, jogar_evolucao=True)

def centralizar_combobox_teste(x):
	x.setEditable(True)
	x.lineEdit().setReadOnly(True)
	x.lineEdit().setAlignment(Qt.AlignCenter)
	x.setStyleSheet("QComboBox { background-color: #e1e1e1 }")
	for i in range(x.count()):
		x.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

app = QApplication([])
dlg = uic.loadUi("MPinch.ui")



#streams
dlg.tableWidget.itemChanged.connect(lambda: editar_corrente(correntes, 0, dlg.tableWidget))
dlg.tableWidget_5.itemChanged.connect(lambda: editar_corrente(correntes_util, 1, dlg.tableWidget_5))
dlg.botao_addstream.clicked.connect(add_corrente) #add stream
dlg.botao_addutility.clicked.connect(add_utilidade)
dlg.remover_corrente.clicked.connect(lambda: remover_corrente(dlg.tableWidget.currentRow(), dlg.tableWidget, "corrente"))
dlg.remover_utilidade.clicked.connect(lambda: remover_corrente(dlg.tableWidget_5.currentRow(), dlg.tableWidget_5, "utilidade"))
dlg.actionOpen.triggered.connect(lambda: os.execl(sys.executable, os.path.abspath(__file__), *sys.argv))
dlg.actionOpen_2.triggered.connect(lambda: openfile_teste(True)) #file > open
dlg.actionSave_File.triggered.connect(savefile)
dlg.donebutton.clicked.connect(lambda: done_teste(False)) #done
dlg.pinchbutton.clicked.connect(pinch_teste) #pinch
dlg.sistema_unidades.currentIndexChanged.connect(lambda: unidades(False))
dlg.temp_unidade.currentIndexChanged.connect(unidades)
dlg.cp_unidade.currentIndexChanged.connect(unidades)
dlg.pelicula_unidade.currentIndexChanged.connect(unidades)
dlg.temp_unidade_util.currentIndexChanged.connect(lambda: unidades(corrente=False))
dlg.pelicula_unidade_util.currentIndexChanged.connect(lambda: unidades(corrente=False))



#diagrams comparison
dlg.GC.clicked.connect(grande_curva_comp)
dlg.botaocurvac.clicked.connect(curva_comp_balanceada)
dlg.botaocurva.clicked.connect(curva_comp)
dlg.CASCA.clicked.connect(cascataaa)
dlg.ESTIMA.clicked.connect(lambda: area_information(dlg.DTMIN1, dlg.graficodt1))
dlg.ESTIMA2.clicked.connect(lambda: area_information(dlg.DTMIN2, dlg.graficodt2))



#Heat Exchanger Network
#above
dlg.radioButton.toggled.connect(lambda: dlg.lineEdit_5.setEnabled(True)) #quando marca o heat load libera a linha pra digitar
dlg.radioButton_4.toggled.connect(lambda: dlg.lineEdit_5.setEnabled(False)) #block o heat load quando max heat ta ativado
dlg.radioButton_4.setChecked(True) #por padrao abre o prog com max heat selecionado
dlg.pushButton_9.clicked.connect(lambda: dividir_corrente("Q", "above"))
dlg.pushButton_13.clicked.connect(lambda: dividir_corrente("F", "above"))
dlg.divq_acima.clicked.connect(lambda: dividir_corrente("Q", "above"))
dlg.divf_acima.clicked.connect(lambda: dividir_corrente("F", "above"))
dlg.checkBox.stateChanged.connect(printar) #show splited streams printa tudo dnv
dlg.checkBox_2.stateChanged.connect(printar) #show splited streams printa tudo dnv
dlg.pushButton_6.clicked.connect(inserir_teste) #add heat exchanger
dlg.pushButton_10.clicked.connect(remover_teste) #remove heat exchanger
dlg.trocador_acima.currentIndexChanged.connect(lambda: botao_remover(dlg.trocador_acima.currentIndex()+1, dlg.pushButton_10, "acima"))
dlg.pushButton_14.clicked.connect(calcular_calor_teste) #choose stream temperature to calculate heat
dlg.pushButton_8.clicked.connect(utilidade_teste_acima) #add cold utility
dlg.addutil_acima.clicked.connect(utilidade_teste_acima)
dlg.pushButton_16.clicked.connect(lambda: wid_acima.desenho.salvar())
dlg.completa_acima.clicked.connect(lambda: evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, 1, jogar_evolucao=True, sub=True))
dlg.zoom_acima.valueChanged.connect(lambda: zoom_barra(dlg.zoom_acima, wid_acima, zoom_atual))
#below
dlg.radioButton_17.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(True)) #quando marca o heat load libera a linha pra digitar
dlg.radioButton_20.toggled.connect(lambda: dlg.lineEdit_25.setEnabled(False)) #block o heat load quando max heat ta ativado
dlg.radioButton_20.setChecked(True) #por padrao abre o prog com max heat selecionado
dlg.pushButton_11.clicked.connect(lambda: dividir_corrente("Q", "below"))
dlg.pushButton_12.clicked.connect(lambda: dividir_corrente("F", "below"))
dlg.divq_abaixo.clicked.connect(lambda: dividir_corrente("Q", "below"))
dlg.divf_abaixo.clicked.connect(lambda: dividir_corrente("F", "below"))
dlg.checkBox_9.stateChanged.connect(printar_abaixo) #show splited streams printa tudo dnv
dlg.checkBox_10.stateChanged.connect(printar_abaixo) #show splited streams printa tudo dnv
dlg.pushButton_18.clicked.connect(inserir_teste_abaixo) #add heat exchanger
dlg.pushButton_15.clicked.connect(remover_teste_abaixo) #remove heat exchanger
dlg.trocador_abaixo.currentIndexChanged.connect(lambda: botao_remover(dlg.trocador_abaixo.currentIndex()+1, dlg.pushButton_15, "abaixo"))
dlg.pushButton_17.clicked.connect(calcular_calor_abaixo) #choose stream temperature to calculate heat
dlg.pushButton_20.clicked.connect(utilidade_teste_abaixo) #add hot utility
dlg.addutil_abaixo.clicked.connect(utilidade_teste_abaixo)
dlg.pushButton_19.clicked.connect(lambda: wid_abaixo.desenho.salvar())
dlg.completa_abaixo.clicked.connect(lambda: evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, 1, jogar_evolucao=True, sub=True))
dlg.zoom_abaixo.valueChanged.connect(lambda: zoom_barra(dlg.zoom_abaixo, wid_abaixo, zoom_atual_abaixo))



#custos
dlg.otimizabotao.clicked.connect(eq)
dlg.CUSTO.clicked.connect(lambda: dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva1.png")))
dlg.AREA.clicked.connect(lambda: dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva2.png")))
dlg.UT.clicked.connect(lambda: dlg.GRAFICO.setPixmap(QtGui.QPixmap("canva3.png")))
dlg.OPTA.clicked.connect(OPTA)



#evolução
dlg.trocador_path.currentIndexChanged.connect(lambda: dlg.calor_path.setPlaceholderText("-"))
dlg.botao_evolucao.clicked.connect(lambda: evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, 1, jogar_evolucao=True))
dlg.identificar_laco.clicked.connect(lambda: evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, int(dlg.nivel.currentText()), jogar_evolucao=False))
dlg.identificar_todos.clicked.connect(lambda: evolucao(matriz_armazenada + utilidades, matriz_trocadores_abaixo + utilidades_abaixo, "todos", todos=True))
dlg.botao_editar.clicked.connect(lambda: editar_calor(matriz_evolucao, dlg.trocador_editar.currentIndex(), float(dlg.calor_editar.text().replace(",", "."))))
dlg.botao_path.clicked.connect(lambda: editar_calor(matriz_evolucao, dlg.trocador_path.currentIndex(), float(dlg.calor_path.text().replace(",", ".")), path=True))
dlg.add_util.clicked.connect(lambda: utilidade(matriz_evolucao, []))





dlg.stream_supply.setPlaceholderText(" Ex: 273.15")
dlg.stream_target.setPlaceholderText(" Ex: 273.15")
dlg.util_inlet.setPlaceholderText(" Ex: 273.15")
dlg.util_outlet.setPlaceholderText(" Ex: 273.15")
dlg.stream_cp.setPlaceholderText(" Ex: 200.20")

dlg.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
dlg.tableWidget_5.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
dlg.TABELA.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
for i in range(5):
	dlg.tableWidget.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
	dlg.tableWidget_5.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
	dlg.TABELA.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)
	if i == 3:
		dlg.TABELA.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)


# openfile_teste(pergunta=False, nome="50 correntes.xls")
# openfile_teste(pergunta=False, nome="40 correntes - 3 dtmin.xls")
# openfile_teste(pergunta=False, nome="25 correntes.xls")
# openfile_teste(pergunta=False, nome="4 correntes - 10 dtmin.xls")
openfile_teste(pergunta=False, nome="9 correntes - 20 dtmin.xls")
done_teste(True)
pinch_teste(False)
suprir_9_correntes()



dlg.showMaximized()
app.exec()
