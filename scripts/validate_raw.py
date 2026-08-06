#!/usr/bin/env python3
"""Validate raw JSONL format."""
import json
import sys
from pathlib import Path

raw_dir = Path('data/raw')
errors = 0

for file in raw_dir.glob('*.jsonl'):
    print(f"📄 Validating JSONL: {file.name}")
    with open(file) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                print(f"❌ {file.name}:{i}: {e}")
                errors += 1

if errors:
    sys.exit(1)

print("✅ All JSONL files valid")
