---
name: writing-plans
description: >
  Transforma uma direção acordada num plano em arquivo — tarefas atômicas, cada uma com
  a evidência que prova que terminou, dependências mapeadas e estado vivo. Use quando o
  trabalho tem vários passos, atravessa sessões, ou envolve mais de uma pessoa.
  Triggers: "escreve o plano", "monta o passo a passo", "como a gente organiza isso".
---

# writing-plans

Plano que vive no chat morre quando a conversa fecha. Plano em arquivo sobrevive à sessão, à troca de computador e ao feriado no meio.

## Quando não usar

Tarefa de um passo só. Plano para isso é burocracia — faça.

## Os cinco princípios

**1. Tarefa atômica.** Uma tarefa é uma coisa que dá pra terminar e marcar. "Arrumar o relatório" não é tarefa, é assunto. "Trocar a fonte dos dados de X para Y" é tarefa.

**2. Cada tarefa carrega a própria prova.** Escrever, junto com a tarefa, **o que vai provar que ela terminou**. Sem isso "pronto" vira opinião, e duas pessoas discordam sobre o mesmo item estar pronto.

**3. Dependência explícita.** Se T3 precisa de T1, escrever. É o que permite ver o que dá para tocar em paralelo e o que está travado esperando.

**4. Estimativa honesta.** Se não sabe, escrever "não sei" e dizer o que faria você saber. Estimativa inventada é pior que estimativa ausente, porque alguém planeja em cima dela.

**5. O arquivo é vivo.** O plano é atualizado enquanto roda, não no fim. Plano que só é atualizado no fim vira relatório, e relatório não ajuda ninguém a decidir no meio do caminho.

## O formato

Arquivo em `content/drafts/{projeto}/PLANO.md`:

```markdown
# Plano · {projeto}

**Objetivo:** {o resultado observável, não a atividade}
**Pronto quando:** {o fato que encerra o plano inteiro}

## Fase 1 — {nome}

- [ ] **T1.1** {a tarefa, no infinitivo}
  - **Prova:** {o que eu rodo/leio/olho pra saber que terminou}
  - **Depende de:** —
  - **Tempo:** {estimativa, ou "não sei — depende de {o quê}"}

- [ ] **T1.2** {...}
  - **Prova:** {...}
  - **Depende de:** T1.1

## Fase 2 — {nome}

...

## Checkpoint

Ao fim da Fase 1, parar e mostrar o resultado antes de seguir.

## Riscos

| Risco | Sinal de que aconteceu | O que fazer |
|---|---|---|

## Fora de escopo

{o que este plano deliberadamente não faz}
```

## O objetivo é resultado, não atividade

- ❌ "Revisar o processo de aprovação"
- ✅ "O processo de aprovação documentado em um arquivo, com quem aprova cada faixa de valor"

O primeiro nunca acaba. O segundo acaba e dá pra ver.

## A seção "Fora de escopo" não é opcional

É ela que impede o plano de crescer sozinho no meio da execução. Toda boa ideia que aparecer e não estiver no objetivo vai para lá, com a data — e vira o começo do próximo plano em vez de atrasar este.

## Checkpoints

Ponha um no fim de cada fase, e trate como parada de verdade. É onde alguém olha o resultado parcial e diz "é isso" ou "não é isso" — e descobrir isso na fase 1 custa muito menos que na fase 4.

## Depois

Para executar, `executing-plans`. Para fechar, `verification-before-completion`.
