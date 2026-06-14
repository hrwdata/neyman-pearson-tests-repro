from __future__ import annotations

from scipy.stats import chi2, norm

from np1933.api import run_all_examples, run_example


def _by_object():
    return {r.object_id: r for r in run_all_examples()}


def test_example_1_threshold_matches_paper_rounding():
    r = run_example("ex01")
    assert round(r.computed_value, 4) == 1.6449
    assert abs(r.computed_value - norm.ppf(0.95)) < 1e-12
    assert r.rounding_match is True


def test_example_2_chi_square_values_match_paper_rounding():
    rows = _by_object()
    assert round(rows["ex02_known_mean_chi2_critical"].computed_value, 3) == 15.086
    assert round(rows["ex02_sample_variance_chi2_critical"].computed_value, 3) == 13.277
    assert round(rows["ex02_known_mean_accept_h2"].computed_value, 2) == 0.42
    assert round(rows["ex02_known_mean_accept_h3"].computed_value, 2) == 0.11
    assert round(rows["ex02_sample_variance_accept_h2"].computed_value, 2) == 0.49
    assert round(rows["ex02_sample_variance_accept_h3"].computed_value, 2) == 0.17
    assert abs(rows["ex02_known_mean_chi2_critical"].computed_value - chi2.ppf(0.99, 5)) < 1e-12


def test_examples_8_to_11_have_valid_tail_probabilities():
    rows = [r for r in run_all_examples() if r.example_id in {"ex08", "ex09", "ex10", "ex11"}]
    assert rows
    for r in rows:
        assert r.status == "exact_numeric"
        assert r.null_probability is not None
        assert abs(r.null_probability - 0.05) < 1e-12
        assert r.critical_value is not None
