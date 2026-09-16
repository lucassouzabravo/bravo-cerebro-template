"""
build_cover.py
==============
Gera o PNG da capa A4 full-bleed (1654×2339 px @ 200 dpi) para documentos
longos Bravo. A capa é construída inteira como imagem porque Word não
suporta gradiente de página com cobertura total confiável.

Uso:

    from build_cover import build_cover

    build_cover(
        out_path='/tmp/cover_full.png',
        eyebrow='CAPACITAÇÃO AI OPERATIONS  ·  BLOCO 1',
        title_lines=['Fundamentos', 'de IA Aplicada'],
        subtitle_lines=[
            'Base conceitual para liderança e governança',
            'de Claude na Bravo',
        ],
        audience_lines=[
            'Documento preparado para a Diretoria',
            'AI Operations  ·  Bravo  ·  2025–2026',
        ],
        footer_lines=[
            'Confidencial — Uso interno Bravo',
            'Versão 1.0  ·  Maio de 2026',
        ],
        logo_white_alpha_path='/.../assets/logos/bravo-logo-branco-alpha.png',
    )

Requer:
    - Pillow
    - Logo branco com transparência alfa REAL
      (use o arquivo bravo-logo-branco-alpha.png desta skill — NÃO o original
      da bravo-brand-guidelines, que é JPEG renomeado)
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os


# Cores do Gradient 1 + acentos translúcidos
PURPLE_DARK = (32, 29, 73)        # #201D49
PURPLE_DEEP = (61, 53, 158)       # #3D359E
AMETHYST_T = (170, 108, 201, 60)  # com alfa
JACARTA_T  = (128, 98, 222, 45)
VIKING_T   = (94, 202, 218, 35)
LIGHT_PUR  = (200, 191, 243)      # texto secundário
MUTED_PUR  = (170, 151, 220)      # texto terciário


def _find_font(*candidates, size):
    """Tenta carregar a primeira fonte disponível da lista de candidatos."""
    for path in candidates:
        if path and os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except (OSError, IOError):
                continue
    # último recurso: fonte default Pillow (bitmap, pixelizada)
    return ImageFont.load_default()


def _candidates(weight):
    """Retorna lista ordenada de fontes a tentar para um peso.
    Montserrat primeiro (se instalada); DejaVu como fallback aceitável."""
    return [
        f'/usr/share/fonts/truetype/montserrat/Montserrat-{weight}.ttf',
        f'/tmp/montserrat/Montserrat-{weight}.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if weight in ('Bold', 'SemiBold')
            else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]


def build_cover(
    out_path,
    *,
    eyebrow,
    title_lines,
    subtitle_lines,
    audience_lines,
    footer_lines,
    logo_white_alpha_path,
    page_size_px=(1654, 2339),
):
    """Gera PNG A4 full-bleed para capa.
    title_lines:    1 a 3 linhas de título principal
    subtitle_lines: 1 a 3 linhas de subtítulo
    audience_lines: 1 a 2 linhas (público / data)
    footer_lines:   1 a 2 linhas (classificação / versão)
    """
    W, H = page_size_px

    # 1. Gradiente vertical Purple Dark → Purple Deep
    img = Image.new('RGB', (W, H), PURPLE_DARK)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        r = int(PURPLE_DARK[0] + (PURPLE_DEEP[0] - PURPLE_DARK[0]) * t)
        g = int(PURPLE_DARK[1] + (PURPLE_DEEP[1] - PURPLE_DARK[1]) * t)
        b = int(PURPLE_DARK[2] + (PURPLE_DEEP[2] - PURPLE_DARK[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 2. Círculos blurred (Amethyst, Jacarta, Viking) — quebram a chapadidão
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.ellipse([W - 700, -300, W + 300, 700], fill=AMETHYST_T)
    odraw.ellipse([-250, H - 900, 650, H - 100], fill=JACARTA_T)
    odraw.ellipse([100, 100, 350, 350], fill=VIKING_T)
    overlay = overlay.filter(ImageFilter.GaussianBlur(80))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

    # 3. Logo branco transparente centralizado no topo (~16% from top)
    if not os.path.exists(logo_white_alpha_path):
        raise FileNotFoundError(
            f"Logo white-alpha não encontrado: {logo_white_alpha_path}\n"
            "Use bravo-logo-branco-alpha.png desta skill (não o original da brand-guidelines)."
        )
    logo = Image.open(logo_white_alpha_path)
    target_w = 380
    ratio = target_w / logo.width
    logo_r = logo.resize((target_w, int(logo.height * ratio)), Image.LANCZOS)
    img.paste(logo_r, ((W - target_w) // 2, int(H * 0.16)), logo_r)

    # 4. Texto
    draw = ImageDraw.Draw(img)
    title_f = _find_font(*_candidates('Bold'), size=90)
    sub_f   = _find_font(*_candidates('Regular'), size=38)
    tag_f   = _find_font(*_candidates('Bold'), size=26)
    small_f = _find_font(*_candidates('Regular'), size=24)
    foot_f  = _find_font(*_candidates('Regular'), size=20)

    def cx(y, txt, font, color):
        bb = draw.textbbox((0, 0), txt, font=font)
        w = bb[2] - bb[0]
        draw.text(((W - w) // 2, y), txt, font=font, fill=color)

    # Eyebrow pill (capsule outlined)
    y_eb = int(H * 0.36)
    bb = draw.textbbox((0, 0), eyebrow, font=tag_f)
    ebw = bb[2] - bb[0]; ebh = bb[3] - bb[1]
    pad_x, pad_y = 32, 16
    px = (W - ebw) // 2 - pad_x
    py = y_eb - pad_y
    pw = ebw + 2 * pad_x
    ph = ebh + 2 * pad_y + 8
    draw.rounded_rectangle([px, py, px + pw, py + ph],
                           radius=ph // 2, outline=LIGHT_PUR, width=2)
    draw.text(((W - ebw) // 2, y_eb), eyebrow, font=tag_f, fill=LIGHT_PUR)

    # Título (1 a 3 linhas, line-height ~110px)
    base_y = int(H * 0.43)
    line_h = 110
    for i, ln in enumerate(title_lines):
        cx(base_y + i * line_h, ln, title_f, (255, 255, 255))

    # Subtítulo
    sub_base = int(H * 0.59)
    sub_lh = 50
    for i, ln in enumerate(subtitle_lines):
        cx(sub_base + i * sub_lh, ln, sub_f, LIGHT_PUR)

    # Divisor curto Amethyst
    dy = int(H * 0.69)
    draw.rectangle([(W // 2 - 120, dy), (W // 2 + 120, dy + 3)],
                   fill=(170, 108, 201))

    # Audiência
    aud_base = int(H * 0.72)
    aud_lh = 32
    for i, ln in enumerate(audience_lines):
        col = (255, 255, 255) if i == 0 else MUTED_PUR
        cx(aud_base + i * aud_lh, ln, small_f, col)

    # Rodapé
    foot_base = int(H * 0.92)
    foot_lh = 30
    for i, ln in enumerate(footer_lines):
        cx(foot_base + i * foot_lh, ln, foot_f, MUTED_PUR)

    img.save(out_path, 'PNG', dpi=(200, 200))
    return out_path


if __name__ == '__main__':
    # Smoke test
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    logo = os.path.join(here, '..', 'assets', 'logos', 'bravo-logo-branco-alpha.png')
    out = sys.argv[1] if len(sys.argv) > 1 else '/tmp/cover_test.png'
    build_cover(
        out_path=out,
        eyebrow='SKILL  ·  TESTE DE CAPA',
        title_lines=['Documento', 'de Exemplo'],
        subtitle_lines=['Subtítulo explicativo', 'em duas linhas'],
        audience_lines=['Preparado para destinatário', 'Bravo  ·  2026'],
        footer_lines=['Confidencial — Uso interno Bravo', 'Versão 0.1'],
        logo_white_alpha_path=logo,
    )
    print('Capa gerada em:', out)
