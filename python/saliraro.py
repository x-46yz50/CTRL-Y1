import time

num = 25
hrs = 100
salario = 5.50
receber = hrs * salario

num2 = 1
hrs2 = 200
salario2 = 20.50
receber2 = hrs2 * salario2

num3 = 6
hrs3 = 145
salario3 = 15.55
receber3 = hrs3 * salario3

print("\nFuncionario número:", num,"|| Horas trabalhadas", hrs,"|| Salário a receber: U$ %0.2f"%receber)
print("\n------------------------------\n")
time.sleep(1)
print("Funcionario número:", num2,"|| Horas trabalhadas", hrs2,"|| Salário a receber: U$ %0.2f"%receber2)
print("\n------------------------------\n")
time.sleep(1)
print("Funcionario número:", num3,"|| Horas trabalhadas", hrs3,"|| Salário a receber: U$ %0.2f"%receber3)
time.sleep(2)
print("\n------------------------------\n")
print("\nFeito por Felipe")
time.sleep(5)