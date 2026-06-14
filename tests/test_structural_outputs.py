from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_RESULT_COLUMNS = {
    "object_id",
    "example_id",
    "statistic",
    "status",
    "critical_value",
    "null_probability",
    "alternative_probability",
    "paper_value",
    "paper_rounding_digits",
    "computed_value",
    "abs_error",
    "rounding_match",
    "source_equations",
    "description",
}


def test_scripts_create_declared_outputs():
    subprocess.run([sys.executable, "scripts/reproduce_examples.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "scripts/make_figures.py"], cwd=ROOT, check=True)

    for path in [
        ROOT / "outputs/tables/critical_values.csv",
        ROOT / "outputs/tables/power_values.csv",
        ROOT / "outputs/tables/geometry_checks.csv",
        ROOT / "outputs/tables/figure_inventory.csv",
    ]:
        assert path.exists()
        assert path.stat().st_size > 0

    for path in [
        ROOT / "outputs/figures/fig04.png",
        ROOT / "outputs/figures/fig05.png",
        ROOT / "outputs/figures/fig07.png",
        ROOT / "outputs/figures/fig08.png",
        ROOT / "outputs/figures/fig10.png",
    ]:
        assert path.exists()
        assert path.stat().st_size > 0


def test_output_table_schemas_after_scripts():
    subprocess.run([sys.executable, "scripts/reproduce_examples.py"], cwd=ROOT, check=True)
    for name in ["critical_values.csv", "power_values.csv", "geometry_checks.csv"]:
        df = pd.read_csv(ROOT / "outputs/tables" / name)
        assert REQUIRED_RESULT_COLUMNS.issubset(set(df.columns))
        assert "notes" not in df.columns
        assert len(df) > 0


def test_figure_inventory_has_implemented_and_deferred_statuses():
    subprocess.run([sys.executable, "scripts/make_figures.py"], cwd=ROOT, check=True)
    df = pd.read_csv(ROOT / "outputs/tables/figure_inventory.csv")
    assert set(df["figure_id"]) == {"fig01", "fig02", "fig03", "fig04", "fig05", "fig06", "fig07", "fig08", "fig09", "fig10"}
    implemented = set(df[df["path"].notna()]["figure_id"])
    assert implemented == {"fig04", "fig05", "fig07", "fig08", "fig10"}
    assert "description" in df.columns
    assert "notes" not in df.columns
    assert all(not Path(path).is_absolute() for path in df["path"].dropna())


def test_validate_script_records_optional_pdf_status():
    subprocess.run([sys.executable, "scripts/validate.py"], cwd=ROOT, check=True)
    payload = json.loads((ROOT / "outputs/logs/validation_summary.json").read_text(encoding="utf-8"))
    row = next(item for item in payload if item["check_id"] == "pdf_crosscheck_state")
    details = row["details"]
    assert "paper_pdf_present" in details
    assert "pdf_crosscheck_status" in details
