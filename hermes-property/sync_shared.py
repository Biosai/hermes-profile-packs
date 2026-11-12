#!/usr/bin/env python3
"""Copy shared/RULES.md into the shared-rules block at the end of every SOUL.md.

The canonical team rules live once in shared/RULES.md. Each profile's SOUL.md
ends with:

    <!-- shared-rules:start -->
    ...RULES.md, byte for byte...
    <!-- shared-rules:end -->

Run without arguments to rewrite every block; run with --check to report
SOULs whose block differs from RULES.md without changing anything (exit 1).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RULES = ROOT / "shared" / "RULES.md"
START = "<!-- shared-rules:start -->\n"
END = "<!-- shared-rules:end -->\n"


def expected_soul(text: str, rules: str) -> str:
    """Return the SOUL text with its shared block replaced by the canonical rules."""
    index = text.find(START)
    if index == -1:
        body = text.rstrip("\n") + "\n\n"
    else:
        body = text[:index]
    return body + START + rules + END


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="Report drift without writing (exit 1 on drift).")
    args = parser.parse_args()

    rules = RULES.read_text(encoding="utf-8")
    if not rules.endswith("\n"):
        rules += "\n"
    if START in rules or END in rules:
        print("error: shared/RULES.md must not contain the block markers", file=sys.stderr)
        return 2

    souls = sorted((ROOT / "profiles").glob("*/SOUL.md"))
    if not souls:
        print("error: no profiles/*/SOUL.md found", file=sys.stderr)
        return 2

    drift: list[str] = []
    for soul in souls:
        text = soul.read_text(encoding="utf-8")
        if text.count(START) > 1 or text.count(END) > 1:
            print(f"error: {soul.relative_to(ROOT)} has more than one shared-rules block", file=sys.stderr)
            return 2
        updated = expected_soul(text, rules)
        if updated == text:
            continue
        drift.append(str(soul.relative_to(ROOT)))
        if not args.check:
            soul.write_text(updated, encoding="utf-8")

    if args.check:
        if drift:
            for path in drift:
                print(f"out of sync: {path}", file=sys.stderr)
            print("run: python sync_shared.py", file=sys.stderr)
            return 1
        print(f"shared rules in sync: {len(souls)} SOULs")
        return 0
    print(f"shared rules synced: {len(drift)} of {len(souls)} SOULs rewritten")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
