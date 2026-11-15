// ============ CONFIGURAÇÃO (edite aqui, direto no nó do n8n) ============
const NUMERO_ATENDENTE = '55DDXXXXXXXXX'; // TROQUE: quem recebe os avisos e pode usar comandos (só dígitos: DDI + DDD + número)
const FUSO = 'America/Sao_Paulo';         // fuso horário da loja (lista: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
const PAUSA_HORAS = 12;                   // depois de passar para uma pessoa, o bot fica quieto nessa conversa
const HORARIOS = {                        // TROQUE: 1 = segunda ... 7 = domingo; null = fechado. Exemplo abaixo.
  1: ['11:00', '22:00'],
  2: ['11:00', '22:00'],
  3: ['11:00', '22:00'],
  4: ['11:00', '22:00'],
  5: ['11:00', '22:00'],
  6: ['11:00', '22:00'],
  7: null,
};
const DIAS_FECHADOS = [];                 // feriados e folgas, formato 'AAAA-MM-DD'

// Mensagens fixas (não passam pela IA). Ajuste o tom para combinar com a sua loja.
const MSG_LOCALIZACAO = 'Recebi sua localização! Em instantes alguém te responde para ajudar com o endereço. 😊';
const MSG_MIDIA = 'Recebi sua mensagem! Por aqui eu só consigo ler texto. Pode escrever o que precisa? Em instantes alguém também te responde. 😊';
// =====================================================================

const sd = $getWorkflowStaticData('global');
sd.pausas = sd.pausas || {};

// 1) Só interessa mensagem recebida de contato individual
const body = $json.body || $json;
const p = body.payload;
if (body.event !== 'message' || !p || p.fromMe) return [];
if (p.type === 'sticker') return [];

let chatId = p.from || '';
if (chatId.endsWith('@lid') && p._data && p._data.key && p._data.key.remoteJidAlt) {
  chatId = p._data.key.remoteJidAlt;
}
if (!chatId.endsWith('@c.us') && !chatId.endsWith('@lid')) return []; // grupos, status e canais

const numero = chatId.split('@')[0];
const ult8 = (s) => String(s).replace(/\D/g, '').slice(-8); // compara só o final (evita problema do 9º dígito)
const ehAtendente = ult8(NUMERO_ATENDENTE).length === 8 && ult8(numero) === ult8(NUMERO_ATENDENTE);
const texto = String(p.body || '').trim();

const base = { chatId, numero, texto, atendente: NUMERO_ATENDENTE, pausaHoras: PAUSA_HORAS };
const pronto = (resposta, extra = {}) => [{ json: { ...base, acao: 'pronto', resposta, ...extra } }];

// 2) A loja está aberta agora?
const agora = $now.setZone(FUSO);
const hoje = agora.toFormat('yyyy-LL-dd');
const minutos = (s) => { const [h, m] = s.split(':').map(Number); return h * 60 + m; };
function lojaAberta() {
  if (sd.override === 'aberto') return true;
  if (sd.override === 'fechado') return false;
  if (DIAS_FECHADOS.includes(hoje)) return false;
  const h = HORARIOS[agora.weekday];
  if (!h) return false;
  const m = agora.hour * 60 + agora.minute;
  return m >= minutos(h[0]) && m < minutos(h[1]);
}

// 3) Comandos do atendente (mensagens que começam com /)
if (ehAtendente && texto.startsWith('/')) {
  const [cmd, arg] = texto.toLowerCase().split(/\s+/);
  if (cmd === '/fechar') { sd.override = 'fechado'; return pronto('🔴 Bot desligado: não vai responder ninguém. Para voltar ao horário normal: /auto'); }
  if (cmd === '/abrir')  { sd.override = 'aberto';  return pronto('🟢 Bot ligado, mesmo fora do horário. Para voltar ao horário normal: /auto'); }
  if (cmd === '/auto')   { sd.override = null;      return pronto('⚙️ Bot seguindo o horário de funcionamento.'); }
  if (cmd === '/status') {
    const modo = sd.override ? 'manual (' + sd.override + ')' : 'automático';
    const pausas = Object.values(sd.pausas).filter((t) => t > Date.now()).length;
    return pronto('Bot: ' + (lojaAberta() ? 'ligado' : 'desligado') + '\nModo: ' + modo + '\nConversas com atendente: ' + pausas);
  }
  if (cmd === '/liberar') {
    const alvo = arg ? ult8(arg) : ult8(numero);
    let n = 0;
    for (const k of Object.keys(sd.pausas)) {
      if (ult8(k.split('@')[0]) === alvo) { delete sd.pausas[k]; n++; }
    }
    return pronto(n ? '✅ Conversa liberada: o bot volta a responder esse cliente.' : 'Não achei conversa pausada para esse número.');
  }
  return pronto('Comandos: /status, /fechar, /abrir, /auto, /liberar [número]');
}

// 4) Fechada: não responde nada
if (!lojaAberta()) return [];

// 5) Conversa que já foi para uma pessoa: o bot fica quieto
const ate = sd.pausas[chatId];
if (ate && ate > Date.now()) return [];
if (ate) delete sd.pausas[chatId];

// 6) Mensagens que não são texto
if (p.location || p.type === 'location') {
  const lat = p.location && p.location.latitude;
  const lon = p.location && p.location.longitude;
  const mapa = lat && lon ? ' https://maps.google.com/?q=' + lat + ',' + lon : '';
  return pronto(MSG_LOCALIZACAO,
    { handoff: true, motivo: 'Enviou a localização.' + mapa });
}
if (!texto) {
  return pronto(MSG_MIDIA,
    { handoff: true, motivo: 'Enviou áudio, imagem ou outro tipo de arquivo.' });
}

// 7) Texto normal: vai para o agente de IA
return [{ json: { ...base, acao: 'ia' } }];
