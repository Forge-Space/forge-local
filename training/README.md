# Training — LoRA Fine-Tuning Pipeline

Captures cloud API calls → exports as ShareGPT JSONL → fine-tunes local models with unsloth.

## Pipeline

```
Cloud API call
  └── ForgeTrainer (LiteLLM callback)
        └── ~/.forge-training/sessions/{uuid}.json
              └── export_training_data.py
                    └── training_data.jsonl (ShareGPT format)
                          └── unsloth LoRA fine-tune
                                └── ollama create forge-dev-ft:14b
```

## Capture

The proxy captures automatically. Check what you have:

```bash
python3 ../proxy/export_training_data.py --stats
```

## Export

```bash
python3 ../proxy/export_training_data.py training_data.jsonl
```

## Fine-tuning (unsloth)

### Requirements

```bash
# ROCm (AMD GPU):
pip install torch --index-url https://download.pytorch.org/whl/rocm6.2
pip install unsloth
```

> **Note:** unsloth ROCm support is experimental. RX 9070 XT (gfx1201) may require
> `HSA_OVERRIDE_GFX_VERSION=11.0.0` or building from source.

### Run fine-tune

Scripts coming soon — background agent is generating these.

- `finetune.py` — unsloth LoRA training script (ShareGPT → merged model)
- `finetune.sh` — wrapper with default hyperparameters

### Export to Ollama

```bash
# After fine-tune completes:
ollama create forge-dev-ft:14b -f /path/to/output/Modelfile
```

## Hyperparameter Defaults

| Parameter | Value | Notes |
|---|---|---|
| `r` | 16 | LoRA rank |
| `lora_alpha` | 16 | Alpha |
| `learning_rate` | 2e-4 | Standard for Qwen 2.5 |
| `num_train_epochs` | 3 | Adjust based on dataset size |
| `max_seq_length` | 2048 | Match model context |
