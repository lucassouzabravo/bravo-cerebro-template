#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera os adaptadores de `.claude/skills/` a partir das skills canonicas.

POR QUE ISTO EXISTE

  A skill de verdade mora em `skills/{categoria}/{nome}/SKILL.md`, organizada por
  proposito. O Claude Code, por outro lado, procura skills numa pasta plana em
  `.claude/skills/{nome}/`.

  Manter as duas na mao significa duas copias do mesmo texto, e duas copias sempre
  divergem. Entao `.claude/skills/` e GERADO: cada adaptador tem so o frontmatter
  (copiado byte a byte) mais um `@import` apontando para a canonica. O corpo nunca
  e duplicado.

  Consequencia pratica: NUNCA edite nada dentro de `.claude/skills/`. Edite a
  canonica e rode este script.

USO

    python scripts/sync_runtime_adapters.py            # gera
    python scripts/sync_runtime_adapters.py --conferir # so confere, nao escreve

  Sem `--conferir` ele escreve. Com, ele sai com codigo 1 se algo estiver
  dessincronizado -- util antes de enviar ao GitHub.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CANONICAS = REPO / 'skills'
RUNTIME = REPO / '.claude' / 'skills'

# Pastas irmas da SKILL.md que viajam junto com o adaptador.
ASSETS = ('referencias', 'references', 'scripts', 'assets', 'exemplos', 'examples')


def frontmatter(texto: str, origem: Path) -> str:
    """Devolve o bloco --- ... --- do topo. Sem ele o Claude nao descobre a skill."""
    m = re.match(r'\A(---\n.*?\n---\n)', texto, re.S)
    if not m:
        raise SystemExit('ERRO: %s nao tem frontmatter YAML no topo.' % origem)
    return m.group(1)


def nome_da_skill(texto: str, origem: Path) -> str:
    m = re.search(r'^name:\s*["\']?([^"\'\n]+)', texto, re.M)
    if not m:
        raise SystemExit('ERRO: %s nao tem o campo `name:` no frontmatter.' % origem)
    return m.group(1).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--conferir', action='store_true',
                    help='nao escreve; sai com 1 se algo estiver dessincronizado')
    args = ap.parse_args()

    canonicas = sorted(CANONICAS.glob('*/*/SKILL.md'))
    if not canonicas:
        raise SystemExit('ERRO: nenhuma skill encontrada em skills/{categoria}/{nome}/SKILL.md')

    # O namespace de .claude/skills/ e PLANO. Duas categorias com o mesmo nome de
    # pasta colidiriam e uma sobrescreveria a outra em silencio.
    pastas = [p.parent.name for p in canonicas]
    duplicadas = sorted({n for n in pastas if pastas.count(n) > 1})
    if duplicadas:
        raise SystemExit(
            'ERRO: nome de pasta repetido entre categorias: %s\n'
            'O Claude Code usa uma pasta plana, entao o nome tem que ser unico '
            'no cerebro inteiro.' % ', '.join(duplicadas)
        )

    esperadas = set()
    divergentes = []

    for skill in canonicas:
        texto = skill.read_text(encoding='utf-8')
        nome_pasta = skill.parent.name
        nome_da_skill(texto, skill)  # valida; erro para o script
        esperadas.add(nome_pasta)

        destino = RUNTIME / nome_pasta
        relativo = '../../../' + skill.relative_to(REPO).as_posix()
        adaptador = frontmatter(texto, skill) + '\n# Adaptador de runtime\n\n@%s\n' % relativo

        alvo = destino / 'SKILL.md'
        atual = alvo.read_text(encoding='utf-8') if alvo.exists() else None

        if atual != adaptador:
            divergentes.append(nome_pasta)
            if not args.conferir:
                destino.mkdir(parents=True, exist_ok=True)
                alvo.write_text(adaptador, encoding='utf-8')

        # Assets sao COPIADOS, nao linkados: link simbolico nao e confiavel no Windows.
        if not args.conferir:
            for nome_asset in ASSETS:
                origem_asset = skill.parent / nome_asset
                destino_asset = destino / nome_asset
                if not origem_asset.is_dir():
                    # A canonica nao tem (mais) esse asset. Se o adaptador tem, e
                    # sobra de um rename anterior -- e sobra de asset e pior que
                    # sobra de skill, porque nao aparece como orfa na varredura
                    # de pastas e fica sendo lida como se fosse atual.
                    if destino_asset.is_dir():
                        shutil.rmtree(destino_asset)
                        print('  removido asset orfao: %s/%s' % (nome_pasta, nome_asset))
                    continue
                if destino_asset.exists():
                    shutil.rmtree(destino_asset)
                shutil.copytree(origem_asset, destino_asset)

    # Adaptador cuja canonica sumiu vira lixo que o Claude ainda descobre.
    orfaos = []
    if RUNTIME.exists():
        for pasta in sorted(RUNTIME.iterdir()):
            if pasta.is_dir() and pasta.name not in esperadas:
                orfaos.append(pasta.name)
                if not args.conferir:
                    shutil.rmtree(pasta)

    print('canonicas encontradas: %d' % len(canonicas))
    for p in canonicas:
        print('  %s/%s' % (p.parent.parent.name, p.parent.name))

    if args.conferir:
        problemas = divergentes + orfaos
        if problemas:
            print('\nDESSINCRONIZADO:')
            for n in divergentes:
                print('  adaptador desatualizado: %s' % n)
            for n in orfaos:
                print('  adaptador orfao (canonica sumiu): %s' % n)
            print('\nRode sem --conferir para corrigir.')
            sys.exit(1)
        print('\nOK: .claude/skills/ esta em dia.')
    else:
        print('\ngerados/atualizados: %d' % len(divergentes))
        print('orfaos removidos:    %d' % len(orfaos))
        print('\nReinicie o Claude Code para ele enxergar as mudancas.')


if __name__ == '__main__':
    main()
