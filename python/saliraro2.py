import time
import os

FILE_NAME = "funcionarios.txt"

def registrar_funcionario():
    num = input("Número do funcionário: ").strip()
    hrs = float(input("Horas trabalhadas: ").strip())
    salario = float(input("Salário por hora (U$): ").strip())
    receber = hrs * salario

    # salva no txt
    with open(FILE_NAME, "a") as f:
        f.write(f"{num},{hrs},{salario},{receber}\n")

    print("\nFuncionário registrado com sucesso!\n")
    time.sleep(1)

def importar_funcionarios():
    funcionarios = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            for line in f:
                num, hrs, salario, receber = line.strip().split(",")
                funcionarios.append((num, float(hrs), float(salario), float(receber)))
    return funcionarios

def mostrar_funcionarios():
    funcionarios = importar_funcionarios()
    if not funcionarios:
        print("\nNenhum funcionário registrado ainda.\n")
        return

    print("\n--- Funcionários Registrados ---\n")
    for num, hrs, salario, receber in funcionarios:
        print(f"Funcionário número: {num} || Horas trabalhadas: {hrs} || Salário a receber: U$ {receber:.2f}")
        print("\n------------------------------\n")
        time.sleep(1)
    print("\nFeito por Isa\n")
    time.sleep(2)

while True:
    print("Escolha uma opção:")
    print("1 - Registrar novo funcionário")
    print("2 - Mostrar todos os funcionários (importar do arquivo)")
    print("3 - Sair")

    escolha = input("> ").strip()

    if escolha == "1":
        registrar_funcionario()
    elif escolha == "2":
        mostrar_funcionarios()
    elif escolha == "3":
        print("\nEncerrando programa...")
        break
    else:
        print("\nOpção inválida, tente novamente!\n")