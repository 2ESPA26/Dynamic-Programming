import csv

from carregar_dados import escadas
from alertas import leitura_em_alerta


def buscar_primeiro_limite_linear(acumulados, limite):
    comparacoes = 0

    for i in range(len(acumulados)):
        comparacoes += 1

        if acumulados[i] >= limite:
            return i, comparacoes

    return -1, comparacoes


def buscar_primeiro_limite_binaria(acumulados, limite):
    inicio = 0
    fim = len(acumulados) - 1
    posicao = -1
    comparacoes = 0

    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1

        if acumulados[meio] >= limite:
            posicao = meio
            fim = meio - 1
        else:
            inicio = meio + 1

    return posicao, comparacoes


def carregar_leituras():
    leituras = []

    with open("sensores.csv", encoding="utf-8", newline="") as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)

        for leitura in leitor:
            leituras.append(leitura)

    return leituras


if __name__ == "__main__":
    leituras = carregar_leituras()
    resultados = []

    total_linear = 0
    total_binaria = 0
    escadas_com_limite = 0

    for id_escada in escadas:
        horarios = []
        acumulados = []
        total_alertas = 0

        for leitura in leituras:
            if leitura[0] == id_escada:
                if leitura_em_alerta(leitura):
                    total_alertas += 1

                horarios.append(leitura[3])
                acumulados.append(total_alertas)

        posicao_linear, comparacoes_linear = buscar_primeiro_limite_linear(
            acumulados, 5
        )

        posicao_binaria, comparacoes_binaria = buscar_primeiro_limite_binaria(
            acumulados, 5
        )

        if posicao_linear != posicao_binaria:
            raise ValueError(
                "As buscas encontraram posições diferentes: " + id_escada
            )

        if posicao_linear == -1:
            horario = ""
            situacao = "Limite não atingido"
        else:
            horario = horarios[posicao_linear]
            situacao = "Limite atingido"
            escadas_com_limite += 1

        resultados.append([
            id_escada,
            len(acumulados),
            total_alertas,
            situacao,
            posicao_linear,
            posicao_binaria,
            horario,
            comparacoes_linear,
            comparacoes_binaria
        ])

        total_linear += comparacoes_linear
        total_binaria += comparacoes_binaria

        print(
            id_escada,
            "|", situacao,
            "| Linear:", comparacoes_linear,
            "| Binária:", comparacoes_binaria
        )

    with open(
        "comparacao_alertas.csv",
        "w",
        encoding="utf-8",
        newline=""
    ) as arquivo:
        escritor = csv.writer(arquivo)

        escritor.writerow([
            "id_escada",
            "quantidade_leituras",
            "total_alertas",
            "situacao",
            "posicao_linear",
            "posicao_binaria",
            "horario_quinto_alerta",
            "comparacoes_linear",
            "comparacoes_binaria"
        ])

        escritor.writerows(resultados)

    print("\nEscadas analisadas:", len(escadas))
    print("Escadas que atingiram cinco alertas:", escadas_com_limite)
    print("Total de comparações da linear:", total_linear)
    print("Total de comparações da binária:", total_binaria)
    print("Arquivo gerado: comparacao_alertas.csv")