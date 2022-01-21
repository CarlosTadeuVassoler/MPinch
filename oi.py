def quentes(onde, correntes_desenho, presente):
  global y_acima, y_abaixo, tamanho_acima, tamanho_abaixo
  distancia_x = 500
  for i in range(len(correntes_desenho)):
    temp.sety(y_acima - 8)
    temp.setx(-distancia_x - len("Cp = " + str(correntes[i][2]))*3 - 110)
    temp.write("Cp = " + str(correntes[i][2]), align="left", font=("Arial", 10, "normal"))
    if presente[i]:
      correntes_desenho[i] = turtle.Turtle()
      correntes_desenho[i].color("red")
      correntes_desenho[i].pensize(3)
      correntes_desenho[i].penup()
      correntes_desenho_sub_acima = [0] * nhot
      correntes_desenho_sub_abaixo = [0] * nhot
      if onde == "above":
        temp.sety(y_acima - 8)
        correntes_desenho[i].setx(-distancia_x)
        correntes_desenho[i].sety(y_acima)
        correntes_desenho[i].pendown()
        if dividida_quente[i]:
          correntes_desenho_sub_acima[i] = [0] * (quantidade_quente[i] - 1)
          for j in range(quantidade_quente[i]-1):
            correntes_desenho_sub_acima[i][j] = turtle.Turtle()
            correntes_desenho_sub_acima[i][j].color("red")
            correntes_desenho_sub_acima[i][j].pensize(3)
            correntes_desenho_sub_acima[i][j].penup()
            correntes_desenho_sub_acima[i][j].setx(-distancia_x + 40)
            correntes_desenho_sub_acima[i][j].sety(y_acima)
            correntes_desenho_sub_acima[i][j].pendown()
            correntes_desenho_sub_acima[i][j].right(90)
            correntes_desenho_sub_acima[i][j].forward(30)
            correntes_desenho_sub_acima[i][j].left(90)
            if Thf_acima[i] == pinchq:
              correntes_desenho_sub_acima[i][j].forward(distancia_x - 84)
            else:
              correntes_desenho_sub_acima[i][j].forward(distancia_x - 180)
            correntes_desenho_sub_acima[i][j].left(90)
            correntes_desenho_sub_acima[i][j].forward(30*(j+1))
            correntes_desenho_sub_acima[i][j].right(90)
            correntes_desenho_sub_acima[i][j].forward(40)
            y_acima -= 30
        if Thf_acima[i] == pinchq:
          correntes_desenho[i].forward(distancia_x - 4)
        else:
          correntes_desenho[i].forward(distancia_x - 100)
          temp.setx(-94)
          temp.write(str(Thf_acima[i]), align="left", font=("Arial", 10, "normal"))
        if dividida_quente[i] and dividida_quente_abaixo[i]:
          if quantidade_quente[i] < quantidade_quente_abaixo[i]:
            y_acima -= 30 * (quantidade_quente_abaixo[i] - quantidade_quente[i])
        elif dividida_quente_abaixo[i]:
          y_acima -= 30 * (quantidade_quente_abaixo[i] - 1)
        temp.setx(-distancia_x - len(str(Th0[i]))*3 - 20)
        temp.write(str(Th0[i]), align="left", font=("Arial", 10, "normal"))
      elif onde == "below":
        temp.sety(y_abaixo - 8)
        correntes_desenho[i].sety(y_abaixo)
        if dividida_quente_abaixo[i]:
          correntes_desenho_sub_abaixo[i] = [0] * (quantidade_quente_abaixo[i] - 1)
          for j in range(quantidade_quente_abaixo[i]-1):
            correntes_desenho_sub_abaixo[i][j] = turtle.Turtle()
            correntes_desenho_sub_abaixo[i][j].color("red")
            correntes_desenho_sub_abaixo[i][j].pensize(3)
            correntes_desenho_sub_abaixo[i][j].penup()
            correntes_desenho_sub_abaixo[i][j].sety(y_abaixo)
            if Th0_abaixo[i] == pinchq:
              correntes_desenho_sub_abaixo[i][j].setx(44)
              correntes_desenho_sub_abaixo[i][j].pendown()
              correntes_desenho_sub_abaixo[i][j].right(90)
              correntes_desenho_sub_abaixo[i][j].forward(30)
              correntes_desenho_sub_abaixo[i][j].left(90)
              correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 84)
            else:
              correntes_desenho_sub_abaixo[i][j].setx(140)
              correntes_desenho_sub_abaixo[i][j].pendown()
              correntes_desenho_sub_abaixo[i][j].right(90)
              correntes_desenho_sub_abaixo[i][j].forward(30)
              correntes_desenho_sub_abaixo[i][j].left(90)
              correntes_desenho_sub_abaixo[i][j].forward(distancia_x - 180)
            correntes_desenho_sub_abaixo[i][j].left(90)
            correntes_desenho_sub_abaixo[i][j].forward(30*(j+1))
            correntes_desenho_sub_abaixo[i][j].right(90)
            correntes_desenho_sub_abaixo[i][j].forward(40)
            y_abaixo -= 30
        if Th0_abaixo[i] == pinchq:
          correntes_desenho[i].setx(4)
          correntes_desenho[i].pendown()
          correntes_desenho[i].forward(distancia_x - 4)
        else:
          correntes_desenho[i].setx(100)
          correntes_desenho[i].pendown()
          correntes_desenho[i].forward(distancia_x - 100)
          temp.setx(100 - len(str(Th0[i]))*3 - 20)
          temp.write(str(Th0_abaixo[i]), align="left", font=("Arial", 10, "normal"))
        if dividida_quente[i] and dividida_quente_abaixo[i]:
          if quantidade_quente[i] > quantidade_quente_abaixo[i]:
            y_abaixo -= 30 * (quantidade_quente[i] - quantidade_quente_abaixo[i])
        elif dividida_quente[i]:
          y_abaixo -= 30 * (quantidade_quente[i] - 1)
        temp.setx(distancia_x + 6)
        temp.write(str(Thf[i]), align="left", font=("Arial", 10, "normal"))
    y_acima -= 30
    y_abaixo -= 30
