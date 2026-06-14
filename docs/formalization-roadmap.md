# Formalization Roadmap

This repository does not ship Lean files or other formal proofs. The purpose of this document is to identify the mathematical targets that would matter for a future standalone formalization project once the analytic reproduction in this repository is stable and well-audited.

## Future target 1: statistical experiment primitives

Define a statistical experiment as a measurable sample space, a base measure, and a parameter-indexed family of densities. Define critical regions, size, power, simple hypotheses, composite hypotheses, and likelihood-ratio regions.

Main blockers:

- choosing a stable density representation;
- managing real-valued versus nonnegative extended-real integrals;
- avoiding unnecessary smooth-geometry assumptions from the paper.

## Future target 2: simple Neyman-Pearson lemma

Formalize the simple-vs-simple optimality result using the set-difference integral inequality rather than the paper's variational boundary argument.

Main blockers:

- boundary randomization or tie handling on `{p0 = k p1}`;
- measurable-set algebra and integral monotonicity lemmas;
- exact-size assumptions.

## Future target 3: normal examples

Formalize Examples 1 and 2 first. These require finite products of normal measures, sample mean and sum-of-squares statistics, and chi-square distributional facts.

Main blockers:

- distribution of finite sums of squared centered normal variables;
- sample-variance convention alignment with the paper.

## Future target 4: Student, chi-square, F, and beta examples

Formalize Examples 8-11 after the simpler normal examples. These require independence of sample mean and sample variance, pooled variance, Student t distribution, F distribution, and beta-transform relationships.

Main blockers:

- t/F/beta distribution infrastructure and transformation lemmas;
- two-sample independence bookkeeping;
- exact alignment between paper notation and modern conventions.

## Future target 5: composite-hypothesis similar-region theory

The general theory in Sections IV-V uses differentiability under the integral sign, score-level hypersurfaces, moment determinacy, and conditional optimization on level sets. This should not be the first formalization target.

Main blockers:

- conditional measures on statistic-level sets;
- measurable selection for replacing better pieces of level sets;
- Hamburger moment problem assumptions;
- geometric hypersurface language not directly suited to early Lean development.

## Not yet formalized in this repository

- Example 3: normal mean/variance envelope geometry.
- Example 7: general similar-region construction.
