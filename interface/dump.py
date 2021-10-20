import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createTable()
 
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 
 
        # Show widget
        self.show()
 
    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Cell (1,2)"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Cell (2,1)"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Cell (2,2)"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Cell (4,2)"))
        self.tableWidget.move(0,0)
 
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
 
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


    	correntes=[]
	for i in range (n):#[0]=Tent  [1]=Tsai  [2]=CP  [3]=tipo
		x1=[]
		for j in range (4):
			x1.append(dlg.tableWidget.getItem(i-1, j)
	correntes.append(x1)


	print (dlg.tableWidget.item(1, 3).text())


g1=float(dlg.tableWidget.item(i,0).text())
g2=float(dlg.tableWidget.item(i,1).text())

def apertarconversor () :
	print(dlg.tempcombo1.currentText())
	if (dlg.tempcombo1.currentText()) != (dlg.tempcombo2.currentText()) :
		if (dlg.tempcombo1.currentText()) == 'Kelvin':
			if (dlg.tempcombo2.currentText()) == 'Celsius':
				dlg.lineEdit.setText(str(KpC(float(dlg.lineEdit.text()))))
				dlg.lineEdit2.setText(str(KpC(float(dlg.lineEdit2.text()))))
			if (dlg.tempcombo2.currentText()) == 'Fahrenheit':
				dlg.lineEdit.setText(str(CpF(KpC(float(dlg.lineEdit.text())))))
				dlg.lineEdit2.setText(str(CpF(KpC(float(dlg.lineEdit2.text())))))
			if (dlg.tempcombo2.currentText()) == 'Rankine':
				dlg.lineEdit.setText(str(FpR(CpF(KpC(float(dlg.lineEdit.text()))))))
				dlg.lineEdit2.setText(str(FpR(CpF(KpC(float(dlg.lineEdit2.text()))))))
		if (dlg.tempcombo1.currentText()) == 'Celsius':
			if (dlg.tempcombo2.currentText()) == 'Kelvin':
				dlg.lineEdit.setText(str(CpK(float(dlg.lineEdit.text()))))
				dlg.lineEdit2.setText(str(CpK(float(dlg.lineEdit2.text()))))
			if (dlg.tempcombo2.currentText()) == 'Fahrenheit':
				dlg.lineEdit.setText(str(CpF(float(dlg.lineEdit.text()))))
				dlg.lineEdit2.setText(str(CpF(float(dlg.lineEdit2.text()))))
			if (dlg.tempcombo2.currentText()) == 'Rankine':
				dlg.lineEdit.setText(str(FpR(CpF(float(dlg.lineEdit.text())))))
				dlg.lineEdit2.setText(str(FpR(CpF(float(dlg.lineEdit2.text())))))
		if (dlg.tempcombo1.currentText()) == 'Fahrenheit':
			if (dlg.tempcombo2.currentText()) == 'Celsius':
				dlg.lineEdit.setText(str(FpC(float(dlg.lineEdit.text()))))
				dlg.lineEdit2.setText(str(FpC(float(dlg.lineEdit2.text()))))
			if (dlg.tempcombo2.currentText()) == 'Kelvin':
				dlg.lineEdit.setText(str(CpK(FpC(float(dlg.lineEdit.text())))))
				dlg.lineEdit2.setText(str(CpK(FpC(float(dlg.lineEdit2.text())))))
			if (dlg.tempcombo2.currentText()) == 'Rankine':
				dlg.lineEdit.setText(str(FpR(float(dlg.lineEdit.text()))))
				dlg.lineEdit2.setText(str(FpR(float(dlg.lineEdit2.text()))))
		if (dlg.tempcombo1.currentText()) == 'Rankine':
			if (dlg.tempcombo2.currentText()) == 'Fahrenheit':
				dlg.lineEdit.setText(str(RpF(float(dlg.lineEdit.text()))))
				dlg.lineEdit2.setText(str(RpF(float(dlg.lineEdit2.text()))))
			if (dlg.tempcombo2.currentText()) == 'Celsius':
				dlg.lineEdit.setText(str(FpC(RpF(float(dlg.lineEdit.text())))))
				dlg.lineEdit2.setText(str(FpC(RpF(float(dlg.lineEdit2.text())))))
			if (dlg.tempcombo2.currentText()) == 'Kelvin':
				dlg.lineEdit.setText(str(CpK(FpC(RpF(float(dlg.lineEdit.text()))))))
				dlg.lineEdit2.setText(str(CpK(FpC(RpF(float(dlg.lineEdit2.text()))))))



wb = copy(workbook)
w_sheet = wb.get_sheet(0)
for i in range (len(enactors)):
	w_sheet.write(i, 0, enactors[i])
wb.save('horas.xls')


timeList = ['0:00:00', '0:00:15', '9:30:56']
sum = datetime.timedelta()
for i in timeList:
    (h, m, s) = i.split(':')
    d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    sum += d
print(str(sum))






Ana Paula Brustolin  Beatriz Linhares  Bianca Seabra  Camila Inumaru  Cindy Futimoto  Diniara Munhoz Dias  Eloá Marcela  Erik Seiji  Fábio Yuiti  Franccesco Poiani  Gabriel Mandelli  Gabriel Jardim  Gabrielly Camargo  Giselle Mansolelli  Guilherme Nascimento  Humberto Mitayatake  Isabela Luana  Izabela Tessaro   João Vitor Nogueira  Laura Sabongi  Leonardo Tomoike  Leticia Toledo  Lucas Yamaguti  Marcos Vinicius  Mariana Zanin    Natasha Dias  Patrícia de Souza  Thais Tiemi  Vinicius Ferrari  Rodrigo Rodrigues  Stephani Lima  Vanessa Katayama  Victoria Faila e Vinícius Sanches 