# Roteiro de apresentação (10 min)

Comando da demo: `.venv/bin/python agente.py`

| Tempo | Mostrar | Falar |
|---|---|---|
| 0:00 a 0:45 | Nada | O agente original só enxerga a foto do momento. Eu dei a ele a visão do tempo. |
| 0:45 a 2:15 | `cenario.py`, linha 17 | O `dep-398` causou um vazamento de memória no `checkout-api`: estável em 40%, hoje em 72%. A CPU segue estável, então não é carga. |
| 2:15 a 3:45 | `tools.py`, linha 83 | `analisar_serie_temporal`: base normal, tendência, início, taxa e previsão. A conta é feita em Python e o modelo recebe só o resumo. |
| 3:45 a 6:45 | Terminal | Demo. Destacar a resposta da tool (0,25% por hora, 110 h até esgotar), o cruzamento com o deploy, o relatório, as métricas e o e-mail recebido. |
| 6:45 a 7:45 | `agente.py`, linha 13 | Port da OpenAI para o Claude Sonnet 5 no AWS Bedrock. Mudaram o cliente, o schema das tools e o loop. |
| 7:45 a 9:15 | `agente.py`, função `metricas` | Evolução: tools em paralelo (de 8 rodadas para 3 a 6), métricas ao fim de cada investigação, e-mail e código em três módulos. |
| 9:15 a 10:00 | Nada | O agente achou o problema antes de virar incidente. Limites: uma série só e previsão linear. |

## Antes de começar

- Senha de app preenchida no `.env`.
- `aws sts get-caller-identity --profile ntt-presales` respondendo.
- Uma execução salva como plano B: `.venv/bin/python agente.py | tee docs/saida-backup.txt`

## Se o tempo apertar

Encurtar o port para duas frases. Não cortar a resposta da tool na demo.

## Perguntas prováveis

- **Por que a conta em Python?** Resultado exato e menos tokens. O modelo fica com a interpretação.
- **O deploy é a causa comprovada?** Não. É correlação temporal forte, e o agente recomenda validar depois do rollback.
- **Por que o Sonnet 5 e não o 5.5?** O 5.5 não estava liberado na conta.
- **O agente executa o rollback?** Não. Ele só abre o pedido, que depende de aprovação humana.
