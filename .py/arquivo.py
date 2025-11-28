x = str(input("sla:\n> "))
xd = "xd.txt"
k = "f1.txt"
k2 = "f2.txt"
with open(xd, "w") as f:
    f.write(x)
with open(xd, "r") as f:
    f.seek(0)
    print(f.read())
with open(xd, "a") as f:
    f.write("\n"+x)
with open(xd, "r") as f:
    f.seek(0)
    print(f.read())


try:
    with open(k,"x") as f1:
        f1.write(x)
    with open(k2,"x") as f2:
        f2.write(x)
except FileExistsError as e:
    print(f"Erro: o arquivo ja existe {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado {e}")