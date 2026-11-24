#!/usr/bin/env python3
# Copyright (c) 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under Apache 2.0 license as described in the file LICENSE.
# Authors: Benjamin Stanley Frohman
"""Scan a CI log in full, with no skip lists, for sorry / admit / native_decide / sorryAx.
Usage: python3 scripts/log_scan.py LOG [LOG...]
Exit status 1 if any hit is found, including a `declaration uses 'sorry'` warning."""
import re, sys

token = re.compile(r"(?<![\w.])(sorry|admit|native_decide|sorryAx)(?![\w.])")
sorry_warn = re.compile(r"declaration uses 'sorry'")

logs = sys.argv[1:]
if not logs:
    print("usage: python3 scripts/log_scan.py LOG [LOG...]", file=sys.stderr)
    sys.exit(2)

total_warns = 0
total_hits = 0
total_lines = 0
for path in logs:
    text = open(path, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    total_lines += len(lines)
    warns = list(sorry_warn.finditer(text))
    total_warns += len(warns)
    print(f"log: {path}")
    print(f"log lines: {len(lines)}")
    print(f"build-log 'declaration uses sorry' warnings: {len(warns)}")
    for i, line in enumerate(lines, 1):
        for m in token.finditer(line):
            total_hits += 1
            print(f"{path}:{i}: {m.group(1)}: {line}")
print(f"logs scanned: {len(logs)}")
print(f"log lines scanned: {total_lines}")
print(f"sorry/admit/native_decide/sorryAx token hits in log: {total_hits}")
print(f"declaration-uses-sorry warnings: {total_warns}")
sys.exit(1 if total_hits or total_warns else 0)
