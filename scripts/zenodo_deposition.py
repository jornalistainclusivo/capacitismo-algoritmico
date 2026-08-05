#!/usr/bin/env python3
"""
Zenodo deposition management script for GitHub Actions.
Handles creating/finding draft depositions and getting fresh bucket URLs.
"""
import sys
import json
import os
import requests


def get_auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def find_existing_draft(token, title_keyword="Capacitismo Algorítmico"):
    """Find existing draft deposition matching title keyword."""
    # Always return None to force new deposition creation (avoids file conflicts)
    return None, None


def create_deposition(token, metadata_file):
    """Create new deposition with metadata."""
    url = "https://zenodo.org/api/deposit/depositions"
    with open(metadata_file) as f:
        metadata = json.load(f)

    # Normalize metadata to what Zenodo expects for creation
    meta = metadata.get("metadata", {})
    # Ensure upload_type exists
    if "upload_type" not in meta:
        meta["upload_type"] = "dataset"
    # If resource_type is a dict (e.g. {"type":"dataset"}), convert to string
    rt = meta.get("resource_type")
    if isinstance(rt, dict):
        # prefer type key, fallback to subtype or to 'dataset'
        meta["resource_type"] = rt.get("type") or rt.get("subtype") or "dataset"
    # Put normalized metadata back
    metadata["metadata"] = meta

    resp = requests.post(url, headers=get_auth_headers(token), json=metadata)
    if resp.status_code != 201:
        print(f"❌ Failed to create deposition: {resp.status_code}")
        # print full json for debugging
        try:
            print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
        except Exception:
            print(resp.text)
        sys.exit(1)
    data = resp.json()
    return data["id"], data["links"]["bucket"]


def get_deposition_details(token, dep_id):
    """Get fresh deposition details including bucket URL and state."""
    url = f"https://zenodo.org/api/deposit/depositions/{dep_id}"
    resp = requests.get(url, headers=get_auth_headers(token))
    if resp.status_code != 200:
        print(f"❌ Failed to get deposition details: {resp.status_code}")
        sys.exit(1)
    data = resp.json()
    return {
        "id": data["id"],
        "bucket": data["links"]["bucket"],
        "state": data.get("state", "unknown"),
        "submitted": data.get("submitted", False)
    }


def main():
    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        print("❌ ZENODO_TOKEN not set")
        sys.exit(1)

    metadata_file = "zenodo_metadata.json"

    # Try to find existing draft
    dep_id, bucket = find_existing_draft(token)

    if dep_id is None:
        print("Creating new deposition...")
        dep_id, bucket = create_deposition(token, metadata_file)
        print(f"Created: {dep_id}")
    else:
        print(f"Found existing draft: {dep_id}")

    # Verify state
    details = get_deposition_details(token, dep_id)
    print(f"State: {details['state']}, Submitted: {details['submitted']}")

    # Zenodo uses "unsubmitted" for drafts not yet submitted
    valid_draft_states = ["draft", "unsubmitted"]
    if details["state"] not in valid_draft_states or details["submitted"]:
        print("⚠️ Not in draft state, creating new...")
        dep_id, bucket = create_deposition(token, metadata_file)
        details = get_deposition_details(token, dep_id)
        print(f"New deposition: {dep_id}")

    # Output for GitHub Actions
    print(f"DEPOSITION_ID={dep_id}")
    print(f"BUCKET_URL={details['bucket']}")

    # Also write to GITHUB_OUTPUT if available
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"DEPOSITION_ID={dep_id}\n")
            f.write(f"BUCKET_URL={details['bucket']}\n")


if __name__ == "__main__":
    main()