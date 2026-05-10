"""Generate FeiThink brand header in the Sam Harris 'Truth & Consequences' style.

Pipeline: rembg cutout -> grayscale + S-curve -> ordered spot-dot halftone -> composite
on black canvas with orange Fraunces title + white Inter subtitle.

Run: python scripts/brand-image/make_brand_image.py
"""
from __future__ import annotations

import io
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = Path(r"C:\Users\huang\github\dating\photos\current_profile\backup_cafe_beer_neutral.jpeg")
OUT = ROOT / "out" / "feithink_brand.png"
FONT_TITLE = ROOT / "fonts" / "Fraunces.ttf"
FONT_SUB = ROOT / "fonts" / "Inter.ttf"

CANVAS = 1200
BG = (10, 10, 10)
ORANGE = (232, 76, 31)
WHITE = (245, 245, 245)

TITLE_TOP = "Living &"
TITLE_BOT = "Thinking"
SUB_TOP = "Fei Huang"
SUB_BOT = "feithink.org"


def cutout(src: Path) -> Image.Image:
    """rembg cutout -> RGBA."""
    from rembg import remove
    raw = src.read_bytes()
    return Image.open(io.BytesIO(remove(raw))).convert("RGBA")


def s_curve(arr: np.ndarray, low: float = 0.18, high: float = 0.82) -> np.ndarray:
    """Push contrast: clip below `low` to 0 and above `high` to 1, smoothstep middle."""
    x = np.clip((arr - low) / (high - low), 0.0, 1.0)
    return x * x * (3 - 2 * x)


def halftone(gray: np.ndarray, cell: int = 6) -> np.ndarray:
    """Ordered spot-dot halftone. gray in [0,1]; returns uint8 0/255."""
    h, w = gray.shape
    yy, xx = np.mgrid[0:cell, 0:cell].astype(np.float32)
    cx = cy = (cell - 1) / 2.0
    r = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    # threshold matrix: 0 at center, ~1 at corners
    thr = r / r.max()
    big = np.tile(thr, (h // cell + 1, w // cell + 1))[:h, :w]
    return ((gray > big).astype(np.uint8)) * 255


def render_subject(rgba: Image.Image, target_h: int) -> Image.Image:
    """rembg cutout -> halftone subject as RGBA (white dots, transparent elsewhere)."""
    # crop to alpha bbox so positioning is deterministic (no padding from source canvas)
    bbox = rgba.split()[-1].getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    w0, h0 = rgba.size
    scale = target_h / h0
    new_size = (int(w0 * scale), int(h0 * scale))
    rgba = rgba.resize(new_size, Image.LANCZOS)

    # alpha mask
    alpha = np.array(rgba.split()[-1], dtype=np.float32) / 255.0

    # grayscale of subject; lift shadows enough that the black t-shirt still emits some halftone
    # coverage (otherwise the silhouette breaks at neck/torso and the head looks decapitated)
    gray = np.array(rgba.convert("L"), dtype=np.float32) / 255.0
    gray = s_curve(gray, 0.06, 0.82)

    ht = halftone(gray, cell=6)

    # mask halftone by alpha (so background outside subject stays transparent)
    out = np.zeros((*ht.shape, 4), dtype=np.uint8)
    out[..., 0] = 240  # near-white dots
    out[..., 1] = 240
    out[..., 2] = 235
    out[..., 3] = (ht.astype(np.float32) * alpha).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    print(f"[1/4] cutout: {SRC.name}")
    rgba = cutout(SRC)

    print("[2/4] halftone subject")
    # subject occupies ~95% of canvas; head pushed to upper third so title overlays body only
    subject = render_subject(rgba, target_h=int(CANVAS * 0.95))

    print("[3/4] compose canvas")
    canvas = Image.new("RGBA", (CANVAS, CANVAS), BG + (255,))
    sw, sh = subject.size
    # subject bbox includes the cup which biases the geometric center to the right of the face;
    # shift left so the face — the actual focal point — sits near canvas center
    x = (CANVAS - sw) // 2 - 130
    y = 20
    canvas.alpha_composite(subject, (x, y))

    print("[4/4] typography")
    draw = ImageDraw.Draw(canvas)

    # Fraunces axes: [opsz 9-144, wght 100-900, SOFT 0-100, WONK 0-1]
    # 850 weight + 55 softness ≈ Recoleta/Reckless feel; size 140 matches Sam's relative title scale
    title_font = ImageFont.truetype(str(FONT_TITLE), 140)
    title_font.set_variation_by_axes([144, 850, 55, 1])

    # Inter axes: [opsz 14-32, wght 100-900]
    sub_font_name = ImageFont.truetype(str(FONT_SUB), 38)
    sub_font_name.set_variation_by_axes([32, 700])
    sub_font_url = ImageFont.truetype(str(FONT_SUB), 30)
    sub_font_url.set_variation_by_axes([14, 400])

    # title: pushed lower and with tighter leading to match Sam's vertical proportions
    title_x = 50
    title_top_y = 720
    title_bot_y = 895
    draw.text((title_x, title_top_y), TITLE_TOP, font=title_font, fill=ORANGE)
    draw.text((title_x, title_bot_y), TITLE_BOT, font=title_font, fill=ORANGE)

    # subtitle:
    #   - name baseline ⇄ "Living &" baseline (anchor='ls')
    #   - URL placed with explicit visual gap below name (line-spacing param)
    # strict url-bottom-↔-living-descender alignment + bigger gap can't both hold with
    # these font sizes; we prioritize visible leading. URL ends ~20px past "Living" descender.
    title_top_baseline = title_top_y + title_font.getmetrics()[0]
    name_descent = sub_font_name.getmetrics()[1]
    url_leading = 22   # gap between name descender bottom and URL ascender top
    sub_x = 800
    draw.text((sub_x, title_top_baseline), SUB_TOP, font=sub_font_name, fill=WHITE, anchor="ls")
    draw.text((sub_x, title_top_baseline + name_descent + url_leading), SUB_BOT,
              font=sub_font_url, fill=(190, 190, 190), anchor="la")

    canvas.convert("RGB").save(OUT, "PNG", optimize=True)
    print(f"\nwrote: {OUT}")


if __name__ == "__main__":
    main()
