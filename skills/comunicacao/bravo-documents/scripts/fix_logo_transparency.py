"""
fix_logo_transparency.py
========================
Converte os arquivos de logo da skill bravo-brand-guidelines (que são JPEG
renomeados como .png, sem canal alfa) em PNGs com transparência alfa real.

PROBLEMA QUE ESTE SCRIPT RESOLVE
---------------------------------
Os arquivos:
    bravo-brand-guidelines/assets/logos/bravo-logo-color.png
    bravo-brand-guidelines/assets/logos/bravo-logo-branco.png

São JPEG (verifique com `file`). JPEG não suporta canal alfa — então
quando compostos sobre qualquer fundo que não seja a cor embutida do JPEG,
aparece um retângulo sólido (preto, no caso do "branco").

Foi exatamente isso que gerou o "fundo preto atrás do logo" no PDF antigo
de Fundamentos de IA. Este script processa os originais e gera versões
com pixels pretos convertidos em alfa = 0.

USO
---
    python fix_logo_transparency.py \
        --color-src   /path/to/bravo-logo-color.png \
        --branco-src  /path/to/bravo-logo-branco.png \
        --out-dir     /path/to/bravo-documents/assets/logos/

Os arquivos gerados são:
    bravo-logo-color-alpha.png   — use sobre fundos CLAROS (header de páginas)
    bravo-logo-branco-alpha.png  — use sobre fundos ESCUROS (capa)

REGRA OPERACIONAL
-----------------
SEMPRE use os arquivos *-alpha.png desta skill, nunca os originais.
"""
import argparse
import os
import sys

from PIL import Image
import numpy as np


def fix_color_logo(src_path, out_path):
    """Logo colorido em JPEG-com-fundo-preto → PNG com pretos transparentes."""
    img = Image.open(src_path).convert('RGBA')
    data = np.array(img)
    r, g, b, _ = data.T
    black_mask = (r < 30) & (g < 30) & (b < 30)
    data[..., 3][black_mask.T] = 0
    out = Image.fromarray(data)
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    out.save(out_path, 'PNG')
    return out.size


def fix_white_logo(src_path, out_path):
    """Logo branco em JPEG-com-fundo-preto → PNG com pretos transparentes
    + pixels não-pretos forçados a branco puro."""
    img = Image.open(src_path).convert('RGBA')
    data = np.array(img)
    r, g, b, _ = data.T
    black_mask = (r < 30) & (g < 30) & (b < 30)
    data[..., 3][black_mask.T] = 0
    non_black = ~black_mask.T
    data[..., 0][non_black] = 255
    data[..., 1][non_black] = 255
    data[..., 2][non_black] = 255
    out = Image.fromarray(data)
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    out.save(out_path, 'PNG')
    return out.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--color-src', required=True,
                    help='Caminho para bravo-logo-color.png original (JPEG renomeado)')
    ap.add_argument('--branco-src', required=True,
                    help='Caminho para bravo-logo-branco.png original (JPEG renomeado)')
    ap.add_argument('--out-dir', required=True,
                    help='Diretório de saída para os arquivos *-alpha.png')
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    out_color = os.path.join(args.out_dir, 'bravo-logo-color-alpha.png')
    out_branco = os.path.join(args.out_dir, 'bravo-logo-branco-alpha.png')

    size_c = fix_color_logo(args.color_src, out_color)
    print(f'OK  color  → {out_color}  ({size_c[0]}×{size_c[1]})')
    size_w = fix_white_logo(args.branco_src, out_branco)
    print(f'OK  branco → {out_branco}  ({size_w[0]}×{size_w[1]})')


if __name__ == '__main__':
    main()
