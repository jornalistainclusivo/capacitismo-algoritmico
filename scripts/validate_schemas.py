#!/usr/bin/env python3
"""Validate Parquet files against JSON schemas."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from jsonschema import ValidationError, validate

schemas_dir = Path('schemas')
data_dir = Path('data/processed')

schema_file = schemas_dir / 'incident.json'
print(f"📋 Validating {schema_file.name}...")
with open(schema_file) as f:
    schema = json.load(f)

data_file = data_dir / 'incidents.parquet'
if not data_file.exists():
    print(f"⚠️  No data file for schema {schema_file.name}")
    sys.exit(1)

df = pd.read_parquet(data_file)
errors = 0

for idx, row in df.iterrows():
    # Convert row to dict with proper serialization
    row_dict = {}
    for col in df.columns:
        val = row[col]
        if isinstance(val, (list, dict)):
            row_dict[col] = val
        elif isinstance(val, np.ndarray):
            # Handle numpy arrays (like tags column)
            row_dict[col] = val.tolist()
        elif isinstance(val, (np.integer, np.floating)):
            row_dict[col] = val.item()
        elif isinstance(val, np.bool_):
            row_dict[col] = bool(val)
        elif isinstance(val, (np.ndarray, pd.Series)):
            # Handle numpy arrays (like tags column)
            row_dict[col] = val.tolist() if hasattr(val, 'tolist') else list(val)
        elif pd.isna(val):
            row_dict[col] = None
        elif isinstance(val, pd.Timestamp):
            row_dict[col] = val.isoformat()
        elif isinstance(val, str):
            if col in ['platform', 'agent_profile', 'evidence', 'impact', 'remediation', 'tags']:
                try:
                    row_dict[col] = json.loads(val)
                except json.JSONDecodeError:
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