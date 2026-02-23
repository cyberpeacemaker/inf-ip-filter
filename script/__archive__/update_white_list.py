import socket
import csv
from pathlib import Path
from ipaddress import ip_address

BASE = Path(__file__).resolve().parent.parent

IP_DOMAIN_FILE = BASE / "ip-white-list-domain.csv"
IP_RAW_FILE = BASE / "ip-white-list-raw.csv"


def load_existing():
    """Load existing Reason,IP pairs"""
    existing = set()

    if not IP_RAW_FILE.exists():
        return existing

    with open(IP_RAW_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for reason, ip in reader:
            existing.add((reason, ip))

    return existing


def resolve_domains():
    """Resolve domains to Reason,IP pairs"""
    resolved = set()

    with open(IP_DOMAIN_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for domain, reason in reader:
            try:
                infos = socket.getaddrinfo(domain, 443, proto=socket.IPPROTO_TCP)
                ips = {info[4][0] for info in infos}

                for ip in ips:
                    resolved.add((reason, ip))
                    print(f"[+] Updated {reason}, {ip}")


            except socket.gaierror:
                print(f"[!] Could not resolve {domain}")

    return resolved


def sort_key(item):
    reason, ip = item
    return (reason.lower(), ip_address(ip))


def generate_whitelist():
    existing = load_existing()
    resolved = resolve_domains()

    combined = existing | resolved  # keep old + add new

    sorted_rows = sorted(combined, key=sort_key)

    with open(IP_RAW_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Reason", "IP"])
        writer.writerows(sorted_rows)

    print(f"[+] Updated {IP_RAW_FILE}")
    print(f"    Existing: {len(existing)}")
    print(f"    Resolved: {len(resolved)}")
    print(f"    Total:    {len(sorted_rows)}")


if __name__ == "__main__":
    generate_whitelist()
