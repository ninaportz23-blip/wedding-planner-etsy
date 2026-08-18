# -*- coding: utf-8 -*-
from marketing_lib import *

img = new_canvas()
draw_paper_background(img, seed=33)

accent_title(img, "Venues And Vendors", "Compared Clearly", top=64, script_size=40, title_size=70)
draw_centered_multiline(img, (CANVAS_W / 2, 210), "VENUE COMPARISON + FOOD & DRINKS", font("sans_bold", 24),
                         MUTED_GREY, 1000)

VEN_SS = "venue-comparison.png"
venue_box = (170, 290, 1030, 290 + (1030 - 170) / 1.6)
venue_meta = paste_laptop(img, VEN_SS, venue_box, crop_box_frac=(0.0, 0.0, 1.0, 0.56))
pill_label(img, (300, venue_box[1] - 6), "VENUE COMPARISON", LAVENDER, font_size=20, pad_x=20, pad_y=10)

FOOD_SS = "food-drinks.png"
food_w = 520
food_box = (520, venue_box[3] + 70, 520 + food_w, venue_box[3] + 70 + food_w / 1.38)
food_meta = paste_tablet(img, FOOD_SS, food_box, crop_box_frac=(0.0, 0.0, 0.55, 0.74), bezel_color=WHITE)
pill_label(img, (food_box[0] + 90, food_box[1] - 6), "FOOD & DRINKS", PEACH, font_size=18, pad_x=18, pad_y=9)

thin_callout(img, (60, venue_box[1] + 55), "**Compare up to 5 venues** side by side on fees and capacity",
             frame_target(venue_meta, (0.06, 0.12)), align="left", max_width=210)
thin_callout(img, (1060, venue_box[1] + 55), "**Best value pick** flagged automatically once costs are in",
             frame_target(venue_meta, (0.75, 0.30)), align="right", max_width=220)

draw_badge(img, (110, venue_box[3] - 40), 58, "5 Venues\nSide By Side", LAVENDER, font_size=16)

thin_callout(img, (1060, food_box[1] + 40), "**Track tasting ratings** for every course, item by item",
             frame_target(food_meta, (0.55, 0.30)), align="right", max_width=210)
draw_badge(img, (1085, food_box[3] - 30), 50, "Cost\nTracker", PEACH, font_size=15)

bar_top = food_box[3] + 65
trust_bar(img, (60, bar_top, 1140, bar_top + 110), [
    (icon_sync, "Costs Roll Up\nTo Your Budget"),
    (icon_download, "Instant\nDownload"),
    (icon_spreadsheet, "Excel +\nGoogle Sheets"),
])

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=4)

save(img, "04-venue-food.png")
