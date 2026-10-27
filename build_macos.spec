# -*- mode: python ; coding: utf-8 -*-
# macOS build spec for Lulu Desktop Pet.
# IMPORTANT: PyInstaller cannot cross-compile. Run this ON A MAC:
#   python3 -m pip install -r requirements.txt
#   python3 scripts/build_icons.py        # generates assets/lulu_icon.icns
#   pyinstaller build_macos.spec --noconfirm --clean
# Output: dist/LuluDesktopPet.app
#
# After build (unsigned apps are blocked by Gatekeeper until you allow them):
#   codesign --deep --force --sign - dist/LuluDesktopPet.app
#   xattr -dr com.apple.quarantine dist/LuluDesktopPet.app
# Then zip for distribution:
#   ditto -c -k --keepParent dist/LuluDesktopPet.app LuluDesktopPet-macos.zip

from pathlib import Path

ROOT = Path.cwd()
ICNS = ROOT / "assets" / "lulu_icon.icns"


def _icns() -> str | None:
    return str(ICNS) if ICNS.exists() else None


a = Analysis(
    ["run_lulu_pet.py"],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(ROOT / "assets"), "assets"),
        (str(ROOT / "config"), "config"),
    ],
    hiddenimports=[
        "PySide6.QtGui",
        "PySide6.QtWidgets",
        "PySide6.QtCore",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="LuluDesktopPet",
    icon=_icns(),
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    target_arch=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="LuluDesktopPet",
)

app = BUNDLE(
    coll,
    name="LuluDesktopPet.app",
    icon=_icns(),
    bundle_identifier="com.lulu.desktoppet",
    info_plist={
        "CFBundleName": "水豚噜噜",
        "CFBundleDisplayName": "水豚噜噜 Lulu",
        "CFBundleIdentifier": "com.lulu.desktoppet",
        "NSHighResolutionCapable": True,
        "NSRequiresAquaSystemAppearance": False,
        "LSMinimumSystemVersion": "10.15",
    },
)
