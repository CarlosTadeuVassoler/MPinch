import turtle

turtle.delay(0)


trocador = turtle.Turtle()
trocador.shapesize(0.001, 0.001, 0.001)
trocador.color("black", "white")
trocador.pensize(3)
trocador.penup()
trocador.speed(1000)

corrente = turtle.Turtle()
corrente.pensize(3)
corrente.speed(1000)

texto = turtle.Turtle()
texto.shapesize(0.001, 0.001, 0.001)
texto.penup()
texto.speed(1000)


legenda_comeco_corrente = -150
legenda_trocador = -20
legenda_raio_trocador = 30

corrente.penup()
corrente.setx(legenda_comeco_corrente)
corrente.pendown()
corrente.forward(300)
trocador.setx(legenda_trocador)
trocador.sety(corrente.pos()[1] - legenda_raio_trocador)
trocador.pendown()
trocador.begin_fill()
trocador.circle(legenda_raio_trocador)
trocador.end_fill()
texto.setx(trocador.pos()[0])
texto.sety(corrente.pos()[1] + legenda_raio_trocador + 20)
texto.write("HEAT", align="center", font=("Arial", 10, "bold"))
texto.sety(corrente.pos()[1] + legenda_raio_trocador)
texto.write("EXCHANGED", align="center", font=("Arial", 10, "bold"))
texto.setx(trocador.pos()[0] - legenda_raio_trocador - len("temperature")*2.75)
texto.sety(corrente.pos()[1] - 14)
texto.write("inlet", align="center", font=("Arial", 8, "normal"))
texto.sety(corrente.pos()[1] - 24)
texto.write("temperature", align="center", font=("Arial", 8, "normal"))
texto.setx(trocador.pos()[0] + legenda_raio_trocador + len("temperature")*2.90)
texto.write("temperature", align="center", font=("Arial", 8, "normal"))
texto.sety(corrente.pos()[1] - 14)
texto.write("outlet", align="center", font=("Arial", 8, "normal"))
texto.sety(corrente.pos()[1] + 2)
texto.setx(legenda_comeco_corrente - len("temperature")*4)
texto.write("Supply", align="center", font=("Arial", 10, "normal"))
texto.sety(corrente.pos()[1] - 14)
texto.write("Temperature", align="center", font=("Arial", 10, "normal"))
texto.setx(-legenda_comeco_corrente + len("temperature")*4)
texto.sety(corrente.pos()[1] + 2)
texto.write("Target", align="center", font=("Arial", 10, "normal"))
texto.sety(corrente.pos()[1] - 14)
texto.write("Temperature", align="center", font=("Arial", 10, "normal"))
texto.sety(legenda_trocador - 50)
texto.setx(legenda_trocador)
texto.write("UNITS", align="center", font=("Arial", 10, "bold"))
texto.setx(legenda_trocador - len("Temperatures: K")*3)
texto.sety(legenda_trocador - 70)
texto.write("Heat: kW", align="left", font=("Arial", 10, "normal"))
texto.sety(legenda_trocador - 90)
texto.write("Temperatures: K", align="left", font=("Arial", 10, "normal"))










turtle.done()
