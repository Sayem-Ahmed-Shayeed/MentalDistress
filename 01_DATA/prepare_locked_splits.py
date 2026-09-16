#!/usr/bin/env python3
"""Regenerate and verify the exact MentalDistress locked split CSVs."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent
MASTER = ROOT / "MentalDistress.csv"
SPLIT_COLUMNS = ["original_row", "text", "label", "text_length"]
EXPECTED = {
    "master": (9935, "b189657dcdca2969bc5d158abf0d92b7d0155882ca50ca5ffc248e5b95afece9"),
    "train": (6954, "1bac0d2f4e0f4d3da940b08a21bd3c6e18b1d958c57cb263c89a900381572d5b"),
    "validation": (1490, "88835cd714b02efbd230536c7de3f455e807051a23a1786640b0e8b26b430165"),
    "test": (1491, "e3a61197d1d4a57e61269be260570cc5aa5b504275f0370b1c379f0453517270"),
}
EXPECTED_COUNTS = {
    "train": {"Suicidal": 1492, "Depressed": 1021, "Anxious": 1370, "Frustrated": 1292, "Others": 1779},
    "validation": {"Suicidal": 319, "Depressed": 219, "Anxious": 294, "Frustrated": 277, "Others": 381},
    "test": {"Suicidal": 320, "Depressed": 218, "Anxious": 294, "Frustrated": 277, "Others": 382},
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_path(name: str) -> Path:
    return ROOT / f"MentalDistress_{name}_LOCKED.csv"


def verify(path: Path, name: str, expected_rows: int, expected_hash: str) -> None:
    observed_hash = sha256(path)
    frame = pd.read_csv(path)
    if len(frame) != expected_rows:
        raise RuntimeError(f"{name}: expected {expected_rows} rows, found {len(frame)}")
    if observed_hash != expected_hash:
        raise RuntimeError(f"{name}: SHA-256 mismatch: {observed_hash}")
    print(f"PASS {name:10s} rows={len(frame):4d} sha256={observed_hash}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    verify(MASTER, "master", *EXPECTED["master"])
    master = pd.read_csv(MASTER)
    required = set(SPLIT_COLUMNS + ["locked_split"])
    if not required.issubset(master.columns):
        raise RuntimeError(f"Master dataset is missing columns: {sorted(required - set(master.columns))}")

    for name in ("train", "validation", "test"):
        target = split_path(name)
        selected = master.loc[master["locked_split"].eq(name), SPLIT_COLUMNS]
        if selected["label"].value_counts().to_dict() != EXPECTED_COUNTS[name]:
            raise RuntimeError(f"{name}: class-count mismatch")
        if not args.verify_only:
            selected.to_csv(target, index=False, lineterminator="\r\n")
        if not target.exists():
            raise FileNotFoundError(f"Missing {target}; run without --verify-only first")
        verify(target, name, *EXPECTED[name])


if __name__ == "__main__":
    main()
