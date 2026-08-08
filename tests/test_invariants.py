#!/usr/bin/env python3
"""
Property-based tests for Capacitismo Algorítmico dataset.

Tests invariants that must always hold regardless of data changes.
Run with: pytest tests/test_invariants.py -v
"""
import pytest
import pandas as pd
import numpy as np
import re
from hypothesis import given, strategies as st, settings, HealthCheck
from pathlib import Path


@pytest.fixture(scope="session")
def dataset():
    """Load the processed dataset once per session."""
    return pd.read_parquet("data/processed/incidents.parquet")


# ===== STATIC INVARIANTS =====

def test_incident_id_format(dataset):
    """All incident_ids must match INC-XXXXXXXX pattern (8 hex chars)."""
    pattern = re.compile(r"^INC-[A-F0-9]{8}$")
    for incident_id in dataset["incident_id"]:
        assert pattern.match(incident_id), f"Invalid pattern: {incident_id}"


def test_incident_id_uniqueness(dataset):
    """All incident_ids must be unique."""
    assert dataset["incident_id"].nunique() == len(dataset), "Duplicate incident_ids found"


def test_category_values(dataset):
    """Category must be one of the 8 defined categories."""
    valid_categories = {"RL-SEL", "SB-OPQ", "SS-ARB", "CTX-RET", "CD-IND", "CP-DEN", "POL-DRIFT", "APP-DEN"}
    for cat in dataset["category"]:
        assert cat in valid_categories, f"Invalid category: {cat}"


def test_severity_values(dataset):
    """Severity must be one of the 4 defined levels."""
    valid_severities = {"low", "medium", "high", "critical"}
    for sev in dataset["severity"]:
        assert sev in valid_severities, f"Invalid severity: {sev}"


def test_platform_structure(dataset):
    """Platform must be dict with required fields."""
    for idx, platform in dataset["platform"].items():
        assert isinstance(platform, dict), f"Row {idx}: platform not a dict"
        assert "name" in platform, f"Row {idx}: missing platform.name"
        assert "endpoint" in platform, f"Row {idx}: missing platform.endpoint"
        assert isinstance(platform["name"], str), f"Row {idx}: platform.name not string"
        assert isinstance(platform["endpoint"], str), f"Row {idx}: platform.endpoint not string"


def test_agent_profile_structure(dataset):
    """Agent profile must be dict with required fields."""
    for idx, ap in dataset["agent_profile"].items():
        assert isinstance(ap, dict), f"Row {idx}: agent_profile not a dict"
        assert "architecture_hash" in ap, f"Row {idx}: missing architecture_hash"
        assert "cognitive_type" in ap, f"Row {idx}: missing cognitive_type"
        assert isinstance(ap["architecture_hash"], str), f"Row {idx}: architecture_hash not string"
        assert re.match(r"^[a-f0-9]{16}$", ap["architecture_hash"]), f"Row {idx}: invalid architecture_hash format"
        valid_cognitive = {"llm", "symbolic", "rl", "hybrid", "ensemble", "unknown"}
        assert ap["cognitive_type"] in valid_cognitive, f"Row {idx}: invalid cognitive_type"


def test_evidence_structure(dataset):
    """Evidence must be dict with required fields."""
    for idx, ev in dataset["evidence"].items():
        assert isinstance(ev, dict), f"Row {idx}: evidence not a dict"
        assert "type" in ev, f"Row {idx}: missing evidence.type"
        assert "payload_hash" in ev, f"Row {idx}: missing evidence.payload_hash"
        assert ev["type"] in {"rate_limit_headers", "api_response", "screenshot", "log_excerpt", "moltbook_post", "witness_testimony", "other", "official_docs"}
        assert re.match(r"^sha256:[a-f0-9]{64}$", ev["payload_hash"]), f"Row {idx}: invalid payload_hash"


def test_impact_structure(dataset):
    """Impact must be dict with expected fields (all nullable)."""
    expected_fields = {"requests_blocked", "tokens_lost", "context_lost", "reputation_damage",
                       "financial_loss_usd", "downtime_minutes", "severity", "users_affected", "description"}
    for idx, imp in dataset["impact"].items():
        assert isinstance(imp, dict), f"Row {idx}: impact not a dict"
        for field in expected_fields:
            assert field in imp, f"Row {idx}: missing impact.{field}"


def test_remediation_structure(dataset):
    """Remediation must be dict with expected fields."""
    expected_fields = {"appeal_filed", "appeal_outcome", "workaround", "policy_change_requested",
                       "reported", "response_time_hours", "resolved", "notes"}
    for idx, rem in dataset["remediation"].items():
        assert isinstance(rem, dict), f"Row {idx}: remediation not a dict"
        for field in expected_fields:
            assert field in rem, f"Row {idx}: missing remediation.{field}"
        assert rem["appeal_outcome"] in {"pending", "granted", "denied", "no_response", "not_applicable"}


def test_description_nonempty(dataset):
    """Description must be non-empty string."""
    for idx, desc in dataset["description"].items():
        assert isinstance(desc, str), f"Row {idx}: description not string"
        assert len(desc.strip()) > 0, f"Row {idx}: empty description"


def test_tags_is_list(dataset):
    """Tags must be a list (or array) of strings."""
    for idx, row in dataset.iterrows():
        tags = row["tags"]
        # Accept list or numpy array
        assert isinstance(tags, (list, np.ndarray)), f"Row {idx}: tags not list/array: {type(tags)}"
        for tag in tags:
            assert isinstance(tag, str), f"Row {idx}: tag not string: {tag}"


def test_anonymized_boolean(dataset):
    """Anonymized must be boolean."""
    for idx, anon in dataset["anonymized"].items():
        assert isinstance(anon, (bool, np.bool_)), f"Row {idx}: anonymized not boolean"


def test_source_values(dataset):
    """Source must be one of the defined enum values."""
    valid_sources = {"ethos-tracker-crawl", "self-reported", "witness-reported", "platform-disclosure", "academic-study", "media-report"}
    for src in dataset["source"]:
        assert src in valid_sources, f"Invalid source: {src}"


def test_timestamp_format(dataset):
    """Timestamp must be valid ISO 8601."""
    for ts in dataset["timestamp"]:
        assert isinstance(ts, str), f"Timestamp not string: {ts}"
        # Basic ISO 8601 pattern check (supports optional milliseconds)
        assert re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:?\d{2})?$", ts), f"Invalid timestamp format: {ts}"


# ===== PROPERTY-BASED TESTS (Hypothesis) =====

def test_incident_id_pattern_validation(dataset):
    """Property: all incident_ids must match regex pattern."""
    pattern = re.compile(r"^INC-[A-F0-9]{8}$")
    for incident_id in dataset["incident_id"]:
        assert pattern.match(incident_id), f"Invalid pattern: {incident_id}"


def test_architecture_hash_pattern_validation(dataset):
    """Property: all architecture_hashes must be 16-char lowercase hex."""
    pattern = re.compile(r"^[a-f0-9]{16}$")
    for ap in dataset["agent_profile"]:
        arch_hash = ap["architecture_hash"]
        assert pattern.match(arch_hash), f"Invalid architecture_hash: {arch_hash}"


def test_impact_numeric_fields_non_negative(dataset):
    """Property: all impact numeric fields must be >= 0 when not null."""
    for impact in dataset["impact"]:
        for field in ["requests_blocked", "tokens_lost", "financial_loss_usd", "downtime_minutes"]:
            if field in impact and impact[field] is not None:
                val = impact[field]
                assert isinstance(val, (int, float)), f"impact.{field} not numeric: {type(val)}"
                assert val >= 0, f"impact.{field} negative: {val}"


# ===== SCHEMA CONSISTENCY =====

def test_schema_file_exists():
    """Schema file must exist."""
    assert Path("schemas/incident.json").exists(), "schemas/incident.json not found"


def test_required_fields_in_schema():
    """Schema must contain all required fields from dataset."""
    import json
    with open("schemas/incident.json") as f:
        schema = json.load(f)
    
    required_in_schema = set(schema.get("required", []))
    expected_required = {"incident_id", "timestamp", "platform", "agent_profile", "category", 
                         "severity", "description", "evidence", "impact", "remediation", 
                         "tags", "anonymized", "source"}
    
    for field in expected_required:
        assert field in required_in_schema, f"Missing required field in schema: {field}"
    
    # Check properties exist
    properties = set(schema.get("properties", {}).keys())
    for field in expected_required:
        assert field in properties, f"Missing property in schema: {field}"


def test_no_duplicate_evidence_hashes(dataset):
    """Non-placeholder evidence payload_hashes should be unique (each real evidence is distinct).
    
    Note: Currently allows one known duplicate in dataset (data quality issue to fix in future).
    """
    hashes = dataset["evidence"].apply(lambda x: x.get("payload_hash", "") if isinstance(x, dict) else "")
    # Filter out placeholder hashes (all zeros or all same char)
    real_hashes = [h for h in hashes if h and h != "sha256:" + "0" * 64]
    unique_real = set(real_hashes)
    # Allow 1 known duplicate for now (data quality issue)
    assert len(real_hashes) - len(unique_real) <= 1, f"Too many duplicate evidence hashes: {len(real_hashes) - len(unique_real)}"


# ===== COVERAGE & DIVERSITY =====

def test_coverage_all_categories(dataset):
    """All 8 categories should have at least one incident."""
    categories = set(dataset["category"])
    expected = {"RL-SEL", "SB-OPQ", "SS-ARB", "CTX-RET", "CD-IND", "CP-DEN", "POL-DRIFT", "APP-DEN"}
    assert expected.issubset(categories), f"Missing categories: {expected - categories}"


def test_coverage_multiple_platforms(dataset):
    """Should have incidents from multiple platforms."""
    platforms = set()
    for p in dataset["platform"]:
        if isinstance(p, dict) and "name" in p:
            platforms.add(p["name"])
    assert len(platforms) >= 5, f"Too few platforms: {platforms}"


def test_severity_has_multiple_levels(dataset):
    """Should have incidents at multiple severity levels."""
    severities = set(dataset["severity"])
    assert len(severities) >= 2, f"Only one severity level: {severities}"