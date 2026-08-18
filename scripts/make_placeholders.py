# -*- coding: utf-8 -*-
"""Generates elegant photo-frame placeholder PNGs embedded in the workbook
where couples add their own images (dashboard hero, moodboard, decor, etc.).
Editorial look: soft tint, thin frame, corner crop marks, a fine line-art
image glyph, and a small letter-spaced caption."""
import os
from PIL import Image, ImageDraw, ImageFont

ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(ASSET_DIR, exist_ok=True)

SCALE = 3  # supersample for crisp downscaled edges

# palette (RGB)
CREAM = (247, 243, 236)
BLUSH = (246, 217, 222)
SAGE = (220, 232, 216)
LAV = (216, 211, 240)
POWDER = (216, 230, 240)
PEACH = (245, 223, 208)
INK = (150, 143, 136)
INK_SOFT = (176, 170, 163)
FRAME = (198, 190, 181)


def _font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else ""),
        "/usr/share/fonts/truetype/liberation/LiberationSans%s.ttf" % ("-Bold" if bold else ""),
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _rounded(draw, box, r, **kw):
    draw.rounded_rectangle(box, radius=r, **kw)


def _letterspace(draw, xy, text, font, fill, spacing):
    x, y = xy
    total = 0
    widths = []
    for ch in text:
        w = draw.textlength(ch, font=font)
        widths.append(w)
        total += w + spacing
    total -= spacing
    x = xy[0] - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + spacing
    return total


def image_glyph(draw, cx, cy, s, color):
    """Fine line-art 'landscape photo' glyph: frame + sun + two hills."""
    lw = max(2, s // 22)
    left, top = cx - s / 2, cy - s / 2
    right, bottom = cx + s / 2, cy + s / 2
    draw.rounded_rectangle([left, top, right, bottom], radius=s * 0.10,
                           outline=color, width=lw)
    # sun
    sr = s * 0.11
    scx, scy = left + s * 0.30, top + s * 0.30
    draw.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], outline=color, width=lw)
    # hills (two triangles) sitting on the base
    base = bottom - lw * 1.2
    draw.line([(left + lw, base), (left + s * 0.42, top + s * 0.55),
               (left + s * 0.62, base)], fill=color, width=lw, joint="curve")
    draw.line([(left + s * 0.45, base), (left + s * 0.72, top + s * 0.42),
               (right - lw, base)], fill=color, width=lw, joint="curve")


def make_placeholder(name, w, h, tint, caption="YOUR PHOTO HERE", crop_marks=True):
    W, H = w * SCALE, h * SCALE
    img = Image.new("RGB", (W, H), tint)
    d = ImageDraw.Draw(img)
    m = int(min(W, H) * 0.045)
    # inner panel slightly lighter
    panel = tuple(min(255, int(c + (255 - c) * 0.45)) for c in tint)
    _rounded(d, [m, m, W - m, H - m], r=int(min(W, H) * 0.05), fill=panel)
    # thin frame
    _rounded(d, [m, m, W - m, H - m], r=int(min(W, H) * 0.05),
             outline=FRAME, width=max(2, SCALE))
    # corner crop marks (editorial)
    if crop_marks:
        cm = int(min(W, H) * 0.11)
        off = int(m * 1.9)
        lw = max(2, SCALE)
        for (cx, cy, dx, dy) in [(off, off, 1, 1), (W - off, off, -1, 1),
                                 (off, H - off, 1, -1), (W - off, H - off, -1, -1)]:
            d.line([(cx, cy), (cx + dx * cm, cy)], fill=INK_SOFT, width=lw)
            d.line([(cx, cy), (cx, cy + dy * cm)], fill=INK_SOFT, width=lw)
    # glyph
    gs = int(min(W, H) * 0.34)
    gcy = H * 0.44
    image_glyph(d, W / 2, gcy, gs, INK)
    # caption
    fsize = int(min(W, H) * 0.075)
    f = _font(fsize, bold=True)
    _letterspace(d, (W / 2, gcy + gs * 0.72), caption, f, INK, spacing=fsize * 0.22)
    out = img.resize((w, h), Image.LANCZOS)
    path = os.path.join(ASSET_DIR, name)
    out.save(path)
    print("wrote", path, (w, h))
    return path


if __name__ == "__main__":
    # Dashboard hero — wide strip matching a 5-col x 4-row card (~2.3:1)
    make_placeholder("photo_hero.png", 450, 194, CREAM, caption="ADD YOUR PHOTO")
    # Moodboard / theme tiles — one per soft tint
    tints = {"blush": BLUSH, "sage": SAGE, "lav": LAV, "powder": POWDER,
             "peach": PEACH, "cream": CREAM}
    for key, t in tints.items():
        make_placeholder("tile_%s.png" % key, 300, 220, t, caption="ADD IMAGE")
