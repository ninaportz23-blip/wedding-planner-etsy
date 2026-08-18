# -*- coding: utf-8 -*-
from marketing_lib import *
from PIL import ImageDraw

img = new_canvas()
draw_background(img, seed=41)

title_block(img, "850+ Tasks,\nAlready Written For You", "The Wedding Checklist", top=54,
            title_size=74, subtitle_size=26)

MAIN_SS = "checklist.png"
main_size = load_screenshot(MAIN_SS).size
main_crop = (0.0, 0.0, 0.58, 0.42)
main_box = (140, 320, 1060, 940)
paste_device(img, MAIN_SS, main_box, bezel_color=WHITE, style="tablet", crop_box_frac=main_crop, bezel_width=16)

draw_badge(img, (200, 350), 66, "850+\nItems", BLUSH, font_size=22)
draw_badge(img, (1030, 900), 70, "Pre-Filled", SAGE, font_size=21)
draw_badge(img, (150, 900), 60, "Editable", PEACH, font_size=20)

callouts = [
    ((30, 590, 300, 720), "**Progress bars** show exactly how each timeframe is tracking", (0.02, 0.05), "right"),
    ((900, 590, 1170, 710), "**Assign tasks** to bride, groom, or both with one click", (0.42, 0.05), "left"),
]
for bubble, text, target_frac, side in callouts:
    target = frac_to_canvas(main_box, 16, main_crop, main_size, target_frac)
    draw_callout(img, bubble, text, target, connector_from=side, font_size=21)

# ---- reference list of the 12 real timeframe sections ----
panel_box = (110, 990, 1090, 1500)
draw = ImageDraw.Draw(img, "RGBA")
shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([panel_box[0], panel_box[1] + 10, panel_box[2], panel_box[3] + 10], radius=34, fill=(20, 16, 30, 45))
shadow = shadow.filter(ImageFilter.GaussianBlur(20))
img.paste(Image.alpha_composite(img.convert("RGB").convert("RGBA"), shadow).convert("RGB"), (0, 0))
draw = ImageDraw.Draw(img, "RGBA")
rounded_rect(draw, panel_box, radius=34, fill=WHITE, outline=(224, 219, 213), width=2)

header_f = font("display_bold", 32)
draw.text((panel_box[0] + 50, panel_box[1] + 36), "12 Timeframes, Fully Organized", font=header_f, fill=CHARCOAL)

sections = [
    "12+ Months Before", "10-12 Months Before", "8-10 Months Before", "6-8 Months Before",
    "4-6 Months Before", "2-4 Months Before", "1 Month Before", "2 Weeks Before",
    "1 Week Before", "2 Days Before", "1 Day Before", "Legal Items",
]
cols = 3
col_w = (panel_box[2] - panel_box[0] - 100) / cols
row_h = 66
start_x = panel_box[0] + 50
start_y = panel_box[1] + 110
f_item = font("sans_semibold", 22)
for i, sec in enumerate(sections):
    col = i % cols
    row = i // cols
    x = start_x + col * col_w
    y = start_y + row * row_h
    draw.ellipse([x, y + 6, x + 12, y + 18], fill=SAGE)
    draw.text((x + 26, y), sec, font=f_item, fill=CHARCOAL)

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=5)

save(img, "05-checklist.png")
