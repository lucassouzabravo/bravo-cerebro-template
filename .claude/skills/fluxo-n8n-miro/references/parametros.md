# Parâmetros que funcionaram (medidos no board, 11/08/2026)

> Todos estes números saíram de um fluxo de teste real de 8 nós criado no board do Lucas, corrigido
> em 5 rodadas até fechar sem sobreposição, com o espaçamento conferido em zoom de 599%.
> **Comece por aqui em vez de recalibrar.** Se mudar algum valor, mude com motivo e re-meça.

**Distinção que importa em todo este arquivo:**

- **declarado** = o valor que vai no SVG;
- **renderizado** = o que aparece na tela.

Para forma, faixa e conector os dois batem. Para **post-it** e **lista de campos** não batem, e é
o renderizado que vale (ver as seções específicas).

---

## 0. O padrão horizontal (validado e aprovado pelo Lucas em 12/08/2026)

**Estes são os números do padrão atual.** As seções 1 e 2 abaixo são do fluxo de teste original
(card de 280, explicação em coluna) e continuam valendo como referência de ritmo, mas quando
houver conflito, **vale esta seção**.

### Larguras — só existem três

| Elemento | Largura | Observação |
|---|---|---|
| **Faixa de título** (qualquer uma) | **440** | "O que faz", "Campos", "Observações", "sai do X · entra no Y" — todas iguais |
| **Card do nó** | **440** × 120 | mesma largura da faixa |
| **Lista** (`<textArea>`) | **440** | mesmo `x` da faixa: título e lista alinhados, sem sobra à direita |
| **Card interno** (post-it amarelo e card cinza) | **360** | recuado 40 dentro do bloco de 440 |

O desencontro que cria hierarquia é **faixa 440 contra card 360**. A lista, não: ela acompanha a
faixa. Foi correção explícita do Lucas — lista mais estreita que o título deixa "um espaço em
branco do lado direito muito grande".

### Espaçamentos verticais

| Entre | Valor |
|---|---|
| Faixa → o que vem abaixo dela | **15** renderizado (10 declarado no post-it) |
| Card → card empilhado | **30** |
| Base do card do nó → faixa "O que faz" | **42** |
| **Fim da lista → a linha do fluxo** | **20** |
| **Linha do fluxo → faixa "Observações"** | **20** |

Os 20px são **da linha**, não do bloco. Erro cometido: afastar a lista do título e deixar ela
descer em cima da linha e do título de baixo.

### Cores e formas dos recipientes

| Recipiente | Estilo |
|---|---|
| Faixa de seção | `fill="#EDEDED"`, texto `#6E6E6E`, 13px |
| Faixa da linha ("sai do X · entra no Y") | `fill="#D0D0D0"`, texto `#333333`, 13px — cinza mais escuro para separar |
| Post-it "o que faz" | sticky `data-color="yellow"`, 360×234 |
| Card de observação | `<rect rx="16" fill="#F5F5F5">`, texto `#1a1a1a`, 13px, 360×180 |
| Ponto de junção | `<circle r="5" fill="#000000">` |

**Amarelo significa "explicação do nó" e nada mais.** Observação em card cinza.

### A geometria da ramificação

```
coluna de dobra da saída        coluna de dobra da entrada
        x = Xs                          x = Xe
          ●─────────────────────────────●          y do ramo de cima
          │                             │
  ──●─────┤                             ├─────●──  y da linha principal
          │                             │
          ●─────────────────────────────●          y do ramo de baixo
```

- Cada `●` é um `<circle r="5">`; os conectores ligam ponto a ponto, sempre no mesmo `x` ou no
  mesmo `y`.
- Distância entre ramos: **1800** (ex.: ramo de cima em y=1760, principal em 2600, baixo em 3560).
- Trecho horizontal do ramo: **≥ 1000**. Precisa caber o bloco de 440 centralizado com folga.

### Altura do bloco de explicação (medido no Fluxo Geral, 12/08)

**É este número que decide a altura dos ramos numa ramificação.** A conta:

```
altura = 42                      (base do card até a faixa "O que faz")
       + 26                      (a faixa)
       + 15                      (faixa → primeiro post-it)
       + n × 234                 (os post-its)
       + (n − 1) × 30            (o vão entre post-its)
       + 40                      (último post-it → faixa "Campos")
       + 26 + 15                 (a faixa e o respiro dela)
       + altura_da_lista         (automática: LEIA do board)
```

Valores reais medidos, para estimar antes de criar:

| Post-its | Lista | Altura do bloco | Exemplo no board |
|---|---|---|---|
| 2 | curta (112) | **~770** | 10 · Executar Fluxo Meeting |
| 2 | média (280–308) | **~950** | 9 · Executar Fluxo Aircall |
| 3 | longa (476–560) | **~1400** | 8 · Executar Fluxo WhatsApp · 18 · Gravar conversa |
| 5 | muito longa (896) | **~2100** | 13 · Fatiar por etapa do funil |

### Ramificação com N ramos: a altura de cada ramo é calculada, não copiada

Para dois ramos, 1800 de distância funcionou (1760 / 2600 / 3560). **Para três ramos com alturas
diferentes, número fixo quebra:** o bloco do nó de cima invade a linha do meio.

```
Yc (ramo de cima)  = LINE_Y − altura_do_bloco_do_no_de_cima − 200 de folga
Yb (ramo de baixo) = LINE_Y + altura_do_bloco_do_no_do_meio + 300 de folga
```

Medido no Fluxo Geral, com LINE_Y = 2600:

| Ramo | Nó | Bloco dele | y escolhido | Folga real até a próxima linha |
|---|---|---|---|---|
| cima | 8 · WhatsApp (3 post-its, lista 476) | 1396 | **1000** | 144 |
| meio | 9 · Aircall (2 post-its, lista 280) | 936 | **2600** | 304 |
| baixo | 10 · Meeting (2 post-its, lista 112) | 768 | **3900** | — |

**Por que os blocos de trecho não colidem com os blocos de explicação:** eles vivem em faixas
verticais diferentes de `x`. O bloco de explicação fica no **x do nó** (centrado entre as dobras);
os blocos de trecho ficam no **x das sobras**. Cada um desce o quanto precisar.

Colunas de dobra, medidas:

```
Xs (dobra de saída)   = borda direita do nó de origem + ~360
Xe (dobra de entrada) = borda esquerda do nó de destino − ~700
```

No Fluxo Geral: nó 7 termina em 7040 → **Xs = 7400**; nó 11 começa em 11400 → **Xe = 10700**.
Nós dos três ramos centrados entre elas: `(7400+10700)/2 = 9050` → card x = **8830**.
Blocos: sobra esquerda em **7895**, sobra direita em **9765**.

### O loop: os quatro corredores

| Corredor | y no Fluxo Geral | Como se escolhe |
|---|---|---|
| ramo `done` | 1760 | acima da linha, com folga do bloco do nó de destino |
| linha principal | 2600 | — |
| ramo `loop` (corpo) | 3560 | abaixo da linha |
| ramo da ponta terminal | 5000 | abaixo do corpo, com folga do bloco do nó do corpo |
| corredor de retorno | 7000 | **abaixo de TUDO**: fundo do bloco mais baixo (6540) + 460 |

Colunas: `pin` **17800** (entrada do loop, recebe duas linhas) · círculo `cx=18110 r=110` ·
`pout` **18800** (saída) · dobra do corpo **20700** · fim do corpo **23700**.

**A coluna do `pin` fica entre o bloco do trecho e o círculo:** bloco ocupa 17000–17440, `pin` em
17800, círculo começa em 18000. Apertar isso faz a linha de retorno atravessar o bloco.

### Centralização (a conta)

Para um nó cujo trecho de linha vai de `A` (dobra de origem) a `B` (dobra de destino):

```
centro_do_no   = (A + B) / 2          → card x = centro − 220
sobra_esquerda = de A até (card x)     → bloco x = (A + card_x)/2 − 220
sobra_direita  = de (card x + 440) a B → bloco x = (card_x + 440 + B)/2 − 220
```

Exemplo medido no board: A=2100, B=4700 → nó em 3400 (x=3180); bloco esquerdo centrado em 2640
(x=2420); bloco direito centrado em 4160 (x=3940). Conferido no print: bateu em cima.

---

## 1. Grade horizontal

| Parâmetro | Valor | Por quê |
|---|---|---|
| Largura do card do nó | **280** | cabe nome de nó do n8n em Roboto Mono 18 sem quebrar |
| Passo entre colunas (pitch) | **580** | 280 do card + 300 de vão |
| **Vão entre cards** | **300** | mínimo para o rótulo do conector não invadir os vizinhos |
| x da coluna i | **60 + i × 580** | 60, 640, 1220, 1800, 2380, 2960, 3540... |

O vão de 300 é o parâmetro mais importante desta tabela. Com 80 o rótulo do conector atropelou
dois cards e deixou o nome do nó ilegível.

---

## 2. Ritmo vertical (explicação ABAIXO do nó)

Fileira de nós com o **centro vertical em y = 620**:

| Elemento | y declarado | altura | ocupa |
|---|---|---|---|
| forma do nó | 580 | 80 | 580–660 |
| faixa "O que faz" | **740** | 26 | 740–766 |
| post-it | **776** | 130 | 776–906 (declarado) |
| faixa "Campos" | **936** | 26 | 936–962 |
| lista de campos | calculada | automática | topo em **972** |

### As três distâncias, e como calculá-las

**a) Base da forma mais alta da fileira → faixa: 42px.**
A fileira mistura alturas (retângulo 80, hexágono 120, losango 150, círculo 156). A faixa tem que
limpar a **mais alta**, não a média:

```
faixa1_y = (base da forma mais alta da fileira) + 42
```

No teste, a mais alta era o círculo (r=78, base em 698) → faixa em 740.

**b) Faixa → post-it: 10 declarado, 15 renderizado.**
O post-it **encolhe e se centraliza** dentro da caixa declarada, então os 10 do SVG aparecem como
15 na tela. Use 10 no SVG e confira 15 na medição.

**c) Faixa → lista de campos: 15 renderizado**, e exige cálculo (seção 5).

**A régua de ouro do espaçamento:** a distância da lista para a faixa dela tem que ser **igual** à
do post-it para a faixa dele. Medido: 15,2 (post-it) contra 15,3 e 15,8 (listas de 2 e 5 linhas).
Nunca escolha um valor novo "que pareça bom" — copie o que já existe no desenho.

---

## 3. Ritmo vertical espelhado (explicação ACIMA do nó)

Mesmos valores, ordem invertida, lido de baixo para cima:

```
lista de campos
faixa "Campos"
post-it
faixa "O que faz"
CARD DO NÓ          ← base do bloco
```

As distâncias são as mesmas da seção 2. **No fluxo de teste o bloco espelhado usou 14px onde a
regra pede 42** (post-it y=150, faixa y=294, card y=334): funcionou porque ali não havia forma alta
na mesma fileira, mas **não siga esse número** — siga a seção 2.

Quando usar: sempre que uma ramificação precisar do corredor de baixo. Ver a regra de ramificação
no `SKILL.md`.

---

## 4. Geometria por forma (valores testados)

| Nó | Declaração | Ocupa em y (centro 620) |
|---|---|---|
| Gatilho (pílula) | `<rect y="580" width="280" height="80" rx="40">` | 580–660 |
| Processa (retângulo) | `<rect y="580" width="280" height="80">` | 580–660 |
| Decide (losango) | `<rect y="545" width="300" height="150" data-shape="rhombus">` | 545–695 |
| Repete (círculo) | `<circle cy="620" r="78">` | 542–698 |
| Chama fora (hexágono) | `<rect y="560" width="280" height="120" data-shape="hexagon">` | 560–680 |
| Espera (elipse) | `<ellipse cy="620" rx="145" ry="58">` | 562–678 |
| Encerra (canto forte) | `<rect y="580" width="280" height="80" rx="16">` | 580–660 |

**Losango e círculo precisam ser maiores que o retângulo** para o texto caber: o losango foi de
280×120 para **300×150** e o círculo de r=60 para **r=78** justamente porque o texto ficou
espremido na primeira rodada. Mesmo assim, texto dentro deles é de 2 a 4 palavras.

---

## 5. Lista de campos: o cálculo em duas passadas

O `y` de um `<textArea>` é **âncora de centro**, não de topo, e a altura é automática. Medido:

```
topo_real = y_enviado − altura/2 + 12       (escrita)
y_enviar  = topo_desejado + altura/2 − 12   (a inversa, que é a que se usa)
```

**Validado em massa em 12/08:** 17 listas de trecho corrigidas de uma vez ficaram com **0 a 1px** de
desvio do topo pretendido, contra desvios de até 310px antes. Truque para validar a fórmula de
graça: inclua no lote listas que **já estavam certas** — se elas não se movem, a fórmula está certa.

Os dois topos, por tipo de bloco:

| Bloco | Topo desejado |
|---|---|
| lista de trecho (acima da linha) | `linha_y − 20 − altura` |
| lista de campos (abaixo da faixa) | `faixa_y + 41` |
| lista de campos no **bloco espelhado** | `faixa_y − 15 − altura` ← a conta inverte |

| altura da caixa | topo real com y=1020 |
|---|---|
| 40 | 1012 |
| 59 | 1002,5 |
| 79 | 992,5 |
| 98 | 983 |

Por isso `y` fixo em listas de tamanhos diferentes produz topos diferentes (variação de 29px no
teste). **O procedimento correto:**

1. criar com um `y` aproximado qualquer;
2. `canvas_read_as_svg` e anotar a **altura real** de cada lista;
3. reenviar com

```
y = 972 + altura/2 − 12
```

Resultado: sete listas de 2 a 5 linhas com topo entre 1001 e 1002 — **1px de variação**.

Outros parâmetros da lista:

| Parâmetro | Valor |
|---|---|
| x | x_da_coluna + 10 |
| width | **260** (contra 280 do card) |
| font-size | 14 |
| altura de linha efetiva | ~19,75px por linha |
| separador de linha | `<br/>` — nunca vários elementos |

---

## 6. Post-it

| Parâmetro | Valor |
|---|---|
| Caixa declarada | **200 × 130** |
| x | x_da_coluna + **40** (recuado: mais estreito que o card, de propósito) |
| Cor | `data-color="yellow"` (nome, nunca hex) |
| Texto | `data-content`, uma ideia por post-it |

Proporção travada pelo board: a caixa 200×130 tem razão 1,54, que cai no post-it **largo**
(350:228 = 1,535). Para post-it quadrado, use `altura = largura × 1,15`. **Nunca declare caixa
achatada** (ex.: 610×130) — o post-it encolhe para o lado menor e sai muito mais estreito.

---

## 7. Faixa de rótulo

| Parâmetro | Valor |
|---|---|
| Tamanho | **largura do card × 26** (280 × 26) |
| Fundo | `#EDEDED` |
| Texto | `data-content`, 13px, `#6E6E6E` |
| Alinhamento | centralizado — `data-content` **sempre** centraliza, não há como alinhar à esquerda |

A faixa ocupa a **largura inteira** do card; o post-it e a lista, não. Esse desencontro é o que faz
uma ler como título e a outra como conteúdo.

---

## 8. Conector

```xml
<line x1="0" y1="0" x2="1" y2="1" stroke="#000000" stroke-width="2"
      data-start="<id origem>" data-end="<id destino>" data-arrow="end"
      data-content="N clientes" />
```

| Parâmetro | Valor / regra |
|---|---|
| `stroke-width` | 2 |
| `data-arrow` | `end` |
| `data-start` / `data-end` | **obrigatórios**, senão a linha não gruda |
| `data-content` | o que passa entre os nós, **até ~16 caracteres** |
| coordenadas | irrelevantes: com origem e destino, o Miro roteia sozinho |
| `data-shape="elbowed"` | **ignorado** — volta sempre como `straight` |

Rótulos que funcionaram no teste: `1 execucao vazia`, `N clientes`, `sim: 1 ou mais`, `1 cliente`,
`status + id`, `1 item`, `nao: vazio`.

---

## 9. Tipografia

| Onde | Fonte | Tamanho | Cor |
|---|---|---|---|
| Nome do nó | Roboto Mono | 18 (17 no hexágono, 15–16 em losango e círculo) | `#FFFFFF` |
| Faixa de rótulo | Roboto Mono | 13 | `#6E6E6E` |
| Lista de campos | Roboto Mono | 14 | `#333333` |
| Título da legenda | Roboto Mono | 26 | `#111111` |
| Item da legenda | Roboto Mono | 15 | `#444444` |
| Post-it | fonte do board (não declarar) | — | — |

Monoespaçada em tudo que é estrutura. O post-it fica com a fonte proporcional do próprio widget, e
esse contraste separa "estrutura" de "explicação humana" sem gastar mais nenhuma cor.

---

## 10. Legenda

| Parâmetro | Valor |
|---|---|
| Quadradinho de cor | 24 × 24 |
| Rótulo | `<textArea>` em x_do_quadradinho + **34** |
| Passo entre itens | ≥ 220 (o suficiente para o rótulo caber numa linha só) |
| Largura do rótulo | dimensionada para **caber numa linha** |

Larguras que funcionaram: "Gatilho" 100 · "Banco de dados" 160 · "Logica de controle" 200 ·
"Servico externo" 170 · "Registro e saida" 180 · título "Legenda" 200.

**Cuidado:** largura apertada quebra no meio da palavra. No teste "Legenda" virou "Legend / a" e
"Gatilho" virou "Gatilh / o". Ao mover um rótulo, **restate a `width`**.

---

## 11. Paleta do teste (5 categorias)

| Categoria | Hex |
|---|---|
| Gatilho | `#6C5CE7` |
| Banco de dados | `#2D9BF0` |
| Lógica de controle | `#F2A33C` |
| Serviço externo | `#00B86B` |
| Registro e saída | `#DA0063` |

Teto de 6 a 8 cores. Post-it é sempre amarelo, em qualquer categoria.

---

## 12. Frame

| Parâmetro | Valor do teste |
|---|---|
| Tamanho | 3900 × 1200 para 8 nós em 7 colunas |
| Fundo | `#FFFFFF` |
| Legenda | topo esquerdo, y ≈ 30 (título) e 82 (itens) |

Faltou espaço? **Cresça o frame** e reposicione. Canvas é infinito; aperto nunca justifica sobrepor.

---

## 13. Ordem de criação no SVG (importa)

Profundidade no Miro é **ordem de criação**: quem nasce primeiro fica atrás.

```
1. <rect data-type="frame">     (primeiro filho do <g>, obrigatório)
2. legenda
3. CONECTORES                   ← antes das formas, senão a linha fica em cima e tapa o card
4. formas dos nós
5. faixas
6. post-its
7. listas de campos
```

Referência para frente funciona: o conector pode citar em `data-start` o `id` de uma forma
declarada depois dele.

---

## 14. Envelope obrigatório para editar filho de frame

```xml
<g data-miro-id="<id do frame>" transform="translate(0,0)" data-frame="Titulo do frame">
  <rect data-type="frame" x="0" y="0" width="3900" height="1200" fill="#FFFFFF" data-title="Titulo do frame" />
  <!-- o elemento que você quer alterar -->
</g>
```

Sem o `data-frame` **e** o `<rect data-type="frame">`, mover um filho falha com
*"Attempted to move a widget relative to canvas, while it has a parent"*.

E lembre: **geometria é uma unidade** — para mover ou redimensionar, restate `x`, `y`, `width` e
`height` juntos. Bbox parcial é ignorado como ambíguo.
