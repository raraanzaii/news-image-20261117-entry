#!/usr/bin/env python3
"""make.fun news-image-20261117 entry: "Sum up 17 November's world news in one image".

The entry image (entry.png, drawn at build time by render.py) is stored in
this repository, and this program copies it, byte for byte, to
/output/entry.png -- or to $MAKEFUN_OUTPUT_DIR/entry.png when that
variable is set, as it is for local runs outside the grader's container.

Copying fixed bytes is what makes the program deterministic: it runs
twice and both runs write exactly the same file. After writing, the
program reads the copy back and checks it against the stored image, so
a short or corrupt write fails loudly instead of entering a bad file.
It uses only the Python standard library and never touches the network.
"""

import os
import sys

ASSET = "entry.png"
OUTPUT_NAME = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, ASSET)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)
    with open(source, "rb") as fh:
        data = fh.read()
    with open(target, "wb") as fh:
        fh.write(data)
    with open(target, "rb") as fh:
        written = fh.read()
    if written != data:
        print("error: written file does not match the stored image", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
