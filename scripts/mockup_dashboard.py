#!/usr/bin/env python3
"""Render a faithful mockup of the Calm Money Reset Dashboard tab.

Doubles as (a) visual QA for the workbook layout and (b) the Etsy hero image:
a Pinterest-style pastel flat lay of the Dashboard on a soft device panel.
Output: etsy-listing-images/calm-dashboard-mockup.png
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT_DIR = os.path.join(HERE, "..", "etsy-listing-images")
os.makedirs(OUT_DIR, exist_ok=True)

# House of Calm palette (RGB)
BLUSH = (244, 201, 206)
SKY = (201, 221, 232)
SAGE = (200, 216, 196)
BUTTER = (245, 227, 179)
LAV = (217, 208, 232)
CREAM = (251, 246, 239)
CHARCOAL = (58, 58, 58)
MUTED = (140, 134, 129)
WHITE = (255, 255, 255)
BLUSH_S = (251, 231, 233)
SKY_S = (233, 242, 247)
SAGE_S = (231, 239, 228)
BUTTER_S = (251, 242, 218)
LAV_S = (240, 235, 247)
SAGEBAR = (123, 168, 122)


def F(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "PlayfairDisplay-Bold.ttf"
SERIF_BLACK = "PlayfairDisplay-Black.ttf"
SANS = "Poppins-Regular.ttf"
SANS_SB = "Poppins-SemiBold.ttf"
SANS_B = "Poppins-Bold.ttf"


def rrect(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)


def shadow_panel(base, box, r, fill, blur=34, dy=18, alpha=60):
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((x0, y0 + dy, x1, y1 + dy), radius=r,
                         fill=(120, 110, 100, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(sh)
    ImageDraw.Draw(base).rounded_rectangle(box, radius=r, fill=fill)


def center_text(draw, cx, y, text, font, fill, anchor="mm"):
    draw.text((cx, y), text, font=font, fill=fill, anchor=anchor)


def build():
    W, H = 1200, 1600
    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)

    # soft top wash
    wash = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(wash).rectangle((0, 0, W, 520), fill=BLUSH_S + (255,))
    wash = wash.filter(ImageFilter.GaussianBlur(120))
    img.alpha_composite(wash)

    # header kicker + title
    center_text(d, W // 2, 96, "HOUSE OF CALM", F(SANS_SB, 26), MUTED)
    center_text(d, W // 2, 158, "Calm Money Reset", F(SERIF_BLACK, 74), CHARCOAL)
    center_text(d, W // 2, 222,
                "an ADHD-friendly budget & debt tracker", F(SANS, 30), MUTED)

    # device panel
    px0, py0, px1, py1 = 96, 300, W - 96, 1360
    shadow_panel(img, (px0, py0, px1, py1), 40, WHITE + (255,))
    d = ImageDraw.Draw(img)

    pad = 44
    ix0 = px0 + pad
    ix1 = px1 - pad

    # banner inside
    by0 = py0 + 40
    rrect(d, (ix0, by0, ix1, by0 + 92), 20, BLUSH + (255,))
    d.text((ix0 + 30, by0 + 46), "Calm Money Reset  ·  Dashboard",
           font=F(SERIF, 40), fill=CHARCOAL, anchor="lm")
    d.text((ix0 + 4, by0 + 128),
           "One calm glance. No dense charts, no red flags,",
           font=F(SANS, 24), fill=MUTED, anchor="lm")
    d.text((ix0 + 4, by0 + 160),
           "just what you need to decide right now.",
           font=F(SANS, 24), fill=MUTED, anchor="lm")

    # three cards
    cy0 = by0 + 200
    cy1 = cy0 + 200
    gap = 28
    cw = (ix1 - ix0 - 2 * gap) / 3
    cards = [
        ("SAFE TO SPEND THIS WEEK", "$210", SAGE_S, SAGE),
        ("DAYS UNTIL NEXT BILL", "6 days", SKY_S, SKY),
        ("LOW-SPEND STREAK", "7 days", BLUSH_S, BLUSH),
    ]
    for i, (lab, val, fill, edge) in enumerate(cards):
        x0 = ix0 + i * (cw + gap)
        x1 = x0 + cw
        rrect(d, (x0, cy0, x1, cy1), 22, fill + (255,))
        d.rounded_rectangle((x0, cy0, x1, cy1), radius=22, outline=edge + (255,),
                            width=2)
        cx = (x0 + x1) / 2
        # wrap label to 2 lines
        words = lab.split(" ")
        mid = len(words) // 2 + (len(words) % 2)
        l1 = " ".join(words[:mid])
        l2 = " ".join(words[mid:])
        center_text(d, cx, cy0 + 40, l1, F(SANS_SB, 19), MUTED)
        center_text(d, cx, cy0 + 66, l2, F(SANS_SB, 19), MUTED)
        center_text(d, cx, cy0 + 132, val, F(SERIF_BLACK, 52), CHARCOAL)

    # progress section
    sy = cy1 + 46
    rrect(d, (ix0, sy, ix1, sy + 50), 14, SAGE + (255,))
    d.text((ix0 + 24, sy + 25), "Your progress", font=F(SANS_B, 26),
           fill=CHARCOAL, anchor="lm")

    def bar(y, name, pct):
        d.text((ix0 + 6, y + 22), name, font=F(SANS_SB, 24), fill=CHARCOAL,
               anchor="lm")
        bx0 = ix0 + 300
        bx1 = ix1 - 120
        rrect(d, (bx0, y, bx1, y + 44), 22, (236, 232, 224, 255))
        fillw = bx0 + (bx1 - bx0) * pct
        if fillw > bx0 + 44:
            rrect(d, (bx0, y, fillw, y + 44), 22, SAGEBAR + (255,))
        d.text((ix1, y + 22), f"{int(pct*100)}%", font=F(SANS_B, 28),
               fill=CHARCOAL, anchor="rm")

    bar(sy + 78, "Debt paid off", 0.42)
    bar(sy + 150, "Savings goal", 0.68)

    # at-a-glance strip
    gy = sy + 232
    rrect(d, (ix0, gy, ix1, gy + 50), 14, SKY + (255,))
    d.text((ix0 + 24, gy + 25), "This month, at a glance", font=F(SANS_B, 26),
           fill=CHARCOAL, anchor="lm")
    sy2 = gy + 70
    sy3 = sy2 + 150
    stats = [("Income", "$3,200", SAGE_S), ("Spent", "$2,140", BLUSH_S),
             ("Left to spend", "$1,060", BUTTER_S)]
    for i, (lab, val, fill) in enumerate(stats):
        x0 = ix0 + i * (cw + gap)
        x1 = x0 + cw
        rrect(d, (x0, sy2, x1, sy3), 20, fill + (255,))
        cx = (x0 + x1) / 2
        center_text(d, cx, sy2 + 40, lab.upper(), F(SANS_SB, 20), MUTED)
        center_text(d, cx, sy2 + 96, val, F(SERIF_BLACK, 40), CHARCOAL)

    # affirmation
    ay = sy3 + 30
    rrect(d, (ix0, ay, ix1, ay + 96), 18, LAV_S + (255,))
    center_text(d, (ix0 + ix1) / 2, ay + 36,
                "This isn't about restriction. It's about awareness,",
                F(SANS, 24), CHARCOAL)
    center_text(d, (ix0 + ix1) / 2, ay + 66,
                "and you're already here, paying attention. That counts.",
                F(SANS, 24), CHARCOAL)

    # footer tag
    center_text(d, W // 2, 1440,
                "Google Sheets + Excel  ·  shame-free  ·  low-overwhelm",
                F(SANS_SB, 26), MUTED)
    center_text(d, W // 2, 1500,
                "12 gentle tabs to plan, notice, and reset",
                F(SANS, 26), MUTED)

    out = os.path.join(OUT_DIR, "calm-dashboard-mockup.png")
    img.convert("RGB").save(out, "PNG")
    print("Saved", os.path.abspath(out))


if __name__ == "__main__":
    build()
