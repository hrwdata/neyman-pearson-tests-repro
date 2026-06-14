from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from np1933.api import run_all_examples
from np1933.io import write_example_tables


def main() -> None:
    results = run_all_examples()
    write_example_tables(results)
    print(f"wrote example tables for {len(results)} result rows")


if __name__ == "__main__":
    main()
