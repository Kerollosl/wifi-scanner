#!/Users/kerolowandy/Scripts/wifi-scanner/.venv/bin/python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Wi-Fi Scanner
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 📶
# @raycast.packageName WiFi

# Documentation:
# @raycast.description Scan nearby Wi-Fi networks — top 5 strongest, no enterprise
# @raycast.author kerolowandy

import sys
sys.path.insert(0, "/Users/kerolowandy/Scripts/wifi-scanner")

from wifi_scan import scan, filter_and_sort, print_table

networks = scan()
results = filter_and_sort(networks)
print_table(results)
print(f"\n({len(results)} of {len(networks)} networks passed filters)")
