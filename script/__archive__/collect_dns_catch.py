import csv
from pathlib import Path

# Setup paths
BASE = Path(__file__).resolve().parent.parent
LOG_DIR = BASE / "logs" / "rotate" / "2026-02-04"
MASTER_FILE = BASE / "logs" / "dns_cache_master.csv"

def consolidate_logs():
    all_data = set()  # Use a set to automatically handle duplicates
    
    # 1. Find all CSV files in the directory
    csv_files = list(LOG_DIR.glob("*.csv"))
    
    # Filter out the master file if it already exists to avoid recursive reading
    csv_files = [f for f in csv_files if f.name != MASTER_FILE.name]
    
    if not csv_files:
        print("No log files found to consolidate.")
        return

    print(f"Found {len(csv_files)} files. Processing...")

    # 2. Read every file
    for file_path in csv_files:
        with file_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None) # Skip header
            for row in reader:
                if row: # Ensure row isn't empty
                    all_data.add(tuple(row))

    # 3. Sort the combined data by 'Entry' (index 0)
    sorted_data = sorted(list(all_data), key=lambda x: x[0].lower())

    # 4. Write to the master file
    with MASTER_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Entry", "RecordType", "Data", "TimeToLive"])
        writer.writerows(sorted_data)

    print(f"Success! {len(sorted_data)} unique records consolidated into: {MASTER_FILE}")
    
    # Optional: Delete the old files after consolidation
    # for file_path in csv_files:
    #     file_path.unlink()

if __name__ == "__main__":
    consolidate_logs()