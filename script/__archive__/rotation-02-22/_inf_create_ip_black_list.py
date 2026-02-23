import wmi
import psutil
import csv
from pathlib import Path

PATH_DATA = Path(__file__).resolve().parent.parent / "data"
PATH_DNS_MASTER = PATH_DATA / "dns-cache-master.csv"
PATH_WHITE_MASTER = PATH_DATA / "ip-white-list-master.csv"
PATH_WHITE_EXCLUSION = PATH_DATA / "ip-white-list-exclusion.csv"
PATH_BLACK_MASTER = PATH_DATA / "ip-black-list-master.txt"
PATH_BLACK_MANNUAL = PATH_DATA / "ip-black-list-mannual.txt"

# Hardcoded excludes that don't necessarily need to be in the CSV
DEFAULT_EXCLUDE = {"0.0.0.0", "1.1.1.1", "8.8.8.8", "9.9.9.9", "127.0.0.1", "::1"}

def update_dns_master():
    # 1. Fetch current DNS Cache via WMI
    c = wmi.WMI(namespace="root\\StandardCimv2")
    dns_records = c.query("SELECT * FROM MSFT_DNSClientCache")
    
    # 2. Use a Dictionary for Deduplication
    # Key: (Entry, Data) -> Value: [Entry, Type, Data, TimeToLive]
    master_records = {}

    # Load existing data first (if file exists)
    if PATH_DNS_MASTER.exists():
        with PATH_DNS_MASTER.open("r", newline="", encoding="utf-8") as f:
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
    with PATH_DNS_MASTER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Entry", "RecordType", "Data", "TimeToLive"])
        writer.writerows(sorted_rows)
            
    print(f"Added {new_count} new unique pairs. Total unique entries: {len(sorted_rows)}")
    print(f"Output File: {PATH_DNS_MASTER}")
    print("----------------------------------------------------")
    # TODO: return dns-master
    
def update_white_master(dns_master):
    # TODO
    # 1. add dns master into white-master
    # 2. subtract white-master with white-exclusion
    return white_master

def update_ip_log(input_path=None):
    PATH_BLACK_MASTER = input_path or PATH_BLACK_MASTER
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
    if PATH_BLACK_MASTER.exists():
        with open(PATH_BLACK_MASTER, "r") as f:
            existing_blacklist = set(line.strip() for line in f)

    # 3. Find only the NEW suspicious IPs
    new_ips = current_ips - existing_blacklist

    # # 4. Append only the new ones
    # if new_ips:
    #     with open(PATH_BLACK_MASTER, "a") as f:
    #         for ip in new_ips:
    #             f.write(f"{ip}\n")
    #             print(f">>> Added to Blacklist: {ip}")
    # else:
    #     print("\nNo new unknown IPs detected.")
    # print(f"Success! Output at: {PATH_BLACK_MASTER}")

if __name__ == "__main__":
    # 1. update dns-catch-master with current dns cache 
    dns_master = update_dns_master()

    # 2. update ip-white-list-master with [dns-catch-master - ip-white-list-exclusion]
    white_master = update_white_master(dns_master)

    # 3. update ip-black-list-master with [current established ip - ip-white-list-master] + ip-black-list-mannual
    black_master = update_black_master(white_master)

    # 4. recreate simplewall profile with ip-black-list-master
    create_simplewall_profile()