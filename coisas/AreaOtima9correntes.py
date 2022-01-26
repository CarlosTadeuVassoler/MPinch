import xlrd
import matplotlib.pyplot as P
import math

startingdTmin = float(1)
finaldTmin = float(40)
step = float(0.1)
plantlife = 5
# Utilidade Quente
Tinh = float(330)
Touth = float(250)
hh = float(0.0005)
#Utilidade Fria
Tinc = float(15)
Toutc = float(30)
hc = float(0.0005)
a = 10000
b = 350
c = 1
ntrocadores = 0
interest = 0
anualcosthot = 60
anualcostcold = 6
custoanualmin = 999999999999999999999
startingdTmin1 = float(startingdTmin)
atual = 0
custocapitalv = []
custooperacionalv = []
custoanualv = []
Aredev = []
while startingdTmin <= finaldTmin:
    # workbook = xlrd.open_workbook(r'pinchexcaderno2.xls')
    # worksheet = workbook.sheet_by_index(0)
    # correntes = []
    # n = 9  # numero de correntes
    # numerodecorrentes = worksheet.cell(0, 4).value
    # for i in range(n):  # [0]=Tent [1]=Tsai [2]=CP [3]=tipo [4]=h
    #     x1 = []
    #     for j in range(5):
    #         x1.append(worksheet.cell(i + 1, j + 1).value)
    #     correntes.append(x1)
    # dTmin = startingdTmin
    # print('DTmin: ', startingdTmin)
    # for i in range(n):  # correção das temperaturas
    #     if correntes[i][3] == 'quente':
    #         correntes[i][0] = (correntes[i][0]) - (dTmin) / 2
    #         correntes[i][1] = (correntes[i][1]) - (dTmin) / 2
    #     if correntes[i][3] == "fria":
    #         correntes[i][0] = (correntes[i][0]) + (dTmin) / 2
    #         correntes[i][1] = (correntes[i][1]) + (dTmin) / 2
    n = 9
    dTmin = 10
    correntes = [[ 327, 40,0.10,'quente', 0.5010**-3],
                 [ 220, 160,0.16,'quente', 0.4010-3],
                 [ 220, 60,0.06,'quente', 0.14*10-3],
                 [ 160, 45,0.40,'quente', 0.3010**-3],
                 [100, 300,0.10,'fria', 0.3510-3],
                [ 35, 164,0.07,'fria', 0.70*10-3],
                [85, 138,0.35, 'fria', 0.5010**-3],
                 [ 60, 170,0.06,'fria', 0.1410-3],
                 [140, 300,0.20,'fria', 0.60*10-3]]
    Tmax = 0
    Tmin = 99999
    for i in range(n):
        for j in range(2):
            if Tmax < correntes[i][j]:
                Tmax = correntes[i][j]
            if Tmin > correntes[i][j]:
                Tmin = correntes[i][j]
    dT = []
    for i in range(n):
        dT.append(correntes[i][0]-correntes[i][1])
    Tdecre = []  # recebeu as temperaturas corrigidas
    for i in range(n):
        for j in range(2):
            Tdecre.append(correntes[i][j])
    Tdecre.sort(reverse=True)  # temperaturas decrescentes
    dTdecre = []
    for i in range(2 * n - 1):  # encontrando a variação das temperaturas
        x2 = Tdecre[i] - Tdecre[i + 1]
        dTdecre.append(x2)
    quaiscp = []
    v = []
    for k in range(2 * n - 1):  # escolha dos cps
        v = []
        for i in range(n):
            for j in range(1):
                if correntes[i][3] == "quente":
                    if (correntes[i][j] > Tdecre[k + 1]) and (correntes[i][j + 1] < Tdecre[k]):
                        cptq = correntes[i][2]
                        cptq = -cptq
                        v.append(cptq)
                        break
                if correntes[i][3] == "fria":
                    if (correntes[i][j + 1] > Tdecre[k + 1]) and (correntes[i][j] < Tdecre[k]):
                        cptf = correntes[i][2]
                        v.append(cptf)
                        break
            if i == 3:
                quaiscp.append(v)
    somacps = []
    soma = 0
    tamanhocps = len(quaiscp)
    for i in range(len(quaiscp)):
        soma2 = 0
        for j in range(len(quaiscp[i])):
            soma = quaiscp[i][j]
            soma2 = float(soma + soma2)
        somacps.append(soma2)
    somacpscerto = ['%.2f' % elem for elem in somacps]
    dH = []
    for i in range(2 * n - 1):  # achando a variação da entalpia
        mult = somacps[i] * dTdecre[i]
        dH.append(mult)
    dHcerto = (['%.2f' % elem for elem in dH])
    cascat = [0 - dH[0]]
    for i in range(2 * n - 2):  # primeira cascata de energia
        sub2 = dH[i + 1]
        sub3 = cascat[i] - sub2
        cascat.append(sub3)
    cascatcerto = (['%.2f' % elem for elem in cascat])
    menor = min(float(s) for s in cascat)  # encontrando a maior demanda de energia
    cascat2 = [-menor - dH[0]]
    for i in range(2 * n - 2):  # segunda cascata
        sub2 = dH[i + 1]
        sub3 = cascat2[i] - sub2
        cascat2.append(sub3)
    cascat2certo = ['%.2f' % elem for elem in cascat2]
    menor = menor*(-1)
    menorc = ['%.2f' % menor]
    utilidadesquente = float(menorc[0])
    for i in range(len(cascat2)):  # arredondar para encontrar o 0
        x = round(cascat2[i], 2)
        cascat2[i] = x
    ponto0 = min(float(s) for s in cascat2)
    pinch = 0
    for i in range(len(cascat2)):  # encontrar temperatura no ponto pinch
        if ponto0 == cascat2[i]:
            pinch = Tdecre[i + 1]
    pinchq = pinch + (dTmin / 2)  # arrumando as temperatura das correntes quentes e frias
    pinchf = pinch - (dTmin / 2)
    utilidadesfria = float(cascat2certo[2*n-2])
    for i in range(n):  # correção das temperaturas
        if correntes[i][3] == 'quente':
            correntes[i][0] = float(f'{((correntes[i][0]) + (dTmin) / 2):.2f}')
            correntes[i][1] = float(f'{((correntes[i][1]) + (dTmin) / 2):.2f}')
        if correntes[i][3] == "fria":
            correntes[i][0] = float(f'{((correntes[i][0]) - (dTmin) / 2):.2f}')
            correntes[i][1] = float(f'{((correntes[i][1]) - (dTmin) / 2):.2f}')
    Cputilhot = (utilidadesquente/(Tinh-Touth))
    Cputilcold = (utilidadesfria/(Toutc-Tinc))
    utilhot = [Tinh, Touth, Cputilhot, 'quente', hh]
    utilcold = [Tinc, Toutc, Cputilcold, 'fria', hc]
    correntes.append(utilhot)
    correntes.append(utilcold)
    n += 2
    tempq1 = []
    tempq = []
    tempf1 = []
    tempf = []

    #escolha das temperaturas das correntes com as utilidades
    for i in range(n):
        if correntes[i][3] == 'quente':
            tempq1.append(correntes[i][0])
            tempq1.append(correntes[i][1])
    tempq1.sort()
    for i in tempq1:
        if i not in tempq:
            tempq.append(i)

    for i in range(n):
        if correntes[i][3] == 'fria':
            tempf1.append(correntes[i][0])
            tempf1.append(correntes[i][1])
    tempf1.sort()
    for j in tempf1:
        if j not in tempf:
            tempf.append(j)

    #calculando a variação de temperatura
    dtempq = []
    dtempf = []
    x = 0
    for i in range(len(tempq) - 1):
        x = (tempq[i+1]-tempq[i])
        dtempq.append(x)
    for j in range(len(tempf) - 1):
        x = (tempf[j+1]-tempf[j])
        dtempf.append(x)

    #escolha dos cps das correntes com as utilidades
    v = []
    cpsq = []
    cpsf = []
    for z in range(len(tempq) - 1):
        v = []
        for i in range(n):
            if correntes[i][3] == 'quente':
                if (correntes[i][0] >= tempq[z+1]) and (correntes[i][1] <= tempq[z]):
                    v.append(correntes[i][2])
        cpsq.append(v)

    for z in range(len(tempf) - 1):
        v = []
        for j in range(n):
            if correntes[j][3] == 'fria':
                if (correntes[j][0] <= tempf[z]) and (correntes[j][1] >= tempf[z+1]):
                    v.append(correntes[j][2])
        cpsf.append(v)

    #soma dos cps das correntes com as utilidades
    somacpsq = []
    soma = 0
    soma2 = 0
    for i in range(len(cpsq)):
        soma2 = 0
        for j in range(len(cpsq[i])):
            soma = cpsq[i][j]
            soma2 = (soma + soma2)
        somacpsq.append(soma2)

    somacpsf = []
    for i in range(len(cpsf)):
        soma2 = 0
        for j in range(len(cpsf[i])):
            soma = cpsf[i][j]
            soma2 = (soma + soma2)
        somacpsf.append(soma2)

    #entalpias das correntes com as utilidades
    dhq = [0]
    dhf = [0]

    x1 = 0
    for i in range(len(somacpsq)):
        x = (somacpsq[i])*(tempq[i+1]-tempq[i])
        x1 += x
        dhq.append(x1)

    x1 = 0
    for j in range(len(somacpsf)):
        x = (somacpsf[j])*(tempf[j+1]-tempf[j])
        x1 += x
        dhf.append(x1)

    #coeficientes angulares da curva composta das correntes
    mq = []
    mf = []
    for i in range(len(dhq) - 1):
        if (dhq[i+1] - dhq[i]) == 0:
            mq.append(0)
        else:
            x = (tempq[i+1] - tempq[i])/(dhq[i+1] - dhq[i])
            mq.append(x)

    for j in range(len(dhf) - 1):
        if (dhf[j+1] - dhf[j]) == 0:
            mf.append(0)
        else:
            x = (tempf[j+1] - tempf[j])/(dhf[j+1] - dhf[j])
            mf.append(x)

    #termo independente da equação de reta
    bq = []
    bf = []
    for i in range(len(dhq)-1):
        if mq[i] == 0:
            bq.append(0)
        else:
            x = (-mq[i]*dhq[i]) + tempq[i]
            bq.append(x)

    for j in range(len(dhf)-1):
        if mf[j] == 0:
            bf.append(0)
        else:
            x = (-mf[j]*dhf[j]) + tempf[j]
            bf.append(x)

    #equações de reta
    eqq = []
    eqf = []
    for i in range(len(mq)):
        v = []
        v.append(mq[i])
        v.append(bq[i])
        v.append(dhq[i])
        v.append(dhq[i+1])
        eqq.append(v) #eqq[coeficiente_angular][termo_independente][primeiro_valor_de_entalpia][último_valor_de_entalpia]

    for j in range(len(mf)):
        v = []
        v.append(mf[j])
        v.append(bf[j])
        v.append(dhf[j])
        v.append(dhf[j+1])
        eqf.append(v) #eqf[coeficiente_angular][termo_independente][primeiro_valor_de_entalpia][último_valor_de_entalpia]

    #intervalo de entalpias totais
    dhtotal1 = []
    dhtotal = []
    for i in dhq:
        dhtotal1.append(i)
    for j in dhf:
        dhtotal1.append(j)
    for z in dhtotal1:
        if z not in dhtotal:
            dhtotal.append(z)
    dhtotal.sort()

    #temperaturas de entrada e saida correntes quentes e frias nos intervalos totais
    tesq = []
    tesf = []
    x0 = x1 = 0
    for z in range(len(dhtotal) - 1):
        v = []
        for i in range(len(eqq)):
            if eqq[i][2] <= dhtotal[z] and eqq[i][3] >= dhtotal[z]:
                x0 = (eqq[i][0]*dhtotal[z]) + eqq[i][1]
                x0 = float(f'{x0:.6f}')
                if eqq[i][3] >= dhtotal[z+1]:
                    x1 = (eqq[i][0]*dhtotal[z+1]) + eqq[i][1]
                    x1 = float(f'{x1:.6f}')
        v.append(x0)
        v.append(x1)
        tesq.append(v)

    for z in range(len(dhtotal) - 1):
        v = []
        for j in range(len(eqf)):
            if eqf[j][2] <= dhtotal[z] and eqf[j][3] >= dhtotal[z]:
                x0 = (eqf[j][0]*dhtotal[z]) + eqf[j][1]
                x0 = float(f'{x0:.6f}')
                if eqf[j][3] >= dhtotal[z+1]:
                    x1 = (eqf[j][0]*dhtotal[z+1]) + eqf[j][1]
                    x1 = float(f'{x1:.6f}')
        v.append(x0)
        v.append(x1)
        tesf.append(v)

    #temperaturas 1 e 2 para fazer o DeltaTlm
    tlm1 = []
    tlm2 = []
    for i in range(len(dhtotal) - 1):
        x = (tesq[i][1] - tesf[i][1])
        tlm1.append(x)
        x = (tesq[i][0] - tesf[i][0])
        tlm2.append(x)

    #cálculo DeltaTlm
    dtlm = []
    for i in range(len(dhtotal) - 1):
        if tlm1[i] == tlm2[i]:
            x = tlm1[i]
        else:
            x0 = tlm2[i] - tlm1[i]
            x1 = math.log((tlm2[i]/tlm1[i]))
            x = (x0/x1)
        dtlm.append(x)

    #cálculo do q/h
    temptotalq = []
    temptotalf = []
    somatorioQHq1 = []
    somatorioQHf1 = []
    somatorioQHq = []
    somatorioQHf = []
    v = []

    for i in tesq:
        for z in i:
            if z not in temptotalq:
                temptotalq.append(z)

    for j in tesf:
        for z in j:
            if z not in temptotalf:
                temptotalf.append(z)

    for z in range(len(tesq)):
        v = 0
        for i in range(n):
            if correntes[i][3] == 'quente' and (correntes[i][0] >= tesq[z][1]) and (correntes[i][1] <= tesq[z][0]):
                x = ((tesq[z][1] - tesq[z][0])*correntes[i][2])/(correntes[i][4])
                v += x
        somatorioQHq.append(v)

    for z in range(len(tesf)):
        v = 0
        for j in range(n):
            if correntes[j][3] == 'fria' and (correntes[j][0] <= tesf[z][0]) and (correntes[j][1] >= tesf[z][1]):
                x = ((tesf[z][1] - tesf[z][0])*correntes[j][2])/(correntes[j][4])
                v += x
        somatorioQHf.append(v)

    #somatorio total de q/h dos intervalos
    somatoriototalQH = []

    for z in range(len(dtlm)):
        x = somatorioQHq[z] + somatorioQHf[z]
        somatoriototalQH.append(x)
    for i in range(len(somatoriototalQH)):
        somatoriototalQH[i] = float('{:.5f}'.format(somatoriototalQH[i]))

    #cálculo da área da rede
    Aredev = []
    Arearede = 0
    v = 0
    for z in range(len(dtlm)):
        x = somatoriototalQH[z]/dtlm[z]
        v += x
    Aredev.append(v)
    for i in Aredev:
        Arearede += i
    startingdTmin += step
    startingdTmin = float(f'{startingdTmin:.2f}')

    #Custo
    ntrocadores = n - 1
    Arede = Aredev[0]
    custocapital = 0
    custoanual = 0
    if(interest != 0):
        custocapital1 = ntrocadores*(a + b*(Arede/ntrocadores)**c)
        custocapital = ((interest*((1 + interest)**plantlife))/(((1 + interest)**plantlife) - 1))*custocapital1
        custocapitalv.append(custocapital)
        custooperacional = (anualcosthot*utilidadesquente) + (anualcostcold*utilidadesfria)
        custooperacionalv.append(custooperacional)
        custoanual = custocapital + custooperacional
        custoanualv.append(custoanual)
    else:
        custocapital1 = ntrocadores*(a + b*((Arede/ntrocadores)**c))
        custocapital = (custocapital1)/plantlife
        custocapitalv.append(custocapital)
        custooperacional = (anualcosthot*utilidadesquente) + (anualcostcold*utilidadesfria)
        custooperacionalv.append(custooperacional)
        custoanual = custocapital + custooperacional
        custoanualv.append(custoanual)

    print('Área da Rede: ', Arede)
    print('Custo Capital: ', custocapital)
    print('Custo Operacional: ', custooperacional)
    print('Custo Anual: ', custoanual)
    print()

    #grafico 1
    if dTmin > startingdTmin1:
        P.plot([(dTmin - step), dTmin], [(custocapitalv[atual - 1]), (custocapitalv[atual])], color='r')
        P.plot([(dTmin - step), dTmin], [(custooperacionalv[atual - 1]), (custooperacionalv[atual])], color='b')
        P.plot([(dTmin - step), dTmin], [(custoanualv[atual - 1]), (custoanualv[atual])], color='k')
    atual = atual + 1
    if(custoanual < custoanualmin):
        custoanualmin = custoanual
        Areaotima = Arede
        custooperacionalotimo = custooperacional
        custocapitalotimo = custocapital1
        dTminotimo = dTmin
        custocapitalotimo = float("{:.2f}".format(custocapitalotimo))
        custooperacionalotimo = float("{:.2f}".format(custooperacionalotimo))
        custoanualmin = float("{:.2f}".format(custoanualmin))

print('-'*40)
print('CONDIÇÕES ÓTIMAS')
print('DTmin: ', dTminotimo)
print('Área: ', Areaotima)
print('Custo de Capital: ', custocapitalotimo)
print('Custo Operacional: ', custooperacionalotimo)
print('Custo Anual: ', custoanualmin)
print('-'*40)

P.gca().legend((("Custo Capital: {} $".format(custocapitalotimo)), ("Custo Operacional: {} $/ano".format(custooperacionalotimo)), ("Custo Anual: {} $/ano".format(custoanualmin))))
P.show()

print("utilidade quente", Cputilhot)
print("utilidade fria", Cputilcold)
