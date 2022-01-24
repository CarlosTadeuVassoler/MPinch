import turtle
from PIL import Image

turtle.delay(0)
turtle.setup(width=1.0, height=1.0)

y_acima, y_abaixo = 200, 200

def quentes(onde, correntes):
    global y_acima, y_abaixo
    distancia_x = 420
    for i in range(len(correntes)):
        correntes[i] = turtle.Turtle()
        correntes[i].color("red")
        correntes[i].pensize(3)
        correntes[i].penup()
        if onde == "above":
            correntes[i].setx(-distancia_x)
            correntes[i].sety(y_acima)
            correntes[i].pendown()
            correntes[i].forward(distancia_x - 4)
            y_acima -= 30
        elif onde == "below":
            correntes[i].setx(4)
            correntes[i].sety(y_abaixo)
            correntes[i].pendown()
            correntes[i].forward(distancia_x - 4)
            y_abaixo -= 30

def frias(onde, correntes):
    global y_acima, y_abaixo
    distancia_x = 420
    for i in range(len(fria)):
        correntes[i] = turtle.Turtle()
        correntes[i].color("blue")
        correntes[i].pensize(3)
        correntes[i].penup()
        if onde == "above":
            correntes[i].setx(-4)
            correntes[i].sety(y_acima)
            correntes[i].pendown()
            correntes[i].left(180)
            correntes[i].forward(distancia_x - 4)
            y_acima -= 30
        elif onde == "below":
            correntes[i].setx(420)
            correntes[i].sety(y_abaixo)
            correntes[i].pendown()
            correntes[i].left(180)
            correntes[i].forward(distancia_x - 4)
            y_abaixo -= 30

def pinch(correntes_acima, correntes_abaixo):
    pinch = turtle.Turtle()
    pinch.shapesize(0.001, 0.001, 0.001)
    pinch.pensize(2)
    pinch.right(90)
    pinch.penup()
    pinch.sety(235)
    if len(correntes_acima) > len(correntes_abaixo):
        tamanho = len(correntes_acima)
    else:
        tamanho = len(correntes_abaixo)
    for i in range(tamanho * 3 + 4):
        pinch.pendown()
        pinch.forward(5)
        pinch.penup()
        pinch.forward(5)

def trocador(onde, corrente_quente, corrente_fria, subestagio):
    trocador = turtle.Turtle()
    trocador.pensize(3)
    trocador.color("black", "white")
    trocador.shapesize(0.001, 0.001, 0.001)
    trocador.penup()
    if onde == "above":
        trocador.setx((subestagio+1)*-40)
    elif onde == "below":
        trocador.setx((subestagio+1)*40)
    trocador.sety(corrente_quente.pos()[1]-10)
    trocador.pendown()
    trocador.begin_fill()
    trocador.circle(10)
    trocador.end_fill()
    trocador.sety(corrente_fria.pos()[1] - 10)
    trocador.begin_fill()
    trocador.circle(10)
    trocador.end_fill()

seta = [0] * 2
fria = [0] * 3
seta_baixo = [0] * 2
fria_baixo = [0] * 3
correntes = len(seta) + len(fria)
correntes_baixo = len(seta_baixo) + len(fria_baixo)
quentes("above", seta)
quentes("below", seta_baixo)
frias("above", fria)
frias("below", fria_baixo)
correntes_acima = seta + fria
correntes_abaixo = seta_baixo + fria_baixo
pinch(correntes_acima, correntes_abaixo)
trocador("above", seta[1], fria[2], 0)
trocador("below", seta_baixo[0], fria_baixo[1], 0)





#turtle.done()
turtle.getscreen()
turtle.getcanvas().postscript(file="duck.eps")

# convert -density 300 duck.eps -resize 1024x1024 image.jpg

turtle.done()
