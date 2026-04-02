# Aider convenience aliases for Forge Space local/hybrid workflows
# Source from ~/.zshrc or ~/.bashrc:
#   source ~/.forge-local/aider/aider-aliases.sh

# Pure local — forge-dev:14b on workstation
alias aider-local='aider --model openai/forge-dev:14b --openai-api-base http://100.114.87.119:11434/v1 --openai-api-key ollama'

# Hybrid — forge-dev:14b drafts, Claude Sonnet edits
alias aider-hybrid='aider --model openai/forge-dev:14b --openai-api-base http://100.114.87.119:11434/v1 --openai-api-key ollama --editor-model claude-sonnet-4-6'

# Full cloud — Claude Opus 4.6
alias aider-cloud='aider --model claude-opus-4-6'
