import csv
from pathlib import Path

# Path configuration
PATH_DATA = Path(__file__).resolve().parent.parent / "data"
PATH_WHITE_MASTER = PATH_DATA / "ip-white-master.csv"

def extract_unique_domains(file_path: Path):
    """
    Reads the whitelist and extracts a sorted list of unique domains/reasons.
    """
    if not file_path.exists():
        print(f"Error: {file_path} not found.")
        return []

    unique_domains = set()

    try:
        with file_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            # Skip header "Reason,IP"
            next(reader, None)
            
            for row in reader:
                if len(row) >= 1:
                    domain = row[0].strip()
                    if domain:
                        unique_domains.add(domain)
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

    # Sort lexicographically
    sorted_domains = sorted(list(unique_domains))

    # Output results
    print(f"\nExtracted {len(sorted_domains)} unique domains from {file_path.name}:")
    print("-" * 40)
    for domain in sorted_domains:
        print(f"  • {domain}")
    
    return sorted_domains

if __name__ == "__main__":
    # TODO: path arg
    extract_unique_domains(PATH_WHITE_MASTER)