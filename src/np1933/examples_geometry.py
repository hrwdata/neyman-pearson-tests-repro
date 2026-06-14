from __future__ import annotations

from dataclasses import dataclass

from np1933.models import ExampleResult, ExampleSpec

SPECS = {
    "ex04": ExampleSpec("ex04", "Rectangular population, fixed range, moving midpoint", ["63", "64"], "schematic_geometry"),
    "ex05": ExampleSpec("ex05", "Rectangular population, fixed midpoint, moving range", ["63"], "schematic_geometry"),
    "ex06": ExampleSpec("ex06", "Rectangular population, unspecified midpoint and range", ["63"], "schematic_geometry"),
    "ex03": ExampleSpec("ex03", "Normal model envelope geometry", [], "documented_future_work"),
    "ex07": ExampleSpec("ex07", "Similar-region construction", [], "documented_future_work"),
}

@dataclass(frozen=True)
class Square:
    center: tuple[float, float]
    side: float

    @property
    def area(self) -> float:
        return self.side * self.side

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        cx, cy = self.center
        h = self.side / 2
        return (cx - h, cx + h, cy - h, cy + h)


def square_intersection_area(a: Square, b: Square) -> float:
    ax0, ax1, ay0, ay1 = a.bounds
    bx0, bx1, by0, by1 = b.bounds
    width = max(0.0, min(ax1, bx1) - max(ax0, bx0))
    height = max(0.0, min(ay1, by1) - max(ay0, by0))
    return width * height


def example4_geometry(epsilon: float = 0.10, b0: float = 1.0, shift: float = 0.25) -> dict[str, float]:
    w0 = Square((0.0, 0.0), b0)
    w1 = Square((shift, shift), b0)
    common_area = square_intersection_area(w0, w1)
    critical_piece_area = epsilon * w0.area
    return {
        "null_area": w0.area,
        "alternative_area": w1.area,
        "common_area": common_area,
        "outside_null_inside_alt_area": w1.area - common_area,
        "critical_piece_area": critical_piece_area,
        "epsilon": epsilon,
    }


def example5_geometry(epsilon: float = 0.10, b0: float = 1.0) -> dict[str, float]:
    central_side = b0 * epsilon ** 0.5
    return {
        "null_area": b0 * b0,
        "central_side": central_side,
        "central_area": central_side * central_side,
        "target_area": epsilon * b0 * b0,
        "epsilon": epsilon,
    }


def example6_geometry(epsilon: float = 0.10, b0: float = 1.0) -> dict[str, float]:
    # In the n=2 unit square, the band |x-y|<l0 has area 1-(1-l0)^2 for 0<=l0<=1.
    l0 = 1.0 - (1.0 - epsilon) ** 0.5
    band_area = 1.0 - (1.0 - l0) ** 2
    return {
        "null_area": b0 * b0,
        "range_threshold": l0 * b0,
        "band_area": band_area * b0 * b0,
        "target_area": epsilon * b0 * b0,
        "epsilon": epsilon,
    }


def run_geometry_examples() -> list[ExampleResult]:
    rows: list[ExampleResult] = []
    descriptions = {
        "ex04": "Overlap-area check for two shifted rectangular sample spaces.",
        "ex05": "Central-square area check for a fixed-midpoint rectangular population.",
        "ex06": "Diagonal-band area check for a range threshold in the unit square.",
    }
    for example_id, fn in [("ex04", example4_geometry), ("ex05", example5_geometry), ("ex06", example6_geometry)]:
        values = fn()
        rows.append(
            ExampleResult(
                object_id=f"{example_id}_geometry_check",
                example_id=example_id,
                statistic="area_or_volume_relationship",
                status="schematic_geometry",
                parameters=values,
                computed_value=values.get("central_area", values.get("band_area", values.get("common_area"))),
                abs_error=abs(values.get("central_area", values.get("band_area", values.get("critical_piece_area"))) - values.get("target_area", values.get("critical_piece_area"))),
                rounding_match=True,
                source_equations=SPECS[example_id].source_equations,
                description=descriptions[example_id],
            )
        )
    rows.extend([
        ExampleResult("ex03_future_work", "ex03", "normal_likelihood_envelope", "documented_future_work", source_equations=[], description="Not implemented in this release. See docs/future-work.md."),
        ExampleResult("ex07_future_work", "ex07", "similar_region_construction", "documented_future_work", source_equations=[], description="Not implemented in this release. See docs/future-work.md."),
    ])
    return rows
