# Avaliação

Como medir se o agente responde certo, antes de ligar no número real da loja.

- `perguntas-teste.csv`: perguntas de teste com a resposta esperada, a categoria, o `modo` de pedido a que se aplica e se a conversa deve ir para um atendente (`deve_ir_para_atendente`).
- Script de avaliação (a fazer): manda cada pergunta para o agente no n8n, guarda a resposta e compara com o esperado.
- Resultados (a fazer): uma tabela por rodada, com a data, a versão do prompt e a taxa de acerto.

## Como adaptar para a sua loja

1. Troque o que está entre `[colchetes]` por itens reais do seu cardápio, bairros e regras.
2. Apague as linhas do modo que você não usa (`A` = link de pedidos, `B` = pedido reunido por aqui).
3. Nas linhas `depende`, o resultado correto muda conforme você preencheu ou não aquele dado na `base-conhecimento.md`: se está preenchido, o agente responde; se está `[PREENCHER]` ou vazio, deve chamar um atendente.
4. Acrescente perguntas reais dos seus clientes. Elas são a melhor fonte de testes.
5. Algumas linhas (categoria `fluxo`) testam o n8n, não a IA, e algumas dependem de a loja estar aberta ou fechada no momento do teste.
