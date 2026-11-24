#!/usr/bin/env python3
# Copyright (c) 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under Apache 2.0 license as described in the file LICENSE.
# Authors: Benjamin Stanley Frohman
"""Check collectAxioms output: every theorem must use only
{propext, Classical.choice, Quot.sound}. Prints the sorted listing and a summary.
Usage: python3 scripts/check_audit.py axioms.raw.txt
Exit status 1 on a nonstandard axiom, unexpected output, or no theorems."""
import re, sys

raw = open(sys.argv[1], encoding="utf-8").read().splitlines()
ok = {"propext", "Classical.choice", "Quot.sound"}
rows, bad = [], []
for l in raw:
    if not l.strip():
        continue
    # Lean may emit info/warning lines around the audit; record errors, ignore
    # ordinary info/warning chatter, and require every other line to be an axiom result.
    if l.startswith("error:") or " error:" in l or l.startswith("MODULE NOT LOADED"):
        bad.append(f"UNEXPECTED OUTPUT: {l}")
        continue
    if l.startswith("info:") or l.startswith("warning:") or l.startswith("warn:"):
        continue
    m = re.match(r"'(.*)' depends on axioms: \[(.*)\] \[module (.*)\]$", l)
    n = re.match(r"'(.*)' does not depend on any axioms \[module (.*)\]$", l)
    if m:
        ax = [a.strip() for a in m.group(2).split(",") if a.strip()]
        rows.append((m.group(3), m.group(1), ax))
        if not set(ax) <= ok:
            bad.append(f"NONSTANDARD AXIOMS {m.group(1)}: {sorted(set(ax) - ok)}")
    elif n:
        rows.append((n.group(2), n.group(1), []))
    else:
        bad.append(f"UNEXPECTED OUTPUT: {l}")
rows.sort()
for mod, name, ax in rows:
    if ax:
        print(f"'{name}' depends on axioms: [{', '.join(ax)}]")
    else:
        print(f"'{name}' does not depend on any axioms")
for b in bad:
    print(b)
nmods = len({r[0] for r in rows})
if bad or not rows:
    print(f"AUDIT FAIL: {len(bad)} problems, {len(rows)} theorems")
    sys.exit(1)
print(
    f"AUDIT PASS: {len(rows)} theorems in {nmods} modules depend only on "
    "propext, Classical.choice, Quot.sound (or on no axioms)"
)
