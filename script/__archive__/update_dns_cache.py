import wmi
import csv
from pathlib import Path

# Setup paths
BASE = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE / "data"
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_FILE = OUTPUT_DIR / "dns_cache_master.csv"

def dump_dns_sorted(log_path=None):
    log_file = log_path or LOG_FILE

    # 1. Fetch current DNS Cache via WMI
    c = wmi.WMI(namespace="root\\StandardCimv2")
    dns_records = c.query("SELECT * FROM MSFT_DNSClientCache")
    
    # 2. Use a Dictionary for Deduplication
    # Key: (Entry, Data) -> Value: [Entry, Type, Data, TimeToLive]
    master_records = {}

    # Load existing data first (if file exists)
    if log_file.exists():
        with log_file.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 3:
                    # Create a unique key using (Entry, Data)
                    key = (row[0].lower(), row[2].lower())
                    master_records[key] = row

    # 3. Merge new data
    new_count = 0
    for record in dns_records:
        key = (record.Entry.lower(), record.Data.lower())
        if key not in master_records:
            new_count += 1
        
        # This will update the TTL to the most recent capture
        master_records[key] = [record.Entry, record.Type, record.Data, record.TimeToLive]

    # 4. Sort by Entry name
    sorted_rows = sorted(master_records.values(), key=lambda x: x[0].lower())

    # 5. Write back to the same file
    with log_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Entry", "RecordType", "Data", "TimeToLive"])
        writer.writerows(sorted_rows)
            
    print(f"Success! Output at: {log_file}")
    print(f"Added {new_count} new unique pairs. Total unique entries: {len(sorted_rows)}")

if __name__ == "__main__":
    dump_dns_sorted()