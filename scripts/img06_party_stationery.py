# -*- coding: utf-8 -*-
from marketing_lib import *
from PIL import ImageDraw

img = new_canvas()
draw_background(img, seed=52)

title_block(img, "Every Detail,\nOne Home Base", "Wedding Party + Stationery + Logistics", top=54,
            title_size=66, subtitle_size=24)

frames = [
    ("wedding-party.png", (0.0, 0.0, 0.62, 0.62), "WEDDING PARTY",
     "Track roles, attire, and who's confirmed", LAVENDER),
    ("stationery.png", (0.0, 0.0, 0.55, 0.6), "STATIONERY",
     "Design and print status, piece by piece", CREAM),
    ("transportation.png", (0.0, 0.0, 0.72, 0.62), "LOGISTICS",
     "Hotel blocks and transportation in one spot", POWDER),
]

gap = 30
fw = (1200 - 2 * 60 - 2 * gap) / 3
x0 = 60
y0 = 310
fh = 560

draw = ImageDraw.Draw(img, "RGBA")
for i, (ss, crop, label, caption, color) in enumerate(frames):
    bx0 = x0 + i * (fw + gap)
    box = (bx0, y0, bx0 + fw, y0 + fh)
    paste_device(img, ss, box, bezel_color=WHITE, style="tablet", crop_box_frac=crop, bezel_width=12)

    chip_w, chip_h = fw * 0.72, 40
    chip_x = bx0 + (fw - chip_w) / 2
    chip_y = y0 - 22
    rounded_rect(draw, [chip_x, chip_y, chip_x + chip_w, chip_y + chip_h], radius=20, fill=color)
    f_chip = font("sans_extrabold", 18)
    tw, th = text_size(draw, label, f_chip)
    draw.text((chip_x + chip_w / 2 - tw / 2, chip_y + chip_h / 2 - th / 2 - 2), label, font=f_chip, fill=CHARCOAL)

    cap_y = y0 + fh + 34
    draw_centered_multiline(img, (bx0 + fw / 2, cap_y), caption, font("sans_semibold", 21), CHARCOAL, fw - 10,
                             line_spacing=1.25)

# ---- summary panel filling the remaining canvas ----
panel_box = (110, 1150, 1090, 1490)
shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([panel_box[0], panel_box[1] + 10, panel_box[2], panel_box[3] + 10], radius=34, fill=(20, 16, 30, 45))
shadow = shadow.filter(ImageFilter.GaussianBlur(20))
img.paste(Image.alpha_composite(img.convert("RGB").convert("RGBA"), shadow).convert("RGB"), (0, 0))
draw = ImageDraw.Draw(img, "RGBA")
rounded_rect(draw, panel_box, radius=34, fill=WHITE, outline=(224, 219, 213), width=2)

bullets = [
    "**Wedding party roles sync** with your Guest List automatically",
    "**Stationery costs roll up** into your Wedding Budget tab",
    "**Every logistics detail** lives in the same file as everything else",
]
bx = panel_box[0] + 55
by = panel_box[1] + 48
row_h = 94
for text in bullets:
    r = 18
    cy = by + r
    draw.ellipse([bx - r, cy - r, bx + r, cy + r], fill=CHARCOAL)
    draw.line([(bx - 9, cy + 1), (bx - 2, cy + 8), (bx + 10, cy - 9)], fill=WHITE, width=5, joint="curve")
    draw_rich_paragraph(img, (bx + 42, by - 8), text, font("sans_semibold", 24), font("sans_extrabold", 24),
                         CHARCOAL, panel_box[2] - (bx + 42) - 45, line_spacing=1.3)
    by += row_h

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=6)

save(img, "06-party-stationery-logistics.png")
