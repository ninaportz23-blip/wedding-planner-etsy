# -*- coding: utf-8 -*-
from marketing_lib import *

img = new_canvas()
draw_paper_background(img, seed=52)

accent_title(img, "Every Detail", "One Home Base", top=60, script_size=40, title_size=72)
draw_centered_multiline(img, (CANVAS_W / 2, 200), "WEDDING PARTY + STATIONERY + LOGISTICS", font("sans_bold", 22),
                         MUTED_GREY, 1000)

frames = [
    ("wedding-party.png", "WEDDING PARTY", "Track roles, attire, and who's confirmed", LAVENDER, (0.0, 0.0, 0.74, 0.64)),
    ("stationery.png", "STATIONERY", "Design and print status, piece by piece", CREAM, (0.0, 0.0, 0.56, 0.50)),
    ("transportation.png", "LOGISTICS", "Hotel blocks and transportation, together", POWDER, (0.0, 0.0, 0.98, 0.60)),
]

gap = 34
fw = (1200 - 2 * 70 - 2 * gap) / 3
fh = fw / 1.35
x0 = 70
y0 = 300

metas = []
for i, (ss, label, caption, color, crop) in enumerate(frames):
    bx0 = x0 + i * (fw + gap)
    box = (bx0, y0, bx0 + fw, y0 + fh)
    meta = paste_tablet(img, ss, box, crop_box_frac=crop, bezel_color=WHITE)
    metas.append(meta)
    pill_label(img, (bx0 + fw / 2, y0 - 6), label, color, font_size=17, pad_x=16, pad_y=8)
    cap_y = y0 + fh + 32
    draw_centered_multiline(img, (bx0 + fw / 2, cap_y), caption, font("sans_semibold", 20), CHARCOAL, fw - 16,
                             line_spacing=1.25)

panel_box = (110, y0 + fh + 150, 1090, y0 + fh + 150 + 430)
draw = ImageDraw.Draw(img, "RGBA")
shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([panel_box[0], panel_box[1] + 10, panel_box[2], panel_box[3] + 10], radius=28, fill=(15, 12, 22, 45))
shadow = shadow.filter(ImageFilter.GaussianBlur(20))
img.paste(Image.alpha_composite(img.convert("RGBA"), shadow).convert("RGB"), (0, 0))
draw = ImageDraw.Draw(img, "RGBA")
rounded_rect(draw, panel_box, radius=28, fill=(255, 255, 255, 245), outline=(224, 219, 213), width=1)

bullets = [
    "**Wedding party roles sync** with your Guest List automatically",
    "**Stationery costs roll up** into your Wedding Budget tab",
    "**Every logistics detail** lives in the same file as everything else",
]
bx = panel_box[0] + 55
by = panel_box[1] + 55
row_h = 108
for text in bullets:
    r = 19
    cy = by + r
    draw.ellipse([bx - r, cy - r, bx + r, cy + r], fill=CHARCOAL)
    draw.line([(bx - 9, cy + 1), (bx - 2, cy + 8), (bx + 10, cy - 9)], fill=WHITE, width=5, joint="curve")
    draw_rich_paragraph(img, (bx + 44, by - 6), text, font("sans_semibold", 25), font("sans_extrabold", 25),
                         CHARCOAL, panel_box[2] - (bx + 44) - 45, line_spacing=1.3)
    by += row_h

bar_top = panel_box[3] + 65
trust_bar(img, (60, bar_top, 1140, bar_top + 110), [
    (icon_sync, "Everything\nStays In Sync"),
    (icon_download, "Instant\nDownload"),
    (icon_spreadsheet, "Excel +\nGoogle Sheets"),
])

draw_close_icon(img)
draw_pagination_dots(img, total=8, current=6)

save(img, "06-party-stationery-logistics.png")
