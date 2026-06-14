# Reproduction Guide

This guide explains how the generated tables should be read and how the implemented computations correspond to the published examples.

## Pipeline

From the repository root:

```powershell
uv sync
uv run python scripts/reproduce_examples.py
uv run python scripts/make_figures.py
uv run python scripts/validate.py
uv run pytest
```

The public Python API is exposed through `np1933.api`:

- `run_example(example_id: str) -> ExampleResult`
- `run_all_examples() -> list[ExampleResult]`
- `generate_figure(figure_id: str) -> FigureResult`
- `validate_all() -> list[ValidationResult]`

## Reading The Numeric Tables

`outputs/tables/critical_values.csv` contains every numeric result row from Examples 1, 2, and 8-11. `outputs/tables/power_values.csv` contains the subset of rows with non-null `alternative_probability`, which in this repository is the Example 2 acceptance-probability comparison.

The key public columns are:

- `status`: interpretation class for the row. Numeric rows are either `paper_rounded_numeric` or `exact_numeric`.
- `paper_value`: the value printed or rounded in the paper when the row is compared against a historical rounded target.
- `paper_rounding_digits`: the number of decimal places used for the rounded comparison.
- `computed_value`: the modern numerical value computed with SciPy.
- `abs_error`: for `paper_rounded_numeric`, the absolute difference between the rounded `computed_value` and `paper_value`; for `exact_numeric`, the recorded comparison error carried by the implementation.
- `rounding_match`: `True` when the row matches the declared interpretation rule.
- `description`: a short explanation of what the row represents.
- `source_equations`: semicolon-separated equation identifiers linked to `data/interim/referenced_equations.csv`.

Paper-rounded values such as `1.6449`, `15.086`, `13.277`, `0.42`, `0.11`, `0.49`, and `0.17` should be read as published rounded targets. They are not treated as exact mathematical constants.

The validation rules follow the status:

- `paper_rounded_numeric`: `round(computed_value, paper_rounding_digits) == paper_value`;
- `exact_numeric`: `abs_error` is required to be zero within the repository's `1e-12` numeric tolerance, and the null tail probabilities used in the tests are checked against `0.05` to the same tolerance;
- `schematic_geometry`: the area identities in `outputs/tables/geometry_checks.csv` are checked to machine precision.

## Example 1

Example 1 reproduces the one-sided known-variance normal mean threshold by computing `norm.ppf(0.95)`. The output row is `ex01_z095` in `outputs/tables/critical_values.csv`.

- paper object: one-sided best critical region for the known-variance normal mean test;
- statistic: `standard_normal_upper_0.05_threshold`;
- status: `paper_rounded_numeric`;
- published target: `paper_value = 1.6449`, `paper_rounding_digits = 4`;
- modern computation: `computed_value = norm.ppf(0.95)`.

## Example 2

Example 2 compares two variance-testing statistics for `n = 5` and `epsilon = 0.01`:

- the known-mean second-moment statistic with `df = 5`;
- the centered sample-variance comparator with `df = 4`.

The critical-value rows appear in `outputs/tables/critical_values.csv`. The acceptance-probability rows under `sigma_1 = h sigma_0` appear in both `critical_values.csv` and `power_values.csv`.

Interpret the Example 2 rows as follows:

- `ex02_known_mean_chi2_critical`: `chi2.ppf(0.99, 5)` compared against the paper-rounded `15.086`;
- `ex02_sample_variance_chi2_critical`: `chi2.ppf(0.99, 4)` compared against the paper-rounded `13.277`;
- `ex02_known_mean_accept_h2` and `ex02_known_mean_accept_h3`: acceptance probabilities `chi2.cdf(q_known / h^2, 5)` compared against `0.42` and `0.11`;
- `ex02_sample_variance_accept_h2` and `ex02_sample_variance_accept_h3`: acceptance probabilities `chi2.cdf(q_sample / h^2, 4)` compared against `0.49` and `0.17`.

All Example 2 rows carry `status = paper_rounded_numeric`.

## Examples 4-6

`outputs/tables/geometry_checks.csv` records deterministic schematic geometry checks rather than literal reconstructions of the paper's drawings:

- Example 4 checks overlap area for two shifted rectangular sample spaces;
- Example 5 checks the central-square area formula;
- Example 6 checks the diagonal-band area formula for a range threshold.

These rows use `status = schematic_geometry`. Their `computed_value` and `abs_error` fields summarize the target area or overlap relation that is being checked. Validation and tests require these geometric equalities to hold to machine precision.

## Example 8

Example 8 records the one-sample Student critical-value relationship for `n = 10`, `df = 9`, and `epsilon = 0.05`. The row `ex08_student_one_sample_upper_tail` in `outputs/tables/critical_values.csv` is `exact_numeric`: the repository checks the null tail probability directly with `scipy.stats.t`.

This release documents the paper's cone-based interpretation but does not attempt to reproduce the full geometric derivation.

## Example 9

Example 9 records upper- and lower-tail chi-square critical values for a normal variance test with unknown mean. The rows `ex09_chi2_variance_upper_tail` and `ex09_chi2_variance_lower_tail` use `df = n - 1` and verify the corresponding null tail probabilities with `scipy.stats.chi2`.

## Example 10

Example 10 records the distributional relationship for the two-sample variance problem in two equivalent forms:

- an upper-tail F critical value;
- the corresponding upper-tail beta critical value for `U = Y2 / (Y1 + Y2)`.

The rows `ex10_f_upper_tail_variance_ratio` and `ex10_beta_equivalent_upper_tail` are `exact_numeric`. They verify the null tail probability with `scipy.stats.f` and `scipy.stats.beta`.

## Example 11

Example 11 records the two-sample equal-variance mean-test relationship through a Student critical value with `df = n1 + n2 - 2`. The row `ex11_two_sample_t_upper_tail` is `exact_numeric` and verifies its null tail probability with `scipy.stats.t`.

## Equation Registry And OCR Cross-Checking

`data/interim/referenced_equations.csv` is the equation registry used by the implemented examples, figures, and validation logic. It is not a full inventory of the paper.

Rows marked `ocr_only_pending_pdf_verification` should be read as corrected working descriptions derived from the distributed OCR text. Manual cross-checking against a locally supplied `data/raw/paper_pdf.pdf` is optional and recorded separately in the validation summary.
