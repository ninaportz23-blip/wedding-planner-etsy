# -*- coding: utf-8 -*-
from marketing_lib import *
from PIL import ImageDraw

img = new_canvas()
draw_background(img, seed=33)

title_block(img, "Venues And Vendors,\nCompared Clearly", "Venue Comparison + Food & Drinks", top=54,
            title_size=72, subtitle_size=26)

VEN_SS = "venue-comparison.png"
FOOD_SS = "food-drinks.png"
ven_box = (80, 330, 590, 760)
food_box = (610, 330, 1120, 760)
paste_device(img, VEN_SS, ven_box, bezel_color=WHITE, style="tablet",
             crop_box_frac=(0.0, 0.0, 1.0, 0.55), bezel_width=14)
paste_device(img, FOOD_SS, food_box, bezel_color=WHITE, style="tablet",
             crop_box_frac=(0.0, 0.0, 0.62, 0.30), bezel_width=14)

draw_badge(img, (985, 300), 60, "5 Venues\nSide by Side", SAGE, font_size=16)

# ---- clean bullet column, no connector lines ----
panel_box = (110, 870, 1090, 1440)
draw = ImageDraw.Draw(img, "RGBA")
shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([panel_box[0], panel_box[1] + 10, panel_box[2], panel_box[3] + 10], radius=34, fill=(20, 16, 30, 45))
shadow = shadow.filter(ImageFilter.GaussianBlur(20))
img.paste(Image.alpha_composite(img.convert("RGB").convert("RGBA"), shadow).convert("RGB"), (0, 0))
draw = ImageDraw.Draw(img, "RGBA")
rounded_rect(draw, panel_box, radius=34, fill=WHITE, outline=(224, 219, 213), width=2)

bullets = [
    "**Compare up to 5 venues** side by side: fees, capacity, and availability",
    "**See your best value pick** flagged automatically once you enter costs",
    "**Track rehearsal dinner and reception menus** by course, with tasting ratings",
    "**Know your food and drink total** before you ever sign a catering contract",
]
bx = panel_box[0] + 60
by = panel_box[1] + 55
row_h = 128
for text in bullets:
    r = 20
    cy = by + r
    draw.ellipse([bx - r, cy - r, bx + r, cy + r], fill=CHARCOAL)
    check_pts = [(bx - 10, cy + 1), (bx - 3, cy + 8), (bx + 11, cy - 10)]
    draw.line(check_pts, fill=WHITE, width=5, joint="curve")
    draw_rich_paragraph(img, (bx + 46, by - 6), text, font("sans_semibold", 25), font("sans_extrabold", 25),
                         CHARCOAL, panel_box[2] - (bx + 46) - 50, line_spacing=1.35)
    by += row_h

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=4)

save(img, "04-venue-food.png")
