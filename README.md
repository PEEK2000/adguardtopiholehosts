## Purpose

This is a very basic script that extracts urls from blocklists and converts them to HOSTS syntax used by Pi-Hole.

Some AdGuard lists contain whitelisted domains marked with the prefix "@@" 
(e.g.  `@@¦¦example.com^`)    
These whitelisted domains are extracted and placed in a separate *whitelist.txt* file that is created in the directory of the script file.
This allows separate whitelisting of the domains in Pi-Hole.

## How to use:

Add any links blocklists in AdGuard syntax to the *AdGuard_blocklists.csv* and specify a name for the list in the second row.
Then put the .py script and .csv file in the same directory and execute the script.
The script will run for some time, depending on blocklist sizes and create the folder *Blocklists_outputs* where you can find the converted blocklists.
Whitelisted domains will be compiled in form of a single *whitelist.txt* file in the root folder of the script.

**Original repositories are credited in the respective blocklist.**
