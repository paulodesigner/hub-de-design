#!/usr/bin/env bash
# Adota um agente do catálogo (agentes-catalogo/) para o seu escopo PESSOAL
# (~/.claude/agents/). Fica disponível só para você; NÃO mexe no repo
# compartilhado nem afeta o time. Pra remover depois: rm ~/.claude/agents/<nome>.md
#
# Uso: scripts/adotar-agente.sh <nome>
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CATALOG="$HERE/../agentes-catalogo"
DEST_DIR="$HOME/.claude/agents"
NOME="${1:-}"

listar() {
  echo "Disponíveis no catálogo:"
  local found=0 f b
  for f in "$CATALOG"/*.md; do
    [[ -e "$f" ]] || continue
    b="$(basename "$f")"
    case "$b" in README.md|CATALOG.md) continue ;; esac
    echo "  • ${b%.md}"
    found=1
  done
  [[ "$found" == 1 ]] || echo "  (catálogo vazio)"
}

if [[ -z "$NOME" ]]; then
  echo "Uso: scripts/adotar-agente.sh <nome>"
  listar
  exit 1
fi

SRC="$CATALOG/${NOME}.md"
if [[ ! -f "$SRC" ]]; then
  echo "❌ Não achei '${NOME}' no catálogo (agentes-catalogo/${NOME}.md)."
  listar
  exit 1
fi

mkdir -p "$DEST_DIR"
cp "$SRC" "$DEST_DIR/${NOME}.md"
echo "✅ Agente '${NOME}' adotado em ~/.claude/agents/ — disponível só pra você."
echo "   (abra uma sessão nova pra ele aparecer; pra remover: rm ~/.claude/agents/${NOME}.md)"
