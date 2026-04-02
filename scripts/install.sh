#!/usr/bin/env bash
# install.sh — Build Forge Ollama models on the workstation
# Run on the machine where Ollama is installed (oac-workstation)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODELS_DIR="$(dirname "$SCRIPT_DIR")/models"

if ! command -v ollama &>/dev/null; then
  echo "ERROR: ollama not found. Install from https://ollama.com" >&2
  exit 1
]

echo "==> Pulling base models..."
ollama pull qwen2.5-coder:14b
ollama pull llama3.1:8b-instruct-q4_K_M

echo "==> Building forge-dev:14b..."
ollama create forge-dev:14b -f "$MODELS_DIR/forge-dev.modelfile"

echo "==> Building forge-claude:14b..."
ollama create forge-claude:14b -f "$MODELS_DIR/forge-claude.modelfile"

echo ""
echo "Done. Available models:"
ollama list | grep -E 'forge|llama|qwen'
