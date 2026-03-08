import csv
import argparse
from pathlib import Path

# Default path configuration
PATH_DATA = Path(__file__).resolve().parent.parent / "data"
PATH_ARCHIVE = PATH_DATA / "__archive__"
DEFAULT_OUTPUT = PATH_DATA / "dns-merged-master.csv"

def merge_dns_archives(archive_root: Path, output_file: Path):
    """
    Enumerates all subfolders in the archive, reads dns-master.csv files,
    and merges them into one file with an added 'Source' column.
    """
    if not archive_root.exists():
        print(f"Error: Archive path not found: {archive_root}")
        return

    merged_records = {} # Key: (Domain, Type, Data) to ensure uniqueness
    found_files = list(archive_root.rglob("dns-master.csv"))

    if not found_files:
        print("No dns-master.csv files found in the archive.")
        return

    print(f"Found {len(found_files)} archive files. Merging...")

    for file_path in found_files:
        # Get the folder name for the "Source" column
        source_folder = file_path.parent.name
        print(f"  [+] Reading: {file_path.relative_to(archive_root.parent)}")
        try:
            with file_path.open("r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None) # Skip individual headers
                
                for row in reader:
                    if len(row) < 3:
                        continue
                    
                    # Normalize data
                    entry = row[0].strip()
                    rtype = row[1].strip()
                    data = row[2].strip()
                    
                    # Use a tuple of the record itself as a key to deduplicate
                    # We store the source folder along with the record
                    record_key = (entry, rtype, data)
                    
                    if record_key not in merged_records:
                        merged_records[record_key] = source_folder
                    else:
                        # TODO
                        # Optional: If you want to track multiple sources for the same IP
                        existing_source = merged_records[record_key]
                        if source_folder not in existing_source:
                            merged_records[record_key] = f"{existing_source}; {source_folder}"

        except Exception as e:
            print(f"  [!] Failed to read {file_path}: {e}")

    # Write the merged results
    try:
        with output_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Entry", "RecordType", "Data", "SourceFolders"])
            
            # Sort by entry name for a clean output
            for (entry, rtype, data), sources in sorted(merged_records.items()):
                writer.writerow([entry, rtype, data, sources])
                
        print(f"\n{'-'*60}")
        print(f"Success! Merged {len(merged_records)} unique records.")
        print(f"Output saved to: {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge all archived dns-master.csv files.")
    parser.add_argument(
        "--input", 
        default=str(PATH_ARCHIVE),
        help="Root folder to search for archived CSVs"
    )
    parser.add_argument(
        "--output", 
        default=str(DEFAULT_OUTPUT),
        help="Path for the final merged CSV"
    )

    args = parser.parse_args()
    merge_dns_archives(Path(args.input), Path(args.output))