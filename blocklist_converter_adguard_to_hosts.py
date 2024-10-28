

#
# This script was written with help from ChatGPT, as I am a novice in programming and had to find a quick solution for the syntax problem of incompatible blocklists.
#

import requests
import os
import csv
import re

# Define paths
BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, "Blocklist_outputs")
CSV_PATH = os.path.join(BASE_DIR, "AdGuard_blocklists.csv")

# Fetch blocklist data from the AdGuard_blocklists.csv file
def fetch_blocklist(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

# Add disclaimer and convert blocklist to HOSTS format
def convert_to_hosts_format(blocklist, url):
    disclaimer = [
        "# This blocklist was converted from AdGuard syntax to a HOSTS file for Pi-Hole.",
        f"# All credits go to the original repository: {url}\n"
    ]
    hosts_lines = []
    
    for line in blocklist:
        # Skip comments and empty lines
        if line.startswith(('!', '#')) or not line:
            continue

        # Remove "||", and everything after "^"
        cleaned_line = re.sub(r'^\|\|', '', line)
        cleaned_line = re.sub(r'\^.*', '', cleaned_line)

        # Add "0.0.0.0" in front of the url
        if cleaned_line.strip():
            hosts_lines.append(f"0.0.0.0 {cleaned_line.strip()}")

    return disclaimer + hosts_lines

# Create the output path and save blocklist as txt
def save_to_file(lines, filename):
    output_path = os.path.join(OUTPUT_DIR, f"{filename}.txt")
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Ensure output directory exists
    with open(output_path, 'w') as file:
        file.write("\n".join(lines))
    print(f"Blocklist saved to {output_path}")

def main():
    try:
        with open(CSV_PATH, newline='') as csvfile:
            for url, output_filename in csv.reader(csvfile):
                blocklist = fetch_blocklist(url)
                hosts_lines = convert_to_hosts_format(blocklist, url)
                save_to_file(hosts_lines, output_filename)
    except Exception as e:
        print(f"An error occurred: {e}")  # Print Error-message if necessary

if __name__ == "__main__":
    main()

