from carregar_dados import escadas

escadas_ordenadas = sorted(escadas)

inicio = 0
fim = len(escadas_ordenadas) - 1

meio = (inicio + fim) // 2

print("Lista ordenada:", escadas_ordenadas)
print("Posição inicial:", inicio)
print("Posição final:", fim)
print("Posição do meio:", meio)
print("Escada do meio:", escadas_ordenadas[meio])

from carregar_dados import escadas

escadas_ordenadas = sorted(escadas)
procurado = "SIM-ECR-001"

inicio = 0
fim = len(escadas_ordenadas) - 1

comparacoes = 0
posicao = -1

while inicio <= fim:
    meio = (inicio + fim) // 2
    comparacoes += 1

    if escadas_ordenadas[meio] == procurado:
        posicao = meio
        break

    elif procurado < escadas_ordenadas[meio]:
        fim = meio - 1

    else:
        inicio = meio + 1

if posicao == -1:
    print("Escada não encontrada")
else:
    print("Escada encontrada na posição:", posicao)

print("Comparações:", comparacoes)