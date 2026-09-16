# -*- coding: utf-8 -*-
"""Confere o resultado de um canvas_create_from_svg.

Uso: python conferir_envio.py <arquivo-do-tool-result> <esperado_elementos> <esperado_conectores>

Existe porque o numero que o gerador imprime NAO e o created_count:
    created_count = elementos + conectores + 1 (o frame)
Foi o erro 33/34 da skill fluxo-n8n-miro: comparar o numero errado reprova um
envio que estava correto.
"""
import json, re, sys, collections, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

arq, el, cn = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
d = json.load(open(arq, encoding='utf-8'))
esperado = el + cn + 1

print('=' * 62)
print('success      =', d['success'])
print('created      =', d['created_count'], '| esperado', esperado,
      '->', 'BATE' if d['created_count'] == esperado else '*** NAO BATE ***')
print('failed_items =', len(d['failed_items']), d['failed_items'][:3] if d['failed_items'] else '')
print('skipped      =', len(d['skipped']), d['skipped'][:3] if d['skipped'] else '')

svg = d['result_svg']
saida = arq.replace('.txt', '_result.svg')
open(saida, 'w', encoding='utf-8').write(svg)

# frame: onde nasceu
m = re.search(r'<g[^>]*transform="translate\(([^)]*)\)"', svg)
g = re.search(r'<g[^>]*data-miro-id="(\d+)"', svg)
print('frame id     =', g.group(1) if g else '?')
print('translate    =', m.group(1) if m else '?')

# formas: o Miro degrada em silencio o que nao reconhece
print('-- formas dos nos (data-shape / rx) --')
degradou = []
for m in re.finditer(r'<(rect|circle|ellipse)[^>]*id="(n\d+)"[^>]*>', svg):
    seg, tag, nid = m.group(0), m.group(1), m.group(2)
    sh = re.search(r'data-shape="([^"]+)"', seg)
    rx = re.search(r' rx="([^"]+)"', seg)
    print('   %-5s %-8s shape=%-9s rx=%s' % (nid, tag, sh.group(1) if sh else '-',
                                             rx.group(1) if rx else '-'))

# fonte: nome errado degrada em silencio (erro 28)
print('-- fontes devolvidas --')
for k, v in collections.Counter(re.findall(r'data-font-family="([^"]*)"', svg)).items():
    print('   forma/faixa  %-14s %d' % (k, v))
for k, v in collections.Counter(re.findall(r'(?<!data-)font-family="([^"]*)"', svg)).items():
    print('   textArea     %-14s %d' % (k, v))
    if k not in ('Roboto Mono', 'Plex Mono'):
        degradou.append(k)

print('-- tipos preservados --')
print('   sticky =', len(re.findall(r'data-type="sticky"', svg)),
      '| conectores =', len(re.findall(r'<line', svg)),
      '| textArea =', len(re.findall(r'<textArea', svg)))

if degradou:
    print('*** ALERTA: fonte degradada ->', degradou)
print('svg salvo em', saida)
print('=' * 62)
