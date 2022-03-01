a = [[0, 0, 1, 0, 1, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0,
 0, -1, -1, 0, 0, 0, 0], [-1, -1, -1, 0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1, 0, 0, 0], [0, 0, 0, 0, 0, 0, -1, 0, 0], [0, 0
, 0, 0, 0, 0, 0, -1, 0]]


nivel = 2

nhot = 4
ncold = 5

def teste():
	soma_quente = [0, 0, 0, 0]
	soma_fria = [0, 0, 0, 0, 0]
	for t1 in range(len(a[0])):
		for corrente in range(len(a)):
			if a[corrente][t1] == 1:
				soma_quente[corrente] += 1
			if a[corrente - nhot][t1] == -1:
				soma_fria[corrente - nhot] -= 1
		for t2 in range(t1+1, len(a[0])):
			for corrente in range(len(a)):
				if a[corrente][t2] == 1:
					soma_quente[corrente] += 1
				if a[corrente - nhot][t2] == -1:
					soma_fria[corrente - nhot] -= 1
			for t3 in range(t2+1, len(a[0])):
				for corrente in range(len(a)):
					if a[corrente][t3] == 1:
						soma_quente[corrente] += 1
					if a[corrente - nhot][t3] == -1:
						soma_fria[corrente - nhot] -= 1
				for t4 in range(t3+1, len(a[0])):
					for corrente in range(len(a)):
						if a[corrente][t4] == 1:
							soma_quente[corrente] += 1
						if a[corrente - nhot][t4] == -1:
							soma_fria[corrente - nhot] -= 1

					soma = 0
					for i in range(len(soma_quente)):
						if soma_quente[i] == 2:
							soma += 2
					for j in range(len(soma_fria)):
						if soma_fria[j] == 2:
							soma += 2

					print("comparando", t1+1, t2+1, t3+1, t4+1)
					print(soma_quente)
					print(soma_fria)
					print()

					if soma == 4*nivel:
						print("laço")
						return
					else:
						for corrente in range(len(a)):
							if a[corrente][t4] == 1:
								soma_quente[corrente] -= 1
							if a[corrente-nhot][t4] == -1:
								soma_fria[corrente-nhot] += 1
						print("num foi")

teste()











#oi
