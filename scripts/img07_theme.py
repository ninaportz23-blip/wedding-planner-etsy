# -*- coding: utf-8 -*-
from marketing_lib import *
from PIL import ImageDraw

img = new_canvas()
draw_background(img, seed=63)

title_block(img, "Design Your\nWedding Look", "Moodboard + Decor + Flowers + Attire", top=54,
            title_size=74, subtitle_size=25)

items = [
    ("moodboard.png", (0.0, 0.0, 0.5, 0.7), "Moodboard", "Pin every inspiration image in one place", BLUSH),
    ("decor.png", (0.0, 0.0, 0.42, 0.62), "Decor Inventory", "Track cost and status for every rented piece", SAGE),
    ("flowers.png", (0.0, 0.0, 0.42, 0.62), "Flower Arrangements", "Every bouquet and centerpiece, costed out", PEACH),
    ("attire-makeup.png", (0.0, 0.0, 0.65, 0.55), "Attire & Makeup", "Looks organized by event and by person", LAVENDER),
]

gap = 40
fw = (1200 - 2 * 80 - gap) / 2
fh = 400
x0 = 80
y_rows = [320, 320 + fh + 130]

draw = ImageDraw.Draw(img, "RGBA")
for i, (ss, crop, label, caption, color) in enumerate(items):
    col = i % 2
    row = i // 2
    bx0 = x0 + col * (fw + gap)
    by0 = y_rows[row]
    box = (bx0, by0, bx0 + fw, by0 + fh)
    paste_device(img, ss, box, bezel_color=WHITE, style="tablet", crop_box_frac=crop, bezel_width=12)

    chip_w, chip_h = min(fw * 0.8, 300), 42
    chip_x = bx0 + (fw - chip_w) / 2
    chip_y = by0 - 22
    rounded_rect(draw, [chip_x, chip_y, chip_x + chip_w, chip_y + chip_h], radius=21, fill=color)
    f_chip = font("sans_extrabold", 19)
    tw, th = text_size(draw, label, f_chip)
    draw.text((chip_x + chip_w / 2 - tw / 2, chip_y + chip_h / 2 - th / 2 - 2), label, font=f_chip, fill=CHARCOAL)

    cap_y = by0 + fh + 30
    draw_centered_multiline(img, (bx0 + fw / 2, cap_y), caption, font("sans_semibold", 21), CHARCOAL, fw - 20,
                             line_spacing=1.25)

draw_badge(img, (600, 1462), 64, "Cohesive\nBy Design", CREAM, font_size=19)

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=7)

save(img, "07-theme.png")
