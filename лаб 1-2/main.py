import random

a = 1000*random.random()
l = []
for i in range(1, 10):
    l.append((i, round(a*random.uniform(0.8, 1.1))+9.99, i))

print(l)