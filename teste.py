import numpy as np

a = np.array([0])
a.resize(3, 3)
# a = a.tolist()
a[2][0] = 2
print(a)

a.resize(5)
print(a)
