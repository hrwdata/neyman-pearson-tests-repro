# Neyman-Pearson 1933 Reproducibility Package

This repository reproduces selected numerical examples and schematic figures from Jerzy Neyman and Egon S. Pearson's 1933 paper, *On the Problem of the Most Efficient Tests of Statistical Hypotheses*. The package is a deterministic Python workflow for regenerating the committed tables, figures, and validation summary.

## Scope

The implemented material covers:

- paper-rounded numeric checks for Example 1 and Example 2;
- exact modern critical-value computations for Examples 8-11;
- schematic geometry checks for Examples 4-6;
- schematic figures for Figures 4, 5, 7, 8, and 10;
- a corrected equation registry for equations actually used by the implemented examples, figures, and validation logic.

Example 3, Example 7, and Figures 1, 2, 3, 6, and 9 are documented but not generated in this release.

## Source And Data Policy

The distributed source text is [data/raw/paper_ocr.txt](data/raw/paper_ocr.txt). It is useful for structure, example numbering, and published numerical targets, but it is not authoritative where OCR errors conflict with the scanned paper.

The scanned paper PDF is not bundled. For manual OCR cross-checking, place a local copy at `data/raw/paper_pdf.pdf`. The repository records the presence or absence of that optional file in the validation summary without treating its absence as a default validation failure.

The corrected equation registry is [data/interim/referenced_equations.csv](data/interim/referenced_equations.csv). It is intentionally partial: only equations used by implemented examples, figures, or validation checks are included.

## Installation

This project targets Python `>=3.11,<3.13` and uses `uv` as the canonical workflow.

```powershell
uv sync
```

## Reproduction Workflow

Regenerate numeric and geometry tables:

```powershell
uv run python scripts/reproduce_examples.py
```

Regenerate schematic figures and the figure inventory:

```powershell
uv run python scripts/make_figures.py
```

Write the validation summary:

```powershell
uv run python scripts/validate.py
```

Run the test suite:

```powershell
uv run pytest
```

## Paper Object Status

| Paper object | Repository artifact | Status | Output |
| --- | --- | --- | --- |
| Example 1 | one-sided known-variance normal mean threshold | `paper_rounded_numeric` | `outputs/tables/critical_values.csv` |
| Example 2 | chi-square critical values and acceptance probabilities | `paper_rounded_numeric` | `outputs/tables/critical_values.csv`, `outputs/tables/power_values.csv` |
| Example 3 | normal mean/variance likelihood-envelope geometry | `documented_future_work` | documented only |
| Examples 4-6 | rectangular-population geometry checks | `schematic_geometry` | `outputs/tables/geometry_checks.csv` |
| Example 7 | similar-region construction | `documented_future_work` | documented only |
| Examples 8-11 | Student, chi-square, F, and beta critical-value relationships | `exact_numeric` | `outputs/tables/critical_values.csv` |
| Figures 4, 5, 7, 8, 10 | generated schematic figures | `schematic_geometry` | `outputs/figures/` |
| Figures 1, 2, 3, 6, 9 | figure inventory entries only | `documented_future_work` | `outputs/tables/figure_inventory.csv` |

Detailed mappings appear in [docs/paper-objects.md](docs/paper-objects.md).

## Generated Outputs

The main generated artifacts are:

- [outputs/tables/critical_values.csv](outputs/tables/critical_values.csv)
- [outputs/tables/power_values.csv](outputs/tables/power_values.csv)
- [outputs/tables/geometry_checks.csv](outputs/tables/geometry_checks.csv)
- [outputs/tables/figure_inventory.csv](outputs/tables/figure_inventory.csv)
- [outputs/figures/fig04.png](outputs/figures/fig04.png)
- [outputs/figures/fig05.png](outputs/figures/fig05.png)
- [outputs/figures/fig07.png](outputs/figures/fig07.png)
- [outputs/figures/fig08.png](outputs/figures/fig08.png)
- [outputs/figures/fig10.png](outputs/figures/fig10.png)
- [outputs/logs/validation_summary.json](outputs/logs/validation_summary.json)

[docs/reproduction-guide.md](docs/reproduction-guide.md) explains how to interpret the numeric tables. [docs/artifacts.md](docs/artifacts.md) describes every distributed and generated artifact.

## Validation Model

`scripts/validate.py` checks required output files, table schemas, equation linkage for implemented examples, numeric expectations, absence of deprecated public headers such as `notes`, and repo-relative figure inventory paths. It also records the optional PDF cross-check state in [outputs/logs/validation_summary.json](outputs/logs/validation_summary.json).

Validation details appear in [docs/validation.md](docs/validation.md).

## Optional Local PDF Cross-Check

If `data/raw/paper_pdf.pdf` is present, it can be used for manual comparison against OCR-derived text and corrected equation rows. If it is absent, the validation summary reports:

```json
{
  "paper_pdf_present": false,
  "pdf_crosscheck_status": "not_run_optional_local_input_absent"
}
```

## Mathematical And Formalization Note

This repository reproduces analytic outputs and schematic reconstructions. It does not provide formal proofs of the Neyman-Pearson theory. The longer-term formal targets are summarized in [docs/formalization-roadmap.md](docs/formalization-roadmap.md).

## Limitations

- Paper-rounded values such as `1.6449`, `15.086`, `13.277`, `0.42`, `0.11`, `0.49`, and `0.17` are treated as printed targets, not as exact mathematical values.
- Generated figures are schematic mathematical illustrations, not pixel-exact historical reproductions.
- `referenced_equations.csv` is not a complete equation inventory for the paper.

## License Note

No license file is bundled with this repository. Reuse permissions are not granted by the repository itself.
