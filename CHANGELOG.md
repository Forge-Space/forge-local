# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.1.0] - 2026-04-01

### Added
- `models/forge-dev.modelfile` — Qwen 2.5 Coder 14B base with Forge coding standards system prompt
- `models/forge-claude.modelfile` — agent-aware model extending forge-dev with oh-my-openagent routing context and Forge ecosystem gotchas
- `proxy/litellm-config.yaml` — LiteLLM proxy routing Claude/GPT model names to local Ollama models; training callback enabled
- `proxy/forge_trainer.py` — LiteLLM CustomLogger that captures cloud API calls as ShareGPT-format training pairs in `~/.forge-training/sessions/`
- `proxy/export_training_data.py` — CLI to export captured sessions to ShareGPT JSONL for LoRA fine-tuning; supports `--stats` flag
- `routing/oh-my-opencode.json` — oh-my-openagent config with 11 agents + 10 routing categories; fallback chains for all entries
- `routing/AGENTS.md.template` — AGENTS.md template with category routing table, heuristics, and inline routing guide
- `aider/aider.conf.yml` — hybrid aider config: forge-dev:14b as main model, claude-sonnet-4-6 as editor
- `aider/aider-aliases.sh` — `aider-local`, `aider-hybrid`, `aider-cloud` shell aliases
- `rag/README.md` — RAG setup guide: nomic-embed-text embeddings + qdrant vector DB + codebase indexing
- `training/README.md` — fine-tuning guide: session capture → ShareGPT export → unsloth LoRA → Ollama import
- `scripts/install.sh` — workstation setup script: pulls base models + builds forge-dev and forge-claude via Modelfile
- `.github/workflows/release.yml` — auto tag + GitHub release on CHANGELOG version bump
- `.github/workflows/secret-scan.yml` — TruffleHog secret scanning on push/PR
