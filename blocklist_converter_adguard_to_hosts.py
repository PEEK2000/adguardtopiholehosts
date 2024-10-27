
#
# This script was written with a lot of help from Chatgpt, as I am a novice in programming and had to find a quick solution for the syntax problem of my blocklists.
#


import requests
import os
import csv

# Fetch blocklist data from a URL
def fetch_blocklist(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensure request success
    return response.text.splitlines()

# Convert blocklist lines to HOSTS format, adding disclaimer at the start
def convert_to_hosts_format(blocklist, url):
    disclaimer = [
        "# This blocklist was converted from AdGuard syntax to a HOSTS file for Pi-Hole.",
        f"# All credits go to the original repository: {url}\n"
    ]
    hosts_lines = disclaimer + [
        line.replace('^', '').replace('||', '0.0.0.0 ').strip()
        for line in blocklist
        if line and not line.startswith(('!', '#'))
    ]
    return hosts_lines

# Save the formatted lines to a file
def save_to_file(lines, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        file.write("\n".join(lines))
    print(f"Blocklist saved to {output_path}")

def main():
    # Read each URL and filename from CSV and process
    with open("AdGuard_blocklists.csv", newline='') as csvfile:
        for url, output_filename in csv.reader(csvfile):
            output_path = os.path.join("Blocklist_outputs", f"{output_filename}.txt")
            try:
                blocklist = fetch_blocklist(url)
                hosts_lines = convert_to_hosts_format(blocklist, url)
                save_to_file(hosts_lines, output_path)
            except Exception as e:
                print(f"An error occurred for {url}: {e}")

if __name__ == "__main__":
    main()
