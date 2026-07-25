#!/usr/bin/env python3
"""Validate Parquet files against JSON schemas."""
import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError
import pandas as pd

schemas_dir = Path('schemas')
data_dir = Path('data/processed')

for schema_file in schemas_dir.glob('*.json'):
    print(f"📋 Validating {schema_file.name}...")
    with open(schema_file) as f:
        schema = json.load(f)

    data_file = data_dir / f'{schema_file.stem}.parquet'
    if not data_file.exists():
        print(f"⚠️  No data file for schema {schema_file.name}")
        continue

    df = pd.read_parquet(data_file)
    errors = 0

    for idx, row in df.iterrows():
        # Convert row to dict with proper serialization
        row_dict = {}
        for col in df.columns:
            val = row[col]
            if isinstance(val, (list, dict)):
                row_dict[col] = val
            elif pd.isna(val):
                row_dict[col] = None
            elif isinstance(val, pd.Timestamp):
                row_dict[col] = val.isoformat()
            elif isinstance(val, str):
                if col in ['platform', 'agent_profile', 'evidence', 'impact', 'remediation', 'tags']:
                    try:
                        row_dict[col] = json.loads(val)
                    except:
                        row_dict[col] = val
                else:
                    row_dict[col] = val
            else:
                row_dict[col] = val

        try:
            validate(instance=row_dict, schema=schema)
        except ValidationError as e:
            print(f"❌ {data_file.name} row {idx}: {e.message}")
            errors += 1

    if errors == 0:
        print(f"✅ {data_file.name}: all records valid against {schema_file.name}")
    else:
        sys.exit(1)

print("✅ All schemas validated")