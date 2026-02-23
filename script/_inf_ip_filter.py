import wmi
import psutil
import csv
from pathlib import Path
import xml.etree.ElementTree as ET

PATH_DATA = Path(__file__).resolve().parent.parent / "data"
PATH_DNS_MASTER = PATH_DATA / "dns-master.csv"
PATH_WHITE_MASTER = PATH_DATA / "ip-white-master.csv"
PATH_WHITE_EXCLUDE = PATH_DATA / "ip-white-exclude.csv"
PATH_WHITE_MANNUAL = PATH_DATA / "ip-white-mannual.csv"
# PATH_BLACK_MASTER = PATH_DATA / "ip-black-master.txt"
# PATH_BLACK_MANNUAL = PATH_DATA / "ip-black-mannual.txt"
XML_FILE = PATH_DATA / "profile.xml" 
GROUP_SIZE = 8
USER_ITEM_NAME = "white"

def create_simplewall_profile_white_list(white_master):

    # Step 1: Read IPs from white_master
    all_entries = sorted(white_master.keys())

    # Step 2: Load existing XML
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    # Step 3: Find or create <rules_custom>
    rules_custom = root.find("rules_custom")
    if rules_custom is None:
        rules_custom = ET.SubElement(root, "rules_custom")

    # Step 4: Remove old USER items
    for item in list(rules_custom.findall("item")):
        if item.attrib.get("name", "").startswith(f"{USER_ITEM_NAME}_"):
            rules_custom.remove(item)

    # Step 5: Add new items
    for i in range(0, len(all_entries), GROUP_SIZE):
        chunk = all_entries[i:i + GROUP_SIZE]
        
        # Format each entry in the chunk to include the port
        formatted_rule = ";".join([f"{entry}:443" for entry in chunk])
        
        ET.SubElement(
            rules_custom,
            "item",
            name=f"{USER_ITEM_NAME}_{i // GROUP_SIZE + 1}",
            rule=formatted_rule,
            protocol="6",
            # apps=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            apps=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            is_enabled="true"
        )

    # Step 6: Pretty print
    def indent(elem, level=0):
        i = "\n" + level * "    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            for child in elem:
                indent(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

    indent(root)

    # Step 7: Write file
    tree.write(XML_FILE, encoding="utf-8", xml_declaration=True)

    group_count = (len(all_entries) + GROUP_SIZE - 1) // GROUP_SIZE
    print(f"Success! {len(all_entries)} IPs → {group_count} rules")
    print(f"Output File: {XML_FILE}")

def update_white_master(dns_master):
    """
    Build ip-white-list-master.csv from:
      - dns-cache-master.csv (A records only)
      - minus ip-white-list-exclusion.csv
      - plus ip-white-list-mannual.csv (manual overrides)
    Output: [Reason, IP]
    """

    # Load unique exclude IPs
    excluded_ips = set()

    if PATH_WHITE_EXCLUDE.exists():
        with PATH_WHITE_EXCLUDE.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    excluded_ips.add(row[1].strip())

    # TODO: load exclude domains
    excluded_domains = set()

    # Build whitelist from DNS
    white_records = {}

    for row in dns_master:
        # TODO: is this check necessary? [Entry, Data] seems works as well?
        if len(row) < 4:
            continue

        entry, record_type, data, _ttl = row

        # Only A records
        if str(record_type) != "1":
            continue

        # exclude
        ip = data.strip()
        if ip in excluded_ips:
            continue
        # TODO:
        # if entry in excluded_domains:
        #     continue

        # Deduplicate by IP (first DNS reason wins for now)        
        if ip not in white_records:
            white_records[ip] = entry
        
        # TODO: Detect same IP reason
        # if ip in white_records:
        #     white_records[ip] == entry ? if not, why?

    # -----------------------------
    # 3. Merge manual whitelist (OVERRIDE)
    # -----------------------------
    if PATH_WHITE_MANNUAL.exists():
        with PATH_WHITE_MANNUAL.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    reason = row[0].strip()
                    ip = row[1].strip()

                    if ip in excluded_ips:
                        continue

                    # Manual always wins
                    white_records[ip] = reason

    # -----------------------------
    # 4. Write master whitelist
    # -----------------------------
    # TODO: create one if no existed file
    with PATH_WHITE_MASTER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Reason", "IP"])
        for ip, reason in sorted(white_records.items(), key=lambda x: x[0]):
            writer.writerow([reason, ip])

    print(f"White list entries: {len(white_records)}")
    print(f"Output File: {PATH_WHITE_MASTER}")
    print("----------------------------------------------------")

    return white_records
    
def update_dns_master():
    # Fetch current DNS Cache via WMI
    c = wmi.WMI(namespace="root\\StandardCimv2")
    dns_records = c.query("SELECT * FROM MSFT_DNSClientCache")
    
    # Use a Dictionary for Deduplication
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

    # Merge new data
    new_count = 0
    for record in dns_records:
        # TODO: fixed the problen when encounter numeric instead of alphabet, but still normalized
        # key = (record.Entry.lower(), record.Data.lower())
        key = (record.Entry, record.Data)
        if key not in master_records:
            new_count += 1
            print(f"{key}")
        
        # This will update the TTL to the most recent capture
        # TODO: maybe not necessary? only add new entry is enough?
        master_records[key] = [record.Entry, record.Type, record.Data, record.TimeToLive]

    # Sort by Entry name
    # sorted_rows = sorted(master_records.values(), key=lambda x: x[0].lower())
    # TODO: deal with numerical
    sorted_rows = sorted(master_records.values(), key=lambda x: x[0])

    # Write back to the same file
    with PATH_DNS_MASTER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Entry", "RecordType", "Data", "TimeToLive"])
        writer.writerows(sorted_rows)
            
    print(f"Added {new_count} new unique pairs. Total unique entries: {len(sorted_rows)}")
    print(f"Output File: {PATH_DNS_MASTER}")
    print("----------------------------------------------------")
    return sorted_rows

if __name__ == "__main__":
    # 1. update dns-master with current dns cache 
    dns_master = update_dns_master()

    # 2. (Optional)
    # Mannualy update ip-exclude.csv

    # 3. update ip-white-master with [dns-catch-master - ip-white-list-exclusion]
    # TODO: [dns-catch-master - ip-white-list-exclusion + ip-white-list-mannual]
    white_master = update_white_master(dns_master)

    # 4. recreate simplewall profile with ip-white-list-master
    create_simplewall_profile_white_list(white_master)

