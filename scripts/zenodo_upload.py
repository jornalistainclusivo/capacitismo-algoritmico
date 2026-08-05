#!/usr/bin/env python3
"""
Upload files to Zenodo deposition with fresh bucket URL.
"""
import sys
import os
import requests


def get_auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def get_fresh_bucket_url(token, dep_id):
    """Get fresh bucket URL from deposition."""
    url = f"https://zenodo.org/api/deposit/depositions/{dep_id}"
    resp = requests.get(url, headers=get_auth_headers(token))
    if resp.status_code != 200:
        print(f"❌ Failed to get deposition details: {resp.status_code}")
        print(resp.text)
        sys.exit(1)
    data = resp.json()
    return data["links"]["bucket"]


def upload_file(token, bucket_url, file_path):
    """Upload a single file to Zenodo bucket."""
    if not os.path.exists(file_path):
        print(f"⚠️ File not found: {file_path}")
        return False

    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        resp = requests.post(bucket_url, headers=get_auth_headers(token), files=files)

    if resp.status_code == 201:
        print(f"✅ Uploaded: {file_path}")
        return True
    else:
        print(f"❌ Upload failed ({resp.status_code}): {file_path}")
        print(resp.text)
        return False


def main():
    if len(sys.argv) < 4:
        print("Usage: python zenodo_upload.py <deposition_id> <file1> [file2] ...")
        sys.exit(1)

    token = os.environ.get("ZENODO_TOKEN")
    if not token:
        print("❌ ZENODO_TOKEN not set")
        sys.exit(1)

    dep_id = sys.argv[1]
    files = sys.argv[2:]

    # Get fresh bucket URL
    bucket_url = get_fresh_bucket_url(token, dep_id)
    print(f"Using bucket: {bucket_url}")

    # Upload all files
    failed = []
    for file_path in files:
        if not upload_file(token, bucket_url, file_path):
            failed.append(file_path)

    if failed:
        print(f"❌ {len(failed)} file(s) failed to upload")
        sys.exit(1)

    print(f"✅ All {len(files)} files uploaded successfully")


if __name__ == "__main__":
    main()