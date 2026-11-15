<!--
COMO PREENCHER ESTE ARQUIVO
Aqui ficam os DADOS da sua loja. O agente só responde o que estiver escrito aqui (ou no prompt-sistema.md).
O que não estiver aqui, ou continuar como [PREENCHER], vai para um atendente humano.

Regras simples:
  - Troque cada [PREENCHER: ...] pelo dado real. Se não se aplica, escreva "Não se aplica" ou apague a linha.
  - Seja específico e literal: o agente repete o que lê. "Taxa R$ 5,00" funciona; "taxa baixa" não.
  - Quanto mais completo, menos conversas vão para o atendente. Mas só escreva o que é verdade e o que você consegue manter atualizado.
  - Preço e item que mudam toda hora (promoção do dia, item esgotado) são melhores no link de pedidos do que aqui.
  - Os horários de funcionamento que LIGAM e DESLIGAM o bot ficam em n8n/codigo/preparar-mensagem.js (HORARIOS).
    A seção 2 abaixo é só para o agente poder informar o horário ao cliente: mantenha as duas iguais.
  - Fora do horário o bot fica em silêncio (não responde nada).

Comentários como este não são enviados ao agente.
-->

# Base de conhecimento — [PREENCHER: nome da loja]

## 1. Sobre a loja
- Nome: [PREENCHER: nome da loja]
- Tipo de negócio e especialidade: [PREENCHER: ex.: pizzaria artesanal, hamburgueria, cafeteria e confeitaria, marmitas caseiras]
- Descrição em uma frase: [PREENCHER: ex.: "Pizzas assadas no forno a lenha, com massa de fermentação natural."]
- Endereço da loja: [PREENCHER: rua, número, bairro, cidade/UF]
- Instagram / site / outros contatos que o cliente pode receber: [PREENCHER ou "Não se aplica"]

## 2. Horário de funcionamento
<!-- Mantenha igual ao HORARIOS do preparar-mensagem.js. Informe feriados e folgas fixas. -->
- Segunda: [PREENCHER: ex.: 11h às 22h ou "fechado"]
- Terça: [PREENCHER]
- Quarta: [PREENCHER]
- Quinta: [PREENCHER]
- Sexta: [PREENCHER]
- Sábado: [PREENCHER]
- Domingo: [PREENCHER]
- Feriados e datas especiais: [PREENCHER: ex.: "Abrimos nos feriados, exceto Natal e Ano Novo" ou "Fechado nos feriados"]
- Último pedido aceito até: [PREENCHER: ex.: 30 minutos antes de fechar, ou "Não se aplica"]

## 3. Cardápio e preços
- Link do cardápio / pedidos online: [PREENCHER: link ou "Não temos link"]
- Categorias que a loja oferece (visão geral, sem preços): [PREENCHER: ex.: pizzas, esfirras, bebidas, sobremesas]

<!--
Se você usa o MODO A (link) no prompt, a lista abaixo é opcional: o agente manda o link e não lista preços.
Se você usa o MODO B (sem link), preencha o cardápio COMPLETO abaixo; o agente só informa o que estiver aqui.
Formato sugerido, uma linha por item: Nome — descrição curta — preço (ou preço por tamanho).
Remova os exemplos e as categorias que não existem.
-->
### Itens e preços
- [PREENCHER: Categoria 1 — ex.: Pizzas]
  - [PREENCHER: item — descrição — preço por tamanho, ex.: Margherita — molho, mussarela e manjericão — P R$ 30 / M R$ 40 / G R$ 50]
- [PREENCHER: Categoria 2 — ex.: Bebidas]
  - [PREENCHER: item — tamanho — preço]

### Tamanhos, adicionais e combos
- Tamanhos e como são medidos: [PREENCHER ou "Não se aplica"]
- Adicionais e preços: [PREENCHER ou "Não se aplica"]
- Combos e o que incluem: [PREENCHER ou "Não se aplica"]

### Disponibilidade
- Itens que variam por dia ou acabam durante o dia: [PREENCHER: ex.: "Disponibilidade confirmada por um atendente" ou "Veja no link"]

## 4. Como fazer o pedido
- Canal principal de pedido: [PREENCHER: ex.: "pelo link de pedidos" ou "pelo WhatsApp, com um atendente"]
- Passo a passo para o cliente: [PREENCHER: ex.: escolher os produtos, informar o endereço, escolher a forma de pagamento e finalizar]
- Pedido mínimo: [PREENCHER: valor ou "Não há"]
- Pedidos para outro dia ou horário (agendados): [PREENCHER: ex.: "Aceitamos com 2 horas de antecedência" ou "Não aceitamos"]

## 5. Entrega e retirada
- Cidades e bairros atendidos: [PREENCHER: lista clara]
- Lugares que NÃO atendemos: [PREENCHER: ex.: outras cidades e povoados, ou "Não se aplica"]
- Taxa de entrega: [PREENCHER: valor único, tabela por bairro ou "Grátis"]
- Entrega grátis acima de: [PREENCHER: valor ou "Não se aplica"]
- Tempo médio de entrega: [PREENCHER: ex.: 40 a 60 minutos]
- Como é feita a entrega: [PREENCHER: ex.: entregador próprio, aplicativo de entregas, moto/bike]
- Retirada no balcão: [PREENCHER: "Sim, no endereço da loja, sem taxa" ou "Não temos retirada"]

## 6. Formas de pagamento
- Formas aceitas: [PREENCHER: ex.: Pix, dinheiro, cartão de crédito e débito, vale-refeição (quais)]
- Quando o cliente paga: [PREENCHER: ex.: na entrega, online pelo link ou antecipado via Pix]
- Troco: [PREENCHER: ex.: "Levamos troco; o cliente informa para quanto" ou "Não se aplica"]
- Pix (chave ou como receber): [PREENCHER ou "Informado pelo atendente"]
<!-- Em repositório público nunca escreva chave Pix, CPF ou CNPJ reais. Prefira "Informado pelo atendente". -->

## 7. Alergênicos e restrições alimentares
<!-- Seja conservador: só escreva o que você tem certeza. O prompt manda o agente nunca garantir nada que não esteja aqui. -->
- Ingredientes que aparecem em vários produtos (leite, glúten, ovos, amendoim, castanhas, soja, frutos do mar): [PREENCHER ou "Informado pelo atendente"]
- Opções vegetarianas / veganas / sem lactose / sem glúten: [PREENCHER ou "Não temos opções específicas"]
- Risco de contaminação cruzada: [PREENCHER: ex.: "Tudo é produzido na mesma cozinha"]

## 8. Promoções, cupons e fidelidade
- Promoções fixas (ex.: "terça em dobro"): [PREENCHER ou "Não temos"]
- Cupom de desconto / primeira compra: [PREENCHER ou "Não temos"]
- Programa de fidelidade: [PREENCHER ou "Não temos"]

## 9. Encomendas e pedidos especiais
<!-- O agente SEMPRE passa esses casos para uma pessoa. Aqui você só descreve o que a loja faz, para ele saber o que responder antes. -->
- A loja faz encomendas (bolos, festas, kits, grandes quantidades)? [PREENCHER: sim/não e para quê]
- Antecedência mínima: [PREENCHER ou "Informada pelo atendente"]

## 10. Problemas com o pedido
- Atraso: [PREENCHER: ex.: "O atendente verifica a posição do pedido"]
- Item errado ou faltando: [PREENCHER: política da loja]
- Cancelamento: [PREENCHER: ex.: "Só antes de o pedido entrar em preparo"]
- Troca ou reembolso: [PREENCHER ou "Avaliado pelo atendente caso a caso"]

## 11. Perguntas frequentes extras
<!-- Coloque aqui perguntas reais que seus clientes fazem e que não cabem nas seções acima. Apague os exemplos. -->
- Pergunta: [PREENCHER: ex.: "Vocês têm estacionamento?"] — Resposta: [PREENCHER]
- Pergunta: [PREENCHER] — Resposta: [PREENCHER]

## 12. Sempre passar para um atendente
<!-- Além do que já está no prompt (reclamação, encomenda, pedir uma pessoa...), liste assuntos específicos da sua loja. -->
- [PREENCHER: ex.: pedidos para empresas, orçamento para eventos, dúvidas sobre nota fiscal]
