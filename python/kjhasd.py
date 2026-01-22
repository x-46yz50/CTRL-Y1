op = input("insira uma opção ('idade' para informar a sua idade, 'nota' para a sua nota e faltas,'desconto' para verificar desconto):\n > ")

if op == "idade":
    idade = int(input("Informe a sua idade(-1 para sair):\n> "))
    if idade >= 0 and idade <= 12:
        print("você é uma criança.")
    elif idade >= 13 and idade <= 17:
        print("você é uma adolescente.")
    elif idade >= 18 and idade <= 59:
        print("você é uma adulta.")
    elif idade >= 60 and idade != -1:
        print("você é uma idosa.")
    elif idade == -1:
        print("saindo..")
        exit()
    else:
        print("insira uma idade válida.")

if op == "nota":
    notas = float(input("insira sua nota escolar:\n> "))
    faltas = int(input("insira as suas faltas:\n> "))
    if notas >= 7 and notas <= 10 and faltas <= 10:
        print("aprovado.")
    elif notas <= 6 and notas >= 0 and faltas >= 11:
        print("reprovado.")
    else:
        print("entrada inválida. tente novamente.")

if op == "desconto":
    valor = float(input("insira o valor do produto:\n> "))
    if valor >= 100:
        valor *= 0.9
        print("esse produto vai ter um desconto de 10%. o valor final é %0.2f" % valor)
    else:
        print("o produto não tem desconto, então o valor final é %0.2f" % valor)