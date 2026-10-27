#!/usr/bin/env python3
"""Wi-Fi Scanner — scans nearby networks using macOS CoreWLAN and prints the top 5."""

import subprocess
import sys
import time

# CoreWLAN requires pyobjc — fall back to airport CLI if unavailable
try:
    import CoreWLAN
    USE_COREWLAN = True
except ImportError:
    USE_COREWLAN = False

AIRPORT = (
    "/System/Library/PrivateFrameworks/Apple80211.framework"
    "/Versions/Current/Resources/airport"
)


def scan_corewlan():
    """Scan using the native CoreWLAN framework (modern macOS)."""
    iface = CoreWLAN.CWWiFiClient.sharedWiFiClient().interface()
    for attempt in range(3):
        networks, error = iface.scanForNetworksWithName_error_(None, None)
        if not error:
            break
        if attempt < 2:
            time.sleep(1)
    else:
        print(f"Scan error: {error}", file=sys.stderr)
        return []

    results = []
    for net in networks:
        results.append({
            "SSID": net.ssid() or "<Hidden>",
            "RSSI": net.rssiValue(),
            "Security": security_string(net),
        })
    return results


def security_string(network):
    """Derive a human-readable security label from CWNetwork flags."""
    if network.isOpen():
        return "Open"
    if network.supportsEAP():
        return "WPA-ENT"
    if network.supportsPSK():
        return "WPA-PSK"
    return "Secure"


def scan_airport():
    """Scan using the legacy airport CLI tool (older macOS)."""
    try:
        out = subprocess.check_output([AIRPORT, "-s"], text=True)
    except FileNotFoundError:
        print("Error: neither CoreWLAN nor airport CLI available.", file=sys.stderr)
        print("Install pyobjc-framework-CoreWLAN: pip install pyobjc-framework-CoreWLAN", file=sys.stderr)
        sys.exit(1)

    lines = out.strip().splitlines()
    if len(lines) < 2:
        return []

    header = lines[0]
    # airport uses fixed-width columns; find column positions from the header
    rssi_col = header.index("RSSI")
    sec_col = header.index("SECURITY")

    results = []
    for line in lines[1:]:
        if not line.strip():
            continue
        ssid = line[:rssi_col].strip()
        parts = line[rssi_col:].split()
        if len(parts) < 3:
            continue
        rssi = int(parts[0])
        security = parts[-1]
        results.append({"SSID": ssid, "RSSI": rssi, "Security": security})
    return results


def scan():
    """Run a Wi-Fi scan using the best available method."""
    if USE_COREWLAN:
        return scan_corewlan()
    return scan_airport()


def filter_and_sort(networks):
    """Filter out enterprise and weak networks, sort strongest first."""
    filtered = [
        n for n in networks
        if "ENT" not in n["Security"].upper() and n["RSSI"] >= -85
    ]
    filtered.sort(key=lambda n: n["RSSI"], reverse=True)
    return filtered


def print_table(networks, limit=5):
    """Print a clean table of networks."""
    top = networks[:limit]
    if not top:
        print("No suitable networks found.")
        return

    ssid_w = max(len(n["SSID"]) for n in top)
    ssid_w = max(ssid_w, 4)  # minimum width for header

    print(f"{'#':<3} {'SSID':<{ssid_w}}  {'RSSI':>5}  {'Security'}")
    print(f"{'─'*3} {'─'*ssid_w}  {'─'*5}  {'─'*12}")
    for i, n in enumerate(top, 1):
        bar = signal_bar(n["RSSI"])
        print(f"{i:<3} {n['SSID']:<{ssid_w}}  {n['RSSI']:>5}  {n['Security']}  {bar}")


def signal_bar(rssi):
    """Return a visual signal strength indicator."""
    # Map RSSI (-30 best, -85 worst we allow) to 1-5 bars
    strength = max(0, min(5, (rssi + 90) // 12 + 1))
    return "|" * strength + " " * (5 - strength)


def main():
    print("Scanning Wi-Fi networks...\n")
    networks = scan()
    results = filter_and_sort(networks)
    print_table(results)
    print(f"\n({len(results)} networks passed filters out of {len(networks)} total)")


if __name__ == "__main__":
    main()
