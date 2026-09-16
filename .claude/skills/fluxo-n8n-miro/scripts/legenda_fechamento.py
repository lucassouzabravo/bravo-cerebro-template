# -*- coding: utf-8 -*-
"""Pecas compartilhadas entre varios quadros: legenda de cores/formas e o
fechamento (dimensiona o frame, roda o verificador, grava o SVG).

Generico: ajuste CATS para o vocabulario de categorias do SEU fluxo (aqui vai
o conjunto de exemplo da skill). O que nao muda e o mecanismo: legenda() e
fecha() sao as mesmas para qualquer projeto.
"""
import io, sys
from quadro import esc, CARD_W

FORMAS = [
    'pílula = dispara o fluxo',
    'retângulo = processa, transforma ou consulta',
    'losango = decide um caminho',
    'círculo = repete',
    'elipse = espera',
    'hexágono = sai do fluxo e volta',
    'canto forte = grava o resultado',
]
CATS = [('gatilho', 'gatilho'), ('consulta', 'consulta'), ('codigo', 'codigo'),
        ('decisao', 'decisao'), ('juntar', 'juntar'), ('subfluxo', 'subfluxo'),
        ('loop', 'loop'), ('banco', 'banco')]


def legenda(q, como_ler):
    """Legenda no topo esquerdo: post-its de leitura + swatches de cor + formas."""
    q.faixa('lg0', 100, 60, 'Como ler este quadro', w=400)
    for k, t in enumerate(como_ler):
        q.add('postit', 'lgp%d' % k, 140, 96 + k * 238, 319, 208,
              '<rect id="lgp%d" data-type="sticky" x="140" y="%d" width="319" height="208" '
              'data-color="yellow" data-content="%s" />' % (k, 96 + k * 238, esc(t)))
    q.faixa('lg1', 560, 60, 'Legenda de cores · a cor diz de que categoria o nó é', w=800)
    from quadro import COR
    for i, (cat, rot) in enumerate(CATS):
        cx = 560 + (i % 4) * 205
        cy = 96 + (i // 4) * 80
        q.add('no', 'lgc%d' % i, cx, cy, 195, 70,
              '<rect id="lgc%d" x="%d" y="%d" width="195" height="70" rx="14" '
              'data-content="%s" fill="%s" data-text-color="#ffffff" data-font-size="15" '
              'data-font-family="Roboto Mono" stroke="#1a1a1a" />'
              % (i, cx, cy, rot, COR[cat]))
    q.faixa('lg2', 560, 320, 'A forma diz o que o nó faz com o dado', w=800)
    h = 19.7 * len(FORMAS)
    q.add('lista', 'lgf', 570, 404, 780, h,
          '<textArea id="lgf" x="570" y="%d" width="780" font-size="14" '
          'font-family="Roboto Mono" fill="#333333" text-align="left">%s</textArea>'
          % (404, '<br />'.join(esc(l) for l in FORMAS)))


def fecha(q, nome, arquivo, frame_x, frame_y, margem=700):
    """Dimensiona o frame com folga, roda os verificadores e grava o SVG em disco."""
    if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    mx, my = q.extremos()
    fw = int((mx + margem) / 100 + 1) * 100
    fh = int((my + margem) / 100 + 1) * 100
    print('== %s ==' % nome)
    print('conteudo ate %.0f x %.0f  ->  frame %d x %d  em (%d,%d)' % (mx, my, fw, fh, frame_x, frame_y))
    print('elementos: %d  conectores: %d' % (len(q.el), len(q.conns)))
    prob = q.verifica() + q.verifica_conectores()
    if prob:
        print('!! %d PROBLEMAS NA GEOMETRIA CALCULADA' % len(prob))
        for p in prob:
            print('   ' + p)
    else:
        print('OK: 0 sobreposicoes, 0 desalinhamentos, 0 diagonais na geometria calculada')
    svg = '<svg xmlns="http://www.w3.org/2000/svg">\n%s\n</svg>' % q.svg(frame_x, frame_y, fw, fh)
    open(arquivo, 'w', encoding='utf-8').write(svg)
    print('svg: %s  (%d chars)' % (arquivo, len(svg)))
    return prob
