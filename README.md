# Escala — Dynamic Programming

## Integrantes

| Nome | RM |
|------|-----|
| Gabriel Ardito | 568318 |
| João Gonzales | 568166 |
| Giovanna Oliveira | 566643 |
| Marianne Mukai | 568001 |
| Maria Druzeic | 566634 |

Implementação da atividade revisada do Desafio Motiva, em Python puro.

## Estado do projeto

Etapa 0 e atividades 1, 2 e 3 implementadas. O notebook.ipynb contém código,
saídas executadas, tabelas e interpretação dos experimentos.

## Executar

Na pasta do repositório, com Python 3.10 ou superior, sem dependências externas:

```text
python percurso.py
python gerar_dataset.py
python comparar_buscas.py
python alertas_acumulados.py
python planejamento.py
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
- Oito estações da Linha 4-Amarela, em ordem: Luz, República, Higienópolis-Mackenzie,
  Paulista, Oscar Freire, Fradique Coutinho, Faria Lima e Pinheiros.
- Base simulada em Luz. Tempos de deslocamento hipotéticos e iguais nos dois sentidos.
  Fonte dos nomes e ordem: https://trilhos.motiva.com.br/viaquatro/linha-4---amarela/

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

## Notebook e entrega

Abra `notebook.ipynb` em Jupyter ou em um editor compatível, mantendo os módulos
Python na mesma pasta. Reinicie o kernel e execute as células de cima para baixo.
O notebook acompanha as funções dos arquivos `.py` e inclui as saídas dos experimentos.
Os algoritmos usam somente a biblioteca padrão. Jupyter é necessário apenas para
executar a interface do notebook. A execução recria os CSVs na pasta do projeto.

A entrega é o link do repositório GitHub via Teams, com notebook executado,
arquivos de dados, módulos Python e este README.

## Busca linear e binária

`carregar_dados.py` lê uma entrada por ID, mantendo a ordem do arquivo.
`busca_linear.py` e `busca_binaria.py` implementam as buscas manualmente.
`comparar_buscas.py` usa 1.000 consultas com reposição e semente 42.
As buscas recebem os mesmos alvos: a linear usa a ordem original e a binária,
a ordem crescente. A unidade registrada é uma posição consultada; não contamos
separadamente os dois testes condicionais da binária. Preparação e ordenação
ficam fora da contagem. Não foram medidos tempos de execução.

| Busca | Consultas | Total de posições consultadas | Média |
| --- | --- | --- | --- |
| Linear | 1.000 | 15.569 | 15,569 |
| Binária | 1.000 | 4.082 | 4,082 |

A redução ocorre porque a binária descarta metade do intervalo a cada repetição.
O experimento considera alvos existentes; o notebook também mostra um ID ausente.
Resultados em `comparacao_buscas.csv`.

`alertas.py` aplica os seis limites. `alertas_acumulados.py` compara as buscas
pela primeira leitura com pelo menos cinco alertas acumulados em todas as escadas.
A binária continua à esquerda após encontrar um valor que atende ao limite.
O acumulado não diminui e já está ordenado. Ausência é representada por -1,
com horário vazio. Resultados em `comparacao_alertas.csv`.

## Percurso e planejamento

`percurso.py` cria `linha.csv` e `tempos_base.csv`, encontra estações com busca
linear e representa ida e volta com pilha (`append` e `pop`). Pinheiros fica
a 19 minutos de Luz no cenário, totalizando 38 de ida e volta.

`planejamento.py` cria filas por grupo, ordenadas pelo primeiro alerta, com
ID como desempate. O planejamento usa o primeiro alerta, não o quinto.
Processa a fila crítica antes da normal, retirando com `pop(0)`.
Cada atendimento inclui ida, serviço e volta à base. Serviço: 60 minutos para
críticas e 40 para normais. Se um serviço não cabe, ele passa para pendentes
e o programa verifica os seguintes. Os horários são minutos desde o início do
turno; o fim inclui o retorno à base.

| Turno | Limite em minutos | Usados | Atendidos | Pendentes |
| --- | --- | --- | --- | --- |
| 4 horas | 240 | 238 | 3 | 9 |
| 4 horas menos 1 | 180 | 170 | 2 | 10 |
| 6 horas | 360 | 334 | 4 | 8 |
| 6 horas menos 1 | 300 | 246 | 3 | 9 |
| 8 horas | 480 | 480 | 6 | 6 |
| 8 horas menos 1 | 420 | 412 | 5 | 7 |

Os 12 equipamentos em alerta ficam na agenda ou em pendentes, sem duplicação.
Todos os cenários respeitam o limite. Ao reduzir uma hora, os últimos atendimentos
são removidos com `pop()` até caber, sem preencher novamente a folga.
A política segue as filas; não garante quantidade máxima de serviços.

Os arquivos `turno_*_agenda.csv` e `turno_*_pendentes.csv` incluem os turnos
originais e reduzidos. O notebook mostra as agendas, as rotas e os pendentes.
O cenário é uma fotografia dos alertas do dataset; não simula novos alertas
chegando durante a execução do turno.

Não são usados grafos, `deque` ou bibliotecas prontas de busca.
