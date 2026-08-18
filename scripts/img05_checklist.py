# -*- coding: utf-8 -*-
from marketing_lib import *

img = new_canvas()
draw_paper_background(img, seed=41)

accent_title(img, "Jump Start Your Planning", "Ready-Made Checklists", top=64, script_size=38, title_size=64)
draw_centered_multiline(img, (CANVAS_W / 2, 200), "850+ PRE-WRITTEN WEDDING TASKS", font("sans_bold", 24),
                         MUTED_GREY, 1000)

CL_SS = "checklist.png"
cl_box = (150, 280, 1050, 280 + (1050 - 150) / 1.6)
cl_meta = paste_laptop(img, CL_SS, cl_box, crop_box_frac=(0.0, 0.0, 1.0, 0.88))
pill_label(img, (270, cl_box[1] - 6), "WEDDING CHECKLIST", CREAM, font_size=20, pad_x=20, pad_y=10)

thin_callout(img, (60, cl_box[1] + 60), "**Progress bars** show how each timeframe is tracking",
             frame_target(cl_meta, (0.03, 0.06)), align="left", max_width=210)
thin_callout(img, (1060, cl_box[1] + 60), "**Assign tasks** to bride, groom, or both",
             frame_target(cl_meta, (0.55, 0.06)), align="right", max_width=200)

draw_badge(img, (150, cl_box[3] - 10), 58, "850+\nItems", BLUSH, font_size=22)
draw_badge(img, (330, cl_box[3] + 40), 50, "Pre-Filled", SAGE, font_size=17)
draw_badge(img, (1050, cl_box[3] - 10), 56, "Editable", PEACH, font_size=18)

panel_box = (110, cl_box[3] + 110, 1090, cl_box[3] + 110 + 470)
draw = ImageDraw.Draw(img, "RGBA")
shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([panel_box[0], panel_box[1] + 10, panel_box[2], panel_box[3] + 10], radius=28, fill=(15, 12, 22, 45))
shadow = shadow.filter(ImageFilter.GaussianBlur(20))
img.paste(Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB"), (0, 0))
draw = ImageDraw.Draw(img, "RGBA")
rounded_rect(draw, panel_box, radius=28, fill=(255, 255, 255, 245), outline=(224, 219, 213), width=1)

draw.text((panel_box[0] + 46, panel_box[1] + 32), "12 Timeframes, Fully Organized", font=font("display_bold", 30),
           fill=CHARCOAL)

sections = [
    "12+ Months Before", "10-12 Months Before", "8-10 Months Before", "6-8 Months Before",
    "4-6 Months Before", "2-4 Months Before", "1 Month Before", "2 Weeks Before",
    "1 Week Before", "2 Days Before", "1 Day Before", "Legal Items",
]
cols = 3
col_w = (panel_box[2] - panel_box[0] - 92) / cols
row_h = 62
start_x = panel_box[0] + 46
start_y = panel_box[1] + 104
f_item = font("sans_semibold", 21)
for i, sec in enumerate(sections):
    col = i % cols
    row = i // cols
    x = start_x + col * col_w
    y = start_y + row * row_h
    draw.ellipse([x, y + 5, x + 11, y + 16], fill=SAGE)
    draw.text((x + 24, y), sec, font=f_item, fill=CHARCOAL)

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=5)

save(img, "05-checklist.png")
