# Contributing

Contributions are welcome. This repo is part of the Forge Space ecosystem.

## What to contribute

- New Ollama Modelfiles for specialized roles
- Routing configs for other AI coding tools (Cursor, Windsurf, Codex CLI)
- Improvements to the training capture pipeline
- RAG indexing strategies for different repo types
- LoRA fine-tuning recipes tested on real sessions

## Process

1. Open an issue before large changes
2. Branch from `main` using `feature/`, `fix/`, or `chore/` prefix
3. Update `CHANGELOG.md` under `[Unreleased]`
4. Open a PR — CI must pass

## Code standards

- Python: functions <50 lines, no comments unless non-obvious
- Shell: `set -euo pipefail`, quote variables
- No speculative features — implement what's needed now
