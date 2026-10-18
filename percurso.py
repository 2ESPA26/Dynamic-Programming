import csv


def criar_linha():
    # Estação e minutos até a próxima.
    # Tempos simulados para a atividade.
    linha = [
        ["Luz", 3],
        ["República", 3],
        ["Higienópolis-Mackenzie", 2],
        ["Paulista", 3],
        ["Oscar Freire", 3],
        ["Fradique Coutinho", 2],
        ["Faria Lima", 3],
        ["Pinheiros", 0]
    ]

    with open(
        "linha.csv", "w", encoding="utf-8", newline=""
    ) as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["estacao", "minutos_proxima"])
        escritor.writerows(linha)


def carregar_linha():
    linha = []

    with open(
        "linha.csv", encoding="utf-8", newline=""
    ) as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)

        for registro in leitor:
            estacao = registro[0]
            minutos = int(registro[1])

            linha.append([estacao, minutos])

    return linha


def tempo_ate(linha, estacao):
    """Busca a estação e soma os minutos desde a base."""
    minutos = 0

    for i in range(len(linha)):
        if linha[i][0] == estacao:
            return minutos

        minutos += linha[i][1]

    raise ValueError("Estação não encontrada: " + estacao)


def rota_ida_e_volta(linha, estacao):
    """Empilha as estações na ida e desempilha na volta."""
    ida = []
    volta = []
    pilha = []
    encontrada = False

    for i in range(len(linha)):
        nome = linha[i][0]

        ida.append(nome)
        pilha.append(nome)

        if nome == estacao:
            encontrada = True
            break

    if encontrada == False:
        raise ValueError("Estação não encontrada: " + estacao)

    while pilha:
        nome = pilha.pop()
        volta.append(nome)

    return ida, volta


def salvar_tempos(linha):
    resultados = []

    for i in range(len(linha)):
        estacao = linha[i][0]
        minutos_ida = tempo_ate(linha, estacao)

        resultados.append([
            estacao,
            minutos_ida,
            minutos_ida * 2
        ])

    with open(
        "tempos_base.csv", "w", encoding="utf-8", newline=""
    ) as arquivo:
        escritor = csv.writer(arquivo)

        escritor.writerow([
            "estacao",
            "minutos_ida",
            "minutos_ida_volta"
        ])

        escritor.writerows(resultados)


if __name__ == "__main__":
    criar_linha()
    linha = carregar_linha()
    salvar_tempos(linha)

    print("Base:", linha[0][0])

    for i in range(len(linha)):
        estacao = linha[i][0]

        minutos = tempo_ate(linha, estacao)
        ida, volta = rota_ida_e_volta(linha, estacao)

        print("\nEstação:", estacao)
        print("Ida:", " -> ".join(ida))
        print("Volta:", " -> ".join(volta))
        print("Minutos de ida:", minutos)
        print("Minutos de ida e volta:", minutos * 2)

    print("\nArquivos gerados: linha.csv e tempos_base.csv")