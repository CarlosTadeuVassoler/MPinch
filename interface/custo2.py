import numpy as np
import funchpinchcerto as fp2
import testesoriginal as tt
import matplotlib.pyplot as plt

def varia(inicio,passo,fim,corrente):
    variadt = np.arange(inicio, fim + passo, passo)

    a = 6600
    b = 600
    c = 0.63

    ncorrentes=4
    nut=2 #nutilidades
    yplot=[]
    custocapital=[]
    i=3#taxa de juros/periodo
    periodo=2#n de periodos
    Fatoranual= 1#(i*(i+1)**periodo)/(-1+(i+1)**periodo)
    custocapitalanual=[]
    precoufano=20
    precouqano=120
    custototanual=[]
    custoopano=[]
    uflista=[]
    uqlista=[]
    print(Fatoranual)
    for n in range(0,len(variadt)):

        uf,uq=fp2.pontopinch(corrente,ncorrentes,variadt[n])
        uflista.append(uf)
        uqlista.append(uq)
        print(uq,uf)
        print(corrente)
        print(corrente[4][1])
        corrente[4][2]=uq/(corrente[4][0]-corrente[4][1])
        corrente[5][2] = uf / (corrente[5][1] - corrente[5][0])

        #dar um jeito de tirar os append, criar uma matriz de n elementos de correntes+n de ut
        areat,nareas = tt.CUSTO(corrente, ncorrentes + nut)
        yplot.append(areat)

        custoopano.append((precoufano*uf*1000)+(precouqano*uq*1000))
        custocapital.append(nareas*(a+b*(areat/nareas)**c))
        custocapitalanual.append(Fatoranual*nareas*(a+b*(areat/nareas)**c))
        custototanual.append(custoopano[n]+custocapitalanual[n])

    return uflista,uqlista,variadt,yplot,custoopano,custocapital,custocapitalanual,custototanual

"""
figura=plt.figure(figsize=(20,20))
figura.suptitle('Graficos ΔTmin')

figura.add_subplot(121)
plt.plot(variadt,custoopano, label='C.Operacional x ΔTmin', color='r')
plt.plot(variadt,custocapitalanual, label='C.Capital x ΔTmin')
plt.plot(variadt,custototanual, label='C.Total x ΔTmin')
plt.xlabel('ΔTmin')
plt.ylabel('Custo')

figura.add_subplot(122)
plt.plot(variadt,yplot, label='Area x ΔTmin')

plt.xlabel('ΔTmin')
plt.ylabel('Area')


plt.show()

"""
