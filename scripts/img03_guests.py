# -*- coding: utf-8 -*-
from marketing_lib import *

img = new_canvas()
draw_background(img, seed=21)

title_block(img, "Guests And Seating,\nSorted Automatically", "Guest List + Seating Plan", top=50,
            title_size=72, subtitle_size=26)

MAIN_SS = "guest-list.png"
main_size = load_screenshot(MAIN_SS).size
main_crop = (0.0, 0.0, 1.0, 0.42)
main_box = (150, 300, 1050, 1120)
paste_device(img, MAIN_SS, main_box, bezel_color=WHITE, style="tablet", crop_box_frac=main_crop, bezel_width=16)

SEAT_SS = "seating-plan.png"
seat_size = load_screenshot(SEAT_SS).size
seat_crop = (0.0, 0.44, 0.56, 0.80)
seat_box = (700, 1060, 1150, 1370)
paste_device(img, SEAT_SS, seat_box, bezel_color=CHARCOAL, style="tablet", crop_box_frac=seat_crop, bezel_width=14)

draw_badge(img, (170, 1220), 82, "Up To\n1,000 Guests", BLUSH, font_size=22)
draw_badge(img, (215, 1380), 60, "Unique\nFeature", SAGE, font_size=17)

callouts = [
    ((10, 300, 260, 410), "**Visual guest dashboard** with live RSVP and meal counts", (0.30, 0.06), "right"),
    ((10, 640, 270, 760), "**Track RSVPs and meal preferences** for every single guest", (0.35, 0.28), "right"),
    ((950, 300, 1195, 420), "**Rehearsal dinner list** builds itself from your RSVPs", (0.55, 0.14), "left"),
]
for bubble, text, target_frac, side in callouts:
    target = frac_to_canvas(main_box, 16, main_crop, main_size, target_frac)
    draw_callout(img, bubble, text, target, connector_from=side, font_size=21)

seat_target = frac_to_canvas(seat_box, 14, seat_crop, seat_size, (0.5, 0.06))
draw_callout(img, (700, 1400, 1170, 1500),
             "**Smart Seating** automatically groups couples and families at the same table",
             seat_target, connector_from="top", font_size=20)

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=3)

save(img, "03-guests-seating.png")
