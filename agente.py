import json
import os
from pathlib import Path

from anthropic import AnthropicBedrockMantle
from dotenv import load_dotenv

from tools import TOOLS, executar_ferramenta

load_dotenv(Path(__file__).with_name(".env"))
os.environ["AWS_PROFILE"] = "ntt-presales"

client = AnthropicBedrockMantle(aws_region="us-east-1")
MODEL = "anthropic.claude-sonnet-5"
MAX_RODADAS = 8
MAX_OUTPUT_TOKENS = 1000
LIMITE_ESTIMADO_USD = 0.10
PRECO_INPUT_1M = 2.00
PRECO_OUTPUT_1M = 10.00


INSTRUCOES = '''
Voce e o agente legista de incidentes Cloud da Loja Nebulosa.
Seu objetivo e investigar a causa raiz usando apenas evidencias retornadas pelas ferramentas.

Regras:
- Nao trate proximidade temporal como prova de causalidade.
- Investigue primeiro; nao chute valores ou eventos.
- Faca consultas curtas e seletivas.
- Encerre assim que a evidencia for suficiente; nao consulte o que nao muda a conclusao.
- Diferencie sintoma, causa raiz e impacto financeiro.
- Se houver evidencia suficiente, solicite rollback com justificativa objetiva.
- Nunca diga que uma acao foi executada quando a ferramenta disser que aguarda aprovacao.
- Encerre com: diagnostico, evidencias, impacto, acao recomendada e nivel de confianca.
- O relatorio final vai direto ao ponto, sem introducao, com no maximo 150 palavras.
- Seja conciso.
'''.strip()

INCIDENTE = '''
INC-2026-0911: desde 14h03, usuarios relatam lentidao no e-commerce.
O api-gateway disparou alerta de latencia e o custo cloud esta subindo.
Descubra a causa raiz e recomende a resposta operacional mais segura.
'''.strip()

INCIDENTE_CHECKOUT = '''
INC-2026-0912: em 2026-09-11 14:00, o monitoramento alertou memoria do checkout-api em 72%.
Nao ha reclamacao de usuarios ainda, mas o time quer saber se existe risco.
Descubra a causa e recomende a resposta operacional mais segura.
'''.strip()


def estimar_custo(input_tokens, output_tokens):
    """Custo estimado em dolares a partir dos tokens consumidos."""
    return (
        input_tokens * PRECO_INPUT_1M / 1_000_000
        + output_tokens * PRECO_OUTPUT_1M / 1_000_000
    )


def investigar_incidente(incidente=INCIDENTE):
    """Roda o loop do agente ate o relatorio final ou ate um dos limites."""
    historico = [{"role": "user", "content": incidente}]
    resumo = {
        "resposta": None,
        "input_tokens": 0,
        "output_tokens": 0,
        "custo_estimado_usd": 0,
        "rodadas": 0,
        "ferramentas_usadas": [],
    }

    for rodada in range(1, MAX_RODADAS + 1):
        resposta = client.messages.create(
            model=MODEL,
            system=INSTRUCOES,
            messages=historico,
            tools=TOOLS,
            thinking={"type": "disabled"},
            max_tokens=MAX_OUTPUT_TOKENS,
        )

        resumo["rodadas"] = rodada
        resumo["input_tokens"] += resposta.usage.input_tokens
        resumo["output_tokens"] += resposta.usage.output_tokens
        resumo["custo_estimado_usd"] = estimar_custo(resumo["input_tokens"], resumo["output_tokens"])
        print(f"\n--- Rodada {rodada} | custo estimado acumulado: US$ {resumo['custo_estimado_usd']:.6f} ---")

        # Preserva mensagens e chamadas do modelo para a proxima rodada.
        historico.append({"role": "assistant", "content": resposta.content})
        chamadas = [bloco for bloco in resposta.content if bloco.type == "tool_use"]

        if not chamadas:
            resumo["resposta"] = "".join(bloco.text for bloco in resposta.content if bloco.type == "text")
            print("\nRELATORIO FINAL\n")
            print(resumo["resposta"])
            resumo["email"] = executar_ferramenta(
                "enviar_relatorio_email",
                {"assunto": f"Relatorio {incidente.split(':')[0]}", "corpo": resumo["resposta"]},
            )
            print("\nE-mail:", json.dumps(resumo["email"], ensure_ascii=False))
            return resumo

        resultados = []
        for chamada in chamadas:
            print(f"Agente pediu: {chamada.name}({chamada.input})")
            resultado = executar_ferramenta(chamada.name, chamada.input)
            resumo["ferramentas_usadas"].append({"nome": chamada.name, "argumentos": chamada.input})
            print("Observacao:", json.dumps(resultado, ensure_ascii=False))
            resultados.append({
                "type": "tool_result",
                "tool_use_id": chamada.id,
                "content": json.dumps(resultado, ensure_ascii=False),
            })
        historico.append({"role": "user", "content": resultados})

        if resumo["custo_estimado_usd"] >= LIMITE_ESTIMADO_USD:
            print(f"\nLimite didatico estimado de US$ {LIMITE_ESTIMADO_USD:.2f} atingido.")
            return {**resumo, "interrompido": True}

    print("\nNumero maximo de rodadas atingido. O agente foi interrompido pelo software.")
    return {**resumo, "interrompido": True}


def metricas(resumo):
    """Metricas da investigacao, validas para qualquer incidente."""
    return {
        "entregou_relatorio": bool(resumo["resposta"]),
        "enviou_email": resumo.get("email", {}).get("status") == "enviado",
        "rodadas": resumo["rodadas"],
        "chamadas_de_tools": len(resumo["ferramentas_usadas"]),
        "custo_estimado_usd": round(resumo["custo_estimado_usd"], 4),
    }


if __name__ == "__main__":
    resumo = investigar_incidente(INCIDENTE_CHECKOUT)
    print("\nMETRICAS\n")
    for nome, valor in metricas(resumo).items():
        print(f"{nome}: {valor}")
