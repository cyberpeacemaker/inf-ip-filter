import csv
import argparse
import shutil
import datetime
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
PATH_DATA         = Path(__file__).resolve().parent.parent / "data"
PATH_DNS_MASTER   = PATH_DATA / "dns-master.csv"
PATH_WHITE_MASTER = PATH_DATA / "ip-white-master.csv"
PATH_ARCHIVE_ROOT = PATH_DATA / "__archive__"

# ── Configuration ────────────────────────────────────────────────────────────
HEADERS = {
    PATH_DNS_MASTER: ["Entry", "RecordType", "Data"],
    PATH_WHITE_MASTER: ["Reason", "IP"]
}

def refresh_data(archive_tag=None):
    """
    If archive_tag is provided, moves master files to a new rotation folder.
    Then resets both master files to contain only their headers.
    """
    # 1. Archiving Logic
    if archive_tag:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        rotation_folder = PATH_ARCHIVE_ROOT / f"rotation-{timestamp}-{archive_tag}"
        rotation_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"Archiving to: {rotation_folder.name}")
        
        for file_path in [PATH_DNS_MASTER, PATH_WHITE_MASTER]:
            if file_path.exists():
                dest = rotation_folder / file_path.name
                shutil.copy2(file_path, dest) # copy2 preserves metadata
                print(f"  [archive] {file_path.name} -> {rotation_folder.name}")
            else:
                print(f"  [!] Skip archive: {file_path.name} (not found)")

    # 2. Refresh/Clean Logic
    print("\nRefreshing master files...")
    for file_path, header in HEADERS.items():
        try:
            # This 'w' mode truncates the file, effectively cleaning it
            with file_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(header)
            print(f"  [cleaned] {file_path.name} (header only)")
        except Exception as e:
            print(f"  [!] Error cleaning {file_path.name}: {e}")

    print("\nRefresh complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refresh and optionally archive DNS and Whitelist master files.")
    
    parser.add_argument(
        "--archive", 
        metavar="TAG",
        help="Archive current data into __archive__/rotation-timestamp-TAG/ before cleaning."
    )
    
    args = parser.parse_args()
    
    # Simple confirmation if cleaning without archiving
    if not args.archive:
        confirm = input("No archive tag provided. This will DELETE current master data. Proceed? [y/N]: ").strip().lower()
        if confirm != 'y':
            print("Operation cancelled.")
            exit()

    refresh_data(archive_tag=args.archive)