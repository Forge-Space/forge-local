#!/usr/bin/env python3
"""Export captured training sessions to ShareGPT JSONL format.

Usage:
  python3 export_training_data.py                    # → training_data.jsonl
  python3 export_training_data.py output.jsonl       # custom output path
  python3 export_training_data.py --stats            # show capture stats only
"""
import argparse
import json
from pathlib import Path

TRAINING_DIR = Path.home() / ".forge-training" / "sessions"


def load_sessions():
    if not TRAINING_DIR.exists():
        return []
    sessions = []
    for path in sorted(TRAINING_DIR.glob("*.json")):
        try:
            sessions.append(json.loads(path.read_text()))
        except Exception:
            pass
    return sessions


def print_stats(sessions):
    total_tokens = sum(
        s.get("usage", {}).get("prompt_tokens", 0)
        + s.get("usage", {}).get("completion_tokens", 0)
        for s in sessions
    )
    by_model: dict[str, int] = {}
    for s in sessions:
        m = s.get("model", "unknown")
        by_model[m] = by_model.get(m, 0) + 1

    print(f"Sessions captured : {len(sessions)}")
    print(f"Total tokens      : {total_tokens:,}")
    print("By model:")
    for model, count in sorted(by_model.items()):
        print(f"  {model}: {count}")


def to_sharegpt(session: dict) -> dict:
    return {
        "id": session.get("id"),
        "conversations": session.get("conversations", []),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="training_data.jsonl")
    parser.add_argument("--stats", action="store_true")
    args = parser.parse_args()

    sessions = load_sessions()

    if args.stats:
        print_stats(sessions)
        return

    with open(args.output, "w") as f:
        for s in sessions:
            f.write(json.dumps(to_sharegpt(s)) + "\n")

    print(f"Exported {len(sessions)} sessions → {args.output}")


if __name__ == "__main__":
    main()
