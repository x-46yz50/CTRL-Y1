# variaveis
nome = "Felipe"
sobrenome = "Reategui"
nomesobrenome = "Felipe Reategui de Moraes"
nim = 15

# pula linha
print("\n")

#printa as variaveis
print(nome)
print(sobrenome)

# printa oq ta na p/os 0 e 3 do sobrenome
print(sobrenome[0])
print(sobrenome[3])

# printa tudo q ta antes ou depois de 4 letras do sobrenome
print(sobrenome[:4])
print(sobrenome[4:])

# printa tudo entre 2 e 5 e 3 e 6
print(sobrenome[2:5])
print(sobrenome[3:6])

# printa a quarta letra do sobrenome ao contrario e tudo antes de 3
print(sobrenome[-4])
print(sobrenome[:-3])

# printa quantas letras tem no sobrenome e nome
print(len(nome))
print(len(sobrenome))

# junta o nome com o sobrenome
print(nome+"",sobrenome)

# conersao de tipo de variavel int pra string
print("eu tenho", str(nim), "anos de idade")

# uppercase
print(sobrenome.upper())

# lowercase
print(sobrenome.lower())

# divide a frasep pelo espaço em branco
separar = nomesobrenome.split()
print(separar[0])
print(separar[1])
print(separar[2])
print(separar[3])