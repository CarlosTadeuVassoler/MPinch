import numpy as np
from itertools import product

n = 5
ti = tj = 0
count = 0
nstages = nsk = 3
nhot_A = 2
ncold_A = 1
nhot_B = 3
ncold_B = 2
resf = 0
aquec = 0
troc = 0
stop = 0
stopcount = 0
vertical_1 = horizontal_1 = vertical_neg1 = horizontal_neg1 = 0
vertical_1_aux = horizontal_1_aux = vertical_neg1_aux = horizontal_neg1_aux = 0
position_aux = []
position_exc = []
position_resf = []
position_aquec = []
positions_loop = []
positions_loop_aux = []
repeat = []
starting_position = []
real_loop = []
real_loop_aux = []
show_loops = []
show_loops_aux = []
test_loops = []
test_loops_aux = []
line_1 = []
line_neg1 = []
different = []
pair = []
true = []
all_loops = []


hot_streams = [1, 2, 3]
cold_streams = [4, 5]
above_hot_streams = [2, 3]
above_cold_streams = [5]
bellow_hot_streams = [1, 2, 3]
bellow_cold_streams = [4, 5]

Qutilhotarr = np.array([0])
Qutilhotarr.resize(3)
Qutilhot = Qutilhotarr.tolist()

Qutilcoldarr = np.array([0])
Qutilcoldarr.resize(1)
Qutilcold = Qutilcoldarr.tolist()

Qutilhot[0] = 746.1
Qutilhot[1] = 113.5
Qutilhot[2] = 176.1

Qutilcold[0] = 1260.1

Q_A = [[[[[[0, 0, 0], [0, 0, 0], [0, 0, 220.32]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]]], [[[[[0, 0, 306.43999999999994], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 677.96], [0, 0, 0]]]]]]
Q_B = [[[[[[0, 715.8300000000002, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]], [[[411.81, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]], [[[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]], [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]]], [[[[[0, 0, 0], [31.3, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]], [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]], [[[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]], [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]]], [[[[[0, 0, 0], [0, 0, 0], [195.2, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]], [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]], [[[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]], [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]]]]
Thki_A = [[266.843137254902, 266.843137254902, 159], [342.9252336448598, 342.9252336448598, 159]]
Tcki_A = [[200.3972463029067, 200.3972463029067, 139]]
Thkf_A = [[266.843137254902, 266.843137254902, 266.843137254902], [342.9252336448598, 342.9252336448598, 342.9252336448598]]
Tckf_A = [[200.3972463029067, 200.3972463029067, 200.3972463029067]]
Tcski_A = [[[[200.3972463029067, 200.3972463029067, 161.47016828148904], [200.3972463029067, 200.3972463029067, 161.47016828148904], [200.3972463029067, 200.3972463029067, 139]], [[184.79296277409486, 184.79296277409486, 208.14431412544621], [184.79296277409486, 184.79296277409486, 139], [184.79296277409486, 184.79296277409486, 139]]]]
Thski_A = [[[[266.843137254902, 266.843137254902, 267.0], [266.843137254902, 266.843137254902, 267.0], [266.843137254902, 266.843137254902, 159]]], [[[342.9252336448598, 342.9252336448598, 285.72149532710284], [342.9252336448598, 342.9252336448598, 159], [342.9252336448598, 342.9252336448598, 159]]]]
Tcskf_A = [[[[200.3972463029067, 200.3972463029067, 192.72361040285568], [200.3972463029067, 200.3972463029067, 161.47016828148904], [200.3972463029067, 200.3972463029067, 161.47016828148904]], [[184.79296277409486, 184.79296277409486, 208.14431412544621], [184.79296277409486, 184.79296277409486, 208.14431412544621], [184.79296277409486, 184.79296277409486, 139]]]]
Thskf_A = [[[[266.843137254902, 266.843137254902, 267.0], [266.843137254902, 266.843137254902, 267.0], [266.843137254902, 266.843137254902, 267.0]]], [[[342.9252336448598, 342.9252336448598, 343.00000000000006], [342.9252336448598, 342.9252336448598, 285.72149532710284], [342.9252336448598, 342.9252336448598, 159]]]]
Thki_B = [[159.0, 141.01312910284463, 109.72210065645514], [159, 143.80392156862746, 143.80392156862746], [159, 122.55140186915887, 122.55140186915887]]
Tcki_B = [[127.0, 102.7770632368703, 26.14255091103965], [139, 118.0413054563998, 118.0413054563998]]
Thkf_B = [[141.01312910284463, 109.72210065645514, 109.72210065645514], [143.80392156862746, 143.80392156862746, 143.80392156862746], [122.55140186915887, 122.55140186915887, 122.55140186915887]]
Tckf_B = [[102.7770632368703, 26.14255091103965, 26.14255091103965], [118.0413054563998, 118.0413054563998, 118.0413054563998]]
Tcski_B = [[[[127.0, 102.7770632368703, 26.14255091103965], [127.0, 26.053590568060002, 26.14255091103965], [123.64523043944266, 26.053590568060002, 26.14255091103965]], [[127.0, 127.0, 127.0], [127.0, 127.0, 127.0], [127.0, 127.0, 127.0]], [[127.0, 127.0, 127.0], [127.0, 127.0, 127.0], [127.0, 127.0, 127.0]]], [[[139, 118.0413054563998, 118.0413054563998], [118.0, 118.0413054563998, 118.0413054563998], [118.0, 118.0413054563998, 118.0413054563998]], [[139, 139, 139], [139, 139, 139], [139, 139, 139]], [[139, 139, 139], [139, 139, 139], [139, 139, 139]]]]
Thski_B = [[[[159.0, 141.01312910284463, 109.72210065645514], [140.97768052516412, 109.68577680525163, 109.72210065645514], [140.97768052516412, 109.68577680525163, 109.72210065645514]], [[159.0, 159.0, 159.0], [159.0, 159.0, 159.0], [159.0, 159.0, 159.0]]], [[[159, 143.80392156862746, 143.80392156862746], [159, 143.80392156862746, 143.80392156862746], [143.65686274509804, 143.80392156862746, 143.80392156862746]], [[159, 159, 159], [159, 159, 159], [159, 159, 159]]], [[[159, 122.55140186915887, 122.55140186915887], [159, 122.55140186915887, 122.55140186915887], [159, 122.55140186915887, 122.55140186915887]], [[159, 159, 159], [159, 159, 159], [159, 159, 159]]]]
Tcskf_B = [[[[127.0, 26.053590568060002, 26.14255091103965], [123.64523043944266, 26.053590568060002, 26.14255091103965], [102.72347266881029, 26.053590568060002, 26.14255091103965]], [[127.0, 127.0, 127.0], [127.0, 127.0, 127.0], [127.0, 127.0, 127.0]], [[127.0, 127.0, 127.0], [127.0, 127.0, 127.0], [127.0, 127.0, 127.0]]], [[[118.0, 118.0413054563998, 118.0413054563998], [118.0, 118.0413054563998, 118.0413054563998], [118.0, 118.0413054563998, 118.0413054563998]], [[139, 139, 139], [139, 139, 139], [139, 139, 139]], [[139, 139, 139], [139, 139, 139], [139, 139, 139]]]]
Thskf_B = [[[[140.97768052516412, 109.68577680525163, 109.72210065645514], [140.97768052516412, 109.68577680525163, 109.72210065645514], [140.97768052516412, 109.68577680525163, 109.72210065645514]], [[159.0, 159.0, 159.0], [159.0, 159.0, 159.0], [159.0, 159.0, 159.0]]], [[[159, 143.80392156862746, 143.80392156862746], [143.65686274509804, 143.80392156862746, 143.80392156862746], [143.65686274509804, 143.80392156862746, 143.80392156862746]], [[159, 159, 159], [159, 159, 159], [159, 159, 159]]], [[[159, 122.55140186915887, 122.55140186915887], [159, 122.55140186915887, 122.55140186915887], [122.51401869158879, 122.55140186915887, 122.55140186915887]], [[159, 159, 159], [159, 159, 159], [159, 159, 159]]]]

#DETERMINANDO OS TROCADORES EXISTENTES ACIMA DO PINCH E EM QUAL POSIÇÃO ELES ESTÃO
for k in range(nstages-1, -1, -1):
    for sk in range(nsk-1, -1, -1):
        for i in range(nhot_A-1, -1, -1):
            for si in range(ncold_A-1, -1, -1):
                for j in range(ncold_A-1, -1, -1):
                    for sj in range(nhot_A-1, -1, -1):
                        if Q_A[i][si][j][sj][sk][k] != 0:
                            position_aux = []
                            troc += 1
                            for t in range(len(above_hot_streams)):
                                if i == t:
                                    ti = above_hot_streams[t]
                            position_aux.append(ti)
                            for t in range(len(above_cold_streams)):
                                if j == t:
                                    tj = above_cold_streams[t]
                            position_aux.append(tj)
                            position_exc.append(position_aux)

#DETERMINANDO OS TROCADORES EXISTENTES ABAIXO DO PINCH E EM QUAL POSIÇÃO ELES ESTÃO
for k in range(nstages):
    for sk in range(nsk):
        for i in range(nhot_B):
            for si in range(ncold_B):
                for j in range(ncold_B):
                    for sj in range(nhot_B):
                        if Q_B[i][si][j][sj][sk][k] != 0:
                            position_aux = []
                            troc += 1
                            for t in range(len(bellow_hot_streams)):
                                if i == t:
                                    ti = bellow_hot_streams[t]
                            position_aux.append(ti)
                            for t in range(len(bellow_cold_streams)):
                                if j == t:
                                    tj = bellow_cold_streams[t]
                            position_aux.append(tj)
                            position_exc.append(position_aux)

#DETERMINANDO QUANTOS RESFRIADORES EXISTEM E EM QUAIS POSIÇÕES ELES ESTÃO
for i in range(len(Qutilhot)):
    if Qutilhot[i] != 0:
        resf += 1
        for t in range(len(bellow_hot_streams)):
            if i == t:
                ti = bellow_hot_streams[t]
                position_resf.append(ti)

#DETERMINANDO QUANTOS AQUECEDORES EXISTEM E EM QUAIS POSIÇÕES ELES ESTÃO
for j in range(len(Qutilcold)):
    if Qutilcold[j] != 0:
        aquec += 1
        for t in range(len(above_cold_streams)):
            if j == t:
                tj = above_cold_streams[t]
                position_aquec.append(tj)

#CRIANDO A MATRIZ INCIDÊNCIA
matriz_incidencia = np.array([0])
matriz_incidencia.resize((n+resf+aquec), (resf+aquec+troc))

#ALOCANDO OS TROCADORES NA MATRIZ INCIDÊNCIA
for i in range(len(position_exc)):
    matriz_incidencia[position_exc[i][0]-1][i] = 1
for j in range(len(position_exc)):
    matriz_incidencia[position_exc[j][1]-1][j] = -1

#ALOCANDO OS AQUECEDORES NA MATRIZ INCIDÊNCIA
ti = 1
for i in range(len(position_exc), (len(position_exc) + len(position_resf))):
    matriz_incidencia[position_resf[i-len(position_exc)]-1][i] = 1
    matriz_incidencia[n+ti-1][i] = -1
    ti += 1

#ALOCANDO RESFRIADORES NA MATRIZ INCIDÊNCIA
tj = 1
for j in range(len(position_exc) + len(position_resf), len(position_exc) + len(position_resf) + len(position_aquec)):
    matriz_incidencia[position_aquec[j-(len(position_exc)+len(position_resf))]-1][j] = -1
    matriz_incidencia[n+ti+tj-2][j] = 1

#CALCULANDO O NÚMERO DE LOOPS DA MATRIZ
rank = np.linalg.matrix_rank(matriz_incidencia)
loops = matriz_incidencia.shape[1] - rank
print('O número de laços independentes é: ', loops)

#ENCONTRANDO OS LOOPS
for j in range(matriz_incidencia.shape[1]):
    for i in range(matriz_incidencia.shape[0]):
        if matriz_incidencia[i][j] == 1:
            positions_loop_aux = []
            positions_loop = []
            repeat = []
            real_loop = []
            show_loops = []
            test_loops = []
            all_loops = []
            all_loops_aux = []
            delete_positions = []
            starting_position = []
            stopcount = 0
            stop = 0
            count = 0
            vertical_1 = i
            horizontal_neg1 = j
            starting_position.append(i)
            starting_position.append(j)
            positions_loop_aux.append(i)
            positions_loop_aux.append(j)
            positions_loop.append(positions_loop_aux)
            repeat.append(positions_loop)
            while stop == 0:
                positions_loop = []
                for h in range(len(repeat[count])):
                    for horizontal_1_aux in range(matriz_incidencia.shape[1]):
                        if horizontal_1_aux == repeat[count][h][1]:
                            continue
                        elif matriz_incidencia[repeat[count][h][0]][horizontal_1_aux] == 1:
                            horizontal_1 = horizontal_1_aux
                            positions_loop_aux = []
                            positions_loop_aux.append(repeat[count][h][0])
                            positions_loop_aux.append(horizontal_1)
                            positions_loop.append(positions_loop_aux)
                repeat.append(positions_loop)
                count += 1
                positions_loop = []
                for h in range(len(repeat[count])):
                    for vertical_neg1_aux in range(matriz_incidencia.shape[0]):
                        if matriz_incidencia[vertical_neg1_aux][repeat[count][h][1]] == -1:
                            vertical_neg1 = vertical_neg1_aux
                            positions_loop_aux = []
                            positions_loop_aux.append(vertical_neg1)
                            positions_loop_aux.append(repeat[count][h][1])
                            positions_loop.append(positions_loop_aux)
                repeat.append(positions_loop)
                count += 1
                positions_loop = []
                for h in range(len(repeat[count])):
                    for horizontal_neg1_aux in range(matriz_incidencia.shape[1]):
                        if horizontal_neg1_aux == repeat[count][h][1]:
                            continue
                        elif matriz_incidencia[repeat[count][h][0]][horizontal_neg1_aux] == -1:
                            horizontal_neg1 = horizontal_neg1_aux
                            positions_loop_aux = []
                            positions_loop_aux.append(repeat[count][h][0])
                            positions_loop_aux.append(horizontal_neg1)
                            positions_loop.append(positions_loop_aux)
                repeat.append(positions_loop)
                count += 1
                positions_loop = []
                for h in range(len(repeat[count])):
                    for vertical_1_aux in range(matriz_incidencia.shape[0]):
                        if matriz_incidencia[vertical_1_aux][repeat[count][h][1]] == 1:
                            vertical_1 = vertical_1_aux
                            positions_loop_aux = []
                            positions_loop_aux.append(vertical_1)
                            positions_loop_aux.append(repeat[count][h][1])
                            positions_loop.append(positions_loop_aux)
                repeat.append(positions_loop)
                count += 1
                stopcount += 1
                for h in range(len(repeat)-1):
                    for loop in repeat[h+1]:
                        if loop == starting_position:
                            stop = 1
                if stopcount == 4:
                    stop = 1

            #filtrando valores
            count = 0
            for h in range(len(repeat)-1, 0, -1):
                real_loop_aux = []
                for loop in range(len(repeat[h])):
                    if h == (len(repeat)-1):
                        if starting_position == repeat[h][loop]:
                            real_loop_aux.append(repeat[h][loop][1])
                    else:
                        for g in range(len(real_loop[count-1])):
                            if h % 2 == 1:
                                if real_loop[count-1][g] == repeat[h][loop][1]:
                                    real_loop_aux.append(repeat[h][loop][0])
                            elif h % 2 == 0:
                                if real_loop[count-1][g] == repeat[h][loop][0]:
                                    real_loop_aux.append(repeat[h][loop][1])
                real_loop.append(real_loop_aux)
                count += 1

            for h in range(0, len(real_loop), 2):
                show_loops_aux = []
                for g in real_loop[h]:
                    if g not in show_loops_aux:
                        show_loops_aux.append(g)
                show_loops.append(show_loops_aux)

            test_loops = list(product(*show_loops))

            for h in range(len(test_loops)):
                line_1 = []
                line_neg1 = []
                for g in range(len(test_loops[h])):
                    for z in range(matriz_incidencia.shape[0]):
                        if matriz_incidencia[z][test_loops[h][g]] == 1:
                            line_1.append(z)
                        elif matriz_incidencia[z][test_loops[h][g]] == -1:
                            line_neg1.append(z)
                different = []
                pair = []
                true = []
                cont = 0
                for z in line_1:
                    if z not in different:
                        different.append(z)
                for z in different:
                    b = 0
                    for y in range(len(line_1)):
                        if z == line_1[y]:
                            b += 1
                    pair.append(b)
                for z in pair:
                    if (z % 2) == 0:
                        true.append(0)
                    else:
                        continue
                    if len(true) == len(pair):
                        cont += 1

                different = []
                pair = []
                true = []
                for z in line_neg1:
                    if z not in different:
                        different.append(z)
                for z in different:
                    b = 0
                    for y in range(len(line_1)):
                        if z == line_1[y]:
                            b += 1
                    pair.append(b)
                for z in pair:
                    if (z % 2) == 0:
                        true.append(0)
                    else:
                        continue
                    if len(true) == len(pair):
                        cont += 1
                if cont == 2:
                    all_loops.append(test_loops[h])

            cont = 0
            for z in range(len(all_loops)):
                for g in all_loops[z]:
                    cont = 0
                    for k in all_loops[z]:
                        if g == k:
                            cont += 1
                        if cont > 1:
                            delete_positions.append(all_loops[z])
                            break
                    if cont > 1:
                        break

            for z in range(len(delete_positions)):
                all_loops.remove(delete_positions[z])
#             print('Para o trocador: ', j+1)
#             print(all_loops)
#
# print()
# print('Matriz Incidência')
# print(matriz_incidencia)
