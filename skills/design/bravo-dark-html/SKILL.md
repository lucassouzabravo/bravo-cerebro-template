---
name: bravo-dark-html
description: >-
  Design system dark-theme Bravo para relatórios e reports HTML self-contained. Use sempre que precisar gerar um relatório, report ou dashboard HTML interno da AI Ops — incluindo o relatório mensal do RollOut IA (acompanhamento de projetos), qualquer apresentação de métricas, ou page HTML com tema escuro no padrão da Bravo. Trigger: palavras "relatório", "report", "dashboard", "dark Bravo", "HTML Bravo". Cobre tokens de cor (fundo #07051a, superfícies, bordas roxas), glassmorphism no header, ambient glow, tipografia Montserrat, logo com mix-blend-mode:screen, e biblioteca completa de componentes (KPI cards, manager cards, phase table, project cards, summary grid, next-delivery banner).
---

# Bravo Dark HTML — Design System

Sistema de design para reports e páginas HTML self-contained com tema escuro Bravo.
Inspirado no design wope.com adaptado para a identidade Bravo.
**Resultado entregue:** arquivo `.html` único, sem dependências externas além do Google Fonts.

---

## Referências

| Precisa criar… | Leia |
|---|---|
| HTML do zero (boilerplate + estrutura) | `references/boilerplate.md` |
| Componentes específicos (cards, tables, pills) | `references/componentes.md` |
| **Diagramas — a parte mais importante** | `references/visual.md` |

---

## 0. Regra zero — isto é um documento VISUAL

> Aprendizado de 2026-07-28: uma entrega deste padrão foi reprovada com *"muito texto, não tem formas nenhuma, são uns quadrados e pronto — eu pedi pra você desenhar um funil, quero ver literalmente um funil"*. O Lucas é altamente visual (ver `USER.md`). Card com texto dentro **não é** visualização.

Antes de escrever qualquer seção, responda: **qual é a relação que esta seção explica?** E desenhe essa relação.

| A seção explica… | Desenhe |
|---|---|
| Etapas que se estreitam, perda a cada passo | **Funil** — polígonos em SVG que afunilam de verdade |
| Hierarquia, o que contém o quê | **Árvore** com linhas de conexão, ou **caixas aninhadas** |
| Ordem, o que dispara o quê, loop | **Fluxo** com setas e marcador de seta |
| Níveis de zoom, detalhe dentro de detalhe | **Caixas literalmente dentro** umas das outras |
| Sequência com dependência entre etapas | **Cadeia com portas/comportas** entre as caixas |
| Ramificação por condição | **Árvore que abre** da esquerda para a direita |
| Empilhamento onde um nível sustenta o outro | **Andares** empilhados |
| Troca entre pessoas ou sistemas, quem manda o quê | **Raias horizontais** (uma linha por ator, setas entre elas) |
| Status de um item ao longo do tempo (ticket, aprovação) | **Trilha de estados** — pills conectadas em sequência, com desvio para os estados de exceção |
| Campos de UM objeto parado (não uma cadeia) | **Anatomia com callouts** — marcadores numerados apontando pra parte do card |
| Como algo fica gravado de verdade (arquivo, registro, payload) | **Mockup de arquivo/código** — fonte monoespaçada, cor por tipo de campo |
| A mesma estrutura vazia × preenchida com exemplo real | **Molde × ficha** — comparação lado a lado, molde tracejado |
| Comparação de campos exatos | Tabela — aqui tabela é certo |

Antes de desenhar qualquer fluxo, identifique por escrito: **gatilho, atores/sistemas envolvidos, decisões que mudam de caminho, e condição de término.** Depois confira cada seta contra a explicação original — não inventar sistema, permissão ou ação automática que ninguém descreveu. É o mesmo cuidado do fluxo do n8n no Miro, só que em SVG.

**Como fazer:** SVG inline, escrito à mão, em função Python que devolve string. **Não use Mermaid** — exige biblioteca externa e quebra o self-contained. E Mermaid não desenha funil.

**Regras de figura:**
- Toda figura tem **rótulo** em cima e **legenda** embaixo — a legenda diz *como ler*, o *ponto crítico*, e a *premissa* se houver.
- Toda figura carrega **exemplo real vivo dentro dela**, não abstração. Se a figura explica "tarefa", a caixa diz `levantar um contrato`, não `A TAREFA`.
- Se a explicação tem ordem de execução, **numere dentro da figura** (`2.1`, `2.2`) — o número na caixa é o que faz o leitor enxergar a sequência.
- Envolva a figura em container com `overflow-x:auto`, e o `<svg>` com `width:100%;max-width:Npx;height:auto`. A página nunca rola na horizontal.
- **Nunca estime largura de texto por número de caracteres** para posicionar rótulo ao lado de outro — use `<tspan dx="8">` e deixe o navegador calcular. Estimar colide.
- Caixa de uma linha precisa de **altura mínima**; senão o texto encosta na borda.
- Posição vertical de ramo com nº variável de filhos é **calculada**, nunca fixada — fixar sobrepõe.

**Valide sempre:** sirva por HTTP local, tire screenshot **de cada figura** (`.fig`) e olhe uma por uma. Confira `scrollWidth > clientWidth` em 1280px e em 390px. Texto estourando caixa e elemento sobreposto só aparecem no olho.

---

## 1. Fundamentos

### Google Fonts (única dependência externa)
```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

### Logo Bravo (isotipo colorido com fundo transparente)
O arquivo `bravo-iso-color.png` tem fundo **preto** (JPEG sem alpha). Para remover o fundo no tema escuro, use `mix-blend-mode: screen`.

```html
<!-- Header: height 36px -->
<img src="[DATA_URI_DO_JPEG]" alt="Bravo" style="height:36px;width:auto;mix-blend-mode:screen;">

<!-- Footer: height 28px, centralizado -->
<img src="[DATA_URI_DO_JPEG]" alt="Bravo" style="height:28px;width:auto;display:block;margin:0 auto 10px;mix-blend-mode:screen;">
```

Para embutir o logo como data URI (self-contained):
```powershell
$bytes = [System.IO.File]::ReadAllBytes("C:\Users\brass\.claude\skills\bravo-brand-guidelines\assets\logos\bravo-iso-color.png")
$b64 = [Convert]::ToBase64String($bytes)
$dataUri = "data:image/jpeg;base64,$b64"
```

---

## 2. Design Tokens — CSS Custom Properties

Cole no `:root` de todo HTML deste sistema:

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  /* ── Backgrounds (ultra-dark, camadas de profundidade) */
  --bg:          #07051a;   /* fundo da página */
  --surface-1:   #0d0a22;   /* surface nível 1 (não usado direto, reserva) */
  --surface-2:   #110e2c;   /* cards e painéis */
  --surface-3:   #17143a;   /* hover states, header de tabela, item ativo */

  /* ── Bordas (tintadas em Jacarta) */
  --border:      rgba(128, 98, 222, 0.14);   /* borda padrão */
  --border-md:   rgba(128, 98, 222, 0.28);   /* borda em hover */
  --border-hi:   rgba(128, 98, 222, 0.50);   /* borda de destaque */

  /* ── Paleta Bravo */
  --jacarta:     #8062de;   /* roxo primário — CTAs, destaques */
  --amethyst:    #aa6cc9;   /* roxo secundário — eyebrows, pills */
  --viking:      #5ecada;   /* turquesa — links, ferramentas, acento frio */

  /* ── Texto */
  --text-hi:     #ffffff;   /* título, dado principal */
  --text-md:     #c8bff3;   /* corpo, descrições */
  --text-lo:     #6b6090;   /* labels, muted, captions */

  /* ── Semânticas */
  --pos:         #4ade80;   /* positivo / concluído */
  --neu:         #fbbf24;   /* neutro / atenção / prazo */
  --neg:         #f87171;   /* negativo / urgente */

  /* ── Tipografia */
  --font: 'Montserrat', system-ui, -apple-system, sans-serif;
}

html { font-family: var(--font); -webkit-font-smoothing: antialiased; scroll-behavior: smooth; }
body  { background: var(--bg); color: var(--text-hi); min-height: 100vh; }
```

---

## 3. Efeito Ambient Glow

Gradientes radiais fixos no body — criam profundidade atmosférica sem poluir o conteúdo.

```css
body::before {
  content: ''; pointer-events: none; position: fixed; inset: 0; z-index: 0;
  background:
    radial-gradient(ellipse 800px 500px at 20% -10%, rgba(128,98,222,.10) 0%, transparent 70%),
    radial-gradient(ellipse 600px 400px at 80% 110%, rgba(94,202,218,.07) 0%, transparent 70%);
}
/* Todo conteúdo precisa de position: relative; z-index: 1 para ficar acima do glow */
.wrap { position: relative; z-index: 1; max-width: 1100px; margin: 0 auto; padding: 0 32px; }
```

**Regra:** o glow superior-esquerdo é sempre Jacarta (roxo); o inferior-direito é sempre Viking (teal). Não inverta.

---

## 4. Header Glassmorphism (sticky)

```css
.site-header {
  position: sticky; top: 0; z-index: 100;
  background: rgba(7, 5, 26, 0.80);   /* --bg com 80% opacidade */
  backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
}
.header-inner {
  max-width: 1100px; margin: 0 auto; padding: 14px 32px;
  display: flex; align-items: center; justify-content: space-between;
}
.logo-row { display: flex; align-items: center; gap: 12px; }
.logo-sep  { width: 1px; height: 18px; background: var(--border-md); }
.logo-sub  { font-size: 13px; color: var(--text-lo); font-weight: 500; }

/* Tags de status no canto direito */
.tag {
  font-size: 11px; font-weight: 600; letter-spacing: .8px; text-transform: uppercase;
  color: var(--text-lo); border: 1px solid var(--border); border-radius: 4px; padding: 3px 9px;
}
.tag-live { border-color: rgba(74,222,128,.3); color: var(--pos); }
.tag-live::before { content: '● '; font-size: 8px; }
```

```html
<header class="site-header">
  <div class="header-inner">
    <div class="logo-row">
      <img src="[DATA_URI]" alt="Bravo" style="height:36px;width:auto;mix-blend-mode:screen;">
      <div class="logo-sep"></div>
      <span class="logo-sub">AI Operations</span>
    </div>
    <div style="display:flex;gap:10px;align-items:center;">
      <span class="tag tag-live">Ativo</span>
      <span class="tag">Interno Confidencial</span>
    </div>
  </div>
</header>
```

---

## 5. Hero Section

```css
.hero { padding: 72px 0 56px; }

/* Eyebrow pill */
.eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(128,98,222,.08); border: 1px solid rgba(128,98,222,.25);
  color: var(--amethyst); font-size: 11px; font-weight: 700; letter-spacing: 1.5px;
  text-transform: uppercase; padding: 5px 14px; border-radius: 9999px; margin-bottom: 24px;
}
.eyebrow-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--viking); }

/* Título com gradiente */
.hero-title {
  font-size: clamp(36px, 4.5vw, 54px); font-weight: 800; line-height: 1.08;
  letter-spacing: -1.5px; margin-bottom: 18px;
}
.grad {
  background: linear-gradient(120deg, #e0d8ff 0%, var(--jacarta) 45%, var(--viking) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { font-size: 17px; color: var(--text-md); max-width: 560px; line-height: 1.65; margin-bottom: 52px; }
```

```html
<section class="hero">
  <div class="wrap">
    <div class="eyebrow">
      <span class="eyebrow-dot"></span>
      LABEL DA SEÇÃO
    </div>
    <h1 class="hero-title">Título Normal <span class="grad">Título Gradiente</span></h1>
    <p class="hero-sub">Subtítulo descritivo da página.</p>
    <!-- KPI Row vai aqui -->
  </div>
</section>
```

---

## 6. KPI Cards (grid de 4)

```css
.kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.kpi-card {
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: 14px; padding: 22px 24px; transition: border-color .2s, box-shadow .2s;
}
.kpi-card:hover { border-color: var(--border-md); box-shadow: 0 0 24px rgba(128,98,222,.15); }
.kpi-lbl  { font-size: 11px; font-weight: 600; letter-spacing: .8px; text-transform: uppercase; color: var(--text-lo); margin-bottom: 10px; }
.kpi-val  { font-size: 38px; font-weight: 800; line-height: 1; }
.kpi-hint { font-size: 12px; color: var(--text-lo); margin-top: 6px; }
/* Cores do valor */
.c-jacarta  { color: var(--jacarta);  }
.c-amethyst { color: var(--amethyst); }
.c-viking   { color: var(--viking);   }
.c-pos      { color: var(--pos);      }
```

```html
<div class="kpi-row">
  <div class="kpi-card">
    <div class="kpi-lbl">Label</div>
    <div class="kpi-val c-jacarta">42</div>
    <div class="kpi-hint">Descrição curta</div>
  </div>
  <!-- repita para os outros 3 -->
</div>
```

---

## 7. Section Shell (padrão de seção)

```css
.section     { padding: 72px 0; border-top: 1px solid var(--border); }
.sec-eyebrow { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-lo); margin-bottom: 8px; }
.sec-title   { font-size: 30px; font-weight: 800; letter-spacing: -.5px; margin-bottom: 8px; }
.sec-desc    { font-size: 15px; color: var(--text-md); max-width: 600px; line-height: 1.6; margin-bottom: 40px; }
```

---

## 8. Manager Cards (diagnóstico / perfis)

```css
.mgr-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.mgr-card {
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: 16px; padding: 28px; transition: all .2s;
}
.mgr-card:hover { border-color: var(--border-md); transform: translateY(-2px); box-shadow: 0 12px 32px rgba(128,98,222,.10); }
.mgr-name    { font-size: 19px; font-weight: 800; }
.mgr-role    { font-size: 12px; color: var(--jacarta); font-weight: 600; margin-top: 3px; }
.mgr-profile {
  font-size: 12px; color: var(--text-lo); background: var(--surface-3);
  border-radius: 8px; padding: 10px 14px; margin-bottom: 20px;
  border-left: 3px solid var(--jacarta); line-height: 1.55; font-style: italic;
}

/* Lista de dores */
.pain-list { list-style: none; display: flex; flex-direction: column; gap: 9px; }
.pain-item { display: grid; grid-template-columns: 1fr auto; align-items: start; gap: 10px; }
.pain-inner { display: flex; align-items: flex-start; gap: 9px; }
.pain-dot   { width: 5px; height: 5px; background: var(--amethyst); border-radius: 50%; margin-top: 6px; flex-shrink: 0; }
.pain-txt   { font-size: 13px; color: var(--text-md); line-height: 1.4; }

/* Frequency pills */
.freq-pill { font-size: 10px; font-weight: 700; letter-spacing: .3px; text-transform: uppercase; padding: 2px 8px; border-radius: 9999px; white-space: nowrap; margin-top: 2px; }
.f-d { background: rgba(248,113,113,.10); color: var(--neg);      }  /* Diária */
.f-s { background: rgba(251,191,36,.10);  color: var(--neu);      }  /* Semanal */
.f-m { background: rgba(74,222,128,.10);  color: var(--pos);      }  /* Mensal */
.f-c { background: rgba(170,108,201,.12); color: var(--amethyst); }  /* Crônica */
.f-p { background: rgba(94,202,218,.10);  color: var(--viking);   }  /* Pontual */
```

```html
<div class="mgr-grid">
  <div class="mgr-card">
    <div class="mgr-head">
      <div class="mgr-name">Nome</div>
      <div class="mgr-role">Cargo / Área</div>
    </div>
    <div class="mgr-profile">Perfil curto em itálico.</div>
    <ul class="pain-list">
      <li class="pain-item">
        <div class="pain-inner">
          <span class="pain-dot"></span>
          <span class="pain-txt">Descrição da dor</span>
        </div>
        <span class="freq-pill f-d">Diária</span>
      </li>
    </ul>
  </div>
</div>
```

---

## 9. Phase Table (trilha de treinamento)

```css
.phases-wrap { background: var(--surface-2); border: 1px solid var(--border); border-radius: 16px; overflow: hidden; }
.phases-header {
  display: grid; grid-template-columns: 44px 1fr 150px 120px 110px; gap: 16px;
  padding: 11px 24px; background: var(--surface-3);
  font-size: 11px; font-weight: 700; letter-spacing: .8px; text-transform: uppercase; color: var(--text-lo);
  border-bottom: 1px solid var(--border);
}
.phase-row {
  display: grid; grid-template-columns: 44px 1fr 150px 120px 110px; gap: 16px;
  align-items: center; padding: 15px 24px; border-bottom: 1px solid var(--border);
  transition: background .15s;
}
.phase-row:last-child { border-bottom: none; }
.phase-row:hover      { background: var(--surface-3); }
.phase-row.is-next    { background: rgba(128,98,222,.04); }

/* Número da fase */
.phase-num { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; background: var(--surface-3); color: var(--text-lo); border: 1px solid var(--border); }
.phase-num.n-done { background: rgba(74,222,128,.08);  color: var(--pos);    border-color: rgba(74,222,128,.25); }
.phase-num.n-next { background: rgba(128,98,222,.14);  color: var(--jacarta); border-color: rgba(128,98,222,.35); box-shadow: 0 0 12px rgba(128,98,222,.2); }
.phase-num.n-pill { background: rgba(94,202,218,.08);  color: var(--viking);  border-color: rgba(94,202,218,.25); }

.phase-name { font-size: 14px; font-weight: 700; color: var(--text-hi); }
.phase-sub  { font-size: 12px; color: var(--text-lo); margin-top: 2px; }
.phase-tool { font-size: 12px; color: var(--text-lo); }
.phase-week { font-size: 12px; color: var(--text-md); }

/* Status badges */
.phase-badge { display: inline-flex; align-items: center; font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 9999px; }
.pb-done     { background: rgba(74,222,128,.08);  color: var(--pos);    border: 1px solid rgba(74,222,128,.2); }
.pb-next     { background: rgba(128,98,222,.12);  color: var(--jacarta); border: 1px solid rgba(128,98,222,.3); }
.pb-pending  { background: var(--surface-3);      color: var(--text-lo); border: 1px solid var(--border); }
```

---

## 10. Project Cards (AI Hub / Kanban)

```css
.hub-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.proj-card {
  background: var(--surface-2); border: 1px solid var(--border); border-radius: 14px;
  padding: 22px; display: flex; flex-direction: column; gap: 12px; transition: all .2s;
}
.proj-card:hover        { border-color: var(--border-md); transform: translateY(-2px); box-shadow: 0 8px 28px rgba(128,98,222,.10); }
.proj-card.urgent       { border-color: rgba(251,191,36,.30); }
.proj-card.urgent:hover { box-shadow: 0 8px 28px rgba(251,191,36,.12); }
.proj-card.done         { opacity: .55; }

.proj-top    { display: flex; align-items: flex-start; justify-content: space-between; gap: 8px; }
.proj-name   { font-size: 14px; font-weight: 800; color: var(--text-hi); line-height: 1.3; }
.proj-area   { font-size: 10px; font-weight: 700; letter-spacing: .5px; text-transform: uppercase; color: var(--text-lo); background: var(--surface-3); border-radius: 4px; padding: 3px 8px; white-space: nowrap; }
.proj-desc   { font-size: 12px; color: var(--text-md); line-height: 1.55; flex: 1; }
.proj-footer { display: flex; align-items: center; justify-content: space-between; padding-top: 10px; border-top: 1px solid var(--border); }
.proj-owner  { font-size: 11px; color: var(--text-lo); }
.proj-dl     { font-size: 11px; font-weight: 700; }
.dl-ok       { color: var(--text-lo); }
.dl-warn     { color: var(--neu); }
.dl-done     { color: var(--pos); }

/* Status pills dos cards */
.s-new { background: rgba(128,98,222,.10); color: var(--amethyst); border: 1px solid rgba(128,98,222,.22); }
.s-dev { background: rgba(94,202,218,.09);  color: var(--viking);   border: 1px solid rgba(94,202,218,.25); }
.s-fin { background: rgba(74,222,128,.08);  color: var(--pos);      border: 1px solid rgba(74,222,128,.22); }
```

---

## 11. Summary Grid + Next-Delivery Banner

```css
/* Grid tabular de resumo */
.sum-grid {
  display: grid; grid-template-columns: repeat(5, 1fr); gap: 1px;
  background: var(--border); border: 1px solid var(--border); border-radius: 14px; overflow: hidden;
}
.sum-cell { background: var(--surface-2); padding: 22px 20px; }
.sum-lbl  { font-size: 10px; font-weight: 700; letter-spacing: .8px; text-transform: uppercase; color: var(--text-lo); margin-bottom: 8px; }
.sum-val  { font-size: 13px; color: var(--text-md); font-weight: 600; line-height: 1.4; }

/* Banner de próxima entrega */
.next-banner {
  background: linear-gradient(135deg, rgba(128,98,222,.10), rgba(94,202,218,.06));
  border: 1px solid rgba(128,98,222,.22); border-radius: 12px;
  padding: 18px 24px; margin-top: 24px;
  display: flex; align-items: center; justify-content: space-between; gap: 24px;
}
.next-inner { display: flex; flex-direction: column; gap: 3px; }
.next-lbl   { font-size: 10px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: var(--text-lo); }
.next-val   { font-size: 15px; font-weight: 700; color: var(--text-hi); }
.next-pill  {
  background: rgba(128,98,222,.15); color: var(--jacarta);
  border: 1px solid rgba(128,98,222,.30); border-radius: 9999px;
  font-size: 12px; font-weight: 700; padding: 5px 16px;
  box-shadow: 0 0 16px rgba(128,98,222,.18); white-space: nowrap;
}
/* Variante viking (teal) para outras entregas */
/* border-color: rgba(94,202,218,.25); background: rgba(94,202,218,.05); */
/* .next-lbl { color: var(--viking); } */
/* .next-pill { border-color: rgba(94,202,218,.4); color: var(--viking); } */
```

---

## 12. Alert Row e Cross-Cutting Box

```css
/* Alerta de prazo crítico */
.alert-row {
  background: rgba(251,191,36,.06); border: 1px solid rgba(251,191,36,.25); border-radius: 10px;
  padding: 14px 18px; margin-top: 20px;
  display: flex; align-items: center; gap: 10px;
  font-size: 13px; color: var(--neu); font-weight: 600;
}

/* Box de dores/temas transversais */
.cross-box {
  background: linear-gradient(135deg, rgba(128,98,222,.06), rgba(94,202,218,.04));
  border: 1px solid rgba(128,98,222,.20); border-radius: 14px; padding: 28px; margin-top: 28px;
}
.cross-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.cross-item { background: var(--surface-3); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; }
.cross-pain { font-size: 13px; color: var(--text-md); line-height: 1.4; margin-bottom: 8px; }
.cross-tool { font-size: 11px; font-weight: 600; color: var(--viking); background: rgba(94,202,218,.08); border-radius: 4px; padding: 2px 8px; display: inline-block; }
```

---

## 13. Site Footer

```css
.site-footer   { border-top: 1px solid var(--border); padding: 24px 0; text-align: center; }
.site-footer p { font-size: 12px; color: var(--text-lo); }
```

```html
<footer class="site-footer">
  <img src="[DATA_URI]" alt="Bravo" style="height:28px;width:auto;display:block;margin:0 auto 10px;mix-blend-mode:screen;">
  <p>Bravo AI Operations · Mês Ano · Interno Confidencial</p>
</footer>
```

---

## 14. Responsive (breakpoint 900px)

```css
@media (max-width: 900px) {
  .kpi-row       { grid-template-columns: repeat(2, 1fr); }
  .mgr-grid      { grid-template-columns: 1fr; }
  .hub-grid      { grid-template-columns: repeat(2, 1fr); }
  .cross-grid    { grid-template-columns: 1fr; }
  .outcome-strip { grid-template-columns: 1fr; }
  .sum-grid      { grid-template-columns: repeat(2, 1fr); }
  .phases-header { display: none; }
  .phase-row     { grid-template-columns: 44px 1fr; gap: 12px; }
}
```

---

## 15. Regras de Aplicação

**Sempre:**
- Fundo da página: `#07051a` (nunca preto puro)
- Cards: `var(--surface-2)` com borda `var(--border)` e `border-radius: 14px` ou `16px`
- Hover em cards: `translateY(-2px)` + `box-shadow` com alpha de Jacarta
- Bordas sempre tintadas em Jacarta — nunca cinza neutro
- Sombras sempre com matiz roxo: `rgba(128,98,222,…)` — nunca sombras pretas
- Spacing: múltiplos de 8px (8, 12, 16, 24, 32, 48, 64, 72)
- Fonte única: Montserrat, sem exceção

**Nunca:**
- Fundos completamente pretos (#000000)
- Sombras pretas (rgba(0,0,0,…))
- Gradientes fora dos aprovados
- Bordas sem tinta Jacarta ou Viking
- Cores fora da paleta Bravo

---

## 16. Decisões Rápidas

| Situação | Resposta |
|---|---|
| Status "concluído" | Verde (`--pos`) + `rgba(74,222,128,…)` |
| Status "em desenvolvimento" | Viking (`--viking`) + `rgba(94,202,218,…)` |
| Status "novo / aguardando" | Amethyst (`--amethyst`) + `rgba(128,98,222,…)` |
| Prazo crítico / urgente | Amarelo (`--neu`) + borda `rgba(251,191,36,.30)` |
| Frequência diária | Vermelho (`--neg`) — pill `.f-d` |
| Frequência semanal | Amarelo (`--neu`) — pill `.f-s` |
| Frequência mensal | Verde (`--pos`) — pill `.f-m` |
| Frequência crônica | Amethyst — pill `.f-c` |
| Frequência pontual | Viking — pill `.f-p` |
| Número/KPI principal | 38px, weight 800 |
| Label de KPI | 11px, uppercase, letter-spacing .8px, `--text-lo` |
| Eyebrow de seção | 11px, uppercase, letter-spacing 1.5px, `--amethyst` ou `--text-lo` |
| Título de seção | 30px, weight 800 |
| Gradient text | `linear-gradient(120deg, #e0d8ff, var(--jacarta), var(--viking))` |
