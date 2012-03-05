import random
from datetime import datetime

px, py = 100, 100

L = 20
N = 10

for n in range(N):

    cx, cy = px, py

    for item in range(L):
        datetime.now()
        cx += random.randint(-10, 10) / 100.0
        cy += random.randint(-10, 10) / 100.0

        print('%d\t%d\t%d\t%f\t%f' % ( (n+1), (n*L)+item, random.randint(1, 30), cx, cy ))

