# Escala — Dynamic Programming

Implementação da atividade revisada do Desafio Motiva, em Python puro.

## Estado do projeto

Etapa 0 implementada: geração sintética e resumos. As atividades de buscas,
percurso, planejamento e o notebook executado ainda serão desenvolvidos.

## Executar

Na pasta do repositório, com Python 3.10 ou superior, sem dependências externas:

```text
python gerar_dataset.py
```

No PyCharm, execute `gerar_dataset.py` com a pasta do repositório como diretório
de trabalho. Também é possível escolher os parâmetros:

```text
python gerar_dataset.py --escadas 30 --leituras 240 --semente 42
```

A execução substitui os CSVs gerados na pasta atual. A mesma semente e os mesmos
parâmetros reproduzem a base no mesmo ambiente Python.

## Base padrão

- 30 escadas, 240 leituras horárias por escada: 7.200 registros.
- Período: 01/08/2026 às 00h até 10/08/2026 às 23h.
- Semente: 42, configurada com `random.seed`.
- 18 escadas saudáveis, 9 em desgaste gradual e 3 com falhas pontuais.
- 10 escadas críticas e 20 não críticas. Grupo e perfil têm significados distintos:
  grupo é a prioridade de atendimento; perfil é o comportamento simulado.
- O arquivo embaralha os blocos das escadas, mantendo suas leituras em ordem temporal.
- Oito identificadores provisórios de estação (`ESTACAO-01` a `ESTACAO-08`).
  Na atividade 2, serão substituídos pelos nomes de estações de uma linha da Motiva,
  em conjunto com a criação de `linha.csv`. Não representam uma rede real ainda.

## Arquivos

| Arquivo | Conteúdo |
| --- | --- |
| `gerar_dataset.py` | Função solicitada, resumos e execução por terminal |
| `sensores.csv` | Dez colunas exigidas e todas as leituras |
| `resumo_sensores.csv` | Mínimo, média e máximo dos seis sensores |
| `resumo_perfis.csv` | Quantidade de escadas por perfil |
| `perfis_escadas.csv` | Cadastro auxiliar para conferir os perfis simulados |

`gerar_dataset(n_escadas, n_leituras, semente)` salva `sensores.csv` e retorna
as leituras e o cadastro com os perfis. `gerar_resumos` produz os demais CSVs.

## Sensores e limites

| Campo | Unidade | Faixa normal inclusiva |
| --- | --- | --- |
| vibracao | mm/s | 1 a 4 |
| temperatura | °C | 35 a 65 |
| corrente | A | 10 a 25 |
| tensao | V | 361 a 399 |
| nivel_oleo | % | 60 a 100 |
| velocidade | m/s | 0,48 a 0,52 |

CSV em UTF-8, separado por vírgulas, com ponto decimal e datas ISO 8601.
As outras colunas são `id_escada`, `estacao`, `grupo` e `data_hora`.
Uma leitura estará em alerta se pelo menos um sensor sair da faixa normal;
vários sensores fora da faixa na mesma leitura não devem multiplicar essa leitura.

## Regras da simulação e interpretação

Cada escada tem centros de operação próprios dentro das faixas sugeridas pelo
professor, com pequenas oscilações. As saudáveis permanecem nessas faixas.
No desgaste gradual, um sensor escolhido avança progressivamente para fora da
faixa. Nas falhas pontuais, um sensor ultrapassa o limite em horários isolados.
Óleo e velocidade caem; os outros sensores aumentam. Os perfis são atribuídos
aleatoriamente; a criticidade é definida separadamente a cada terceiro equipamento.
As proporções são aproximadas quando o número de escadas não é múltiplo de dez.

O resumo considera todas as leituras, inclusive anomalias: extremos fora da faixa
são esperados e não devem ser removidos automaticamente. Os perfis auxiliares
servem para auditoria; as buscas e o planejamento devem identificar alertas pelos
valores dos sensores, sem usar o perfil como atalho.

Os dados e limites têm finalidade acadêmica. Não são medições da Motiva nem
limites de diagnóstico validados. A base anterior do projeto permanece separada.

## Próximas etapas

1. Buscas linear e binária manuais, comparações e 1.000 consultas.
2. Primeira leitura que alcança cinco alertas acumulados por escada.
3. Linha com estações reais em ordem, tempos de ida e volta e pilha com listas.
4. Filas de atendimento, planos de 4, 6 e 8 horas, pendentes e redução do turno.
5. `notebook.ipynb` executado com tabelas, experimentos e interpretação.

Não usar grafos, `deque` ou bibliotecas prontas de busca.
