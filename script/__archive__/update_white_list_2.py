import csv
from pathlib import Path

# Your current list
raw_whitelist = """
142.250.196.206, "Gemini or Google"
142.250.66.78, "Gemini or Google"
142.250.204.46, "Gemini or Google"
142.250.198.69, "Gemini or Google"
142.250.196.202, "Gemini or Google"
142.250.196.196, "Gemini or Google"
142.250.196.206, "Gemini or Google"
142.250.66.78, "Gemini or Google"
142.250.204.36, "Gemini or Google"
142.250.204.37, "Gemini or Google"
34.54.88.138, "Virsutotal"
172.67.70.74, "abuseip"
104.26.12.38, "abuseip"
"""

BASE = Path(__file__).resolve().parent.parent
WHITELIST_CSV = BASE / "logs" / "whitelist.csv"

def reverse_whitelist():
    lines = raw_whitelist.strip().split('\n')
    unique_entries = set()

    for line in lines:
        # Split by comma and clean up whitespace/quotes
        parts = [p.strip().replace('"', '') for p in line.split(',')]
        
        if len(parts) == 2:
            ip, reason = parts[0], parts[1]
            # Store as (Reason, IP) tuple for deduplication
            unique_entries.add((reason, ip))

    # Sort by Reason (index 0)
    sorted_entries = sorted(list(unique_entries), key=lambda x: x[0].lower())

    # Write to CSV
    WHITELIST_CSV.parent.mkdir(exist_ok=True)
    with WHITELIST_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Reason", "IP"])
        writer.writerows(sorted_entries)

    print(f"Done! Reversed and cleaned {len(sorted_entries)} unique entries.")
    print(f"File saved to: {WHITELIST_CSV}")

if __name__ == "__main__":
    reverse_whitelist()