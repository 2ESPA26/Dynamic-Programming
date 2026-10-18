import argparse
import csv
import random
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from percurso import carregar_linha
from statistics import mean

FAIXAS = {
    'vibracao': (1.0, 4.0),
    'temperatura': (35.0, 65.0),
    'corrente': (10.0, 25.0),
    'tensao': (361.0, 399.0),
    'nivel_oleo': (60.0, 100.0),
    'velocidade': (0.48, 0.52),
}
COLUNAS = ['id_escada', 'estacao', 'grupo', 'data_hora', *FAIXAS]
INICIO = datetime(2026, 8, 1)


def salvar_csv(caminho, colunas, registros):
    """Salva registros em CSV UTF-8, com cabeçalho e separador vírgula."""
    with Path(caminho).open('w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(registros)


def gerar_dataset(n_escadas, n_leituras, semente):
    """Salva sensores.csv e retorna (leituras, cadastros com perfil).

    Embaralha os blocos das escadas, preservando a ordem horária dentro
    de cada bloco. Os dados são uma simulação acadêmica, não medições reais.
    """
    if type(n_escadas) is not int or not 30 <= n_escadas <= 197:
        raise ValueError('n_escadas deve ser inteiro entre 30 e 197.')
    if type(n_leituras) is not int or n_leituras < 200:
        raise ValueError('n_leituras deve ser inteiro maior ou igual a 200.')
    if type(semente) is not int:
        raise ValueError('semente deve ser um número inteiro.')
    random.seed(semente)
    saudaveis = round(n_escadas * 0.6)
    desgaste = round(n_escadas * 0.3)
    perfis = (['saudavel'] * saudaveis + ['desgaste_gradual'] * desgaste
              + ['falhas_pontuais'] * (n_escadas - saudaveis - desgaste))
    random.shuffle(perfis)
    cadastros = []
    blocos = []
    linha = carregar_linha()
    for numero, perfil in enumerate(perfis, start=1):
        cadastro = {
            'id_escada': f'SIM-ECR-{numero:03d}',
            'estacao': linha[(numero - 1) % len(linha)][0],
            'grupo': 'crítica' if numero % 3 == 0 else 'não crítica',
            'perfil': perfil,
        }
        cadastros.append(cadastro)
        # Centros próprios por equipamento, sempre dentro da faixa normal.
        centros = {sensor: random.uniform(lo + (hi-lo)*0.3, lo + (hi-lo)*0.7)
                   for sensor, (lo, hi) in FAIXAS.items()}
        sensor_afetado = random.choice(list(FAIXAS))
        horas_falha = set(random.sample(range(n_leituras), max(5, n_leituras // 40)))
        bloco = []
        for hora in range(n_leituras):
            registro = {k: cadastro[k] for k in COLUNAS[:3]}
            registro['data_hora'] = (INICIO + timedelta(hours=hora)).isoformat()
            for sensor, (lo, hi) in FAIXAS.items():
                amplitude = hi - lo
                valor = centros[sensor] + random.uniform(-0.05, 0.05) * amplitude
                if sensor == sensor_afetado:
                    direcao = -1 if sensor in ('nivel_oleo', 'velocidade') else 1
                    if perfil == 'desgaste_gradual':
                        valor += direcao * amplitude * 0.9 * hora / (n_leituras - 1)
                    elif perfil == 'falhas_pontuais' and hora in horas_falha:
                        valor = (lo - 0.2 * amplitude if direcao < 0 else hi + 0.2 * amplitude)
                registro[sensor] = round(valor, 4)
            bloco.append(registro)
        blocos.append(bloco)
    random.shuffle(blocos)
    # Garante ordem de IDs não crescente mesmo em um embaralhamento excepcional.
    if all(blocos[i][0]['id_escada'] < blocos[i+1][0]['id_escada'] for i in range(len(blocos)-1)):
        blocos.reverse()
    leituras = [registro for bloco in blocos for registro in bloco]
    salvar_csv('sensores.csv', COLUNAS, leituras)
    return leituras, cadastros


def gerar_resumos(leituras, cadastros):
    """Salva estatísticas por sensor e contagem de equipamentos por perfil."""
    resumo = []
    for sensor in FAIXAS:
        valores = [registro[sensor] for registro in leituras]
        resumo.append({'sensor': sensor, 'minimo': min(valores),
                       'media': round(mean(valores), 4), 'maximo': max(valores)})
    salvar_csv('resumo_sensores.csv', ['sensor', 'minimo', 'media', 'maximo'], resumo)
    contagens = Counter(cadastro['perfil'] for cadastro in cadastros)
    salvar_csv('resumo_perfis.csv', ['perfil', 'quantidade'],
               [{'perfil': perfil, 'quantidade': quantidade} for perfil, quantidade in contagens.items()])
    salvar_csv('perfis_escadas.csv', ['id_escada', 'estacao', 'grupo', 'perfil'], cadastros)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--escadas', type=int, default=30)
    parser.add_argument('--leituras', type=int, default=240)
    parser.add_argument('--semente', type=int, default=42)
    args = parser.parse_args()
    leituras, cadastros = gerar_dataset(args.escadas, args.leituras, args.semente)
    gerar_resumos(leituras, cadastros)
    print(f'Geradas {len(leituras)} leituras de {len(cadastros)} escadas.')
    print('Arquivos salvos na pasta atual. Semente:', args.semente)


if __name__ == '__main__':
    main()
