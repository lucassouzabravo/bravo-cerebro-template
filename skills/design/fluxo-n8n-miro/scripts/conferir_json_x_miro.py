# -*- coding: utf-8 -*-
"""PROVA CRUZADA: o JSON do n8n e o gerador do Miro contam a MESMA topologia?

Existe porque o JSON de um fluxo e o quadro correspondente no board podem
divergir sem ninguém perceber: quem construísse pelo board construiria o
fluxo errado. Rodar isto ANTES de enviar qualquer quadro ao Miro.

ADAPTE A LISTA `PARES` ABAIXO com os pares (gerador .py, json do n8n) do seu
próprio projeto.
"""
import json, re, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# EXEMPLO — troque pelos arquivos do seu próprio projeto.
PARES = [
    ('quadro_01.py', 'Fluxo Principal.json'),
]
RX = re.compile(r"q\.forma\(\s*'([^']+)'\s*,\s*'([^']*)'\s*,\s*'([^']+)'")
# se algum quadro cria nós repetidos num loop de Python (ex.: N consultas
# geradas por um `for`), o regex só vê a chamada uma vez — declare aqui
# quantos nós "extras" aquele arquivo produz de verdade
LOOP_EXTRA = {}
falhou = 0
for py, js in PARES:
    base = os.path.dirname(os.path.abspath(__file__))
    src = open(os.path.join(base, py), encoding='utf-8').read()
    formas = RX.findall(src)
    doc = json.load(open(os.path.join(base, js), encoding='utf-8'))
    n_json = len(doc['nodes'])
    n_miro = len(formas)
    n_miro += LOOP_EXTRA.get(os.path.basename(py), 0)
    # a ORDEM de declaracao nao importa (os nos podem ser declarados por
    # corredor, nao por numero). O que importa e o CONJUNTO: os numeros tem
    # que ser 1..N, sem furo e sem repeticao.
    nums = sorted(int(f[1]) for f in formas if f[1].isdigit())
    if os.path.basename(py) in LOOP_EXTRA:
        nums = sorted(nums + list(range(3, 3 + LOOP_EXTRA[os.path.basename(py)])))
    completo = nums == list(range(1, n_miro + 1))
    status = 'OK ' if (n_json == n_miro and completo) else '!! '
    if status == '!! ':
        falhou += 1
    faltando = sorted(set(range(1, n_miro + 1)) - set(nums))
    print('%s%-16s  miro %2d nos  x  json %2d nos   numeros 1..N sem furo: %s'
          % (status, os.path.basename(py), n_miro, n_json,
             'sim' if completo else 'NAO (faltando %s)' % faltando))
print()
print('RESULTADO: %s' % ('todos batem' if falhou == 0 else '%d divergencia(s)' % falhou))
