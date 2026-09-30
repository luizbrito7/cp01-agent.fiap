# Decisões de Arquitetura

Uma linha por decisão. Decisão aceita não se edita: se mudar de ideia, adicionar uma nova linha e marcar a antiga como substituída.

| # | Decisão | Por quê | Rejeitado |
|---|---------|---------|-----------|
| 1 | Laboratório real em Docker Compose | O mockup do notebook entrega evidência inventada | floci, que emula API de nuvem e não guarda série temporal |
| 2 | Vazamento de memória até OOM kill e restart | Depois do restart o estado atual mente, então a causa só existe na série | Pico periódico e deploy suspeito |
| 3 | Segundo cenário com Postgres fora | Com um cenário só, o agente acerta por sorte e não dá para avaliar | Cenário único |
| 4 | Falha parcial: `/liveness` sem banco, `/readiness` com banco | Container `up` e métrica normal com usuário em erro obriga cruzar log e métrica | Derrubar o app inteiro |
| 5 | Prometheus com `predict_linear` | O OOM kill apaga qualquer histórico guardado dentro do app, então o historiador precisa ser externo. Também tira a aritmética do LLM e devolve um número no lugar de centenas de pontos, cortando token em toda rodada | App guardar o próprio histórico, e arquivo em volume, que exigiria reescrever coleta, janela e cálculo à mão |
| 6 | Grafana no compose | Prova visual na demonstração. Não serve ao agente | Não usar |
| 7 | App em Node.js, Express, HTML puro e `prom-client` | Front sem build e botão do vazamento visível no palco | App em Python |
| 8 | Agente em Python puro, sem framework | Loop visível linha por linha é requisito para explicar na apresentação | LangChain e Agents SDK |
