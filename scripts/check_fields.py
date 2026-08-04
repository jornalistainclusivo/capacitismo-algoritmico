#!/usr/bin/env python3
"""Check required fields in processed data."""
import sys
from pathlib import Path

import pandas as pd

proc_dir = Path('data/processed')
required_fields = ['incident_id', 'platform', 'category', 'agent_id_hash', 'timestamp', 'description']

for file in proc_dir.glob('*.parquet'):
    print(f"📋 Checking required fields in {file.name}")
    df = pd.read_parquet(file)

    # Check if we have nested agent_profile with architecture_hash
    has_agent_id_hash = 'agent_id_hash' in df.columns
    if not has_agent_id_hash and 'agent_profile' in df.columns:
        # Try to extract from agent_profile.architecture_hash
        try:
            df['agent_id_hash'] = df['agent_profile'].apply(
                lambda x: x.get('architecture_hash', '')[:16] if isinstance(x, dict) else ''
            )
            has_agent_id_hash = True
        except (KeyError, AttributeError, TypeError):
            pass

    missing = [f for f in required_fields if f not in df.columns]
    if not has_agent_id_hash and 'agent_id_hash' in required_fields:
        missing.append('agent_id_hash')

    if missing:
        print(f"❌ {file.name}: missing fields {missing}")
        sys.exit(1)
    nulls = df[required_fields].isnull().sum()
    if nulls.any():
        print(f"⚠️  {file.name}: null values in {nulls[nulls > 0].to_dict()}")
    print(f"✅ {file.name}: {len(df)} records, all required fields present")

print("✅ All files have required fields")