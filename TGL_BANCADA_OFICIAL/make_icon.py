"""Generate a code-native TGL sigil as SVG and Windows ICO (stdlib only)."""

from __future__ import annotations

import math
import struct
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATIC = HERE / "static"

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" role="img" aria-label="TGL: igualdade luminosa e órbitas">
<defs><radialGradient id="bg"><stop stop-color="#142c42"/><stop offset="1" stop-color="#04101e"/></radialGradient><linearGradient id="ring" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#3ce5ef"/><stop offset="1" stop-color="#f2b75c"/></linearGradient></defs>
<circle cx="128" cy="128" r="122" fill="url(#bg)" stroke="#3ce5ef" stroke-width="3"/>
<circle cx="128" cy="128" r="99" fill="none" stroke="url(#ring)" stroke-width="2" opacity=".8"/>
<ellipse cx="128" cy="128" rx="109" ry="45" fill="none" stroke="#3ce5ef" stroke-width="3" transform="rotate(-32 128 128)" opacity=".85"/>
<ellipse cx="128" cy="128" rx="109" ry="45" fill="none" stroke="#f2b75c" stroke-width="2" transform="rotate(32 128 128)" opacity=".7"/>
<circle cx="43" cy="102" r="6" fill="#72f7f4"/><circle cx="211" cy="102" r="5" fill="#ffd38c"/>
<rect x="70" y="97" width="116" height="17" rx="8.5" fill="#f4d18e"/><rect x="70" y="142" width="116" height="17" rx="8.5" fill="#f4d18e"/>
<path d="M128 21v30M128 205v30M21 128h30M205 128h30" stroke="#67e8f0" stroke-width="2" opacity=".65"/>
</svg>'''


def crc_chunk(kind: bytes, body: bytes) -> bytes:
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))


def png(size: int) -> bytes:
    rows = bytearray()
    scale = 256 / size
    for yi in range(size):
        rows.append(0)
        for xi in range(size):
            x = (xi + 0.5) * scale - 128
            y = (yi + 0.5) * scale - 128
            r = math.hypot(x, y)
            if r > 121:
                rows.extend((0, 0, 0, 0))
                continue
            col = [6, 19, 33, 255]
            if abs(r - 119) < 3 or abs(r - 99) < 1.8:
                col[:3] = [55, 211, 222]
            # Two opposed tilted ellipses, the traversing fold.
            for angle, color in ((-0.56, (52, 207, 225)), (0.56, (229, 167, 87))):
                u = x * math.cos(angle) + y * math.sin(angle)
                v = -x * math.sin(angle) + y * math.cos(angle)
                e = (u / 108) ** 2 + (v / 45) ** 2
                if abs(e - 1) < 0.035:
                    col[:3] = color
            if 70 - 128 < x < 186 - 128 and (97 - 128 < y < 114 - 128 or 142 - 128 < y < 159 - 128):
                col[:3] = [245, 210, 145]
            rows.extend(col)
    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + crc_chunk(b"IHDR", header) + crc_chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + crc_chunk(b"IEND", b"")


def main() -> None:
    STATIC.mkdir(parents=True, exist_ok=True)
    (STATIC / "TGL.svg").write_text(SVG, encoding="utf-8")
    images = [(size, png(size)) for size in (16, 32, 48, 64, 256)]
    offset = 6 + 16 * len(images)
    entries = []
    for size, body in images:
        entries.append(struct.pack("<BBBBHHII", 0 if size == 256 else size,
                                   0 if size == 256 else size, 0, 0, 1, 32,
                                   len(body), offset))
        offset += len(body)
    ico = struct.pack("<HHH", 0, 1, len(images)) + b"".join(entries) + b"".join(body for _, body in images)
    (HERE / "TGL.ico").write_bytes(ico)
    (STATIC / "favicon.ico").write_bytes(ico)
    print(f"Generated TGL.ico ({len(ico)} bytes), SVG and favicon")


if __name__ == "__main__":
    main()
