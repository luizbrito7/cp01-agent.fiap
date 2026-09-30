## -- Arquivo 100% escrito pelo Luiz ---

1. o que é rediness e livess probes e como esse conceito vai ser utilizado nesse laboratório? 
- Readiness probes determine when a container is ready to accept traffic.
    - aqui a app tá no ar e pronta pra receber tráfego 
    - aqui a app sai do ar quando mesmo no ar não está funcionando 100%
- Liveness probes determine when to restart a container.
    - aqui é se a app tá no ar
    - a app pode tá no ar, mas pode não tá funcional 100%

2. como o prometheus se integra?
- ele vai ser o coletor de métricas onde vai ser possíveis consultar dados sobre nossa aplicação

3. qual o papel do prom-client?
- é o que expoe as métricas para que o prometheus possa coletar. 

