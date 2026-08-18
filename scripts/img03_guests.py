# -*- coding: utf-8 -*-
from marketing_lib import *

img = new_canvas()
draw_paper_background(img, seed=21)

accent_title(img, "Never Lose Track Of", "Guests & Seating", top=64, script_size=40, title_size=70)
draw_centered_multiline(img, (CANVAS_W / 2, 210), "GUEST LIST + SEATING PLAN", font("sans_bold", 24),
                         MUTED_GREY, 1000)

GUEST_SS = "guest-list.png"
guest_box = (170, 290, 1030, 290 + (1030 - 170) / 1.6)
guest_meta = paste_laptop(img, GUEST_SS, guest_box, crop_box_frac=(0.0, 0.0, 1.0, 0.88))
pill_label(img, (280, guest_box[1] - 6), "GUEST LIST", BLUSH, font_size=20, pad_x=20, pad_y=10)

SEAT_SS = "seating-plan.png"
seat_w = 520
seat_box = (520, guest_box[3] + 70, 520 + seat_w, guest_box[3] + 70 + seat_w / 1.38)
seat_meta = paste_tablet(img, SEAT_SS, seat_box, crop_box_frac=(0.0, 0.0, 1.0, 1.0), bezel_color=WHITE)
pill_label(img, (seat_box[0] + 95, seat_box[1] - 6), "SEATING PLAN", SAGE, font_size=18, pad_x=18, pad_y=9)

thin_callout(img, (60, guest_box[1] + 55), "**Visual dashboard** with live RSVP and meal counts",
             frame_target(guest_meta, (0.06, 0.10)), align="left", max_width=210)
thin_callout(img, (1060, guest_box[1] + 55), "**Meal preferences** roll up into a chart automatically",
             frame_target(guest_meta, (0.86, 0.10)), align="right", max_width=210)
thin_callout(img, (60, guest_box[1] + 300), "**Track RSVPs** for every single guest, Yes / No / Awaited",
             frame_target(guest_meta, (0.30, 0.24)), align="left", max_width=220)

draw_badge(img, (110, guest_box[3] - 40), 56, "Up To\n1,000 Guests", BLUSH, font_size=15)

thin_callout(img, (1060, seat_box[1] + 40), "**Smart Seating** groups couples and families at the same table",
             frame_target(seat_meta, (0.30, 0.55)), align="right", max_width=210)
draw_badge(img, (1085, seat_box[3] - 30), 50, "Unique\nFeature", SAGE, font_size=15)

bar_top = seat_box[3] + 65
trust_bar(img, (60, bar_top, 1140, bar_top + 110), [
    (icon_sync, "RSVPs Sync\nAutomatically"),
    (icon_download, "Instant\nDownload"),
    (icon_spreadsheet, "Excel +\nGoogle Sheets"),
])

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=3)

save(img, "03-guests-seating.png")
