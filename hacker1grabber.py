#!/usr/bin/env python3

import csv
import os
import sys
import glob

def extract_domains_from_csv(file_path):
    domains = set()
    
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = None
        for line in csvfile:
            if line.startswith('identifier'):
                reader = csv.DictReader([line] + csvfile.readlines())
                break
        
        if reader is None:
            return domains
            
        for row in reader:
            if row.get('eligible_for_submission', 'true').lower() == 'true':
                identifier = row['identifier'].strip()
                instruction = row.get('instruction', '').upper()
                if 'OUT OF SCOPE' not in instruction:
                    domains.add(identifier)
    
    return domains

def process_all_csvs(input_directory, output_file):
    all_domains = set()
    
    csv_pattern = os.path.join(input_directory, "*.csv")
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        print(f"No CSV files found in {input_directory}")
        return
    
    for csv_file in csv_files:
        print(f"Processing {os.path.basename(csv_file)}...")
        domains = extract_domains_from_csv(csv_file)
        all_domains.update(domains)
    
    with open(output_file, 'w') as f:
        for domain in sorted(all_domains):
            f.write(f"{domain}\n")
    
    print(f"Extracted {len(all_domains)} unique domains to {output_file}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 hacker1grabber.py <input_directory> <output_file>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_dir):
        print(f"Error: Directory '{input_dir}' does not exist")
        sys.exit(1)
    
    process_all_csvs(input_dir, output_file)

if __name__ == "__main__":
    main()