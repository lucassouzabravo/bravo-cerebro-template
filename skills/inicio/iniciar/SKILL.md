---
name: iniciar
description: >
  Configura este cérebro na primeira vez. Explica como ele funciona, prepara a máquina,
  conecta ao GitHub, entrevista a pessoa para preencher SOUL/USER/MEMORY, semeia o
  contexto de trabalho dela, cria a estação no inbox da alçada, e roda um teste de ponta
  a ponta. Use quando o cérebro acabou de ser criado, quando os arquivos-raiz ainda têm
  marcadores entre chaves, ou quando a pessoa trocou de máquina.
  Triggers: "/iniciar", "configura meu cérebro", "primeira vez".
disable-model-invocation: true
---

# /iniciar

> Orquestradora. Ela **não faz** o trabalho: chama a sub-skill de cada passo e conduz a pessoa entre eles. Cada sub-skill é responsável por detectar o que já existe e não refazer.

`disable-model-invocation` porque este fluxo instala software, autentica conta e cria repositório. São ações externas — só rodam quando a pessoa pede.

## Antes de começar: quem está falando comigo

Se `USER.md` já tem nome preenchido, use-o. Se ainda está com `{PESSOA}`, pergunte o nome agora e use daqui em diante. Ninguém merece ser chamado de "usuário".

## As quatro regras deste fluxo

Valem em todos os passos e em todas as sub-skills.

**1. Detectar antes de perguntar.** Antes de qualquer passo, olhar o que já existe. Nunca refazer o que está pronto, nunca sobrescrever o que a pessoa customizou à mão. Se algo já estiver preenchido de um jeito que não parece o padrão, perguntar: manter, ajustar ou refazer?

**2. Mostrar o resultado de verdade.** Quando um passo roda um comando, são três mensagens, nesta ordem:

```
1. "Vou rodar isto agora: {comando exato}"
2. {a saída literal do comando, copiada}
3. "Isso quer dizer que {interpretação}"
```

**Nunca pular a mensagem 2, e nunca fingir sucesso.** Se falhou, mostrar a falha e tratar. Boa parte do que dá errado numa configuração é silencioso — quem não vê a saída não sabe que quebrou.

**3. Uma pergunta por vez.** Perguntar três coisas de uma vez confunde e faz a pessoa responder só a última.

**4. Rascunho antes de gravar.** Quando um passo vai escrever num arquivo-raiz, mostrar o texto, esperar o "pode gravar", e só então escrever. Nunca "já salvei, dá uma olhada".

## Se a pessoa sair do trilho

Toda mensagem dela cai em um de quatro casos:

| Caso | O que fazer |
|---|---|
| Respondeu o que foi perguntado | seguir |
| Pediu para ver algo do próprio cérebro | atender, e voltar para a pergunta |
| Perguntou algo relacionado | responder em duas linhas e voltar |
| Puxou outro assunto | responder curto, e oferecer: "quer que eu pause a configuração e a gente volta depois?" |

Três desvios seguidos no mesmo passo: **oferecer pausa**. Anotar em `MEMORY.md` o passo em que parou, para retomar sem repetir.

## Os sete passos

| # | Passo | Sub-skill | Tempo |
|---|---|---|---|
| 1 | Entender o que é este lugar | *(aqui mesmo, ver abaixo)* | 4 min |
| 2 | Preparar a máquina e conectar ao GitHub | `iniciar-ambiente` | 8 min |
| 3 | Criar e ligar os repositórios | `iniciar-repo` | 4 min |
| 4 | Te conhecer | `iniciar-entrevista` | 6 min |
| 5 | Trazer seu contexto de trabalho | `iniciar-contexto` | 6 min |
| 6 | Abrir sua estação no inbox da alçada | `iniciar-estacao` | 3 min |
| 7 | Provar que funciona | `iniciar-verificar` | 4 min |

A ordem importa. Os passos 3 a 7 dependem do 2 (sem GitHub conectado, nada sobe), e o 6 depende do 4 (a estação usa o nome e a alçada).

---

## Passo 1 — Entender o que é este lugar

Antes de configurar qualquer coisa, a pessoa precisa entender o modelo. Configuração sem modelo mental vira sequência de cliques que ninguém consegue repetir nem consertar.

**Abrir dizendo de onde isto veio.** Não é formalidade: saber que a estrutura já roda de verdade muda como a pessoa a trata. Em duas frases, com as suas palavras:

> "Antes de começar: isto aqui não é template genérico baixado da internet. É o cérebro que o Lucas e o Banguela construíram juntos ao longo de meses trabalhando na Bravo, e que eles adaptaram pra que outras pessoas pudessem ter o próprio. Cada regra que você vai ver aqui existe porque alguma coisa deu errado antes e ensinou. Você tá começando de um lugar que já funciona."

Se a pessoa quiser saber mais, o `CREDITOS.md` conta a história inteira.

Depois, ler `referencias/o-que-e-o-cerebro.md` e conduzir a explicação a partir dele. **Não despejar o arquivo inteiro** — é roteiro para você, não texto para colar.

Fechar com a pergunta-âncora:

> "Antes de eu mexer na sua máquina: faz sentido até aqui? Alguma coisa ficou estranha?"

Se ela responder com dúvida sobre onde as coisas ficam, mostrar o `MAPA.md` de verdade em vez de explicar de novo.

---

## Passo 2 — `iniciar-ambiente`

Invocar a sub-skill `iniciar-ambiente`.

Ela instala o `gh` (o programa que fala com o GitHub), conecta a conta e confere a identidade do git.

> ⚠️ **A autenticação é feita pela pessoa, no navegador dela.** Você mostra o código e o endereço; ela abre, cola e autoriza. Você **não digita senha, não digita token, não preenche credencial de ninguém** — nunca, nem se ela oferecer.

Ao voltar, confirmar em uma linha o que ficou pronto e seguir.

---

## Passo 3 — `iniciar-repo`

Invocar `iniciar-repo`.

Ela cria o repositório pessoal a partir deste template, deixa a pasta no lugar certo, e clona o inbox da alçada ao lado.

Se a pessoa ainda não souber a alçada dela, perguntar aqui:

> "Você entra como **gerência**, **liderança** ou **analista**? Isso define para qual inbox o seu material da Bravo vai — e é o Lucas quem te libera o acesso."

Se ela não tiver acesso liberado ainda, **não travar o fluxo**: seguir para o passo 4, marcar a pendência, e fechar o passo 6 depois que o acesso sair.

---

## Passo 4 — `iniciar-entrevista`

Invocar `iniciar-entrevista`.

Ela preenche `SOUL.md` (quem eu sou e como falo), `USER.md` (quem é a pessoa) e a parte de identidade do `MEMORY.md`.

Ao voltar: **reler os três arquivos e provar que não sobrou nenhum marcador entre chaves.** Mostrar o resultado da conferência.

---

## Passo 5 — `iniciar-contexto`

Invocar `iniciar-contexto`.

Ela pergunta o que a pessoa está tocando hoje, pede material real se houver, e semeia `memory/projects/`, `memory/hot.md` e `memory/context/`.

Este é o passo que transforma o cérebro de "estrutura vazia" em "assistente que sabe do que você está falando". Se a pessoa estiver com pressa, este é o passo que **não** pode ser cortado — sem ele o cérebro nasce oco.

---

## Passo 6 — `iniciar-estacao`

Invocar `iniciar-estacao`.

Ela cria a pasta da pessoa dentro do inbox da alçada e configura o `/cerebro` e o `/salve` com os endereços certos dos dois repositórios.

---

## Passo 7 — `iniciar-verificar`

Invocar `iniciar-verificar`.

Ela roda um `/salve` de teste de verdade — escreve, envia ao GitHub, e **confirma no remoto** que chegou. Depois faz três perguntas curtas sobre os gatilhos, para confirmar que a pessoa entendeu o que sobe e o que não sobe.

---

## Fechamento

Marcar em `MEMORY.md`:

```markdown
- `cerebro_iniciado`: true — {data}
```

E fechar assim, com o que está pronto e o que ficou pendente:

```
Pronto. Seu cérebro está no ar.

  ✓ Máquina preparada e conectada ao GitHub
  ✓ Seu repositório: {url}
  ✓ Inbox da alçada {alcada}: {url}
  ✓ {N} projetos e {M} pendências já registrados
  ✓ Teste de ponta a ponta passou

Daqui pra frente são dois comandos:

  /cerebro   no começo do dia, pra eu lembrar de tudo
  /salve     quando terminar algo que vale guardar

Não precisa decorar mais nada.
```

Se algo ficou pendente (acesso ao inbox, por exemplo), listar embaixo com o que falta e de quem depende. **Não declarar pronto o que não está.**

## Quando não usar

- O cérebro já foi iniciado e a pessoa só quer trabalhar → é `/cerebro`.
- Ela quer só guardar uma coisa → é `/salve`.
- Ela quer refazer um passo específico → chamar a sub-skill direto, sem o fluxo inteiro.

## Se rodar de novo

É seguro. Cada sub-skill detecta o que já existe e oferece pular. Rodar duas vezes não duplica nem apaga nada.
