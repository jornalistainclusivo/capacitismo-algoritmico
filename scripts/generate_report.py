#!/usr/bin/env python3
"""Generate validation report."""
from pathlib import Path

import pandas as pd

print("## Dataset Validation Report")
print()
print("Repository: jornalistainclusivo/capacitismo-algoritmico")
print("Branch: master")
print("Commit: latest")
print()

raw_files = list(Path('data/raw').glob('*.jsonl'))
proc_files = list(Path('data/processed').glob('*.parquet'))
schema_files = list(Path('schemas').glob('*.json'))

print(f"📁 Raw files: {len(raw_files)}")
print(f"📁 Processed files: {len(proc_files)}")
print(f"📋 Schemas: {len(schema_files)}")
print()

total_records = 0
for f in proc_files:
    df = pd.read_parquet(f)
    total_records += len(df)
    print(f"  - {f.name}: {len(df)} records")

print(f"📊 Total records: {total_records}")