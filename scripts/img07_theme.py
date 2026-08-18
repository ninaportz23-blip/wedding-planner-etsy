# -*- coding: utf-8 -*-
from marketing_lib import *

img = new_canvas()
draw_paper_background(img, seed=63)

accent_title(img, "Design Your", "Wedding Look", top=60, script_size=40, title_size=72)
draw_centered_multiline(img, (CANVAS_W / 2, 200), "MOODBOARD + DECOR + FLOWERS + ATTIRE", font("sans_bold", 22),
                         MUTED_GREY, 1000)

items = [
    ("moodboard.png", "Moodboard", "Pin every inspiration image in one place", BLUSH),
    ("decor.png", "Decor Inventory", "Track cost and status for every rented piece", SAGE),
    ("flowers.png", "Flower Arrangements", "Every bouquet and centerpiece, costed out", PEACH),
    ("attire-makeup.png", "Attire & Makeup", "Looks organized by event and by person", LAVENDER),
]

gap = 40
fw = (1200 - 2 * 80 - gap) / 2
fh = fw / 1.35
x0 = 80
y_rows = [300, 300 + fh + 120]

for i, (ss, label, caption, color) in enumerate(items):
    col = i % 2
    row = i // 2
    bx0 = x0 + col * (fw + gap)
    by0 = y_rows[row]
    box = (bx0, by0, bx0 + fw, by0 + fh)
    paste_tablet(img, ss, box, crop_box_frac=(0.0, 0.0, 1.0, 1.0), bezel_color=WHITE)
    pill_label(img, (bx0 + fw / 2, by0 - 6), label, color, font_size=18, pad_x=18, pad_y=9)
    cap_y = by0 + fh + 28
    draw_centered_multiline(img, (bx0 + fw / 2, cap_y), caption, font("sans_semibold", 20), CHARCOAL, fw - 20,
                             line_spacing=1.25)

bar_top = y_rows[1] + fh + 110
trust_bar(img, (60, bar_top, 1140, bar_top + 110), [
    (icon_sync, "Cohesive\nBy Design"),
    (icon_download, "Instant\nDownload"),
    (icon_spreadsheet, "Excel +\nGoogle Sheets"),
])

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=7)

save(img, "07-theme.png")
