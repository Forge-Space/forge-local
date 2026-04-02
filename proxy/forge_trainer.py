"""ForgeTrainer — LiteLLM CustomLogger that captures cloud API calls as ShareGPT training pairs.

Place this file where PYTHONPATH can find it (e.g. ~/forge_trainer.py with PYTHONPATH=~).
Captures to ~/.forge-training/sessions/{uuid}.json.
Filters: cloud models only, min 50-char response, must have a user message.
"""
import json
import os
import uuid
from datetime import datetime

from litellm.integrations.custom_logger import CustomLogger

TRAINING_DIR = os.path.expanduser("~/.forge-training/sessions")

LOCAL_PREFIXES = (
    "forge-dev",
    "forge-claude",
    "ollama",
    "llama",
    "qwen",
    "mistral",
)


class ForgeTrainer(CustomLogger):
    def __init__(self):
        os.makedirs(TRAINING_DIR, exist_ok=True)

    def _is_cloud_call(self, model: str) -> bool:
        model_lower = (model or "").lower()
        return not any(model_lower.startswith(p) for p in LOCAL_PREFIXES)

    def log_success_event(self, kwargs, response_obj, start_time, end_time):
        try:
            model = kwargs.get("model", "")
            if not self._is_cloud_call(model):
                return

            messages = kwargs.get("messages", [])
            user_messages = [m for m in messages if m.get("role") == "user"]
            if not user_messages:
                return

            choices = getattr(response_obj, "choices", [])
            if not choices:
                return

            response_text = choices[0].message.content or ""
            if len(response_text) < 50:
                return

            conversation = []
            for msg in messages:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if isinstance(content, list):
                    content = " ".join(
                        c.get("text", "") for c in content if isinstance(c, dict)
                    )
                if role in ("system", "user", "assistant") and content:
                    conversation.append({"from": role, "value": content})

            conversation.append({"from": "assistant", "value": response_text})

            usage = getattr(response_obj, "usage", None)
            session = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "model": model,
                "conversations": conversation,
                "usage": {
                    "prompt_tokens": getattr(usage, "prompt_tokens", 0) if usage else 0,
                    "completion_tokens": getattr(usage, "completion_tokens", 0) if usage else 0,
                },
            }

            path = os.path.join(TRAINING_DIR, f"{session['id']}.json")
            with open(path, "w") as f:
                json.dump(session, f, indent=2)

        except Exception:
            pass


forge_trainer = ForgeTrainer()
