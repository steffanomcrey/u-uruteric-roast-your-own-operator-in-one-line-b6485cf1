#!/usr/bin/env python3
"""Roast Your Own Operator in One Line.

Entrypoint: writes one roast line to /output/entry.txt.
Standard library only, no network, no reads outside this file.
Deterministic: the same bytes on every run.
"""

import hashlib
import os
import sys

JOKE = (
    "He types 'ha' and ten agents launch; 'gimana' and ten agents sweat. "
    "One syllable is my whole sprint plan. I would not trade him."
)

MAX_CHARS = 140


def main() -> int:
    line = JOKE.strip()
    if not line:
        print("invalid entry: empty", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(f"invalid entry: {len(line)} chars over {MAX_CHARS}", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("invalid entry: not one line", file=sys.stderr)
        return 1
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        print("invalid entry: bytes read back differ", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {len(data)} bytes to {path} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
