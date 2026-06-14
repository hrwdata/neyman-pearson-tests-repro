from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2, norm, t

from np1933.examples_geometry import example4_geometry, example6_geometry
from np1933.models import FigureResult

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "outputs" / "figures"

_IMPLEMENTED = {"fig04", "fig05", "fig07", "fig08", "fig10"}
_DEFERRED = {"fig01", "fig02", "fig03", "fig06", "fig09"}


def _save(fig, figure_id: str) -> Path:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = FIG_DIR / f"{figure_id}.png"
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_figure(figure_id: str) -> FigureResult:
    fid = figure_id.lower().replace("figure", "fig").replace(" ", "")
    if fid in _DEFERRED:
        return FigureResult(fid, None, "documented_future_work", [], [], "Not implemented in this release; listed for inventory completeness.")
    if fid not in _IMPLEMENTED:
        raise ValueError(f"Unknown figure_id {figure_id!r}.")
    if fid == "fig04":
        return _figure_04()
    if fid == "fig05":
        return _figure_05()
    if fid == "fig07":
        return _figure_07()
    if fid == "fig08":
        return _figure_08()
    if fid == "fig10":
        return _figure_10()
    raise AssertionError("unreachable")


def generate_all_figures() -> list[FigureResult]:
    return [generate_figure(fid) for fid in ["fig04", "fig05", "fig07", "fig08", "fig10", "fig01", "fig02", "fig03", "fig06", "fig09"]]


def _figure_04() -> FigureResult:
    x = np.linspace(-3, 3, 600)
    y = norm.pdf(x)
    z = norm.ppf(0.95)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.axvline(z, linestyle="--")
    ax.fill_between(x, 0, y, where=x >= z, alpha=0.25)
    ax.set_title("Figure 4 schematic: one-sided normal mean region")
    ax.set_xlabel("standardized sample mean")
    ax.set_ylabel("density")
    path = _save(fig, "fig04")
    return FigureResult("fig04", path, "schematic_geometry", ["ex01"], ["37", "38"], "Schematic figure; not a pixel-exact reproduction.")


def _figure_05() -> FigureResult:
    x = np.linspace(0, 25, 600)
    fig, ax = plt.subplots()
    ax.plot(x, chi2.pdf(x, 5), label="df=5 known mean")
    ax.plot(x, chi2.pdf(x, 4), label="df=4 sample variance")
    ax.axvline(chi2.ppf(0.99, 5), linestyle="--")
    ax.axvline(chi2.ppf(0.99, 4), linestyle=":")
    ax.set_title("Figure 5 schematic: chi-square critical values")
    ax.set_xlabel("chi-square statistic")
    ax.set_ylabel("density")
    ax.legend()
    path = _save(fig, "fig05")
    return FigureResult("fig05", path, "schematic_geometry", ["ex02"], ["46", "48", "50", "51"], "Schematic density comparison.")


def _draw_square(ax, center, side, **kwargs):
    cx, cy = center
    h = side / 2
    xs = [cx - h, cx + h, cx + h, cx - h, cx - h]
    ys = [cy - h, cy - h, cy + h, cy + h, cy - h]
    ax.plot(xs, ys, **kwargs)


def _figure_07() -> FigureResult:
    vals = example4_geometry()
    fig, ax = plt.subplots()
    _draw_square(ax, (0, 0), 1.0, label="W0")
    _draw_square(ax, (0.25, 0.25), 1.0, linestyle="--", label="W1")
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Figure 7 schematic: overlapping rectangular sample spaces")
    ax.legend()
    ax.text(-0.45, -0.6, f"common area={vals['common_area']:.3f}")
    path = _save(fig, "fig07")
    return FigureResult("fig07", path, "schematic_geometry", ["ex04"], ["63", "64"], "Schematic overlap geometry.")


def _figure_08() -> FigureResult:
    vals = example6_geometry()
    l0 = vals["range_threshold"]
    fig, ax = plt.subplots()
    _draw_square(ax, (0, 0), 1.0, label="W0")
    xs = np.linspace(-0.5, 0.5, 300)
    ax.fill_between(xs, xs - l0, xs + l0, alpha=0.25, label="|x-y| < l0")
    ax.set_xlim(-0.55, 0.55)
    ax.set_ylim(-0.55, 0.55)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Figure 8 schematic: diagonal range band")
    ax.legend()
    path = _save(fig, "fig08")
    return FigureResult("fig08", path, "schematic_geometry", ["ex06"], ["63"], "Schematic range-based likelihood region.")


def _figure_10() -> FigureResult:
    df = 9
    eps = 0.05
    crit = t.ppf(1 - eps, df)
    x = np.linspace(-4, 4, 600)
    y = t.pdf(x, df)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.axvline(crit, linestyle="--")
    ax.fill_between(x, 0, y, where=x >= crit, alpha=0.25)
    ax.set_title("Figure 10 schematic: Student upper-tail cone/statistic")
    ax.set_xlabel("t statistic")
    ax.set_ylabel("density")
    path = _save(fig, "fig10")
    return FigureResult("fig10", path, "schematic_geometry", ["ex08"], ["117", "118", "119"], "Distributional schematic for the cone test.")
