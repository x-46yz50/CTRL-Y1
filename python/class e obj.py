class x():
    x = 1234
    y = [1,2,3,4]
    
    def z(self):
        return type(x.y), type(x.x)

x = x()
print(x.z())