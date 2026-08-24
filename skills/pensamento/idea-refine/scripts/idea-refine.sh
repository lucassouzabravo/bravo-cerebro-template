#!/bin/bash
set -e

# This script helps initialize the ideas directory for the idea-refine skill.
# Destino padrão: a pasta de ideias do cérebro.
# não docs/ideas (ver "Output" em SKILL.md).

IDEAS_DIR="memory/context/ideias"

if [ ! -d "$IDEAS_DIR" ]; then
  mkdir -p "$IDEAS_DIR"
  echo "Created directory: $IDEAS_DIR" >&2
else
  echo "Directory already exists: $IDEAS_DIR" >&2
fi

echo "{\"status\": \"ready\", \"directory\": \"$IDEAS_DIR\"}"
