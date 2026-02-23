import wmi
import csv
from pathlib import Path

# Define your directory structure
BASE = Path(__file__).resolve().parent.parent
# If you want to save the CSV in the same base folder:
OUTPUT_DIR = BASE / "logs" 
OUTPUT_DIR.mkdir(exist_ok=True) # Ensure the directory exists

def get_unique_path(target_path: Path):
    if not target_path.exists():
        return target_path
    
    stem = target_path.stem
    suffix = target_path.suffix
    counter = 1
    
    while True:
        new_path = target_path.with_name(f"{stem}_{counter}{suffix}")
        if not new_path.exists():
            return new_path
        counter += 1

def dump_dns_wmi():
    # Setup WMI
    c = wmi.WMI(namespace="root\\StandardCimv2")
    dns_records = c.query("SELECT * FROM MSFT_DNSClientCache")
    
    # Define the starting file path
    base_file_path = OUTPUT_DIR / "dns_cache_dump.csv"
    final_path = get_unique_path(base_file_path)
    
    with final_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Entry", "RecordType", "Data", "TimeToLive"])
        
        for record in dns_records:
            writer.writerow([record.Entry, record.Type, record.Data, record.TimeToLive])
            
    print(f"Success! Data logged to: {final_path}")

if __name__ == "__main__":
    dump_dns_wmi()