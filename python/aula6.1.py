dic = {'dog':'cachorro','cat':'gato','water':'água','tree':'árvore','one':'um','two':'dois','three':'três'}

while True:
    x = input("palavra em ingles:\n> ")
    if x in dic:
        print(dic[x])
    else:
        print("invalid option")