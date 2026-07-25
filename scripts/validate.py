#!/usr/bin/env python3
"""
Validate dataset against JSON schemas.
Usage: python scripts/validate.py data/processed/
"""

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError
import pandas as pd


def validate_parquet_files(processed_dir: Path, schemas_dir: Path) -> int:
    """Validate all Parquet files against their corresponding schemas."""
    errors = 0
    
    for parquet_file in processed_dir.glob("*.parquet"):
        schema_file = schemas_dir / f"{parquet_file.stem}.json"
        
        if not schema_file.exists():
            print(f"⚠️  No schema for {parquet_file.name}, skipping")
            continue
            
        print(f"📋 Validating {parquet_file.name} against {schema_file.name}...")
        
        with open(schema_file) as f:
            schema = json.load(f)
        
        df = pd.read_parquet(parquet_file)
        
        for idx, row in df.iterrows():
            # Convert row to dict with proper serialization
            row_dict = {}
            for col in df.columns:
                val = row[col]
                if isinstance(val, (list, dict)):
                    row_dict[col] = val
                elif isinstance(val, pd.Series) or (hasattr(val, '__iter__') and not isinstance(val, str)):
                    # Handle arrays/lists that come from parquet
                    try:
                        row_dict[col] = val.tolist() if hasattr(val, 'tolist') else list(val)
                    except:
                        row_dict[col] = val
                elif pd.isna(val):
                    row_dict[col] = None
                elif isinstance(val, pd.Timestamp):
                    row_dict[col] = val.isoformat()
                elif isinstance(val, str):
                    # Try to parse JSON strings for nested fields
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
                print(f"❌ {parquet_file.name} row {idx}: {e.message}")
                errors += 1
        
        if errors == 0:
            print(f"✅ {parquet_file.name}: {len(df)} records valid")
    
    return errors


def validate_raw_jsonl(raw_dir: Path) -> int:
    """Validate all JSONL files have valid JSON."""
    errors = 0
    
    for jsonl_file in raw_dir.glob("*.jsonl"):
        print(f"📄 Validating JSONL: {jsonl_file.name}")
        
        with open(jsonl_file) as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"❌ {jsonl_file.name}:{i}: {e}")
                    errors += 1
        
        if errors == 0:
            print(f"✅ {jsonl_file.name}: valid JSONL")
    
    return errors


def check_required_fields(processed_dir: Path) -> int:
    """Check required fields exist in processed data."""
    errors = 0
    required_fields = ['incident_id', 'platform', 'category', 'agent_id_hash', 'timestamp', 'description']
    
    for parquet_file in processed_dir.glob("*.parquet"):
        df = pd.read_parquet(parquet_file)
        
        # Check if we have nested agent_profile with architecture_hash
        has_agent_id_hash = 'agent_id_hash' in df.columns
        if not has_agent_id_hash and 'agent_profile' in df.columns:
            # Try to extract from agent_profile.architecture_hash
            try:
                df['agent_id_hash'] = df['agent_profile'].apply(
                    lambda x: x.get('architecture_hash', '')[:16] if isinstance(x, dict) else ''
                )
                has_agent_id_hash = True
            except:
                pass
        
        missing = [f for f in required_fields if f not in df.columns]
        if not has_agent_id_hash and 'agent_id_hash' in required_fields:
            # Check if we can derive it
            pass
        
        if missing:
            print(f"❌ {parquet_file.name}: missing fields {missing}")
            errors += 1
        else:
            # Check for nulls in required fields
            nulls = df[required_fields].isnull().sum()
            if nulls.any():
                print(f"⚠️  {parquet_file.name}: null values in {nulls[nulls > 0].to_dict()}")
            print(f"✅ {parquet_file.name}: all required fields present ({len(df)} records)")
    
    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py <processed_dir>")
        sys.exit(1)
    
    processed_dir = Path(sys.argv[1])
    raw_dir = processed_dir.parent / "raw"
    schemas_dir = processed_dir.parent.parent / "schemas"
    
    print(f"🔍 Validating dataset...")
    print(f"   Processed: {processed_dir}")
    print(f"   Raw: {raw_dir}")
    print(f"   Schemas: {schemas_dir}")
    print()
    
    total_errors = 0
    
    # Validate raw JSONL
    total_errors += validate_raw_jsonl(raw_dir)
    print()
    
    # Validate required fields
    total_errors += check_required_fields(processed_dir)
    print()
    
    # Validate against schemas
    total_errors += validate_parquet_files(processed_dir, schemas_dir)
    print()
    
    if total_errors > 0:
        print(f"❌ Validation failed with {total_errors} errors")
        sys.exit(1)
    else:
        print("✅ All validations passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()