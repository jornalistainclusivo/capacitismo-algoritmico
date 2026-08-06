#!/usr/bin/env python3
"""
Exporta dataset processado para CSV/Parquet para análise
Referenciado em README.md e docs/contributing.md

Uso:
    python scripts/export.py --input data/processed/incidents.parquet --output data/exports/ --format csv
    python scripts/export.py --input data/processed/incidents.parquet --output data/exports/ --format parquet --partition-by category
    python scripts/export.py --input data/processed/incidents.parquet --output data/exports/incidents.csv --format csv --columns incident_id,category,severity,platform,timestamp
"""

import argparse
import sys
from pathlib import Path

# Adiciona path para imports locais
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError as e:
    print(f"Erro: dependências não instaladas. Rode: pip install pandas pyarrow\n{e}", file=sys.stderr)
    sys.exit(1)


def load_parquet(input_path: Path) -> pd.DataFrame:
    """Carrega arquivo Parquet processado."""
    if not input_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")
    return pd.read_parquet(input_path)


def export_csv(df: pd.DataFrame, output_path: Path, columns: list[str] | None = None) -> None:
    """Exporta para CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if columns:
        df = df[columns]
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"CSV exportado: {output_path} ({len(df)} linhas, {len(df.columns)} colunas)")


def export_parquet(df: pd.DataFrame, output_path: Path, partition_by: str | None = None) -> None:
    """Exporta para Parquet, opcionalmente particionado."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pandas(df)

    if partition_by and partition_by in df.columns:
        # Cria dataset particionado
        pq.write_to_dataset(
            table,
            root_path=str(output_path),
            partition_cols=[partition_by],
            compression="snappy",
        )
        print(f"Parquet particionado exportado: {output_path}/ (particionado por {partition_by})")
    else:
        # Arquivo único
        pq.write_table(table, str(output_path), compression="snappy")
        print(f"Parquet exportado: {output_path} ({len(df)} linhas, {len(df.columns)} colunas)")


def export_jsonl(df: pd.DataFrame, output_path: Path) -> None:
    """Exporta para JSONL (formato raw)."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_json(output_path, orient="records", lines=True, force_ascii=False)
    print(f"JSONL exportado: {output_path} ({len(df)} linhas)")


def export_summary_stats(df: pd.DataFrame, output_path: Path) -> None:
    """Gera estatísticas resumidas do dataset."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    stats = {
        "total_incidents": len(df),
        "unique_platforms": df["platform"].nunique() if "platform" in df.columns else 0,
        "unique_categories": df["category"].nunique() if "category" in df.columns else 0,
        "severity_distribution": df["severity"].value_counts().to_dict() if "severity" in df.columns else {},
        "category_distribution": df["category"].value_counts().to_dict() if "category" in df.columns else {},
        "platform_distribution": df["platform"].value_counts().to_dict() if "platform" in df.columns else {},
        "date_range": {
            "min": df["timestamp"].min() if "timestamp" in df.columns else None,
            "max": df["timestamp"].max() if "timestamp" in df.columns else None,
        },
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
    }

    import json
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False, default=str)
    print(f"Estatísticas exportadas: {output_path}")


def filter_dataframe(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Aplica filtros ao DataFrame."""
    filtered = df.copy()
    for col, value in filters.items():
        if col in filtered.columns:
            if isinstance(value, list):
                filtered = filtered[filtered[col].isin(value)]
            else:
                filtered = filtered[filtered[col] == value]
    return filtered


def main():
    parser = argparse.ArgumentParser(description="Exporta dataset processado para análise")
    parser.add_argument("--input", type=Path, required=True, help="Arquivo Parquet de entrada (data/processed/incidents.parquet)")
    parser.add_argument("--output", type=Path, required=True, help="Diretório ou arquivo de saída")
    parser.add_argument("--format", choices=["csv", "parquet", "jsonl", "stats"], default="csv", help="Formato de saída")
    parser.add_argument("--columns", type=str, help="Colunas para exportar (separadas por vírgula)")
    parser.add_argument("--partition-by", type=str, help="Coluna para particionar Parquet (ex: category, platform, severity)")
    parser.add_argument("--filter", action="append", help="Filtro no formato coluna=valor (pode repetir)")
    parser.add_argument("--filter-in", action="append", help="Filtro IN no formato coluna=valor1,valor2 (pode repetir)")

    args = parser.parse_args()

    # Carrega dados
    print(f"Carregando: {args.input}", file=sys.stderr)
    df = load_parquet(args.input)
    print(f"  {len(df)} incidentes carregados", file=sys.stderr)

    # Aplica filtros
    if args.filter:
        filters = {}
        for f in args.filter:
            if "=" in f:
                col, val = f.split("=", 1)
                filters[col] = val
        df = filter_dataframe(df, filters)
        print(f"  Após filtros: {len(df)} incidentes", file=sys.stderr)

    if args.filter_in:
        filters_in = {}
        for f in args.filter_in:
            if "=" in f:
                col, vals = f.split("=", 1)
                filters_in[col] = vals.split(",")
        df = filter_dataframe(df, filters_in)
        print(f"  Após filtros IN: {len(df)} incidentes", file=sys.stderr)

    # Seleciona colunas
    columns = None
    if args.columns:
        columns = [c.strip() for c in args.columns.split(",")]
        missing = set(columns) - set(df.columns)
        if missing:
            print(f"Aviso: colunas não encontradas: {missing}", file=sys.stderr)
            columns = [c for c in columns if c in df.columns]

    # Exporta
    try:
        if args.format == "csv":
            export_csv(df, args.output, columns)
        elif args.format == "parquet":
            export_parquet(df, args.output, args.partition_by)
        elif args.format == "jsonl":
            export_jsonl(df, args.output)
        elif args.format == "stats":
            export_summary_stats(df, args.output)
        else:
            print(f"Formato não suportado: {args.format}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Erro na exportação: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
