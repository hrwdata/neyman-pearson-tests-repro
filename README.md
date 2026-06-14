# Neyman-Pearson 1933 Reproducibility Package

This repository reproduces selected numerical examples and schematic figures from Jerzy Neyman and Egon S. Pearson's 1933 paper, *On the Problem of the Most Efficient Tests of Statistical Hypotheses*.

Manuscript: [https://doi.org/10.1098/rsta.1933.0009](https://doi.org/10.1098/rsta.1933.0009)

The package is a deterministic Python workflow for regenerating tables, figures, and local validation outputs.

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

The scanned paper PDF is not bundled. Users who want to manually cross-check OCR-derived text and corrected equation rows should obtain the manuscript from an appropriate source, such as the DOI landing page above, and place a local copy at:

```text
data/raw/paper_pdf.pdf