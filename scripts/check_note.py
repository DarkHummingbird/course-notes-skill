#!/usr/bin/env python3
"""Deterministic checks for a course note.

Usage:
    python3 check_note.py path/to/note.md

Exit code 0: no errors (warnings are allowed).
Exit code 1: at least one error.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


FORBIDDEN = [
    "老师",
    "讲师",
    "课堂",
    "课件",
    "上一讲",
    "这一讲",
    "本讲",
    "今天讲",
    "同学们",
    "课堂口径",
    "待核实",
    "我们来看",
    "这一页",
    "这张图",
    "大家看",
]

H2_OK = re.compile(r"^## (?:[一二三四五六七八九十百]+、|数据说明|附录)")
H3_OK = re.compile(r"^### (?:\d+\.\d+\s|Q\d+\s|数据说明)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
TABLE_SEP = re.compile(r"^\s*\|[\s:|-]+\|\s*$")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python3 check_note.py path/to/note.md")
        return 2

    note = Path(sys.argv[1]).resolve()
    if not note.is_file():
        print(f"error: not a file: {note}")
        return 2

    text = note.read_text(encoding="utf-8")
    lines = text.splitlines()
    base = note.parent
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Forbidden lecturer / logistics language.
    for i, line in enumerate(lines, 1):
        for word in FORBIDDEN:
            if word in line:
                errors.append(f"L{i}: forbidden phrase {word!r}: {line.strip()[:90]}")

    # 2. Headings.
    h2 = [(i, l) for i, l in enumerate(lines, 1) if l.startswith("## ")]
    h3 = [(i, l) for i, l in enumerate(lines, 1) if l.startswith("### ")]
    for i, line in h2:
        if not H2_OK.match(line):
            errors.append(f"L{i}: H2 should use Chinese numerals: {line}")
    for i, line in h2 + h3:
        if "案例" in line:
            errors.append(f"L{i}: do not make a '案例' heading; put examples under knowledge points")
    for i, line in h3:
        if not H3_OK.match(line):
            errors.append(f"L{i}: H3 should be '### 1.1' or '### Q1': {line}")
    if len(h2) < 2:
        warnings.append("only one H2; a full note usually has at least 3–6 sections")
    if len(h3) < 3:
        warnings.append("few H3 sections; check that methods are broken down")

    # 3. Images exist.
    for i, line in enumerate(lines, 1):
        for target in IMAGE_RE.findall(line):
            if target.startswith(("http://", "https://", "data:")):
                continue
            candidate = (base / target).resolve()
            if not candidate.is_file():
                errors.append(f"L{i}: missing image: {target}")

    # 4. Tables.
    i = 0
    table_count = 0
    while i < len(lines):
        if lines[i].strip().startswith("|") and i + 1 < len(lines) and TABLE_SEP.match(lines[i + 1]):
            table_count += 1
            cols = lines[i].count("|")
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                if lines[j].count("|") != cols:
                    errors.append(f"L{j + 1}: table column count differs from header")
                j += 1
            i = j
        else:
            i += 1
    if table_count == 0:
        warnings.append("no tables; consider tables for steps/fields/comparisons")

    # 5. Bold markers.
    for i, line in enumerate(lines, 1):
        if line.count("**") % 2:
            errors.append(f"L{i}: unmatched bold marker: {line.strip()[:90]}")

    # 6. Examples and data note.
    example_count = sum(1 for l in lines if re.search(r"^> \*\*(?:例|反例)｜", l))
    if example_count == 0:
        warnings.append("no '例｜' / '反例｜' blocks; check that examples are woven under points")
    if not re.search(r"数据说明|数据口径", text):
        warnings.append("no data note; add a short '数据说明' if the note contains numbers")

    # 7. Empty headings / stray separators.
    for i, line in enumerate(lines, 1):
        if re.match(r"^#{1,4}\s*$", line):
            errors.append(f"L{i}: empty heading")

    print(f"note: {note}")
    print(f"lines: {len(lines)} | H2: {len(h2)} | H3: {len(h3)} | tables: {table_count} | examples: {example_count}")

    if warnings:
        print("\nWARNINGS")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print("\nERRORS")
        for e in errors:
            print(f"  - {e}")
        print(f"\n{len(errors)} error(s). Fix before delivery.")
        return 1

    print("\nOK: no errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
