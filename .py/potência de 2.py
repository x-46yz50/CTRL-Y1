import time

x = 1
y = 0

while y <= 100:
    time.sleep(0.25)
    print("2 ^",y," = ", x)
    x *= 2
    y += 1
    