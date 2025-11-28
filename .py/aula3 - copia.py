x = int(input("valor 1: "))
y = int(input("valor 2: "))
z = int(input("operação( 1= +; 2 = -; 3 = *; 4 = /; 5 = **): "))
resultado = int
print("resultado: ")

if z == 1:
    resultado = x + y
    print(resultado)
if z == 2:
    resultado = x - y
    print(resultado)
if z == 3:
    resultado = x * y
    print(resultado)
if z == 4:
    resultado = x / y
    print(resultado)
if z == 5:
    resultado = x ** y
    print(resultado)