from carregar_dados import escadas


def busca_binaria(escadas, alvo):
    inicio = 0
    fim = len(escadas) - 1
    comparacoes = 0

    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1

        if escadas[meio] == alvo:
            return meio, comparacoes

        elif alvo < escadas[meio]:
            fim = meio - 1

        else:
            inicio = meio + 1

    return -1, comparacoes


if __name__ == "__main__":
    escadas_ordenadas = sorted(escadas)
    procurado = "SIM-ECR-001"

    posicao, comparacoes = busca_binaria(
        escadas_ordenadas, procurado
    )

    if posicao == -1:
        print("Escada não encontrada")
    else:
        print("Escada encontrada na posição:", posicao)

    print("Comparações:", comparacoes)

