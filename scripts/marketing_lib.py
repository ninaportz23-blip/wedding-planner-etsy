# -*- coding: utf-8 -*-
"""Reusable Pillow toolkit for building the Etsy marketing/listing images."""
import os, re, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

HERE = os.path.dirname(__file__)
FONT_DIR = os.path.join(HERE, "fonts")
SCREENS_DIR = os.path.join(HERE, "..", "qa_screens")
OUT_DIR = os.path.join(HERE, "..", "etsy-listing-images")
os.makedirs(OUT_DIR, exist_ok=True)

CANVAS_W, CANVAS_H = 1200, 1600

# ------------------------------------------------------------------ palette
LAVENDER = (216, 211, 240)
BLUSH = (246, 217, 222)
SAGE = (220, 232, 216)
CREAM = (245, 239, 214)
POWDER = (216, 230, 240)
PEACH = (245, 223, 208)
CHARCOAL = (46, 46, 46)
OFFWHITE = (251, 249, 246)
GREY = (229, 225, 218)
WHITE = (255, 255, 255)
MUTED_GREY = (90, 90, 90)

BADGE_ROTATION = [LAVENDER, BLUSH, SAGE, PEACH]

# -------------------------------------------------------------------- fonts
_FONT_CACHE = {}

FONT_FILES = {
    "display_black": "PlayfairDisplay-Black.ttf",
    "display_bold": "PlayfairDisplay-Bold.ttf",
    "display_italic": "PlayfairDisplay-Italic.ttf",
    "sans_regular": "Poppins-Regular.ttf",
    "sans_semibold": "Poppins-SemiBold.ttf",
    "sans_bold": "Poppins-Bold.ttf",
    "sans_extrabold": "Poppins-ExtraBold.ttf",
}


def font(key, size):
    cache_key = (key, size)
    if cache_key not in _FONT_CACHE:
        path = os.path.join(FONT_DIR, FONT_FILES[key])
        _FONT_CACHE[cache_key] = ImageFont.truetype(path, size)
    return _FONT_CACHE[cache_key]


# ------------------------------------------------------------------ canvas
def new_canvas():
    return Image.new("RGB", (CANVAS_W, CANVAS_H), OFFWHITE)


# ---------------------------------------------------------- paper texture
PAPER_BASE = (246, 242, 235)


def draw_paper_background(img, base=PAPER_BASE, seed=5, vignette=True):
    """A warm, light cream paper-card background: soft warmth in the upper
    area, a faint vignette at the very edges, and fine grain. No flat dead
    void, but never dark/muddy -- stays airy and bright."""
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle([0, 0, CANVAS_W, CANVAS_H], fill=base)

    # soft warm glow near the top where the title sits
    glow = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-200, -500, CANVAS_W + 200, 600], fill=(255, 255, 252, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))

    if vignette:
        vig = Image.new("L", (CANVAS_W, CANVAS_H), 0)
        vd = ImageDraw.Draw(vig)
        vd.rectangle([0, 0, CANVAS_W, CANVAS_H], fill=0)
        vd.ellipse([-380, -380, CANVAS_W + 380, CANVAS_H + 380], fill=26)
        vig = vig.filter(ImageFilter.GaussianBlur(180))
        vig_rgba = Image.merge("RGBA", (Image.new("L", vig.size, 40), Image.new("L", vig.size, 34),
                                         Image.new("L", vig.size, 26), vig))
        img.paste(Image.alpha_composite(img.convert("RGBA"), vig_rgba).convert("RGB"), (0, 0))

    # fine paper grain
    grain = Image.effect_noise((CANVAS_W, CANVAS_H), 22).convert("L")
    grain_rgba = Image.merge("RGBA", (grain, grain, grain, Image.new("L", (CANVAS_W, CANVAS_H), 9)))
    img.paste(Image.alpha_composite(img.convert("RGBA"), grain_rgba).convert("RGB"), (0, 0))
    return img


def draw_background(img, tint=OFFWHITE, blobs=True, seed=7):
    """Soft warm paper background with faint pastel blobs for depth and a
    light grain texture, never a flat dead void behind the content."""
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rectangle([0, 0, CANVAS_W, CANVAS_H], fill=tint)
    if blobs:
        blob_layer = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(blob_layer)
        rng = random.Random(seed)
        colors = [LAVENDER, BLUSH, SAGE, PEACH, POWDER]
        for i in range(5):
            c = colors[i % len(colors)]
            cx = rng.randint(-100, CANVAS_W + 100)
            cy = rng.randint(-100, CANVAS_H + 100)
            r = rng.randint(260, 480)
            bdraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(c[0], c[1], c[2], 30))
        blob_layer = blob_layer.filter(ImageFilter.GaussianBlur(90))
        img.paste(Image.alpha_composite(img.convert("RGBA"), blob_layer).convert("RGB"), (0, 0))
    # faint grain
    grain = Image.effect_noise((CANVAS_W, CANVAS_H), 14).convert("L")
    grain = grain.point(lambda p: 250 + (p - 128) * 0.02)
    grain_rgba = Image.merge("RGBA", (grain, grain, grain, Image.new("L", (CANVAS_W, CANVAS_H), 10)))
    img.paste(Image.alpha_composite(img.convert("RGBA"), grain_rgba).convert("RGB"), (0, 0))
    return img


def rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def drop_shadow(size, radius, blur=30, opacity=70, offset=(0, 18)):
    """Returns an RGBA shadow image the size of the canvas with a rounded
    shadow shape centered per the caller's paste offset handling."""
    w, h = size
    shadow = Image.new("RGBA", (w + blur * 4, h + blur * 4), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([blur * 2, blur * 2, blur * 2 + w, blur * 2 + h], radius=radius, fill=(20, 16, 30, opacity))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    return shadow, blur


def paste_rgba(base, layer, xy):
    base.paste(layer, xy, layer)


# --------------------------------------------------------------- text utils
def text_size(draw, text, f):
    bbox = draw.textbbox((0, 0), text, font=f)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(draw, text, f, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        tw, _ = text_size(draw, trial, f)
        if tw <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered_multiline(img, xy_top_center, text, f, fill, max_width, line_spacing=1.15, stroke_width=0, stroke_fill=None):
    draw = ImageDraw.Draw(img)
    lines = wrap_text(draw, text, f, max_width)
    x, y = xy_top_center
    for line in lines:
        tw, th = text_size(draw, line, f)
        draw.text((x - tw / 2, y), line, font=f, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)
        y += th * line_spacing + 6
    return y


# ---- rich text with **bold** spans, left-aligned wrapped paragraph -------
_TOKEN_RE = re.compile(r"\*\*(.+?)\*\*|(\S+)")


def _tokenize_rich(text):
    tokens = []
    for m in re.finditer(r"\*\*(.+?)\*\*|\S+", text):
        if m.group(1) is not None:
            for w in m.group(1).split():
                tokens.append((w, True))
        else:
            tokens.append((m.group(0), False))
    return tokens


def draw_rich_paragraph(img, xy, text, f_regular, f_bold, fill, max_width, line_spacing=1.3, align="left"):
    draw = ImageDraw.Draw(img)
    tokens = _tokenize_rich(text)
    space_w, _ = text_size(draw, " ", f_regular)
    lines = []
    cur, cur_w = [], 0
    for word, bold in tokens:
        f = f_bold if bold else f_regular
        ww, _ = text_size(draw, word, f)
        add = ww + (space_w if cur else 0)
        if cur_w + add <= max_width or not cur:
            cur.append((word, bold))
            cur_w += add
        else:
            lines.append(cur)
            cur, cur_w = [(word, bold)], ww
    if cur:
        lines.append(cur)

    x0, y = xy
    line_h = text_size(draw, "Ag", f_bold)[1] * line_spacing
    for line in lines:
        widths = [text_size(draw, w, f_bold if b else f_regular)[0] for w, b in line]
        total_w = sum(widths) + space_w * (len(line) - 1)
        if align == "center":
            x = x0 - total_w / 2
        else:
            x = x0
        for (word, bold), ww in zip(line, widths):
            f = f_bold if bold else f_regular
            draw.text((x, y), word, font=f, fill=fill)
            x += ww + space_w
        y += line_h
    return y


# --------------------------------------------------------------- badges ---
def draw_badge(img, center, radius, text, fill_color, text_color=CHARCOAL, font_key="sans_extrabold", font_size=30, border=None):
    d = Image.new("RGBA", (radius * 2 + 20, radius * 2 + 20), (0, 0, 0, 0))
    dd = ImageDraw.Draw(d)
    cx = cy = radius + 10
    dd.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(*fill_color, 255),
               outline=(255, 255, 255, 255), width=6)
    f = font(font_key, font_size)
    lines = wrap_text(dd, text, f, radius * 1.6)
    lh = text_size(dd, "Ag", f)[1] * 1.2
    total_h = lh * len(lines)
    ty = cy - total_h / 2
    for line in lines:
        tw, th = text_size(dd, line, f)
        dd.text((cx - tw / 2, ty), line, font=f, fill=(*text_color, 255))
        ty += lh
    shadow = Image.new("RGBA", d.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=(20, 16, 30, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(12))
    base_pos = (int(center[0] - radius - 10), int(center[1] - radius - 10 + 6))
    paste_rgba(img, shadow, base_pos)
    paste_rgba(img, d, (int(center[0] - radius - 10), int(center[1] - radius - 10)))


# -------------------------------------------------------------- close icon
def draw_close_icon(img, center=(1140, 60), radius=26):
    d = Image.new("RGBA", (radius * 2, radius * 2), (0, 0, 0, 0))
    dd = ImageDraw.Draw(d)
    dd.ellipse([0, 0, radius * 2, radius * 2], fill=(255, 255, 255, 235), outline=(220, 214, 210, 255), width=2)
    pad = radius * 0.55
    dd.line([pad, pad, radius * 2 - pad, radius * 2 - pad], fill=(120, 115, 112, 255), width=4)
    dd.line([radius * 2 - pad, pad, pad, radius * 2 - pad], fill=(120, 115, 112, 255), width=4)
    paste_rgba(img, d, (center[0] - radius, center[1] - radius))


# --------------------------------------------------------- pagination dots
def draw_pagination_dots(img, total=8, current=1, y=1560, active_color=CHARCOAL, inactive_color=(206, 200, 194)):
    dot_r = 7
    gap = 24
    total_w = (total - 1) * gap
    x0 = CANVAS_W / 2 - total_w / 2
    draw = ImageDraw.Draw(img, "RGBA")
    for i in range(total):
        x = x0 + i * gap
        r = dot_r + 3 if (i + 1) == current else dot_r
        color = active_color if (i + 1) == current else inactive_color
        draw.ellipse([x - r, y - r, x + r, y + r], fill=color)


# -------------------------------------------------------------- screenshot
def load_screenshot(name):
    path = os.path.join(SCREENS_DIR, name)
    return Image.open(path).convert("RGB")


def crop_top_left_content(im, content_w_frac=1.0, content_h_frac=1.0):
    w, h = im.size
    return im.crop((0, 0, int(w * content_w_frac), int(h * content_h_frac)))


def device_frame(screenshot, box, bezel_color=WHITE, bezel_width=18, radius=28,
                  crop_box_frac=None, style="tablet"):
    """Draws a simple device bezel (Pillow-drawn, not a sourced mockup image)
    with the screenshot inside, cropped to crop_box_frac (l,t,r,b in 0..1 of
    the source image) and scaled to fill. Returns an RGBA layer sized to box
    (x0,y0,x1,y1) ready to paste onto the canvas, plus its own drop shadow
    baked in below it (so callers just paste_rgba at (x0 - pad, y0 - pad)).
    """
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    inner = (x0 + bezel_width, y0 + bezel_width, x1 - bezel_width, y1 - bezel_width)
    iw, ih = inner[2] - inner[0], inner[3] - inner[1]

    sw, sh = screenshot.size
    if crop_box_frac:
        l, t, r, b = crop_box_frac
        crop = screenshot.crop((int(l * sw), int(t * sh), int(r * sw), int(b * sh)))
    else:
        crop = screenshot
    cw, ch = crop.size
    # scale to cover inner box, then center-crop
    scale = max(iw / cw, ih / ch)
    new_size = (max(1, int(cw * scale)), max(1, int(ch * scale)))
    crop = crop.resize(new_size, Image.LANCZOS)
    cw, ch = crop.size
    left = max(0, (cw - iw) / 2)
    top = 0  # keep top of the sheet (title/content) visible rather than centering vertically
    crop = crop.crop((int(left), int(top), int(left + iw), int(top + ih)))

    pad = 60
    layer = Image.new("RGBA", (int(w + pad * 2), int(h + pad * 2)), (0, 0, 0, 0))
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([pad, pad + 14, pad + w, pad + h + 14], radius=radius + bezel_width, fill=(20, 16, 30, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    layer = Image.alpha_composite(layer, shadow)

    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([pad, pad, pad + w, pad + h], radius=radius + bezel_width, fill=(*bezel_color, 255),
                          outline=(224, 219, 213, 255), width=2)

    mask = Image.new("L", (int(iw), int(ih)), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, iw, ih], radius=radius, fill=255)
    layer.paste(crop, (int(pad + bezel_width), int(pad + bezel_width)), mask)

    if style == "laptop":
        base_h = 22
        ld.rounded_rectangle([pad - 40, pad + h, pad + w + 40, pad + h + base_h], radius=10,
                              fill=(236, 231, 224, 255), outline=(224, 219, 213, 255), width=2)

    return layer, pad


def paste_device(img, screenshot_name, box, bezel_color=WHITE, style="tablet", crop_box_frac=None, bezel_width=18):
    screenshot = load_screenshot(screenshot_name)
    layer, pad = device_frame(screenshot, box, bezel_color=bezel_color, style=style,
                               crop_box_frac=crop_box_frac, bezel_width=bezel_width)
    x0, y0, x1, y1 = box
    paste_rgba(img, layer, (int(x0 - pad), int(y0 - pad)))
    return box  # callers use this box (in canvas coords) for callout targets


def _cover_crop(crop, target_w, target_h):
    target_w, target_h = int(target_w), int(target_h)
    cw, ch = crop.size
    scale = max(target_w / cw, target_h / ch)
    new_size = (max(1, int(cw * scale)), max(1, int(ch * scale)))
    crop = crop.resize(new_size, Image.LANCZOS)
    cw, ch = crop.size
    left = max(0, int((cw - target_w) / 2))
    return crop.crop((left, 0, left + target_w, target_h))


def laptop_frame(screenshot, box, crop_box_frac=None, bezel=16, radius=16,
                  bezel_color=(28, 27, 26), deck_color=(214, 209, 201)):
    """A simplified, clearly-readable laptop silhouette: dark screen bezel
    with a small camera dot, and a keyboard deck below. Hand-drawn with
    Pillow, not a sourced device mockup."""
    x0, y0, x1, y1 = box
    screen_w = x1 - x0
    screen_h = y1 - y0
    deck_h = max(20, screen_w * 0.028)
    pad = 70

    total_h = screen_h + deck_h
    layer = Image.new("RGBA", (int(screen_w + pad * 2), int(total_h + pad * 2)), (0, 0, 0, 0))

    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([pad, pad + 20, pad + screen_w, pad + total_h + 20], radius=radius + 10,
                          fill=(15, 12, 22, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(32))
    layer = Image.alpha_composite(layer, shadow)

    ld = ImageDraw.Draw(layer)
    # screen bezel
    ld.rounded_rectangle([pad, pad, pad + screen_w, pad + screen_h], radius=radius, fill=(*bezel_color, 255))
    cam_r = 2.4
    ld.ellipse([pad + screen_w / 2 - cam_r, pad + bezel * 0.42, pad + screen_w / 2 + cam_r, pad + bezel * 0.42 + cam_r * 2],
               fill=(70, 68, 66, 255))

    inner = (pad + bezel, pad + bezel, pad + screen_w - bezel, pad + screen_h - bezel)
    iw, ih = inner[2] - inner[0], inner[3] - inner[1]
    sw, sh = screenshot.size
    l, t, r, b = crop_box_frac if crop_box_frac else (0, 0, 1, 1)
    crop = screenshot.crop((int(l * sw), int(t * sh), int(r * sw), int(b * sh)))
    crop = _cover_crop(crop, iw, ih)
    mask = Image.new("L", (int(iw), int(ih)), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, iw, ih], radius=max(2, radius - bezel * 0.4), fill=255)
    layer.paste(crop, (int(inner[0]), int(inner[1])), mask)

    # keyboard deck (trapezoid-ish base narrower look via two-tone)
    deck_top = pad + screen_h
    overhang = screen_w * 0.045
    deck_pts = [
        (pad - overhang * 0.3, deck_top),
        (pad + screen_w + overhang * 0.3, deck_top),
        (pad + screen_w + overhang, deck_top + deck_h),
        (pad - overhang, deck_top + deck_h),
    ]
    ld.polygon(deck_pts, fill=(*deck_color, 255))
    ld.rounded_rectangle([pad - overhang, deck_top + deck_h - 10, pad + screen_w + overhang, deck_top + deck_h],
                          radius=8, fill=(*deck_color, 255))
    notch_w = screen_w * 0.09
    ld.rounded_rectangle([pad + screen_w / 2 - notch_w / 2, deck_top + 2, pad + screen_w / 2 + notch_w / 2, deck_top + 6],
                          radius=3, fill=(190, 184, 175, 255))

    return layer, pad, (screen_w, screen_h), bezel


def paste_laptop(img, screenshot_name, box, crop_box_frac=None, bezel=16, radius=16,
                  bezel_color=(28, 27, 26), deck_color=(214, 209, 201)):
    screenshot = load_screenshot(screenshot_name)
    layer, pad, (sw, sh), bw = laptop_frame(screenshot, box, crop_box_frac, bezel, radius, bezel_color, deck_color)
    x0, y0, x1, y1 = box
    paste_rgba(img, layer, (int(x0 - pad), int(y0 - pad)))
    return {"screen_box": box, "bezel": bw, "crop_box_frac": crop_box_frac, "source_size": screenshot.size}


def tablet_frame(screenshot, box, crop_box_frac=None, bezel=14, radius=26, bezel_color=WHITE):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    pad = 60
    layer = Image.new("RGBA", (int(w + pad * 2), int(h + pad * 2)), (0, 0, 0, 0))
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([pad, pad + 16, pad + w, pad + h + 16], radius=radius + bezel, fill=(15, 12, 22, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))
    layer = Image.alpha_composite(layer, shadow)

    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([pad, pad, pad + w, pad + h], radius=radius + bezel, fill=(*bezel_color, 255),
                          outline=(210, 204, 196, 255), width=2)
    inner = (pad + bezel, pad + bezel, pad + w - bezel, pad + h - bezel)
    iw, ih = inner[2] - inner[0], inner[3] - inner[1]
    sw, sh = screenshot.size
    l, t, r, b = crop_box_frac if crop_box_frac else (0, 0, 1, 1)
    crop = screenshot.crop((int(l * sw), int(t * sh), int(r * sw), int(b * sh)))
    crop = _cover_crop(crop, iw, ih)
    mask = Image.new("L", (int(iw), int(ih)), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, iw, ih], radius=radius, fill=255)
    layer.paste(crop, (int(inner[0]), int(inner[1])), mask)
    return layer, pad


def paste_tablet(img, screenshot_name, box, crop_box_frac=None, bezel=14, radius=26, bezel_color=WHITE):
    screenshot = load_screenshot(screenshot_name)
    layer, pad = tablet_frame(screenshot, box, crop_box_frac, bezel, radius, bezel_color)
    x0, y0, x1, y1 = box
    paste_rgba(img, layer, (int(x0 - pad), int(y0 - pad)))
    return {"screen_box": box, "bezel": bezel, "crop_box_frac": crop_box_frac, "source_size": screenshot.size}


def frame_target(frame_meta, frac_xy):
    """Maps a fractional point of the ORIGINAL screenshot to canvas coords
    for a laptop/tablet frame produced above (screen area only, cover-crop
    centered horizontally, top-anchored vertically)."""
    return frac_to_canvas(frame_meta["screen_box"], frame_meta["bezel"], frame_meta["crop_box_frac"],
                           frame_meta["source_size"], frac_xy)


# --------------------------------------------------------- pill / chip label
def pill_label(img, center, text, fill_color, text_color=CHARCOAL, font_size=24, pad_x=26, pad_y=14,
               font_key="sans_extrabold"):
    draw = ImageDraw.Draw(img, "RGBA")
    f = font(font_key, font_size)
    tw, th = text_size(draw, text, f)
    w, h = tw + pad_x * 2, th + pad_y * 2
    x0, y0 = center[0] - w / 2, center[1] - h / 2

    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([x0, y0 + 5, x0 + w, y0 + h + 5], radius=h / 2, fill=(15, 12, 22, 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img.paste(Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB"), (0, 0))

    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=h / 2, fill=fill_color)
    draw.text((x0 + pad_x, y0 + pad_y - 2), text, font=f, fill=text_color)
    return (x0, y0, x0 + w, y0 + h)


# --------------------------------------------------------- delicate callout
def thin_callout(img, label_xy, text, target_xy, align="left", font_size=19, max_width=260,
                  label_fill=(255, 255, 255, 235), text_color=CHARCOAL, line_color=(140, 134, 128)):
    """A small, light label (no heavy border/shadow) connected to target_xy
    by a thin line and a small dot -- the delicate style used for detail
    call-outs, as opposed to the bold pill_label."""
    draw = ImageDraw.Draw(img, "RGBA")
    f_reg = font("sans_semibold", font_size)
    f_bold = font("sans_extrabold", font_size)

    tokens = _tokenize_rich(text)
    space_w, _ = text_size(draw, " ", f_reg)
    lines, cur, cur_w = [], [], 0
    for word, bold in tokens:
        f = f_bold if bold else f_reg
        ww, _ = text_size(draw, word, f)
        add = ww + (space_w if cur else 0)
        if cur_w + add <= max_width or not cur:
            cur.append((word, bold)); cur_w += add
        else:
            lines.append(cur); cur, cur_w = [(word, bold)], ww
    if cur:
        lines.append(cur)

    line_h = text_size(draw, "Ag", f_bold)[1] * 1.3
    box_w = max(text_size(draw, " ".join(w for w, b in l), f_bold)[0] for l in lines)
    box_h = line_h * len(lines)
    lx, ly = label_xy
    if align == "right":
        lx = lx - box_w

    pad = 4
    draw.rounded_rectangle([lx - pad, ly - pad, lx + box_w + pad, ly + box_h + pad], radius=8, fill=label_fill)

    y = ly
    for line in lines:
        widths = [text_size(draw, w, f_bold if b else f_reg)[0] for w, b in line]
        x = lx if align == "left" else lx + box_w - sum(widths) - space_w * (len(line) - 1)
        for (word, bold), ww in zip(line, widths):
            draw.text((x, y), word, font=f_bold if bold else f_reg, fill=text_color)
            x += ww + space_w
        y += line_h

    label_edge = (lx + box_w + pad, ly + box_h / 2) if align == "left" else (lx - pad, ly + box_h / 2)
    draw.line([label_edge, target_xy], fill=(*line_color, 230), width=2)
    draw.ellipse([label_edge[0] - 3, label_edge[1] - 3, label_edge[0] + 3, label_edge[1] + 3], fill=line_color)
    r = 5
    draw.ellipse([target_xy[0] - r, target_xy[1] - r, target_xy[0] + r, target_xy[1] + r],
                 fill=(255, 255, 255, 255), outline=line_color, width=2)
    return (lx, ly, lx + box_w, ly + box_h)


# ------------------------------------------------------------- small icons
def icon_play(img, center, r, ring=(30, 30, 30), tri=WHITE):
    d = Image.new("RGBA", (r * 2 + 8, r * 2 + 8), (0, 0, 0, 0))
    dd = ImageDraw.Draw(d)
    cx = cy = r + 4
    dd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*ring, 255))
    s = r * 0.5
    dd.polygon([(cx - s * 0.5, cy - s), (cx - s * 0.5, cy + s), (cx + s, cy)], fill=(*tri, 255))
    paste_rgba(img, d, (int(center[0] - r - 4), int(center[1] - r - 4)))


def icon_download(img, center, r, color=CHARCOAL):
    d = Image.new("RGBA", (r * 2 + 8, r * 2 + 8), (0, 0, 0, 0))
    dd = ImageDraw.Draw(d)
    cx = cy = r + 4
    dd.line([cx, cy - r * 0.7, cx, cy + r * 0.15], fill=(*color, 255), width=max(3, int(r * 0.18)))
    dd.polygon([(cx - r * 0.4, cy - r * 0.15), (cx + r * 0.4, cy - r * 0.15), (cx, cy + r * 0.35)], fill=(*color, 255))
    dd.arc([cx - r * 0.85, cy - r * 0.1, cx + r * 0.85, cy + r * 0.95], start=20, end=160, fill=(*color, 255),
           width=max(3, int(r * 0.16)))
    paste_rgba(img, d, (int(center[0] - r - 4), int(center[1] - r - 4)))


def icon_sync(img, center, r, color=CHARCOAL):
    d = Image.new("RGBA", (r * 2 + 8, r * 2 + 8), (0, 0, 0, 0))
    dd = ImageDraw.Draw(d)
    cx = cy = r + 4
    w = max(3, int(r * 0.18))
    dd.arc([cx - r * 0.75, cy - r * 0.75, cx + r * 0.75, cy + r * 0.75], start=-150, end=120, fill=(*color, 255), width=w)
    dd.arc([cx - r * 0.75, cy - r * 0.75, cx + r * 0.75, cy + r * 0.75], start=30, end=300, fill=(*color, 255), width=w)
    import math as _m
    a1 = _m.radians(120)
    p1 = (cx + r * 0.75 * _m.cos(a1), cy + r * 0.75 * _m.sin(a1))
    dd.polygon([(p1[0] - 8, p1[1] - 2), (p1[0] + 9, p1[1] - 6), (p1[0] + 2, p1[1] + 10)], fill=(*color, 255))
    a2 = _m.radians(300)
    p2 = (cx + r * 0.75 * _m.cos(a2), cy + r * 0.75 * _m.sin(a2))
    dd.polygon([(p2[0] + 8, p2[1] + 2), (p2[0] - 9, p2[1] + 6), (p2[0] - 2, p2[1] - 10)], fill=(*color, 255))
    paste_rgba(img, d, (int(center[0] - r - 4), int(center[1] - r - 4)))


def icon_stars_row(img, center, r):
    draw = ImageDraw.Draw(img, "RGBA")
    n = 5
    sr = r * 0.36
    spacing = sr * 2.15
    x0 = center[0] - spacing * (n - 1) / 2
    for i in range(n):
        icon_star(draw, (x0 + i * spacing, center[1]), sr)


def icon_star(draw, center, r, fill=(232, 178, 60)):
    import math as _m
    pts = []
    for i in range(10):
        ang = _m.pi / 2 + i * _m.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((center[0] + rr * _m.cos(ang), center[1] - rr * _m.sin(ang)))
    draw.polygon(pts, fill=fill)


def icon_funnel(img, center, r, color=CHARCOAL):
    d = Image.new("RGBA", (r * 2 + 8, r * 2 + 8), (0, 0, 0, 0))
    dd = ImageDraw.Draw(d)
    cx = cy = r + 4
    dd.polygon([(cx - r * 0.85, cy - r * 0.6), (cx + r * 0.85, cy - r * 0.6),
                (cx + r * 0.18, cy + r * 0.15), (cx + r * 0.18, cy + r * 0.75),
                (cx - r * 0.18, cy + r * 0.75), (cx - r * 0.18, cy + r * 0.15)], fill=(*color, 255))
    paste_rgba(img, d, (int(center[0] - r - 4), int(center[1] - r - 4)))


def icon_flag_rainbow(img, box):
    x0, y0, x1, y1 = box
    colors = [(230, 70, 60), (240, 145, 40), (245, 205, 55), (95, 170, 90), (70, 130, 200), (130, 90, 170)]
    h = (y1 - y0) / len(colors)
    draw = ImageDraw.Draw(img)
    for i, c in enumerate(colors):
        draw.rectangle([x0, y0 + i * h, x1, y0 + (i + 1) * h + 1], fill=c)
    draw.line([x0, y0, x0, y1], fill=(60, 60, 60), width=4)


def icon_spreadsheet(img, center, r, color=(52, 133, 76)):
    x0, y0, x1, y1 = center[0] - r, center[1] - r, center[0] + r, center[1] + r
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle([x0, y0, x1, y1], radius=(x1 - x0) * 0.18, fill=(*color, 255))
    m = (x1 - x0) * 0.18
    draw.rectangle([x0 + m, y0 + m, x1 - m, y1 - m], fill=WHITE)
    n = 3
    gw = (x1 - x0 - 2 * m) / n
    gh = (y1 - y0 - 2 * m) / n
    for i in range(1, n):
        draw.line([x0 + m + i * gw, y0 + m, x0 + m + i * gw, y1 - m], fill=(*color, 255), width=3)
        draw.line([x0 + m, y0 + m + i * gh, x1 - m, y0 + m + i * gh], fill=(*color, 255), width=3)


# ------------------------------------------------------------- trust bar
def trust_bar(img, box, segments, bg=(255, 255, 255, 245), divider=(222, 216, 208)):
    """segments: list of (draw_icon_fn, label) where draw_icon_fn(img, center, r).
    Icon centered above a centered label -- avoids any icon/text collision
    regardless of label length."""
    x0, y0, x1, y1 = box
    draw = ImageDraw.Draw(img, "RGBA")
    rounded_rect(draw, [x0, y0, x1, y1], radius=18, fill=bg, outline=(224, 219, 213, 255), width=1)
    n = len(segments)
    seg_w = (x1 - x0) / n
    f = font("sans_bold", 18)
    icon_r = 20
    for i, (icon_fn, label) in enumerate(segments):
        cx = x0 + seg_w * i + seg_w / 2
        icon_cy = y0 + 30
        icon_fn(img, (cx, icon_cy), icon_r)
        draw = ImageDraw.Draw(img, "RGBA")
        lines = wrap_text(draw, label, f, seg_w - 30)
        lh = text_size(draw, "Ag", f)[1] * 1.2
        ty = icon_cy + icon_r + 12
        for line in lines:
            tw, th = text_size(draw, line, f)
            draw.text((cx - tw / 2, ty), line, font=f, fill=CHARCOAL)
            ty += lh
        if i > 0:
            draw.line([x0 + seg_w * i, y0 + 14, x0 + seg_w * i, y1 - 14], fill=divider, width=2)


def frac_to_canvas(box, bezel_width, crop_box_frac, source_size, frac_xy):
    """Maps a fractional point (fx,fy) of the ORIGINAL screenshot into canvas
    pixel coordinates, replicating device_frame's crop/scale/center logic, so
    callout connector lines land on the right spot inside a device frame."""
    x0, y0, x1, y1 = box
    iw, ih = (x1 - x0) - 2 * bezel_width, (y1 - y0) - 2 * bezel_width
    sw, sh = source_size
    l, t, r, b = crop_box_frac if crop_box_frac else (0, 0, 1, 1)
    crop_l, crop_t = l * sw, t * sh
    cw, ch = (r - l) * sw, (b - t) * sh
    scale = max(iw / cw, ih / ch)
    left_offset = max(0, (cw * scale - iw) / 2)
    fx, fy = frac_xy
    px = fx * sw - crop_l
    py = fy * sh - crop_t
    sx = px * scale - left_offset
    sy = py * scale
    sx = min(max(sx, 0), iw)
    sy = min(max(sy, 0), ih)
    return (x0 + bezel_width + sx, y0 + bezel_width + sy)


# ------------------------------------------------------------------ callouts
def draw_callout(img, bubble_box, text, target_xy, dot_color=CHARCOAL,
                  bubble_fill=WHITE, border_color=(224, 219, 213), text_color=CHARCOAL,
                  font_size=25, connector_from="auto"):
    """bubble_box = (x0,y0,x1,y1) rounded rect on the canvas. Draws wrapped
    bold-aware text inside, a connector line from the bubble edge to
    target_xy on the canvas, and a solid dot at the target."""
    x0, y0, x1, y1 = bubble_box
    draw = ImageDraw.Draw(img, "RGBA")

    # shadow
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([x0, y0 + 6, x1, y1 + 6], radius=22, fill=(20, 16, 30, 55))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    img.paste(Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(img, "RGBA")

    rounded_rect(draw, [x0, y0, x1, y1], radius=22, fill=bubble_fill, outline=border_color, width=2)

    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    if connector_from == "auto":
        connector_from = "right" if target_xy[0] > cx else "left"
    if connector_from == "right":
        start = (x1, cy)
    elif connector_from == "left":
        start = (x0, cy)
    elif connector_from == "bottom":
        start = (cx, y1)
    else:
        start = (cx, y0)

    draw.line([start, target_xy], fill=(*CHARCOAL, 220), width=4)
    r = 8
    draw.ellipse([start[0] - 5, start[1] - 5, start[0] + 5, start[1] + 5], fill=CHARCOAL)
    draw.ellipse([target_xy[0] - r, target_xy[1] - r, target_xy[0] + r, target_xy[1] + r], fill=CHARCOAL,
                  outline=WHITE, width=3)

    pad_x, pad_y = 22, 18
    draw_rich_paragraph(img, (x0 + pad_x, y0 + pad_y), text, font("sans_semibold", font_size),
                         font("sans_extrabold", font_size), text_color, (x1 - x0) - pad_x * 2, line_spacing=1.35)


def eyebrow_bar(img, text, top=40, icon_fn=None, bg=(255, 255, 255, 210), height=54):
    draw = ImageDraw.Draw(img, "RGBA")
    f = font("sans_bold", 19)
    tw, th = text_size(draw, text, f)
    icon_gap = 70 if icon_fn else 0
    w = tw + icon_gap + 60
    x0 = CANVAS_W / 2 - w / 2
    y0 = top
    draw.rounded_rectangle([x0, y0, x0 + w, y0 + height], radius=height / 2, fill=bg,
                            outline=(224, 219, 213, 255), width=1)
    if icon_fn:
        icon_fn(img, (x0 + height / 2 + 6, y0 + height / 2), height / 2 - 6)
    draw = ImageDraw.Draw(img, "RGBA")
    draw.text((x0 + icon_gap + 20, y0 + height / 2 - th / 2 - 2), text, font=f, fill=(60, 58, 56))
    return y0 + height


def accent_title(img, script_word, bold_title, top=110, script_size=54, title_size=88,
                  title_color=CHARCOAL, max_width=1080):
    draw = ImageDraw.Draw(img)
    f_script = font("display_italic", script_size)
    tw, th = text_size(draw, script_word, f_script)
    draw.text((CANVAS_W / 2 - tw / 2, top), script_word, font=f_script, fill=(90, 86, 82))
    y = top + th * 1.25
    f_title = font("display_black", title_size)
    y = draw_centered_multiline(img, (CANVAS_W / 2, y), bold_title, f_title, title_color, max_width, line_spacing=1.05)
    return y


def title_block(img, title, subtitle=None, top=64, title_size=100, subtitle_size=30,
                 title_color=CHARCOAL, subtitle_color=MUTED_GREY, max_width=1080, gap=26):
    f_title = font("display_black", title_size)
    y = draw_centered_multiline(img, (CANVAS_W / 2, top), title, f_title, title_color, max_width, line_spacing=1.15)
    if subtitle:
        f_sub = font("sans_bold", subtitle_size)
        draw = ImageDraw.Draw(img)
        sub = subtitle.upper()
        y += gap
        draw_centered_multiline(img, (CANVAS_W / 2, y), sub, f_sub, subtitle_color, max_width, line_spacing=1.2)
        y += text_size(draw, "Ag", f_sub)[1] * 1.2 + 10
    return y


def draw_bell_icon(img, center, size, color=CHARCOAL):
    d = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
    dd = ImageDraw.Draw(d)
    cx, cy = size, size * 0.85
    r = size * 0.6
    dd.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(*color, 255))
    dd.rectangle([cx - r, cy, cx + r, cy + r * 0.55], fill=(*color, 255))
    dd.polygon([(cx - r * 1.15, cy + r * 0.55), (cx + r * 1.15, cy + r * 0.55),
                (cx + r * 0.85, cy + r * 0.78), (cx - r * 0.85, cy + r * 0.78)], fill=(*color, 255))
    dd.ellipse([cx - r * 0.22, cy + r * 0.78, cx + r * 0.22, cy + r * 1.22], fill=(*color, 255))
    paste_rgba(img, d, (int(center[0] - size), int(center[1] - size)))


def save(img, name):
    path = os.path.join(OUT_DIR, name)
    img.save(path, "PNG", optimize=True)
    print("Saved", path)
    return path
