escadas = ["SIM-ECR-003", "SIM-ECR-001", "SIM-ECR-002"]
procurado = "SIM-ECR-001"


def busca_linear(escadas, alvo):
    comparacoes = 0

    for i in range(len(escadas)):
        comparacoes += 1

        if escadas[i] == alvo:
            return i, comparacoes

    return -1, comparacoes


posicao, comparacoes = busca_linear(escadas, procurado)

if posicao == -1:
    print("Escada não encontrada")
else:
    print("Escada encontrada na posição:", posicao)

print("Comparações:", comparacoes)