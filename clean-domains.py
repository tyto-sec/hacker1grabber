#!/usr/bin/env python3

import re
import sys
import os

def is_valid_ip(address):
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ip_pattern, address):
        parts = address.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False

def is_valid_domain(domain):
    if not domain or '.' not in domain:
        return False
    domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-\.]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
    if not re.match(domain_pattern, domain):
        return False
    parts = domain.split('.')
    if all(part.isdigit() for part in parts):
        return False
    
    return True

def clean_domain(domain):
    domain = domain.strip()
    domain = re.sub(r'^https?://', '', domain)
    domain = re.sub(r'^(\*\.|\*|api\.|www\.|ftp\.|mail\.|blog\.|cdn\.|ns\d*\.)+', '', domain)
    domain = domain.split('/')[0]
    domain = domain.split(':')[0]
    if domain.endswith('.'):
        domain = domain[:-1]
    domain = domain.split('?')[0]
    domain = domain.split('#')[0]
    
    return domain.strip()

def main(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"[!] File {input_file} not found.")
        sys.exit(1)

    cleaned_domains = set()
    ip_addresses = set()

    with open(input_file, 'r') as f:
        domains = f.readlines()

    for domain in domains:
        cleaned = clean_domain(domain)
        if is_valid_ip(cleaned):
            ip_addresses.add(cleaned)
        if cleaned and is_valid_domain(cleaned) and not is_valid_ip(cleaned):
            cleaned_domains.add(cleaned)

    with open(output_file, 'w') as f:
        for d in sorted(cleaned_domains):
            f.write(d + "\n")

    with open("ips_" + output_file, 'w') as f:
        for ip in sorted(ip_addresses):
            f.write(ip + "\n")

    print(f"[+] Cleaning completed. {len(cleaned_domains)} unique domains saved to {output_file}")
    print(f"[+] {len(ip_addresses)} unique IP addresses saved to ips_{output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 clean_domains.py <input.txt> <output.txt>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    main(input_file, output_file)