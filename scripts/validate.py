from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from np1933.api import validate_all
from np1933.io import write_validation_summary


def main() -> None:
    results = validate_all()
    write_validation_summary(results)
    failed = [r for r in results if not r.passed]
    for result in results:
        prefix = "PASS" if result.passed else "FAIL"
        print(f"{prefix} {result.check_id}: {result.message}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
