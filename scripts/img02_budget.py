# -*- coding: utf-8 -*-
from marketing_lib import *

img = new_canvas()
draw_background(img, seed=14)

title_block(img, "Know Where\nEvery Dollar Goes", "Wedding Budget + Vendor Research", top=50,
            title_size=78, subtitle_size=26)

MAIN_SS = "budget.png"
main_size = load_screenshot(MAIN_SS).size
main_crop = (0.0, 0.0, 0.62, 0.62)
main_box = (150, 300, 1050, 1010)
paste_device(img, MAIN_SS, main_box, bezel_color=WHITE, style="tablet", crop_box_frac=main_crop, bezel_width=16)

VEN_SS = "vendor-selection.png"
ven_size = load_screenshot(VEN_SS).size
ven_crop = (0.0, 0.0, 0.5, 0.42)
ven_box = (690, 970, 1140, 1300)
paste_device(img, VEN_SS, ven_box, bezel_color=CHARCOAL, style="tablet", crop_box_frac=ven_crop, bezel_width=14)

draw_bell_icon(img, (135, 1258), 30, CHARCOAL)
draw_badge(img, (150, 1330), 76, "Payment\nReminders", PEACH, font_size=22)

callouts = [
    ((10, 300, 260, 410), "**See exactly** where your money's going, category by category", (0.08, 0.08), "right"),
    ((10, 620, 260, 730), "**Vendor cost auto-updates** your budget the moment you mark a vendor Final", (0.10, 0.30), "right"),
    ((950, 300, 1195, 420), "**Payments turn red** automatically once they're past due and unpaid", (0.30, 0.55), "left"),
]
for bubble, text, target_frac, side in callouts:
    target = frac_to_canvas(main_box, 16, main_crop, main_size, target_frac)
    draw_callout(img, bubble, text, target, connector_from=side, font_size=21)

ven_target = frac_to_canvas(ven_box, 14, ven_crop, ven_size, (0.08, 0.18))
draw_callout(img, (700, 1330, 1170, 1430), "**Compare vendor quotes** side by side before you commit",
             ven_target, connector_from="top", font_size=21)

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=2)

save(img, "02-budget-vendors.png")
