import requests
import os
import csv
import re

# Define paths
BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, "Blocklist_outputs")
WHITELIST_DIR = os.path.join(BASE_DIR, "whitelist.txt")
CSV_DIR = os.path.join(BASE_DIR, "AdGuard_blocklists.csv")

# Fetch blocklist data from the AdGuard_blocklists.csv file
def fetch_blocklist(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

# Add disclaimer and convert blocklist to HOSTS format and extract whitelisted domains
def convert_to_hosts_format(blocklist, url):
    disclaimer = [
        "# This blocklist was converted from AdGuard syntax to HOSTS syntax to enable it being used for Pi-Hole.",
        f"# All credits go to the original repository: {url}\n"
    ]
    
    domain_pattern = re.compile(r'\|\|([^|^]+)\^')  # Extract domains between "||" and "^"
    whitelist_pattern = re.compile(r'^@@\|\|([^|^]+)\^')  # Extract whitelisted domains between "@@||" and "^"

    hosts_lines = []
    whitelisted_domains = []
    
    for line in blocklist:
        # Ignore comments and empty lines
        if line.startswith(('!', '#')) or not line:
            continue
        
        # Check for whitelisted domain and add to whitelist.txt if found
        if whitelist_match := whitelist_pattern.search(line):
            whitelisted_domains.append(whitelist_match.group(1).strip())
            continue  # Skip adding this line to hosts_lines

        # Check for regular blocklist domain and add to hosts_lines if found
        if domain_match := domain_pattern.search(line):
            hosts_lines.append(f"0.0.0.0 {domain_match.group(1).strip()}")

    return disclaimer + hosts_lines, whitelisted_domains

# Save list of lines to the specified directory
def save_to_file(lines, filename):
    output_path = os.path.join(OUTPUT_DIR, f"{filename}.txt")
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists
    with open(output_path, 'w') as file:
        file.write("\n".join(lines))
    print(f"Blocklist saved to {output_path}")

# Append whitelisted domains to the whitelist.txt file
def save_whitelist(whitelisted_domains):
    with open(WHITELIST_DIR, 'a') as whitelist_file:
        for domain in whitelisted_domains:
            whitelist_file.write(f"{domain}\n")
    print(f"Whitelisted domains appended to {WHITELIST_DIR}")

def main():
    # Clear whitelist.txt at the beginning to avoid adding multiples
    open(WHITELIST_DIR, 'w').close()

    try:
        with open(CSV_DIR, newline='') as csvfile:
            for url, output_filename in csv.reader(csvfile):
                blocklist = fetch_blocklist(url)
                hosts_lines, whitelisted_domains = convert_to_hosts_format(blocklist, url)
                save_to_file(hosts_lines, output_filename)
                save_whitelist(whitelisted_domains)
    except Exception as e:
        print(f"An error occurred: {e}")  # Print Error-message if necessary

print("Conversion completed.")

if __name__ == "__main__":
    main()