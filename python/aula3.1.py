import random
import time

alunos = ["Wilton","Felipe","Eduardo","Pedro","Roberto"]
faltas = int
numero = 0
timer = 0

while numero <= 4:
    timer = random.randint(0.2,1.5)
    time.sleep(timer)
    faltas = random.randint(0,100)
    print(alunos[numero],faltas)
    numero += 1