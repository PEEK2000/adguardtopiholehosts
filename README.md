## Purpose

This is a very basic script that extracts urls from blocklists and converts them to HOSTS syntax used by Pi-Hole.

**Careful!**
Some AdGuard lists contain whitelisted domains marked with the prefix "@@" (e.g.  `@@¦¦example.com^`)    
These whitelisted domains need to be added to the Pi-Hole separateley, as domains found inside blocklist cannot be whitelisted.

## How to use:

Add any adguard blocklist to the *"AdGuard_blocklists.csv"* and specify a name for the list in the second row.
Then put the .py script and .csv file in the same directory and execute the script. (pip required)
The script will run for some time, depending on blocklist sizes and create the folder *"Blocklists_outputs"*.

Voilà

**Original repositories are credited in the respective blocklist.**
