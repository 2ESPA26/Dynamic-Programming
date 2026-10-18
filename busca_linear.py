from carregar_dados import escadas


def busca_linear(escadas, alvo):
    comparacoes = 0

    for i in range(len(escadas)):
        comparacoes += 1

        if escadas[i] == alvo:
            return i, comparacoes

    return -1, comparacoes


if __name__ == "__main__":
    procurado = "SIM-ECR-021"

    posicao, comparacoes = busca_linear(escadas, procurado)

    if posicao == -1:
        print("Escada não encontrada")
    else:
        print("Escada encontrada na posição:", posicao)

    print("Comparações:", comparacoes)