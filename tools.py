import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from statistics import median

from cenario import ambiente

SERVICOS = list(ambiente["metricas"])
MARGEM = 2
PONTOS_BASE = 3
EMAIL_RELATORIO = "luizbrito.x@gmail.com"


def _validar_servico(servico):
    """Devolve um erro se o servico nao existir no cenario."""
    if servico not in ambiente["metricas"]:
        return {"erro": f"Servico desconhecido: {servico}", "disponiveis": list(ambiente["metricas"])}
    return None


def consultar_metricas(servico):
    """Valores atuais de CPU, memoria, latencia, erros e instancias."""
    erro = _validar_servico(servico)
    if erro:
        return erro
    metricas = {
        nome: valor["atual"] if isinstance(valor, dict) else valor
        for nome, valor in ambiente["metricas"][servico].items()
    }
    return {"servico": servico, **metricas}


def buscar_logs(servico):
    """Linhas recentes de log do servico."""
    erro = _validar_servico(servico)
    return erro or {"servico": servico, "linhas": ambiente["logs"].get(servico, [])}


def consultar_deploys(servico):
    """Deploys recentes do servico."""
    erro = _validar_servico(servico)
    return erro or {"servico": servico, "deploys": ambiente["deploys"].get(servico, [])}


def consultar_configuracao(servico):
    """Configuracao operacional atual do servico."""
    erro = _validar_servico(servico)
    return erro or {"servico": servico, "configuracao": ambiente["configuracoes"].get(servico, {})}


def consultar_custos(servico):
    """Custo atual por hora comparado com o baseline."""
    erro = _validar_servico(servico)
    if erro:
        return erro
    custo = ambiente["custos"][servico]
    multiplicador = round(custo["atual_usd_h"] / custo["baseline_usd_h"], 1)
    return {"servico": servico, **custo, "multiplicador": multiplicador}


def consultar_eventos_recentes():
    """Eventos recentes de deploy, autoscaling e alerta."""
    return {"eventos": ambiente["eventos"]}


def _tendencia(valor, base):
    """Compara o valor atual com a base normal."""
    if valor > base + MARGEM:
        return "crescente"
    if valor < base - MARGEM:
        return "decrescente"
    return "estavel"


def _taxa_por_hora(inicio, atual):
    """Quanto a metrica sobe por hora entre dois pontos."""
    intervalo = datetime.fromisoformat(atual["data_hora"]) - datetime.fromisoformat(inicio["data_hora"])
    horas = intervalo.total_seconds() / 3600
    return (atual["valor"] - inicio["valor"]) / horas if horas else 0


def analisar_serie_temporal(servico, metrica):
    """Resume a serie: base normal, inicio do crescimento, taxa e previsao de esgotamento."""
    erro = _validar_servico(servico)
    if erro:
        return erro
    dado = ambiente["metricas"][servico][metrica]
    if not isinstance(dado, dict):
        return {"servico": servico, "metrica": metrica, "aviso": "sem serie temporal"}

    serie = dado["serie"]
    atual = serie[-1]
    # 1. Base normal e 2. tendencia
    base = median(ponto["valor"] for ponto in serie[:PONTOS_BASE])
    resumo = {
        "servico": servico,
        "metrica": metrica,
        "tendencia": _tendencia(atual["valor"], base),
        "valor_atual": atual["valor"],
    }
    if resumo["tendencia"] != "crescente":
        return resumo

    # 3. Inicio do crescimento, 4. taxa e 5. quando esgota
    indice = next(i for i, ponto in enumerate(serie) if ponto["valor"] > base + MARGEM)
    taxa = _taxa_por_hora(serie[indice], atual)
    return {
        **resumo,
        "base_normal": base,
        "ultimo_ponto_normal": serie[indice - 1]["data_hora"] if indice else None,
        "inicio_crescimento": serie[indice]["data_hora"],
        "taxa_pct_por_hora": round(taxa, 2),
        "horas_ate_esgotar": round((100 - atual["valor"]) / taxa) if taxa > 0 else None,
    }


def solicitar_rollback(deploy_id, justificativa):
    """Abre um pedido de rollback. Nao executa; depende de aprovacao humana."""
    encontrado = None
    for servico, deploys in ambiente["deploys"].items():
        for deploy in deploys:
            if deploy["id"] == deploy_id:
                encontrado = {"servico": servico, **deploy}
                break
    if not encontrado:
        return {"status": "rejeitado", "motivo": "deploy inexistente"}
    return {
        "status": "AGUARDANDO_APROVACAO_HUMANA",
        "deploy": encontrado,
        "justificativa_registrada": justificativa,
        "executado": False,
    }


def enviar_relatorio_email(assunto, corpo):
    """Envia o relatorio por e-mail para o endereco fixo. Chamada pelo codigo, nao pelo modelo."""
    mensagem = EmailMessage()
    mensagem["Subject"] = assunto
    mensagem["From"] = EMAIL_RELATORIO
    mensagem["To"] = EMAIL_RELATORIO
    mensagem.set_content(corpo)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_RELATORIO, os.environ["GMAIL_SENHA_APP"])
        smtp.send_message(mensagem)
    return {"status": "enviado", "destinatario": EMAIL_RELATORIO}


def schema_servico(nome, descricao):
    """Schema de uma tool que recebe apenas o servico."""
    return {
        "name": nome,
        "description": descricao,
        "input_schema": {
            "type": "object",
            "properties": {
                "servico": {
                    "type": "string",
                    "enum": SERVICOS,
                    "description": "Nome do servico",
                }
            },
            "required": ["servico"],
            "additionalProperties": False,
        },
    }


TOOLS = [
    schema_servico("consultar_metricas", "Consulta CPU, memoria, latencia, erros e numero de instancias de um servico."),
    schema_servico("buscar_logs", "Busca as linhas recentes de log de um servico. Use para investigar sintomas e erros."),
    schema_servico("consultar_deploys", "Lista deploys recentes e mudancas conhecidas de um servico."),
    schema_servico("consultar_configuracao", "Consulta a configuracao operacional atual de um servico."),
    schema_servico("consultar_custos", "Compara o custo atual por hora de um servico com seu baseline."),
    {
        "name": "analisar_serie_temporal",
        "description": "Analisa a serie temporal de CPU ou memoria de um servico: base normal, ultimo ponto normal, inicio do crescimento, taxa por hora e horas ate esgotar.",
        "input_schema": {
            "type": "object",
            "properties": {
                "servico": {
                    "type": "string",
                    "enum": SERVICOS,
                    "description": "Nome do servico",
                },
                "metrica": {
                    "type": "string",
                    "enum": ["cpu_pct", "memoria_pct"],
                    "description": "Metrica a analisar",
                },
            },
            "required": ["servico", "metrica"],
            "additionalProperties": False,
        },
    },
    {
        "name": "consultar_eventos_recentes",
        "description": "Lista eventos cloud recentes em ordem temporal: deploys, autoscaling e alertas.",
        "input_schema": {"type": "object", "properties": {}, "required": [], "additionalProperties": False},
    },
    {
        "name": "solicitar_rollback",
        "description": "Solicita rollback de um deploy suspeito. Apenas abre pedido; exige aprovacao humana para executar.",
        "input_schema": {
            "type": "object",
            "properties": {
                "deploy_id": {"type": "string", "description": "ID exato de um deploy consultado"},
                "justificativa": {"type": "string", "description": "Evidencia objetiva que justifica o rollback"},
            },
            "required": ["deploy_id", "justificativa"],
            "additionalProperties": False,
        },
    },
]


# dispatcher
FUNCOES_PERMITIDAS = {
    "consultar_metricas": consultar_metricas,
    "buscar_logs": buscar_logs,
    "consultar_deploys": consultar_deploys,
    "consultar_configuracao": consultar_configuracao,
    "consultar_custos": consultar_custos,
    "consultar_eventos_recentes": consultar_eventos_recentes,
    "analisar_serie_temporal": analisar_serie_temporal,
    "solicitar_rollback": solicitar_rollback,
    "enviar_relatorio_email": enviar_relatorio_email,
}


def executar_ferramenta(nome, argumentos):
    """Executa uma tool permitida e devolve erro em vez de quebrar o loop."""
    if nome not in FUNCOES_PERMITIDAS:
        return {"erro": f"Ferramenta nao permitida: {nome}"}
    try:
        return FUNCOES_PERMITIDAS[nome](**argumentos)
    except Exception as exc:
        return {"erro": type(exc).__name__, "detalhe": str(exc)}
