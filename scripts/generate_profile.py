#!/usr/bin/env python3
"""
Generate data profiling report using ydata-profiling.
Run as part of CI to produce HTML artifact with dataset statistics.
"""
import pandas as pd
import sys
from pathlib import Path

try:
    from ydata_profiling import ProfileReport
except ImportError:
    print("ydata-profiling not installed. Run: pip install ydata-profiling")
    sys.exit(1)

def generate_profile():
    processed_dir = Path("data/processed")
    output_dir = Path("profiling-reports")
    output_dir.mkdir(exist_ok=True)

    for parquet_file in processed_dir.glob("*.parquet"):
        print(f"📊 Generating profile for {parquet_file.name}...")
        df = pd.read_parquet(parquet_file)

        # Generate profile report
        profile = ProfileReport(
            df,
            title=f"Capacitismo Algorítmico - {parquet_file.stem}",
            explorative=True,
            minimal=False,
            html={
                "style": {
                    "theme": "flatly"
                }
            }
        )

        output_file = output_dir / f"{parquet_file.stem}_profile.html"
        profile.to_file(output_file)
        print(f"✅ Profile saved to {output_file}")

        # Also generate a summary JSON for programmatic access
        summary_file = output_dir / f"{parquet_file.stem}_profile.json"
        df.describe(include="all").to_json(summary_file)
        print(f"✅ Summary JSON saved to {summary_file}")

    print(f"\n✅ All profiling reports saved to {output_dir}/")
    return 0

if __name__ == "__main__":
    sys.exit(generate_profile())