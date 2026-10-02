W, H = 1400, 650
FONT = "Poppins, sans-serif"
NODE_WEIGHT = 600
GROUP_WEIGHT = 400
PILL_CHAR = 6.9

# Eixo de simetria vertical em x=700; fluxo principal em linha reta em y=170.
GROUPS = [
    dict(style='plain', x=280, y=50, w=840, h=250, label='Agente legista de incidentes · Python', label_color='#545B64'),
    dict(style='aws', x=280, y=380, w=400, h=230, label='AWS Cloud · us-east-1', label_right=True, label_color='#545B64'),
    dict(style='plain', x=720, y=380, w=400, h=230, label='Ambiente simulado', label_color='#545B64'),
]

NODES = [
    dict(icon='User', x=130, y=170, label=['SRE', 'INC-2026-0912', 'alerta de memória']),
    dict(icon='python', x=480, y=170, size=60, label=['agente.py', 'loop · máx. 8 rodadas · US$ 0,10']),
    dict(icon='python', x=920, y=170, size=60, label=['tools.py', 'dispatcher · 8 tools']),
    dict(icon='gmail', x=1270, y=170, label=['Gmail SMTP', 'relatório final ao SRE', 'rollback: aprovação humana']),
    dict(icon='AmazonBedrock', x=480, y=480, size=60, label=['Amazon Bedrock', 'Claude Sonnet 5 · Messages API'], chips=['claude']),
    dict(icon='python', x=920, y=480, size=60, label=['cenario.py', 'métricas · logs · deploys · custos']),
]

EDGES = [
    dict(points=[(164, 170), (446, 170)], label='incidente', label_at=(222, 170)),
    dict(points=[(514, 170), (886, 170)], label='tool_use · tool_result', label_at=(700, 170), both=True),
    dict(points=[(954, 170), (1236, 170)], label='SMTP SSL', label_at=(1178, 170)),
    dict(points=[(480, 244), (480, 446)], label='mensagens + tools', label_at=(480, 340), both=True),
    dict(points=[(920, 244), (920, 446)], label='consulta', label_at=(920, 340)),
]
