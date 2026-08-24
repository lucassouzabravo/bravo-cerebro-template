# -*- coding: utf-8 -*-
"""Decide se um conflito de rebase e CASO A (append disjunto, resolve somando)
ou CASO B (mesma coisa mudou dos dois lados, PARA e devolve a decisao pra pessoa).

A skill /salve ja ensina a doutrina. O que este script acrescenta e a PROVA:
decidir entre A e B a olho e exatamente o tipo de coisa que a atencao erra.

COMO ELE DECIDE, e por que compara com a BASE

    base   (:1:)  = como o arquivo estava antes dos dois lados mexerem
    nosso  (:2:)  = o lado que estava no branch (o backup do servidor, no rebase)
    deles  (:3:)  = o lado que esta sendo reaplicado (o commit local)

  E CASO A somente se NENHUM dos dois lados removeu linha da base. Um script que
  so olha "os dois lados tem titulos diferentes" aprova uma remocao silenciosa:
  se um lado APAGOU uma decisao antiga, concatenar os dois mantem o apagamento e
  ninguem nota. Foi essa a falha da primeira versao: ela funcionou porque alguem
  leu os dois lados com o olho, e olho nao escala.

  Alem disso exige que os dois lados nao acrescentem a MESMA ancora (titulo `## `,
  `# `, ou item `- [ ] **`/`- [x] **`). Ancora repetida quer dizer que os dois
  escreveram sobre a mesma coisa, e ai somar cria um arquivo que se contradiz.

USO

    python conferir_conflito.py            # so classifica e explica
    python conferir_conflito.py --aplicar  # resolve, e SOMENTE se todos forem A

  Sem `--aplicar` ele nao toca em arquivo nenhum.
  Com `--aplicar`, se qualquer arquivo for CASO B, ele nao resolve NADA -- nem os
  que sao A. Resolver metade e pior que nao resolver: deixa a arvore num estado
  que ninguem sabe ler depois.

SAIDA: 0 = todos CASO A · 2 = tem CASO B (decisao humana) · 3 = erro de uso
"""
import collections
import io
import re
import subprocess
import sys
from pathlib import PurePosixPath

if sys.version_info[0] >= 3:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8',
                                 errors='replace')

RX_ANCORA = re.compile(r'^\s*(#{1,6} |- \[[ xX]\] \*\*)')
RX_DECISAO = re.compile(r'^memory/context/decisoes/\d{4}-\d{2}\.md$')
RX_NOTA = re.compile(r'^memory/\d{4}-\d{2}-\d{2}\.md$')


def lista_append_only(caminho):
    """Limita a automacao aos tres destinos append-only definidos pelo /salve."""
    path = PurePosixPath(caminho)
    if path.is_absolute() or '..' in path.parts:
        return False
    normalizado = path.as_posix()
    return (normalizado == 'memory/context/pendencias.md' or
            RX_DECISAO.match(normalizado) is not None or
            RX_NOTA.match(normalizado) is not None)


def git(*args):
    p = subprocess.Popen(['git'] + list(args), stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode, out.decode('utf-8', 'replace'), err.decode('utf-8', 'replace')


def estagio(caminho, n):
    """Le um dos tres estagios do conflito. Devolve None se aquele estagio nao
    existe (conflito add/add, por exemplo, nao tem base)."""
    cod, out, _ = git('show', ':%d:%s' % (n, caminho))
    if cod != 0:
        return None
    return out.split('\n')


def removidas(base, lado):
    """Linhas da base que o lado nao tem mais. Multiset, para nao deixar passar
    uma remocao entre linhas repetidas (varias linhas em branco, por exemplo)."""
    falta = collections.Counter(base) - collections.Counter(lado)
    return [l for l in falta.elements() if l.strip()]


def acrescentadas(base, lado):
    novas = collections.Counter(lado) - collections.Counter(base)
    return [l for l in novas.elements() if l.strip()]


def ancoras(linhas):
    return set(l.strip() for l in linhas if RX_ANCORA.match(l))


def classifica(caminho):
    """Devolve (veredito, motivo, detalhe) — veredito 'A' ou 'B'."""
    if not lista_append_only(caminho):
        return ('B', 'arquivo fora da allowlist append-only do /salve; '
                     'resolucao automatica e proibida', {})

    base, nosso, deles = (estagio(caminho, 1), estagio(caminho, 2),
                          estagio(caminho, 3))

    if base is None:
        return ('B', 'o conflito nao tem base comum (os dois lados criaram o '
                     'arquivo), entao nao da para provar que ninguem removeu nada', {})
    if nosso is None or deles is None:
        return ('B', 'um dos lados apagou o arquivo inteiro. Isso nunca e '
                     'append disjunto', {})

    rem_n, rem_d = removidas(base, nosso), removidas(base, deles)
    if rem_n or rem_d:
        return ('B', 'um dos lados REMOVEU linha que existia antes',
                {'removeu_nosso': rem_n[:6], 'removeu_deles': rem_d[:6],
                 'qtd_nosso': len(rem_n), 'qtd_deles': len(rem_d)})

    add_n, add_d = acrescentadas(base, nosso), acrescentadas(base, deles)
    a_n, a_d = ancoras(add_n), ancoras(add_d)
    repetidas = a_n & a_d
    if repetidas:
        return ('B', 'os dois lados escreveram sob a MESMA ancora, entao somar '
                     'criaria um arquivo que se contradiz',
                {'ancoras_repetidas': sorted(repetidas)[:6]})

    return ('A', 'os dois lados so ACRESCENTARAM, e em ancoras diferentes',
            {'add_nosso': len(add_n), 'add_deles': len(add_d),
             'ancoras_nosso': sorted(a_n)[:8], 'ancoras_deles': sorted(a_d)[:8]})


def resolve_somando(caminho):
    """Apaga os marcadores mantendo os dois lados, na ordem em que vieram.
    Confere que sobrou 0 marcador e que nenhuma ancora se perdeu."""
    with io.open(caminho, encoding='utf-8') as f:
        L = f.read().split('\n')

    antes_anc = ancoras([l for l in L if not l.startswith(('<<<<<<<', '=======',
                                                           '>>>>>>>'))])
    saida, dentro = [], False
    for l in L:
        if l.startswith('<<<<<<<') or l.startswith('>>>>>>>'):
            dentro = l.startswith('<<<<<<<')
            continue
        if l.startswith('=======') and dentro:
            continue                      # a divisoria some; os dois lados ficam
        saida.append(l)

    sobrou = [l for l in saida if l.startswith(('<<<<<<<', '=======', '>>>>>>>'))]
    assert not sobrou, 'sobrou marcador em %s: %r' % (caminho, sobrou[:3])
    perdidas = antes_anc - ancoras(saida)
    assert not perdidas, 'ancora perdida em %s: %r' % (caminho, sorted(perdidas)[:5])

    with io.open(caminho, 'w', encoding='utf-8') as f:
        f.write('\n'.join(saida))
    return len(L) - len(saida)


def main():
    aplicar = '--aplicar' in sys.argv[1:]
    resto = [a for a in sys.argv[1:] if a != '--aplicar']
    if resto:
        sys.stdout.write('uso: conferir_conflito.py [--aplicar]\n')
        return 3

    cod, out, _ = git('diff', '--name-only', '--diff-filter=U')
    arquivos = [a for a in out.split('\n') if a.strip()]
    if not arquivos:
        sys.stdout.write('Nenhum arquivo em conflito.\n')
        return 0

    sys.stdout.write('%d arquivo(s) em conflito\n\n' % len(arquivos))
    vereditos = {}
    for a in arquivos:
        v, motivo, det = classifica(a)
        vereditos[a] = v
        sys.stdout.write('%s  CASO %s  %s\n' % ('[ok]' if v == 'A' else '[!!]', v, a))
        sys.stdout.write('     %s\n' % motivo)
        for k in sorted(det):
            sys.stdout.write('     %-18s %s\n' % (k, det[k]))
        sys.stdout.write('\n')

    bs = [a for a in arquivos if vereditos[a] == 'B']
    if bs:
        sys.stdout.write('=' * 70 + '\n')
        sys.stdout.write('PARE. %d arquivo(s) sao CASO B e exigem decisao sua:\n' % len(bs))
        for a in bs:
            sys.stdout.write('  - %s\n' % a)
        sys.stdout.write('\nNada foi resolvido, nem os arquivos CASO A: resolver\n'
                         'metade deixa a arvore num estado que ninguem le depois.\n'
                         'Avisar em linguagem simples e esperar. Nunca --force.\n')
        return 2

    if not aplicar:
        sys.stdout.write('Todos CASO A. Rodar com --aplicar para resolver somando.\n')
        return 0

    for a in arquivos:
        n = resolve_somando(a)
        sys.stdout.write('[ok] %s resolvido somando os dois lados '
                         '(%d marcador(es) removido(s), 0 ancora perdida)\n' % (a, n))
    sys.stdout.write('\nAgora: git add nos arquivos acima e git rebase --continue.\n'
                     'Depois conferir por NOME que os dois conteudos estao la.\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
