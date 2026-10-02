# Prompt para o Claude Design

Crie uma apresentação de 5 slides em português do Brasil para uma demonstração técnica de 10 minutos em sala de aula. O público são colegas de turma e o professor, todos da área de tecnologia. Os slides apoiam a fala e uma demo ao vivo no terminal, então cada slide deve ser entendido em poucos segundos.

## Estilo

- Fonte Poppins em todos os textos. Para código, uma fonte monoespaçada.
- Paleta em tons de azul: fundo azul bem escuro, azul médio nos destaques e azul claro nos textos de apoio.
- Pouco texto: um título curto e no máximo três frases curtas por slide. Sem parágrafos.
- O código é o elemento visual principal: blocos grandes, com realce de sintaxe, cantos arredondados e a linha mais importante destacada.
- Formato 16:9, com muito espaço vazio e uma ideia por slide.

## Slides

**1. Capa.** Título: "Agente de incidentes com visão do tempo". Subtítulo: "Análise temporal, Claude Sonnet 5 no AWS Bedrock". Autor: Luiz Brito, FIAP.

**2. O problema.** Título: "A foto engana, a série revela". Um gráfico de linha da memória do `checkout-api` com os valores 40, 40, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70 e 72, com uma marca vertical no terceiro ponto chamada "deploy dep-398". Ao lado, este bloco:

```python
"memoria_pct": {
    "atual": 72,
    "serie": [
        # antes do dep-398: memoria estavel
        {"data_hora": "2026-09-06 08:00", "valor": 40},
        # depois do dep-398: memory leak
        {"data_hora": "2026-09-06 20:00", "valor": 43},
        {"data_hora": "2026-09-11 14:00", "valor": 72},
    ],
},
```

**3. A tool temporal.** Título: "Cinco passos, calculados em Python". Mostrar o código à esquerda e a resposta à direita:

```python
base = median(ponto["valor"] for ponto in serie[:3])      # 1. base normal
tendencia = _tendencia(atual["valor"], base)              # 2. tendencia
inicio = primeiro_ponto_acima(serie, base + MARGEM)       # 3. inicio do crescimento
taxa = _taxa_por_hora(inicio, atual)                      # 4. taxa por hora
horas_ate_esgotar = round((100 - atual["valor"]) / taxa)  # 5. previsao
```

```json
{
  "tendencia": "crescente",
  "inicio_crescimento": "2026-09-06 20:00",
  "taxa_pct_por_hora": 0.25,
  "horas_ate_esgotar": 110
}
```

**4. Port para o Bedrock.** Título: "Da OpenAI para o Claude". Dois blocos lado a lado, com os rótulos "Antes" e "Depois":

```python
client = OpenAI()
client.responses.create(model="gpt-5.6-luna", instructions=INSTRUCOES, input=historico, tools=TOOLS)
```

```python
client = AnthropicBedrockMantle(aws_region="us-east-1")
client.messages.create(model="anthropic.claude-sonnet-5", system=INSTRUCOES, messages=historico, tools=TOOLS)
```

**5. Resultado.** Título: "Cada investigação termina com métricas". À esquerda, este bloco no estilo de saída de terminal. À direita, três itens curtos: "Tools em paralelo", "Relatório por e-mail" e "Código em três módulos".

```text
entregou_relatorio: True
enviou_email: True
rodadas: 3
chamadas_de_tools: 6
custo_estimado_usd: 0.0315
```

Use exatamente os trechos de código e os números acima, sem inventar outros.
