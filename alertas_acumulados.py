import csv

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


procurado = "SIM-ECR-001"

horarios = []
acumulados = []
total_alertas = 0

with open("sensores.csv", encoding="utf-8", newline="") as arquivo:
    leitor = csv.reader(arquivo)

    next(leitor)

    for leitura in leitor:
        if leitura[0] == procurado:
            if leitura_em_alerta(leitura):
                total_alertas += 1

            horarios.append(leitura[3])
            acumulados.append(total_alertas)

print("Escada:", procurado)
print("Quantidade de leituras:", len(acumulados))
print("Total de leituras em alerta:", total_alertas)

posicao_linear, comparacoes_linear = buscar_primeiro_limite_linear(
    acumulados, 5
)

print("\nBusca linear:")

if posicao_linear == -1:
    print("A escada não atingiu cinco alertas.")
else:
    print("Posição:", posicao_linear)
    print("Data e hora:", horarios[posicao_linear])
    print("Acumulado nessa leitura:", acumulados[posicao_linear])

print("Comparações:", comparacoes_linear)

posicao_binaria, comparacoes_binaria = buscar_primeiro_limite_binaria(
    acumulados, 5
)

print("\nBusca binária:")

if posicao_binaria == -1:
    print("A escada não atingiu cinco alertas.")
else:
    print("Posição:", posicao_binaria)
    print("Data e hora:", horarios[posicao_binaria])
    print("Acumulado nessa leitura:", acumulados[posicao_binaria])

print("Comparações:", comparacoes_binaria)