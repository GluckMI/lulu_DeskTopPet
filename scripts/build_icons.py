"""Generate app icons (.ico for Windows, .icns for macOS) from a transparent GIF frame.

Uses only PySide6 (the app's only runtime dependency) so no extra packages are needed.
The .icns is built manually as a PNG container because Qt's icns writer is only
available on macOS.
"""
from __future__ import annotations

import struct
from pathlib import Path

from PySide6.QtCore import QBuffer, QByteArray, Qt
from PySide6.QtGui import QImage

ROOT = Path(__file__).resolve().parent.parent
# The transparent character GIF used to live in assets/lulu_transparent_gifs/,
# but the assets tree was reorganised into assets/characters/<name>/. Keep both
# locations plus a recursive fallback so the icon build survives future moves.
CANDIDATES = [
    ROOT / "assets" / "characters" / "lulu" / "640 (1).gif",
    ROOT / "assets" / "lulu_transparent_gifs" / "640 (1).gif",
]
ICO_OUT = ROOT / "assets" / "lulu_icon.ico"
ICNS_OUT = ROOT / "assets" / "lulu_icon.icns"


def find_source() -> Path:
    for c in CANDIDATES:
        if c.exists():
            return c
    # Last resort: first GIF found anywhere under assets/.
    for p in sorted(ROOT.glob("assets/**/*.gif")):
        return p
    raise SystemExit("[build_icons] no source GIF found under assets/")


def load_rgba(path: Path) -> QImage:
    img = QImage(str(path))
    if img.isNull():
        raise SystemExit(f"[build_icons] cannot load {path}")
    if img.hasAlphaChannel():
        img = img.convertToFormat(QImage.Format_RGBA8888)
    else:
        img = img.convertToFormat(QImage.Format_RGB32)
    return img


def png_bytes(img: QImage, size: int) -> bytes:
    scaled = img.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    buf = QBuffer()
    buf.open(QBuffer.WriteOnly)
    ok = scaled.save(buf, "PNG")
    if not ok:
        raise SystemExit(f"[build_icons] failed to encode PNG @{size}")
    return bytes(buf.data())


def write_icns(img: QImage, out: Path) -> None:
    specs = [(128, b"ic07"), (256, b"ic08"), (512, b"ic09"), (1024, b"ic10")]
    entries = b""
    for size, ostype in specs:
        data = png_bytes(img, size)
        entries += ostype + struct.pack(">I", len(data) + 8) + data
    payload = b"icns" + struct.pack(">I", len(entries) + 8) + entries
    out.write_bytes(payload)


def main() -> None:
    src = find_source()
    print(f"[build_icons] using source: {src}")
    img = load_rgba(src)
    # Windows .ico (256px, Explorer scales as needed)
    pix = QImage(img)
    pix = pix.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    if not pix.save(str(ICO_OUT), "ICO"):
        raise SystemExit("[build_icons] failed to write .ico")
    # macOS .icns
    write_icns(img, ICNS_OUT)
    print(f"[build_icons] wrote {ICO_OUT} ({ICO_OUT.stat().st_size} bytes)")
    print(f"[build_icons] wrote {ICNS_OUT} ({ICNS_OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
