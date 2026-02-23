from ipaddress import ip_address, IPv4Network
from collections import defaultdict
from pathlib import Path
import ipaddress

BASE = Path(__file__).resolve().parent / "output"

INPUT_FILE = "block-ip-list.raw"
OUTPUT_FILE = BASE / "block-ip-list.grouped-24"

def read_ips(path):
    ips = set()
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        ips.add(ip_address(line))
    return sorted(ips)

def summarize_blocklist(ip_sort):
# 1. Convert strings to IP Network objects
    # We use ip_network(..., strict=False) to handle single IPs and CIDRs
    networks = []
    for ip in ip_sort:
        networks.append(ipaddress.ip_network(ip, strict=False))    
    # 2. Collapse the addresses
    # This automatically detects if it can merge /24 into /23, /22, etc.
    collapsed = list(ipaddress.collapse_addresses(networks))

    return collapsed


def main():
    ips = read_ips(INPUT_FILE)
    grouped = summarize_blocklist(ips)

    Path(OUTPUT_FILE).write_text("\n".join(str(net) for net in grouped) + "\n")

    print(f"Input IPs     : {len(ips)}")
    print(f"Output entries: {len(grouped)}")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
