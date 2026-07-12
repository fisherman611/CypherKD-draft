import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Merge all subset *_cyphers_result.json files in a directory"
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        type=Path,
        help="Directory containing subset result JSON files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output JSON path (default: <input-dir>/test_result.json)",
    )
    return parser.parse_args()


def read_records(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as fin:
        records = json.load(fin)
    if not isinstance(records, list):
        raise TypeError(f"Expected a JSON list in {path}, got {type(records).__name__}")
    return records


def main() -> None:
    args = parse_args()
    input_dir = args.input_dir.resolve()
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input directory does not exist: {input_dir}")

    input_files = sorted(input_dir.glob("*_cyphers_result.json"))
    if not input_files:
        raise FileNotFoundError(
            f"No *_cyphers_result.json files found in {input_dir}"
        )

    merged: list[dict[str, Any]] = []
    for path in input_files:
        records = read_records(path)
        merged.extend(records)
        print(f"Loaded {len(records):>5} records from {path.name}")

    output_path = (args.output or input_dir / "test_result.json").resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as fout:
        json.dump(merged, fout, ensure_ascii=False, indent=2)
        fout.write("\n")

    print(f"Merged {len(input_files)} files and {len(merged)} records into {output_path}")


if __name__ == "__main__":
    main()
