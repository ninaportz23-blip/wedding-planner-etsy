# -*- coding: utf-8 -*-
from marketing_lib import *

img = new_canvas()
draw_paper_background(img, seed=7)

eyebrow_bar(img, "GOOGLE SHEETS + EXCEL  |  FULLY AUTOMATED", top=44, icon_fn=icon_spreadsheet)
accent_title(img, "All-in-one", "Wedding\nDashboard", top=118, script_size=46, title_size=80)

LAPTOP_SS = "dashboard.png"
laptop_box = (150, 460, 1050, 460 + (1050 - 150) / 1.6)
meta = paste_laptop(img, LAPTOP_SS, laptop_box, crop_box_frac=(0.0, 0.0, 1.0, 0.90))

labels = [
    ("Live Budget Tracker", BLUSH),
    ("Guest + RSVP Sync", SAGE),
    ("Checklist Progress", POWDER),
    ("Smart Calendar", CREAM),
    ("Fully Automated", PEACH),
]
lx = laptop_box[0] + (laptop_box[2] - laptop_box[0]) * 0.60
ly = laptop_box[1] + 60
for text, color in labels:
    pill_label(img, (lx, ly), text, color, font_size=22, pad_x=24, pad_y=13)
    ly += 62

draw_badge(img, (940, 985), 58, "33\nTABS", CHARCOAL, text_color=WHITE, font_size=22)
draw_badge(img, (1055, 940), 50, "Easy To\nUse", WHITE, text_color=CHARCOAL, font_size=16)

bar_top = 1300
trust_bar(img, (60, bar_top, 1140, bar_top + 130), [
    (icon_play, "Video Tutorial\nIncluded"),
    (icon_stars_row, "Made For Real\nWedding Planning"),
    (icon_sync, "Smart\nAutomation"),
    (icon_download, "Instant\nDownload"),
])

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=1)

save(img, "01-dashboard-calendar.png")
