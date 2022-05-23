import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
"""corrente=[[ 327, 40,0.10,'Hot', 0.50*10**-3],
 [ 220, 160,0.16,'Hot', 0.40*10**-3],
 [ 220, 60,0.06,'Hot', 0.14*10**-3],
 [ 160, 45,0.40,'Hot', 0.30*10**-3],
 [111, 333,0.10,'Cold', 0.35*10**-3],[ 327, 40,0.10,'Hot', 0.50*10**-3],
 [ 210, 110,0.16,'Hot', 0.40*10**-3],
 [ 20, 6,0.06,'Hot', 0.14*10**-3],
 [ 120, 45,0.40,'Hot', 0.30*10**-3],
 [130, 300,0.10,'Cold', 0.35*10**-3],[ 327, 40,0.10,'Hot', 0.50*10**-3],
 [ 2120, 160,0.16,'Hot', 0.40*10**-3],
 [ 2270, 60,0.06,'Hot', 0.14*10**-3],
 [ 16670, 45,0.40,'Hot', 0.30*10**-3],
 [10012, 300,0.10,'Cold', 0.35*10**-3],[ 327, 40,0.10,'Hot', 0.50*10**-3]]
dtmin=10"""

def cascata(corrente,dtmin):
    correntegrid = []
    print(len(corrente))
    for i in range(0,len(corrente)):
        if (corrente[i][3]=='Cold'):
            correntegrid.append(float(corrente[i][0])+dtmin/2)
            correntegrid.append(float(corrente[i][1]) + dtmin / 2)
        else:
            correntegrid.append(float(corrente[i][0])-dtmin/2)
            correntegrid.append(float(corrente[i][1]) - dtmin / 2)
    sortc=np.unique(correntegrid).tolist()
    # PLT.CLOSE("ALL") PRA NÃO COMER TODA A MEMORIA DO SEU PC PELO AMOR DE DEUS NÃO ESQUECE DISSO
    plt.close("all")
    plt.style.use('default')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_ylabel('T(ºC)',fontsize=20)
    ax.set_xticks([])
    ax.set_xlim(-1, len(corrente))
    ax.set_ylim(-1.5,len(sortc)+0.5)

    if(len(corrente)>10):
        k=0.5
    else:
        k=0.5

    for i in range(0, len(corrente)):
        param=[i,i]
        if (corrente[i][3]=='Hot'):
            param2 = [sortc.index(corrente[i][0]-dtmin/2), sortc.index(corrente[i][1]-dtmin/2)]
            ax.plot(param,param2, color='red')
            """ax.plot([i-0.25,i+0.25],[param2[0],param2[0]],color='red')
            ax.plot([i - 0.25, i - 0.25], [param2[0], param2[0]+1], color='red')
            ax.plot([i + 0.25, i + 0.25], [param2[0], param2[0]+1], color='red')
            ax.plot([i - 0.25, i + 0.25], [param2[0]+1, param2[0]+1], color='red')"""
            ax.plot(i, (param2[0]), 'ro', ms=12, markeredgecolor='red')
            ax.annotate(str(i+1), xy=(i, param2[0]+k), color='black',fontsize="large", weight='heavy',
                        horizontalalignment='center',
                        verticalalignment='center')
            """ax.plot([i-0.125,i],[param2[1]+0.5,param2[1]],color='red')
            ax.plot([i + 0.125, i], [param2[1] + 0.5, param2[1]], color='red')"""
            ax.plot([i], param2[1], marker=7, ms=10, color='red')
        else:
            param2 = [sortc.index(corrente[i][0] + dtmin / 2), sortc.index(corrente[i][1] + dtmin / 2)]
            ax.plot(param,param2, color='blue')
            """ax.plot([i-0.25,i+0.25],[param2[0],param2[0]],color='blue')
            ax.plot([i - 0.25, i - 0.25], [param2[0], param2[0]-1], color='blue')
            ax.plot([i + 0.25, i + 0.25], [param2[0], param2[0]-1], color='blue')
            ax.plot([i - 0.25, i + 0.25], [param2[0]-1, param2[0]-1], color='blue')"""
            ax.plot(i, (param2[0]), 'bo', ms=10, markeredgecolor='blue')
            ax.annotate(str(i+1), xy=(i, param2[0]-k), color='black',fontsize="large", weight='heavy',
                        horizontalalignment='center',
                        verticalalignment='center')
            """ax.plot([i-0.125,i],[param2[1]-0.5,param2[1]],color='blue')
            ax.plot([i + 0.125, i], [param2[1] - 0.5, param2[1]], color='blue')"""
            ax.plot([i], param2[1], marker=6,ms=10,color='blue')
    sortc = [round(num, 5) for num in sortc]
    ax.set_yticks(np.arange(0, len(sortc), step=1))
    ax.set_yticklabels(sortc,fontsize=20)
    ax.grid(axis="y", color="black", alpha=.5, linewidth=.5, linestyle="-")
    op=len(corrente)
    if(op<15):
        op=25
    opy=len(sortc)
    if opy>10:
        opy=15*opy
    else:
        opy=len(correntegrid)

    fig.set_size_inches(0.4*op, 5.3+0.015*opy)
    fig.savefig("EC.png", bbox_inches='tight')

def cascata2(corrente,dtmin):
    correntegrid = []
    print(len(corrente))
    for i in range(0,len(corrente)):
        if (corrente[i][3]=='Cold'):
            correntegrid.append(float(corrente[i][0])+dtmin/2)
            correntegrid.append(float(corrente[i][1]) + dtmin / 2)
        else:
            correntegrid.append(float(corrente[i][0])-dtmin/2)
            correntegrid.append(float(corrente[i][1]) - dtmin / 2)
    sortc=np.unique(correntegrid).tolist()
    # PLT.CLOSE("ALL") PRA NÃO COMER TODA A MEMORIA DO SEU PC PELO AMOR DE DEUS NÃO ESQUECE DISSO
    plt.close("all")
    plt.style.use('default')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_ylabel('T(ºC)',fontsize=20)
    ax.set_xticks([])
    ax.set_xlim(-1, len(corrente))
    ax.set_ylim(-1.5,len(sortc)+0.5)

    if(len(corrente)>10):
        k=0.5
    else:
        k=0.5

    for i in range(0, len(corrente)):
        param=[i,i]
        if (corrente[i][3]=='Hot'):
            param2 = [sortc.index(corrente[i][0]-dtmin/2), sortc.index(corrente[i][1]-dtmin/2)]

            ax.plot(param,param2, color='red')
            """ax.plot([i-0.25,i+0.25],[param2[0],param2[0]],color='red')
            ax.plot([i - 0.25, i - 0.25], [param2[0], param2[0]+1], color='red')
            ax.plot([i + 0.25, i + 0.25], [param2[0], param2[0]+1], color='red')
            ax.plot([i - 0.25, i + 0.25], [param2[0]+1, param2[0]+1], color='red')"""
            ax.plot(i, (param2[0]), 'ro', ms=12, markeredgecolor='red')
            ax.annotate(str(i+1), xy=(i, param2[0]+k), color='black',fontsize="large", weight='heavy',
                        horizontalalignment='center',
                        verticalalignment='center')
            """ax.plot([i-0.125,i],[param2[1]+0.5,param2[1]],color='red')
            ax.plot([i + 0.125, i], [param2[1] + 0.5, param2[1]], color='red')"""
            ax.plot([i], param2[1], marker=7, ms=10, color='red')
        else:
            param2 = [sortc.index(corrente[i][0] + dtmin / 2), sortc.index(corrente[i][1] + dtmin / 2)]

            ax.plot(param,param2, color='blue')
            """ax.plot([i-0.25,i+0.25],[param2[0],param2[0]],color='blue')
            ax.plot([i - 0.25, i - 0.25], [param2[0], param2[0]-1], color='blue')
            ax.plot([i + 0.25, i + 0.25], [param2[0], param2[0]-1], color='blue')
            ax.plot([i - 0.25, i + 0.25], [param2[0]-1, param2[0]-1], color='blue')"""
            ax.plot(i, (param2[0]), 'bo', ms=10, markeredgecolor='blue')
            ax.annotate(str(i+1), xy=(i, param2[0]-k), color='black',fontsize="large", weight='heavy',
                        horizontalalignment='center',
                        verticalalignment='center')
            """ax.plot([i-0.125,i],[param2[1]-0.5,param2[1]],color='blue')
            ax.plot([i + 0.125, i], [param2[1] - 0.5, param2[1]], color='blue')"""
            ax.plot([i], param2[1], marker=6,ms=10,color='blue')
    sortc = [round(num, 5) for num in sortc]
    ax.set_yticks(np.arange(0, len(sortc), step=1))
    ax.set_yticklabels(sortc,fontsize=20)


    ax.grid(axis="y", color="black", alpha=.5, linewidth=.5, linestyle="-")
    op=len(corrente)
    if(op<15):
        op=25
    opy=len(sortc)
    if opy>10:
        opy=15*opy
    else:
        opy=len(correntegrid)

    fig.set_size_inches(0.4*op, 5.3+0.015*opy)
    fig.savefig("EC2.png", bbox_inches='tight')

"""cascata(corrente, dtmin)"""

"""    arrow = mpatches.FancyArrowPatch((20,245), (20, 20),
                                     mutation_scale=1, color='red')
    ax.add_patch(arrow)"""