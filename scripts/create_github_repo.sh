#!/usr/bin/env bash
# Crea el repositorio en GitHub y sube el commit inicial.
# Pre-requisito: autenticarse una sola vez con  ->  gh auth login
set -euo pipefail

REPO_NAME="reflex-rosencharts"
VISIBILITY="--public"   # cambia a --private si lo prefieres

cd "$(dirname "$0")/.."

if ! gh auth status >/dev/null 2>&1; then
  echo "No estás autenticado en gh. Ejecuta primero:  gh auth login"
  exit 1
fi

# Crea el repo bajo tu cuenta, usa el directorio actual como source y hace push.
gh repo create "$REPO_NAME" $VISIBILITY \
  --source=. \
  --remote=origin \
  --description "Port de rosencharts (D3+Tailwind) a custom components de Reflex" \
  --push

echo "Listo: repositorio creado y push realizado."
gh repo view --web
