from __future__ import annotations

import math
import re
from pathlib import Path

import pandas as pd

from np1933.models import ValidationResult

ROOT = Path(__file__).resolve().parents[2]
REF_EQ_PATH = ROOT / "data" / "interim" / "referenced_equations.csv"
PDF_PATH = ROOT / "data" / "raw" / "paper_pdf.pdf"
TABLE_DIR = ROOT / "outputs" / "tables"
FIG_DIR = ROOT / "outputs" / "figures"
LOG_DIR = ROOT / "outputs" / "logs"

REQUIRED_EQUATION_COLUMNS = {
    "equation_id",
    "section",
    "raw_ocr_text",
    "corrected_math_text",
    "used_by",
    "verification_status",
}

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

IMPLEMENTED_STATUSES = {"exact_numeric", "paper_rounded_numeric", "schematic_geometry"}
ALLOWED_STATUSES = {
    "exact_numeric",
    "paper_rounded_numeric",
    "schematic_geometry",
    "documented_future_work",
    "not_implemented_v1",
}


def _looks_like_file_url(path: str) -> bool:
    return path.startswith("file" + ":" + "//")


def _looks_like_windows_absolute_path(path: str) -> bool:
    return re.match(r"^[A-Za-z]:[/\\]", path) is not None


def _result(check_id: str, passed: bool, message: str, **details) -> ValidationResult:
    return ValidationResult(
        check_id=check_id,
        passed=passed,
        status="passed" if passed else "failed",
        message=message,
        details=details,
    )


def _load_referenced_equations() -> pd.DataFrame:
    if not REF_EQ_PATH.exists():
        return pd.DataFrame(columns=sorted(REQUIRED_EQUATION_COLUMNS))
    return pd.read_csv(REF_EQ_PATH, dtype=str).fillna("")


def validate_equation_linkage() -> list[ValidationResult]:
    rows: list[ValidationResult] = []
    eq = _load_referenced_equations()
    missing_cols = sorted(REQUIRED_EQUATION_COLUMNS - set(eq.columns))
    rows.append(_result("referenced_equations_schema", not missing_cols, "referenced_equations.csv has required columns.", missing_columns=missing_cols))

    available = set(eq.get("equation_id", pd.Series(dtype=str)).astype(str))
    missing: dict[str, list[str]] = {}
    from np1933.api import run_all_examples
    for r in run_all_examples():
        if r.status in IMPLEMENTED_STATUSES:
            if not r.source_equations:
                missing[r.object_id] = ["<no source_equations>"]
                continue
            absent = [e for e in r.source_equations if e not in available]
            if absent:
                missing[r.object_id] = absent
    rows.append(_result("implemented_examples_have_equations", not missing, "Every implemented example references equations present in referenced_equations.csv.", missing=missing))

    verified = eq[eq.get("verification_status", "").astype(str).str.lower().str.contains("verified", na=False)] if not eq.empty else eq
    bad_verified = verified[~verified.get("verification_status", "").astype(str).str.lower().str.contains("pdf", na=False)] if not verified.empty else verified
    rows.append(_result("verified_rows_record_pdf_check", bad_verified.empty, "Rows marked verified record PDF verification status.", bad_rows=bad_verified.to_dict(orient="records")))
    return rows


def validate_numeric_results() -> list[ValidationResult]:
    rows: list[ValidationResult] = []
    from np1933.api import run_all_examples
    examples = run_all_examples()
    rounded_failures = [r.object_id for r in examples if r.status == "paper_rounded_numeric" and r.rounding_match is not True]
    rows.append(_result("paper_rounded_numeric_matches", not rounded_failures, "Paper-rounded numeric examples match the published rounded values.", failures=rounded_failures))

    probability_failures = []
    for r in examples:
        for field_name, value in [("null_probability", r.null_probability), ("alternative_probability", r.alternative_probability)]:
            if value is not None and not (-1e-12 <= value <= 1 + 1e-12):
                probability_failures.append({"object_id": r.object_id, "field": field_name, "value": value})
    rows.append(_result("probabilities_in_unit_interval", not probability_failures, "All computed probabilities lie in [0, 1].", failures=probability_failures))

    exact_failures = [r.object_id for r in examples if r.status == "exact_numeric" and not math.isclose(float(r.abs_error or 0.0), 0.0, abs_tol=1e-12)]
    rows.append(_result("exact_numeric_zero_internal_error", not exact_failures, "Exact numeric rows have zero internal comparison error.", failures=exact_failures))
    return rows


def validate_artifacts() -> list[ValidationResult]:
    rows: list[ValidationResult] = []
    expected_tables = ["critical_values.csv", "power_values.csv", "geometry_checks.csv", "figure_inventory.csv"]
    missing_tables = [name for name in expected_tables if not (TABLE_DIR / name).exists()]
    rows.append(_result("declared_tables_exist", not missing_tables, "All declared output tables exist.", missing=missing_tables))

    expected_figures = ["fig04.png", "fig05.png", "fig07.png", "fig08.png", "fig10.png"]
    missing_figures = [name for name in expected_figures if not (FIG_DIR / name).exists()]
    rows.append(_result("declared_figures_exist", not missing_figures, "Implemented schematic figures exist.", missing=missing_figures))

    schema_failures: dict[str, list[str]] = {}
    for name in ["critical_values.csv", "power_values.csv", "geometry_checks.csv"]:
        path = TABLE_DIR / name
        if path.exists():
            df = pd.read_csv(path)
            missing = sorted(REQUIRED_RESULT_COLUMNS - set(df.columns))
            if missing:
                schema_failures[name] = missing
    rows.append(_result("result_table_schemas", not schema_failures, "Result tables contain required standard columns.", failures=schema_failures))

    deprecated_headers: dict[str, list[str]] = {}
    for name in ["critical_values.csv", "power_values.csv", "geometry_checks.csv", "figure_inventory.csv"]:
        path = TABLE_DIR / name
        if path.exists():
            df = pd.read_csv(path)
            if "notes" in df.columns:
                deprecated_headers[name] = ["notes"]
    rows.append(_result("deprecated_output_headers_absent", not deprecated_headers, "Public output headers do not include deprecated fields.", failures=deprecated_headers))

    fig_inv = TABLE_DIR / "figure_inventory.csv"
    fig_status_failure: list[dict[str, str]] = []
    bad_paths: list[dict[str, str]] = []
    if fig_inv.exists():
        df = pd.read_csv(fig_inv)
        expected_ids = {"fig01", "fig02", "fig03", "fig04", "fig05", "fig06", "fig07", "fig08", "fig09", "fig10"}
        actual_ids = set(df.get("figure_id", pd.Series(dtype=str)).astype(str))
        missing_ids = sorted(expected_ids - actual_ids)
        for _, row in df.iterrows():
            if str(row.get("status")) not in ALLOWED_STATUSES:
                fig_status_failure.append({"figure_id": str(row.get("figure_id")), "status": str(row.get("status"))})
            path = str(row.get("path", ""))
            if path and (Path(path).is_absolute() or _looks_like_windows_absolute_path(path) or _looks_like_file_url(path)):
                bad_paths.append({"figure_id": str(row.get("figure_id")), "path": path})
    else:
        missing_ids = sorted({"fig01", "fig02", "fig03", "fig04", "fig05", "fig06", "fig07", "fig08", "fig09", "fig10"})
    rows.append(_result("figure_inventory_complete", not missing_ids and not fig_status_failure and not bad_paths, "Figure inventory includes implemented and deferred figures with allowed statuses and repo-relative paths.", missing_ids=missing_ids, bad_statuses=fig_status_failure, bad_paths=bad_paths))
    return rows


def validate_sources() -> list[ValidationResult]:
    pdf_present = PDF_PATH.exists()
    return [
        _result("paper_ocr_exists", (ROOT / "data" / "raw" / "paper_ocr.txt").exists(), "OCR source text exists."),
        _result(
            "pdf_crosscheck_state",
            True,
            "Optional local PDF cross-check status recorded.",
            paper_pdf_present=pdf_present,
            pdf_crosscheck_status="available_for_manual_crosscheck" if pdf_present else "not_run_optional_local_input_absent",
        ),
    ]


def validate_all() -> list[ValidationResult]:
    return validate_sources() + validate_equation_linkage() + validate_numeric_results() + validate_artifacts()
