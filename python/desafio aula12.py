import random

class xx():
    x = random.randint(0,500)
    y = random.randint(501,1000)

    def z(self):
        return self.x, self.y
    
x = xx()
print(x.z())