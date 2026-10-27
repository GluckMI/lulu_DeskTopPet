#!/usr/bin/env bash
# Build Lulu Desktop Pet for macOS. Run this ON A MAC (PyInstaller cannot cross-compile).
set -euo pipefail
cd "$(dirname "$0")"

python3 -m pip install -r requirements.txt
python3 scripts/build_icons.py
pyinstaller build_macos.spec --noconfirm --clean

# Ad-hoc sign so Gatekeeper lets the unsigned app launch (no Apple Developer cert needed).
codesign --deep --force --sign - dist/LuluDesktopPet.app
xattr -dr com.apple.quarantine dist/LuluDesktopPet.app 2>/dev/null || true

# Zip the .app for distribution, preserving the bundle layout.
ditto -c -k --keepParent dist/LuluDesktopPet.app LuluDesktopPet-macos.zip

echo
echo "Done: dist/LuluDesktopPet.app and LuluDesktopPet-macos.zip"
echo "On first launch, right-click the app > Open if Gatekeeper blocks it."
