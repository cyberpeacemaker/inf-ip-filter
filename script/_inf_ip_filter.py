import argparse
import wmi
import csv
import ipaddress
from pathlib import Path
import xml.etree.ElementTree as ET

# ── ANSI Colors ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

# ── Paths ────────────────────────────────────────────────────────────────────
PATH_DATA        = Path(__file__).resolve().parent.parent / "data"
PATH_DNS_MASTER  = PATH_DATA / "dns-master.csv"
PATH_WHITE_MASTER= PATH_DATA / "ip-white-master.csv"
PATH_WHITE_MANUAL= PATH_DATA / "ip-white-manual.csv"
PATH_BLACK_MANUAL= PATH_DATA / "ip-black-manual.csv"
PATH_BLACK_DOMAIN= PATH_DATA / "ip-black-domain.csv"
XML_FILE         = PATH_DATA / "profile.xml"

GROUP_SIZE     = 8
USER_ITEM_NAME = "white"
BLOCK_ITEM_NAME= "block"

# ── Helpers ───────────────────────────────────────────────────────────────────

def _prompt_ip(ip, entry) -> str:
    """Returns 'y', 'n', or 'b', or 'a'."""
    print(f"\n  {CYAN}{ip:<18}{RESET}  ←  {entry}")
    while True:
        # Added [a]ll to the prompt string
        choice = input("  Add to whitelist? [y]es / [n]o / [b]lock domain / yes to [a]ll: ").strip().lower()
        if choice in ("y", "n", "b", "a"):
            return choice
        
def _is_valid_ip(value: str) -> bool:
    """Return True if value is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def _sort_key_ip_or_domain(value: str):
    """
    Natural sort key that handles both IPs and domain strings.
    IPs sort numerically; domains sort lexicographically (lowercased).
    """
    try:
        return (0, int(ipaddress.ip_address(value)))
    except ValueError:
        return (1, value.lower())


def _indent(elem, level=0):
    """Pretty-print an ElementTree in-place."""
    pad = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = pad + "    "
        for child in elem:
            _indent(child, level + 1)
        # last child tail
        if not child.tail or not child.tail.strip():
            child.tail = pad
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = pad


# ── 1. update_dns_master ──────────────────────────────────────────────────────

def update_dns_master():
    """
    Fetch current Windows DNS client cache via WMI and merge it into
    dns-master.csv.  Records whose Data field is None are skipped.
    Keys are kept in their original case (no .lower()) to avoid
    clobbering mixed-case entries, but deduplication is case-insensitive.
    """
    PATH_DATA.mkdir(parents=True, exist_ok=True)

    # ── fetch live cache ──
    c = wmi.WMI(namespace="root\\StandardCimv2")
    dns_records = c.query("SELECT * FROM MSFT_DNSClientCache")

    # ── load existing master ──
    # Key: (entry_lower, data_lower)  →  row list
    master_records: dict[tuple, list] = {}

    if PATH_DNS_MASTER.exists():
        with PATH_DNS_MASTER.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    key = (row[0].lower(), row[2].lower())
                    master_records[key] = row

    # ── merge new records ──
    new_count = 0
    skipped_none = 0

    for record in dns_records:
        # Guard: some CNAME / SOA records have Data == None
        if record.Data is None:
            skipped_none += 1
            continue
        
        key = (record.Entry.lower(), record.Data.lower())

        if key not in master_records:
            new_count += 1
            print(f"  {GREEN}+{RESET} New: {record.Entry!r:40s}  →  {record.Data}")

            # No refresh TTL to the most recent snapshot
            # master_records[key] = [record.Entry, record.Type, record.Data, record.TimeToLive]
            master_records[key] = [record.Entry, record.Type, record.Data]

    # ── sort: domains lexicographically (case-insensitive), IPs numerically ──
    def _row_sort_key(row):
        return _sort_key_ip_or_domain(row[0])

    sorted_rows = sorted(master_records.values(), key=_row_sort_key)

    # ── write ──
    with PATH_DNS_MASTER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # writer.writerow(["Entry", "RecordType", "Data", "TimeToLive"])
        writer.writerow(["Entry", "RecordType", "Data"])
        writer.writerows(sorted_rows)

    print(f"\n{BOLD}DNS Master{RESET}: +{new_count} new  |  {skipped_none} skipped (None Data)"
          f"  |  {len(sorted_rows)} total")
    print(f"Output: {PATH_DNS_MASTER}")
    print("─" * 60)

    return sorted_rows


def update_white_master(dns_master, mode):
    """
    Build ip-white-master.csv by loading existing records first, 
    then merging new DNS A records and manual overrides.
    """
    PATH_DATA.mkdir(parents=True, exist_ok=True)

    # ── load existing whitelist (NEW) ──
    # This prevents re-prompting for IPs already processed in previous runs
    white_records: dict[str, str] = {}
    if PATH_WHITE_MASTER.exists():
        with PATH_WHITE_MASTER.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 2:
                    reason, ip = row[0].strip(), row[1].strip()
                    if ip:
                        white_records[ip] = reason

    # ── load black IPs and domains (Same as before) ──
    black_ips: set[str] = set()
    black_domains: set[str] = set()
    if PATH_BLACK_MANUAL.exists():
        with PATH_BLACK_MANUAL.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    ip = row[1].strip()
                    if ip:
                        black_ips.add(ip)
                    else:
                        domain = row[0].strip().lower()
                        if domain:
                            black_domains.add(domain)
                elif len(row) == 1:
                    domain = row[0].strip().lower()
                    if domain:
                        black_domains.add(domain)

    # ── build/update whitelist from DNS A records ──
    duplicate_log: list[tuple] = []
    yes_to_all = False 

    for row in dns_master:
        if len(row) < 3: # Changed to 3 based on your DNS writer logic
            continue

        entry, record_type, data = row[0], row[1], row[2]

        if str(record_type) != "1": # A records only
            continue

        ip = data.strip() if data else ""
        if not ip or not _is_valid_ip(ip):
            continue

        # Skip if already in blacklists
        if ip in black_ips or entry.lower() in black_domains:
            continue

        # Process if IP is NEW (not in loaded white_records)
        if ip not in white_records:
            if mode == "interactive" and not yes_to_all:
                choice = _prompt_ip(ip, entry)
                
                if choice == "y":
                    white_records[ip] = entry
                elif choice == "a":
                    white_records[ip] = entry
                    yes_to_all = True
                    print(f"  {GREEN}>>{RESET} Yes to all selected. Processing remaining entries...")
                elif choice == "b":
                    black_domains.add(entry.lower())
                    # TODO: Optionally: write to PATH_BLACK_MANUAL here
            else:
                # Add automatically if batch mode or yes_to_all is active
                white_records[ip] = entry
        else:
            # If IP exists but domain is different, log it for awareness
            if white_records[ip] != entry:
                duplicate_log.append((ip, white_records[ip], entry))

    # ── report same-IP / different-domain entries ──
    if duplicate_log:
        print(f"\n{YELLOW}⚠  Same IP → multiple domains:{RESET}")
        for ip, existing, new in duplicate_log:
            print(f"   {ip:<18}  kept={existing!r}  also={new!r}")

    # ── merge manual whitelist overrides ──
    if PATH_WHITE_MANUAL.exists():
        with PATH_WHITE_MANUAL.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) < 2: continue
                reason, ip = row[0].strip(), row[1].strip()
                if not ip or ip in black_ips or reason.lower() in black_domains:
                    continue
                white_records[ip] = reason

    # ── write combined master ──
    sorted_white = sorted(white_records.items(), key=lambda x: _sort_key_ip_or_domain(x[0]))
    with PATH_WHITE_MASTER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Reason", "IP"])
        writer.writerows([[reason, ip] for ip, reason in sorted_white])

    print(f"\n{BOLD}White Master{RESET}: {len(white_records)} entries"
          f"  |  {len(black_ips)} black IPs  |  {len(black_domains)} black domains")
    print(f"Output: {PATH_WHITE_MASTER}")
    print("─" * 60)

    return white_records


# ── 3. create_simplewall_profile ──────────────────────────────────────────────

def create_simplewall_profile(white_master: dict, black_master: dict | None = None,
                               pretty: bool = True):
    """
    (Re-)write the <rules_custom> section of profile.xml:
      • white_<n>  — ALLOW rules for whitelisted IPs (port 443, Chrome)
      • block_<n>  — BLOCK rules for blacklisted IPs  (all ports)

    Args:
        white_master: {ip: reason}
        black_master: {ip: reason} or None
        pretty:       indent XML output (default True, override via --no-pretty)
    """
    if not XML_FILE.exists():
        raise FileNotFoundError(f"profile.xml not found: {XML_FILE}")

    # ── deduplicate + sort IPs ──
    white_entries = sorted(set(white_master.keys()), key=_sort_key_ip_or_domain)
    black_entries = sorted(set(black_master.keys()), key=_sort_key_ip_or_domain) \
                   if black_master else []

    # ── parse XML ──
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    rules_custom = root.find("rules_custom")
    if rules_custom is None:
        rules_custom = ET.SubElement(root, "rules_custom")

    # Remove all previously generated items (white_* and block_*)
    for item in list(rules_custom.findall("item")):
        name = item.attrib.get("name", "")
        if name.startswith(f"{USER_ITEM_NAME}_") or name.startswith(f"{BLOCK_ITEM_NAME}_"):
            rules_custom.remove(item)

    # ── add ALLOW rules ──
    for i in range(0, len(white_entries), GROUP_SIZE):
        chunk = white_entries[i:i + GROUP_SIZE]
        rule  = ";".join(f"{ip}:443" for ip in chunk)

        item = ET.SubElement(
            rules_custom, "item",
            name=f"{USER_ITEM_NAME}_{i // GROUP_SIZE + 1}",
            rule=rule,
            protocol="6",
            apps=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            is_enabled="true",
        )
        # Add a trailing newline after each item for readability in raw XML
        item.tail = "\n"

    # ── add BLOCK rules ──
    for i in range(0, len(black_entries), GROUP_SIZE):
        chunk = black_entries[i:i + GROUP_SIZE]
        rule  = ";".join(chunk)           # no port restriction — block all

        item = ET.SubElement(
            rules_custom, "item",
            name=f"{BLOCK_ITEM_NAME}_{i // GROUP_SIZE + 1}",
            rule=rule,
            is_block="true",
            is_enabled="true",
        )
        item.tail = "\n"

    # ── pretty-print ──
    if pretty:
        _indent(root)

    # ── write ──
    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

    w_groups = (len(white_entries) + GROUP_SIZE - 1) // GROUP_SIZE
    b_groups = (len(black_entries) + GROUP_SIZE - 1) // GROUP_SIZE

    print(f"\n{BOLD}{GREEN}✓ Simplewall profile updated{RESET}")
    print(f"  ALLOW: {len(white_entries)} IPs  →  {w_groups} rules  ({USER_ITEM_NAME}_*)")
    if black_entries:
        print(f"  BLOCK: {len(black_entries)} IPs  →  {b_groups} rules  ({BLOCK_ITEM_NAME}_*)")
    print(f"Output: {XML_FILE}")
    print("─" * 60)


# ── 4. load_black_master (helper) ─────────────────────────────────────────────

def load_black_master() -> dict[str, str]:
    """Return {ip: reason} for all entries in ip-black-manual.csv."""
    result: dict[str, str] = {}
    if PATH_BLACK_MANUAL.exists():
        with PATH_BLACK_MANUAL.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2 and row[1].strip():
                    ip     = row[1].strip()
                    reason = row[0].strip()
                    result[ip] = reason
    return result


# ── CLI entry-point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="IP filter pipeline: DNS → whitelist → Simplewall profile"
    )
    parser.add_argument(
        "--no-pretty", action="store_true",
        help="Skip XML indentation (faster write)"
    )
    parser.add_argument(
        "--skip-dns", action="store_true",
        help="Skip DNS cache update (use existing dns-master.csv)"
    )
    parser.add_argument(
        "--mode", choices=["batch", "interactive"], default="batch",
        help="Set to 'interactive' to prompt for new IP addresses"
    )    
    args = parser.parse_args()

    # 1. Update dns-master with current DNS cache
    if args.skip_dns:
        print(f"{YELLOW}Skipping DNS update — loading existing {PATH_DNS_MASTER.name}{RESET}")
        dns_master = []
        if PATH_DNS_MASTER.exists():
            with PATH_DNS_MASTER.open("r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                dns_master = list(reader)
    else:
        dns_master = update_dns_master()

    # 2. (Optional) Manually edit ip-black-manual.csv / ip-white-manual.csv

    # 3. Build ip-white-master
    white_master = update_white_master(dns_master, args.mode)

    # 4. Load black master (for block rules in profile)
    black_master = load_black_master()

    # 5. Recreate Simplewall profile
    # create_simplewall_profile(
    #     white_master,
    #     black_master=black_master,
    #     pretty=not args.no_pretty,
    # )