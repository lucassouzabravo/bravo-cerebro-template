#!/bin/sh
# Calibra o conferir_conflito.py num repositorio temporario e descartavel.
# Cinco cenarios: A -> B/remocao -> B/ancora -> A aplicado -> B/fora da allowlist.
set -eu

ORIG="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$ORIG/conferir_conflito.py"
LAB="$(mktemp -d "${TMPDIR:-/tmp}/salve-conflito.XXXXXX")"
FILE="memory/context/decisoes/2026-08.md"
trap 'rm -rf "$LAB"' EXIT HUP INT TERM

roda() {
  esperado="$1"
  shift
  set +e
  python3 "$SCRIPT" "$@"
  codigo=$?
  set -e
  echo "   -> saida $codigo (esperado $esperado)"
  if [ "$codigo" -ne "$esperado" ]; then
    echo "FALHOU: saida $codigo, esperado $esperado" >&2
    exit 1
  fi
}

monta() {   # monta(conteudo_do_lado_local)
  rm -rf "$LAB/repo"
  mkdir -p "$LAB/repo"
  cd "$LAB/repo"
  git init -q .
  git config user.email t@t
  git config user.name t
  mkdir -p "$(dirname "$FILE")"
  printf '# Decisoes\n\n## Decisao velha um\n- corpo um\n\n## Decisao velha dois\n- corpo dois\n' > "$FILE"
  git add "$FILE"
  git commit -qm base
  git checkout -q -b servidor
  printf '# Decisoes\n\n## Decisao velha um\n- corpo um\n\n## Decisao velha dois\n- corpo dois\n\n## Do servidor\n- backup automatico\n' > "$FILE"
  git commit -qam servidor
  git checkout -q master
  printf '%s' "$1" > "$FILE"
  git commit -qam local
  git rebase servidor >/dev/null 2>&1 || true
}

echo "==================================================================="
echo "PASSO 1 - CASO A: os dois lados so acrescentam, ancoras diferentes"
echo "==================================================================="
monta '# Decisoes

## Decisao velha um
- corpo um

## Decisao velha dois
- corpo dois

## Do computador
- trabalho da noite
'
roda 0

echo
echo "==================================================================="
echo "PASSO 2 - CASO B por REMOCAO (o que a versao antiga deixava passar)"
echo "==================================================================="
monta '# Decisoes

## Decisao velha um
- corpo um

## Do computador
- trabalho da noite
'
roda 2

echo
echo "==================================================================="
echo "PASSO 3 - CASO B por ANCORA REPETIDA nos dois lados"
echo "==================================================================="
monta '# Decisoes

## Decisao velha um
- corpo um

## Decisao velha dois
- corpo dois

## Do servidor
- versao do computador, diferente
'
roda 2

echo
echo "==================================================================="
echo "PASSO 4 - VOLTA AO CASO A, e agora RESOLVE com --aplicar"
echo "==================================================================="
monta '# Decisoes

## Decisao velha um
- corpo um

## Decisao velha dois
- corpo dois

## Do computador
- trabalho da noite
'
roda 0 --aplicar
echo
echo "--- arquivo resolvido: as ancoras que sobraram ---"
grep '^## ' "$FILE" | sed 's/^/     /'
echo "--- marcadores restantes (esperado 0) ---"
if grep -q '^<<<<<<<\|^=======\|^>>>>>>>' "$FILE"; then
  echo "FALHOU: sobraram marcadores" >&2
  exit 1
else
  echo "     0"
fi
echo
echo "calibracao concluida; o lab temporario sera removido."

echo
echo "==================================================================="
echo "PASSO 5 - CASO B: arquivo fora da allowlist append-only"
echo "==================================================================="
FILE="memory/hot.md"
monta '# Decisoes

## Decisao velha um
- corpo um

## Decisao velha dois
- corpo dois

## Do computador
- trabalho da noite
'
roda 2
