import random
import time

while True:
    sal = float(input("\ninsira o seu salario:\n>"))
    rea = 0
    if sal >= 0 and  sal <= 400:
        rea = 0.15
        per = rea * 100
        nsal = sal + sal * rea
        rea2 = nsal - sal
        print(" Novo salário:",round(nsal, 2), "\n reajuste ganho:", round(rea2, 2), "\n percentual de ajuste:", per,"%")
    elif sal >= 400.01 and  sal <= 800:
        rea = 0.12
        per = rea * 100
        nsal = sal + sal * rea
        rea2 = nsal - sal
        print(" Novo salário:",round(nsal, 2), "\n reajuste ganho:", round(rea2, 2), "\n percentual de ajuste:", per,"%")
    elif sal >= 800.01 and  sal <= 1200:
        rea = 0.10
        per = rea * 100
        nsal = sal + sal * rea
        rea2 = nsal - sal
        print(" Novo salário:",round(nsal, 2), "\n reajuste ganho:", round(rea2, 2), "\n percentual de ajuste:", per,"%")
    elif sal >= 1200.01 and  sal <= 2000:
        rea = 0.07
        per = rea * 100
        nsal = sal + sal * rea
        rea2 = nsal - sal
        print(" Novo salário:",round(nsal, 2), "\n reajuste ganho:", round(rea2, 2), "\n percentual de ajuste:", per,"%")
    elif sal >= 2000.01 and sal <= 115490000000000.00:
        rea = 0.04
        per = rea * 100
        nsal = sal + sal * rea
        rea2 = nsal - sal
        print(" Novo salário:",round(nsal, 2), "\n reajuste ganho:", round(rea2, 2), "\n percentual de ajuste:", per,"%")
    elif sal >= 115490000000000.01:
       print("mentiroso da porra mlk KKKKKKKKKKK")
    else:
        print("entrada inválida. tente novamente.")