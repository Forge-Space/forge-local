# forge-local

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/Forge-Space/forge-local)](https://github.com/Forge-Space/forge-local/releases)
[![Forge Space](https://img.shields.io/badge/forge--space-ecosystem-blueviolet)](https://github.com/Forge-Space)

Cloud models are powerful but expensive. Local models are cheap but lack context.

`forge-local` bridges the gap — custom Ollama models pre-loaded with Forge coding practices, a LiteLLM proxy that routes tasks to the right tier, training data capture that turns every cloud call into a future fine-tune, and a hybrid aider setup that drafts locally and polishes with Claude.

## Why This Exists

| Without it | With it |
|---|---|
| 100% of tasks hit Claude API | ~60% handled locally, ~30% Sonnet, ~10% Opus |
| Generic model with no project context | `forge-claude:14b` knows agent roles, routing, and ecosystem gotchas |
| Cloud spend with no learning loop | Every Claude call captured as training data |
| Manual model selection per task | Automatic routing by complexity via oh-my-openagent categories |
| Separate local and cloud workflows | Unified proxy — same API endpoint for all models |
| aider limited to one model | Hybrid: local drafts, Claude Sonnet edits |

## Quick Start

### 1) Pull and build the local models

```bash
# On your Ollama workstation:
bash scripts/install.sh
```

Builds `forge-dev:14b` (coding base) and `forge-claude:14b` (agent-aware) from Modelfiles.

### 2) Start the LiteLLM proxy

```bash
cd proxy
pip install litellm
litellm --config litellm-config.yaml
```

Proxy runs on port 4000. All Claude model names are remapped to local Ollama models.
Training data is captured automatically to `~/.forge-training/sessions/`.

### 3) Configure routing

Copy `routing/oh-my-opencode.json` to `~/.config/opencode/oh-my-opencode.json`.

This routes OpenCode agents and task categories to the right model tier:
- `quick` / `librarian` / `explore` → workstation (local)
- `unspecified-high` → Claude Sonnet
- `ultrabrain` / `deep` → Claude Opus

### 4) Set up aider hybrid mode

```bash
cp aider/aider.conf.yml ~/.aider.conf.yml
cat aider/aider-aliases.sh >> ~/.zshrc && source ~/.zshrc
```

Use `aider-hybrid` for local draft + Claude editor, `aider-local` for pure local, `aider-cloud` for full Opus.

### 5) Export training data

```bash
python3 proxy/export_training_data.py --stats
python3 proxy/export_training_data.py training_data.jsonl
```

## Repository Map

### `models/`

Ollama Modelfiles for Forge local models.

| File | Model | Use |
|---|---|---|
| `forge-dev.modelfile` | `forge-dev:14b` | General coding base — Qwen 2.5 Coder 14B + Forge standards |
| `forge-claude.modelfile` | `forge-claude:14b` | Agent-aware — inherits forge-dev + routing/ecosystem context |

### `proxy/`

LiteLLM proxy config and training data capture.

| File | Purpose |
|---|---|
| `litellm-config.yaml` | Routes Claude model names → local Ollama; starts on port 4000 |
| `forge_trainer.py` | LiteLLM CustomLogger — captures cloud calls as ShareGPT training pairs |
| `export_training_data.py` | CLI to export captured sessions to JSONL for fine-tuning |

### `routing/`

oh-my-openagent configuration for OpenCode multi-model routing.

| File | Purpose |
|---|---|
| `oh-my-opencode.json` | Agent + category routing with fallback chains |
| `AGENTS.md.template` | Drop-in AGENTS.md with category routing table and heuristics |

### `aider/`

Hybrid aider setup — local model drafts, Claude edits.

| File | Purpose |
|---|---|
| `aider.conf.yml` | Default config: `forge-dev:14b` primary, `claude-sonnet-4-6` editor |
| `aider-aliases.sh` | `aider-local`, `aider-hybrid`, `aider-cloud` shell aliases |

### `rag/`

Codebase indexing with nomic-embed-text + qdrant.
See [`rag/README.md`](rag/README.md) for setup.

### `training/`

LoRA fine-tuning pipeline using captured training data.
See [`training/README.md`](training/README.md) for setup.

### `scripts/`

| Script | What it does |
|---|---|
| `install.sh` | Builds Forge Ollama models from Modelfiles on the workstation |

## Architecture

```
Mac (Claude Code / OpenCode)
  │
  ├── oh-my-openagent routing
  │     quick/librarian/explore ──────────────────────► Ollama (workstation)
  │     unspecified-low ────────────────────────────► Ollama (workstation)
  │     unspecified-high ───────────────────────────► Claude Sonnet
  │     ultrabrain/deep ────────────────────────────► Claude Opus
  │
  ├── aider-hybrid
  │     draft ──────────────────────────────────────► forge-dev:14b (Ollama)
  │     edit  ──────────────────────────────────────► claude-sonnet-4-6
  │
  └── LiteLLM proxy (workstation :4000)
        claude-* / gpt-* names ──────────────────────► forge-dev:14b / forge-claude:14b
        ForgeTrainer callback ────────────────────────► ~/.forge-training/sessions/
```

## Model Distribution Target

~60% local (workstation), ~30% Claude Sonnet, ~10% Claude Opus.

## Requirements

- Ollama on workstation with 16GB+ VRAM
- LiteLLM: `pip install litellm`
- oh-my-openagent OpenCode plugin
- Tailscale (for workstation routing from Mac)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
