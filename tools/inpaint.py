#!/usr/bin/env python3
"""Seamless erase of the Grok corner mark, using the LaMa inpainting model.

This is the optional, heavy counterpart to `grok-auto clean`. The npm CLI covers
crop / delogo / cover with nothing but ffmpeg; those are instant and need no
install. This script exists for the one case they can't serve: an image that
already exists, in a framing you don't want to crop, where you need the mark
gone without a trace.

INSTALL COST — tell the user before running this. It pulls torch (~1.2 GB) plus
a one-time ~200 MB model download:

    pip install simple-lama-inpainting pillow

WHY IMAGES ONLY: on video LaMa runs per frame at roughly four minutes per six
seconds of footage on CPU, which reads as a hang rather than a feature. For
video, crop is the right answer — and on 16:9 the reservation recipe in
SKILL.md makes that crop free. Stills inpaint in seconds, which is why this
is worth the install for them and not for clips.

Usage:
    python tools/inpaint.py in.png -o out.png
    python tools/inpaint.py in.jpg -o out.jpg --box 200x80+1080+640

Only use this on media you generated yourself, and keep any AI-content
disclosure honest regardless of whether the mark is visible.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Mark geometry as a fraction of frame width — matches `grok-auto clean`.
BOX_W_FRAC = 0.17
BOX_H_RATIO = 0.42
# Pixels of margin around the box, so anti-aliased mark edges are covered too.
MASK_PAD = 4


def parse_box(spec: str | None, w: int, h: int) -> tuple[int, int, int, int]:
    """(bx, by, bw, bh) — defaults to the bottom-right corner box."""
    if spec:
        m = re.fullmatch(r"(\d+)x(\d+)\+(\d+)\+(\d+)", spec)
        if not m:
            sys.exit(f"bad --box '{spec}' (want WxH+X+Y, e.g. 200x80+1080+640)")
        bw, bh, bx, by = (int(g) for g in m.groups())
    else:
        bw = round(w * BOX_W_FRAC)
        bh = min(round(bw * BOX_H_RATIO), h)
        bx, by = w - bw, h - bh
    if bx + bw > w or by + bh > h:
        sys.exit(f"box {bw}x{bh}+{bx}+{by} exceeds the {w}x{h} frame")
    return bx, by, bw, bh


def load_lama():
    try:
        from simple_lama_inpainting import SimpleLama  # type: ignore
    except ImportError:
        # ASCII only: this prints to a Windows console under cp1252, where an
        # em dash comes out as a replacement character.
        sys.exit(
            "This needs the LaMa model wrapper, which is NOT installed by default\n"
            "because it pulls torch (~1.2 GB) plus a one-time ~200 MB model download.\n"
            "Confirm with the user first, then:\n"
            "  pip install simple-lama-inpainting pillow\n"
            "If you only need the mark gone and can afford a slight zoom, use\n"
            "'grok-auto clean' instead - instant, no install."
        )
    return SimpleLama()


def build_mask(size: tuple[int, int], box: tuple[int, int, int, int]):
    """White-on-black mask over the padded box."""
    from PIL import Image, ImageDraw

    bx, by, bw, bh = box
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rectangle(
        [
            max(0, bx - MASK_PAD),
            max(0, by - MASK_PAD),
            min(size[0], bx + bw + MASK_PAD),
            min(size[1], by + bh + MASK_PAD),
        ],
        fill=255,
    )
    return m


def composite(lama, img, mask):
    """Inpaint, then keep ONLY the masked pixels.

    Used raw, the model reconstructs the entire frame and visibly softens
    texture far outside the box, so its output is composited back through the
    mask. LaMa also pads its input up to a multiple of 8 and can hand back a
    larger canvas — every layer is forced to the source size first, since
    Image.composite requires all three to match exactly.
    """
    from PIL import Image

    res = lama(img, mask)
    if res.size != img.size:
        res = res.crop((0, 0, img.size[0], img.size[1]))
    if mask.size != img.size:
        mask = mask.crop((0, 0, img.size[0], img.size[1]))
    return Image.composite(res, img, mask)


def save_hq(img, out: Path) -> None:
    # PIL's default JPEG quality (75) softens the whole image, undoing the point
    # of a seamless erase.
    if out.suffix.lower() in {".jpg", ".jpeg", ".webp"}:
        img.save(out, quality=95, subsampling=0)
    else:
        img.save(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Seamlessly erase the Grok corner mark from an image.")
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path, required=True)
    ap.add_argument("--box", help="explicit mark box as WxH+X+Y (default: auto corner box)")
    args = ap.parse_args()

    if not args.input.exists():
        sys.exit(f"input not found: {args.input}")

    try:
        from PIL import Image
    except ImportError:
        sys.exit("needs Pillow:  pip install pillow")

    img = Image.open(args.input).convert("RGB")
    box = parse_box(args.box, *img.size)

    lama = load_lama()  # after arg/file validation — it loads ~200 MB of weights
    args.output.parent.mkdir(parents=True, exist_ok=True)
    save_hq(composite(lama, img, build_mask(img.size, box)), args.output)
    print(f"inpainted {box[2]}x{box[3]}+{box[0]}+{box[1]} -> {args.output}")


if __name__ == "__main__":
    main()
