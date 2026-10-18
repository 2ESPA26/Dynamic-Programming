import random
import csv

from carregar_dados import escadas
from busca_linear import busca_linear
from busca_binaria import busca_binaria

escadas_ordenadas = sorted(escadas)

random.seed(42)

total_linear = 0
total_binaria = 0

for i in range(1000):
    procurado = random.choice(escadas)

    posicao_linear, comparacoes_linear = busca_linear(
        escadas, procurado
    )

    posicao_binaria, comparacoes_binaria = busca_binaria(
        escadas_ordenadas, procurado
    )

    total_linear += comparacoes_linear
    total_binaria += comparacoes_binaria

print("Quantidade de consultas:", 1000)

print("\nBusca linear:")
print("Total de comparações:", total_linear)
print("Média por consulta:", total_linear / 1000)

print("\nBusca binária:")
print("Total de comparações:", total_binaria)
print("Média por consulta:", total_binaria / 1000)

with open(
    "comparacao_buscas.csv",
    "w",
    newline="",
    encoding="utf-8"
) as arquivo:
    escritor = csv.writer(arquivo)

    escritor.writerow([
        "busca",
        "consultas",
        "total_comparacoes",
        "media_comparacoes"
    ])

    escritor.writerow([
        "linear",
        1000,
        total_linear,
        total_linear / 1000
    ])

    escritor.writerow([
        "binaria",
        1000,
        total_binaria,
        total_binaria / 1000
    ])