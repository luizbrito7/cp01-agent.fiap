<h1 align="center">Agente de incidentes com análise temporal</h1>

<p align="center">
  Agente de IA que investiga incidentes de cloud e prevê quando um recurso vai esgotar
</p>

<p align="center"><img src="docs/arch.gif" alt="O SRE envia o incidente ao agente.py, que conversa com o Claude Sonnet 5 pelo Amazon Bedrock, executa as tools do tools.py sobre o cenario.py e envia o relatório final pelo Gmail" /></p>

<p align="center">
  <img src="docs/icons/python.svg" height="44" alt="Python" />
  <img src="docs/icons/AmazonBedrock.svg" height="44" alt="Amazon Bedrock" />
  <img src="docs/icons/claude.svg" height="44" alt="Claude" />
  <img src="docs/icons/gmail.svg" height="44" alt="Gmail" />
</p>

## Sobre

Checkpoint individual da FIAP. Evolui o agente minimalista do professor com a tool `analisar_serie_temporal`, um cenário de memory leak no `checkout-api`, o port da OpenAI para o Claude Sonnet 5 no AWS Bedrock e o envio do relatório por e-mail.

## Como rodar

```bash
python3 -m venv .venv && .venv/bin/pip install "anthropic[bedrock]" python-dotenv
cp .env.example .env
.venv/bin/python agente.py
```

Requer o profile do AWS CLI definido em `agente.py`, com acesso ao Bedrock, e a senha de app do Gmail no `.env`.
