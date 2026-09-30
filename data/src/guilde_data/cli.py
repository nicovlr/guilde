"""CLI: write a reproducible fictional company JSON dump."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from guilde_data.generator import generate_company


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Generate fictional company data for GUILDE")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=Path, default=Path("data/output/company.json"))
    args = parser.parse_args(argv)

    company = generate_company(seed=args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(company.to_dict(), indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {args.out} (seed={args.seed})")


if __name__ == "__main__":
    main()
