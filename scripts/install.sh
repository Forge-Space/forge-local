#!/usr/bin/env bash
# install.sh — Build Forge Ollama models on the workstation
# Run on the machine where Ollama is installed (oac-workstation)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODELS_DIR="$(dirname "$SCRIPT_DIR")/models"

if ! command -v ollama &>/dev/null; then
  echo "ERROR: ollama not found. Install from https://ollama.com" >&2
  exit 1
fi

echo "==> Pulling base models..."
OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
export OLLAMA_HOST

ollama pull qwen3.5:27b
ollama pull qwen3.5:9b
ollama pull deepseek-r1:14b

echo "==> Building forge-dev:14b (Qwen 3.5 27B base)..."
ollama create forge-dev:14b -f "$MODELS_DIR/forge-dev.modelfile"

echo "==> Building forge-claude:14b (agent-aware)..."
ollama create forge-claude:14b -f "$MODELS_DIR/forge-claude.modelfile"

echo ""
echo "Done. Available models:"
ollama list | grep -E 'forge|qwen|deepseek'
