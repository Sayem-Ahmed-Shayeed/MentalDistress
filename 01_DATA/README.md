# Internal data

`MentalDistress.csv` is the 9,935-row dataset used by the study. It contains `original_row`, `text`, `label`, `text_length`, and `locked_split`.

The three locked split files contain `original_row`, `text`, `label`, and `text_length`. They are deterministically exported with CRLF line endings because byte-level hashes depend on line-ending preservation.

Run `python prepare_locked_splits.py` to regenerate the split files, or add `--verify-only` to verify existing files without rewriting them.

Dataset record: https://doi.org/10.17632/twbypxgzym.1
