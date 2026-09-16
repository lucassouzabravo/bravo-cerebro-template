# Construção de DOCX consulting-grade — receita detalhada

Esta é a receita aprovada para produzir documentos longos Bravo em .docx. Todos os helpers descritos estão implementados em `scripts/bravo_doc_helpers.py`.

---

## 1. Setup inicial obrigatório

```python
from scripts.bravo_doc_helpers import (
    setup_document, insert_cover_image, open_content_section,
    attach_header, attach_footer,
    add_heading1, add_heading2, add_heading3,
    add_lead, add_body, add_bullet, add_numbered,
    add_callout, add_quote, add_bravo_table,
    add_code_block, add_kpi_strip, add_toc_entry,
    add_closing_colophon,
    BRAVO,
)
from scripts.build_cover import build_cover

# Caminhos dos assets desta skill
LOGO_WHITE  = '<skill_dir>/assets/logos/bravo-logo-branco-alpha.png'
LOGO_COLOR  = '<skill_dir>/assets/logos/bravo-logo-color-alpha.png'
COVER_PATH  = '/tmp/cover_final.png'

# 1) Gera capa PNG full-bleed
build_cover(
    out_path=COVER_PATH,
    eyebrow='RELATÓRIO  ·  Q2 2026',
    title_lines=['Título do', 'Documento'],
    subtitle_lines=['Subtítulo explicativo em uma ou duas linhas'],
    audience_lines=['Preparado para a Diretoria', 'Bravo  ·  Maio de 2026'],
    footer_lines=['Confidencial — Uso interno Bravo', 'Versão 1.0'],
    logo_white_alpha_path=LOGO_WHITE,
)

# 2) Cria documento + capa + nova section
doc, content_dxa, content_cm = setup_document()
insert_cover_image(doc, COVER_PATH)
section = open_content_section(doc)
attach_header(section, LOGO_COLOR, 'Título do Documento  ·  Bravo AI Operations',
              content_width_dxa=content_dxa, content_width_cm=content_cm)
attach_footer(section, 'Confidencial — Uso interno Bravo  ·  AI Operations',
              content_width_dxa=content_dxa, content_width_cm=content_cm)
```

Depois disso, vá adicionando seções com os helpers — a primeira chamada de `add_heading1(..., new_page=False)` cria o sumário executivo na página 2; as próximas (`new_page=True`) abrem capítulo em nova página.

---

## 2. Espinha editorial recomendada

```python
# ── SUMÁRIO EXECUTIVO ────────────────────────────────────────────
# (não usa add_heading1 — é página especial; usa parágrafo "eyebrow" + título)
p = doc.add_paragraph()
r = p.add_run('SUMÁRIO EXECUTIVO')
# (style_run em 10pt bold JACARTA — eyebrow discreto)

# Título grande "O que este material entrega" (mesmo style do H1)
# Depois: add_lead com o parágrafo de abertura
# Depois: add_kpi_strip(doc, [('5','Módulos'), ('3-4h','Leitura'), ('100%','Interno')])
# Depois: add_heading3 + lista de aprendizado
# Depois: add_callout(label='OBJETIVO', text='...', kind='objective')

# ── ÍNDICE ───────────────────────────────────────────────────────
add_heading1(doc, 'Índice', new_page=True)
add_toc_entry(doc, '1', 'Capítulo Um',
              subtitles=['1.1 Primeira seção', '1.2 Segunda seção'])
add_toc_entry(doc, '2', 'Capítulo Dois',
              subtitles=['2.1 Primeira seção'])

# ── CAPÍTULOS ────────────────────────────────────────────────────
add_heading1(doc, '1.  Capítulo Um', new_page=True)
add_lead(doc, 'Parágrafo de abertura do capítulo, em 12pt Purple Mid.')

add_heading2(doc, '1.1  Primeira seção')
add_body(doc, [('Texto corrido. Para destaque inline: ', {}),
               ('parte em bold', {'bold': True, 'color': BRAVO.PURPLE}),
               (' e parte normal.', {})])

add_heading2(doc, '1.2  Segunda seção')
add_bravo_table(doc,
    headers=['Coluna A', 'Coluna B', 'Coluna C'],
    rows=[
        ['Linha 1A', 'Linha 1B', 'Linha 1C'],
        ['Linha 2A', 'Linha 2B', 'Linha 2C'],
    ],
    col_widths_cm=[5.5, 5.5, 5.6],  # soma = 16.6 (content width)
    footer_caption='Tabela 1.  Descrição da tabela.',
    unit='(R$ MM)',
)

add_callout(doc, 'Regra prática', 'Conteúdo da regra…', kind='rule')

# ── FECHAMENTO ───────────────────────────────────────────────────
add_closing_colophon(doc, '— FIM DO DOCUMENTO —')
doc.save('saida.docx')
```

---

## 3. Larguras de coluna — atenção

Para A4 com margens de 2.2cm de cada lado, a largura útil é **16.6cm**.

Listas de larguras comuns:
- 1 coluna: `[16.6]`
- 2 colunas iguais: `[8.3, 8.3]`
- 3 colunas iguais: `[5.53, 5.53, 5.54]` (último ajusta arredondamento)
- 4 colunas para tabela de comparação: `[2.5, 4.7, 4.7, 4.7]`

`add_bravo_table` faz auto-ajuste de arredondamento se a soma for próxima da largura útil — mas é melhor já passar valores que somam exatamente.

---

## 4. Inline styling em parágrafos

```python
add_body(doc, [
    ('Você sabe que ', {}),
    ('quanto mais material está no contexto, ', {}),
    ('mais difícil fica localizar o que importa', {'bold': True, 'color': BRAVO.PURPLE}),
    ('. É como pedir para alguém achar uma frase específica.', {}),
])
```

Cada tupla é um run separado dentro do mesmo parágrafo. Atributos:
- `bold`, `italic` — booleanos
- `color` — `RGBColor` ou um dos `BRAVO.*`
- `size` — int em pt (default 11)

---

## 5. Quando usar cada tipo de bloco

| Bloco                  | Quando usar                                                                 |
|------------------------|------------------------------------------------------------------------------|
| `add_lead`             | Primeiro parágrafo de cada capítulo / sumário executivo                     |
| `add_body`             | Parágrafo de texto corrido com inline styling                               |
| `add_bullet`           | Lista não-ordenada de até 5 itens curtos                                    |
| `add_numbered`         | Passos sequenciais ou lista numerada                                        |
| `add_callout` info     | Chamada didática ("DICA", "OBJETIVO", "PRÓXIMO PASSO")                      |
| `add_callout` rule     | Regra prática que o leitor deve memorizar                                   |
| `add_callout` warn     | Atenção a uma armadilha ou exceção                                          |
| `add_callout` danger   | Bloqueador ou risco crítico                                                 |
| `add_quote`            | Frase-síntese, slogan operacional, citação que vira "frase de capítulo"     |
| `add_bravo_table`      | Comparação estruturada, dados tabulares, especificação                      |
| `add_code_block`       | Exemplo de prompt, snippet de input/output                                  |
| `add_kpi_strip`        | Sumário executivo, abertura de capítulo com 3-4 números fortes              |

**Densidade recomendada:** no máximo 1 callout a cada 1-3 páginas, no máximo 1 quote a cada 5-7 páginas. Senão vira PowerPoint.

---

## 6. Cabeçalhos de seção (H1, H2, H3) — regras

- `H1` sempre em nova página (parâmetro default `new_page=True`). Para sumário executivo, passe `new_page=False`.
- `H1` recebe borda inferior Purple automaticamente. Não tente customizar — está padronizado.
- `H2` tem 20pt antes / 8pt depois e `keep_with_next` para não ficar sozinho no fim da página.
- `H3` tem 14pt antes / 4pt depois e `keep_with_next` também.
- Numere capítulos no formato `1.  Texto` (dois espaços após o ponto — fica mais legível que `1. Texto`).
- Numere subseções no formato `1.1  Texto` (idem).

---

## 7. Validação obrigatória pós-build

```bash
# Roda checks programáticos
python scripts/validate_document.py saida.docx

# Converte para PDF
libreoffice --headless --convert-to pdf saida.docx

# Renderiza páginas como imagem para inspeção visual
pdftoppm -r 100 saida.pdf preview/p -png
```

Veja as imagens. Procure especificamente por:
- Bordas brancas na capa
- Logo com fundo opaco em qualquer lugar
- Texto saindo de células de tabela
- Heading órfão no fim de página (sem o parágrafo seguinte)
- Cabeçalho de tabela em verde/vermelho ou qualquer cor fora de Purple

Se algum problema aparecer, corrija no código e regenere. **Não entregue sem inspeção visual.**

---

## 8. Armadilhas conhecidas

**`WidthType.PERCENTAGE` quebra no Google Docs.** Sempre `DXA`. Helpers já forçam isso.

**`ShadingType.SOLID` gera fundo preto em algumas versões.** Sempre `CLEAR`. Helpers já forçam isso.

**Header/footer linkados à seção anterior fazem a página 2 perder os elementos.** Sempre `is_linked_to_previous = False` após criar nova section. Helpers já forçam isso.

**Logo JPEG renomeado como PNG gera retângulo opaco.** Use os arquivos `*-alpha.png` desta skill.

**Capa não cobre 100% da página quando feita como background colorido do parágrafo.** Use imagem A4 (1654×2339 px) com margens zero.

**Parágrafo justificado em PT-BR gera "rios" de espaço.** Sempre alinhamento à esquerda. (`add_body` já é left-aligned por padrão.)

**Texto e shape do Word não respeitam fonte fallback consistentemente.** Sempre force `rFonts` em ascii + hAnsi + cs + eastAsia. `style_run` já faz isso.

---

## 9. Smoke test mínimo

Antes de produzir um documento de verdade, rode um teste mínimo para garantir que o ambiente está OK:

```python
doc, dxa, cm = setup_document()
build_cover(out_path='/tmp/c.png', eyebrow='TESTE', title_lines=['T'],
            subtitle_lines=['s'], audience_lines=['a'], footer_lines=['f'],
            logo_white_alpha_path=LOGO_WHITE)
insert_cover_image(doc, '/tmp/c.png')
s = open_content_section(doc)
attach_header(s, LOGO_COLOR, 'Smoke', content_width_dxa=dxa, content_width_cm=cm)
attach_footer(s, 'Smoke', content_width_dxa=dxa, content_width_cm=cm)
add_heading1(doc, 'Teste', new_page=False)
add_lead(doc, 'Hello.')
doc.save('/tmp/smoke.docx')
```

Converta para PDF e olhe. Se as três páginas (capa, conteúdo) estão impecáveis no teste mínimo, o ambiente está pronto para o documento real.
