import sys
import time

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import xlrd
import matplotlib.pyplot as P
import pylab as P

#remover depois
n=4
correntes=[[165.0, 55.0, 3.0, 'quente'], [145.0, 25.0, 1.5, 'quente'], [85.0, 145.0, 4.0, 'fria'], [25.0, 140.0, 2.0, 'fria']]
dT=[110.0, 120.0, -60.0, -115.0]
dTmin = 10
Tdecre=[165.0, 145.0, 145.0, 140.0, 85.0, 55.0, 25.0, 25.0]
Tmax = Tdecre[0]
Tmin = Tdecre[-1]
cascat2certo=[80.0, 80.0, 82.5, 0.0, 75.0, 60.0, 60.0]

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
figure=P.subplot(121)