import psutil
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
INPUT_FILE = BASE / "ip-black-list-raw.txt"
WHITELIST_CSV = BASE / "ip-white-list-raw.csv"

# Hardcoded excludes that don't necessarily need to be in the CSV
DEFAULT_EXCLUDE = {"0.0.0.0", "1.1.1.1", "8.8.8.8", "9.9.9.9", "127.0.0.1", "::1"}

def load_whitelist_ips():
    """Reads the CSV and returns a set of IPs to ignore."""
    whitelist = set(DEFAULT_EXCLUDE)
    if WHITELIST_CSV.exists():
        try:
            with WHITELIST_CSV.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ip = row.get("IP", "").strip()
                    if ip:
                        whitelist.add(ip)
        except Exception as e:
            print(f"Error reading whitelist: {e}")
    return whitelist

def update_ip_log(input_path=None):
    input_file = input_path or INPUT_FILE
    whitelist = load_whitelist_ips()
    
    current_ips = set()
    print(f"{'Process':<20} | {'Remote Address':<15} | {'Status'}")
    print("-" * 50)

    # 1. Get current ESTABLISHED IPs
    for conn in psutil.net_connections(kind='tcp'):
        if conn.status == 'ESTABLISHED' and conn.raddr:
            try:
                process_name = psutil.Process(conn.pid).name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "Unknown"

            ip = conn.raddr.ip
            print(f"{process_name:<20} | {ip:<15} | {conn.status}")

            # Whitelist exclusion
            if ip not in whitelist:
                current_ips.add(ip)

    # 2. Read existing Blacklist to avoid duplicates
    existing_blacklist = set()
    if input_file.exists():
        with open(input_file, "r") as f:
            existing_blacklist = set(line.strip() for line in f)

    # 3. Find only the NEW suspicious IPs
    new_ips = current_ips - existing_blacklist

    # 4. Append only the new ones
    if new_ips:
        with open(input_file, "a") as f:
            for ip in new_ips:
                f.write(f"{ip}\n")
                print(f">>> Added to Blacklist: {ip}")
    else:
        print("\nNo new unknown IPs detected.")
    print(f"Success! Output at: {input_file}")

if __name__ == "__main__":
    update_ip_log()