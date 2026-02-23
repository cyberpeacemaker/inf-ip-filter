
from update_dns_cache import dump_dns_sorted as update_dns
from record_ip import update_ip_log as record_ips
from group_ip_24 import main as group_ips
from create_simplewall_profile import main as create_xml
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
DNS_LOG_PATH = BASE "dns_cache_master.csv"
IP_RAW_PATH = BASE / "ip-black-list-master.txt"
# IP_GROUP_PATH = BASE / "block-ip-list-group-24.txt"
# MIN_IPS_FOR_CIDR = 4
XML_PATH = BASE / "profile.xml"
GROUP_SIZE = 8
USER_ITEM_NAME = "suspicious"

# 1. Update dns-cache-master
update_dns(log_path=DNS_LOG_PATH)

# 2. Update ip-black-list-master
record_ips(input_path=IP_RAW_PATH)
WHITELIST_CSV = BASE / "ip-white-list-raw.csv"
# Hardcoded excludes that don't necessarily need to be in the CSV
DEFAULT_EXCLUDE = {"0.0.0.0", "1.1.1.1", "8.8.8.8", "9.9.9.9", "127.0.0.1", "::1"}

# Run group_ip_24.py
# group_ips(input_path=IP_RAW_PATH, output_path=IP_GROUP_PATH, min_ips_for_cird_para=MIN_IPS_FOR_CIDR)

# Run create_simplewall_profile.py
create_xml(input_path=IP_RAW_PATH, xml_path=XML_PATH, group_size_para=GROUP_SIZE, user_item_name_para=USER_ITEM_NAME)
