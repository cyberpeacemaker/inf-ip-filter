from ipaddress import ip_address, IPv4Network
from collections import defaultdict
from pathlib import Path
import ipaddress

BASE = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE / "block-ip-list-raw.txt"
OUTPUT_FILE = BASE / "output" / "block-ip-list-group-24.txt"
# OUTPUT_FILE_SORTED = BASE  / "block-ip-list-sorted.txt"

MIN_IPS_FOR_CIDR = 1  


def read_ips(path):
    ips = set()
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        ips.add(ip_address(line))
    return sorted(ips)


def group_by_24(ips, min_ips_for_cird):
    buckets = defaultdict(list)

    for ip in ips:
        net = IPv4Network(f"{ip}/24", strict=False)
        buckets[net].append(ip)

    result = []

    for net, members in buckets.items():
        if len(members) >= min_ips_for_cird:
            result.append(str(net.network_address) + "/24")
        else:
            result.extend(str(ip) for ip in members)

    return sorted(result, key=lambda x: (
        ip_address(x.split("/")[0])
    ))


def main(input_path=None, output_path=None, min_ips_for_cird_para=None):
    # Use provided paths or fall back to your BASE defaults
    input_file = input_path or INPUT_FILE
    output_file = output_path or OUTPUT_FILE
    min_ips_for_cird = min_ips_for_cird_para or MIN_IPS_FOR_CIDR 

    ips = read_ips(input_file)
    grouped = group_by_24(ips, min_ips_for_cird)

    Path(input_file).write_text("\n".join(str(ip) for ip in ips) + "\n")
    Path(output_file).write_text("\n".join(grouped) + "\n")

    print(f"Success! Output at: {output_file}")
    print(f"Input IPs     : {len(ips)}. Output entries: {len(grouped)}")

if __name__ == "__main__":
    main()
