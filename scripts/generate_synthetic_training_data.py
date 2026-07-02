"""Generate synthetic training data for the Phase 4 prototype."""

from __future__ import annotations

import argparse

from floorplan_ai.models.dataset import SYNTHETIC_DATA_WARNING, generate_synthetic_training_rows, write_synthetic_training_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic revision-risk training data.")
    parser.add_argument("--output", required=True, help="Path to write CSV.")
    parser.add_argument("--count", type=int, default=160, help="Number of synthetic rows.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = write_synthetic_training_csv(generate_synthetic_training_rows(args.count, args.seed), args.output)
    print("Synthetic training data written to " + str(output))
    print(SYNTHETIC_DATA_WARNING)


if __name__ == "__main__":
    main()
