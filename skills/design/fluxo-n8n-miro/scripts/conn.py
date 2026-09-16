# -*- coding: utf-8 -*-
"""Le o `connections` de um JSON exportado do n8n e imprime, linha a linha,
quem manda pra quem — a topologia real, sem interpretar visual nenhum.

Rode isto ANTES de posicionar qualquer no no board. E o que resolve a decisao
"lado a lado ou ramificacao?" de forma mecanica (ver SKILL.md -> "Lado a lado
ou ramificacao?"): conte saidas(N) e entradas(N) a partir desta saida.

Uso: python conn.py caminho/do/fluxo.json
"""
import json, sys

d = json.load(open(sys.argv[1], encoding='utf-8'))
for src, v in d.get('connections', {}).items():
    for i, out in enumerate(v.get('main', []) or []):
        for c in (out or []):
            print('%-38s [saida %d] -> %-38s [entrada %s]'
                  % (src, i, c['node'], c.get('index', 0)))
