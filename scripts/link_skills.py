#!/usr/bin/env python3
"""Link this repository's skills without discarding existing installations."""

import argparse
from datetime import datetime
import os
from pathlib import Path
import sys


def main():
    codex_home = Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-dir", type=Path, default=codex_home / "skills")
    parser.add_argument("--backup-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parent.parent
    target = args.target_dir.expanduser().absolute()
    sources = sorted(p for p in (repo / "skills").iterdir() if (p / "SKILL.md").is_file())
    if not sources:
        parser.error("No skills found in this repository.")
    pending = []
    for source in sources:
        destination = target / source.name
        if destination.is_symlink() and destination.resolve() == source.resolve():
            print(f"Already linked: {source.name}")
            continue
        if os.path.lexists(destination) and not args.backup_existing:
            parser.error(f"Existing installation: {destination}. Use --backup-existing to preserve it before linking.")
        pending.append((source, destination))

    if args.dry_run:
        for source, destination in pending:
            action = "Back up and link" if os.path.lexists(destination) else "Link"
            print(f"{action}: {destination} -> {source}")
        return

    backup = codex_home / "skill-backups" / repo.name / datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    changes = []
    try:
        target.mkdir(parents=True, exist_ok=True)
        for source, destination in pending:
            old = None
            if os.path.lexists(destination):
                backup.mkdir(parents=True, exist_ok=True)
                old = backup / destination.name
                destination.rename(old)
            changes.append((destination, old))
            destination.symlink_to(source, target_is_directory=True)
            print(f"Linked: {destination} -> {source}")
    except Exception:
        for destination, old in reversed(changes):
            if destination.is_symlink():
                destination.unlink()
            if old is not None:
                old.rename(destination)
        raise
    if backup.exists():
        print(f"Original installations preserved: {backup}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        sys.exit(1)
