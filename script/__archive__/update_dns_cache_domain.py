import wmi
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LOG_FILE = BASE / "logs" / "dns_map.csv"
LOG_FILE.parent.mkdir(exist_ok=True)

def dump_minimal_dns(log_path=None):
    log_file = log_path or LOG_FILE
    # 1. Fetch current DNS Cache
    c = wmi.WMI(namespace="root\\StandardCimv2")
    dns_records = c.query("SELECT * FROM MSFT_DNSClientCache")
    
    # 2. Load existing mapping (Domain -> IP)
    dns_map = {}
    if LOG_FILE.exists():
        with LOG_FILE.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            # Create dict: { 'google.com': '142.250.1.1' }
            dns_map = {row[0].lower(): row[1] for row in reader if len(row) == 2}

    # 3. Update with new records
    initial_count = len(dns_map)
    for record in dns_records:
        # We use .lower() on the entry to keep it clean
        # This will overwrite old IPs with new ones if they changed
        dns_map[record.Entry.lower()] = record.Data

    # 4. Sort alphabetically by Domain Name
    sorted_entries = sorted(dns_map.items())

    # 5. Write Lean CSV
    with LOG_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Entry", "Data"]) 
        writer.writerows(sorted_entries)

    print(f"Success! Updated and sorted log at: {log_file}")        
    print(f"Success! {len(dns_map)} unique mappings saved.")
    print(f"Discovered {len(dns_map) - initial_count} new domains.")

if __name__ == "__main__":
    dump_minimal_dns()