import time

while True:
    entrada = input("\nDigite base, expoente máximo e delay separados por vírgula (ou 'sair'): ")

    if entrada.lower() == "sair":
        print("Saindo...")
        break

    try:
        partes = entrada.split(",")
        base = int(partes[0].strip())
        limite = int(partes[1].strip())
        delay = float(partes[2].strip())
    except:
        print("Entrada inválida! Exemplo: 2,10,0.25")
        continue

    print(f"\n--- Potências de {base} até expoente {limite} ---")
    x = 1
    for y in range(limite + 1):
        time.sleep(delay)
        print(f"{base} ^ {y} = {x}")
        x *= base