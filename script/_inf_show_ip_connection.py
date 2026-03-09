import psutil
import csv
import argparse
from pathlib import Path
from collections import defaultdict

# ── Paths ────────────────────────────────────────────────────────────────────
PATH_DATA         = Path(__file__).resolve().parent.parent / "data"
PATH_WHITE_MASTER = PATH_DATA / "ip-white-master.csv"
PATH_DNS_MASTER   = PATH_DATA / "dns-master.csv"

DEFAULT_EXCLUDE = {"0.0.0.0", "1.1.1.1", "8.8.8.8", "9.9.9.9", "127.0.0.1", "::1"}

def load_white_list():
    """Load IP -> Reason mapping from ip-white-master.csv."""
    ip_reason = {}
    if PATH_WHITE_MASTER.exists():
        with PATH_WHITE_MASTER.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ip_reason[row["IP"]] = row["Reason"]
    return ip_reason

def load_dns_master():
    """Load IP -> List of Domains mapping from dns-master.csv."""
    ip_to_domains = defaultdict(set)
    if PATH_DNS_MASTER.exists():
        with PATH_DNS_MASTER.open("r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header: Entry,RecordType,Data
            for row in reader:
                if len(row) >= 3 and row[1] == "1":  # Type 1 = A Record
                    domain, ip = row[0], row[2]
                    ip_to_domains[ip].add(domain)
    return {ip: ", ".join(sorted(domains)) for ip, domains in ip_to_domains.items()}

def show_established_connections(show_dns=False):
    ip_reason = load_white_list()
    ip_dns = load_dns_master() if show_dns else {}

    header = f"{'Reason':<25} | {'Remote IP':<15}"
    if show_dns:
        header += " | DNS Entry"
    
    print(header)
    print("-" * (len(header) + 10))

    for conn in psutil.net_connections(kind="tcp"):
        if conn.status != psutil.CONN_ESTABLISHED or not conn.raddr:
            continue
        
        ip = conn.raddr.ip
        if ip in DEFAULT_EXCLUDE:
            continue

        reason = ip_reason.get(ip, "-")
        dns_info = ip_dns.get(ip, "unknown") if show_dns else ""

        line = f"{reason:<25} | {ip:<15}"
        if show_dns:
            line += f" | {dns_info}"
        
        print(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lookup established TCP connections.")
    parser.add_argument(
        "--dns", action="store_true", 
        help="Also lookup domain names in dns-master.csv"
    )
    args = parser.parse_args()

    show_established_connections(show_dns=args.dns)