#!/usr/bin/env python3
"""
Upload files to Zenodo deposition using /files endpoint.
"""
import sys
import os
import glob
import requests


def get_auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def get_files_url(token, dep_id):
    """Get the files endpoint URL for a deposition."""
    return f"https://zenodo.org/api/deposit/depositions/{dep_id}/files"


def upload_file(token, files_url, file_path):
    """Upload a single file to Zenodo via /files endpoint."""
    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return False

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        resp = requests.post(files_url, headers=get_auth_headers(token), files=files)

    if resp.status_code == 201:
        print(f"✅ Uploaded: {file_path}")
        return True
    else:
        print(f"❌ Upload failed ({resp.status_code}): {file_path}")
        print(resp.text)
        return False


def expand_patterns(patterns):
    """Expand glob patterns to actual file paths."""
    files = []
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            files.extend(matches)
        else:
            # If no glob match, treat as literal file (might not exist yet)
            files.append(pattern)
    return files


def main():
    if len(sys.argv) < 3:
        print("Usage: python zenodo_upload.py <deposition_id> <file1> [file2] ...")
        sys.exit(1)

    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        print("❌ ZENODO_TOKEN not set")
        sys.exit(1)

    dep_id = sys.argv[1]
    patterns = sys.argv[2:]

    # Expand glob patterns
    files = expand_patterns(patterns)

    if not files:
        print("❌ No files to upload")
        sys.exit(1)

    # Get files endpoint URL
    files_url = get_files_url(token, dep_id)
    print(f"Using files endpoint: {files_url}")

    # Upload all files
    failed = []
    for file_path in files:
        if not upload_file(token, files_url, file_path):
            failed.append(file_path)

    if failed:
        print(f"❌ {len(failed)} file(s) failed to upload")
        sys.exit(1)

    print(f"✅ All {len(files)} files uploaded successfully")


if __name__ == "__main__":
    main()