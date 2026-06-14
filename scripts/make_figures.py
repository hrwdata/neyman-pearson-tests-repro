from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from np1933.figures import generate_all_figures
from np1933.io import write_figure_inventory


def main() -> None:
    results = generate_all_figures()
    write_figure_inventory(results)
    generated = [r.figure_id for r in results if r.path is not None]
    print(f"generated figures: {', '.join(generated)}")


if __name__ == "__main__":
    main()
