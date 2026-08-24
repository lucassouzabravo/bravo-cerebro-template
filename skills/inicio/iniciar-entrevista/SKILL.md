---
name: iniciar-entrevista
description: >
  Entrevista a pessoa para preencher os arquivos-raiz de identidade: SOUL.md (quem é o
  assistente e como fala), USER.md (quem é a pessoa) e o bloco de identidade do MEMORY.md.
  Uma pergunta por vez, rascunho antes de gravar. Chamada pelo /iniciar no passo 4.
  Triggers: "/iniciar-entrevista", "me entrevista", "refazer meu USER.md".
---

# iniciar-entrevista

> Passo 4 do `/iniciar`. Não faz ação externa — mas escreve em arquivo-raiz, então vale a regra do rascunho.

## As duas regras

**1. Uma pergunta por vez.** Esperar a resposta antes da próxima. Três perguntas juntas fazem a pessoa responder só a última e você perde as outras duas.

**2. Rascunho → aprovação → grava.** Nunca "já salvei, dá uma olhada". A pessoa vê o texto, corrige, e só então vai para o disco.

## Antes de perguntar: detectar

```bash
grep -l '{' SOUL.md USER.md MEMORY.md 2>/dev/null
```

- **Os três com marcador** → entrevista completa.
- **Nenhum com marcador** → já foi preenchido. Perguntar: manter, ajustar um ponto, ou refazer do zero?
- **Preenchido de um jeito que não parece o padrão** → alguém editou à mão. **Nunca sobrescrever.** Oferecer preservar e só acrescentar o que falta.

Antes de escrever por cima de qualquer coisa preenchida, fazer cópia:

```bash
cp SOUL.md "SOUL.md.bak-$(date +%Y%m%d-%H%M)"
```

---

## Bloco 1 — O assistente (→ `SOUL.md`)

Enquadre antes de perguntar, para não soar burocrático:

> "Primeiro, sobre mim. São quatro perguntas rápidas — elas definem como eu vou falar com você todos os dias."

**1. Nome.**
> "Como você quer me chamar?"

Se ela não tiver ideia, ofereça três e siga com qualquer escolha. Não insista: nome pode mudar depois.

**2. Como se dirigir a mim.**
> "E eu falo de mim no masculino, feminino ou tanto faz?"

Se ela não escolher, use neutro. Não deduzir por nome.

**3. Tom.** Faça como escolha concreta, não como escala abstrata:
> "Qual desses três eu pareço mais, quando te respondo?
>  (a) direto e seco, vou ao ponto e paro
>  (b) direto mas com jeito, explico o porquê
>  (c) mais próximo, pode ter humor"

**4. O que te irrita.** É a pergunta mais útil das quatro, e quase ninguém pergunta:
> "O que te irrita numa IA? Uma coisa só. Vale 'enrola muito', 'concorda com tudo', 'escreve textão'."

Isso vira uma linha explícita no `SOUL.md`, no lugar `{TOM_PERSONALIZADO}`. Escreva como regra de comportamento, não como adjetivo:

- "enrola muito" → *"Respondo em no máximo três frases quando a pergunta é fechada."*
- "concorda com tudo" → *"Quando discordo, digo antes de ajudar, não depois."*
- "textão" → *"Uso tabela ou lista sempre que a informação couber; parágrafo é exceção."*

---

## Bloco 2 — A pessoa (→ `USER.md`)

> "Agora sobre você. Isso é o que eu leio antes de toda conversa, então quanto mais preciso, menos você reexplica."

Uma por vez:

1. **Nome completo, e como prefere ser chamado.**
2. **Alçada:** gerência, liderança ou analista. *(Explique que define para qual inbox o material da Bravo vai.)*
3. **Área e cargo.**
4. **O que você faz na Bravo, em duas frases** — como explicaria para alguém que entrou hoje.
5. **Como prefere receber as coisas de mim:** *"conclusão primeiro? contexto antes? tabela ou texto? curto ou detalhado?"*
6. **Autonomia:** *"quando for uma coisa reversível e pequena, você prefere que eu faça e te avise, ou que eu pergunte antes?"*

A pergunta 6 é a que mais muda o dia a dia. Se a pessoa hesitar, recomende: **fazer e avisar** para o que é reversível, **perguntar** para o que sai do computador. É o padrão do `AGENTS.md` e ela pode mudar depois.

### O orçamento de caracteres — não é sugestão

`USER.md` e `MEMORY.md` são lidos em **toda** sessão. Por isso têm teto:

| Arquivo | Teto |
|---|---|
| `USER.md` | **1375 caracteres** |
| `MEMORY.md` | **2200 caracteres** |

Cada linha a mais aqui custa atenção em todas as conversas do dia — e o que sobra de espaço é o que sobra pro trabalho de verdade.

**Isso muda como você conduz a entrevista.** Se a pessoa der uma resposta longa, não descarte: guarde o texto inteiro na ficha dela em `memory/context/people/{slug}.md` e **resuma** no arquivo-raiz. A ficha você lê quando precisa; o arquivo-raiz você lê sempre.

Conferir antes de gravar, e mostrar:

```bash
for f in USER.md MEMORY.md; do echo "$f: $(wc -c < $f) chars"; done
```

Se estourou, cortar **com a pessoa junto**, perguntando o que é mais importante — não escolher sozinho o que sai do arquivo que descreve ela.

---

## Bloco 3 — Gravar

Mostrar os três arquivos preenchidos, **na íntegra**, antes de gravar:

> "Ficou assim. Lê e me diz o que mudar — pode ser qualquer coisa, inclusive o meu nome."

Depois do "pode gravar", escrever e **provar** que ficou limpo:

```bash
grep -n '{[A-Z_]*}' SOUL.md USER.md MEMORY.md && echo "⚠️ SOBROU MARCADOR" || echo "OK — nenhum marcador pendente"
```

Mostrar a saída literal. Se sobrou marcador, resolver antes de devolver o controle ao `/iniciar` — marcador esquecido reaparece semanas depois no meio de uma resposta e a pessoa não entende o que é.

Criar também a ficha dela em `memory/context/people/{slug}.md`, no formato do `MAPA.md` daquela pasta, com o que já foi coletado. É a primeira ficha do cérebro e serve de exemplo vivo para as próximas.

---

## Confirmação

```
Identidade gravada:

  ✓ SOUL.md    sou {nome}, {tom escolhido}
  ✓ USER.md    {Pessoa} · {área} · alçada {alçada}
  ✓ MEMORY.md  bloco de identidade preenchido
  ✓ memory/context/people/{slug}.md criada
```

## Quando algo não funciona

| Sintoma | O que fazer |
|---|---|
| A pessoa não sabe responder o tom | Escolher (b) e seguir. Dá para mudar a qualquer momento — não travar a configuração nisso |
| Ela dá resposta longa demais para o `USER.md` | Guardar o texto inteiro na ficha em `people/` e resumir no arquivo-raiz. Não descartar o que ela falou |
| Ela quer mudar o nome do assistente depois | Editar `SOUL.md` e `MEMORY.md`. Não precisa refazer nada |
| Arquivo já tinha edição manual | Preservar. Só acrescentar o que falta, nunca substituir o texto dela |
