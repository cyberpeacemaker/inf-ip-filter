import csv
import psutil
from pathlib import Path

# --- Configuration ---
BASE = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE / "logs" 
OUTPUT_DIR.mkdir(exist_ok=True)

def get_unique_path(target_path: Path):
    if not target_path.exists():
        return target_path
    stem, suffix = target_path.stem, target_path.suffix
    counter = 1
    while True:
        new_path = target_path.with_name(f"{stem}_{counter}{suffix}")
        if not new_path.exists():
            return new_path
        counter += 1

def dump_tcp_connections():
    base_file_path = OUTPUT_DIR / "tcp_connections.csv"
    final_path = get_unique_path(base_file_path)
    
    # Header for both Console and CSV
    headers = ["Process", "RemoteAddress", "RemotePort", "Status"]
    
    connections_to_log = []

    # Iterate through current TCP connections
    for conn in psutil.net_connections(kind='tcp'):
        # Filter: Must have a remote address and not be 'listening' on all interfaces
        if conn.raddr and conn.raddr.ip not in ("0.0.0.0", "::"):
            try:
                process_name = psutil.Process(conn.pid).name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "Unknown"

            row = [process_name, conn.raddr.ip, conn.raddr.port, conn.status]
            connections_to_log.append(row)
            
            # Print to screen in real-time
            print(f"{process_name:<20} | {conn.raddr.ip:<15} | {conn.status}")

    # Write to CSV
    # with final_path.open("w", newline="", encoding="utf-8") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(headers)
    #     writer.writerows(connections_to_log)
            
    print(f"\n[+] TCP Data logged to: {final_path}")

if __name__ == "__main__":
    # You can call your DNS dump here too if you want both
    # dump_dns_wmi() 
    dump_tcp_connections()