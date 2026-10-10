#!/usr/bin/env python3
"""Read the current planning principles from the configured Obsidian vault."""

import json
import os
from pathlib import Path
import sys


def main():
    configured = os.environ.get("PERSONAL_RECORD_VAULT")
    config = Path(__file__).resolve().parents[3] / "config" / "local.json"
    if not configured and config.is_file():
        configured = json.loads(config.read_text(encoding="utf-8")).get("personal_record_vault")
    if configured is not None and (not isinstance(configured, str) or not configured.strip()):
        raise ValueError("personal_record_vault must be a non-empty path.")
    vault = Path(configured or "~/repo/personal-record").expanduser()
    if not vault.is_absolute():
        raise ValueError("Use an absolute or ~/ path for personal_record_vault.")
    principles = vault / "2_Areas" / "일상과 회고" / "운영 원칙.md"
    print(f"Source: {principles}\n\n{principles.read_text(encoding='utf-8')}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, AttributeError) as error:
        print(f"Cannot read planning principles: {error}", file=sys.stderr)
        sys.exit(1)
