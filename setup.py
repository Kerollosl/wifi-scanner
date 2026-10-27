from setuptools import setup

APP = ["wifi_menubar.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleName": "WiFi Scanner",
        "CFBundleIdentifier": "com.kerolowandy.wifiscanner",
        "CFBundleShortVersionString": "1.0",
        "LSUIElement": True,  # menu bar app, no dock icon
        "NSLocationWhenInUseUsageDescription": "WiFi Scanner needs location access to display network SSIDs.",
        "NSLocationUsageDescription": "WiFi Scanner needs location access to display network SSIDs.",
    },
    "packages": ["rumps"],
    "includes": ["CoreWLAN", "CoreLocation", "objc"],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
