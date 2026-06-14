from __future__ import annotations

from np1933.examples_composite import run_example_8, run_example_9, run_example_10, run_example_11
from np1933.examples_geometry import run_geometry_examples
from np1933.examples_normal import run_example_1, run_example_2
from np1933.figures import generate_figure as _generate_figure
from np1933.models import ExampleResult, FigureResult, ValidationResult
from np1933.validation import validate_all as _validate_all

_NUMERIC_RUNNERS = {
    "ex01": run_example_1,
    "ex02": run_example_2,
    "ex08": run_example_8,
    "ex09": run_example_9,
    "ex10": run_example_10,
    "ex11": run_example_11,
}


def run_example(example_id: str) -> ExampleResult:
    results = _run_example_many(example_id)
    if not results:
        raise ValueError(f"No result produced for {example_id!r}.")
    return results[0]


def _run_example_many(example_id: str) -> list[ExampleResult]:
    normalized = example_id.lower()
    if normalized in _NUMERIC_RUNNERS:
        return _NUMERIC_RUNNERS[normalized]()
    if normalized in {"ex03", "ex04", "ex05", "ex06", "ex07"}:
        return [r for r in run_geometry_examples() if r.example_id == normalized]
    raise ValueError(f"Unknown example_id {example_id!r}.")


def run_all_examples() -> list[ExampleResult]:
    results: list[ExampleResult] = []
    for runner in _NUMERIC_RUNNERS.values():
        results.extend(runner())
    results.extend(run_geometry_examples())
    return results


def generate_figure(figure_id: str) -> FigureResult:
    return _generate_figure(figure_id)


def validate_all() -> list[ValidationResult]:
    return _validate_all()
