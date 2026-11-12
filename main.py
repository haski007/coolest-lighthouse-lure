"""Entry for the make.fun bounty coolest-art-01.

Writes one piece of art to <output dir>/entry.png: the image stored next to
this file, copied byte for byte. Standard library only, no network, and the
same bytes on every run.
"""

import os
import struct
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
OUTPUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

MAX_BYTES = 1_048_576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"
PNG_END = b"\x00\x00\x00\x00IEND\xaeB`\x82"
JPEG_END = b"\xff\xd9"


def image_size(data: bytes) -> tuple[int, int] | None:
    """Width and height from a PNG header or a JPEG frame header, or None."""
    if data.startswith(PNG_MAGIC):
        if data[12:16] != b"IHDR":
            return None
        return struct.unpack(">II", data[16:24])
    pos = 2
    while pos + 9 <= len(data):
        if data[pos] != 0xFF:
            return None
        marker = data[pos + 1]
        if marker == 0xFF:  # fill byte before a marker
            pos += 1
            continue
        length = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        # SOF0..SOF15 carry the frame size; C4, C8 and CC are tables, not frames.
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + length
    return None


def main() -> int:
    if not SOURCE.is_file():
        print(f"error: art not found: {SOURCE}", file=sys.stderr)
        return 1
    data = SOURCE.read_bytes()
    if not data.startswith((PNG_MAGIC, JPEG_MAGIC)):
        print("error: art is neither a PNG nor a JPEG", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"error: art is {len(data)} bytes, over {MAX_BYTES}", file=sys.stderr)
        return 1
    # The gate also caps the picture at 1024 by 1024 pixels: check it here too.
    size = image_size(data)
    if size is None:
        print("error: cannot read the image size from its header", file=sys.stderr)
        return 1
    if size[0] > MAX_SIDE or size[1] > MAX_SIDE:
        print(f"error: art is {size[0]}x{size[1]}, over {MAX_SIDE}x{MAX_SIDE}", file=sys.stderr)
        return 1
    # A whole image: a PNG closes with its IEND chunk, a JPEG with its end marker.
    if not data.endswith((PNG_END, JPEG_END)):
        print("error: art is cut short, its end marker is missing", file=sys.stderr)
        return 1
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = OUTPUT_DIR / "entry.png"
    # Write to a side file and rename it, so a half-written entry.png never exists.
    partial = OUTPUT_DIR / "entry.png.part"
    partial.write_bytes(data)
    os.replace(partial, target)
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
