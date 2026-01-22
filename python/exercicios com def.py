def saudar(nome):
    print("Oiee "+nome+"! Seja bem vindo(a)!!")
def dobro(n):
    n *= 2
    print(n)
def par(n):
    if n % 2 == 0:
        print("é um numero par!")
    else:
        print("é um numero impar!")
def area(a,b):
    ar = a*b
    print(ar)
def desconto(a,b):
    a *= b
    print(a)

while True:
    op = input("selecione uma opção('saudar' para testar saudação, 'dobro' para calcular o dobro de algo, 'par' pra verificar se um numero é par, 'retangulo' para calcular a area de um retangulo, 'desconto' para calcular desconto de algo e 'sair' para sair):\n> ")
    if op == "saudar":
        x = str(input("qual o seu nome??\n> "))
        saudar(x)
    elif op == "dobro":
        x = int(input("digite um número:\n> "))
        dobro(x)
    elif op == "par":
        x = int(input("digite um número:\n> "))
        par(x)
    elif op == "retangulo":
        x = int(input("digite a altura:\n> "))
        y = int(input("digite a largura:\n> "))
        area(x,y)
    elif op == "desconto":
        x = int(input("digite o valor da compra:\n> "))
        y = int(input("digite o desconto(%):\n> "))
        desconto(x,y)
    elif op == "sair":
        exit()
    else:
        print("opção inválida! tente novamente.")