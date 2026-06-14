# Validation

`scripts/validate.py` writes `outputs/logs/validation_summary.json` and exits successfully when all required public checks pass.

## What Is Checked

The validation summary records:

- presence of the distributed OCR text source;
- optional PDF cross-check state for `data/raw/paper_pdf.pdf`;
- schema of `data/interim/referenced_equations.csv`;
- equation linkage for every implemented example;
- PDF-verification wording for rows marked as verified in the equation registry;
- paper-rounded numeric comparisons;
- probability bounds for computed tail or acceptance probabilities;
- zero recorded comparison error for `exact_numeric` rows;
- presence of declared output tables and figures;
- required table columns, including `description`;
- absence of deprecated public headers such as `notes`;
- completeness and path hygiene of `outputs/tables/figure_inventory.csv`.

For the numeric examples, the validation model distinguishes three cases:

- `paper_rounded_numeric`: the repository checks agreement with the published rounded value at the declared number of digits;
- `exact_numeric`: the repository requires zero recorded comparison error and uses `1e-12` tolerances in the numeric tests for the associated tail probabilities;
- `schematic_geometry`: the repository checks area identities to machine precision.

## Optional PDF Status

Manual OCR cross-checking is optional. When `data/raw/paper_pdf.pdf` is absent, the validation summary includes:

```json
{
  "paper_pdf_present": false,
  "pdf_crosscheck_status": "not_run_optional_local_input_absent"
}
```

That condition is informational. It does not make public validation fail.

## Output Interpretation

Each validation row has:

- `check_id`: stable identifier for the check;
- `passed`: boolean result;
- `status`: `passed` or `failed`;
- `message`: short human-readable description;
- `details`: structured data for follow-up inspection.

The validation summary is intended to be machine-readable and auditable. It does not silently upgrade OCR-derived formulas to verified status.
