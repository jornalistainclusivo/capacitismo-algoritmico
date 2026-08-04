#!/usr/bin/env python3
"""Anonymize raw incident data before sharing.

Removes PII, hashes IDs (SHA-256 truncated to 16 chars for architecture_hash,
8 chars for incident_id), and ensures compliance with privacy requirements.

Usage:
    python scripts/anonymize.py data/raw/ data/raw_anonymized/
    python scripts/anonymize.py data/raw/incident.jsonl --output data/raw_anonymized/incident.jsonl
"""
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


def hash_architecture_id(original: str) -> str:
    """Generate deterministic 16-char lowercase hex hash for architecture_hash."""
    hash_obj = hashlib.sha256(original.encode())
    return hash_obj.hexdigest()[:16]


def hash_incident_id(original: str) -> str:
    """Generate deterministic INC-XXXXXXXX format incident_id."""
    hash_obj = hashlib.sha256(original.encode())
    hash_hex = hash_obj.hexdigest().upper()[:8]
    return f"INC-{hash_hex}"


def hash_agent_identifier(original: str) -> str:
    """Hash any agent identifier (username, ID, etc.) to 16-char hex."""
    hash_obj = hashlib.sha256(original.encode())
    return hash_obj.hexdigest()[:16]


def hash_platform_identifier(original: str) -> str:
    """Hash platform-specific identifiers to 16-char hex."""
    hash_obj = hashlib.sha256(original.encode())
    return hash_obj.hexdigest()[:16]


def generate_payload_hash(content: str) -> str:
    """Generate SHA-256 hash for evidence payload."""
    hash_obj = hashlib.sha256(content.encode())
    return f"sha256:{hash_obj.hexdigest()}"


def sanitize_string(value: str, field_name: str = "") -> str:
    """Remove potential PII from string values."""
    # Patterns that might indicate PII
    pii_patterns = [
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REDACTED]'),  # emails
        (r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b', '[PHONE_REDACTED]'),  # phones
        (r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REDACTED]'),  # SSN
        (r'\b(?:\d{4}[-\s]?){3}\d{4}\b', '[CARD_REDACTED]'),  # credit card
        (r'[a-f0-9]{64}', '[HASH_REDACTED]'),  # full SHA-256
        (r'\b[A-Z0-9]{20,}\b', '[TOKEN_REDACTED]'),  # long tokens/keys
    ]

    result = value
    for pattern, replacement in pii_patterns:
        result = re.sub(pattern, replacement, result)

    return result


def anonymize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Anonymize a single incident record."""
    anonymized = record.copy()

    # Anonymize incident_id
    if 'incident_id' in anonymized:
        original_id = anonymized['incident_id']
        if not original_id.startswith('INC-') or len(original_id) != 13:
            anonymized['incident_id'] = hash_incident_id(original_id)

    # Anonymize platform info
    if 'platform' in anonymized and isinstance(anonymized['platform'], dict):
        platform = anonymized['platform']
        # Keep platform name but hash any identifiers
        if 'endpoint' in platform and isinstance(platform['endpoint'], str):
            # Keep domain but hash path/query
            try:
                parsed = urlparse(platform['endpoint'])
                platform['endpoint'] = f"{parsed.scheme}://{parsed.netloc}/[PATH_HASHED]"
            except (ValueError, AttributeError):
                platform['endpoint'] = 'https://[REDACTED]'

    # Anonymize agent_profile
    if 'agent_profile' in anonymized and isinstance(anonymized['agent_profile'], dict):
        ap = anonymized['agent_profile']
        if 'architecture_hash' in ap:
            original_hash = ap['architecture_hash']
            if not re.match(r'^[a-f0-9]{16}$', original_hash):
                ap['architecture_hash'] = hash_architecture_id(original_hash)
        # Hash any other identifiers in agent_profile
        for key in ['agent_id', 'user_id', 'account_id', 'session_id']:
            if key in ap and isinstance(ap[key], str):
                ap[key] = hash_agent_identifier(ap[key])

    # Anonymize evidence
    if 'evidence' in anonymized and isinstance(anonymized['evidence'], dict):
        ev = anonymized['evidence']
        if 'payload_hash' in ev:
            original_hash = ev['payload_hash']
            if not original_hash.startswith('sha256:') or len(original_hash) != 71:
                # Generate new hash from payload_ref or description
                payload_content = ev.get('payload_ref', '') or ev.get('verification_method', '') or str(ev)
                ev['payload_hash'] = generate_payload_hash(payload_content)
        if 'payload_ref' in ev and isinstance(ev['payload_ref'], str):
            # Hash the reference but keep format recognizable
            if ev['payload_ref'].startswith('ipfs://'):
                ev['payload_ref'] = 'ipfs://' + hash_platform_identifier(ev['payload_ref'])
            elif ev['payload_ref'].startswith('http'):
                try:
                    parsed = urlparse(ev['payload_ref'])
                    ev['payload_ref'] = f"{parsed.scheme}://{parsed.netloc}/[PATH_HASHED]"
                except (ValueError, AttributeError):
                    ev['payload_ref'] = '[URL_HASHED]'
        if 'verification_method' in ev and isinstance(ev['verification_method'], str):
            ev['verification_method'] = sanitize_string(ev['verification_method'], 'verification_method')

    # Anonymize description (remove potential PII)
    if 'description' in anonymized and isinstance(anonymized['description'], str):
        anonymized['description'] = sanitize_string(anonymized['description'], 'description')

    # Anonymize tags
    if 'tags' in anonymized and isinstance(anonymized['tags'], list):
        anonymized['tags'] = [sanitize_string(tag, 'tag') for tag in anonymized['tags']]

    # Anonymize workaround
    if ('remediation' in anonymized
        and isinstance(anonymized['remediation'], dict)
        and 'workaround' in anonymized['remediation']
        and isinstance(anonymized['remediation']['workaround'], str)):
        anonymized['remediation']['workaround'] = sanitize_string(
            anonymized['remediation']['workaround'], 'workaround'
        )

    # Mark as anonymized
    anonymized['anonymized'] = True

    return anonymized


def anonymize_file(input_path: Path, output_path: Path) -> int:
    """Anonymize a JSONL file."""
    print(f"🔒 Anonymizing {input_path.name} → {output_path.name}")
    records_processed = 0
    errors = 0

    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for i, line in enumerate(infile, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                anonymized = anonymize_record(record)
                outfile.write(json.dumps(anonymized, ensure_ascii=False) + '\n')
                records_processed += 1
            except json.JSONDecodeError as e:
                print(f"❌ {input_path.name}:{i}: JSON decode error: {e}")
                errors += 1
            except (ValueError, KeyError, TypeError) as e:
                print(f"❌ {input_path.name}:{i}: Anonymization error: {e}")
                errors += 1

    print(f"✅ {input_path.name}: {records_processed} records anonymized, {errors} errors")
    return errors


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python anonymize.py <input_path> <output_path>")
        print("  input_path:  file or directory with raw JSONL files")
        print("  output_path: file or directory for anonymized output")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if input_path.is_file():
        # Single file mode
        output_path.parent.mkdir(parents=True, exist_ok=True)
        errors = anonymize_file(input_path, output_path)
        sys.exit(1 if errors > 0 else 0)

    elif input_path.is_dir():
        # Directory mode - process all .jsonl files
        output_path.mkdir(parents=True, exist_ok=True)
        total_errors = 0
        total_files = 0

        for jsonl_file in input_path.glob('*.jsonl'):
            output_file = output_path / jsonl_file.name
            errors = anonymize_file(jsonl_file, output_file)
            total_errors += errors
            total_files += 1

        print(f"\n📊 Summary: {total_files} files processed, {total_errors} total errors")
        sys.exit(1 if total_errors > 0 else 0)

    else:
        print(f"❌ Input path does not exist: {input_path}")
        sys.exit(1)


if __name__ == '__main__':
    main()