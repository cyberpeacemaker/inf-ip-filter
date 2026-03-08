import csv
import argparse
from pathlib import Path
from collections import defaultdict

# Default path configuration
PATH_DATA = Path(__file__).resolve().parent.parent / "data"
DEFAULT_DNS_MASTER = PATH_DATA / "dns-master.csv"

def analyze_ip_sharing(file_path: Path):
    """
    Scans a specified CSV to find IPs associated with multiple domains.
    Output: [IP, [NAME1, NAME2, ...]]
    """
    if not file_path.exists():
        print(f"Error: {file_path} not found.")
        return

    # Map IP -> Set of Domain Names
    ip_map = defaultdict(set)

    try:
        with file_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            # Skip header
            next(reader, None)
            
            for row in reader:
                # Basic validation for the expected 3-column format
                if len(row) < 3:
                    continue
                
                # strip() ensures data integrity for comparison
                domain = row[0].strip()
                record_type = row[1].strip()
                data = row[2].strip()

                # Focus only on A records (Type 1)
                if record_type == "1":
                    ip_map[data].add(domain)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Filter for IPs shared by more than one unique domain
    shared_ips = [[ip, sorted(list(domains))] for ip, domains in ip_map.items() if len(domains) > 1]
    shared_ips.sort()

    # Output results
    print(f"\nAnalyzing: {file_path.name}")
    print(f"{'IP Address':<18} | Associated Domains")
    print("-" * 60)
    for ip, names in shared_ips:
        print(f"{ip:<18} | {', '.join(names)}")
    
    print(f"\nTotal unique shared IPs found: {len(shared_ips)}")
    return shared_ips

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze DNS sharing by IP address.")
    
    # Add optional argument for the file path
    parser.add_argument(
        "--path", 
        nargs="?", 
        default=str(DEFAULT_DNS_MASTER),
        help="Path to the DNS master CSV file (default: data/dns-master.csv)"
    )
    
    args = parser.parse_args()
    target_path = Path(args.path)
    
    analyze_ip_sharing(target_path)