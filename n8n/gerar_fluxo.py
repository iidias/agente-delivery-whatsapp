"""Gera o fluxo do agente (WhatsApp via WAHA) para importar no n8n: fluxo-agente.json.

Textos e lógica ficam em arquivos do repositório, e o n8n recebe sempre a versão atual:
  - agente/prompt-sistema.md + agente/base-conhecimento.md  -> prompt do agente
  - n8n/codigo/preparar-mensagem.js                         -> filtros, horário, pausa, comandos
  - n8n/codigo/pos-processar.js                             -> [ATENDENTE], aviso e pausa

O JSON gerado não leva nenhuma chave nem número: as credenciais são criadas no n8n.

Uso (na raiz do projeto):
    python n8n/gerar_fluxo.py
"""

import json
import re
import uuid
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PROMPT = RAIZ / "agente" / "prompt-sistema.md"
BASE = RAIZ / "agente" / "base-conhecimento.md"
JS_PREPARAR = Path(__file__).resolve().parent / "codigo" / "preparar-mensagem.js"
JS_POS = Path(__file__).resolve().parent / "codigo" / "pos-processar.js"
SAIDA = Path(__file__).resolve().parent / "fluxo-agente.json"

ID_FLUXO = "agenteDelivery0001"  # id fixo: importar de novo atualiza em vez de duplicar
NOME_FLUXO = "Agente de atendimento (WhatsApp / WAHA)"
FUSO = "America/Sao_Paulo"      # fuso da loja (use o mesmo de preparar-mensagem.js e do docker-compose.yml)
MODELO = "models/gemini-2.5-flash"
JANELA_MEMORIA = 10             # quantas trocas de mensagem o agente lembra por cliente
WAHA = "http://waha:3000/api"   # nome do container na rede do docker compose
SESSAO = "default"

AGENTE = "Agente de atendimento"
PREPARAR = "Preparar mensagem"
POS = "Pós-processar"


def sem_comentarios(texto: str) -> str:
    """Remove os comentários de instrução (<!-- ... -->): são para quem configura, não para o agente."""
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.DOTALL)
    return re.sub(r"\n{3,}", "\n\n", texto).strip()


def montar_prompt() -> str:
    prompt = sem_comentarios(PROMPT.read_text(encoding="utf-8"))
    base = sem_comentarios(BASE.read_text(encoding="utf-8"))
    return prompt.replace("{{base_conhecimento}}", base)


def no(nome, tipo, versao, posicao, parametros, **extra):
    return {
        "parameters": parametros,
        "id": str(uuid.uuid4()),
        "name": nome,
        "type": tipo,
        "typeVersion": versao,
        "position": posicao,
        **extra,
    }


def waha(nome, rota, posicao, corpo_js, **extra):
    """Chamada POST ao WAHA com a credencial Header Auth (X-Api-Key)."""
    return no(
        nome,
        "n8n-nodes-base.httpRequest",
        4.2,
        posicao,
        {
            "method": "POST",
            "url": f"{WAHA}/{rota}",
            "authentication": "genericCredentialType",
            "genericAuthType": "httpHeaderAuth",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ JSON.stringify(" + corpo_js + ") }}",
            "options": {},
        },
        **extra,
    )


def montar_fluxo() -> dict:
    p = f"$('{POS}').first().json"
    nos = [
        no("Mensagem do WhatsApp", "n8n-nodes-base.webhook", 2, [0, 0],
           {"httpMethod": "POST", "path": "waha", "responseMode": "onReceived", "options": {}},
           webhookId=str(uuid.uuid4())),
        no(PREPARAR, "n8n-nodes-base.code", 2, [240, 0], {"jsCode": JS_PREPARAR.read_text(encoding="utf-8")}),
        no("Responder com IA?", "n8n-nodes-base.if", 2.2, [480, 0], {
            "conditions": {
                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                "conditions": [{
                    "id": str(uuid.uuid4()),
                    "leftValue": "={{ $json.acao }}",
                    "rightValue": "ia",
                    "operator": {"type": "string", "operation": "equals"},
                }],
                "combinator": "and",
            },
            "options": {},
        }),
        no(AGENTE, "@n8n/n8n-nodes-langchain.agent", 1.7, [740, -80], {
            "promptType": "define",
            "text": "={{ $json.texto }}",
            "options": {"systemMessage": montar_prompt()},
        }, retryOnFail=True, maxTries=3, waitBetweenTries=2000),
        no("Gemini", "@n8n/n8n-nodes-langchain.lmChatGoogleGemini", 1, [660, 160],
           {"modelName": MODELO, "options": {"temperature": 0.3}}),
        no("Memória da conversa", "@n8n/n8n-nodes-langchain.memoryBufferWindow", 1.3, [840, 160], {
            "sessionIdType": "customKey",
            "sessionKey": f"={{{{ $('{PREPARAR}').item.json.chatId }}}}",
            "contextWindowLength": JANELA_MEMORIA,
        }),
        no(POS, "n8n-nodes-base.code", 2, [1000, 0], {"jsCode": JS_POS.read_text(encoding="utf-8")}),
        waha("Marcar como lida", "sendSeen", [1240, 0],
             f"{{ session: '{SESSAO}', chatId: {p}.destino }}", onError="continueRegularOutput"),
        waha("Digitando", "startTyping", [1460, 0],
             f"{{ session: '{SESSAO}', chatId: {p}.destino }}", onError="continueRegularOutput"),
        no("Esperar", "n8n-nodes-base.wait", 1.1, [1680, 0],
           {"resume": "timeInterval", "amount": f"={{{{ {p}.espera }}}}", "unit": "seconds"},
           webhookId=str(uuid.uuid4())),
        waha("Enviar resposta", "sendText", [1900, 0],
             f"{{ session: '{SESSAO}', chatId: {p}.destino, text: {p}.resposta }}",
             retryOnFail=True, maxTries=3, waitBetweenTries=2000),
        no("Passou para atendente?", "n8n-nodes-base.if", 2.2, [2140, 0], {
            "conditions": {
                "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                "conditions": [{
                    "id": str(uuid.uuid4()),
                    "leftValue": f"={{{{ {p}.handoff }}}}",
                    "rightValue": "",
                    "operator": {"type": "boolean", "operation": "true", "singleValue": True},
                }],
                "combinator": "and",
            },
            "options": {},
        }),
        waha("Avisar atendente", "sendText", [2380, -60],
             f"{{ session: '{SESSAO}', chatId: {p}.atendente.replace(/\\D/g, '') + '@c.us', text: {p}.aviso }}"),
    ]

    def c(destino, tipo="main"):
        return [[{"node": destino, "type": tipo, "index": 0}]]

    conexoes = {
        "Mensagem do WhatsApp": {"main": c(PREPARAR)},
        PREPARAR: {"main": c("Responder com IA?")},
        "Responder com IA?": {"main": [
            [{"node": AGENTE, "type": "main", "index": 0}],   # verdadeiro
            [{"node": POS, "type": "main", "index": 0}],               # falso: resposta pronta/comando
        ]},
        AGENTE: {"main": c(POS)},
        "Gemini": {"ai_languageModel": c(AGENTE, "ai_languageModel")},
        "Memória da conversa": {"ai_memory": c(AGENTE, "ai_memory")},
        POS: {"main": c("Marcar como lida")},
        "Marcar como lida": {"main": c("Digitando")},
        "Digitando": {"main": c("Esperar")},
        "Esperar": {"main": c("Enviar resposta")},
        "Enviar resposta": {"main": c("Passou para atendente?")},
        "Passou para atendente?": {"main": [[{"node": "Avisar atendente", "type": "main", "index": 0}], []]},
    }
    return {
        "id": ID_FLUXO,
        "name": NOME_FLUXO,
        "nodes": nos,
        "connections": conexoes,
        "settings": {"executionOrder": "v1", "timezone": FUSO},
        "pinData": {},
        "active": False,
    }


if __name__ == "__main__":
    pendentes = montar_prompt().count("[PREENCHER")
    if pendentes:
        print(f"ATENÇÃO: ainda há {pendentes} campo(s) [PREENCHER] em agente/. "
              "O agente trata esses campos como informação que ele não tem.")
    SAIDA.write_text(json.dumps(montar_fluxo(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Fluxo salvo em {SAIDA}")
