from __future__ import annotations

from pathlib import Path

from np1933.api import generate_figure
from np1933.examples_geometry import example4_geometry, example5_geometry, example6_geometry


def test_rectangular_geometry_area_relationships():
    ex4 = example4_geometry(epsilon=0.10, b0=1.0, shift=0.25)
    assert abs(ex4["common_area"] - 0.5625) < 1e-12
    assert abs(ex4["critical_piece_area"] - 0.10) < 1e-12

    ex5 = example5_geometry(epsilon=0.10, b0=1.0)
    assert abs(ex5["central_area"] - ex5["target_area"]) < 1e-12

    ex6 = example6_geometry(epsilon=0.10, b0=1.0)
    assert abs(ex6["band_area"] - ex6["target_area"]) < 1e-12


def test_implemented_figures_generate_files():
    for figure_id in ["fig04", "fig05", "fig07", "fig08", "fig10"]:
        result = generate_figure(figure_id)
        assert result.path is not None
        assert Path(result.path).exists()
        assert result.status == "schematic_geometry"


def test_deferred_figures_return_metadata_only():
    result = generate_figure("fig01")
    assert result.path is None
    assert result.status == "documented_future_work"
