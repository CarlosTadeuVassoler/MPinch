from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QVBoxLayout
import sys
from PyQt5.QtGui import QPainter, QPen

class Desenho(QWidget):
	def __init__(self):
		super().__init__()

	def paintEvent(self, event):
		painter = QPainter(self)
		pen = QPen()
		pen.setWidth(5)
		painter.setPen(pen)
		painter.drawLine(15, 80, 2900, 1900)

class test(QWidget):
	def __init__(self):
		super().__init__()
		...
		...
		self.setUI()

	def setUI(self):
		self.setGeometry(250, 200, 1500, 3000)
		self.setWindowTitle('data structure visualization simulator')

		self.topFiller = Desenho()
		self.topFiller.setMinimumSize(1200, 2000)
		self.scroll = QScrollArea()
		self.scroll.setWidget(self.topFiller)

		self.vbox = QVBoxLayout()
		self.vbox.addWidget(self.scroll)
		self.setLayout(self.vbox)

app = QApplication(sys.argv)
# window = Window()
window = test()
window.showMaximized()
sys.exit(app.exec())
