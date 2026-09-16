# -*- coding: utf-8 -*-
"""Gerador de quadro de fluxo n8n no padrao fluxo-n8n-miro (medido no quadro 01).

Toda a geometria vertical e mecanica: nada de numero escolhido a olho.
Roda o verificador de sobreposicao/alinhamento na geometria CALCULADA antes de
enviar pro board.

Este arquivo e generico: nao ha nada de projeto especifico aqui, so a logica de
layout que a skill fluxo-n8n-miro documenta em prosa. Adapte cores (COR) e
categorias (usadas em legenda_fechamento.py) ao vocabulario do fluxo que voce
esta desenhando.
"""
import math

# ---------------------------------------------------------------- parametros
CARD_W, CARD_H = 440, 120
FAIXA_H = 26
POSTIT_W, POSTIT_H = 359, 234
POSTIT_GAP = 30
OBS_W, OBS_H = 360, 180
OBS_GAP = 30
RECUO = 40                 # card interno dentro do bloco de 440
BASE_TO_FAIXA = 42         # base da forma mais alta -> faixa "O que faz"
FAIXA_TO_BLOCO = 10        # declarado (renderiza 15)
POSTIT_TO_FAIXA = 40       # ultimo post-it -> faixa "Campos"
FAIXA_TO_LISTA = 15
FOLGA_LINHA = 20           # fim da lista -> linha ; linha -> faixa "Observacoes"

LH_CAMPOS = 28.0           # px por linha, fs=20 ibm_plex_mono, width 440
LH_PAYLOAD = 19.7          # px por linha, fs=14 roboto_mono,  width 440
CPL_CAMPOS = 33
# MEDIDO no render: na CRIACAO o y de um <textArea> e o TOPO e nao precisa
# correcao nenhuma. E canvas_update_from_svg NAO MOVE textArea: responde
# "1 updated", ecoa o y novo, e o widget fica onde nasceu. Testado com -300px.
# Consequencia: acertar na criacao. Consertar depois exige apagar e recriar.
DESVIO_RENDER = {14: 0, 20: 0}
CPL_PAYLOAD = 50

COR = {
    'gatilho': '#f2c744', 'consulta': '#4b8bf5', 'codigo': '#8b5cf6',
    'decisao': '#ff8c00', 'juntar': '#00b86b', 'subfluxo': '#e0457b',
    'loop': '#00c4cc', 'banco': '#2d3142',
}

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))

def nlines(lines, cpl):
    n = 0
    for ln in lines:
        n += max(1, int(math.ceil(len(ln) / float(cpl))))
    return n

def alt_campos(lines):
    return LH_CAMPOS * nlines(lines, CPL_CAMPOS)

def alt_payload(lines):
    return LH_PAYLOAD * nlines(lines, CPL_PAYLOAD)


class Quadro(object):
    def __init__(self, titulo, line_y=2600):
        self.titulo = titulo
        self.line_y = line_y
        self.el = []          # dicts: kind,x,y,w,h,svg
        self.conns = []
        self.ids = {}
        self.trecho_ly = {}
        self.pares = []       # (origem, destino) de cada conector
        self.pos = {}         # id -> (cx, cy) para a prova de diagonal

    # ---------------------------------------------------------- primitivas
    def add(self, kind, eid, x, y, w, h, svg, owner=None, role=None):
        self.el.append(dict(kind=kind, id=eid, x=float(x), y=float(y),
                            w=float(w), h=float(h), svg=svg,
                            owner=owner, role=role))

    def faixa(self, eid, x, y, texto, w=CARD_W, trecho=False, owner=None, role=None):
        fill = '#d0d0d0' if trecho else '#ededed'
        tc = '#333333' if trecho else '#6e6e6e'
        self.add('faixa', eid, x, y, w, FAIXA_H,
                 '<rect id="%s" x="%d" y="%d" width="%d" height="%d" data-content="%s" '
                 'fill="%s" data-text-color="%s" data-font-size="13" '
                 'data-font-family="roboto_mono" stroke="#1a1a1a" />'
                 % (eid, x, y, w, FAIXA_H, esc(texto), fill, tc),
                 owner, role or ('faixa_trecho' if trecho else 'faixa'))

    def postit(self, eid, x, y, texto, owner=None):
        self.add('postit', eid, x, y, POSTIT_W, POSTIT_H,
                 '<rect id="%s" data-type="sticky" x="%d" y="%d" width="%d" height="%d" '
                 'data-color="yellow" data-content="%s" />'
                 % (eid, x, y, POSTIT_W, POSTIT_H, esc(texto)), owner, 'postit')

    def obs(self, eid, x, y, texto, owner=None):
        self.add('obs', eid, x, y, OBS_W, OBS_H,
                 '<rect id="%s" x="%d" y="%d" width="%d" height="%d" rx="16" '
                 'data-content="%s" fill="#f5f5f5" data-text-color="#1a1a1a" '
                 'data-font-size="13" data-font-family="roboto_mono" stroke="#1a1a1a" />'
                 % (eid, x, y, OBS_W, OBS_H, esc(texto)), owner, 'obs')

    def lista(self, eid, x, topo, lines, tipo='campos', owner=None):
        if tipo == 'campos':
            h, fs, ff = alt_campos(lines), 20, 'Plex Mono'
        else:
            h, fs, ff = alt_payload(lines), 14, 'Roboto Mono'
        # MEDIDO no render, com a faixa de 26px como regua:
        # 1. o y enviado e o TOPO da caixa (x=100 numa caixa de 440 volta com
        #    centro 320; y=3375 com altura 140 volta com centro 3445);
        # 2. mas o TEXTO renderiza mais baixo que o topo da caixa, e o desvio
        #    depende do corpo da fonte. Sem corrigir, a lista de payload encosta
        #    na linha do fluxo e o rotulo do conector cai em cima dela.
        # A correcao e o desvio medido, com sinal invertido.
        y_env = topo + DESVIO_RENDER[fs]
        body = '<br />'.join(esc(l) for l in lines)
        self.add('lista', eid, x, topo, CARD_W, h,
                 '<textArea id="%s" x="%d" y="%d" width="%d" font-size="%d" '
                 'font-family="%s" fill="#333333" text-align="left">%s</textArea>'
                 % (eid, x, round(y_env), CARD_W, fs, ff, body), owner, 'lista_' + tipo)
        return h

    def forma(self, eid, num, nome, x, ycentro, cat, forma='rect', fs=16):
        cor = COR[cat]
        label = ('%s · %s' % (num, nome)) if num else nome
        if forma == 'circulo':
            r = 110
            self.add('no', eid, x, ycentro - r, 2 * r, 2 * r,
                     '<circle id="%s" cx="%d" cy="%d" r="%d" data-content="%s" fill="%s" '
                     'data-text-color="#ffffff" data-font-size="%d" '
                     'data-font-family="roboto_mono" stroke="#1a1a1a" />'
                     % (eid, x + r, ycentro, r, esc(label), cor, fs), eid, 'no')
            self.pos[eid] = (float(x + r), float(ycentro))
            return dict(x=x, cx=x + r, top=ycentro - r, base=ycentro + r, w=2 * r)
        if forma == 'elipse':
            rx, ry = 220, 70
            self.add('no', eid, x, ycentro - ry, 2 * rx, 2 * ry,
                     '<ellipse id="%s" cx="%d" cy="%d" rx="%d" ry="%d" data-content="%s" '
                     'fill="%s" data-text-color="#ffffff" data-font-size="%d" '
                     'data-font-family="roboto_mono" stroke="#1a1a1a" />'
                     % (eid, x + rx, ycentro, rx, ry, esc(label), cor, fs), eid, 'no')
            self.pos[eid] = (float(x + rx), float(ycentro))
            return dict(x=x, cx=x + rx, top=ycentro - ry, base=ycentro + ry, w=2 * rx)
        h = 240 if forma == 'rhombus' else CARD_H
        rx = {'pilula': 60, 'grava': 16}.get(forma, 14)
        shape = ' data-shape="%s"' % forma if forma in ('rhombus', 'hexagon') else ''
        y = ycentro - h / 2
        self.add('no', eid, x, y, CARD_W, h,
                 '<rect id="%s" x="%d" y="%d" width="%d" height="%d"%s rx="%d" '
                 'data-content="%s" fill="%s" data-text-color="#ffffff" data-font-size="%d" '
                 'data-font-family="roboto_mono" stroke="#1a1a1a" />'
                 % (eid, x, y, CARD_W, h, shape, rx, esc(label), cor, fs), eid, 'no')
        self.pos[eid] = (float(x + CARD_W / 2), float(ycentro))
        return dict(x=x, cx=x + CARD_W / 2, top=y, base=y + h, w=CARD_W)

    def ponto(self, eid, x, y):
        self.add('ponto', eid, x - 5, y - 5, 10, 10,
                 '<circle id="%s" cx="%d" cy="%d" r="5" fill="#000000" stroke="#1a1a1a" />'
                 % (eid, x, y), eid, 'ponto')
        self.ids[eid] = (x, y)
        self.pos[eid] = (float(x), float(y))

    def conn(self, a, b, label=''):
        self.pares.append((a, b))
        self.conns.append('<line x1="0" y1="0" x2="1" y2="1" stroke="#000000" '
                          'stroke-width="2" data-start="%s" data-end="%s" data-arrow="end"%s />'
                          % (a, b, (' data-content="%s"' % esc(label)) if label else ''))

    def verifica_conectores(self):
        """Erro 27 da skill: conector cujos dois pontos estao em corredores
        diferentes vira DIAGONAL, e o verificador de geometria nunca ve isso
        (ele mede caixas, e conector nao tem caixa). A regra e mecanica:
        y_origem != y_destino exige que o par esteja alinhado em x (segmento
        vertical de dobra). Qualquer par que difira nos DOIS eixos e diagonal."""
        prob = []
        for a, b in self.pares:
            pa, pb = self.pos.get(a), self.pos.get(b)
            if pa is None or pb is None:
                prob.append('CONECTOR SEM POSICAO: %s -> %s' % (a, b))
                continue
            dx, dy = abs(pa[0] - pb[0]), abs(pa[1] - pb[1])
            if dx > 2 and dy > 2:
                prob.append('DIAGONAL %s(%.0f,%.0f) -> %s(%.0f,%.0f): dx=%.0f dy=%.0f'
                            % (a, pa[0], pa[1], b, pb[0], pb[1], dx, dy))
        return prob

    # ------------------------------------------------------------- blocos
    def bloco_no(self, no, geo, oquefaz, postits, campos_titulo, campos, cima=False,
                 base=None, top=None):
        """Bloco de explicacao de um no. cima=True -> espelhado.

        base/top: quando o no divide corredor com formas de alturas diferentes,
        passar a base da forma MAIS ALTA do corredor (parametros.md secao 2a),
        para as faixas do corredor inteiro nascerem no mesmo y.
        """
        x = int(geo['cx'] - CARD_W / 2)
        if not cima:
            fy = (base if base is not None else geo['base']) + BASE_TO_FAIXA
            self.faixa(no + 'f1', x, fy, oquefaz, owner=no, role='faixa_oquefaz')
            py = fy + FAIXA_H + FAIXA_TO_BLOCO
            for k, t in enumerate(postits):
                self.postit('%sp%d' % (no, k), x + RECUO, py + k * (POSTIT_H + POSTIT_GAP), t, owner=no)
            last = py + (len(postits) - 1) * (POSTIT_H + POSTIT_GAP)
            cy = last + POSTIT_H + POSTIT_TO_FAIXA
            self.faixa(no + 'f2', x, cy, campos_titulo, owner=no, role='faixa_campos')
            h = self.lista(no + 'l', x, cy + FAIXA_H + FAIXA_TO_LISTA, campos, 'campos', owner=no)
            return cy + FAIXA_H + FAIXA_TO_LISTA + h
        fy = (top if top is not None else geo['top']) - BASE_TO_FAIXA - FAIXA_H
        self.faixa(no + 'f1', x, fy, oquefaz, owner=no, role='faixa_oquefaz')
        py = fy - FAIXA_TO_BLOCO - POSTIT_H
        for k, t in enumerate(postits):
            self.postit('%sp%d' % (no, k), x + RECUO, py - k * (POSTIT_H + POSTIT_GAP), t, owner=no)
        last = py - (len(postits) - 1) * (POSTIT_H + POSTIT_GAP)
        cy = last - POSTIT_TO_FAIXA - FAIXA_H
        self.faixa(no + 'f2', x, cy, campos_titulo, owner=no, role='faixa_campos')
        h = alt_campos(campos)
        self.lista(no + 'l', x, cy - FAIXA_TO_LISTA - h, campos, 'campos', owner=no)
        return cy - FAIXA_TO_LISTA - h

    def bloco_trecho(self, tid, xcentro, line_y, rotulo, payload, obs):
        """Bloco de um trecho de linha: faixa+lista acima, faixa+cards abaixo."""
        x = int(xcentro - CARD_W / 2)
        h = alt_payload(payload)
        topo = line_y - FOLGA_LINHA - h
        self.faixa(tid + 'ft', x, topo - 41, rotulo, trecho=True, owner=tid, role='faixa_trecho')
        self.lista(tid + 'lt', x, topo, payload, 'payload', owner=tid)
        self.trecho_ly[tid] = line_y
        oy = line_y + FOLGA_LINHA
        self.faixa(tid + 'fo', x, oy, 'Observações', owner=tid, role='faixa_obs')
        for k, t in enumerate(obs):
            self.obs('%so%d' % (tid, k), x + RECUO, oy + FAIXA_H + FAIXA_TO_LISTA + k * (OBS_H + OBS_GAP), t, owner=tid)
        fim = oy + FAIXA_H + FAIXA_TO_LISTA + (len(obs) - 1) * (OBS_H + OBS_GAP) + OBS_H
        return (topo - 41, fim)

    # -------------------------------------------------------------- saida
    def extremos(self):
        xs = [e['x'] for e in self.el] + [e['x'] + e['w'] for e in self.el]
        ys = [e['y'] for e in self.el] + [e['y'] + e['h'] for e in self.el]
        return max(xs), max(ys)

    def svg(self, fx, fy, fw, fh):
        out = ['<g transform="translate(%d,%d)" data-frame="%s">' % (fx, fy, esc(self.titulo)),
               '<rect data-type="frame" x="0" y="0" width="%d" height="%d" fill="#FFFFFF" '
               'data-title="%s" />' % (fw, fh, esc(self.titulo))]
        out += self.conns                      # conectores ANTES das formas
        for role in ('ponto', 'no', 'faixa', 'postit', 'obs', 'lista'):
            for e in self.el:
                k = e['kind']
                if role == 'faixa' and k == 'faixa':
                    out.append(e['svg'])
                elif role == k:
                    out.append(e['svg'])
        out.append('</g>')
        return '\n'.join(out)

    # --------------------------------------------------------- verificador
    def verifica(self):
        prob = []
        # Elemento com x ou y negativo nasce FORA do frame. O frame comeca em
        # (0,0); bloco espelhado (cima=True) perto do topo pode estourar para
        # cima, e o verificador de sobreposicao nunca ve isso.
        for e in self.el:
            if e['x'] < 0 or e['y'] < 0:
                prob.append('FORA DO FRAME %s: (%.0f,%.0f)' % (e['id'], e['x'], e['y']))
        els = [e for e in self.el]
        for i in range(len(els)):
            for k in range(i + 1, len(els)):
                A, B = els[i], els[k]
                ox = min(A['x'] + A['w'], B['x'] + B['w']) - max(A['x'], B['x'])
                oy = min(A['y'] + A['h'], B['y'] + B['h']) - max(A['y'], B['y'])
                if ox > 1 and oy > 1:
                    cont = (A['x'] <= B['x'] and A['y'] <= B['y'] and
                            A['x'] + A['w'] >= B['x'] + B['w'] and A['y'] + A['h'] >= B['y'] + B['h']) or \
                           (B['x'] <= A['x'] and B['y'] <= A['y'] and
                            B['x'] + B['w'] >= A['x'] + A['w'] and B['y'] + B['h'] >= A['y'] + A['h'])
                    if not cont:
                        prob.append('SOBREPOE %s(%.0f,%.0f %.0fx%.0f) x %s(%.0f,%.0f %.0fx%.0f) -> %.0f x %.0f'
                                    % (A['id'], A['x'], A['y'], A['w'], A['h'],
                                       B['id'], B['x'], B['y'], B['w'], B['h'], ox, oy))
        # alinhamento: as 4 pecas de um bloco de trecho no mesmo x
        for own in sorted(set(e['owner'] for e in self.el if e['owner'] and e['owner'].startswith('t'))):
            pecas = [e for e in self.el if e['owner'] == own]
            base = [e for e in pecas if e['role'] in ('faixa_trecho', 'lista_payload', 'faixa_obs')]
            xs = set(round(e['x']) for e in base)
            if len(xs) > 1:
                prob.append('DESALINHADO %s: x=%s' % (own, sorted(xs)))
            for e in pecas:
                if e['role'] == 'obs' and round(e['x']) != round(min(xs) + RECUO):
                    prob.append('DESALINHADO card obs %s: x=%.0f esperado %.0f' % (e['id'], e['x'], min(xs) + RECUO))
            if not [e for e in pecas if e['role'] == 'faixa_obs']:
                prob.append('SEM BLOCO DE OBS: %s' % own)
        # alinhamento: pecas do bloco de explicacao no mesmo x do card
        for own in sorted(set(e['owner'] for e in self.el if e['owner'] and e['owner'].startswith('n'))):
            pecas = [e for e in self.el if e['owner'] == own]
            no = [e for e in pecas if e['role'] == 'no']
            if not no:
                continue
            cx = no[0]['x'] + no[0]['w'] / 2.0
            esperado = round(cx - CARD_W / 2)
            for e in pecas:
                if e['role'] in ('faixa_oquefaz', 'faixa_campos', 'lista_campos') and round(e['x']) != esperado:
                    prob.append('DESALINHADO %s %s: x=%.0f esperado %d' % (own, e['role'], e['x'], esperado))
                if e['role'] == 'postit' and round(e['x']) != esperado + RECUO:
                    prob.append('DESALINHADO postit %s: x=%.0f esperado %d' % (e['id'], e['x'], esperado + RECUO))
        # folga da lista de trecho ate a linha do corredor dela
        for e in self.el:
            if e['role'] == 'lista_payload':
                ly = self.trecho_ly.get(e['owner'])
                if ly is None:
                    continue
                folga = ly - (e['y'] + e['h'])
                if not (19 <= folga <= 23):
                    prob.append('FOLGA %s: %.1f (esperado 20)' % (e['owner'], folga))
            if e['role'] == 'faixa_obs':
                ly = self.trecho_ly.get(e['owner'])
                if ly is not None and abs((e['y'] - ly) - 20) > 1:
                    prob.append('FOLGA OBS %s: %.1f (esperado 20)' % (e['owner'], e['y'] - ly))
        return prob
