// Junta os dois caminhos (resposta da IA ou resposta pronta) e decide o que enviar.
const ctx = $('Preparar mensagem').first().json;
const sd = $getWorkflowStaticData('global');
sd.pausas = sd.pausas || {};

let resposta;
let handoff = false;
let motivo = ctx.motivo || '';

if (ctx.acao === 'ia') {
  let saida = String($json.output || '').trim();
  handoff = saida.includes('[ATENDENTE]');
  saida = saida.replace(/\[ATENDENTE\]/g, '').trim();
  if (!saida) { saida = 'Em instantes alguém te responde. 😊'; handoff = true; }
  resposta = saida;
  motivo = ctx.texto;
} else {
  resposta = ctx.resposta;
  handoff = !!ctx.handoff;
}

if (handoff) sd.pausas[ctx.chatId] = Date.now() + ctx.pausaHoras * 3600 * 1000;

const aviso = handoff
  ? '🔔 Cliente precisa de atendimento\nNúmero: ' + ctx.numero +
    '\nÚltima mensagem: ' + motivo +
    '\nO bot fica em silêncio nessa conversa por ' + ctx.pausaHoras + 'h. Para liberar antes: /liberar ' + ctx.numero
  : '';

// pausa de "digitando", proporcional ao tamanho da resposta (2 a 6 segundos)
const espera = Math.min(6, Math.max(2, Math.round(resposta.length / 20)));

return [{ json: { destino: ctx.chatId, resposta, handoff, aviso, atendente: ctx.atendente, espera } }];
