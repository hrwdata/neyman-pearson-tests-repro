from __future__ import annotations

import pandas as pd

from np1933.api import run_all_examples


def test_every_implemented_example_has_linked_equation_row():
    eq = pd.read_csv("data/interim/referenced_equations.csv", dtype=str).fillna("")
    equation_ids = set(eq["equation_id"])
    implemented_statuses = {"exact_numeric", "paper_rounded_numeric", "schematic_geometry"}
    for result in run_all_examples():
        if result.status in implemented_statuses:
            assert result.source_equations, result.object_id
            assert set(result.source_equations).issubset(equation_ids), result.object_id


def test_verified_rows_record_manual_pdf_status_if_present():
    eq = pd.read_csv("data/interim/referenced_equations.csv", dtype=str).fillna("")
    verified = eq[eq["verification_status"].str.lower().str.contains("verified")]
    for _, row in verified.iterrows():
        assert "pdf" in row["verification_status"].lower()
