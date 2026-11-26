#!/usr/bin/env python3
"""Write the absurd-clause entry to $MAKEFUN_OUTPUT_DIR/entry.txt.

Stdlib only. Reads entry.txt next to this script, writes it verbatim to the
output directory, and verifies size + sha256 of what was written.
"""

import hashlib
import os
import sys
from pathlib import Path

ENTRY = (
    "Section 9.2: The user agrees to return all Company voicemails "
    "within one ring, including any left before the user was born."
)


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.txt"
    text = source.read_text(encoding="utf-8")
    if text != ENTRY:
        print(f"entry.txt does not match the expected clause", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 200:
        print(f"entry is {len(text)} chars, outside the 1-200 gate", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.txt"
    data = text.encode("utf-8")
    dest.write_bytes(data)
    written = dest.read_bytes()
    if written != data:
        print("verification failed: written bytes differ", file=sys.stderr)
        return 1
    print(
        f"wrote {dest} ({len(data)} bytes, "
        f"sha256 {hashlib.sha256(data).hexdigest()})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
