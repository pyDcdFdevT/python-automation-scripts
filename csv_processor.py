"""
CSV Processor

What this script does:
1. Reads a CSV file.
2. Removes fully empty rows.
3. Calculates simple summary stats for numeric columns.
4. Saves a cleaned CSV and a summary TXT report.
"""

from __future__ import annotations

__version__ = "1.0.0"

import argparse
import csv
from pathlib import Path
import sys


def read_csv(file_path: Path) -> tuple[list[dict[str, str]], list[str]]:
    """Read CSV file and return rows + headers."""
    with file_path.open("r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)
        headers = list(reader.fieldnames or [])
    return rows, headers


def remove_empty_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Remove rows where all values are empty."""
    cleaned_rows = []
    for row in rows:
        values = [str(value).strip() for value in row.values()]
        if any(values):
            cleaned_rows.append(row)
    return cleaned_rows


def summarize_numeric_columns(
    rows: list[dict[str, str]], headers: list[str]
) -> dict[str, dict[str, int | float]]:
    """Build min/max/avg/count summary for numeric columns."""
    numbers_by_column: dict[str, list[float]] = {header: [] for header in headers}

    for row in rows:
        for header in headers:
            value = str(row.get(header, "")).strip()
            if not value:
                continue
            try:
                numbers_by_column[header].append(float(value))
            except ValueError:
                continue

    summary: dict[str, dict[str, float]] = {}
    for header, numbers in numbers_by_column.items():
        if not numbers:
            continue
        summary[header] = {
            "count": len(numbers),
            "min": min(numbers),
            "max": max(numbers),
            "avg": sum(numbers) / len(numbers),
        }
    return summary


def write_cleaned_csv(
    output_path: Path, headers: list[str], rows: list[dict[str, str]]
) -> None:
    """Write cleaned rows into a new CSV file."""
    with output_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def write_summary_report(
    report_path: Path, summary: dict[str, dict[str, int | float]], total_rows: int
) -> None:
    """Write a text report with summary statistics."""
    lines = [
        "CSV PROCESS REPORT",
        "===================",
        f"Total cleaned rows: {total_rows}",
        "",
    ]

    if not summary:
        lines.append("No numeric columns found.")
    else:
        lines.append("Numeric columns summary:")
        for column, stats in summary.items():
            lines.append(f"- {column}")
            lines.append(f"  count: {int(stats['count'])}")
            lines.append(f"  min:   {stats['min']:.2f}")
            lines.append(f"  max:   {stats['max']:.2f}")
            lines.append(f"  avg:   {stats['avg']:.2f}")
            lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def process_csv(input_file: Path, output_dir: Path) -> None:
    """Run the full CSV automation flow."""
    rows, headers = read_csv(input_file)
    cleaned_rows = remove_empty_rows(rows)
    summary = summarize_numeric_columns(cleaned_rows, headers)

    output_dir.mkdir(parents=True, exist_ok=True)
    cleaned_csv_path = output_dir / f"{input_file.stem}_cleaned.csv"
    report_path = output_dir / f"{input_file.stem}_summary.txt"

    write_cleaned_csv(cleaned_csv_path, headers, cleaned_rows)
    write_summary_report(report_path, summary, len(cleaned_rows))

    print("✔ Processing completed successfully")
    print(f"→ Cleaned CSV: {cleaned_csv_path}")
    print(f"→ Summary report: {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple CSV automation script.")
    parser.add_argument("input_csv", help="Path to the input CSV file.")
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory where processed files will be saved (default: output).",
    )
    return parser.parse_args()


# Entry point for CLI usage
def main() -> None:
    args = parse_args()
    input_path = Path(args.input_csv)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        print(f"Error: File not found -> {input_path}")
        sys.exit(1)
    if input_path.suffix.lower() != ".csv":
        print("Error: Input file must be a CSV.")
        sys.exit(1)

    process_csv(input_path, output_dir)


if __name__ == "__main__":
    main()
