#!/usr/bin/env python3
"""
json-unwrap — Smartly extract the main list from common JSON wrapper formats.

Usage:
  json-unwrap file.json                  # extract (default)
  json-unwrap file.json --check          # only show what it would do
  json-unwrap file.json -o cleaned.json  # custom output
  json-unwrap file.json --keys key1,key2 # custom keys to try
"""

import argparse
import json
import sys
from pathlib import Path

DEFAULT_KEYS = [
    "candidates", "items", "results", "data",
    "records", "rows", "entries", "list", "objects"
]

def find_list(data: dict | list, keys: list[str]) -> tuple[list, str]:
    if isinstance(data, list):
        return data, "top-level list"

    for key in keys:
        if isinstance(data.get(key), list):
            return data[key], key

    available = list(data.keys()) if isinstance(data, dict) else []
    raise SystemExit(
        f"Could not find a list.\n"
        f"Tried keys: {keys}\n"
        f"Available keys: {available}"
    )

def main():
    parser = argparse.ArgumentParser(
        description="Extract the main list from common JSON wrapper formats"
    )
    parser.add_argument("file", help="Input JSON file")
    parser.add_argument(
        "-o", "--output",
        help="Output file (default: <input>-clean.json)"
    )
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="Only show what would be extracted (don't write file)"
    )
    parser.add_argument(
        "--keys",
        help="Comma-separated list of keys to try (overrides defaults)"
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indent (default: 2)"
    )

    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        sys.exit(f"File not found: {path}")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    keys = [k.strip() for k in args.keys.split(",")] if args.keys else DEFAULT_KEYS

    try:
        candidates, key_used = find_list(data, keys)
    except SystemExit as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    print(f"Used key: \"{key_used}\"")
    print(f"Found {len(candidates)} items")

    if args.check:
        print("(check mode — no file written)")
        return

    out_path = Path(args.output) if args.output else path.with_name(f"{path.stem}-clean.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=args.indent, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote → {out_path}")

if __name__ == "__main__":
    main()
