# Guia do padrão visual "card + nota" para fluxogramas no Miro

> Extraído elemento a elemento de `modelo fluxograma explicado.jpg` (árvore de OKR feita no Miro,
> 680×453px). Cores amostradas por pixel, regiões ampliadas 4–6× e lidas uma a uma.
> **O objetivo não é copiar a árvore de OKR. É roubar a lógica de organização dela** e aplicar
> na explicação de fluxos do n8n.

---

## 1. A lógica de fundo, antes de qualquer estilo

A referência resolve um problema idêntico ao nosso: **mostrar uma estrutura e, ao mesmo tempo,
explicar cada pedaço dela, sem virar um monte de texto solto ao lado do desenho.**

Ela resolve com quatro decisões, e é isso que vale copiar:

### 1.1 Cor é parentesco, não decoração

Cada ramo da árvore tem uma cor, e **tudo que pertence àquele ramo carrega a cor dele**: o
cabeçalho do card, os filhos, e o texto dos itens. Só existem três cores de estrutura no desenho
inteiro. Nenhuma cor é escolhida por gosto.

### 1.2 A cor atravessa o nível e amarra pai e filho

Este é o truque mais forte da imagem, e é fácil não perceber.

No card raiz, os dois resultados-chave estão escritos assim:

```
1. Get 1K new signups        ← escrito em ROSA
2. Launch a brand event      ← escrito em AZUL
```

O item 1 é rosa porque **quem vai executá-lo é o ramo rosa**. O item 2 é azul pelo mesmo motivo.
O olho liga o pai ao filho **antes de ler**, só pela cor. A seta confirma o que a cor já disse.

### 1.3 O que desce de cima vira uma nota amarela embaixo

O resultado-chave do pai **reaparece literalmente como o objetivo do filho**, e reaparece dentro
de uma nota amarela.

```
PAI  (Head of Brand)   Key Result nº1: "Get 1K new signups"
                                  ↓
FILHO (Head of Content)   Objective: [nota amarela] "Get 1K new signups"
```

A nota amarela é sempre a mesma coisa em todo nível: **o compromisso que veio de cima**. O olho
aprende esse significado uma vez e usa no desenho inteiro.

### 1.4 Rótulo nunca flutua: ele é uma faixa

Nenhuma palavra de rótulo aparece solta. "Objective" e "Key Results" vivem dentro de uma
**faixa cinza que ocupa a largura inteira do card**. A faixa é o título; o que vem embaixo dela é
o conteúdo. É o que impede o efeito de "texto jogado".

**A regra geral, que é a que você pediu:**
> Todo texto pertence a um recipiente, e todo recipiente tem um rótulo acima dele.
> Se um texto não está dentro de nada, ele está errado.

---

## 2. Vocabulário de elementos (só existem 5)

O desenho inteiro é feito com cinco peças. Não invente uma sexta.

| # | Peça | Função | Como é |
|---|---|---|---|
| 1 | **Barra de título** | nomeia o nó | retângulo cheio na cor do ramo, texto branco, negrito, monoespaçado, centralizado |
| 2 | **Faixa de rótulo** | titula uma seção dentro do card | retângulo cinza claro, largura total do card, texto cinza escuro monoespaçado, alinhado à esquerda |
| 3 | **Nota amarela** | um compromisso ou um dado fechado | quadrado amarelo pálido, sombra suave embaixo, texto pequeno centralizado, **mais estreito que o card** |
| 4 | **Lista numerada** | vários itens de um mesmo tipo | `1.` `2.` `3.`, texto na cor do ramo dono do item, recuo pendente (a 2ª linha alinha com o texto, não com o número) |
| 5 | **Conector** | ligação pai→filho | linha preta ~2px, cotovelo ortogonal com canto arredondado, ponta de seta cheia entrando no topo do card filho |

### Paleta exata (amostrada da imagem)

| Cor | Hex | Uso |
|---|---|---|
| Azul-marinho | `#050039` | raiz / nível 1 |
| Rosa | `#ED2663` | ramo 1 e tudo que pertence a ele |
| Azul | `#5B9CCB` | ramo 2 e tudo que pertence a ele |
| Cinza da faixa | `#EDEDED` aprox. | fundo da faixa de rótulo |
| Amarelo da nota | `#F7EFA8` aprox. | nota |
| Preto do conector | `#000000` | setas |
| Fundo | branco | canvas |

Tipografia: **monoespaçada em tudo que é estrutura** (títulos, rótulos, listas). A nota amarela usa
fonte de texto normal, menor. Esse contraste entre mono e não-mono separa "estrutura" de
"conteúdo humano" sem precisar de mais nenhuma cor.

---

## 3. Anatomia do card, por profundidade

A gramática é a mesma em todo nível. **O que muda é só a densidade, nunca o vocabulário.**

### Nível 1 e 2 — card largo, duas colunas lado a lado

```
┌───────────────────────────────────────────────┐
│           BARRA DE TÍTULO (cor do ramo)       │  ← texto branco centralizado
├───────────────────────────────────────────────┤
│ Objective      │ Key Results                  │  ← UMA faixa cinza, dois rótulos
├────────────────┼──────────────────────────────┤
│ ┌──────────┐   │ 1. item na cor do filho      │
│ │  nota    │   │ 2. item na cor do filho      │
│ │ amarela  │   │ 3. item na cor do filho      │
│ └──────────┘   │                              │
└───────────────────────────────────────────────┘
```

A coluna da esquerda ocupa cerca de 30% e a da direita o resto. A nota amarela fica na coluna
esquerda, **encostada no topo da área de conteúdo**, não centralizada verticalmente.

### Nível 3 — card estreito, tudo empilhado

Quando o card fica estreito demais para duas colunas, **as colunas viram andares**, na mesma
ordem de leitura:

```
┌─────────────────────┐
│     BARRA (cor)     │
├─────────────────────┤
│ Objective           │  ← faixa cinza, largura total
├─────────────────────┤
│     ┌─────────┐     │
│     │  nota   │     │  ← nota mais estreita que o card, recuada
│     └─────────┘     │
├─────────────────────┤
│ Key Results         │  ← faixa cinza, largura total
├─────────────────────┤
│     ┌─────────┐     │
│     │  nota   │     │
│     └─────────┘     │
└─────────────────────┘
```

Detalhe que faz diferença: **a faixa cinza vai de ponta a ponta, a nota não.** Esse
desencontro proposital é o que faz a faixa ler como título e a nota ler como conteúdo. Se as duas
tivessem a mesma largura, virariam duas listras e a hierarquia sumiria.

---

## 4. Regras de alinhamento e espaço

1. **Irmãos compartilham o topo.** Os três cards de um mesmo nível começam exatamente na mesma
   altura. Nada de escadinha.
2. **Irmãos compartilham a linha de base interna.** A faixa "Objective" dos três cards está na
   mesma altura; a nota também; a faixa "Key Results" também. O desenho tem uma grade horizontal
   invisível que atravessa os irmãos.
3. **Uma margem esquerda por card.** Faixa e conteúdo começam no mesmo x.
4. **Vão igual entre irmãos.** A distância entre os cards do mesmo nível é constante.
5. **Respiro interno em tudo.** Nenhum texto encosta na borda do recipiente.
6. **A nota é menor que o card** e recuada, nunca colada na margem.

---

## 5. Conectores

- Saem do **centro da base** do card pai.
- Descem, viram numa **barra horizontal única** compartilhada por todos os filhos, e descem de
  novo em cada filho.
- Canto **arredondado**, não em bico.
- Ponta de seta **cheia**, entrando no **centro do topo** do card filho.
- Preto, espessura constante em todos os níveis.
- Um pai com filho único usa só um segmento reto vertical, sem barra horizontal.

---

## 5-B. Sistema de cores quando existem muitas categorias

A referência usa três cores porque tem três ramos. **Um fluxo de n8n tem muito mais coisa, então
a regra não é "use rosa e azul", é "tenha um sistema".**

1. **Antes de desenhar, escreva a legenda.** Decida a lista de categorias e a cor de cada uma.
   A categoria pode ser o tipo de nó (gatilho, transformação, condição, requisição, banco, IA) ou
   o subfluxo dono (WhatsApp, Aircall, Meeting). Escolha **um** critério e mantenha.
2. **Uma cor significa uma coisa só, no desenho inteiro.** Se azul é "banco", nada mais é azul.
3. **A legenda fica visível no canvas**, num canto, com o quadradinho de cor e o nome da categoria.
4. **Teto de 6 a 8 cores.** Passou disso, o olho não decora mais e vira arco-íris: agrupe
   categorias parecidas sob a mesma cor e diferencie por texto.
5. **As cores precisam ser distinguíveis entre si.** Nada de dois azuis próximos para duas coisas
   diferentes. Se precisar de variação dentro de uma família, mude também a forma ou a borda.
6. **Cor herdada continua valendo:** o que pertence a uma categoria carrega a cor dela, e um item
   que aponta para outro nó pode ser escrito na cor do nó de destino, exatamente como na referência.

---

## 5-C. Nada pode tapar nada (regra dura)

**Proibido — um elemento escondendo outro, no todo ou em parte:**

- card por cima de card;
- texto por cima de texto;
- linha ou seta atravessando por cima de um card;
- rótulo de ligação em cima da própria linha;
- nota sobrepondo a borda de outro elemento.

**Permitido, e não conta como sobreposição — elemento contido em outro:**

Texto dentro de um card, nota dentro de uma coluna, rótulo dentro de uma faixa. Isso é
**pertencimento**, e é justamente o que o padrão pede. A diferença é simples: contido significa
que o de dentro está inteiro visível e o de fora serve de moldura. Sobreposto significa que um
esconde pedaço do outro.

> O teste: **algum elemento ficou parcialmente escondido?** Se sim, é sobreposição e está errado.
> Se tudo está inteiramente visível, está certo.

**Espaçamento mínimo, para nada encostar:**

| Entre | Regra |
|---|---|
| Texto e a borda do próprio recipiente | respiro em todos os lados, nunca colado |
| Dois textos irmãos | espaço maior que a altura de uma linha |
| Dois cards vizinhos | vão constante, e maior que o respiro interno |
| Card e qualquer linha | a linha não encosta na lateral do card; só toca no ponto de entrada da seta |
| Rótulo de ligação e a linha | o rótulo fica **acima** da linha, com folga, sem cruzá-la |

Se um cruzamento de linhas for inevitável, a linha **contorna** o card em vez de passar por cima.

---

## 6. Como isso vira a explicação de um fluxo do n8n

Tradução direta do padrão para o nosso caso. **Nada aqui é invenção nova: é a mesma gramática.**

Tradução direta, peça por peça:

| Na referência | No nosso fluxo do n8n |
|---|---|
| Card de pessoa/área | **Card = um nó do n8n** |
| Cor do ramo | Cor da **categoria do nó**, conforme a legenda (seção 5-B) |
| Barra de título | Nome do nó, igual ao que está no n8n |
| Nota amarela | **A explicação daquele nó**: o que ele faz, em linguagem humana, uma ideia por nota |
| Lista de texto ao lado | **Os campos preenchidos dentro do nó** — um item por campo, com o valor escolhido |
| Faixa cinza | Título de cada bloco: "O que faz", "Campos", "Saída" |
| Seta pai→filho | Ordem de execução |
| — (novo) | **Rótulo acima da linha**: o que passa de um nó para o outro |

### O que passa entre os nós vai escrito acima da linha

Este é o acréscimo em cima da referência. Cada ligação carrega, **acima da linha e sem encostar
nela**, o que sai de um nó e entra no seguinte: o nome do dado, o formato, a quantidade de itens.
É o que responde "de onde veio esse campo?" sem precisar abrir o n8n.

```
   ┌──────────────┐
   │  Nó A        │
   └──────┬───────┘
          │  ← rótulo aqui em cima: "1 item por conversa: id, telefone, texto"
          ▼
   ┌──────────────┐
   │  Nó B        │
   └──────────────┘
```

### O fim do texto jogado

Onde hoje existe um parágrafo corrido à direita do desenho, passa a existir: **faixa cinza com o
título do assunto + notas embaixo, uma ideia por nota.** Explicação com quatro assuntos vira
quatro faixas com suas notas, nunca um parágrafo com quatro assuntos.

### Não existe linha tracejada, e é de propósito

A referência **não usa nenhuma linha de ligação entre a explicação e o nó**, e mesmo assim não
resta dúvida sobre o que pertence a quem. O pertencimento é dito por três coisas ao mesmo tempo:

1. **contenção** — a explicação está *dentro* do card, não ao lado dele;
2. **faixa titulando** — a faixa cinza logo acima diz o que aquele bloco é;
3. **alinhamento em coluna** — tudo do mesmo nó divide a mesma margem esquerda.

Linha tracejada seria muleta para um problema que o layout já resolve, e cada linha a mais é mais
uma coisa para cruzar, tapar e poluir. **Se você sentiu falta de uma tracejada, o layout está
errado:** o bloco está longe demais do dono, ou sem faixa, ou desalinhado. Conserte a posição,
não acrescente linha.

Linha, no desenho, significa **uma coisa só: fluxo de execução**.

---

## 7. Checagem final (tudo é sim ou não)

1. Existe algum texto fora de um recipiente? Tem que ser **não**.
2. Todo recipiente tem uma faixa de rótulo acima dele?
3. Existe legenda de cores no canvas, e cada cor significa uma coisa só?
4. Alguma cor é usada para duas categorias diferentes? Tem que ser **não**.
5. **Algum elemento está parcialmente escondido por outro? Tem que ser não.**
6. Algum texto encosta na borda do recipiente? Tem que ser **não**.
7. Alguma linha passa por cima de um card? Tem que ser **não**.
8. Os irmãos começam na mesma altura, e as faixas internas deles também?
9. Toda faixa ocupa a largura do card, e nenhuma nota ocupa?
10. Todo conector é ortogonal, com canto arredondado e ponta cheia no topo do filho?
11. Toda ligação tem, acima dela e sem encostar, o que passa de um nó para o outro?
12. Alguma nota tem mais de uma ideia dentro? Tem que ser **não**.
13. Todo bloco de explicação está **dentro** do card do nó que ele explica, sob uma faixa e na
    mesma margem? (se você precisou de linha para explicar o pertencimento, está errado)

---

*Extraído em 11/08/2026 a partir de `modelo fluxograma explicado.jpg`. Cores por amostragem de
pixel; layout por leitura de 7 recortes ampliados.*
