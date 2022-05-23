
import numpy as np

def CUSTO (correntes, n,pinchf,pinchq) :
    cfria = []
    cquente = []
    tfria = []
    tquente = []


    cp=1
    ncorrentefria=0
    ncorrentequente = 0
    for i in range(0,n):
        if correntes[i][3]=="Cold":
            cfria.append(correntes[i])
            ncorrentefria +=1
        else:
            cquente.append(correntes[i])
            ncorrentequente += 1

    TmaxCold=max(cfria, key=lambda l: l[1])
    TminCold=min(cfria, key=lambda l: l[0])
    TmaxHOT=max(cquente, key=lambda l: l[0])
    TminHOT=min(cquente, key=lambda l: l[1])


    for n in range(0,ncorrentefria):
        tfria.append(cfria[n][0])
        tfria.append(cfria[n][1])
    tfria=sorted(set(tfria))
    somacp = np.zeros(len(tfria),dtype=float)
    hentalpia = np.zeros(len(tfria),dtype=float)
    for n in range(0,len(tfria)-1):
        for i in range(0,len(cfria)):
                if (cfria[i][0] <= tfria[n] and cfria[i][1] <= tfria[n]):
                    c = 0
                elif (cfria[i][0] >= tfria[n+1] and cfria[i][1] >= tfria[n+1]):
                    c = 0
                else:
                    somacp[n]+=cfria[i][2]
    hentalpia[0]=pinchf
    cont=int(len(hentalpia))
    for n in range(cont-1,0,-1):
        if n==len(hentalpia)-1:
            for i in range(0,ncorrentefria):
                hentalpia[n]+=(cfria[i][1]-cfria[i][0])*cfria[i][2]
        else:
            hentalpia[n]=hentalpia[n+1]-(tfria[n+1]-tfria[n])*somacp[n]

################################################################################
    for n in range(0, ncorrentequente):
        tquente.append(cquente[n][0])
        tquente.append(cquente[n][1])
    tquente = sorted(set(tquente))
    somacpquente = np.zeros(len(tquente), dtype=float)
    hentalpiaquente = np.zeros(len(tquente), dtype=float)
    hentalpiaquente[len(tquente)-1]=pinchq
    for n in range(0, len(tquente) - 1):
        for i in range(0, len(cquente)):
            if (cquente[i][0] <= tquente[n] and cquente[i][1] <= tquente[n]):
                    # simplesmente n tem nada aqui oq importa é o else
                    c = 0
            elif (cquente[i][0] >= tquente[n+1] and cquente[i][1] >= tquente[n+1]):
                    c = 0
            else:
                somacpquente[n] += cquente[i][2]





    cont = int(len(hentalpiaquente))
    for n in range(cont - 1, 0, -1):
        print(hentalpiaquente)
        if n == len(hentalpiaquente) - 1:
            for i in range(0, ncorrentequente):
                hentalpiaquente[n] += (cquente[i][0] - cquente[i][1]) * cquente[i][2]
        else:
            hentalpiaquente[n] = hentalpiaquente[n + 1] - (tquente[n + 1] - tquente[n]) * somacpquente[n]
    print("FFFFFFFFFFFFF")
    print(hentalpiaquente)
    ajusteF = np.full((1, len(tfria)), '-999')
    ajusteQ = np.full((1, len(tquente)), '-999')

    ajusteF=np.vstack((ajusteF,tfria,hentalpia))
    ajusteQ = np.vstack((tquente,ajusteQ, hentalpiaquente))
    ajuste= np.hstack((ajusteF,ajusteQ))
    ajuste=np.asarray(ajuste, dtype=np.float64)



    for i in range(0,len(ajuste[2])):
        ajuste[2][i]=round(ajuste[2][i],2)

    for n in range(0, len(ajuste[0])):
        for i in range(0, len(ajuste[0])):
            if(ajuste[2][n]==ajuste[2][i]):
                if(ajuste[0][i]=='-999'):
                    ajuste[0][i]=ajuste[0][n]
                else:
                    ajuste[1][i]=ajuste[1][n]



    b2=[]
    b3=[]
    c=1
    ajuste2=[]

    for n in range(0, len(ajuste[2])):
        for i in range(0, len(ajuste[2])):
            if ajuste[2][n]==ajuste[2][i] and i!=n:
                if ajuste[2][n] not in b3:
                    b3.append(ajuste[2][n])
                    b2.append(n)

    for n in range(0, len(b2)):
        ajuste = np.delete(ajuste, b2[n], 1)
        b2=list(np.asarray(b2) - 1)

    print(ajuste)
    ajuste = sorted(ajuste.T, key=lambda l: l[2])




    for n in range(0,len(ajuste)):
        for i in range(0,2):
            if(ajuste[n][i]==-999 and ajuste[n+1][i]!=ajuste[n][i]):
                ajuste[n][i]=ajuste[n-1][i]+(ajuste[n-1][i]-ajuste[n+1][i])*(ajuste[n][2]-ajuste[n-1][2])/(ajuste[n-1][2]-ajuste[n+1][2])
            if(ajuste[n][i]==-999 and ajuste[n+1][i]==ajuste[n][i]):
                b=n
                c=n
                while(ajuste[n][i]==-999 and ajuste[n+1][i]==ajuste[n][i]):
                    n=c
                    c+=1
                ajuste[b][i]=ajuste[b-1][i]+(ajuste[b-1][i]-ajuste[c][i])*(ajuste[b][2]-ajuste[b-1][2])/(ajuste[b-1][2]-ajuste[c][2])
                n=b

    ajuste=np.transpose(ajuste)

    cphquente=[]
    cphfrio = []
    somador=0
    c=0


    for n in range(0,len(ajuste[0])-1):
        for i in range(0,len(cquente)):
            if (cquente[i][0] <= ajuste[0][n] and cquente[i][1] <= ajuste[0][n]):
                #simplesmente n tem nada aqui oq importa é o else
                c=0
            elif (cquente[i][0] >= ajuste[0][n + 1] and cquente[i][1] >= ajuste[0][n + 1]):
                c = 0
            else:
                somador+=(cquente[i][2]/cquente[i][4])
        cphquente.append((ajuste[0][n+1]-ajuste[0][n])*somador)
        somador=0
    for n in range(0,len(ajuste[1])-1):
        for i in range(0,len(cfria)):
            if (cfria[i][0] <= ajuste[1][n] and cfria[i][1] <= ajuste[1][n]):
                c = 0
            elif(cfria[i][0] >= ajuste[1][n+1] and cfria[i][1] >= ajuste[1][n+1]):
                c = 0
            else:
                somador += (cfria[i][2] / cfria[i][4])
        cphfrio.append((ajuste[1][n+1]-ajuste[1][n])*somador)
        somador=0

    print(ajuste)

corrente=[[20,180,0.2,'Cold', 0.0006 ],
          [250,40,0.15,'Hot', 0.001 ],
          [140,230,0.3,'Cold', 0.0008 ],
          [200,80,0.25,'Hot', 0.0008 ]]

n=4

pinchf=10.8
pinchq=-8.30

CUSTO(corrente,n,pinchf,pinchq)

