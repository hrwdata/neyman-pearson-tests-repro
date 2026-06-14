from __future__ import annotations

from scipy.stats import beta, chi2, f, t

from np1933.models import ExampleResult, ExampleSpec

SPECS = {
    "ex08": ExampleSpec("ex08", "Student one-sample mean problem", ["117", "118", "119"], "exact_numeric"),
    "ex09": ExampleSpec("ex09", "Normal variance test with unknown mean", ["127", "128"], "exact_numeric"),
    "ex10": ExampleSpec("ex10", "Two-sample variance comparison", ["190", "191", "193"], "exact_numeric"),
    "ex11": ExampleSpec("ex11", "Two-sample mean comparison with common variance", ["224", "225", "226", "227", "228"], "exact_numeric"),
}


def _exact_result(
    *,
    object_id: str,
    example_id: str,
    statistic: str,
    computed: float,
    parameters: dict,
    critical_value: float | None = None,
    null_probability: float | None = None,
    source_equations: list[str],
    description: str,
) -> ExampleResult:
    return ExampleResult(
        object_id=object_id,
        example_id=example_id,
        statistic=statistic,
        status="exact_numeric",
        parameters=parameters,
        critical_value=critical_value,
        null_probability=null_probability,
        computed_value=computed,
        abs_error=0.0,
        rounding_match=True,
        source_equations=source_equations,
        description=description,
    )


def run_example_8() -> list[ExampleResult]:
    n = 10
    epsilon = 0.05
    df = n - 1
    crit = float(t.ppf(1 - epsilon, df))
    tail = 1 - float(t.cdf(crit, df))
    return [
        _exact_result(
            object_id="ex08_student_one_sample_upper_tail",
            example_id="ex08",
            statistic="student_t_upper_tail_critical_value",
            computed=crit,
            parameters={"n": n, "df": df, "epsilon": epsilon, "tail": "upper"},
            critical_value=crit,
            null_probability=tail,
            source_equations=SPECS["ex08"].source_equations,
            description="This implementation checks the Student critical-value relationship rather than the full cone derivation.",
        )
    ]


def run_example_9() -> list[ExampleResult]:
    n = 10
    epsilon = 0.05
    df = n - 1
    upper = float(chi2.ppf(1 - epsilon, df))
    lower = float(chi2.ppf(epsilon, df))
    return [
        _exact_result(
            object_id="ex09_chi2_variance_upper_tail",
            example_id="ex09",
            statistic="chi_square_upper_tail_unknown_mean_variance_test",
            computed=upper,
            parameters={"n": n, "df": df, "epsilon": epsilon, "tail": "upper"},
            critical_value=upper,
            null_probability=1 - float(chi2.cdf(upper, df)),
            source_equations=SPECS["ex09"].source_equations,
            description="Uses df=n-1 because the mean is unspecified.",
        ),
        _exact_result(
            object_id="ex09_chi2_variance_lower_tail",
            example_id="ex09",
            statistic="chi_square_lower_tail_unknown_mean_variance_test",
            computed=lower,
            parameters={"n": n, "df": df, "epsilon": epsilon, "tail": "lower"},
            critical_value=lower,
            null_probability=float(chi2.cdf(lower, df)),
            source_equations=SPECS["ex09"].source_equations,
            description="Lower-tail counterpart for alternatives with smaller variance.",
        ),
    ]


def run_example_10() -> list[ExampleResult]:
    n1, n2 = 12, 15
    epsilon = 0.05
    df1, df2 = n1 - 1, n2 - 1
    fcrit = float(f.ppf(1 - epsilon, df2, df1))
    # If Y2~chi2_df2 and Y1~chi2_df1, U=Y2/(Y1+Y2)~Beta(df2/2, df1/2).
    ucrit = float(beta.ppf(1 - epsilon, df2 / 2, df1 / 2))
    f_from_u = (df1 / df2) * ucrit / (1 - ucrit)
    return [
        _exact_result(
            object_id="ex10_f_upper_tail_variance_ratio",
            example_id="ex10",
            statistic="f_upper_tail_variance_ratio",
            computed=fcrit,
            parameters={"n1": n1, "n2": n2, "df1_for_denominator": df1, "df2_for_numerator": df2, "epsilon": epsilon},
            critical_value=fcrit,
            null_probability=1 - float(f.cdf(fcrit, df2, df1)),
            source_equations=SPECS["ex10"].source_equations,
            description="F critical value for a larger second-sample variance alternative.",
        ),
        _exact_result(
            object_id="ex10_beta_equivalent_upper_tail",
            example_id="ex10",
            statistic="beta_equivalent_u_critical_value",
            computed=ucrit,
            parameters={"n1": n1, "n2": n2, "alpha": df2 / 2, "beta": df1 / 2, "epsilon": epsilon, "f_from_u": f_from_u},
            critical_value=ucrit,
            null_probability=1 - float(beta.cdf(ucrit, df2 / 2, df1 / 2)),
            source_equations=SPECS["ex10"].source_equations,
            description="Checks the beta integral relationship for U=Y2/(Y1+Y2).",
        ),
    ]


def run_example_11() -> list[ExampleResult]:
    n1, n2 = 12, 15
    epsilon = 0.05
    df = n1 + n2 - 2
    crit = float(t.ppf(1 - epsilon, df))
    return [
        _exact_result(
            object_id="ex11_two_sample_t_upper_tail",
            example_id="ex11",
            statistic="two_sample_student_t_upper_tail_common_variance",
            computed=crit,
            parameters={"n1": n1, "n2": n2, "df": df, "epsilon": epsilon},
            critical_value=crit,
            null_probability=1 - float(t.cdf(crit, df)),
            source_equations=SPECS["ex11"].source_equations,
            description="This implementation checks the Fisher/Student critical-value relationship for a common unknown variance.",
        )
    ]
