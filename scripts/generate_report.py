#!/usr/bin/env python3
"""Generate comprehensive validation report."""
from pathlib import Path

import pandas as pd


def main():
    print("## Dataset Validation Report")
    print()
    print("Repository: jornalistainclusivo/capacitismo-algoritmico")
    print("Branch: master")
    print("Commit: latest")
    print()

    raw_files = list(Path("data/raw").glob("*.jsonl"))
    proc_files = list(Path("data/processed").glob("*.parquet"))
    schema_files = list(Path("schemas").glob("*.json"))

    print(f"📁 Raw files: {len(raw_files)}")
    print(f"📁 Processed files: {len(proc_files)}")
    print(f"📋 Schemas: {len(schema_files)}")
    print()

    total_records = 0
    for f in proc_files:
        df = pd.read_parquet(f)
        total_records += len(df)
        print(f"  - {f.name}: {len(df)} records")

    print(f"📊 Total records: {total_records}")
    print()

    if total_records > 0:
        # Load the main dataset for statistics
        df = pd.read_parquet("data/processed/incidents.parquet")

        # Category distribution
        print("### Category Distribution")
        cat_dist = df["category"].value_counts()
        for cat, count in cat_dist.items():
            pct = (count / total_records) * 100
            print(f"  - {cat}: {count} ({pct:.1f}%)")
        print()

        # Severity distribution
        print("### Severity Distribution")
        sev_dist = df["severity"].value_counts()
        for sev, count in sev_dist.items():
            pct = (count / total_records) * 100
            print(f"  - {sev}: {count} ({pct:.1f}%)")
        print()

        # Platform distribution (top 10)
        print("### Platform Distribution (Top 10)")
        platforms = df["platform"].apply(lambda x: x.get("name", "unknown") if isinstance(x, dict) else str(x))
        plat_dist = platforms.value_counts().head(10)
        for plat, count in plat_dist.items():
            pct = (count / total_records) * 100
            print(f"  - {plat}: {count} ({pct:.1f}%)")
        print()

        # Source distribution
        print("### Source Distribution")
        src_dist = df["source"].value_counts()
        for src, count in src_dist.items():
            pct = (count / total_records) * 100
            print(f"  - {src}: {count} ({pct:.1f}%)")
        print()

        # Date range
        print("### Date Range")
        timestamps = pd.to_datetime(df["timestamp"], format="ISO8601")
        print(f"  - Earliest: {timestamps.min().strftime('%Y-%m-%d')}")
        print(f"  - Latest: {timestamps.max().strftime('%Y-%m-%d')}")
        print()

        # Anonymization status
        print("### Anonymization Status")
        anon_counts = df["anonymized"].value_counts()
        for anon, count in anon_counts.items():
            pct = (count / total_records) * 100
            print(f"  - {anon}: {count} ({pct:.1f}%)")
        print()


if __name__ == "__main__":
    main()
