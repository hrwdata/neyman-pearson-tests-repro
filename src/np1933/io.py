from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd

from np1933.models import ExampleResult, FigureResult, ValidationResult

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_TABLES = ROOT / "outputs" / "tables"
OUTPUT_LOGS = ROOT / "outputs" / "logs"


def ensure_output_dirs() -> None:
    (ROOT / "outputs" / "figures").mkdir(parents=True, exist_ok=True)
    OUTPUT_TABLES.mkdir(parents=True, exist_ok=True)
    OUTPUT_LOGS.mkdir(parents=True, exist_ok=True)


def write_example_tables(results: Iterable[ExampleResult]) -> None:
    ensure_output_dirs()
    records = [r.to_record() for r in results]
    df = pd.DataFrame(records)
    numeric_stats = df[df["status"].isin(["exact_numeric", "paper_rounded_numeric"])].copy()
    power = numeric_stats[numeric_stats["alternative_probability"].notna()].copy()
    geometry = df[df["status"].eq("schematic_geometry")].copy()
    numeric_stats.to_csv(OUTPUT_TABLES / "critical_values.csv", index=False)
    power.to_csv(OUTPUT_TABLES / "power_values.csv", index=False)
    geometry.to_csv(OUTPUT_TABLES / "geometry_checks.csv", index=False)


def write_figure_inventory(results: Iterable[FigureResult]) -> None:
    ensure_output_dirs()
    records = [r.to_record() for r in results]
    for record in records:
        path = record.get("path")
        if path:
            record["path"] = Path(path).resolve().relative_to(ROOT).as_posix()
    pd.DataFrame(records).to_csv(OUTPUT_TABLES / "figure_inventory.csv", index=False)


def write_validation_summary(results: Iterable[ValidationResult]) -> None:
    ensure_output_dirs()
    payload = [r.to_record() for r in results]
    (OUTPUT_LOGS / "validation_summary.json").write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
