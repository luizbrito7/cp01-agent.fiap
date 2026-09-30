# Roadmap

Evoluir o agente de `assets/Agente_de_IA_Minimalista.ipynb` conforme `assets/context.md`, trocando o mockup de métricas por um laboratório real em Docker Compose.

## Tarefas

### Laboratório

- [x] App em Node.js com Express: `/liveness` e rota que dispara o vazamento
- [ ] `/readiness` com banco, rota que consulta o banco e botão no front
- [x] Expor a métrica de memória do app para o Prometheus
- [x] Compose com app e Prometheus coletando de 1 em 1 segundo
- [ ] Adicionar Postgres e Grafana ao compose
- [x] Limite de memória no container do app
- [ ] Dashboard mínimo no Grafana

### Agente

- [ ] Tool de análise temporal consultando Prometheus com `predict_linear`
- [ ] Trocar as tools de mockup pelas que leem o laboratório real
- [ ] Ajustar o prompt para cobrir os dois cenários

### Avaliação

- [ ] Cenário 1: conferir se usa a tool temporal e acerta o vazamento
- [ ] Cenário 2: conferir se acerta a conexão com o banco sem usar a tool temporal
- [ ] Registrar custo estimado e número de rodadas de cada execução

### Porte de LLM

- [ ] Portar o loop para outra LLM e comparar resposta, custo e uso de tools

## Entrega

- 7 pontos: os quatro itens pedidos no `context.md`
- 3 pontos de inovação: laboratório real no lugar do mockup, extrapolação determinística no Prometheus e redução de token na consulta da série

Roteiro da demo: aperta o botão, o gráfico sobe, e com o app ainda vivo o agente prevê o estouro pela série. Depois `docker stop` no Postgres e o agente aponta a conexão usando o log. O OOM kill acontece sozinho no fundo e confirma a previsão.
