from data_base import criar_db
from manipular_db import db_criar, db_read, db_delete


criar_db()

i = 1
j = 1
si = 1
sj = 1
sk = 1
k = 1
q = 300
thki = 70
thkf = 170
tcki = 60
tckf = 135
thski = 70
thskf = 170
tcski = 60
tcskf = 135
fh = 1
fc = 1

#db_criar(i, j, si, sj, sk, k, q, thki, thkf, tcki, tckf, thski, thskf, tcski, tcskf, fh, fc)
db_delete(i, j, si, sj, sk, k)
matriz = db_read()

print(matriz)
