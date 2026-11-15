# n8n + WAHA: como colocar o agente para rodar

## Como a mensagem anda

```
Cliente (WhatsApp)
  → WAHA (container que mantém o WhatsApp conectado, estilo WhatsApp Web)
  → webhook do n8n
  → [Preparar mensagem]  filtros, loja aberta?, conversa pausada?, comandos, localização/áudio
        ├─ texto normal → [Agente de atendimento] (Gemini + memória por cliente) ┐
        └─ resposta pronta ───────────────────────────────────────────────┤
  → [Pós-processar]  tira o [ATENDENTE], pausa a conversa, monta o aviso
  → lida → "digitando..." → espera 2–6 s → envia a resposta
  → se passou para atendente: avisa o número do atendente
```

## Passo a passo

1. **Pré-requisito:** Docker Desktop rodando.
2. **Configuração:** em `n8n/`, copie `.env.example` para `.env` e troque as senhas e a chave (`WAHA_API_KEY` e `WHATSAPP_API_KEY` com o mesmo valor).
3. **Subir tudo** (dentro de `n8n/`):
   ```powershell
   docker compose up -d
   docker compose logs waha --tail 30
   ```
4. **Conectar o WhatsApp:** abra http://localhost:3000/dashboard, entre com o login do `.env` e informe a chave. Inicie a sessão `default`, escaneie o QR (WhatsApp → Aparelhos conectados). **Comece com um chip reserva, não o número principal da loja** (veja "Risco do WAHA" abaixo).
5. **Preencher o agente e gerar o fluxo:** preencha `agente/prompt-sistema.md` e `agente/base-conhecimento.md` (procure por `[PREENCHER]`) e rode `python n8n/gerar_fluxo.py` na raiz do projeto. O script avisa se ainda sobrou algum campo.
6. **n8n:** abra http://localhost:5679, crie a conta de dono e importe `n8n/fluxo-agente.json` (menu do workflow → *Import from File*). Sempre que mudar o prompt ou a base, gere de novo com `python n8n/gerar_fluxo.py` e importe de novo: o id é fixo e atualiza o mesmo workflow.
7. **Credenciais** (Credentials → Create):
   - **Google Gemini (PaLM) API:** chave do [Google AI Studio](https://aistudio.google.com/apikey). Escolha no nó *Gemini*.
   - **Header Auth:** Name `X-Api-Key`, Value = a `WAHA_API_KEY` do `.env`. Escolha nos nós *Marcar como lida*, *Digitando*, *Enviar resposta* e *Avisar atendente*.
8. **Configurar o nó `Preparar mensagem`** (abra e edite o topo do código; o mesmo conteúdo está em `n8n/codigo/preparar-mensagem.js`):
   - `NUMERO_ATENDENTE`: o número que recebe os avisos e pode usar comandos (DDI+DDD+número, só dígitos).
   - `FUSO`: o fuso horário da loja.
   - `HORARIOS` e `DIAS_FECHADOS`: os horários reais de funcionamento (fora deles o bot fica em silêncio). Mantenha iguais aos da seção 2 de `agente/base-conhecimento.md`.
   - `MSG_LOCALIZACAO` e `MSG_MIDIA`: as respostas fixas para localização e áudio/foto.
   - Esse número fica só dentro do n8n: **não faça commit do JSON exportado do n8n com ele**.
   - Atenção: ao importar o JSON de novo, o código do nó volta a ser o do arquivo `.js`. Deixe `FUSO`, `HORARIOS` e as mensagens já ajustados no arquivo e refaça só o `NUMERO_ATENDENTE` no n8n depois de cada importação.
9. **Publicar o workflow** (*Publish/Activate*). O WAHA chama `http://n8n:5678/webhook/waha`, que é a URL de produção: só funciona com o workflow publicado. A pausa por conversa e o `/fechar` ficam guardados no workflow e **só persistem com ele publicado**, não em execuções manuais de teste.
10. **Testar** de outro celular (dentro do horário, ou use `/abrir` do número do atendente).

## Comandos do atendente

Mande para o número da loja, do `NUMERO_ATENDENTE`:

| Comando | O que faz |
|---|---|
| `/status` | mostra se o bot está ligado e quantas conversas estão com atendente |
| `/fechar` | desliga o bot (loja fechada de última hora, feriado) |
| `/abrir` | liga o bot mesmo fora do horário |
| `/auto` | volta a seguir os horários |
| `/liberar` ou `/liberar 5579...` | o bot volta a responder aquele cliente (sem número: libera o seu, útil nos testes) |

## Atendimento humano

Quando a IA passa para uma pessoa, o bot **fica 12 horas em silêncio naquela conversa** e você recebe um aviso. Responda pelo próprio WhatsApp do celular conectado.

## Risco do WAHA (leia antes de ligar no número da loja)

- O WAHA usa o WhatsApp Web de forma **não oficial**. O WhatsApp pode restringir ou banir o número. Se o número da loja for o canal principal de venda, isso dói.
- Reduz o risco: só responder quem escreve primeiro (já é assim), nunca mandar mensagem em massa, manter a pausa de "digitando", usar uma sessão só e manter o celular conectado.
- Caminho seguro: rodar 1 semana num chip reserva, ver como se comporta e só então decidir. A alternativa oficial é a WhatsApp Cloud API da Meta (mais burocracia e cobrança por conversa, sem risco de banimento por usar API não oficial).
- A versão gratuita (Core) do WAHA tem **uma sessão** e **só envia texto** (sem imagem/áudio/arquivo). Para este fluxo basta.

## Melhorias para depois

- Agrupar várias mensagens seguidas do cliente numa só resposta.
- Registrar as conversas numa planilha (fonte de perguntas reais para o `perguntas-teste.csv`).
- Avisar o atendente quando o WAHA desconectar (evento `session.status`) e ter um *Error Workflow* no n8n.
- Painel de atendimento humano com o Chatwoot.
- Hospedar num servidor barato (VPS) para não depender de o computador ficar ligado.
