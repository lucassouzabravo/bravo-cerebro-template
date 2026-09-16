# Diagramas em SVG — padrão Bravo dark

Receitas prontas. Copie e adapte. Tudo em SVG inline, zero dependência externa.

## Setup — defs e helpers

```python
J="#8062de"; A="#aa6cc9"; V="#5ecada"          # jacarta, amethyst, viking
TH="#ffffff"; TM="#c8bff3"; TL="#6b6090"        # texto alto, médio, baixo
S2="#110e2c"; S3="#17143a"                       # superfícies
POS="#4ade80"; NEU="#fbbf24"; NEG="#f87171"     # semânticas
BD="rgba(128,98,222,.28)"

DEFS = f'''<defs>
<linearGradient id="gfun" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="{J}" stop-opacity=".55"/>
  <stop offset="100%" stop-color="{V}" stop-opacity=".45"/>
</linearGradient>
<linearGradient id="gsoft" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0%" stop-color="{J}" stop-opacity=".14"/>
  <stop offset="100%" stop-color="{V}" stop-opacity=".07"/>
</linearGradient>
<marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
  <path d="M0,0 L9,4.5 L0,9 z" fill="{A}"/>
</marker>
</defs>'''

def wrap(vb, body, mw="1000px"):
    return (f'<div class="fig"><svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'style="width:100%;max-width:{mw};height:auto;display:block;margin:0 auto">'
            f'{DEFS}{body}</svg></div>')

def txt(x, y, s, fill=TM, fs=12, w="500", anchor="start", ital=False):
    it = ' font-style="italic"' if ital else ''
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{fill}" font-size="{fs}" '
            f'font-weight="{w}" font-family="Montserrat,sans-serif"{it}>{s}</text>')
```

CSS do container:

```css
.fig{background:rgba(13,10,34,.5);border:1px solid var(--border);border-radius:16px;padding:22px;margin:6px 0 4px;overflow-x:auto}
.fig-lbl{display:inline-flex;align-items:center;gap:7px;font-size:10px;font-weight:800;letter-spacing:1.1px;text-transform:uppercase;color:var(--viking);margin-bottom:10px}
.fig-lbl::before{content:'';width:14px;height:1.5px;background:var(--viking);opacity:.6}
.fig-cap{font-size:12px;color:var(--text-lo);line-height:1.6;margin:10px 0 30px}
.fig-cap b{color:var(--text-md)}
```

---

## 1. Funil de verdade

Trapézios que afunilam, com anotação conectada por linha pontilhada à direita.

```python
cx = 300                                  # centro do funil
hw = [265, 228, 192, 156, 120, 86, 56]    # meias-larguras: n+1 pontos para n etapas
H, GAP = 66, 8
for i, (nome, sub, col) in enumerate(stages):
    y = 24 + i*(H+GAP)
    p = f"{cx-hw[i]},{y} {cx+hw[i]},{y} {cx+hw[i+1]},{y+H} {cx-hw[i+1]},{y+H}"
    o += f'<polygon points="{p}" fill="url(#gfun)" stroke="{col}" stroke-opacity=".55" stroke-width="1.5"/>'
    o += txt(cx, y+H/2-3, nome, TH, 13, "800", "middle")
    o += txt(cx, y+H/2+14, sub, TM, 10.5, "500", "middle")
    # anotação: linha pontilhada até a coluna da direita
    o += f'<line x1="{cx+hw[i+1]+6}" y1="{y+H/2}" x2="600" y2="{y+H/2}" stroke="{cor}" stroke-opacity=".35" stroke-dasharray="3 3"/>'
    o += f'<circle cx="600" cy="{y+H/2}" r="3" fill="{cor}"/>'
    o += txt(612, y+H/2+4, nota, cor, 11.5, "600")
```

Deixe o funil à esquerda (centro em ~300) e a coluna de anotação a partir de x=600, num viewBox de 1100 de largura.

## 2. Árvore hierárquica (3 níveis)

Colunas fixas por nível; conector em curva de Bézier; altura do pai calculada a partir dos filhos.

```python
X1,W1 = 24,172    # nível 1
X2,W2 = 232,244   # nível 2
X3    = 516       # nível 3 (texto, sem caixa)
RH, MINH = 32, 52 # altura de linha e altura mínima de caixa

# altura do pai = soma dos filhos + gaps + compensação de altura mínima
extra = sum(max(0, MINH - (len(f)*RH - 6)) for f in filhos_por_no)
bh = max(n_filhos*RH + (n_nos-1)*18 + 20 + extra, 78)

# conector em curva
o += (f'<path d="M{X1+W1} {cy_pai} C{X1+W1+30} {cy_pai}, {X2-30} {cy_filho}, {X2} {cy_filho}" '
      f'fill="none" stroke="{col}" stroke-opacity=".38" stroke-width="1.3"/>')
```

**Nome próprio + referência entre parênteses no mesmo texto** (o navegador calcula o espaçamento):

```python
o += (f'<text x="88" y="{y}" font-family="Montserrat,sans-serif">'
      f'<tspan fill="{col}" font-size="13" font-weight="800">{nome}</tspan>'
      f'<tspan fill="{TL}" font-size="10.5" font-weight="600" dx="8">({ref})</tspan></text>')
```

## 3. Caixas aninhadas (níveis de zoom)

Retângulos um dentro do outro, com recuo crescente. Comunica "isto acontece dentro daquilo" sem precisar de legenda.

```python
o += f'<rect x="16"  y="16"  width="968" height="316" rx="14" fill="url(#gsoft)" stroke="{J}" stroke-opacity=".5" stroke-width="1.6"/>'
o += f'<rect x="48"  y="86"  width="904" height="228" rx="12" fill="rgba(170,108,201,.06)" stroke="{A}" stroke-opacity=".5"/>'
o += f'<rect x="80"  y="154" width="840" height="142" rx="11" fill="rgba(94,202,218,.055)" stroke="{V}" stroke-opacity=".5"/>'
o += f'<rect x="104" y="216" width="792" height="62"  rx="9"  fill="rgba(248,113,113,.07)" stroke="{NEG}" stroke-dasharray="5 4"/>'
```

Use tracejado para o nível que é **dependência externa** — lê como "isto não é nosso".

## 4. Fluxo com loop de retorno

```python
# cadeia horizontal
o += f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{A}" stroke-width="1.6" marker-end="url(#ar)"/>'
o += txt((x1+x2)/2, y-9, verbo, A, 9.5, "800", "middle")   # verbo ACIMA da seta

# convergência de dois nós para um
o += f'<path d="M597 116 L597 142 L430 142 L430 168" fill="none" stroke="{NEU}" stroke-width="1.5" marker-end="url(#arn)"/>'

# loop de volta — sempre tracejado, para não competir com o caminho principal
o += f'<path d="M340 201 L110 201 L110 120" fill="none" stroke="{J}" stroke-width="1.4" stroke-dasharray="5 4" marker-end="url(#ar)"/>'
```

## 5. Cadeia com comportas (dependência sequencial)

Salas lado a lado, com barra entre elas: só passa fechando a anterior.

```python
W, GAP = 124, 13
xd = x + W + GAP/2
o += f'<line x1="{xd}" y1="52" x2="{xd}" y2="162" stroke="{NEU}" stroke-width="2.4" stroke-linecap="round"/>'
o += f'<circle cx="{xd}" cy="107" r="4.5" fill="{S3}" stroke="{NEU}" stroke-width="1.6"/>'
```

## 6. Ramificação (árvore que abre)

Posição vertical de cada ramo **calculada**, nunca fixada:

```python
ys, cur = [], TOP
for ramo in ramos:
    ys.append(cur)
    cur += len(ramo.folhas)*LH - 12 + BGAP
total = cur - BGAP
center = (TOP + total)/2        # o nó raiz fica no centro do conjunto
```

## 7. Raias horizontais (troca entre pessoas ou sistemas)

Uma faixa por ator, empilhadas; a mensagem cruza de uma faixa pra outra na horizontal. Use quando a
seção explica "quem manda o quê pra quem", não só "o que acontece depois".

```python
LANES = ["Cliente", "Vendedor", "Sistema"]
LH = 84                                   # altura de cada raia
for i, nome in enumerate(LANES):
    y = 30 + i*LH
    o += f'<rect x="16" y="{y}" width="968" height="{LH-8}" rx="10" fill="{S2}" stroke="{BD}"/>'
    o += txt(34, y+20, nome, TL, 10.5, "700")

# mensagem: seta diagonal de uma raia pra outra, rótulo no meio do traço
o += (f'<line x1="{x1}" y1="{y_origem}" x2="{x2}" y2="{y_destino}" '
      f'stroke="{A}" stroke-width="1.5" marker-end="url(#ar)"/>')
o += txt((x1+x2)/2, (y_origem+y_destino)/2 - 6, msg, A, 10.5, "600", "middle")
```

A ordem das raias segue quem inicia a troca (topo) até quem executa por baixo dos panos (base). Se
o volume de mensagens for grande, corte em duas figuras (visão geral + zoom de um trecho) em vez de
espremer texto.

## 8. Trilha de estados (status ao longo do tempo)

Pills conectadas numa linha, com desvio pra baixo nos estados de exceção — não sobrepõe o caminho
feliz com o caminho de erro.

```python
STATES = ["Criado", "Em análise", "Aprovado"]
EXC = {1: "Recusado"}                     # índice do estado de origem -> exceção
PW, GAP = 130, 46
for i, nome in enumerate(STATES):
    x = 24 + i*(PW+GAP)
    o += f'<rect x="{x}" y="40" width="{PW}" height="34" rx="17" fill="rgba(128,98,222,.12)" stroke="{J}" stroke-opacity=".45"/>'
    o += txt(x+PW/2, 61, nome, TH, 12, "700", "middle")
    if i < len(STATES)-1:
        o += f'<line x1="{x+PW}" y1="57" x2="{x+PW+GAP}" y2="57" stroke="{A}" stroke-width="1.5" marker-end="url(#ar)"/>'
    if i in EXC:
        o += f'<path d="M{x+PW/2},74 L{x+PW/2},110" stroke="{NEG}" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#ar)"/>'
        o += f'<rect x="{x-10}" y="114" width="{PW+20}" height="30" rx="15" fill="rgba(248,113,113,.10)" stroke="{NEG}" stroke-opacity=".45"/>'
        o += txt(x+PW/2, 133, EXC[i], NEG, 11, "700", "middle")
```

## 9. Passo numerado dentro da figura

Quando a figura explica ordem de execução, o número vai **na caixa**:

```python
o += f'<rect x="{x}" y="{y}" width="34" height="19" rx="9" fill="{col}" fill-opacity=".16" stroke="{col}" stroke-opacity=".45"/>'
o += txt(x+17, y+13.5, "2.1", col, 10, "800", "middle")
```

Um badge por caixa, canto superior esquerdo, com o rótulo do campo à direita dele.

## 10. Anatomia de um objeto único (callouts numerados)

Um card só, parado, com marcadores apontando pra campos específicos dele — diferente do "passo
numerado" acima (que é ordem numa cadeia). Aqui o número identifica uma **parte**, não uma
**sequência**. Use quando a seção dissecar algo ("os campos de um arquivo", "as partes de uma
tarefa") em vez de mostrar fluxo.

```python
CAMPOS = [("id", 64, "identificador único, nunca muda"),
          ("bloco", 118, "em que fase da metodologia isso vive")]
o += f'<rect x="40" y="30" width="500" height="260" rx="12" fill="{S2}" stroke="{BD}"/>'
for i, (nome, y, nota) in enumerate(CAMPOS):
    # marcador circular colado na borda esquerda do card
    o += f'<circle cx="40" cy="{y}" r="11" fill="{J}" fill-opacity=".18" stroke="{J}"/>'
    o += txt(40, y+4, str(i+1), J, 11, "800", "middle")
    # texto do campo, DENTRO do card
    o += txt(58, y+4, nome, TH, 13, "700")
    # linha pontilhada saindo do marcador até a nota, FORA do card (coluna direita)
    o += f'<line x1="51" y1="{y}" x2="560" y2="{y}" stroke="{A}" stroke-opacity=".3" stroke-dasharray="2 3"/>'
    o += txt(572, y+4, nota, TM, 11.5, "500")
```

O card mostra o objeto real (com valor de exemplo em cada campo, nunca abstrato); a coluna à
direita é só anotação, nunca duplica o que já está escrito dentro do card.

## 11. Mockup de arquivo ou código (metadado colorido)

Quando a seção explica "é assim que isto fica gravado" — um arquivo, um registro, um payload —
desenhe o arquivo de verdade, não uma lista de bullets descrevendo ele. Fonte monoespaçada, cores
por tipo de dado (mesma lógica de um editor com syntax highlight).

```python
o += f'<rect x="24" y="24" width="700" height="360" rx="12" fill="#0b0820" stroke="{J}" stroke-opacity=".4"/>'
o += txt(44, 48, "tarefas/levantar-contrato.md", V, 11, "700")       # "nome do arquivo"
o += f'<line x1="44" y1="58" x2="700" y2="58" stroke="{BD}"/>'
LINHAS = [("---", TL), ("id: tarefa-levantar-contrato", TM), ("bloco: contexto", NEU)]
for i, (texto, cor) in enumerate(LINHAS):
    o += (f'<text x="44" y="{80+i*18}" fill="{cor}" font-size="10.5" '
          f'font-family="Consolas,Menlo,monospace">{texto}</text>')
```

Cor por categoria de campo (ex.: identificador numa cor, metadado de local noutra) ajuda o olho a
separar "isto é estrutura" de "isto é conteúdo" sem precisar ler palavra por palavra.

## 12. Molde vazio × ficha preenchida

Comparação lado a lado da MESMA estrutura em dois estados — não é tabela (que compara campos
diferentes) nem card duplicado (que compara coisas diferentes). É a forma vazia à esquerda, o
exemplo real preenchido à direita, com uma seta curta ligando os dois.

```python
o += f'<rect x="24"  y="30" width="460" height="280" rx="12" fill="{S2}" stroke="{BD}" stroke-dasharray="4 3"/>'
o += txt(254, 20, "MOLDE (vazio)", TL, 10, "700", "middle")
o += f'<rect x="560" y="30" width="460" height="280" rx="12" fill="{S2}" stroke="{J}" stroke-opacity=".5"/>'
o += txt(790, 20, "FICHA (preenchida)", J, 10, "700", "middle")
o += f'<line x1="484" y1="170" x2="560" y2="170" stroke="{A}" stroke-width="1.4" marker-end="url(#ar)"/>'
```

O molde usa borda tracejada (é template, não é dado real); a ficha usa borda sólida na cor de
destaque. O mesmo campo ocupa a mesma posição y nos dois lados, pra ficar óbvio "isto virou aquilo".

---

## Checklist antes de entregar

- [ ] Cada seção que explica relação tem figura — não card com texto
- [ ] Cada figura tem rótulo em cima e legenda embaixo (como ler · ponto crítico)
- [ ] Cada figura tem exemplo real dentro dela, não abstração
- [ ] Se há ordem, os números estão dentro das caixas
- [ ] Servido por HTTP e visto figura por figura em screenshot
- [ ] `scrollWidth > clientWidth` é falso em 1280px **e** em 390px
- [ ] Nenhum texto encostando ou passando de borda
- [ ] Nenhuma caixa sobreposta a outra
