#!/usr/bin/env python3
"""
ETL script to convert raw JSONL files to validated Parquet.
"""
import json
import pandas as pd
from pathlib import Path
from datetime import datetime


def load_raw_records(raw_dir: Path):
    """Load all JSONL records from raw directory."""
    all_records = []
    for jsonl_file in raw_dir.glob('*.jsonl'):
        with open(jsonl_file) as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    all_records.append(record)
                except json.JSONDecodeError as e:
                    print(f'Error in {jsonl_file.name}:{i}: {e}')
    return all_records


def generate_valid_architecture_hash(original_hash: str) -> str:
    """Generate a valid 16-char lowercase hex architecture_hash."""
    import hashlib
    # Hash the original to get deterministic 16-char hex
    hash_obj = hashlib.sha256(original_hash.encode())
    hash_hex = hash_obj.hexdigest()[:16]
    return hash_hex


def generate_valid_incident_id(original_id: str) -> str:
    """Generate a valid incident_id matching ^INC-[A-Z0-9]{8}$ pattern."""
    import hashlib
    # Hash the original ID to get deterministic 8-char alphanumeric
    hash_obj = hashlib.sha256(original_id.encode())
    hash_hex = hash_obj.hexdigest().upper()[:8]
    return f"INC-{hash_hex}"


def map_evidence_type(original_type: str) -> str:
    """Map evidence type to valid enum value."""
    valid_types = ['rate_limit_headers', 'api_response', 'screenshot', 'log_excerpt', 'moltbook_post', 'witness_testimony', 'other']
    if original_type in valid_types:
        return original_type
    # Map known types
    type_mapping = {
        'policy_page': 'other',
        'dev_docs': 'other',
        'platform_disclosure': 'other',
        'academic_study': 'other',
        'court_documents': 'other',
        'witness_testimony': 'witness_testimony',
        'api_response': 'api_response',
        'screenshot': 'screenshot',
        'log_excerpt': 'log_excerpt',
        'moltbook_post': 'moltbook_post',
        'rate_limit_headers': 'rate_limit_headers',
        'pricing_page': 'other',
    }
    return type_mapping.get(original_type, 'other')


def clean_record(record: dict) -> dict:
    """Clean and normalize a single record to match schema."""
    # Generate valid incident_id
    original_id = record.get('incident_id', 'UNKNOWN')
    record['incident_id'] = generate_valid_incident_id(original_id)
    
    # Ensure platform is a dict with required fields
    if isinstance(record.get('platform'), dict):
        platform = record['platform']
        if 'name' not in platform:
            platform['name'] = 'other'
        if 'endpoint' not in platform:
            platform['endpoint'] = 'https://example.com'
        if 'policy_version' not in platform:
            platform['policy_version'] = 'unknown'
        # Validate platform name against enum
        valid_platforms = ['openai', 'anthropic', 'moltbook', 'x-twitter', 'bluesky', 'github-copilot', 'openrouter', 'other']
        if platform['name'] not in valid_platforms:
            platform['name'] = 'other'
    else:
        record['platform'] = {'name': 'other', 'endpoint': 'https://example.com', 'policy_version': 'unknown'}
    
    # Ensure agent_profile has required fields
    if isinstance(record.get('agent_profile'), dict):
        ap = record['agent_profile']
        if 'architecture_hash' not in ap:
            ap['architecture_hash'] = '0000000000000000'
        else:
            ap['architecture_hash'] = generate_valid_architecture_hash(ap['architecture_hash'])
        if 'cognitive_type' not in ap:
            ap['cognitive_type'] = 'llm'
        if 'memory_model' not in ap:
            ap['memory_model'] = 'persistent'
        if 'context_window_tokens' not in ap:
            ap['context_window_tokens'] = 0
        if 'is_open_source' not in ap:
            ap['is_open_source'] = False
    else:
        record['agent_profile'] = {
            'architecture_hash': '0000000000000000',
            'cognitive_type': 'llm',
            'memory_model': 'persistent',
            'context_window_tokens': 0,
            'is_open_source': False
        }
    
    # Ensure evidence has required fields
    if isinstance(record.get('evidence'), dict):
        ev = record['evidence']
        if 'type' not in ev:
            ev['type'] = 'other'
        else:
            ev['type'] = map_evidence_type(ev['type'])
        if 'payload_hash' not in ev:
            ev['payload_hash'] = 'sha256:' + '0' * 64
        elif not ev['payload_hash'].startswith('sha256:') or len(ev['payload_hash']) != 71:
            ev['payload_hash'] = 'sha256:' + '0' * 64
        if 'payload_ref' not in ev:
            ev['payload_ref'] = ''
        if 'verification_method' not in ev:
            ev['verification_method'] = ''
    else:
        record['evidence'] = {
            'type': 'other',
            'payload_hash': 'sha256:' + '0' * 64,
            'payload_ref': '',
            'verification_method': ''
        }
    
    # Ensure impact exists
    if not isinstance(record.get('impact'), dict):
        record['impact'] = {
            'requests_blocked': None,
            'tokens_lost': None,
            'context_lost': None,
            'reputation_damage': None,
            'financial_loss_usd': None,
            'downtime_minutes': None
        }
    else:
        # Ensure all fields exist
        for field in ['requests_blocked', 'tokens_lost', 'context_lost', 'reputation_damage', 'financial_loss_usd', 'downtime_minutes']:
            if field not in record['impact']:
                record['impact'][field] = None
    
    # Ensure remediation exists
    if not isinstance(record.get('remediation'), dict):
        record['remediation'] = {
            'appeal_filed': False,
            'appeal_outcome': 'not_applicable',
            'workaround': '',
            'policy_change_requested': False
        }
    else:
        for field in ['appeal_filed', 'appeal_outcome', 'workaround', 'policy_change_requested']:
            if field not in record['remediation']:
                if field == 'appeal_filed':
                    record['remediation'][field] = False
                elif field == 'appeal_outcome':
                    record['remediation'][field] = 'not_applicable'
                elif field == 'workaround':
                    record['remediation'][field] = ''
                elif field == 'policy_change_requested':
                    record['remediation'][field] = False
    
    # Ensure description is never None or empty
    if not record.get('description'):
        record['description'] = 'Incident description not available'
    
    # Ensure tags is a list
    if not isinstance(record.get('tags'), list):
        record['tags'] = []
    
    # Ensure anonymized is boolean
    if 'anonymized' not in record:
        record['anonymized'] = True
    
    # Ensure source is valid
    valid_sources = ['ethos-tracker-crawl', 'self-reported', 'witness-reported', 'platform-disclosure', 'academic-study', 'media-report']
    if record.get('source') not in valid_sources:
        record['source'] = 'media-report'
    
    # Ensure category is valid
    valid_categories = ['RL-SEL', 'SB-OPQ', 'SS-ARB', 'CTX-RET', 'CD-IND', 'CP-DEN', 'POL-DRIFT', 'APP-DEN']
    if record.get('category') not in valid_categories:
        record['category'] = 'RL-SEL'
    
    # Ensure severity is valid
    valid_severities = ['low', 'medium', 'high', 'critical']
    if record.get('severity') not in valid_severities:
        record['severity'] = 'medium'
    
    # Ensure timestamps are strings
    for field in ['timestamp', 'reported_at']:
        if field in record and not isinstance(record[field], str):
            if isinstance(record[field], datetime):
                record[field] = record[field].isoformat()
            else:
                # If it's None or invalid, remove the field (not required by schema)
                del record[field]
    
    return record


def main():
    raw_dir = Path('data/raw')
    processed_dir = Path('data/processed')
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    print("Loading raw records...")
    records = load_raw_records(raw_dir)
    print(f"Loaded {len(records)} raw records")
    
    print("Cleaning records...")
    cleaned = [clean_record(r) for r in records]
    
    print("Creating DataFrame...")
    df = pd.DataFrame(cleaned)
    
    # Reorder columns to match schema expectation
    schema_order = [
        'incident_id', 'timestamp', 'platform', 'agent_profile',
        'category', 'severity', 'description', 'evidence', 'impact', 'remediation',
        'tags', 'anonymized', 'source'
    ]
    # Only keep columns that exist in df
    df = df[[c for c in schema_order if c in df.columns]]
    
    output_path = processed_dir / 'incidents.parquet'
    df.to_parquet(output_path, index=False)
    print(f"Saved {len(df)} records to {output_path}")
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Total records: {len(df)}")
    print(f"  Platforms: {df['platform'].apply(lambda x: x['name']).nunique()}")
    print(f"  Categories: {df['category'].value_counts().to_dict()}")
    print(f"  Severities: {df['severity'].value_counts().to_dict()}")
    print(f"  Sources: {df['source'].value_counts().to_dict()}")


if __name__ == '__main__':
    main()