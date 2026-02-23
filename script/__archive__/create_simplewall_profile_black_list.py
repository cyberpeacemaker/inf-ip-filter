from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent.parent / "output"

INPUT_FILE = BASE / "block-ip-list-group-24.txt"       # your raw IP list
XML_FILE = BASE / "profile-out.xml"  # the existing XML file
GROUP_SIZE = 8
USER_ITEM_NAME = "suspicious"

def main(input_path=None, xml_path=None, group_size_para=None, user_item_name_para=None):
    input_file = input_path or INPUT_FILE
    xml_file = xml_path or XML_FILE
    gruop_size = group_size_para or GROUP_SIZE 
    user_item_name = user_item_name_para or USER_ITEM_NAME

    # Step 1: Read IPs/CIDRs
    all_entries = []
    for line in Path(input_file).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        all_entries.append(line)

    # Step 2: Load existing XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Step 3: Find <rules_custom> element
    rules_custom = root.find("rules_custom")
    if rules_custom is None:
        # If it doesn't exist, create it
        rules_custom = ET.SubElement(root, "rules_custom")

    # Step 4: Remove all existing suspicious_* items
    for item in list(rules_custom.findall("item")):
        if item.attrib.get("name", "").startswith(f"{user_item_name}_"):
            rules_custom.remove(item)

    # Step 5: Add new items
    for i in range(0, len(all_entries), gruop_size):
        chunk = all_entries[i:i+gruop_size]
        item_name = f"{user_item_name}_{i // gruop_size + 1}"
        ip_list = ";".join(chunk)
        ET.SubElement(
            rules_custom,
            "item",
            name=item_name,
            rule=ip_list,
            is_block="true",
            is_enabled="true"
        )

    # Step 6: Pretty-print helper
    def indent(elem, level=0):
        i = "\n" + level*"    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            for child in elem:
                indent(child, level+1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

    indent(root)

    # Step 7: Write back to XML file
    tree.write(xml_file, encoding="utf-8", xml_declaration=True)

    print(f"Success! Output at: {xml_file}")
    print(f"Done! {len(all_entries)} IPs grouped into {len(all_entries)//gruop_size + (1 if len(all_entries)%gruop_size else 0)} new items.")


if __name__ == "__main__":
    main()