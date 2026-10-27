# -*- mode: python ; coding: utf-8 -*-
# Windows build spec for Lulu Desktop Pet.
# Build:  pyinstaller lulu-pet.spec --noconfirm --clean
# Output: dist/LuluDesktopPet/  (keep the whole folder together)

from pathlib import Path

ROOT = Path.cwd()

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
    icon=str(ROOT / "assets" / "lulu_icon.ico") if (ROOT / "assets" / "lulu_icon.ico").exists() else None,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
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
