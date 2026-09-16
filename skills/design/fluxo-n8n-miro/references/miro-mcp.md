# Miro MCP na prática — o que funciona, o que o board recusa

> Extraído da especificação oficial do canvas-composer (`canvas_get_canvas_composer_skill`).
> Aqui só está o que importa para desenhar fluxo. Para a spec completa, chamar a própria
> ferramenta.

---

## As duas ferramentas

| Momento | Ferramenta |
|---|---|
| Primeira vez | `canvas_create_from_svg` |
| Toda iteração depois | `canvas_update_from_svg` |

Ambas devolvem um `result_svg` com `data-miro-id` carimbado em cada elemento.
**Sempre iterar a partir do último `result_svg`**, editando no lugar. Nunca regerar do zero e
nunca inventar ou transcrever `data-miro-id` de memória: id que não existe no board vira falha
daquele elemento, não duplicata.

---

## As 6 armadilhas que quebram o desenho

### 1. Texto em cima de forma é DESCARTADO

> *"NEVER place `<text>`/`<textArea>` on top of a shape/sticky — text overlapping shapes is discarded."*

O texto simplesmente **some**. Não é aviso de estilo, é o board recusando.

```xml
<!-- ERRADO: o texto desaparece -->
<rect id="n1" x="0" y="0" width="200" height="80" fill="#5B9CCB"/>
<text x="100" y="45" text-anchor="middle">Buscar conversas</text>

<!-- CERTO: o texto vive na forma e centraliza sozinho -->
<rect id="n1" x="0" y="0" width="200" height="80" fill="#5B9CCB"
      data-content="Buscar conversas" data-font-size="16"
      data-font-family="Roboto Mono" data-text-color="#FFFFFF"/>
```

Regra prática: **forma que É o conteúdo usa `data-content`.** Só use `<text>` solto quando a
forma for fundo e o texto precisar de posição livre — o que, no nosso padrão, quase nunca acontece.

### 2. Ordem de criação é profundidade

> *"Z-INDEX IS DETERMINED BY CREATION ORDER."*

Quem nasce primeiro fica atrás. **Escreva as `<line>` ANTES das formas**, senão a linha passa por
cima do card e tapa. Essa é a causa silenciosa da maior parte da sobreposição.

### 3. Conector sem `data-start`/`data-end` não conecta

> *"EVERY `<line>` MUST have data-start and data-end attributes. This is a hard requirement."*

Sem isso a linha até aparece, mas não gruda: mover o card quebra o desenho. Referencie o `id`
local dos widgets, nunca frames nem outros conectores.

### 4. Post-it tem proporção travada

Quadrado renderiza em 199:228, largo em 350:228. O post-it é **encolhido para caber** na caixa
que você desenhou. Caixa achatada (ex.: 610x130) gera post-it muito menor que o esperado.

- quadrado: `height = width * 1.15` (ex.: 199x228)
- largo: `height = width * 0.65` (ex.: 350x228)

Cor por **nome**, não hex: `gray, light_yellow, yellow, orange, light_green, green, dark_green,
cyan, light_pink, pink, violet, red, light_blue, blue, dark_blue`.

### 5. `&`, `<` e `>` sem escape derrubam o SVG inteiro

> *"A raw & is the most common cause of a failed request."*

Nada é criado, nem a parte certa. `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`. Vale em atributo,
título, `data-content` e corpo.

### 6. Dimensão estimada muda, e aí sobrepõe

Alguns widgets crescem sozinhos. A resposta reporta quais mudaram de tamanho.
**Obrigatório:** ao receber esse aviso, conferir no `result_svg` e reposicionar com
`canvas_update_from_svg` antes de dizer que terminou.

---

## Peças, com o comando pronto

### Forma com texto centralizado (o card do nó)

```xml
<rect id="n1" x="0" y="0" width="240" height="70" rx="8" fill="#5B9CCB" stroke="none"
      data-content="Webhook WhatsApp" data-font-size="16"
      data-font-family="Roboto Mono" data-text-color="#FFFFFF"/>
```

`rx` é raio exato em px e não escala: `rx="8"` é canto suave em qualquer tamanho, `rx="62"` vira
pílula. Omita para canto reto. **Mínimo de 8px nos dois eixos** em qualquer forma.

### Faixa cinza de rótulo

```xml
<rect id="f1" x="0" y="76" width="240" height="26" fill="#EDEDED" stroke="none"
      data-content="O que faz" data-font-size="12"
      data-font-family="Roboto Mono" data-text-color="#6E6E6E"/>
```

### Post-it de explicação

```xml
<rect data-type="sticky" x="30" y="112" width="180" height="207"
      data-color="yellow" data-content="Recebe a mensagem crua do WhatsApp e dispara o fluxo."/>
```

### Bloco de campos (texto que flui e quebra)

`<textArea>` é o primitivo de parágrafo: quebra sozinho dentro da largura e vira **um** widget.
Um bloco lógico = um `<textArea>`. Quebra de linha explícita é `<br/>`; quebrar em vários
elementos está errado.

```xml
<textArea x="260" y="112" width="320" font-size="13" font-family="Roboto Mono"
          fill="#333333" text-align="left"><b>Campos</b><br/>1. HTTP Method = POST<br/>2. Path = /whatsapp<br/>3. Response = Immediately</textArea>
```

### Conector, com o rótulo do que passa

```xml
<line x1="120" y1="330" x2="120" y2="420" stroke="#000000" stroke-width="2"
      data-start="n1" data-end="n2" data-arrow="end" data-shape="elbowed"
      data-content="1 item por conversa: id, telefone, texto"/>
```

- `data-content` no conector **é** o rótulo do que passa entre os nós. Nativo, não precisa de
  texto solto perto da linha.
- `data-shape`: `straight` (padrão), `curved`, `elbowed`. Use **elbowed** para o cotovelo
  ortogonal do padrão.
- `data-arrow`: `end`, `start`, `both`, ou omitir.
- **Nunca desenhe ponta de seta à mão** com `<polygon>` ou `<path>`: a única forma é `data-arrow`.

### Frame

```xml
<g id="fr1" transform="translate(3000,2000)" data-frame="Fluxo Geral">
  <rect data-type="frame" x="0" y="0" width="1500" height="1000" fill="#FFFFFF" data-title="Fluxo Geral"/>
  <!-- filhos com coordenadas RELATIVAS ao frame -->
</g>
```

---

## Fontes disponíveis

Para o visual monoespaçado do padrão: **`Roboto Mono`** ou **`Plex Mono`**.
Também existem, entre outras: Arial, Georgia, Noto Sans, Open Sans, PT Sans, Roboto,
Roboto Condensed, Roboto Slab, Plex Sans, Plex Serif, Times New Roman.

⚠️ **Nome de fonte errado degrada em silêncio, igual forma (medido 13/08/2026).** Pedi
`ibm_plex_mono` — que é o nome do pacote, não o do board — e as 10 primeiras listas do quadro 02
voltaram em **`noto_sans`**: sem erro, sem `failed_items`, e o texto deixou de ser monoespaçado, o
que estraga o alinhamento de coluna da lista de campos. O nome aceito é **`Plex Mono`**.

**Regra:** conferir a fonte no read-back com o mesmo rigor com que se confere `data-shape`. As duas
falham do mesmo jeito — o board escolhe um substituto e não conta.

---

## Formas: use o NOME, não o polígono (testado em 11/08/2026)

`<rect>`, `<circle>`, `<ellipse>`, `<polygon>` são aceitos, mas **o `polygon` é uma aposta**: o
Miro tenta reconhecer a geometria e mapear para uma forma nativa dele. Quando não reconhece,
**degrada para retângulo em silêncio** — sem erro, sem aviso, sem entrar em `failed_items`.

Medido no board de teste:

| O que enviei | O que virou |
|---|---|
| `<polygon>` de 4 pontos (losango) | **`<rect>` comum. O losango foi perdido.** |
| `<polygon>` de 6 pontos (hexágono) | `<rect data-shape="hexagon">` — reconhecido |

**A forma segura é declarar o nome:**

```xml
<rect id="n3" x="780" y="220" width="280" height="120" data-shape="rhombus"
      fill="#F2A33C" data-content="Achou alguem?"
      data-font-size="16" data-font-family="Roboto Mono" data-text-color="#FFFFFF"/>
```

Confirmados funcionando por teste: **`rhombus`** (losango) e **`hexagon`**. `circle` e `ellipse`
funcionam como elementos próprios. Outros nomes do catálogo do Miro (triangle, parallelogram,
trapezoid, pentagon, octagon, star, cloud, cross, can) **não foram testados** — testar antes de
usar em entrega, e conferir no read-back se o `data-shape` sobreviveu.

**Regra de ouro:** depois de criar, ler o board de volta com `canvas_read_as_svg` e conferir se a
forma que voltou é a que você pediu. Degradação silenciosa não aparece na resposta de criação.

Não existe `<path>` de contorno livre.

---

## Rótulo de conector fica EM CIMA da linha, centralizado (testado)

A spec diz que `data-content` põe uma legenda no conector. O que ela não diz: **o Miro centraliza
o rótulo no meio da linha e não desvia de nada.** Com vão de 80px entre dois nós, um rótulo de 24
caracteres transbordou por cima dos dois cards vizinhos e deixou o nome do nó ilegível.

Duas consequências práticas:

1. **Vão entre nós tem que caber o rótulo.** No teste, vão de **300px** com rótulo de até ~16
   caracteres ficou limpo. Vão de 80px com 24 caracteres atropelou tudo.
2. **Rótulo é curto por obrigação**, não por estilo: "N clientes", "1 cliente", "status + id",
   "sim: 1 ou mais". O detalhe longo vai no post-it, não na linha.

---

## Para mexer em filho de frame, o `<g>` precisa do envelope completo (testado)

Enviar um `<textArea>` com `data-miro-id` dentro de um `<g data-miro-id="<frame>">` **falha** se o
`<g>` não trouxer também `data-frame` e o `<rect data-type="frame">`:

```
Failed to update text: Attempted to move a widget relative to canvas,
while it has a parent WidgetId(...)
```

O envelope que funciona:

```xml
<g data-miro-id="3458764680605776807" transform="translate(0,0)" data-frame="Titulo do frame">
  <rect data-type="frame" x="0" y="0" width="3900" height="1200" fill="#FFFFFF" data-title="Titulo do frame" />
  <textArea data-miro-id="..." x="60" y="30" width="200" />
</g>
```

---

## O `y` do `<textArea>` é âncora de CENTRO, não de topo (medido)

Essa é a causa de todo desalinhamento de lista, e não está na spec. Mandei `y=1020` nas sete
listas de campos de uma vez. Onde cada uma foi parar:

| altura da caixa | topo real | desvio |
|---|---|---|
| 40 | 1012 | −8 |
| 59 | 1002,5 | −17,5 |
| 79 | 992,5 | −27,5 |
| 98 | 983 | −37 |

O desvio é exatamente **metade da altura**. A relação:

```
topo_real = y_enviado − altura/2 + 12
```

**Consequência prática:** `y` fixo em blocos de alturas diferentes produz topos diferentes. Como a
altura é automática (depende de quantas linhas o texto ocupa depois de quebrar), **não dá para
saber o `y` certo antes de criar**.

### E o `y` da LEITURA não é o mesmo `y` da ESCRITA (medido 12/08/2026)

Pior do que a âncora de centro: as duas direções não usam a mesma convenção, e isso invalida
qualquer correção feita só na calculadora. Dois elementos do mesmo board, na mesma rodada:

| elemento | `y` enviado | `y` devolvido pelo read-back | altura | o que aconteceu |
|---|---|---|---|---|
| lista A | 1138 | **1071,5** | 157 | devolveu o **topo real** (1138 − altura/2 + 12) |
| lista B | 2123 | **2124** | 73 | devolveu **o mesmo valor enviado** |

A diferença aparente: a lista A foi atualizada com **só `x`/`y`/`width`**; a lista B foi enviada
**completa, com `data-content` e fonte**. Não trate isso como regra confirmada — trate como aviso
de que **a semântica do `y` não é confiável o suficiente para calcular posição no papel**.

**O procedimento que funciona, e o único:** escrever → ler de volta → **medir a distância real** →
ajustar → ler de novo, até a folga bater. Duas passadas costumam bastar; uma nunca basta. E um
verificador de sobreposição que assuma a convenção errada **inventa defeito que não existe e
esconde o que existe** — foi o que aconteceu aqui: o mesmo board acusou 17 e depois 23
sobreposições, e os dois números estavam errados, cada um por uma suposição diferente de âncora.

**O jeito que funciona, em duas passadas:**

1. criar com um `y` qualquer aproximado;
2. ler o board (`canvas_read_as_svg`) e pegar a **altura real** de cada `<textArea>`;
3. recalcular e reenviar: `y = topo_desejado + altura/2 − 12`.

Com isso, sete listas de 2 a 5 linhas ficaram com o topo entre 1001 e 1002 — 1px de variação
contra 29px antes.

Ao mover um `<textArea>`, **restate a `width`** junto do `x`/`y`. Largura apertada quebra feio: no
teste "Legenda" virou "Legend / a" e "Gatilho" virou "Gatilh / o".

---

## Espaçamento canônico entre uma faixa e o bloco abaixo dela

**15px de board**, seja o bloco um post-it ou uma lista de campos. Medido nas duas situações:

| Distância | Medida |
|---|---|
| faixa "O que faz" → post-it | 15,2 |
| faixa "Campos" → lista de 2 linhas | 15,3 |
| faixa "Campos" → lista de 5 linhas | 15,8 |

A régua é essa: **a distância da lista para a faixa dela tem que ser a mesma da distância do
post-it para a faixa dele.** Não invente um valor "que parece bom" — copie o que já existe.

Cuidado com o post-it nessa conta: ele **encolhe e se centraliza** dentro da caixa declarada, então
a distância que você escreve no SVG não é a distância que aparece. Só a medição no render vale.

---

## Abrir o board no navegador exige link público

O navegador que a skill controla **não está logado no Miro**. URL comum de board devolve tela de
login; só o link de compartilhamento público funciona:

```
https://miro.com/app/board/<id>=/?share_link_id=<numero>&moveToWidget=<id do widget>
```

Como o Lucas gera: **Share** → "Anyone with the link" → **Can view** → **Copy link**.

Sem esse link, dá para criar e para ler a estrutura de volta, mas **não dá para ver o desenho** —
e nesta skill ver não é luxo, é o único jeito de pegar sobreposição, texto espremido e respiro
errado.

Mecânica da conferência:

| Passo | Detalhe |
|---|---|
| Navegar | `<link publico>&moveToWidget=<id>` |
| Esperar | **14 a 16 segundos** — o canvas não está pronto antes disso |
| Print | pode estourar o tempo na 1ª tentativa; **repetir**, não reinterpretar |
| Enquadramento | id do **frame** mostra o fluxo inteiro; id de widget pequeno dá zoom nele |

`file:` está bloqueado no navegador, então HTML local precisa ser servido por HTTP antes de
qualquer print (usei `python -m http.server` na reconstrução da referência).

---

## Como medir espaçamento no Miro sem se enganar

**Print de tela cheia não serve.** No enquadramento do frame inteiro (43%), a faixa de 26px do
board ocupa **4 pixels de tela**: qualquer medida ali é ruído de antialiasing. Medindo assim eu
reportei "36px de variação" onde a variação real era de 0,5px, e cheguei a calcular correções de
162px que teriam destruído o layout.

**O método confiável:**

1. Navegue para um widget de **tamanho conhecido** com `?moveToWidget=<id>`. O Miro dá zoom para
   enquadrá-lo — uma faixa de 280x26 rende ~599%.
2. Como todas as faixas têm o mesmo tamanho, **o zoom sai idêntico em qualquer coluna**, e as
   medidas ficam comparáveis entre si.
3. Calibre a escala pela espessura da faixa: `escala = espessura_em_pixels / 26`.
4. Só então meça a distância e divida pela escala.

Sem esses quatro passos, não afirme nada sobre espaçamento.

---

## Uma outra coisa que o board decide sozinho (testado)

**1. `data-shape="elbowed"` no conector não gruda.** Enviei na criação e reenviei numa atualização
explícita; nas duas vezes o read-back devolveu `data-shape="straight"`. As coordenadas `x1,y1,x2,y2`
também voltam como `0,0 → 1,1`: assim que o conector tem `data-start`/`data-end`, **o Miro assume o
roteamento inteiro** e ignora tanto o traçado quanto o formato pedido. Não gaste rodada tentando
forçar cotovelo; posicione bem os nós e deixe o roteador trabalhar.

**2. `stroke="#1a1a1a"` no read-back é valor de transporte, não borda de verdade.** Enviei
`stroke="none"` e a leitura devolveu `#1a1a1a` em toda forma — mas **no print não existe borda
visível nenhuma**. Ou seja: nesse campo o read-back não descreve o render. É um caso onde só o
print decide, e por isso o passo do `board_show` não é opcional.

Detalhe menor: `<text>` é normalizado para `<textArea>` na volta, o que é esperado e não quebra nada.

---

## O roteador escolhe a BORDA mais perto, e é isso que atropela card (medido 12/08/2026)

`data-start`/`data-end` entregam o traçado ao Miro, e ele liga **as duas bordas mais próximas**.
Consequência prática: um conector que desce para um destino mais abaixo **sai pela base do nó de
origem** e atravessa tudo o que estiver na mesma coluna, embaixo dele.

No MAPA isso custou três rodadas. A ligação `FLUXO WHATSAPP → tabela 4`:

| Tentativa | O que o roteador fez | Resultado |
|---|---|---|
| tabela 4 embaixo da coluna de tabelas | entrou pela **borda de cima** da tabela 4 | linha cruzou tabela 2 e tabela 3 |
| tabela 4 afastada para baixo | saiu pela **base** do hexágono | linha cruzou os hexágonos LIGAÇÕES e MEET |
| WhatsApp movido para o **fim** da pilha | saiu pela direita, desceu no corredor vazio | limpo |

**A regra que sai disso:** o nó com **mais de uma saída** vai para a ponta da pilha, onde os dois
corredores estão livres. Não tente vencer o roteador movendo o destino — mova **a origem** para um
lugar em que nenhuma rota plausível encontre card.

E ao escolher a posição, teste **as duas rotas plausíveis** (borda lateral e borda de topo do
destino) na conta. Se qualquer uma delas cruzar um card, a posição está errada.

## Conector para item que JÁ EXISTE: os dois endpoints precisam de alias local (medido 13/08/2026)

Consertar a diagonal do quadro 05 exigia criar dois conectores novos ligando itens que já estavam no
board. `data-start`/`data-end` referenciam **`id` local do mesmo documento** — e não existe `id`
local para quem já nasceu. Três tentativas falharam antes de achar o caminho:

| Tentativa | Resultado |
|---|---|
| `data-start="n2"` num documento novo, onde `n2` não está declarado | falha: id não encontrado |
| `data-start="m3458764680731239380"` (prefixo `m` + id do board) | falha |
| `data-start="https://miro.com/app/board/.../moveToWidget=..."` | falha |
| **declarar cada endpoint como stub com `id` local *e* `data-miro-id`, no mesmo documento** | **funcionou** |

```xml
<!-- os endpoints, redeclarados como stub só para ganhar alias local -->
<circle id="pdesc" data-miro-id="3458764680731239380" cx="2900" cy="2000" r="5" fill="#000000"/>
<rect   id="n2"    data-miro-id="3458764680730931401" x="2600" y="1940" width="440" height="120"/>

<!-- agora o conector enxerga os dois -->
<line x1="0" y1="0" x2="1" y2="1" stroke="#000000" stroke-width="2"
      data-start="n2" data-end="pdesc" data-arrow="end"/>
```

**Regra:** o `id` local é o único endereço que o conector entende. Item existente entra no documento
como stub carregando **os dois**: o `id` que o conector vai citar e o `data-miro-id` que diz ao board
que não é para criar de novo.

## O roteador desenha DIAGONAL quando os dois pontos estão em corredores diferentes (medido 13/08/2026)

Consequência direta de "o Miro assume o roteamento inteiro". No quadro 05, o nó 2 estava no corredor
`y=2000` e o loop no corredor `y=3600`. Liguei os dois direto, e o board traçou **uma diagonal
atravessando o quadro** — quebrando a lei de ramificação ortogonal.

O que torna isso perigoso não é o defeito, é a cegueira: **o verificador de sobreposição aprovou.**
Ele compara retângulos e um conector não tem retângulo. O defeito só apareceu no print.

```
ERRADO                              CERTO
                                    n2 ●────────────● pdesc      y = 2000
n2 ●                                                │
     ╲                                              │
       ╲                                            │
         ╲                                          ↓
           ● loop     y = 3600                      ● loop       y = 3600
```

**Regra mecânica, aplicada na geração e não na conferência:** varrer a lista de conectores e, para
todo par com `y_origem ≠ y_destino`, inserir ponto de junção no cotovelo. Sem exceção, sem olhar se
"ficou ok". Um `<circle r="5" fill="#000000">` no canto e dois conectores retos.

## Post-it existente só aceita update com o marcador de tipo no stub (medido 12/08/2026)

Ao mover 28 post-its já criados, declarei cada um como `<rect data-miro-id="..." x=... y=... />`.
**Os 17 da primeira leva falharam de uma vez**, todos com a mesma mensagem:

```
Failed to update _auto_sh_4: the board item is a sticky_note but the element is authored
as a shape; keep the type markers from the result_svg on a sparse stub
(data-type / data-widget-type / the tag)
```

Cards, faixas e listas da **mesma chamada** passaram — só os post-its quebraram. O contorno é uma
linha:

```xml
<rect data-type="sticky" data-miro-id="3458764680626053071" x="12640" y="2738" width="360" height="234" />
```

**Regra:** stub de elemento existente carrega o **tipo**, não só a geometria. Vale para qualquer
widget cujo tipo no board não seja `shape`.

## A semântica do `y` do `<textArea>`, resolvida (13/08/2026)

> ⚠️ **A fórmula que estava escrita aqui estava errada para o caso da criação, e custou as 24 listas
> do quadro 02.** O que segue é o resultado de medir as duas direções contra o render.

O `y` de um `<textArea>` tem **duas semânticas diferentes**, e é isso que fazia a regra parecer
instável:

| Como você autora o elemento | O que o `y` significa |
|---|---|
| **completo** (`x`, `y`, `width`, `font-size`, `font-family`, `fill`, `text-align`, conteúdo) | o `y` é o **TOPO** da caixa |
| **stub esparso** (só `data-miro-id`, `x`, `y`, `width`) | o `y` é tratado como **centro**: o board grava `topo = y − altura/2 + 12` |

**A prova, que não depende de olhar o render:** `board_list_items` devolve `position` com
`origin: "center"`. Numa caixa de `width=440` criada com `x=100`, ele devolve centro `x=320` — ou
seja, o `x` enviado é a borda esquerda. Por simetria o `y` é a borda de cima, e bate: `y=3375` com
`height=140` devolve centro `y=3445`.

**Na criação, portanto, mande o topo desejado e não faça conta nenhuma:**

```
lista de campos:    y = faixa_y + 26 + 15        (= faixa_y + 41)
lista de trecho:    y = linha_y − 20 − altura
bloco espelhado:    y = faixa_y − 15 − altura
```

A altura é previsível e não precisa ser lida do board (medido em 24 listas, desvio zero):

| Tipo | Fonte | px por linha | Máx. de caracteres por linha |
|---|---|---|---|
| lista de campos | `Plex Mono` 20 | **28** | 33 |
| lista de payload / trecho | `Roboto Mono` 14 | **19,7** | 50 |

Mantendo as linhas dentro do limite de caracteres, `altura = px_por_linha × número de linhas`, e o
board devolve exatamente esse número.

## `canvas_update_from_svg` NÃO MOVE `<textArea>` (medido 13/08/2026)

Este é o achado mais caro do dia, e ele muda o procedimento inteiro.

Mandei as 24 listas do quadro 02 para uma posição nova. A resposta:

```
"Applied diff: 0 created, 24 updated"   failed_items: []
```

e o `result_svg` devolveu o `y` novo em todas. **No board, nenhuma se moveu.** Para descartar erro de
medição, mandei uma delas 300px acima — 68 pixels de tela no zoom em que eu estava conferindo. O
print saiu **idêntico**.

O que se move por update: forma, faixa, post-it, card. O que **não** se move: `<textArea>`.

**Consequências práticas:**

1. **Acertar a posição da lista na criação.** Não existe segunda passada para lista.
2. O procedimento antigo de "criar com `y` aproximado, ler a altura, reposicionar" **não funciona**.
   Ele foi escrito quando eu ainda achava que o update movia.
3. Consertar lista mal posicionada exige `data-deleted="true"` no antigo **e criar um novo** — e
   apagar exige confirmação do dono antes.
4. O `y` que o read-back mostra depois de um update **não é onde a lista está**. Ele mostra o que
   você pediu, não o que o board fez. Para saber onde ela está de verdade: print.

## `canvas_read_as_svg` para em 500 elementos, em silêncio (medido 13/08/2026)

O board tinha 582 itens. O SVG devolvido trouxe **500**: 71 do frame 00, 289 do frame 01 e 140 do
frame 02 — que tem 178. **As 13 últimas listas do frame 02 simplesmente não vinham no SVG**, embora
existissem (`board_list_items` com `item_type=text` achou as 24).

O resultado disso é pior do que perder informação: **o verificador de sobreposição rodou em cima de
um conjunto incompleto e devolveu "0 sobreposições"** — justamente sem olhar os elementos que tinham
o defeito.

**Regra:** comparar `item_count` da resposta com o número de elementos que o SVG realmente traz. Se
não bater, o read-back está truncado e não serve para verificar nada. Em board grande, usar
`board_list_items` filtrado por frame e por tipo (ele pagina de verdade), ou verificar a geometria
**calculada** antes de enviar.

⚠️ **Cuidado com o bloco espelhado.** Um script que calcula `topo = faixa_y + 41` acerta o bloco
normal e **erra o espelhado**, onde a lista fica *acima* da faixa (`fim = faixa_y − 15`). Foi a
única sobreposição que sobrou da correção em massa.

## Redimensionar frame: cresce sempre, e às vezes NÃO encolhe de jeito nenhum (medido 12/08/2026)

Depois de mover todo o conteúdo para dentro de 24405 × 6151, tentei reduzir o frame de
25600 × 18000 para 25000 × 6500. Falhou. Tentei 25600 × 6600 (só a altura): falhou. Tentei
25600 × 12000, o dobro do necessário: **falhou também**, sempre com a mesma mensagem de "filho fora
dos limites" — mesmo com `board_list_items` e o read-back concordando que nada estava lá embaixo.

Não é o problema das duas passadas descrito abaixo: o resize foi enviado **sozinho**, sem mover
nada junto. O frame simplesmente recusou encolher.

**Consequência prática:** dimensione o frame **na criação**, com folga. Crescer é sempre seguro;
encolher pode ser impossível depois, e o preço é um vazio embaixo do quadro que só se resolve
recriando o frame.

## Redimensionar frame falha enquanto um filho está fora do novo tamanho (medido 12/08/2026)

```
Failed to update frame: child widget cannot be placed outside the bounds
of its parent with Id WidgetId(...) type Frame
```

O resize do frame é avaliado **contra as posições antigas dos filhos**, não as novas do mesmo SVG.
Então, no mesmo documento, encolher o frame e subir os filhos para dentro **falha**: na hora da
conta, os filhos ainda estão no lugar velho.

Duas saídas:

1. **Crescer sempre passa.** Aumentar o frame nunca deixa filho fora. Se for crescer e reposicionar,
   faça junto sem medo.
2. **Encolher exige duas passadas:** primeiro mova os filhos, depois, num segundo update, encolha o
   frame.

## Atualização de `<textArea>` pode falhar com `API error` — recriar resolve

Um `<textArea>` longo (≈1.400 caracteres, com `<b>` e e-mail no corpo) recusou o update com
`Failed to update text: API error`, três vezes, enquanto os vizinhos passaram. O elemento ficou na
posição antiga — e, como o resto tinha se movido, **virou sobreposição**, que só apareceu no print.

Contorno que funcionou: `data-deleted="true"` no antigo e **criar um novo** com o mesmo conteúdo.
Criação não tem esse problema. Lição maior: `failed_items` com 1 item é motivo para conferir o
print, não para seguir em frente.

## Apagar exige confirmação

Remover elemento do SVG **não** apaga do board — a atualização é aditiva. Apagar é
`data-deleted="true"` no elemento com seu `data-miro-id`, e a spec exige **confirmar com o dono
antes**, porque não tem desfazer por aqui.
