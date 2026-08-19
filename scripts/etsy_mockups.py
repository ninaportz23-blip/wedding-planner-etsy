#!/usr/bin/env python3
"""Filled-in 2000x2000 Etsy listing mockups for Calm Money Reset.

Pinterest-style pastel flat-lay squares showing the tracker with realistic
example data. Output: etsy-listing-images/mock_*.png
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT_DIR = os.path.join(HERE, "..", "etsy-listing-images")
os.makedirs(OUT_DIR, exist_ok=True)

S = 2000  # square canvas

BLUSH = (244, 201, 206); SKY = (201, 221, 232); SAGE = (200, 216, 196)
BUTTER = (245, 227, 179); LAV = (217, 208, 232); CREAM = (251, 246, 239)
CHARCOAL = (58, 58, 58); MUTED = (140, 134, 129); WHITE = (255, 255, 255)
BLUSH_S = (251, 231, 233); SKY_S = (233, 242, 247); SAGE_S = (231, 239, 228)
BUTTER_S = (251, 242, 218); LAV_S = (240, 235, 247); SAGEBAR = (123, 168, 122)
LINE = (233, 227, 218)

SERIF = "PlayfairDisplay-Bold.ttf"; SERIF_BLACK = "PlayfairDisplay-Black.ttf"
SANS = "Poppins-Regular.ttf"; SANS_SB = "Poppins-SemiBold.ttf"; SANS_B = "Poppins-Bold.ttf"
_fc = {}


def F(name, size):
    k = (name, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _fc[k]


def rr(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def shadow(img, box, r, fill, blur=32, dy=16, alpha=38):
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        (box[0] + 10, box[1] + dy, box[2] - 10, box[3] + dy), radius=r,
        fill=(150, 140, 128, alpha))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(img).rounded_rectangle(box, radius=r, fill=fill)


def ctext(d, cx, y, t, f, fill, anchor="mm"):
    d.text((cx, y), t, font=f, fill=fill, anchor=anchor)


def check(d, cx, cy, size, color, width=9):
    d.line([(cx - size * 0.55, cy + size * 0.05),
            (cx - size * 0.12, cy + size * 0.5),
            (cx + size * 0.6, cy - size * 0.5)],
           fill=color, width=width, joint="curve")


def base(wash=BLUSH_S):
    # smooth vertical gradient from a soft pastel tint (top) to cream (bottom)
    top = tuple(int(wash[i] * 0.55 + 255 * 0.45) for i in range(3))
    img = Image.new("RGB", (S, S), CREAM)
    grad = Image.new("RGB", (1, S))
    for y in range(S):
        t = (y / S) ** 0.9
        grad.putpixel((0, y), tuple(int(top[i] + (CREAM[i] - top[i]) * t)
                                    for i in range(3)))
    img.paste(grad.resize((S, S)), (0, 0))
    return img.convert("RGBA")


def header(img, title, tagline, kicker="HOUSE OF CALM"):
    d = ImageDraw.Draw(img)
    ctext(d, S // 2, 150, kicker, F(SANS_SB, 40), MUTED)
    ctext(d, S // 2, 250, title, F(SERIF_BLACK, 120), CHARCOAL)
    ctext(d, S // 2, 355, tagline, F(SANS, 44), MUTED)


def footer(img, line="Google Sheets + Excel  ·  shame-free  ·  low-overwhelm"):
    d = ImageDraw.Draw(img)
    ctext(d, S // 2, S - 90, line, F(SANS_SB, 40), MUTED)


def panel(img, box, r=46):
    shadow(img, box, r, WHITE + (255,))


def banner(d, box, text, fill=BLUSH, size=52):
    rr(d, box, 22, fill=fill + (255,))
    d.text((box[0] + 40, (box[1] + box[3]) // 2), text, font=F(SERIF, size),
           fill=CHARCOAL, anchor="lm")


def table(d, x0, y0, x1, headers, rows, colw, rowh=64, hfill=CHARCOAL,
          hcolor=WHITE, band=(CREAM, SAGE_S)):
    # header
    d.rounded_rectangle((x0, y0, x1, y0 + rowh), radius=12, fill=hfill + (255,))
    cx = x0 + 20
    for h, w in zip(headers, colw):
        d.text((cx, y0 + rowh // 2), h, font=F(SANS_B, 26), fill=hcolor, anchor="lm")
        cx += w
    y = y0 + rowh
    for i, row in enumerate(rows):
        f = band[i % 2]
        d.rectangle((x0, y, x1, y + rowh), fill=f + (255,))
        cx = x0 + 20
        for val, w in zip(row, colw):
            d.text((cx, y + rowh // 2), val, font=F(SANS, 26), fill=CHARCOAL,
                   anchor="lm")
            cx += w
        y += rowh
    return y


def card(d, box, label, value, fill, edge, vsize=88):
    rr(d, box, 24, fill=fill + (255,), outline=edge + (255,), width=3)
    cx = (box[0] + box[2]) // 2
    ctext(d, cx, box[1] + 62, label, F(SANS_SB, 30), MUTED)
    ctext(d, cx, (box[1] + box[3]) // 2 + 32, value, F(SERIF_BLACK, vsize), CHARCOAL)


def save(img, name):
    out = os.path.join(OUT_DIR, name)
    img.convert("RGB").save(out, "PNG")
    print("saved", out)
    return out


# ---------------------------------------------------------------- 1. HERO ----
def hero():
    img = base(BLUSH_S)
    header(img, "Calm Money Reset", "an ADHD-friendly budget & debt tracker")
    box = (150, 470, S - 150, S - 200)
    panel(img, box)
    d = ImageDraw.Draw(img)
    ix0, ix1 = box[0] + 60, box[2] - 60
    banner(d, (ix0, box[1] + 55, ix1, box[1] + 165),
           "Calm Money Reset  ·  Dashboard", BLUSH, 54)
    d.text((ix0 + 6, box[1] + 235), "One calm glance. No dense charts, no red flags.",
           font=F(SANS, 34), fill=MUTED, anchor="lm")
    # cards
    cy0, cy1 = box[1] + 300, box[1] + 520
    gap = 40
    cw = (ix1 - ix0 - 2 * gap) // 3
    for i, (lab, val, fl, ed) in enumerate([
            ("SAFE TO SPEND / WEEK", "$210", SAGE_S, SAGE),
            ("NEXT BILL IN", "6 days", SKY_S, SKY),
            ("LOW-SPEND STREAK", "7 days", BLUSH_S, BLUSH)]):
        x0 = ix0 + i * (cw + gap)
        card(d, (x0, cy0, x0 + cw, cy1), lab, val, fl, ed, 76)
    # progress
    sy = cy1 + 70
    rr(d, (ix0, sy, ix1, sy + 60), 14, SAGE + (255,))
    d.text((ix0 + 28, sy + 30), "Your progress", font=F(SANS_B, 34), fill=CHARCOAL,
           anchor="lm")

    def bar(y, name, pct):
        d.text((ix0 + 6, y + 26), name, font=F(SANS_SB, 32), fill=CHARCOAL, anchor="lm")
        bx0, bx1 = ix0 + 360, ix1 - 150
        rr(d, (bx0, y, bx1, y + 52), 26, (236, 232, 224) + (255,))
        rr(d, (bx0, y, bx0 + (bx1 - bx0) * pct, y + 52), 26, SAGEBAR + (255,))
        d.text((ix1, y + 26), f"{int(pct*100)}%", font=F(SANS_B, 36), fill=CHARCOAL,
               anchor="rm")
    bar(sy + 100, "Debt paid off", 0.42)
    bar(sy + 190, "Savings goal", 0.68)
    # at a glance
    gy = sy + 285
    rr(d, (ix0, gy, ix1, gy + 60), 14, SKY + (255,))
    d.text((ix0 + 28, gy + 30), "This month, at a glance", font=F(SANS_B, 34),
           fill=CHARCOAL, anchor="lm")
    st = [("INCOME", "$3,200", SAGE_S), ("SPENT", "$2,140", BLUSH_S),
          ("LEFT", "$1,060", BUTTER_S)]
    sy2, sy3 = gy + 85, gy + 265
    for i, (lab, val, fl) in enumerate(st):
        x0 = ix0 + i * (cw + gap)
        rr(d, (x0, sy2, x0 + cw, sy3), 20, fl + (255,))
        ctext(d, x0 + cw // 2, sy2 + 52, lab, F(SANS_SB, 30), MUTED)
        ctext(d, x0 + cw // 2, sy2 + 128, val, F(SERIF_BLACK, 58), CHARCOAL)
    footer(img)
    return save(img, "mock_1_hero.png")


# ------------------------------------------------------------ 2. DOOM LOG ----
def doom():
    img = base(BUTTER_S)
    header(img, "Notice, don't judge", "the Doom Spending Log, shame-free by design")
    box = (150, 470, S - 150, S - 200)
    panel(img, box)
    d = ImageDraw.Draw(img)
    ix0, ix1 = box[0] + 60, box[2] - 60
    banner(d, (ix0, box[1] + 55, ix1, box[1] + 165), "Doom Spending Log", BUTTER, 54)
    rows = [
        ("Aug 3", "$18", "Impulse phone case", "Scrolling", "Neutral"),
        ("Aug 7", "$42", "Takeout, tired day", "Stress", "Fine"),
        ("Aug 12", "$9", "App upgrade", "Boredom", "Regret"),
        ("Aug 18", "$26", "Sale I didn't need", "Social pressure", "Regret"),
        ("Aug 24", "$15", "Treat after a win", "Celebration", "Fine"),
    ]
    ty = table(d, ix0, box[1] + 220, ix1,
               ["Date", "Amount", "What I bought", "Trigger", "Feeling"], rows,
               [140, 170, 470, 360, 180], rowh=78)
    # by-trigger tally
    ry = ty + 70
    rr(d, (ix0, ry, ix1, ry + 56), 12, LAV + (255,))
    d.text((ix0 + 24, ry + 28), "What tends to set it off", font=F(SANS_B, 30),
           fill=CHARCOAL, anchor="lm")
    tally = [("Scrolling", "3", LAV_S), ("Stress", "2", SKY_S),
             ("Boredom", "2", BUTTER_S), ("Celebration", "1", SAGE_S)]
    cw = (ix1 - ix0 - 3 * 30) // 4
    cy = ry + 84
    for i, (lab, n, fl) in enumerate(tally):
        x0 = ix0 + i * (cw + 30)
        rr(d, (x0, cy, x0 + cw, cy + 190), 22, fl + (255,))
        ctext(d, x0 + cw // 2, cy + 60, lab, F(SANS_SB, 30), MUTED)
        ctext(d, x0 + cw // 2, cy + 128, n, F(SERIF_BLACK, 60), CHARCOAL)
    ctext(d, S // 2, box[3] - 70,
          "No red flags. No shame column. Just your own patterns, gently.",
          F(SANS, 36), MUTED)
    footer(img)
    return save(img, "mock_2_doom.png")


# --------------------------------------------------------------- 3. STREAK ----
def streak():
    img = base(SAGE_S)
    header(img, "Every low-spend day counts",
           "build a streak, celebrate the small wins")
    box = (150, 470, S - 150, S - 200)
    panel(img, box)
    d = ImageDraw.Draw(img)
    ix0, ix1 = box[0] + 60, box[2] - 60
    banner(d, (ix0, box[1] + 55, ix1, box[1] + 165), "Low-Spend Streaks", SAGE, 54)
    # two cards
    cw = (ix1 - ix0 - 40) // 2
    card(d, (ix0, box[1] + 210, ix0 + cw, box[1] + 420), "CURRENT STREAK",
         "7 days", BLUSH_S, BLUSH, 84)
    card(d, (ix0 + cw + 40, box[1] + 210, ix1, box[1] + 420),
         "LONGEST THIS MONTH", "12 days", SAGE_S, SAGE, 84)
    # calendar grid
    gy = box[1] + 480
    rr(d, (ix0, gy, ix1, gy + 56), 12, SKY + (255,))
    d.text((ix0 + 24, gy + 28), "Mark a check on every low-spend day",
           font=F(SANS_B, 30), fill=CHARCOAL, anchor="lm")
    marked = {2, 3, 4, 8, 9, 10, 11, 12, 13, 14, 20, 21, 24, 25, 26}
    gx0, gy0 = ix0, gy + 80
    cell = (ix1 - ix0) // 7
    for i in range(28):
        rx = gx0 + (i % 7) * cell
        ry = gy0 + (i // 7) * 130
        fill = SAGE if (i + 1) in marked else CREAM
        rr(d, (rx + 8, ry + 8, rx + cell - 8, ry + 112), 16, fill=fill + (255,),
           outline=LINE + (255,), width=2)
        d.text((rx + 22, ry + 24), str(i + 1), font=F(SANS_SB, 24), fill=MUTED)
        if (i + 1) in marked:
            check(d, rx + cell // 2 + 6, ry + 66, 30, (86, 132, 85), 9)
    ctext(d, S // 2, box[3] - 60,
          "A full week. That is real momentum. Be proud.", F(SANS, 36), MUTED)
    footer(img)
    return save(img, "mock_3_streak.png")


# --------------------------------------------------------------- 4. PAUSE ----
def pause():
    img = base(BLUSH_S)
    header(img, "Pause before you buy", "the 24-hour rule, made into a habit")
    box = (150, 470, S - 150, S - 200)
    panel(img, box)
    d = ImageDraw.Draw(img)
    ix0, ix1 = box[0] + 60, box[2] - 60
    banner(d, (ix0, box[1] + 55, ix1, box[1] + 165), "Pause Before You Buy", BLUSH, 54)
    cw = (ix1 - ix0 - 80) // 3
    for i, (lab, val, fl) in enumerate([
            ("TIMES YOU PAUSED", "9", SAGE_S),
            ("MONEY PAUSED", "$486", BUTTER_S),
            ("BOUGHT ANYWAY", "2", BLUSH_S)]):
        x0 = ix0 + i * (cw + 40)
        card(d, (x0, box[1] + 210, x0 + cw, box[1] + 400), lab, val, fl,
             (230, 226, 220), 80)
    rows = [
        ("Second pair of sneakers", "$74", "No", "Waited"),
        ("Kitchen gadget", "$39", "No", "Skipped"),
        ("Book I'll actually read", "$18", "Yes", "Bought"),
        ("Trending jacket", "$120", "No", "Waited"),
    ]
    table(d, ix0, box[1] + 450, ix1,
          ["Item", "Cost", "Need it?", "Decision"], rows,
          [720, 150, 220, 300], rowh=82, band=(CREAM, SKY_S))
    ctext(d, S // 2, box[3] - 60, "Waiting is a win, not a loss.", F(SANS, 36), MUTED)
    footer(img)
    return save(img, "mock_4_pause.png")


# ------------------------------------------------------------ 5. WHAT'S IN ----
def inside():
    img = base(LAV_S)
    header(img, "12 gentle tabs", "everything you need, nothing that overwhelms")
    d = ImageDraw.Draw(img)
    tabs = [
        ("Dashboard", "safe-to-spend at a glance", SAGE_S),
        ("Flexible Income Budget", "for income that varies", SKY_S),
        ("Transactions Log", "type your numbers once", BUTTER_S),
        ("Doom Spending Log", "notice impulse buys", BUTTER_S),
        ("Low-Spend Streaks", "celebrate small wins", SAGE_S),
        ("Pause Before You Buy", "the 24-hour rule", BLUSH_S),
        ("Bill Calendar", "never miss a due date", LAV_S),
        ("Savings & Debt Goals", "watch progress fill up", SAGE_S),
        ("Subscription Tracker", "see what you really pay", SKY_S),
        ("Bank Import Helper", "paste and auto-categorise", SKY_S),
        ("Monthly Reflection", "a soft, kind reset", LAV_S),
        ("Bonus: Habit Tracker", "gentle daily habits", BLUSH_S),
    ]
    x0, y0 = 150, 470
    cw, ch, gx, gy = 545, 300, 40, 40
    for i, (name, sub, fl) in enumerate(tabs):
        cx = x0 + (i % 3) * (cw + gx)
        cy = y0 + (i // 3) * (ch + gy)
        rr(d, (cx, cy, cx + cw, cy + ch), 26, fill=fl + (255,))
        ctext(d, cx + cw // 2, cy + 120, name, F(SANS_B, 40), CHARCOAL)
        ctext(d, cx + cw // 2, cy + 190, sub, F(SANS, 30), MUTED)
    footer(img, "Google Sheets link + Excel file  ·  instant download")
    return save(img, "mock_5_inside.png")


if __name__ == "__main__":
    hero(); doom(); streak(); pause(); inside()
