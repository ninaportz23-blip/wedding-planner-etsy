# -*- coding: utf-8 -*-
from marketing_lib import *
from PIL import Image

img = new_canvas()
draw_background(img)

y = title_block(img, "See It All\nAt A Glance", "Live Dashboard + Smart Calendar", top=50,
                 title_size=86, subtitle_size=26)

MAIN_SS = "dashboard.png"
main_size = load_screenshot(MAIN_SS).size
main_crop = (0.0, 0.0, 1.0, 0.90)
main_box = (150, 300, 1050, 1300)
paste_device(img, MAIN_SS, main_box, bezel_color=WHITE, style="tablet", crop_box_frac=main_crop, bezel_width=16)

CAL_SS = "smart-calendar.png"
cal_size = load_screenshot(CAL_SS).size
cal_crop = (0.0, 0.235, 1.0, 0.86)
cal_box = (760, 1040, 1140, 1360)
paste_device(img, CAL_SS, cal_box, bezel_color=CHARCOAL, style="phone", crop_box_frac=cal_crop, bezel_width=14)

draw_badge(img, (185, 1340), 74, "Fully\nAutomated", LAVENDER, font_size=23)

callouts = [
    ((10, 300, 260, 400), "**Live countdown** ticks down to your wedding day", (0.34, 0.145), "right"),
    ((10, 640, 270, 750), "**Checklist progress** updates as you check off tasks", (0.10, 0.55), "right"),
    ((950, 300, 1195, 400), "**Budget snapshot** from your Budget tab", (0.66, 0.25), "left"),
    ((950, 640, 1195, 760), "**RSVP tracker** synced with your Guest List", (0.60, 0.55), "left"),
]
for bubble, text, target_frac, side in callouts:
    target = frac_to_canvas(main_box, 16, main_crop, main_size, target_frac)
    draw_callout(img, bubble, text, target, connector_from=side, font_size=21)

cal_target = frac_to_canvas(cal_box, 14, cal_crop, cal_size, (0.5, 0.92))
draw_callout(img, (770, 1400, 1140, 1490), "**Smart Calendar** auto-fills every due date",
             cal_target, connector_from="top", font_size=21)

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=1)

save(img, "01-dashboard-calendar.png")
