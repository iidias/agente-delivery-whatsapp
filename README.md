# Agente de atendimento para delivery no WhatsApp

Template de atendente virtual para **pequenos negócios com delivery** (pizzaria, hamburgueria, cafeteria, açaí, marmitaria...). Ele atende o WhatsApp da loja com tom profissional, tira dúvidas só com o que você escreveu, manda o cliente para o link de pedidos e **passa para uma pessoa** quando não souber ou quando o assunto pedir.

Stack: [n8n](https://n8n.io) + [WAHA](https://waha.devlike.pro) (integração não oficial com WhatsApp Web) + Google Gemini, tudo rodando em Docker.

> **Atenção:** antes de usar, leia a seção [Risco do WAHA](n8n/README.md#risco-do-waha-leia-antes-de-ligar-no-numero-da-loja). A integração não oficial pode oferecer risco de restrição ao número.

## Meu caso de uso

A ideia deste projeto surgiu de uma situação que vivencio no meu trabalho como atendente de uma cafeteria. Em alguns períodos do dia, o movimento aumenta bastante e o volume de mensagens recebidas pelo WhatsApp acaba ultrapassando nossa capacidade de atendimento. Mesmo quando a equipe está ocupada atendendo os clientes presencialmente, as pessoas continuam entrando em contato pelo WhatsApp e podem acabar esperando mais do que gostariam por uma resposta.

Comecei a pensar em como a inteligência artificial poderia ajudar nesse processo. Minha proposta foi desenvolver um agente de atendimento capaz de responder às dúvidas mais comuns, orientar os clientes na utilização do nosso sistema de delivery e ajudá-los a encontrar o caminho para realizar seus próprios pedidos. Assim, enquanto o cliente recebe orientações rápidas e educadas, a equipe ganha tempo para cuidar dos atendimentos que realmente precisam de intervenção humana.

O objetivo não é substituir os atendentes, mas funcionar como um primeiro apoio no atendimento: resolver dúvidas recorrentes, direcionar o cliente e reconhecer quando uma situação precisa ser encaminhada para uma pessoa. Dessa forma, buscamos reduzir o tempo de espera e tornar a experiência de atendimento mais ágil, sem perder a cordialidade que faz parte de um bom serviço.

Depois de pensar nessa aplicação para a cafeteria onde trabalho, decidi organizar o projeto para que outros atendentes e pequenos negócios que trabalham com delivery também possam aproveitá-lo. Por isso, este repositório foi desenvolvido como um **modelo reutilizável**: a estrutura técnica e o fluxo principal já estão organizados, e cada negócio pode adaptá-los preenchendo as informações da própria operação, como cardápio, horários, formas de pagamento, regiões atendidas e link de pedidos.

A intenção é facilitar o acesso a uma aplicação prática de IA para pequenos negócios, sem exigir que cada pessoa precise desenvolver toda a automação do zero.


## Como funciona

```
Cliente (WhatsApp) → WAHA → n8n → [filtros: loja aberta? conversa pausada? comandos?]
                                   ├─ texto → agente de IA (prompt + base de conhecimento)
                                   └─ localização / áudio → resposta fixa
                    → envia a resposta → se precisou de gente: avisa o atendente e pausa o bot na conversa
```

## O que tem no repositório

| Pasta / arquivo | Para que serve | Você precisa editar? |
|---|---|---|
| `agente/prompt-sistema.md` | Como o atendente conversa (tom, regras, quando chamar uma pessoa) | Sim: personalize os campos `[PREENCHER]` e escolha o modo de pedido |
| `agente/base-conhecimento.md` | Os dados da sua loja (cardápio, horários, entrega, pagamento...) | **Sim: é o principal** |
| `n8n/codigo/preparar-mensagem.js` | Horário de funcionamento, comandos do atendente, mensagens fixas | Sim: número, fuso e horários |
| `n8n/codigo/pos-processar.js` | Tira a marcação `[ATENDENTE]`, pausa a conversa e monta o aviso | Normalmente não |
| `n8n/gerar_fluxo.py` | Junta tudo e gera `n8n/fluxo-agente.json` para importar | Não |
| `n8n/docker-compose.yml` e `.env.example` | WAHA + n8n | Só senhas e fuso |
| `avaliacao/` | Perguntas de teste para conferir as respostas | Adapte ao seu cardápio |

## O que um delivery pequeno precisa informar

É o roteiro da `base-conhecimento.md`. Se uma seção ficar vazia, o agente passa a pergunta para uma pessoa em vez de inventar.

| # | Assunto | O que escrever | Perguntas de cliente que isso responde |
|---|---|---|---|
| 1 | Sobre a loja | Nome, especialidade, endereço, redes sociais | "Onde fica?", "Vocês têm Instagram?" |
| 2 | Horário | Dias e horários, feriados, último pedido | "Estão abertos?", "Até que horas?" |
| 3 | Cardápio e preços | Link de pedidos **ou** lista completa; tamanhos, adicionais, combos | "O que tem?", "Quanto custa?" |
| 4 | Como pedir | Canal, passo a passo, pedido mínimo, agendamento | "Como faço o pedido?" |
| 5 | Entrega e retirada | Bairros/cidades, taxa, prazo, retirada no balcão | "Entrega aqui?", "Quanto é a taxa?" |
| 6 | Pagamento | Formas, quando paga, troco | "Aceita Pix?", "Pago na entrega?" |
| 7 | Alergênicos e restrições | Ingredientes, opções veganas/sem glúten, contaminação cruzada | "Tem glúten?" |
| 8 | Promoções | Promoções fixas, cupom, fidelidade | "Tem promoção?" |
| 9 | Encomendas | O que a loja faz sob encomenda e antecedência | "Fazem bolo de festa?" |
| 10 | Problemas | Atraso, item errado, cancelamento, reembolso | "Meu pedido veio errado" |
| 11 | FAQ extra | Perguntas reais dos seus clientes | "Tem estacionamento?" |
| 12 | Sempre humano | Assuntos que só uma pessoa resolve | Parcerias, notas fiscais, orçamentos |

## Começando

1. **Personalize** `agente/prompt-sistema.md` e `agente/base-conhecimento.md`. O projeto enviado ainda contém campos de exemplo `[PREENCHER]`; substitua-os pelos dados reais da sua loja. Para localizar os campos:
   ```bash
   grep -rn "PREENCHER" agente/
   ```
2. **Escolha o modo de pedido** no prompt e apague o bloco que não usa:
   - **Modo A**: a loja tem link de pedidos; o agente manda o link.
   - **Modo B**: sem link; o agente tira dúvidas do cardápio, reúne o pedido e uma pessoa confirma.
3. **Gere o fluxo** (Python 3, sem dependências):
   ```bash
   python n8n/gerar_fluxo.py
   ```
   O script avisa se ainda restarem campos `[PREENCHER]`.
4. **Suba e configure o n8n e o WAHA** seguindo [`n8n/README.md`](n8n/README.md).
5. **Teste** com as perguntas de [`avaliacao/perguntas-teste.csv`](avaliacao/perguntas-teste.csv) antes de ligar para clientes reais.

## Antes de publicar a sua versão

- Não faça commit de `.env`, chaves de API nem do número do atendente (o `.gitignore` já cobre o `.env`).
- Não coloque chave Pix, CPF/CNPJ ou telefone pessoal na base de conhecimento de um repositório público.
- Se a sua loja real tem dados próprios, mantenha essa versão em um repositório privado e deixe o público só com o template.

## Limitações

- O WAHA usa o WhatsApp Web de forma não oficial: existe risco de restrição do número.
- O agente não anota, calcula nem confirma pedidos; quem faz isso é o link ou uma pessoa.
- Não há registro de conversas nem painel de atendimento (ideias em `n8n/README.md`).
