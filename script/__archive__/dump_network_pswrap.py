import subprocess
import csv
import os
from datetime import datetime

def get_unique_filepath(base_path):
    if not os.path.exists(base_path):
        return base_path
    
    directory, filename = os.path.split(base_path)
    name, ext = os.path.splitext(filename)
    
    i = 1
    while True:
        new_path = os.path.join(directory, f"{name}_{i}{ext}")
        if not os.path.exists(new_path):
            return new_path
        i += 1

def dump_dns_to_csv():
    # We use PowerShell via Python to get the structured data objects
    cmd = ["powershell", "-Command", "Get-DnsClientCache | Select-Object Entry, RecordType, Data, TimeToLive | ConvertTo-Csv -NoTypeInformation"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        csv_data = result.stdout.strip().splitlines()
        
        output_file = get_unique_filepath(os.path.join(os.path.expanduser("~"), "dns_cache.csv"))
        
        with open(output_file, "w", newline="") as f:
            f.write("\n".join(csv_data))
            
        print(f"Success! DNS cache dumped to: {output_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error accessing DNS cache: {e}")

if __name__ == "__main__":
    dump_dns_to_csv()