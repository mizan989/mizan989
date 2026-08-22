"""
prep_photo.py

One-time prep of a source photo so it converts cleanly to ASCII art:
  1. Remove the background (rembg) so only the subject remains.
  2. Boost local contrast (OpenCV CLAHE) so a flat face gets real
     highlights/shadows instead of converting to a dark blob.
  3. Composite onto pure white so the background maps to the blank
     end of the ASCII ramp (white -> space character).

Usage:
    python scripts/prep_photo.py source-photo.jpg

Writes: source-prepped.png (grayscale, ready for make_ascii_svg.py)
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def prep(src_path: str, out_path: str = "source-prepped.png") -> None:
    src_bytes = Path(src_path).read_bytes()

    # 1. Remove background -> RGBA with alpha mask around the subject
    cutout_bytes = remove(src_bytes)
    cutout = Image.open(__import__("io").BytesIO(cutout_bytes)).convert("RGBA")

    # 2. Composite onto pure white
    white_bg = Image.new("RGBA", cutout.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, cutout).convert("RGB")

    # 3. CLAHE contrast boost (on the grayscale version)
    gray = cv2.cvtColor(np.array(composited), cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    boosted = clahe.apply(gray)

    Image.fromarray(boosted).save(out_path)
    print(f"wrote {out_path}  ({composited.size[0]}x{composited.size[1]})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python scripts/prep_photo.py <source-photo.jpg>")
        sys.exit(1)
    prep(sys.argv[1])
