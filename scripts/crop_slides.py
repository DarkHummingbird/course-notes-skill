#!/usr/bin/env python3
"""Crop a directory of slide screenshots to the content area.

Usage:
    python3 crop_slides.py raw/ out/ --box 256,8,1890,944

Default box is for a 1920x1080 deck with a 256 px left sidebar and a
bottom page counter. Always inspect one output before batch cropping.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image


def parse_box(value: str) -> tuple[int, int, int, int]:
    parts = [int(x.strip()) for x in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("box must be left,top,right,bottom")
    return tuple(parts)  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=Path)
    parser.add_argument("dst", type=Path)
    parser.add_argument("--box", type=parse_box, default=(256, 8, 1890, 944))
    parser.add_argument("--ext", default=".png,.jpg,.jpeg")
    args = parser.parse_args()

    if not args.src.is_dir():
        print(f"error: not a directory: {args.src}")
        return 2

    exts = {e.strip().lower() for e in args.ext.split(",")}
    args.dst.mkdir(parents=True, exist_ok=True)
    count = 0

    for path in sorted(args.src.iterdir()):
        if path.suffix.lower() not in exts:
            continue
        with Image.open(path) as im:
            cropped = im.convert("RGB").crop(args.box)
            out = args.dst / (path.stem + ".png")
            cropped.save(out, optimize=True)
            print(f"{path.name} {im.size} -> {out.name} {cropped.size}")
            count += 1

    print(f"cropped {count} image(s)")
    return 0 if count else 1


if __name__ == "__main__":
    sys.exit(main())
