x = 1
y = 0
import time

while y <= 99:
    x = x * 2
    y = y + 1
    print("2^",y,":", x)
    time.sleep(0.01)

while y >= 99:
    time.sleep(999)