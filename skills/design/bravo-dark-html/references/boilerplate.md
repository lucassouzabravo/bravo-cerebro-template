# Boilerplate — HTML Self-Contained Dark Bravo

Estrutura mínima para qualquer report HTML neste design system.
Copie, substitua os `<!-- CONTEÚDO -->` e preencha o DATA_URI do logo via PowerShell.

## Como gerar o DATA_URI do logo

```powershell
$bytes = [System.IO.File]::ReadAllBytes("C:\Users\brass\.claude\skills\bravo-brand-guidelines\assets\logos\bravo-iso-color.png")
$b64 = [Convert]::ToBase64String($bytes)
# Use "data:image/jpeg;base64,$b64" como src das tags <img> do logo
```

---

## HTML Boilerplate Completo

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title><!-- TÍTULO DA PÁGINA --></title>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:        #07051a; --surface-1: #0d0a22; --surface-2: #110e2c; --surface-3: #17143a;
      --border:    rgba(128,98,222,.14); --border-md: rgba(128,98,222,.28); --border-hi: rgba(128,98,222,.50);
      --jacarta:   #8062de; --amethyst: #aa6cc9; --viking: #5ecada;
      --text-hi:   #ffffff; --text-md: #c8bff3; --text-lo: #6b6090;
      --pos: #4ade80; --neu: #fbbf24; --neg: #f87171;
      --font: 'Montserrat', system-ui, -apple-system, sans-serif;
    }

    html { font-family: var(--font); -webkit-font-smoothing: antialiased; scroll-behavior: smooth; }
    body { background: var(--bg); color: var(--text-hi); min-height: 100vh; }

    body::before {
      content: ''; pointer-events: none; position: fixed; inset: 0; z-index: 0;
      background:
        radial-gradient(ellipse 800px 500px at 20% -10%, rgba(128,98,222,.10) 0%, transparent 70%),
        radial-gradient(ellipse 600px 400px at 80% 110%, rgba(94,202,218,.07) 0%, transparent 70%);
    }

    .wrap { position: relative; z-index: 1; max-width: 1100px; margin: 0 auto; padding: 0 32px; }

    /* HEADER */
    .site-header { position: sticky; top: 0; z-index: 100; background: rgba(7,5,26,.80); backdrop-filter: blur(16px); border-bottom: 1px solid var(--border); }
    .header-inner { max-width: 1100px; margin: 0 auto; padding: 14px 32px; display: flex; align-items: center; justify-content: space-between; }
    .logo-row { display: flex; align-items: center; gap: 12px; }
    .logo-sep  { width: 1px; height: 18px; background: var(--border-md); }
    .logo-sub  { font-size: 13px; color: var(--text-lo); font-weight: 500; }
    .tag { font-size: 11px; font-weight: 600; letter-spacing: .8px; text-transform: uppercase; color: var(--text-lo); border: 1px solid var(--border); border-radius: 4px; padding: 3px 9px; }
    .tag-live { border-color: rgba(74,222,128,.3); color: var(--pos); }
    .tag-live::before { content: '● '; font-size: 8px; }

    /* HERO */
    .hero { padding: 72px 0 56px; }
    .eyebrow { display: inline-flex; align-items: center; gap: 8px; background: rgba(128,98,222,.08); border: 1px solid rgba(128,98,222,.25); color: var(--amethyst); font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 5px 14px; border-radius: 9999px; margin-bottom: 24px; }
    .eyebrow-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--viking); }
    .hero-title { font-size: clamp(36px,4.5vw,54px); font-weight: 800; line-height: 1.08; letter-spacing: -1.5px; margin-bottom: 18px; }
    .grad { background: linear-gradient(120deg, #e0d8ff 0%, var(--jacarta) 45%, var(--viking) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
    .hero-sub { font-size: 17px; color: var(--text-md); max-width: 560px; line-height: 1.65; margin-bottom: 52px; }

    /* KPI CARDS */
    .kpi-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; }
    .kpi-card { background: var(--surface-2); border: 1px solid var(--border); border-radius: 14px; padding: 22px 24px; transition: border-color .2s, box-shadow .2s; }
    .kpi-card:hover { border-color: var(--border-md); box-shadow: 0 0 24px rgba(128,98,222,.15); }
    .kpi-lbl { font-size: 11px; font-weight: 600; letter-spacing: .8px; text-transform: uppercase; color: var(--text-lo); margin-bottom: 10px; }
    .kpi-val { font-size: 38px; font-weight: 800; line-height: 1; }
    .kpi-hint { font-size: 12px; color: var(--text-lo); margin-top: 6px; }
    .c-jacarta { color: var(--jacarta); } .c-amethyst { color: var(--amethyst); } .c-viking { color: var(--viking); } .c-pos { color: var(--pos); }

    /* SECTIONS */
    .section     { padding: 72px 0; border-top: 1px solid var(--border); }
    .sec-eyebrow { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-lo); margin-bottom: 8px; }
    .sec-title   { font-size: 30px; font-weight: 800; letter-spacing: -.5px; margin-bottom: 8px; }
    .sec-desc    { font-size: 15px; color: var(--text-md); max-width: 600px; line-height: 1.6; margin-bottom: 40px; }

    /* FOOTER */
    .site-footer   { border-top: 1px solid var(--border); padding: 24px 0; text-align: center; }
    .site-footer p { font-size: 12px; color: var(--text-lo); }

    /* RESPONSIVE */
    @media (max-width: 900px) {
      .kpi-row { grid-template-columns: repeat(2,1fr); }
    }
  </style>
</head>
<body>

<!-- ══ HEADER ══ -->
<header class="site-header">
  <div class="header-inner">
    <div class="logo-row">
      <img src="<!-- DATA_URI -->" alt="Bravo" style="height:36px;width:auto;mix-blend-mode:screen;">
      <div class="logo-sep"></div>
      <span class="logo-sub"><!-- Subtítulo ex: AI Operations --></span>
    </div>
    <div style="display:flex;gap:10px;align-items:center;">
      <span class="tag tag-live"><!-- Status --></span>
      <span class="tag">Interno Confidencial</span>
    </div>
  </div>
</header>

<!-- ══ HERO ══ -->
<section class="hero">
  <div class="wrap">
    <div class="eyebrow">
      <span class="eyebrow-dot"></span>
      <!-- LABEL EX: RELATÓRIO · JUNHO 2026 -->
    </div>
    <h1 class="hero-title">
      <!-- Título Normal --> <span class="grad"><!-- Título Gradiente --></span>
    </h1>
    <p class="hero-sub"><!-- Subtítulo descritivo --></p>

    <!-- KPI CARDS -->
    <div class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-lbl"><!-- Label --></div>
        <div class="kpi-val c-jacarta"><!-- Número --></div>
        <div class="kpi-hint"><!-- Hint --></div>
      </div>
      <!-- repita os outros 3 cards -->
    </div>
  </div>
</section>

<!-- ══ SEÇÕES DE CONTEÚDO ══ -->
<section class="section">
  <div class="wrap">
    <div class="sec-eyebrow"><!-- NÚMERO · TÍTULO SEÇÃO --></div>
    <h2 class="sec-title"><!-- Título --></h2>
    <p class="sec-desc"><!-- Descrição --></p>
    <!-- CONTEÚDO DA SEÇÃO -->
  </div>
</section>

<!-- ══ FOOTER ══ -->
<footer class="site-footer">
  <img src="<!-- DATA_URI -->" alt="Bravo" style="height:28px;width:auto;display:block;margin:0 auto 10px;mix-blend-mode:screen;">
  <p>Bravo AI Operations · <!-- Mês Ano --> · Interno Confidencial</p>
</footer>

</body>
</html>
```
