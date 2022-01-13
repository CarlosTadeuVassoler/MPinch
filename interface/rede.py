import turtle

def desenhar_rede(correntes_quentes, correntes_frias, Thf_acima, Th0_abaixo, Tc0_acima, Tcf_abaixo, corrente_quente_presente_acima, corrente_quente_presente_abaixo, corrente_fria_presente_acima, corrente_fria_presente_abaixo, pinchq, pinchf):
	global y_acima, y_abaixo
	turtle.reset()
	turtle.delay(0)
	turtle.setup(width=1.0, height=1.0)

	y_acima, y_abaixo = 200, 200

	def quentes(onde, correntes, presente):
		global y_acima, y_abaixo
		distancia_x = 420
		for i in range(len(correntes)):
			if presente[i]:
				correntes[i] = turtle.Turtle()
				correntes[i].color("red")
				correntes[i].pensize(3)
				correntes[i].penup()
				if onde == "above":
					correntes[i].setx(-distancia_x)
					correntes[i].sety(y_acima)
					correntes[i].pendown()
					if Thf_acima[i] == pinchq:
						correntes[i].forward(distancia_x - 4)
					else:
						correntes[i].forward(distancia_x - 200)
				elif onde == "below":
					correntes[i].sety(y_abaixo)
					if Th0_abaixo[i] == pinchq:
						correntes[i].setx(4)
						correntes[i].pendown()
						correntes[i].forward(distancia_x - 4)
					else:
						correntes[i].setx(200)
						correntes[i].pendown()
						correntes[i].forward(distancia_x - 200)
			y_acima -= 30
			y_abaixo -= 30

	def frias(onde, correntes, presente):
		global y_acima, y_abaixo
		distancia_x = 420
		for i in range(len(correntes)):
			if presente[i]:
				correntes[i] = turtle.Turtle()
				correntes[i].color("blue")
				correntes[i].pensize(3)
				correntes[i].penup()
				if onde == "above":
					correntes[i].sety(y_acima)
					correntes[i].left(180)
					if Tc0_acima[i] == pinchf:
						correntes[i].setx(-4)
						correntes[i].pendown()
						correntes[i].forward(distancia_x - 4)
					else:
						correntes[i].setx(-200)
						correntes[i].pendown()
						correntes[i].forward(distancia_x - 200)
				elif onde == "below":
					correntes[i].sety(y_abaixo)
					correntes[i].left(180)
					correntes[i].setx(420)
					if Tcf_abaixo[i] == pinchf:
						correntes[i].pendown()
						correntes[i].forward(distancia_x - 4)
					else:
						correntes[i].pendown()
						correntes[i].forward(distancia_x - 200)
			y_acima -= 30
			y_abaixo -= 30

	def pinch(correntes):
		pinch = turtle.Turtle()
		pinch.shapesize(0.001, 0.001, 0.001)
		pinch.pensize(2)
		pinch.right(90)
		pinch.penup()
		pinch.sety(235)
		tamanho = len(correntes)
		for i in range(tamanho * 3 + 4):
			pinch.pendown()
			pinch.forward(5)
			pinch.penup()
			pinch.forward(5)

	quentes("above", correntes_quentes, corrente_quente_presente_acima)
	frias("above", correntes_frias, corrente_fria_presente_acima)
	y_acima, y_abaixo = 200, 200
	quentes("below", correntes_quentes, corrente_quente_presente_abaixo)
	frias("below", correntes_frias, corrente_fria_presente_abaixo)
	pinch(correntes_quentes+correntes_frias)

	#turtle.done()
