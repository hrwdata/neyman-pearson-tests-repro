from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

Status = Literal[
    "exact_numeric",
    "paper_rounded_numeric",
    "schematic_geometry",
    "documented_future_work",
    "not_implemented_v1",
]

@dataclass(frozen=True)
class ExampleSpec:
    example_id: str
    title: str
    source_equations: list[str]
    status: Status
    parameters: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class ExampleResult:
    object_id: str
    example_id: str
    statistic: str
    status: Status
    parameters: dict[str, Any] = field(default_factory=dict)
    critical_value: float | None = None
    null_probability: float | None = None
    alternative_probability: float | None = None
    paper_value: float | None = None
    paper_rounding_digits: int | None = None
    computed_value: float | None = None
    abs_error: float | None = None
    rounding_match: bool | None = None
    source_equations: list[str] = field(default_factory=list)
    description: str = ""

    def to_record(self) -> dict[str, Any]:
        record = {
            "object_id": self.object_id,
            "example_id": self.example_id,
            "statistic": self.statistic,
            "status": self.status,
            "critical_value": self.critical_value,
            "null_probability": self.null_probability,
            "alternative_probability": self.alternative_probability,
            "paper_value": self.paper_value,
            "paper_rounding_digits": self.paper_rounding_digits,
            "computed_value": self.computed_value,
            "abs_error": self.abs_error,
            "rounding_match": self.rounding_match,
            "source_equations": ";".join(self.source_equations),
            "description": self.description,
        }
        for key, value in self.parameters.items():
            record[key] = value
        return record

@dataclass(frozen=True)
class FigureResult:
    figure_id: str
    path: Path | None
    status: Status
    source_examples: list[str]
    source_equations: list[str]
    description: str = ""

    def to_record(self) -> dict[str, Any]:
        return {
            "figure_id": self.figure_id,
            "path": str(self.path) if self.path else None,
            "status": self.status,
            "source_examples": ";".join(self.source_examples),
            "source_equations": ";".join(self.source_equations),
            "description": self.description,
        }

@dataclass(frozen=True)
class ValidationResult:
    check_id: str
    passed: bool
    status: str
    message: str
    details: dict[str, Any] = field(default_factory=dict)

    def to_record(self) -> dict[str, Any]:
        return {
            "check_id": self.check_id,
            "passed": self.passed,
            "status": self.status,
            "message": self.message,
            "details": self.details,
        }
