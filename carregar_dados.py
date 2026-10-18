import csv

escadas = []

with open("sensores.csv", encoding="utf-8", newline="") as arquivo:
    leitor = csv.reader(arquivo)

    next(leitor)

    for linha in leitor:
        id_escada = linha[0]

        if id_escada not in escadas:
            escadas.append(id_escada)

