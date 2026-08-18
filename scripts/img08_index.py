# -*- coding: utf-8 -*-
from marketing_lib import *

img = new_canvas()
draw_paper_background(img, seed=77)

accent_title(img, "Everything You Need", "What Will You Get?", top=56, script_size=38, title_size=68)
draw_centered_multiline(img, (CANVAS_W / 2, 190), "33 TABS. 1 FILE. EVERY DETAIL COVERED.", font("sans_bold", 24),
                         MUTED_GREY, 1000)

CATEGORIES = [
    ("Get Started", SAGE, ["Get Started", "Dashboard", "Smart Calendar"]),
    ("Budget & Vendors", LAVENDER, ["Wedding Budget", "Vendor Selection", "Venue Comparison"]),
    ("Guest Management", BLUSH, ["Guest List", "Reception Seating Plan", "Rehearsal Dinner Seating"]),
    ("Wedding Planning", PEACH, ["Wedding Checklist", "Wedding Itinerary", "Wedding Activities", "Aisle Order"]),
    ("Decor & Aesthetics", CREAM, ["Moodboard", "Decor Inventory", "Flower Arrangements", "Attire and Makeup"]),
    ("Wedding Logistics", POWDER, ["Accommodation", "Transportation", "Packing List"]),
    ("Wedding Stationery", SAGE, ["Stationery Checklist", "Save the Date"]),
    ("Entertainment & Food", LAVENDER, ["Music Planner", "Food and Drinks", "Photo and Video Shot List"]),
    ("Wedding Party & Gifts", BLUSH, ["Wedding Party", "Wedding Party Gifts", "Wedding Registry", "Gifts and Thank You"]),
    ("Pre-Wedding Events", PEACH, ["Engagement Party", "Bridal Shower", "Bachelor(ette) Planner"]),
    ("Post-Wedding", CREAM, ["Honeymoon Planner"]),
]

col_assign = [[], [], []]
col_load = [0, 0, 0]
for cat in CATEGORIES:
    load = 1.6 + len(cat[2])
    idx = col_load.index(min(col_load))
    col_assign[idx].append(cat)
    col_load[idx] += load

draw = ImageDraw.Draw(img, "RGBA")
col_w = 360
gap = 30
x0 = (CANVAS_W - (col_w * 3 + gap * 2)) / 2
y_top = 280
f_cat = font("display_bold", 27)
f_item = font("sans_semibold", 22)

for c, cats in enumerate(col_assign):
    x = x0 + c * (col_w + gap)
    y = y_top
    for label, color, tabs in cats:
        draw.rounded_rectangle([x, y, x + 11, y + 32], radius=5, fill=color)
        draw.text((x + 23, y - 2), label, font=f_cat, fill=CHARCOAL)
        y += 46
        for t in tabs:
            draw.ellipse([x + 25, y + 9, x + 32, y + 16], fill=(160, 155, 150, 255))
            draw.text((x + 44, y), t, font=f_item, fill=(70, 68, 66))
            y += 37
        y += 30

draw_centered_multiline(img, (CANVAS_W / 2, 1120),
                         "Everything you need to plan the wedding you actually want, in one file.",
                         font("display_bold", 28), CHARCOAL, 980, line_spacing=1.2)

trust_y = 1210
badges = ["Excel + Google Sheets", "Instant Digital Download", "LGBTQ+ Friendly", "Editable Colors & Text"]
bw = 264
bh = 78
bgap = 20
total_w = bw * 4 + bgap * 3
bx0 = (CANVAS_W - total_w) / 2
f_badge = font("sans_bold", 18)
for i, label in enumerate(badges):
    bx = bx0 + i * (bw + bgap)
    box = [bx, trust_y, bx + bw, trust_y + bh]
    rounded_rect(draw, box, radius=20, fill=WHITE, outline=(224, 219, 213), width=2)
    lines = wrap_text(draw, label, f_badge, bw - 30)
    lh = text_size(draw, "Ag", f_badge)[1] * 1.15
    ty = trust_y + bh / 2 - (lh * len(lines)) / 2
    for line in lines:
        tw, th = text_size(draw, line, f_badge)
        draw.text((bx + bw / 2 - tw / 2, ty), line, font=f_badge, fill=CHARCOAL)
        ty += lh

dark_y = trust_y + bh + 40
draw.rounded_rectangle([60, dark_y, 1140, dark_y + 90], radius=18, fill=(38, 36, 34, 255))
icon_stars_row(img, (600, dark_y + 32), 24)
f_dark = font("sans_bold", 21)
draw = ImageDraw.Draw(img, "RGBA")
label = "MADE FOR COUPLES PLANNING THE WEDDING THEY ACTUALLY WANT"
tw, th = text_size(draw, label, f_dark)
draw.text((600 - tw / 2, dark_y + 52), label, font=f_dark, fill=WHITE)

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=8)

save(img, "08-whats-included.png")
