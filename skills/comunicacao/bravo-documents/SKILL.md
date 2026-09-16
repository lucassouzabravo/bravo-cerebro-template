---
name: bravo-documents
description: >-
  Construção de documentos longos consulting-grade Bravo em .docx, .pdf e Google Docs — relatórios, memos, white-papers, capacitação, propostas, contratos. Sempre emparelhada com bravo-brand-guidelines. Cobre capa full-bleed sem bordas brancas, header/footer com logo transparente, tabelas sem overflow, callouts on-brand (info, regra, atenção), code blocks, KPI strips, quotes, índice hierárquico. Helpers Python prontos (python-docx + Pillow) e checklist de validação via PDF. Ativar quando o usuário mencionar "documento", "relatório", "memo", "white-paper", "capacitação", "policy", ".docx", "Word", "PDF longo" ou pedir entrega documental profissional. Ativar mesmo sem "Bravo" explícito se for contexto corporativo da Bravo.
---

# Bravo Documents — Construção de documentos consulting-grade

Esta skill é o **manual de engenharia** para produzir documentos longos da Bravo em padrão consulting (McKinsey/BCG) com qualidade que sobrevive à leitura do CEO. Cobre .docx, .pdf e Google Docs.

**Pré-requisito:** esta skill SEMPRE roda emparelhada com `bravo-brand-guidelines`. Aquela define **o quê** (paleta, logo, fonte, voz da marca); esta define **o como** (estrutura editorial, helpers, armadilhas técnicas, validação).

---

## 1. Filosofia de construção

Três princípios não-negociáveis. Se algum deles for violado, o documento volta para refazer.

**Pyramid Principle.** Conclusão e mensagem principal vêm primeiro; dados e argumentos de suporte vêm depois. Sumário executivo na página 2, capítulos depois, anexos no fim. O leitor (CEO) consegue parar no sumário executivo e ainda ter tomado uma decisão informada.

**Sobriedade visual.** Documento longo Bravo é mais sóbrio que slide. Predominam Purple `#302D71` e Purple Mid `#453D84` sobre branco. Jacarta `#8062DE`, Amethyst e Viking entram só em destaques pontuais — capa, callouts, números de KPI. Gradientes só na capa. **Nunca** verde/vermelho como cor de cabeçalho de tabela (foi o erro do PDF antigo).

**Data-ink ratio (Tufte).** Cada elemento visual precisa carregar informação. Linhas de grade pesadas, sombras gratuitas, ícones decorativos: fora. Borda branca de 1pt entre células, padding generoso, hierarquia tipográfica resolvendo o resto.

---

## 2. Estrutura editorial padrão

Todo documento longo segue esta espinha:

```
CAPA (1 página, full-bleed, sem header/footer)
SUMÁRIO EXECUTIVO (1-2 páginas)
ÍNDICE (1 página)
CAPÍTULOS DE CONTEÚDO (n páginas, um capítulo por seção)
CONCLUSÕES E PRÓXIMOS PASSOS
ANEXOS (opcional)
```

Cada capítulo abre em nova página, com H1 + borda inferior Purple de 18pt-size (na verdade 18 oitavos de pt = 2.25pt visual). Subseções (H2) com 20pt de espaço antes, sem quebra de página. Sub-subseções (H3) com 14pt antes.

Verificação de entendimento ou "próximos passos" no fim de cada bloco é prática editorial padrão. Não decoração — força o leitor a checar se absorveu o material.

---

## 3. Paleta operacional (cópia direta de bravo-brand-guidelines, filtrada para documentos)

| Token | HEX | Onde usar em documento |
|---|---|---|
| Purple | `#302D71` | Títulos H1/H2, cabeçalho de tabela, números de KPI, borda inferior de heading |
| Purple Mid | `#453D84` | H3, texto secundário sobre branco, corpo de texto alternativo |
| Jacarta | `#8062DE` | Border-left de callout/quote, bullets, acentos pontuais, linha "Total" de tabela |
| Amethyst | `#AA6CC9` | Acento decorativo em capa apenas — não usar em corpo |
| Viking | `#5ECADA` | Letra "v" do logo (já vem no PNG) — não usar como cor de texto em documento |
| Light Pur | `#AA97EF` | Eyebrows discretos, "FIM DO BLOCO" |
| Lighter | `#C8BFF3` | Linhas separadoras finas de header/footer |
| BG Light | `#ECEAFA` | Zebra de tabela, fundo de callout info |
| Grey Dark | `#1A1A2E` | Corpo de texto principal |
| Grey Mid | `#666666` | Captions, footnotes, metadados, anotação de unidade |
| Purple Dark | `#201D49` | Topo do Gradient 1 (capa) |
| Purple Deep | `#3D359E` | Base do Gradient 1 (capa) |

Cores semânticas (positivo/neutro/negativo) só dentro de células de tabela ou pílulas. Nunca como cor de cabeçalho ou fundo de bloco. **Aprendizado do erro anterior:** o PDF antigo usava verde para "faz bem" e vermelho para "faz mal" como cabeçalhos de tabela — fora do brand book e visualmente agressivo. A versão final usa Purple em ambos os cabeçalhos; a oposição semântica vem do conteúdo.

---

## 4. Tipografia

Fonte única: **Montserrat**. Fallback estrutural em código: `'Montserrat', 'Inter', system-ui, -apple-system, Arial, sans-serif`.

Escala otimizada para A4 com margens 2.2cm:

| Elemento | Tamanho | Peso | Cor | Notas |
|---|---|---|---|---|
| Título de capa | 90pt (renderizado em PNG) | Bold | Branco | Composto via Pillow no PNG da capa |
| H1 (capítulo) | 24pt | Bold | Purple | Borda inferior Purple, sempre nova página |
| H2 (seção) | 16pt | Bold | Purple | 20pt antes, 8pt depois, keep_with_next |
| H3 (subseção) | 13pt | Bold | Purple Mid | 14pt antes, 4pt depois, keep_with_next |
| Lead (primeiro parágrafo) | 12pt | Regular | Purple Mid | Line-spacing 1.5 |
| Corpo | 11pt | Regular | Grey Dark | Line-spacing 1.5, alinhamento à esquerda — NUNCA justificado em PT-BR |
| Bullet | 11pt | Regular | Grey Dark | Marcador "•" Jacarta bold |
| Tabela — cabeçalho | 10.5pt | Bold | Branco sobre Purple | Centralizado vertical |
| Tabela — corpo | 10pt | Regular | Purple Mid | Padding 120/160 dxa |
| Tabela — total | 11pt | Bold | Branco sobre Jacarta | Opcional |
| Caption de tabela | 9pt | Italic | Grey Mid | "Tabela X. Descrição." centralizado |
| Code block | 9.5pt | Regular | Purple sobre `#F5F3FB` | Fonte Consolas, fundo lilás muito claro |
| Header (página 2+) | 9pt | Regular | Purple Mid | Logo à esquerda, título à direita |
| Footer | 8.5pt | Regular | Grey Mid | Classificação à esquerda, "Pág. X" à direita |

**Não justificar parágrafo em português.** Justificar gera "rios" de espaço entre palavras (palavras longas + acentuação) e arruína a leitura. Alinhamento à esquerda, sempre.

---

## 5. Capa: full-bleed sem bordas brancas

Este é o ponto que mais quebra na prática. O caminho que funciona:

**Não tente "pintar" a capa com Word.** Word não suporta gradiente de página confiável e os shapes flutuantes não cobrem margem. O que funciona é gerar a capa inteira como **um PNG A4 (210×297 mm)** via Pillow e inserir como imagem cobrindo a página com margens zero.

**Receita (implementada em `scripts/build_cover.py`):**

1. Criar imagem 1654×2339 px (A4 a 200 dpi).
2. Pintar gradiente vertical Purple Dark → Purple Deep linha-a-linha.
3. Sobrepor três círculos blurred (Amethyst, Jacarta, Viking translúcidos) com `GaussianBlur(80)` — quebram a chapadidão sem virar enfeite.
4. Compor o logo branco transparente no topo central (resized para ~380px de largura).
5. Compor o texto via `ImageFont.truetype` — Montserrat se disponível; senão DejaVu Sans (fallback aceitável; o documento Word usa Montserrat real).
6. Pillar de elementos: eyebrow em pill (CAPACITAÇÃO XYZ · BLOCO N), título em duas linhas, subtítulo, divisor curto Amethyst, autoria, rodapé.

**No DOCX:**

```python
# Primeira section: margens zero, página de capa como imagem A4 inteira
section = doc.sections[0]
section.top_margin = Cm(0); section.bottom_margin = Cm(0)
section.left_margin = Cm(0); section.right_margin = Cm(0)
section.header_distance = Cm(0); section.footer_distance = Cm(0)

# titlePg: desativa header/footer na primeira página
sectPr = section._sectPr
titlePg = OxmlElement('w:titlePg')
sectPr.append(titlePg)

# Imagem A4 inteira
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run()
r.add_picture('cover_full.png', width=Mm(210), height=Mm(297))

# Próxima section: margens normais, header/footer "vivos"
new_section = doc.add_section(WD_SECTION.NEW_PAGE)
new_section.top_margin = Cm(2.4); ...
new_section.header.is_linked_to_previous = False
new_section.footer.is_linked_to_previous = False
```

**A armadilha que peguei na versão errada:** tentei colocar gradiente como background colorido do parágrafo. Word respeita só metade da página. O caminho correto é margem zero + imagem A4.

---

## 6. Logo: a armadilha do "PNG" que é JPEG

Os arquivos `bravo-logo-color.png` e `bravo-logo-branco.png` em `bravo-brand-guidelines/assets/logos/` **são JPEG renomeados como .png** (verifique com `file`). JPEG não tem canal alfa — significa que aparecem com fundo sólido (preto na versão "branco", branco na versão "color") quando colocados sobre qualquer cor que não seja a do fundo embutido.

**Foi exatamente isso que gerou o "fundo preto atrás do logo" no PDF anterior.**

**Solução:** processar os JPEGs para criar PNGs com transparência real. Script em `scripts/fix_logo_transparency.py`. Os arquivos já processados estão em `assets/logos/`:

- `bravo-logo-color-alpha.png` — logo colorido com pixels pretos convertidos em alfa 0. Use sobre fundos claros (header de páginas internas).
- `bravo-logo-branco-alpha.png` — logo branco com pixels pretos convertidos em alfa 0 e demais forçados a branco puro. Use sobre fundos escuros (capa, slides dark).

**Regra operacional:** SEMPRE use os arquivos `*-alpha.png` desta skill, nunca os originais da bravo-brand-guidelines diretamente. Documentar isso na sua memória de projeto se necessário.

---

## 7. Header e footer

Header (a partir da página 2): tabela invisível de 2 colunas. Coluna esquerda (5cm): logo colorido alfa, altura 0.85cm. Coluna direita (11.6cm): título do documento + " · " + área (ex: "Fundamentos de IA Aplicada · Bravo AI Operations"), 9pt Purple Mid, alinhado à direita. Linha separadora `Lighter` de 4 oitavos de pt logo abaixo.

Footer: tabela invisível de 2 colunas. Esquerda (11cm): "Confidencial — Uso interno Bravo · AI Operations" 8.5pt Grey Mid. Direita (5.6cm): "Pág. " + field `PAGE`, alinhado à direita. Linha separadora `Lighter` em cima.

**Pontos técnicos:**

- A primeira section (capa) tem `titlePg` ativado para esconder header/footer.
- A segunda section (conteúdo) tem `is_linked_to_previous = False` em header e footer — senão ela herda os da capa e fica vazia.
- Field PAGE é construído com `fldChar begin` + `instrText ' PAGE '` + `fldChar end` (não use texto literal "X").

---

## 8. Tabelas: o ponto onde tudo desmorona se você não controlar largura

A versão anterior tinha texto saindo da célula. A regra que resolve:

**Sempre fixe largura na tabela inteira E em cada célula, ambas em DXA.**

`WidthType.PERCENTAGE` quebra no Google Docs. `tblLayout` precisa ser `fixed` (não `autofit`). `tblGrid` precisa listar cada coluna explicitamente, e os números devem somar exatamente à largura da tabela.

```python
# Largura útil em A4 com margens 2.2cm = 16.6cm = 9412 dxa
# (1cm ≈ 567 dxa)
content_width_cm = 16.6
content_width_dxa = int(content_width_cm * 567)

# Para tabela de 2 colunas iguais:
col_widths_cm = [8.3, 8.3]
dxa_widths = [int(w * 567) for w in col_widths_cm]

set_table_width(table, sum(dxa_widths))  # tblW + tblLayout fixed
# preenche tblGrid:
for w in dxa_widths:
    gc = OxmlElement('w:gridCol')
    gc.set(qn('w:w'), str(w))
    tblGrid.append(gc)
# E em cada célula:
cell.width = Cm(col_widths_cm[i])
```

**Cores e padding:**

- Cabeçalho: `set_cell_shading(c, "302D71")` + texto branco bold 10.5pt, centralizado vertical.
- Linha ímpar (zebra): `BG_LIGHT` `#ECEAFA`.
- Linha par: branco.
- Borda: branco de 6 oitavos de pt entre células (separa visualmente sem virar grade pesada).
- Padding interno: 120 dxa top/bottom, 160 dxa left/right (≈ 6pt × 8pt). Em cabeçalhos, 160 em todos os lados.
- Linha "Total" opcional: fundo Jacarta, texto branco bold.

**Caption:** `Tabela X. Descrição. (Fonte: ...)` em 9pt italic Grey Mid, centralizado, 10pt de space-after.

**Unit annotation:** se a tabela tem unidades, alinhamento à direita, 9pt italic Grey Mid, ANTES da tabela: `(R$ MM)`, `(%)`, `(EUR '000s)`.

---

## 9. Callouts (info / regra / atenção / crítico)

Padrão: tabela 1×1 com border-left grossa (36 oitavos de pt) na cor do acento, fundo na cor BG correspondente, padding interno 180/240 dxa.

| Kind | Fundo | Border-left + texto-acento | Label típico |
|---|---|---|---|
| `info` | `#ECEAFA` | Jacarta `#8062DE` | "DICA", "OBJETIVO", "PRÓXIMO PASSO" |
| `rule` | `#ECEAFA` | Jacarta `#8062DE` | "REGRA PRÁTICA" |
| `warn` | `#FFF8DD` | `#7A5F00` (mostarda) | "ATENÇÃO", "IMPORTANTE" |
| `danger` | `#F9E4E4` | `#9B1C1C` (vermelho escuro) | "CRÍTICO", "BLOQUEADOR" |
| `success` | `#E8F4E3` | `#2D6E1E` (verde escuro) | "OK", "APROVADO" |

Estrutura interna: primeira linha = label em maiúsculas 9pt bold na cor do acento. Linha seguinte = texto do callout 11pt Grey Dark, line-spacing 1.4.

**Quando usar:** com parcimônia. Um callout a cada 1-3 páginas, em momentos onde realmente queremos sinalizar "este parágrafo é não-negociável". Encher de callout vira slide PowerPoint.

---

## 10. Code blocks (prompts, snippets)

Tabela 1×1, fundo `#F5F3FB` (lilás quase branco), borda `#ECEAFA` de 6 oitavos de pt, padding 160/200 dxa. Fonte Consolas 9.5pt em Purple. Quebras de linha preservadas (uma `add_paragraph` por linha do snippet). Label opcional acima do bloco em 9pt bold Jacarta: `"EXEMPLO BRAVO · Contexto detalhado vs. vago"`.

Não use para código de produção (este é caso para repositório). Use para mostrar **prompt para o Claude** ou estrutura de input/output, no contexto deste material.

---

## 11. Quotes em destaque

Mesma estrutura de callout mas: fundo BRANCO, border-left Jacarta `#8062DE` de 36 oitavos. Texto entre aspas tipográficas 13pt italic Purple. Linha de autoria abaixo, 10pt Grey Mid, prefixo "— ".

Usar para frases-síntese que o leitor pode "tirar do documento" — slogan operacional, princípio editorial, regra de filtro.

---

## 12. KPI strip (no sumário executivo)

Tabela de 3-4 colunas, alturas iguais, fundo `BG_LIGHT`, borda superior Jacarta de 12 oitavos de pt (acento), demais bordas brancas. Conteúdo: número grande 28pt Bold Purple centralizado + label 9pt Purple Mid centralizado. Padding generoso (240 dxa top/bottom).

Útil no sumário executivo (e.g. "5 módulos · 3-4h leitura · 100% material interno") ou em abertura de capítulo de dados.

---

## 13. Listas

Bullets nativos via `LevelFormat.BULLET` se disponível; fallback manual usa parágrafo com `left_indent = Cm(0.6)`, `first_line_indent = Cm(-0.5)`, e run inicial `"•  "` em Jacarta bold.

Numeração: parágrafo com `left_indent = Cm(0.8)`, `first_line_indent = Cm(-0.8)`, run inicial `"1.  "` em Purple bold.

Máximo 3 níveis de profundidade. Se precisar de 4+, reestruture em subseções.

---

## 14. Workflow de construção

Toda vez que for produzir um documento longo Bravo, siga esta ordem:

1. **Defina a espinha editorial** em texto puro: títulos de capa, sumário executivo, índice, capítulos, conclusões.
2. **Garanta logos com transparência alfa** (`scripts/fix_logo_transparency.py` se for primeira vez no ambiente).
3. **Gere a capa PNG** com `scripts/build_cover.py` parametrizando título/subtítulo/eyebrow.
4. **Construa o DOCX** importando `scripts/bravo_doc_helpers.py` — chama `setup_document()`, monta capa via imagem, segunda section com header/footer, conteúdo por capítulo.
5. **Converta para PDF** via LibreOffice headless e renderize as páginas como imagem (`pdftoppm -r 100`) para verificação visual.
6. **Aplique o checklist** abaixo. Se algo falhar, corrija e regenere — não entregue half-baked.
7. **Entregue o .docx** (para edição futura) e opcionalmente o .pdf (para distribuição final).

---

## 15. Checklist de revisão pré-entrega (não pular)

- [ ] Capa cobre 100% da página: zero borda branca em qualquer lado.
- [ ] Logo da capa é nítido, branco puro, com pixels pretos transparentes (não retângulo preto).
- [ ] Header (página 2+) tem logo colorido sem fundo opaco.
- [ ] Footer tem paginação dinâmica (não "Pág. 2" hardcoded).
- [ ] Toda tabela tem largura igual à largura útil da página, sem texto cortado.
- [ ] Cabeçalho de tabela é Purple `#302D71` — nunca verde/vermelho ou outra cor.
- [ ] Zebra de tabela funciona (linhas pares com fundo `#ECEAFA`).
- [ ] Nenhum parágrafo está justificado (todos alinhamento à esquerda).
- [ ] H1 sempre em nova página, com borda inferior Purple.
- [ ] Caption de tabela existe e referencia a tabela (`Tabela X. ...`).
- [ ] Callouts usam paleta on-brand (sem verde/vermelho como fundo principal).
- [ ] Fonte declarada é Montserrat em todos os runs (verificar via `extract-text` ou inspeção do XML).
- [ ] Tom: tratamento por "você", sem "senhor(a)", sem "devedor", sem "inadimplente".
- [ ] Pyramid: leitor consegue parar no sumário executivo e ter conclusão.
- [ ] Renderização final via LibreOffice + `pdftoppm` foi inspecionada visualmente — não confie só no Word.

---

## 16. Formato-alvo: docx vs. pdf vs. gdocs

**docx — formato primário de produção.**

É onde o documento "vive" para edição. Toda iteração começa e termina aqui. Toda a lógica desta skill foi otimizada para construção via python-docx. Entregue sempre o .docx para que o destinatário consiga editar.

**pdf — formato de distribuição final.**

Exporte do .docx via LibreOffice headless (`libreoffice --headless --convert-to pdf doc.docx`) ou via Word/Acrobat. Configurações importantes:

- Embed de fontes: garantir Montserrat embedada (no Word: Options → Save → Embed fonts in the file). PDF sem fontes embedadas vira pesadelo em outros computadores.
- Bookmarks/structure: ative para PDF acessível.
- Não comprima imagens da capa abaixo de 200 dpi.

**gdocs — só quando o destinatário exige edição colaborativa em tempo real.**

Limitações conhecidas:

- Tabelas com `WidthType.PERCENTAGE` quebram — esta skill já força DXA.
- Numeração de página `PAGE` field renderiza, mas estilo pode ser perdido na conversão.
- Code blocks com Consolas viram fonte padrão se Consolas não estiver no Workspace do destinatário.

Para gdocs, exporte do .docx final pelo Drive (upload → "Converter para Google Docs") e revise o resultado. Não construa direto em gdocs — falta o nível de controle estrutural.

Especificidades adicionais por formato em `references/`:
- `references/docx-construction.md` — receitas python-docx detalhadas.
- `references/pdf-export.md` — fluxo de exportação e validação.
- `references/gdocs-conversion.md` — passos e armadilhas.

---

## 17. Referência rápida — onde está cada coisa

```
bravo-documents/
├── SKILL.md                          ← este arquivo
├── scripts/
│   ├── bravo_doc_helpers.py          ← módulo Python com TODOS os helpers
│   ├── build_cover.py                ← gera capa PNG full-bleed parametrizada
│   ├── fix_logo_transparency.py      ← converte JPEG-como-PNG dos logos em PNG-alfa real
│   └── validate_document.py          ← roda checklist automatizado pós-build
├── assets/
│   ├── logos/
│   │   ├── bravo-logo-color-alpha.png    ← USE este, não o original
│   │   └── bravo-logo-branco-alpha.png   ← USE este, não o original
│   └── templates/                    ← (futuro: templates de capa por tipo de doc)
└── references/
    ├── docx-construction.md
    ├── pdf-export.md
    └── gdocs-conversion.md
```

---

## 18. Lições aprendidas (memória da iteração que originou esta skill)

Em maio de 2026 produzimos uma primeira versão do documento "Fundamentos de IA Aplicada" para o CEO. Três erros graves:

1. **Capa com borda branca:** o gradiente foi aplicado como elemento dentro da página em vez de imagem A4 cheia. Word não pintou as margens. *Correção:* margens zero + PNG A4 inteiro.

2. **Logo com fundo preto:** os arquivos `.png` da skill bravo-brand-guidelines são JPEG renomeados, sem canal alfa. Compostos sobre fundo gradiente, o canal de cor "preto" do JPEG aparece como retângulo. *Correção:* processar os logos para gerar PNG com transparência alfa real antes de usar. Está em `scripts/fix_logo_transparency.py`.

3. **Tabelas com overflow e cabeçalho verde/vermelho:** sem `tblLayout fixed` e sem `tblGrid` explícito, o Word redimensiona colunas conforme conteúdo, e texto longo escapa. Além disso, foram usadas cores verdes/vermelhas em cabeçalho (estilo "FAZ BEM / FAZ MAL") que estão fora do brand book. *Correção:* fixar largura em DXA em três níveis (tabela, grid, célula), e usar Purple em todo cabeçalho — a oposição semântica vem do conteúdo, não da cor.

Esses três pontos devem ser memorizados. Se Claude for produzir um documento Bravo novo e não passar por essa skill, esses erros vão se repetir.

---

## 19. Como esta skill se relaciona com `bravo-brand-guidelines`

Bravo-brand-guidelines é a **referência de identidade** (paleta, logo, tipografia, voz, valores). Cobre todos os artefatos da empresa (slide, app, e-mail, HSM, doc, planilha, redes sociais).

Bravo-documents é a **engenharia de execução para documentos longos**. Aplica as regras da brand-guidelines + adiciona estrutura editorial, helpers de código, armadilhas técnicas conhecidas e validação.

Fluxo correto:

1. Ler `bravo-brand-guidelines/SKILL.md` para garantir identidade (cores, fonte, voz, tom).
2. Ler **este** SKILL.md para a estrutura e os helpers.
3. Ler `references/docx-construction.md` (ou pdf-export.md, gdocs-conversion.md) conforme o formato-alvo.
4. Executar.
5. Validar via checklist da seção 15 antes de entregar.

Se houver conflito entre as duas skills, **brand-guidelines tem precedência em decisões de identidade** (cor, fonte, voz) e **esta skill tem precedência em decisões de construção** (estrutura, código, validação).
