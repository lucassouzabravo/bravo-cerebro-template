# -*- coding: utf-8 -*-
"""Prova 7 — o que um quadro MANDA bate com o que o outro DEVOLVE?

Existe porque dois quadros podem estar cada um individualmente correto e ainda
assim mentir um sobre o outro: o quadro 04 esperava receber `url_assinada` do
quadro 05, que devolvia `status`. A prova cruzada JSON x gerador (ver
conferir_json_x_miro.py) não pega isso porque ela conta NÓS, não campos.

A regra, e é assimétrica de propósito:
    o CONSUMIDOR não pode esperar campo que o PRODUTOR não declara.
O produtor pode declarar campos extras — o consumidor simplesmente os ignora.
O contrário é que quebra: esperar um campo que ninguém produz devolve `undefined`
em silêncio.

ADAPTE A LISTA `PARES` ABAIXO para os seus geradores: cada item é
(consumidor, marcador-no-consumidor, produtor, marcador-no-produtor,
pegar-so-a-ultima-ocorrencia). Os marcadores são qualquer string única que
apareça no seu .py logo antes da lista de campos — ex.: um comentário
"RECEBE:" ou "DEVOLVE:" no gerador, como no exemplo de `exemplo_uso.py`.

Uso: python conferir_contrato.py
"""
import io, re, sys, os

if not isinstance(sys.stdout, io.TextIOWrapper) or sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AQUI = os.path.dirname(os.path.abspath(__file__))

# EXEMPLO — troque pelos arquivos e marcadores do seu próprio projeto.
# (consumidor, marcador, produtor, marcador, pegar_ultima_ocorrencia)
PARES = [
    ('quadro_consumidor.py', 'RECEBE:', 'quadro_produtor.py', 'DEVOLVE:', False),
]

# palavras que aparecem nas listas e NÃO são nome de campo — amplie conforme
# o vocabulário do seu fluxo for gerando falso positivo
RUIDO = {
    'n', 'ok', 'parcial', 'sim', 'nao', 'true', 'false', 'null', 'uma', 'por',
    'e', 'ou', 'de', 'do', 'da',
}


def campos_do_bloco(caminho, marcador, linhas_depois=8, ultima=False):
    """Lê o .py do gerador, acha o marcador e colhe os nomes de campo dali em diante.

    Colhe até a lista terminar (`])`) ou até `linhas_depois`, o que vier primeiro.
    `ultima=True` quando o marcador aparece mais de uma vez e o contrato é o do
    último bloco (ex.: um nó que normaliza eventos e depois um nó que devolve o
    placar final — o contrato é sempre com quem devolve por último).
    """
    texto = open(os.path.join(AQUI, caminho), encoding='utf-8').read().splitlines()
    achados = [i for i, linha in enumerate(texto) if marcador in linha]
    if not achados:
        return None, None
    achou = achados[-1] if ultima else achados[0]

    trecho = []
    for linha in texto[achou:achou + linhas_depois]:
        if '])' in linha:
            trecho.append(linha)
            break
        trecho.append(linha)

    # cada item da lista vira uma linha própria, para o nome que abre a linha
    # não ficar sem separador à esquerda
    bruto = '\n'.join(' ' + l.strip() for l in trecho)
    # nome de campo = snake_case ou palavra simples, antes de : ou , ou }
    # a classe da esquerda precisa incluir aspa e apóstrofo: no gerador cada
    # item é uma string Python, então o campo que abre o item vem logo depois
    # de `'` ou `"`
    nomes = set()
    for m in re.finditer(r"""(?:^|[\s{,\['"])([a-z][a-z0-9_]{2,})\s*[,:}\]]""", bruto, re.M):
        nome = m.group(1)
        if nome not in RUIDO:
            nomes.add(nome)
    return nomes, '\n'.join(l.strip() for l in trecho)


print('=' * 72)
print('PROVA 7 — contrato entre quadros')
print('regra: o consumidor não pode esperar campo que o produtor não declara')
print('=' * 72)

falhas = 0
for consumidor, m_cons, produtor, m_prod, ultima in PARES:
    espera, bloco_c = campos_do_bloco(consumidor, m_cons)
    produz, bloco_p = campos_do_bloco(produtor, m_prod, ultima=ultima)

    print('\n%s  espera de  %s' % (consumidor, produtor))

    if espera is None:
        print('   *** MARCADOR NÃO ACHADO em %s: "%s"' % (consumidor, m_cons))
        falhas += 1
        continue
    if produz is None:
        print('   *** MARCADOR NÃO ACHADO em %s: "%s"' % (produtor, m_prod))
        falhas += 1
        continue

    print('   espera: %s' % ', '.join(sorted(espera)))
    print('   produz: %s' % ', '.join(sorted(produz)))

    orfaos = espera - produz
    if orfaos:
        falhas += 1
        print('   *** FALTA NO PRODUTOR: %s' % ', '.join(sorted(orfaos)))
        print('   --- o que o consumidor declara ---')
        for l in bloco_c.splitlines():
            print('       %s' % l)
        print('   --- o que o produtor declara ---')
        for l in bloco_p.splitlines():
            print('       %s' % l)
    else:
        extras = produz - espera
        obs = (' (produtor declara %d campo(s) a mais, e isso é ok)' % len(extras)) if extras else ''
        print('   OK: todo campo esperado existe no produtor%s' % obs)

print('\n' + '=' * 72)
if falhas:
    print('RESULTADO: %d contrato(s) com problema' % falhas)
    sys.exit(1)
print('RESULTADO: todos os contratos batem')
