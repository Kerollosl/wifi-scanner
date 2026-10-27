# WiFi Scanner — macOS Menu Bar App

Python macOS menu bar app that displays nearby WiFi networks via `CoreWLAN`. Built as a native `.app` with `py2app`. Not a Chrome Extension despite living in the Chrome Extensions folder.

## Files

| File | Purpose |
|------|---------|
| `wifi_menubar.py` | Main entry — `rumps`-based menu bar app |
| `wifi_scan.py` | WiFi scanning via `CoreWLAN` + `CoreLocation` |
| `wifi-scan-raycast.py` | Standalone Raycast script variant |
| `setup.py` | `py2app` build config → produces `.app` bundle |
| `build/` | py2app intermediate files |
| `dist/` | Final `.app` output → `WiFi Scanner.app` |

## Running (Dev Mode)

```bash
python wifi_menubar.py
```

Requires location permission for SSID visibility (macOS 14+).

## Building the .app

```bash
pip install py2app rumps pyobjc-framework-CoreWLAN pyobjc-framework-CoreLocation
python setup.py py2app
# Output: dist/WiFi Scanner.app
```

## Key Details

- `LSUIElement: True` in `setup.py` plist → menu bar only, no Dock icon
- `CoreWLAN` scans require `CWInterface.scanForNetworks(withSSID:)` — wrap calls in `try/except` as macOS can throttle scans
- Location permission prompt only appears on first run of the built `.app`, not in dev mode
- `rumps` handles the NSStatusItem / menu lifecycle; keep the scan off the main thread to avoid blocking UI
