from ipaddress import ip_address
import json
import csv
from pathlib import Path
import socket
from functools import lru_cache
from pathlib import Path

BASE = Path(__file__).resolve().parent / "data"
INPUT_FILE = "ip-block-list.md"

OUT_TXT = BASE / "block-ip-list.sorted.txt"
OUT_CSV = BASE / "block-ip-list.csv"
OUT_JSON_SIMPLE = BASE / "block-ip-list.json"
OUT_JSON_EXT = BASE / "block-ip-list.extended.json"

def read_ips(path):
    ips = set()
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            ips.add(ip_address(line))
        except ValueError:
            print(f"Skipping invalid IP: {line}")
    return sorted(ips)

@lru_cache(maxsize=1024)
def reverse_resolve(ip, timeout=1):
    try:
        socket.setdefaulttimeout(timeout)
        return socket.gethostbyaddr(str(ip))[0]
    except Exception:
        return None

def write_txt(ips, path):
    Path(path).write_text("\n".join(str(ip) for ip in ips) + "\n")


def write_csv(ips, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ip"])
        for ip in ips:
            writer.writerow([str(ip)])


def write_json_simple(ips, path):
    data = [str(ip) for ip in ips]
    Path(path).write_text(json.dumps(data, indent=2) + "\n")


def write_json_extended(ips, path, resolve_dns=False):
    data = {
        "blocklist": [
            {
                "ip": str(ip),
                "hostname": reverse_resolve(ip) if resolve_dns else None,
                "reason": "",
                "added_at": ""
            }
            for ip in ips
        ]
    }
    Path(path).write_text(json.dumps(data, indent=2) + "\n")


def main():
    ips = read_ips(INPUT_FILE)

    write_txt(ips, OUT_TXT)
    write_csv(ips, OUT_CSV)
    write_json_simple(ips, OUT_JSON_SIMPLE)
    write_json_extended(ips, OUT_JSON_EXT)

    print(f"Processed {len(ips)} unique IPs")
    print("Generated:")
    print(f" - {OUT_TXT}")
    print(f" - {OUT_CSV}")
    print(f" - {OUT_JSON_SIMPLE}")
    print(f" - {OUT_JSON_EXT}")


if __name__ == "__main__":
    main()
