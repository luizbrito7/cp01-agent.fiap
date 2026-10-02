from copy import deepcopy

CENARIO_ORIGINAL = {
    "metricas": {
        "api-gateway": {
            "cpu_pct": 38, "memoria_pct": 61, "latencia_p95_ms": 6200,
            "taxa_erro_pct": 18.4, "instancias": 3
        },
        "recommendation-api": {
            "cpu_pct": 98, "memoria_pct": 84, "latencia_p95_ms": 5870,
            "taxa_erro_pct": 31.7, "instancias": 48
        },
        "catalog-api": {
            "cpu_pct": 42, "memoria_pct": 55, "latencia_p95_ms": 93,
            "taxa_erro_pct": 0.2, "instancias": 4
        },
        "checkout-api": {
            "cpu_pct": {
                "atual": 47,
                "serie": [
                    {"data_hora": "2026-09-05 08:00", "valor": 45},
                    {"data_hora": "2026-09-05 20:00", "valor": 46},
                    {"data_hora": "2026-09-06 08:00", "valor": 45},
                    {"data_hora": "2026-09-06 20:00", "valor": 46},
                    {"data_hora": "2026-09-07 08:00", "valor": 47},
                    {"data_hora": "2026-09-07 20:00", "valor": 46},
                    {"data_hora": "2026-09-08 08:00", "valor": 45},
                    {"data_hora": "2026-09-08 20:00", "valor": 46},
                    {"data_hora": "2026-09-09 08:00", "valor": 47},
                    {"data_hora": "2026-09-09 20:00", "valor": 46},
                    {"data_hora": "2026-09-10 08:00", "valor": 45},
                    {"data_hora": "2026-09-10 20:00", "valor": 46},
                    {"data_hora": "2026-09-11 08:00", "valor": 47},
                    {"data_hora": "2026-09-11 14:00", "valor": 47},
                ],
            },
            "memoria_pct": {
                "atual": 72,
                "serie": [
                    # antes do dep-398: memoria estavel
                    {"data_hora": "2026-09-05 08:00", "valor": 40},
                    {"data_hora": "2026-09-05 20:00", "valor": 40},
                    {"data_hora": "2026-09-06 08:00", "valor": 40},
                    # depois do dep-398: memory leak
                    {"data_hora": "2026-09-06 20:00", "valor": 43},
                    {"data_hora": "2026-09-07 08:00", "valor": 46},
                    {"data_hora": "2026-09-07 20:00", "valor": 49},
                    {"data_hora": "2026-09-08 08:00", "valor": 52},
                    {"data_hora": "2026-09-08 20:00", "valor": 55},
                    {"data_hora": "2026-09-09 08:00", "valor": 58},
                    {"data_hora": "2026-09-09 20:00", "valor": 61},
                    {"data_hora": "2026-09-10 08:00", "valor": 64},
                    {"data_hora": "2026-09-10 20:00", "valor": 67},
                    {"data_hora": "2026-09-11 08:00", "valor": 70},
                    {"data_hora": "2026-09-11 14:00", "valor": 72},
                ],
            },
            "latencia_p95_ms": 310, "taxa_erro_pct": 0.6, "instancias": 5,
        },
    },
    "logs": {
        "api-gateway": [
            "14:03:11 WARN upstream recommendation-api timeout after 5000ms",
            "14:03:14 WARN upstream recommendation-api timeout after 5000ms",
            "14:03:18 ERROR circuit breaker recommendation-api OPEN",
        ],
        "recommendation-api": [
            "14:02:57 WARN catalog response missing field related_items",
            "14:02:57 INFO invoking fallback target=recommendation-api depth=1",
            "14:02:58 INFO invoking fallback target=recommendation-api depth=8",
            "14:02:59 ERROR maximum fallback depth reached depth=25",
            "14:03:00 WARN request queue saturation=96%",
        ],
        "catalog-api": [
            "14:02:55 INFO GET /items/842 200 71ms",
            "14:03:01 INFO GET /items/163 200 66ms",
        ],
        "checkout-api": [
            "14:03:02 INFO POST /checkout 200 288ms",
            "14:03:07 INFO POST /checkout 200 302ms",
        ],
    },
    "deploys": {
        "api-gateway": [{"id": "dep-410", "versao": "5.8.1", "hora": "ontem 16:20", "status": "concluido"}],
        "recommendation-api": [
            {
                "id": "dep-442", "versao": "2.4.0", "hora": "13:58", "status": "concluido",
                "mudancas": [
                    "novo fallback para resposta incompleta do catalogo",
                    "FALLBACK_SERVICE: catalog-api -> recommendation-api",
                ],
            },
            {"id": "dep-431", "versao": "2.3.7", "hora": "ontem 11:40", "status": "concluido"},
        ],
        "catalog-api": [{"id": "dep-405", "versao": "3.1.2", "hora": "3 dias atras", "status": "concluido"}],
        "checkout-api": [{"id": "dep-398", "versao": "7.2.0", "hora": "5 dias atras", "status": "concluido"}],
    },
    "configuracoes": {
        "api-gateway": {"timeout_ms": 5000, "retries": 1},
        "recommendation-api": {
            "fallback_service": "recommendation-api",
            "fallback_max_depth": 25,
            "autoscaling_min": 2,
            "autoscaling_max": 50,
            "autoscaling_cpu_target_pct": 60,
        },
        "catalog-api": {"cache_ttl_s": 300, "replicas": 4},
        "checkout-api": {"replicas": 5, "timeout_ms": 1500},
    },
    "custos": {
        "api-gateway": {"baseline_usd_h": 0.22, "atual_usd_h": 0.24},
        "recommendation-api": {"baseline_usd_h": 0.31, "atual_usd_h": 7.44},
        "catalog-api": {"baseline_usd_h": 0.38, "atual_usd_h": 0.40},
        "checkout-api": {"baseline_usd_h": 0.51, "atual_usd_h": 0.52},
    },
    "eventos": [
        {"hora": "13:58", "tipo": "deploy", "servico": "recommendation-api", "id": "dep-442"},
        {"hora": "14:01", "tipo": "autoscaling", "servico": "recommendation-api", "detalhe": "2 -> 18 instancias"},
        {"hora": "14:03", "tipo": "autoscaling", "servico": "recommendation-api", "detalhe": "18 -> 48 instancias"},
        {"hora": "14:03", "tipo": "alerta", "servico": "api-gateway", "detalhe": "latencia p95 acima de 5s"},
    ],
}

ambiente = deepcopy(CENARIO_ORIGINAL)
