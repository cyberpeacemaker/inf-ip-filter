import subprocess
import re
import csv
from pathlib import Path

# Configuration
PATH_DNS_MASTER = Path("dns_master.csv")

def update_dns_master_via_ipconfig():
    # 1. Run ipconfig /displaydns and capture output
    try:
        result = subprocess.run(["ipconfig", "/displaydns"], capture_output=True, text=True, check=True)
        raw_output = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running ipconfig: {e}")
        return

    # 2. Parse the output using Regex
    # This pattern captures the Record Name, Type, and the Data (Address)
    pattern = re.compile(
        r"Record Name\s+\.\s+\.\s+:\s+(?P<name>\S+).*?"
        r"Record Type\s+\.\s+\.\s+:\s+(?P<type>\d+).*?"
        r"(?:A \(Host\) Record\s+\.\s+:\s+|AAAA Record\s+\.\s+\.\s+:\s+|CNAME Record\s+\.\s+:\s+)(?P<data>\S+)",
        re.DOTALL
    )

    current_cache = []
    for match in pattern.finditer(raw_output):
        current_cache.append({
            "Entry": match.group("name"),
            "Type": match.group("type"),
            "Data": match.group("data")
        })

    # 3. Load existing master records for deduplication
    master_records = {}
    if PATH_DNS_MASTER.exists():
        with PATH_DNS_MASTER.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 3:
                    # KEY: (Entry, Type, Data) - Keeps A and AAAA records separate
                    key = (row[0].lower(), row[1], row[2].lower())
                    master_records[key] = row

    # 4. Merge New Data
    new_count = 0
    for record in current_cache:
        key = (record["Entry"].lower(), record["Type"], record["Data"].lower())
        if key not in master_records:
            new_count += 1
            master_records[key] = [record["Entry"], record["Type"], record["Data"]]

    # 5. Sort and Save
    sorted_rows = sorted(master_records.values(), key=lambda x: x[0].lower())
    
    with PATH_DNS_MASTER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Entry", "RecordType", "Data"])
        writer.writerows(sorted_rows)
        print(f"Add: {sorted_rows}")

    print(f"Success! Output at: {PATH_DNS_MASTER}. Added {new_count} new unique pairs. Total unique entries: {len(sorted_rows)}")

update_dns_master_via_ipconfig()