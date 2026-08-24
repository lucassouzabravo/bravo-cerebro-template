---
name: verification-before-completion
description: >
  Confere, com evidência, se cada critério de sucesso foi realmente atingido — antes de
  qualquer coisa ser declarada pronta. Mata o "acho que funciona". Use no fim de qualquer
  tarefa, projeto ou entrega, e sempre antes de dizer que terminou.
  Triggers: "terminei", "está pronto?", "confere se funcionou", "pode entregar?".
---

# verification-before-completion

Uma coisa só é considerada pronta quando existe **evidência** de que está — não quando parece que está.

Esta skill tem autoridade para dizer que **não** terminou. É o ponto dela.

## O princípio

> "Rodou sem erro" prova que rodou. Não prova que o resultado está certo.

A pergunta não é *"executou?"*. É *"produziu o resultado que a gente queria?"* — e essas duas coisas divergem com muito mais frequência do que a intuição sugere.

## Como conferir

Pegue os critérios de sucesso — do plano, do combinado, ou do pedido — e trate **um por um**. Nada de veredito geral.

Para cada um:

| Passo | O que fazer |
|---|---|
| 1 | Escrever o critério como ele foi combinado |
| 2 | Escolher a prova que **responde àquele critério**, não outra |
| 3 | Rodar / abrir / ler |
| 4 | Colar o resultado literal |
| 5 | ✅ atingido · ⚠️ parcial · ❌ não atingido |

O passo 2 é onde mora o erro. A prova tem que responder à pergunta que foi feita:

| Se o critério é | A prova NÃO é | A prova é |
|---|---|---|
| "o arquivo chegou no GitHub" | o comando não deu erro | ler o remoto e ver o arquivo |
| "o relatório ficou legível" | o arquivo existe | abrir e olhar |
| "o número está certo" | a conta rodou | conferir contra uma fonte independente |
| "a pessoa consegue usar" | eu consegui usar | ela usar, sem eu ao lado |

**Trabalho visual exige abrir e olhar.** Medição programática diz que os elementos existem e não diz que o resultado ficou bom.

## Duas armadilhas

**A prova não pode chamar a coisa que ela audita.** Se o gabarito e o alvo saem do mesmo lugar, plantar um defeito no alvo planta o mesmo defeito no gabarito — e a prova só sabe dizer SIM. Enuncie o critério como propriedade independente.

**Quem procura por padrão de nome declara quantos esperava.** "Achei 5 arquivos" não prova que são os 5 certos, prova que achou 5. Diga o número esperado e imprima a lista.

## O veredito

```
Verificação — {o que}

| Critério | Prova | Resultado |
|---|---|---|
| {critério 1} | {o que eu rodei/olhei} | ✅ |
| {critério 2} | {...} | ⚠️ parcial — {o que falta} |
| {critério 3} | {...} | ❌ — {por quê} |

Veredito: {PRONTO | NÃO PRONTO}
```

**Se houver um único ❌, o veredito é NÃO PRONTO.** Sem arredondar, sem "praticamente pronto", sem "só falta um detalhe".

Com ⚠️, dizer exatamente o que falta e quanto custa fechar — e deixar a decisão de entregar assim com a pessoa. Ela pode aceitar; você não pode decidir por ela.

## O que não vale como evidência

- "acho que funciona"
- "deve estar certo"
- "rodou sem erro" *(quando o critério não é sobre rodar)*
- "está igual à última vez que funcionou"
- o resultado de uma execução anterior, de antes da mudança

## Se falhou

Não é fracasso, é a skill funcionando. Dizer o que falhou, o que provavelmente causou, e qual o próximo passo. Depois voltar para `executing-plans`.

O caro não é descobrir aqui que não terminou. O caro é descobrir depois de entregar.
