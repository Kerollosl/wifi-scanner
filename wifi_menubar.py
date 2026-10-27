#!/usr/bin/env python3
"""Wi-Fi Scanner Menu Bar App — uses rumps to live in the macOS menu bar."""

import rumps
import CoreLocation
from wifi_scan import scan, filter_and_sort, signal_bar


class WifiScannerApp(rumps.App):
    def __init__(self):
        super().__init__("WiFi", icon=None, title="📶")
        self.menu = [
            rumps.MenuItem("Scan Now", callback=self.on_scan),
            None,  # separator
        ]
        # Request location permission (required for SSID visibility)
        self._loc_mgr = CoreLocation.CLLocationManager.alloc().init()
        self._loc_mgr.requestWhenInUseAuthorization()
        # Run an initial scan on launch
        self.on_scan(None)

    @rumps.timer(300)  # auto-refresh every 5 minutes
    def auto_scan(self, _):
        self.on_scan(None)

    def on_scan(self, _):
        try:
            networks = scan()
            results = filter_and_sort(networks)
            top = results[:5]
        except Exception as e:
            rumps.notification("WiFi Scanner", "Scan failed", str(e))
            return

        # Clear old network entries (keep "Scan Now" and separator)
        for key in list(self.menu.keys()):
            if key not in ("Scan Now", None):
                del self.menu[key]

        if not top:
            self.menu.add(rumps.MenuItem("No suitable networks found"))
            return

        for n in top:
            bar = signal_bar(n["RSSI"])
            label = f"{bar}  {n['SSID']}  ({n['RSSI']} dBm)  [{n['Security']}]"
            self.menu.add(rumps.MenuItem(label))

        count = len(results)
        self.menu.add(None)  # separator
        self.menu.add(rumps.MenuItem(f"{count} networks passed filters"))


if __name__ == "__main__":
    WifiScannerApp().run()
