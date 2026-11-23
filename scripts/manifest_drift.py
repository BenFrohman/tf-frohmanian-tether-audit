#!/usr/bin/env python3
# Copyright (c) 2026 Benjamin Stanley Frohman. All rights reserved.
# Released under Apache 2.0 license as described in the file LICENSE.
# Authors: Benjamin Stanley Frohman
"""Compare the current lake-manifest.json sha256 to the CI-recorded hash.
Usage: python3 scripts/manifest_drift.py --expected PATH --label TEXT
Fails if the manifest is missing or its sha256 differs from the expected hash.
The expected hash is the one CI computed from the repo's own lake-manifest.json;
it is not a handwritten pin in the workflow."""
import argparse, hashlib, sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--expected", required=True)
p.add_argument("--label", required=True)
p.add_argument("--manifest", default="lake-manifest.json")
args = p.parse_args()

manifest = Path(args.manifest)
if not manifest.is_file():
    print(f"FAIL: {args.manifest} is missing {args.label}")
    sys.exit(1)

got = hashlib.sha256(manifest.read_bytes()).hexdigest()
expected = Path(args.expected).read_text(encoding="utf-8").strip().split()[0]
print(f"{args.label}: lake-manifest.json sha256 {got}")
print(f"expected: {expected}")
if got != expected:
    print("FAIL: lake-manifest.json drifted from the hash CI recorded at the start of this run")
    sys.exit(1)
print("manifest drift guard: OK")
