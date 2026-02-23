from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

BLACK_LIST_FILE = BASE / "ip-black-list-raw.txt"      
WHITE_LIST_FILE = BASE / "ip-white-list-raw.csv" 

def main(black_path=None, white_path=None):
    black_list_file = black_path or BLACK_LIST_FILE
    white_list_file = white_path or WHITE_LIST_FILE

    # Read whitelist IPs (second column after comma)
    white_ips = set()

    with open(white_list_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 2:
                white_ips.add(parts[1].strip())

    # Read blacklist IPs
    black_ips = []

    with open(black_list_file, "r") as f:
        for line in f:
            ip = line.strip()
            if ip:
                black_ips.append(ip)

    # Subtract whitelist IPs from blacklist
    filtered_black_ips = []
    removed_ips = []

    for ip in black_ips:
        if ip in white_ips:
            removed_ips.append(ip)
        else:
            filtered_black_ips.append(ip)

    # Write back to blacklist file
    with open(black_list_file, "w") as f:
        for ip in filtered_black_ips:
            f.write(ip + "\n")

    # Print removed IPs
    if removed_ips:
        for ip in removed_ips:
            print(f"Remove {ip} from black list")
    else:
        print("No IPs were removed from the blacklist.")

    print("Blacklist updated successfully.")

if __name__ == "__main__":
    main()