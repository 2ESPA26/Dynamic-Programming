def leitura_em_alerta(leitura):
    vibracao = float(leitura[4])
    temperatura = float(leitura[5])
    corrente = float(leitura[6])
    tensao = float(leitura[7])
    nivel_oleo = float(leitura[8])
    velocidade = float(leitura[9])

    if vibracao < 1 or vibracao > 4:
        return True

    if temperatura < 35 or temperatura > 65:
        return True

    if corrente < 10 or corrente > 25:
        return True

    if tensao < 361 or tensao > 399:
        return True

    if nivel_oleo < 60 or nivel_oleo > 100:
        return True

    if velocidade < 0.48 or velocidade > 0.52:
        return True

    return False

if __name__ == "__main__":
    leitura = [
        "SIM-ECR-001",
        "ESTACAO-01",
        "crítica",
        "2026-08-01T00:00:00",
        "2.5",
        "70",
        "18",
        "380",
        "80",
        "0.50"
    ]

    print("Leitura em alerta:", leitura_em_alerta(leitura))