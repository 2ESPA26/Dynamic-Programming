escadas = ["SIM-ECR-003", "SIM-ECR-001", "SIM-ECR-002"]
procurado = "SIM-ECR-001"

comparacoes = 0
encontrado = False

for i in range(len(escadas)):
    comparacoes += 1

    if escadas[i] == procurado:
        print("Escada encontrada na posição:", i)
        encontrado = True
        break

if encontrado == False:
    print("Escada não encontrada")

print("Comparações:", comparacoes)