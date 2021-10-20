import xlrd
import matplotlib.pyplot as P
import pylab as P

workbook = xlrd.open_workbook(r"C:\pinchexcaderno.xlsx")
worksheet = workbook.sheet_by_index(0)
correntes = []
n = 4  # numero de correntes
numerodecorrentes = worksheet.cell(0, 4).value
for i in range(n):  # [0]=Tent [1]=Tsai [2]=CP [3]=tipo
    x1 = []
    for j in range(4):
        x1.append(worksheet.cell(i + 1, j + 1).value)
    correntes.append(x1)
dTmin = 10
for i in range(n):  # correção das temperaturas
    if correntes[i][3] == 'quente':
        correntes[i][0] = (correntes[i][0]) - (dTmin) / 2
        correntes[i][1] = (correntes[i][1]) - (dTmin) / 2
    if correntes[i][3] == "fria":
        correntes[i][0] = (correntes[i][0]) + (dTmin) / 2
        correntes[i][1] = (correntes[i][1]) + (dTmin) / 2
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
print('psdpsodp')
print(dT)
Tdecre = []  # recebeu as temperaturas corrigidas
for i in range(n):
    for j in range(2):
        Tdecre.append(correntes[i][j])
Tdecre.sort(reverse=True)  # temperaturas decrescentes
print("correntes:")
print(correntes)
print("temperaturas corrigidas:")
print(Tdecre)
dTdecre = []
for i in range(2 * n - 1):  # encontrando a variação das temperaturas
    x2 = Tdecre[i] - Tdecre[i + 1]
    dTdecre.append(x2)
print("intervalo de temperaturas:")
print(dTdecre)
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
print("cps das correntes quentes e frias:")
print(quaiscp)  # escolha dos cps com base nos dT 'flechinhas'
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
print("somatorios dos cps:")
print(somacpscerto)  # arredondamento dos cps
dH = []
for i in range(2 * n - 1):  # achando a variação da entalpia
    mult = somacps[i] * dTdecre[i]
    dH.append(mult)
dHcerto = (['%.2f' % elem for elem in dH])
print("intervalo de entalpia:")
print(dHcerto)
cascat = [0 - dH[0]]
for i in range(2 * n - 2):  # primeira cascata de energia
    sub2 = dH[i + 1]
    sub3 = cascat[i] - sub2
    cascat.append(sub3)
cascatcerto = (['%.2f' % elem for elem in cascat])
print("primeira cascata de energia:")
print(cascatcerto)
menor = min(float(s) for s in cascat)  # encontrando a maior demanda de energia
cascat2 = [-menor - dH[0]]
for i in range(2 * n - 2):  # segunda cascata
    sub2 = dH[i + 1]
    sub3 = cascat2[i] - sub2
    cascat2.append(sub3)
cascat2certo = ['%.2f' % elem for elem in cascat2]
for i in range(len(cascat2)):  # arredondar para encontrar o 0
    x = round(cascat2[i], 2)
    cascat2[i] = x
print("segunda cascata de energia:")
print(cascat2)
ponto0 = min(float(s) for s in cascat2)
pinch = 0
for i in range(len(cascat2)):  # encontrar temperatura no ponto pinch
    if ponto0 == cascat2[i]:
        pinch = Tdecre[i + 1]
print("ponto de estrangulamento energético")
print(pinch)
pinchq = pinch + (dTmin / 2)  # arrumando as temperatura das correntes quentes e frias
pinchf = pinch - (dTmin / 2)
print("pinch da temperatura da corrente quente:")
print(pinchq)
print("pinch da temperatura da corrente fria:")
print(pinchf)
P.subplot(121)
for i in range(n):
    if correntes[i][3] == 'quente':
        P.arrow(i * 0.5, correntes[i][0], 0.0, -dT[i], fc="r", ec="r", head_width=0.05, head_length=2)
    if correntes[i][3] == 'fria':
        P.arrow(i * 0.5, correntes[i][0], 0.0, -dT[i], fc="b", ec="b", head_width=0.05, head_length=2)
P.xlim([-0.5, n / 2])
P.ylim([Tmin-dTmin, Tmax+dTmin])
P.matplotlib.pyplot.grid(which='major', axis='y')
P.subplot(122)
Temperatura = Tdecre[2*n-1]
newcorrentesq = []
newcorrentesf = []
dHq = []
dHf = []
while Temperatura < Tdecre[0]:
    Intdetemp = Temperatura + 1
    x = []
    x.append(Temperatura)
    x.append(Intdetemp)
    somacpq = 0
    somacpf = 0
    for i in range(n):
        if correntes[i][3] == 'quente':
            if correntes[i][0] >= Intdetemp and correntes[i][1] <= Temperatura:
                somacpq = somacpq + correntes[i][2]
        if correntes[i][3] == 'fria':
            if correntes[i][1] >= Intdetemp and correntes[i][0] <= Temperatura:
                somacpf = somacpf + correntes[i][2]
    if somacpq != 0:
    	auxq = somacpq * 1
    	dHq.append(auxq)
    	newcorrentesq.append(x)
    if somacpf != 0:
    	auxf = somacpf * 1
    	dHf.append(auxf)
    	newcorrentesf.append(x)
    Temperatura = Temperatura + 1
intervalosq = len(dHq)
intervalosf = len(dHf)
somaq = 0
somaf = 0
for i in range(int(intervalosq)):
    if i == 0:
        if dHq[i] != 0:
            P.plot([0, dHq[i]], [newcorrentesq[i][0] + (dTmin/2), newcorrentesq[i][1] + (dTmin/2)], color = 'r')
            somaq = dHq[i]
    else:
        if dHq[i] != 0:
            somaq = somaq + dHq[i]
            P.plot([(somaq - dHq[i]), somaq], [newcorrentesq[i][0] + (dTmin/2), newcorrentesq[i][1] + (dTmin/2)], color = 'r')
for i in range(int(intervalosf)):
    if i == 0:
        if dHf[i] != 0:
           P.plot([float(cascat2certo[2*n-2]), float(cascat2certo[2*n-2]) + dHf[i]], [newcorrentesf[i][0] - (dTmin/2), newcorrentesf[i][1] - (dTmin/2)], color = 'b')
           somaf = float(cascat2certo[2*n-2]) + dHf[i]
    else:
        if dHf[i] != 0:
           somaf = somaf + dHf[i]
           P.plot([(somaf - dHf[i]), somaf], [newcorrentesf[i][0] - (dTmin/2), newcorrentesf[i][1] - (dTmin/2)], color = 'b')                
P.show()