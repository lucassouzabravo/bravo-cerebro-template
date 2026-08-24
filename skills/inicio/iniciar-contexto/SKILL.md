---
name: iniciar-contexto
description: >
  Semeia o cérebro com o trabalho real da pessoa: projetos que ela toca, o que está em
  aberto, pessoas com quem trabalha, e o conhecimento da Bravo que só existe na cabeça
  dela. Aceita material pronto (relatório, planilha, apresentação) e transforma em fichas.
  Chamada pelo /iniciar no passo 5.
  Triggers: "/iniciar-contexto", "semeia meu contexto", "cadastra meus projetos".
---

# iniciar-contexto

> Passo 5 do `/iniciar`. É o passo que transforma o cérebro de estrutura vazia em assistente que sabe do que você está falando. **Se a pessoa estiver com pressa, este é o passo que não pode ser cortado.**

## Por que este passo existe

Um cérebro com `SOUL.md` e `USER.md` preenchidos mas `memory/` vazia sabe *quem* você é e não sabe *no que* você está. Na prática ele ainda não serve para nada — a pessoa faz a primeira pergunta real, não recebe nada de útil, e desiste.

## Como conduzir

Não é formulário. É conversa curta em quatro blocos, e em cada um você **escreve enquanto ela fala** — mostrando o arquivo que nasceu. Ver o arquivo aparecer é o que faz a ficha cair.

---

## Bloco 1 — O que está na sua mesa hoje

> "Me conta o que você está tocando agora. Não precisa ser completo — três ou quatro coisas que ocupam sua cabeça esta semana."

Para cada uma, puxar só o suficiente para a ficha:

- o que é, em duas frases, para quem chega sem contexto;
- onde está hoje;
- qual é a próxima coisa a fazer, e de quem depende.

Criar `memory/projects/{nome}.md` no formato do `MAPA.md` daquela pasta.

**Se ela não souber o próximo passo, escrever "não definido"** e dizer por quê:

> "Deixei 'não definido' de propósito. Projeto sem próximo passo normalmente quer dizer que ele travou ou morreu — e as duas coisas valem você saber quando bater o olho."

Depois, montar o `memory/hot.md` com esses projetos no "Foco imediato". Mostrar o arquivo pronto.

---

## Bloco 2 — O que está te esperando

> "E o que está parado esperando alguém? Aprovação, resposta, material que não chegou."

Cada item vira uma pendência em `memory/context/pendencias.md`, no formato daquela pasta — com **dono** e **condição de fechamento**. Se ela der uma pendência sem dono, perguntar de quem depende. Pendência sem dono não fecha nunca.

---

## Bloco 3 — Com quem você trabalha

> "Quem são as três ou quatro pessoas que mais aparecem no seu trabalho? Quem aprova, quem depende de você, quem você depende."

Uma ficha por pessoa em `memory/context/people/`.

> ⚠️ **Aqui vale reforçar a régua, na hora, com exemplo.** Registrar **como a pessoa trabalha**, não julgar se ela é boa:
> - ✅ "prefere receber os números antes da reunião, não durante"
> - ❌ "é desorganizado"
>
> E dizer por quê: *"isso aqui fica gravado num repositório, com histórico. O que a gente escrever hoje continua legível daqui a dois anos."*

Se ela começar a avaliar desempenho, interromper com jeito e reformular junto para o "como trabalha".

---

## Bloco 4 — O que só existe na sua cabeça

Este é o bloco mais valioso e o menos óbvio. Ancorar num incômodo concreto:

> "Última coisa. Tem alguma coisa da Bravo que você explica direto pra alguém — como um processo funciona, o que uma sigla quer dizer, quem aprova o quê — e que não está escrito em lugar nenhum?"

O sinal é esse: **se ela já explicou a mesma coisa mais de uma vez, vale registrar.**

Cada uma vira um arquivo em `memory/context/bravo/`. Escrever com as palavras dela, não traduzir para um vocabulário corporativo — quem vai ler depois precisa reconhecer o jeito que as pessoas falam de verdade ali dentro.

Ao escrever, dizer em qual das camadas aquilo cai e por quê, em meia linha. É a primeira vez que a pessoa vê a classificação funcionando, e é o que faz o `/salve` parecer óbvio depois:

> "Isso aqui é 'quem faz e o que pode decidir' — camada de Papéis. É exatamente o tipo de coisa que vale subir pro cérebro da Bravo depois."

**Não enviar nada agora.** Este passo só escreve no cérebro pessoal. O envio é do `/salve`, com a confirmação dela, e vai acontecer no passo 7 como teste.

---

## Material pronto

Se a pessoa tiver arquivo (relatório, planilha, apresentação, documento de processo), aceitar:

> "Se você tiver algum material que descreve seu trabalho, me manda que eu leio e já organizo."

Ler, extrair o que é estado (vai para `memory/`) e o que é entregável (vai para `content/drafts/`), e **mostrar o que entendeu antes de gravar**. Não inventar o que não está no material — se ficou dúvida, perguntar.

> ⚠️ Se o material contiver dado que dispara os três gatilhos (dinheiro com nome, avaliação de pessoa, jurídico), avisar na hora e guardar **fora** de `memory/context/bravo/`, para não vazar no primeiro `/salve`.

---

## Confirmação

```
Contexto semeado:

  ✓ {N} projetos em memory/projects/
  ✓ {M} pendências, todas com dono
  ✓ {P} pessoas em memory/context/people/
  ✓ {Q} coisas da Bravo registradas em memory/context/bravo/
  ✓ hot.md montado com o seu foco da semana
```

Se algum número for zero, dizer qual e oferecer voltar. Cérebro com zero projeto não vai servir para nada na segunda-feira.
