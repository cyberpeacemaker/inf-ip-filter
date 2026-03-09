import csv
import ipaddress
import argparse
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
PATH_DATA         = Path(__file__).resolve().parent.parent / "data"
PATH_WHITE_MANUAL = PATH_DATA / "ip-white-manual.csv"
PATH_BLACK_MANUAL = PATH_DATA / "ip-black-manual.csv"
PATH_BLACK_DOMAIN = PATH_DATA / "ip-black-domain.csv"

def _sort_key(row, col_index=0):
    """
    Sort logic:
    1. Attempts to sort numerically if the target column is a valid IP address.
    2. Falls back to case-insensitive lexicographical sorting.
    """
    if col_index < len(row):
        val = row[col_index].strip()
        try:
            # Try numeric IP sorting first
            return (0, int(ipaddress.ip_address(val)))
        except ValueError:
            # Fallback to string sorting (Domains or Reasons)
            return (1, val.lower())
    return (2, "")

def process_file(file_path, sort_col=0):
    """Reads, sorts by specified column index, and overwrites the CSV."""
    if not file_path.exists():
        print(f"Skipping: {file_path.name} (not found)")
        return

    with file_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = [r for r in reader if any(field.strip() for field in r)]

    # Sort using the provided integer index
    rows.sort(key=lambda r: _sort_key(r, col_index=sort_col))

    with file_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        writer.writerows(rows)
    print(f"  [✓] Sorted {file_path.name} by Column {sort_col + 1}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sort manual IP/Domain configuration files."
    )
    parser.add_argument(
        "--col", choices=["1", "2"], default="1",
        help="Sort by column 1 (Reason/Domain) or column 2 (IP/Domain)"
    )    
    args = parser.parse_args()    

    # Convert the string choice ("1" or "2") to a 0-based integer index (0 or 1)
    # This solves the "string not compatible with integrity" (index) issue
    selected_index = int(args.col) - 1

    print(f"Sorting files by column {args.col}...")
    
    files_to_process = [PATH_WHITE_MANUAL, PATH_BLACK_MANUAL, PATH_BLACK_DOMAIN]
    
    for p in files_to_process:
        process_file(p, sort_col=selected_index)