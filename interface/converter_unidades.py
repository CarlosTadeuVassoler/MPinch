def KpC (temp) :
	temp=temp-273.15
	round(temp, 2)
	temp=float(str(round(temp, 3)))
	return temp

def CpK (temp) :
	temp=temp+273.15
	temp=float(str(round(temp, 3)))
	return temp

def CpF (temp) :
	temp=temp*1.8+32
	temp=float(str(round(temp, 3)))
	return temp

def FpC (temp) :
	temp=(temp-32)/1.8
	temp=float(str(round(temp, 3)))
	return temp

def FpR (temp) :
	temp=temp+459.67
	temp=float(str(round(temp, 3)))
	return temp

def RpF (temp) :
	temp=temp-459.67
	temp=float(str(round(temp, 3)))
	return temp

def kWpbtu (cp) :
	cp= 0.2388459*cp
	cp=float(str(round(cp, 3)))
	return cp

def btupkW (cp) :
	cp= cp/0.2388459
	cp=float(str(round(cp, 3)))
	return cp

def SI (dlg) :
	dlg.comboBox.setCurrentIndex(0)
	dlg.comboBox_3.setCurrentIndex(0)
	dlg.lineEdit.setPlaceholderText("K")
	dlg.lineEdit2.setPlaceholderText("K")
	dlg.lineEdit3.setPlaceholderText("kW/K")
	dlg.lineEdit3_2.setPlaceholderText("kW/(m²K)")
	if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != '') :
		dlg.lineEdit.setText(str(CpK(FpC(float(dlg.lineEdit.text())))))
		dlg.lineEdit2.setText(str(CpK(FpC(float(dlg.lineEdit2.text())))))
	if (dlg.lineEdit3.text() != ''):
		dlg.lineEdit3.setText(str(btupkW(float(dlg.lineEdit3.text()))))


def sistemaingles (dlg) :
	dlg.comboBox.setCurrentIndex(2)
	dlg.comboBox_3.setCurrentIndex(1)
	dlg.lineEdit.setPlaceholderText("ºF")
	dlg.lineEdit2.setPlaceholderText("ºF")
	dlg.lineEdit3.setPlaceholderText("Btu/(hºF)")
	dlg.lineEdit3_2.setPlaceholderText("Btu/(ft²hºF)")
	if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
		dlg.lineEdit.setText(str(CpF(KpC(float(dlg.lineEdit.text())))))
		dlg.lineEdit2.setText(str(CpF(KpC(float(dlg.lineEdit2.text())))))
	if (dlg.lineEdit3.text() != ''):
		dlg.lineEdit3.setText(str(kWpbtu(float(dlg.lineEdit3.text()))))

def celsius (dlg):
	if (dlg.tempcombo1.currentText()) == 'SI':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(CpK(float(dlg.lineEdit.text()))))
			dlg.lineEdit2.setText(str(CpK(float(dlg.lineEdit2.text()))))
		dlg.comboBox.setCurrentIndex(0)
	if (dlg.tempcombo1.currentText()) == 'Imperial units':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(CpF(float(dlg.lineEdit.text()))))
			dlg.lineEdit2.setText(str(CpF(float(dlg.lineEdit2.text()))))
		dlg.comboBox.setCurrentIndex(2)

def kelvin (dlg):
	if (dlg.tempcombo1.currentText()) == 'Imperial units':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(CpF(KpC(float(dlg.lineEdit.text())))))
			dlg.lineEdit2.setText(str(CpF(KpC(float(dlg.lineEdit2.text())))))
		dlg.comboBox.setCurrentIndex(2)

def farenheit (dlg):
	if (dlg.tempcombo1.currentText()) == 'SI':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(CpK(FpC(float(dlg.lineEdit.text())))))
			dlg.lineEdit2.setText(str(CpK(FpC(float(dlg.lineEdit2.text())))))
		dlg.comboBox.setCurrentIndex(0)

def rankine (dlg) :
	if (dlg.tempcombo1.currentText()) == 'SI':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(CpK(FpC(RpF(float(dlg.lineEdit.text()))))))
			dlg.lineEdit2.setText(str(CpK(FpC(RpF(float(dlg.lineEdit2.text()))))))
		dlg.comboBox.setCurrentIndex(0)
	if (dlg.tempcombo1.currentText()) == 'Imperial units':
		if (dlg.lineEdit.text() != '') or (dlg.lineEdit2.text() != ''):
			dlg.lineEdit.setText(str(RpF(float(dlg.lineEdit.text()))))
			dlg.lineEdit2.setText(str(RpF(float(dlg.lineEdit2.text()))))
		dlg.comboBox.setCurrentIndex(2)

def btu (dlg) :
	if (dlg.tempcombo1.currentText()) == 'Imperial units':
		if (dlg.lineEdit3.text() != ''):
			dlg.lineEdit3.setText(str(kWpbtu(float(dlg.lineEdit3.text()))))
		dlg.comboBox_3.setCurrentIndex(0)

def kW (dlg) :
		if (dlg.tempcombo1.currentText()) == 'SI':
			if (dlg.lineEdit3.text() != ''):
				dlg.lineEdit3.setText(str(btupkW(float(dlg.lineEdit3.text()))))
		dlg.comboBox_3.setCurrentIndex(1)
