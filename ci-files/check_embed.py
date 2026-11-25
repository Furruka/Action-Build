import argparse
import hashlib
from pathlib import Path
import struct


def main():
    parser = argparse.ArgumentParser(description="Verify the board DTB in a raw arm64 Image.")
    parser.add_argument("image", type=Path)
    parser.add_argument("dtb", type=Path)
    args = parser.parse_args()

    image = args.image.read_bytes()
    dtb = args.dtb.read_bytes()
    if image[56:60] != b"ARM\x64":
        parser.exit(1, "Expected an uncompressed arm64 Image\n")
    if len(dtb) < 40:
        parser.exit(1, "Board DTB header is truncated\n")
    magic, total_size = struct.unpack_from(">II", dtb)
    if magic != 0xD00DFEED or total_size != len(dtb):
        parser.exit(1, "Board DTB magic or total size is invalid\n")

    offset = image.find(dtb)
    if offset < 0:
        parser.exit(1, "The board DTB bytes are missing from Image\n")
    if offset % 8:
        parser.exit(1, f"Board DTB is not 8-byte aligned at offset {offset:#x}\n")
    print(f"Image SHA-256: {hashlib.sha256(image).hexdigest()}")
    print(f"DTB SHA-256: {hashlib.sha256(dtb).hexdigest()}")
    print(f"Matched the complete {total_size}-byte DTB at Image offset {offset:#x}")


if __name__ == "__main__":
    main()
