# -*- coding: utf-8 -*-
"""Exemplo mínimo, de ponta a ponta: cria um quadro pequeno (gatilho -> consulta
-> decisão -> dois desfechos), roda os verificadores e grava o SVG.

Serve pra ver o pipeline inteiro funcionando (Quadro -> forma() -> bloco_no()
-> bloco_trecho() -> conn() -> verifica() -> fecha()) antes de desenhar um
fluxo real. Os nomes dos nós são o mesmo exemplo genérico do SKILL.md
("lembrete de aniversário" por WhatsApp) — troque pelo seu fluxo.

Uso: python exemplo_uso.py
Gera exemplo_uso.svg nesta mesma pasta.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from quadro import Quadro
from legenda_fechamento import legenda, fecha

LINE_Y = 2600
q = Quadro('Exemplo — lembrete de aniversário', line_y=LINE_Y)

# --- nós, da esquerda para a direita, todos no centro da linha ---
# O vão entre nós precisa caber o BLOCO DE TRECHO inteiro (faixa+lista acima,
# 440px de largura), não só o rótulo do conector — por isso 900px aqui, bem
# mais que o mínimo de 300px citado para vãos sem bloco de trecho.
g1 = q.forma('n1', '1', 'Agenda diária 8h',      100,  LINE_Y, 'gatilho', forma='pilula')
g2 = q.forma('n2', '2', 'Busca aniversariantes', 1440, LINE_Y, 'consulta')
g3 = q.forma('n3', '3', 'Achou alguém?',         2780, LINE_Y, 'decisao', forma='rhombus')

# saídas(3) = 2 -> ramificação (ver SKILL.md, "Lado a lado ou ramificação? A
# decisão é MECÂNICA, lida do JSON"): "sim" sobe, "não" desce, coluna de dobra
# única entre a origem e os dois destinos.
Y_SIM, Y_NAO = LINE_Y - 700, LINE_Y + 700
X_DOBRA = g3['cx'] + 580   # ~360px da borda direita do nó 3

g4 = q.forma('n4', '4', 'Envia WhatsApp',        4280, Y_SIM, 'subfluxo', forma='hexagon')
g5 = q.forma('n5', '5', 'Grava log: nada hoje',  4280, Y_NAO, 'banco',    forma='grava')

# --- pontos de junção da dobra (regra: conector nunca diagonal, sempre reto
# na horizontal ou na vertical, com dobra nos pontos) ---
q.ponto('d1',  X_DOBRA, LINE_Y)
q.ponto('d1s', X_DOBRA, Y_SIM)
q.ponto('d1n', X_DOBRA, Y_NAO)

# --- conectores: sempre pelas laterais dos cards, nunca pelo topo/base ---
q.conn('n1', 'n2', '1 item')
q.conn('n2', 'n3', 'lista')
q.conn('n3', 'd1', '')
q.conn('d1', 'd1s', '')
q.conn('d1', 'd1n', '')
q.conn('d1s', 'n4', 'sim')
q.conn('d1n', 'n5', 'não')

# --- blocos de explicação: faixa "O que faz" + post-it(s) + faixa "Campos" + lista ---
q.bloco_no('n1', g1, 'Dispara a rotina todo dia às 8h.',
           ['Gatilho fixo, sem entrada. Existe só pra dar a largada do dia.'],
           'Campos', ['hora = 08:00'])
q.bloco_no('n2', g2, 'Busca quem faz aniversário hoje.',
           ['Consulta direta na base de clientes, filtrando pela data de hoje.'],
           'Campos', ['1. data = hoje', '2. campo = data_nascimento'])
q.bloco_no('n3', g3, 'Decide se tem alguém pra notificar hoje.',
           ['Se a lista veio vazia, não faz sentido seguir seguir — vira "não".'],
           'Campos', ['lista.length > 0'])
# cima=True espelha o bloco pra cima do nó — usado aqui só pra mostrar a
# variante (ver SKILL.md, "O bloco de explicação pode ficar ACIMA do nó").
q.bloco_no('n4', g4, 'Manda a mensagem de parabéns pelo WhatsApp.',
           ['Chamada a um subfluxo à parte — é ele quem fala com a API do WhatsApp.'],
           'Campos', ['telefone', 'nome'], cima=True)
q.bloco_no('n5', g5, 'Registra que rodou e não tinha ninguém.',
           ['Sem isso, uma falha silenciosa da consulta pareceria igual a "não tinha ninguém".'],
           'Campos', ['motivo = sem_aniversariante'], cima=True)

# --- trecho de linha entre dois nós lado a lado: o que passa nesse fio ---
q.bloco_trecho('t12', (g1['cx'] + g2['cx']) / 2, LINE_Y,
               'sai do 1 · entra no 2', ['{ }'],
               ['Sem payload: é só o disparo do relógio.'])
q.bloco_trecho('t23', (g2['cx'] + g3['cx']) / 2, LINE_Y,
               'sai do 2 · entra no 3', ['[{ nome, telefone, data_nascimento }, ...]'],
               ['Uma lista, não um item — pode ter zero, um ou vários aniversariantes.'])

legenda(q, [
    'Amarelo é sempre "o que faz". Observação (se houver) vai em card cinza.',
    'Forma diz o verbo do nó: pílula dispara, retângulo processa, losango decide.',
])

if __name__ == '__main__':
    prob = fecha(q, 'Exemplo — lembrete de aniversário', 'exemplo_uso.svg', frame_x=0, frame_y=0)
    sys.exit(1 if prob else 0)
