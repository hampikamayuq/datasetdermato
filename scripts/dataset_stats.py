"""Generate dataset statistics for paper submission (Table 1) and audit.

Usage:
    python scripts/dataset_stats.py              # print summary to stdout
    python scripts/dataset_stats.py --csv        # also save stats/dataset_stats.csv
    python scripts/dataset_stats.py --only meta  # only metadata table
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))

from dataset_constants import CORE_META, MANIFEST, RELATIONAL_DIR


def _load() -> "pd.DataFrame":
    import pandas as pd

    paths = [MANIFEST, CORE_META]
    for path in paths:
        if path.exists() and path.stat().st_size > 0:
            df = pd.read_csv(path, dtype=str).fillna("")
            if len(df):
                return df
    return pd.DataFrame()


def _table(df: "pd.DataFrame", column: str, label: str) -> list[tuple[str, int, str]]:
    if column not in df.columns:
        return []
    counts = df[column].replace("", "(vazio)").value_counts()
    total = len(df)
    rows = []
    for value, n in counts.items():
        rows.append((str(value), int(n), f"{100 * n / total:.1f}%"))
    return rows


def _print_section(title: str, rows: list[tuple[str, int, str]]) -> None:
    if not rows:
        return
    col_w = max(len(r[0]) for r in rows)
    col_w = max(col_w, len(title))
    print(f"\n{title}")
    print("-" * (col_w + 20))
    for value, n, pct in rows:
        print(f"  {value:<{col_w}}  {n:>6}  {pct:>7}")
    print()


def _completeness(df: "pd.DataFrame") -> list[tuple[str, int, str]]:
    total = len(df)
    if total == 0:
        return []
    fields = [
        ("patient_id", "Paciente identificado"),
        ("lesion_id", "Lesão identificada"),
        ("image_type", "Tipo de imagem"),
        ("diagnosis", "Diagnóstico"),
        ("diagnosis_original", "Diagnóstico original"),
        ("fitzpatrick_skin_type", "Fototipo (Fitzpatrick)"),
        ("anatom_site_general", "Topografia"),
        ("age", "Idade"),
        ("sex", "Sexo"),
    ]
    rows = []
    for col, label in fields:
        if col in df.columns:
            filled = int((df[col] != "").sum())
            rows.append((label, filled, f"{100 * filled / total:.1f}%"))
    return rows


def generate(csv_out: Path | None = None, only: str = "all") -> None:
    try:
        import pandas as pd
    except ImportError:
        sys.exit("pandas is required: pip install pandas")

    df = _load()
    total = len(df)

    print("=" * 50)
    print("DATASET STATISTICS")
    print("=" * 50)
    print(f"\nTotal de imagens: {total}")

    if total == 0:
        print("Nenhuma imagem registrada ainda.")
        return

    sections = {
        "diagnosis": ("Diagnóstico (diagnosis)", "diagnosis_original"),
        "image_type": ("Tipo de imagem", "image_type"),
        "source": ("Fonte (source_id)", "source_id"),
        "specialty": ("Subespecialidade", "specialty_service"),
        "evidence": ("Nível de evidência", "evidence_level"),
        "quality": ("Status de qualidade", "quality_status"),
        "split": ("Split (train/val/test)", "split"),
        "skin_type": ("Fototipo (Fitzpatrick)", "fitzpatrick_skin_type"),
        "sex": ("Sexo", "sex"),
        "source_type": ("Origem do caso", "source_type"),
    }

    for key, (label, col) in sections.items():
        if only not in ("all", key):
            continue
        _print_section(label, _table(df, col, label))

    if only in ("all", "completeness"):
        _print_section("Completude dos campos", _completeness(df))

    if csv_out:
        rows = []
        for label, col in sections.values():
            for value, n, pct in _table(df, col, label):
                rows.append({"grupo": label, "valor": value, "n": n, "pct": pct})
        import pandas as pd
        csv_out.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rows).to_csv(csv_out, index=False)
        print(f"Estatísticas salvas em: {csv_out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate dataset statistics.")
    parser.add_argument("--csv", action="store_true", help="Save stats to stats/dataset_stats.csv")
    parser.add_argument(
        "--only",
        default="all",
        choices=["all", "diagnosis", "image_type", "source", "specialty",
                 "evidence", "quality", "split", "skin_type", "sex",
                 "source_type", "completeness"],
        help="Which section to show",
    )
    args = parser.parse_args()
    csv_out = REPO_ROOT / "stats" / "dataset_stats.csv" if args.csv else None
    generate(csv_out=csv_out, only=args.only)


if __name__ == "__main__":
    main()
