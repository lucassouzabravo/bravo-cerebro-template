---
name: executing-plans
description: >
  Executa um plano escrito, tarefa a tarefa, marcando o progresso no arquivo em tempo
  real, levantando bloqueio assim que aparece e parando nos checkpoints. Use depois do
  writing-plans, ou quando já existe um PLANO.md para tocar.
  Triggers: "executa o plano", "toca isso", "continua de onde parou".
---

# executing-plans

Percorrer o plano sem se perder, sem inventar escopo, e sem chegar no fim com uma lista de coisas que "acho que fiz".

## Antes de começar

Ler o plano inteiro. Se ele não existir em arquivo, é `writing-plans` primeiro — executar de cabeça é como o escopo cresce sem ninguém perceber.

Conferir três coisas:

- o objetivo ainda é o objetivo? (planos envelhecem)
- alguma dependência mudou desde que foi escrito?
- alguma tarefa já está feita?

## O ciclo, por tarefa

```
1. Anunciar: "T1.2 — {a tarefa}"
2. Fazer
3. Rodar a prova que está escrita na tarefa
4. Mostrar o resultado da prova, literal
5. Marcar [x] no arquivo, na hora
6. Próxima
```

**O passo 5 acontece na hora, não no fim.** Marcar tudo de uma vez no final é como se perde o rastro de onde parou quando a sessão cai.

**O passo 4 não se pula.** "Rodei e passou" não é evidência — é afirmação. A saída literal é evidência.

## Os três desfechos de uma tarefa

| Desfecho | O que fazer |
|---|---|
| **Deu certo** | Marcar `[x]`, seguir |
| **Deu errado** | Marcar `[!]`, escrever o que aconteceu, tentar o caminho alternativo óbvio. Se não houver, virar bloqueio |
| **Precisa de decisão** | **Parar.** Não escolher sozinho. Perguntar, com a sua recomendação junto |

O terceiro é o que mais se erra. Quando aparece uma bifurcação que não estava no plano, a tentação é escolher a que parece razoável e seguir. Mas escolha não prevista é justamente onde o trabalho sai do que foi combinado — e quem descobre é a pessoa, três tarefas depois, quando é caro voltar.

## Bloqueio

Assim que travar, **levantar na hora**. Não acumular para o fim do dia.

```
🚧 Travei em T2.3

O que eu precisava: {o quê}
O que aconteceu: {o fato, com a mensagem real}
O que eu já tentei: {1-2 coisas}
O que destrava: {o que você precisa fazer/decidir}

Enquanto isso posso tocar: T2.4 e T3.1 (não dependem desta)
```

A última linha importa: bloqueio não precisa parar o plano inteiro se houver tarefa independente.

## Checkpoint

No checkpoint, parar de verdade e mostrar:

```
Checkpoint — fim da Fase {N}

Feito:     {as tarefas, com a prova de cada uma}
Não feito: {o que ficou, e por quê}
Mudou:     {o que a execução ensinou e não estava no plano}

Continuo pra Fase {N+1}?
```

A linha "mudou" é a mais valiosa. Execução sempre ensina alguma coisa que o plano não sabia, e é aí que o plano é corrigido — não no fim, quando já custou.

## Escopo

Se aparecer uma boa ideia que não está no plano: **anotar em "Fora de escopo" e seguir.** Não fazer no impulso.

Se a pessoa pedir para adicionar algo grande no meio, dizer o custo antes: *"dá pra fazer, mas atrasa a Fase 3 em uns dois dias. Entra agora ou depois?"*

## Ação de risco

Independente de a pessoa ter dito "toca tudo": **qualquer ação irreversível ou externa passa por confirmação.** Enviar, publicar, apagar, comprar, contratar. "Executa tudo" autoriza o trabalho, não autoriza o risco.

## Fechamento

Nunca declarar o plano concluído aqui. Isso é `verification-before-completion` — a última coisa que se faz, e ela tem autoridade para dizer que não terminou.
