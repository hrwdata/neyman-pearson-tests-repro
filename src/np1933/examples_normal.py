from __future__ import annotations

from scipy.stats import chi2, norm

from np1933.models import ExampleResult, ExampleSpec

EXAMPLE_1 = ExampleSpec(
    example_id="ex01",
    title="Known-variance normal mean test",
    source_equations=["37", "38"],
    status="paper_rounded_numeric",
    parameters={"epsilon": 0.05},
)

EXAMPLE_2 = ExampleSpec(
    example_id="ex02",
    title="Known-mean normal variance test and power comparison",
    source_equations=["46", "48", "50", "51"],
    status="paper_rounded_numeric",
    parameters={"n": 5, "epsilon": 0.01},
)


def _rounded_result(
    *,
    object_id: str,
    example_id: str,
    statistic: str,
    computed: float,
    paper_value: float,
    digits: int,
    parameters: dict,
    critical_value: float | None = None,
    null_probability: float | None = None,
    alternative_probability: float | None = None,
    source_equations: list[str],
    description: str = "",
) -> ExampleResult:
    abs_error = abs(round(computed, digits) - paper_value)
    return ExampleResult(
        object_id=object_id,
        example_id=example_id,
        statistic=statistic,
        status="paper_rounded_numeric",
        parameters=parameters,
        critical_value=critical_value,
        null_probability=null_probability,
        alternative_probability=alternative_probability,
        paper_value=paper_value,
        paper_rounding_digits=digits,
        computed_value=computed,
        abs_error=abs_error,
        rounding_match=round(computed, digits) == paper_value,
        source_equations=source_equations,
        description=description,
    )


def run_example_1() -> list[ExampleResult]:
    epsilon = 0.05
    computed = float(norm.ppf(1 - epsilon))
    return [
        _rounded_result(
            object_id="ex01_z095",
            example_id="ex01",
            statistic="standard_normal_upper_0.05_threshold",
            computed=computed,
            paper_value=1.6449,
            digits=4,
            parameters={"epsilon": epsilon, "quantile": 1 - epsilon},
            critical_value=computed,
            null_probability=1 - float(norm.cdf(computed)),
            source_equations=EXAMPLE_1.source_equations,
            description="The paper reports x0-a0 = 1.6449 sigma0/sqrt(n) for epsilon=0.05.",
        )
    ]


def run_example_2() -> list[ExampleResult]:
    n = 5
    epsilon = 0.01
    known_mean_df = n
    sample_variance_df = n - 1
    q_known = float(chi2.ppf(1 - epsilon, known_mean_df))
    q_sample = float(chi2.ppf(1 - epsilon, sample_variance_df))
    results: list[ExampleResult] = []
    results.append(
        _rounded_result(
            object_id="ex02_known_mean_chi2_critical",
            example_id="ex02",
            statistic="chi_square_critical_known_mean_second_moment",
            computed=q_known,
            paper_value=15.086,
            digits=3,
            parameters={"n": n, "epsilon": epsilon, "df": known_mean_df},
            critical_value=q_known,
            null_probability=1 - float(chi2.cdf(q_known, known_mean_df)),
            source_equations=EXAMPLE_2.source_equations,
            description="Upper-tail chi-square critical value for the known-mean second-moment statistic.",
        )
    )
    results.append(
        _rounded_result(
            object_id="ex02_sample_variance_chi2_critical",
            example_id="ex02",
            statistic="chi_square_critical_sample_variance_comparator",
            computed=q_sample,
            paper_value=13.277,
            digits=3,
            parameters={"n": n, "epsilon": epsilon, "df": sample_variance_df},
            critical_value=q_sample,
            null_probability=1 - float(chi2.cdf(q_sample, sample_variance_df)),
            source_equations=EXAMPLE_2.source_equations,
            description="Upper-tail chi-square critical value for the centered sample-variance comparator.",
        )
    )
    for h, paper in [(2.0, 0.42), (3.0, 0.11)]:
        computed = float(chi2.cdf(q_known / (h * h), known_mean_df))
        results.append(
            _rounded_result(
                object_id=f"ex02_known_mean_accept_h{int(h)}",
                example_id="ex02",
                statistic="acceptance_probability_known_mean_second_moment",
                computed=computed,
                paper_value=paper,
                digits=2,
                parameters={"n": n, "epsilon": epsilon, "df": known_mean_df, "sigma_ratio": h},
                critical_value=q_known,
                alternative_probability=computed,
                source_equations=EXAMPLE_2.source_equations,
                description="Acceptance probability under sigma1=h sigma0 for the known-mean second-moment statistic.",
            )
        )
    for h, paper in [(2.0, 0.49), (3.0, 0.17)]:
        computed = float(chi2.cdf(q_sample / (h * h), sample_variance_df))
        results.append(
            _rounded_result(
                object_id=f"ex02_sample_variance_accept_h{int(h)}",
                example_id="ex02",
                statistic="acceptance_probability_sample_variance_comparator",
                computed=computed,
                paper_value=paper,
                digits=2,
                parameters={"n": n, "epsilon": epsilon, "df": sample_variance_df, "sigma_ratio": h},
                critical_value=q_sample,
                alternative_probability=computed,
                source_equations=EXAMPLE_2.source_equations,
                description="Acceptance probability under sigma1=h sigma0 for the centered sample-variance comparator.",
            )
        )
    return results
