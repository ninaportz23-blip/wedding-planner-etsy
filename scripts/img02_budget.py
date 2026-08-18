# -*- coding: utf-8 -*-
from marketing_lib import *

img = new_canvas()
draw_paper_background(img, seed=14)

accent_title(img, "Plan Smarter", "Spend Wiser", top=64, script_size=44, title_size=76)
draw = ImageDraw.Draw(img)
draw_centered_multiline(img, (CANVAS_W / 2, 210), "WEDDING BUDGET + VENDOR RESEARCH", font("sans_bold", 24),
                         MUTED_GREY, 1000)

BUDGET_SS = "budget.png"
budget_box = (170, 290, 1030, 290 + (1030 - 170) / 1.6)
budget_meta = paste_laptop(img, BUDGET_SS, budget_box, crop_box_frac=(0.0, 0.0, 1.0, 0.88))
pill_label(img, (300, budget_box[1] - 6), "WEDDING BUDGET", BLUSH, font_size=20, pad_x=20, pad_y=10)

VEN_SS = "vendor-selection.png"
ven_w = 520
ven_box = (520, budget_box[3] + 70, 520 + ven_w, budget_box[3] + 70 + ven_w / 1.38)
ven_meta = paste_tablet(img, VEN_SS, ven_box, crop_box_frac=(0.0, 0.0, 1.0, 1.0), bezel_color=WHITE)
pill_label(img, (ven_box[0] + 90, ven_box[1] - 6), "VENDOR RESEARCH", SAGE, font_size=18, pad_x=18, pad_y=9)

# thin callouts on the budget laptop
b_targets = {
    "kpi": (0.06, 0.135),
    "chart": (0.55, 0.30),
    "payments": (0.20, 0.62),
}
thin_callout(img, (60, budget_box[1] + 60), "**Know where your money's going**, category by category",
             frame_target(budget_meta, b_targets["kpi"]), align="left", max_width=210)
thin_callout(img, (1060, budget_box[1] + 150), "See a **live breakdown** of spending vs. budget",
             frame_target(budget_meta, b_targets["chart"]), align="right", max_width=210)
thin_callout(img, (60, budget_box[1] + 330), "**Payments turn red** automatically once they're overdue",
             frame_target(budget_meta, b_targets["payments"]), align="left", max_width=220)

draw_badge(img, (110, ven_box[1] + 20), 54, "Payment\nReminder", LAVENDER, font_size=16)

# thin callouts on the vendor tablet
v_targets = {
    "amount": (0.55, 0.30),
    "final": (0.06, 0.35),
}
thin_callout(img, (1080, ven_box[1] + 40), "**Mark a vendor Final** and your budget updates itself",
             frame_target(ven_meta, v_targets["final"]), align="right", max_width=220)
draw_badge(img, (1085, ven_box[3] - 30), 50, "Filter\nFeature", SAGE, font_size=15)

bar_top = ven_box[3] + 65
trust_bar(img, (60, bar_top, 1140, bar_top + 110), [
    (icon_sync, "Vendor Cost\nAuto-Updates"),
    (icon_download, "Instant\nDownload"),
    (icon_spreadsheet, "Excel +\nGoogle Sheets"),
])

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=2)

save(img, "02-budget-vendors.png")
