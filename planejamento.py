import csv

from alertas import leitura_em_alerta
from percurso import carregar_linha, tempo_ate, rota_ida_e_volta


def carregar_primeiros_alertas():
    """Guarda somente a primeira leitura em alerta de cada escada."""
    primeiros = {}

    with open(
        "sensores.csv", encoding="utf-8", newline=""
    ) as arquivo:
        leitor = csv.reader(arquivo)
        next(leitor)

        for leitura in leitor:
            id_escada = leitura[0]

            if leitura_em_alerta(leitura):
                if id_escada not in primeiros:
                    primeiros[id_escada] = {
                        "id_escada": id_escada,
                        "estacao": leitura[1],
                        "grupo": leitura[2],
                        "primeiro_alerta": leitura[3]
                    }

    return list(primeiros.values())


def montar_filas(alertas):
    fila_critica = []
    fila_normal = []

    # Datas ISO podem ser ordenadas como texto neste dataset.
    ordenados = sorted(
        alertas,
        key=lambda escada: (
            escada["primeiro_alerta"],
            escada["id_escada"]
        )
    )

    for escada in ordenados:
        if escada["grupo"] == "crítica":
            fila_critica.append(escada)
        else:
            fila_normal.append(escada)

    return fila_critica, fila_normal


def planejar_turno(base, horas):
    linha = carregar_linha()

    if base != linha[0][0]:
        raise ValueError("A base deve ser a primeira estação da linha.")

    if horas < 0:
        raise ValueError("A duração do turno não pode ser negativa.")

    alertas = carregar_primeiros_alertas()
    fila_critica, fila_normal = montar_filas(alertas)

    agenda = []
    pendentes = []
    tempo_usado = 0
    limite = horas * 60

    # Percorre toda a fila crítica antes da normal.
    for fila in [fila_critica, fila_normal]:
        while fila:
            escada = fila.pop(0)

            if escada["grupo"] == "crítica":
                servico = 60
            else:
                servico = 40

            ida = tempo_ate(linha, escada["estacao"])
            custo = ida + servico + ida

            if tempo_usado + custo <= limite:
                rota_ida, rota_volta = rota_ida_e_volta(
                    linha, escada["estacao"]
                )

                atendimento = {
                    "id_escada": escada["id_escada"],
                    "estacao": escada["estacao"],
                    "grupo": escada["grupo"],
                    "primeiro_alerta": escada["primeiro_alerta"],
                    "rota_ida": " -> ".join(rota_ida),
                    "rota_volta": " -> ".join(rota_volta),
                    "inicio_minutos": tempo_usado,
                    "fim_minutos": tempo_usado + custo,
                    "minutos_servico": servico
                }

                agenda.append(atendimento)
                tempo_usado += custo
            else:
                pendentes.append(escada)

    return agenda, pendentes


def reduzir_turno(agenda, pendentes, novas_horas):
    """Desfaz os últimos atendimentos até a agenda caber."""
    if novas_horas < 0:
        raise ValueError("A duração do turno não pode ser negativa.")

    # Copia as listas para preservar o plano original.
    nova_agenda = list(agenda)
    novos_pendentes = list(pendentes)
    limite = novas_horas * 60

    while nova_agenda:
        if nova_agenda[-1]["fim_minutos"] <= limite:
            break

        removido = nova_agenda.pop()

        novos_pendentes.append({
            "id_escada": removido["id_escada"],
            "estacao": removido["estacao"],
            "grupo": removido["grupo"],
            "primeiro_alerta": removido["primeiro_alerta"]
        })

    return nova_agenda, novos_pendentes


def salvar_plano(nome, agenda, pendentes):
    with open(
        nome + "_agenda.csv", "w", encoding="utf-8", newline=""
    ) as arquivo:
        colunas = [
            "id_escada",
            "estacao",
            "grupo",
            "primeiro_alerta",
            "rota_ida",
            "rota_volta",
            "inicio_minutos",
            "fim_minutos",
            "minutos_servico"
        ]

        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(agenda)

    with open(
        nome + "_pendentes.csv", "w", encoding="utf-8", newline=""
    ) as arquivo:
        colunas = [
            "id_escada",
            "estacao",
            "grupo",
            "primeiro_alerta"
        ]

        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(pendentes)


def mostrar_resumo(nome, agenda, pendentes):
    tempo_usado = 0

    if agenda:
        tempo_usado = agenda[-1]["fim_minutos"]

    print("\nPlano:", nome)
    print("Atendimentos:", len(agenda))
    print("Pendentes:", len(pendentes))
    print("Minutos utilizados:", tempo_usado)


if __name__ == "__main__":
    linha = carregar_linha()
    base = linha[0][0]

    for horas in [4, 6, 8]:
        agenda, pendentes = planejar_turno(base, horas)

        nome = "turno_" + str(horas) + "h"
        salvar_plano(nome, agenda, pendentes)
        mostrar_resumo(nome, agenda, pendentes)

        agenda_reduzida, pendentes_reduzidos = reduzir_turno(
            agenda, pendentes, horas - 1
        )

        nome_reduzido = nome + "_menos_1h"

        salvar_plano(
            nome_reduzido,
            agenda_reduzida,
            pendentes_reduzidos
        )

        mostrar_resumo(
            nome_reduzido,
            agenda_reduzida,
            pendentes_reduzidos
        )