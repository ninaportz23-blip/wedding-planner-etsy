# -*- coding: utf-8 -*-
"""Generates one multi-page HTML file (8 pages) for Canva's import-design-from-url,
replicating the 8 Etsy listing images as real editable Canva elements: text,
pills, badges, and callouts stay as separate text/shape layers; only the
spreadsheet tab screenshots themselves are images."""
import re

GH = "https://raw.githubusercontent.com/ninaportz23-blip/wedding-planner-etsy/claude/wedding-planner-etsy-ek5s5p/qa_screens/"

LAVENDER = "#D8D3F0"
BLUSH = "#F6D9DE"
SAGE = "#DCE8D8"
CREAM = "#F5EFD6"
POWDER = "#D8E6F0"
PEACH = "#F5DFD0"
CHARCOAL = "#2E2E2E"
PAPER = "#F1ECE3"
MUTED = "#5A5A5A"
WHITE = "#FFFFFF"

W, H = 1200, 1600

PAGES = []


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Page:
    def __init__(self, label):
        self.label = label
        self.els = []
        self.svg_lines = []

    def raw(self, html):
        self.els.append(html)

    def eyebrow(self, text, icon=""):
        self.els.append(f'<div class="eyebrow">{icon}{esc(text)}</div>')

    def script_title(self, script, title, title_size=76, top=118):
        self.els.append(f'<div class="script" style="top:{top}px;">{esc(script)}</div>')
        self.els.append(f'<div class="title" style="top:{top+56}px;font-size:{title_size}px;">{esc(title)}</div>')

    def subtitle(self, text, top=210):
        self.els.append(f'<div class="subtitle" style="top:{top}px;">{esc(text)}</div>')

    def laptop(self, img_name, box, crop_top_pct=88):
        x0, y0, x1, y1 = box
        w, h = x1 - x0, y1 - y0
        self.els.append(f'''<div class="laptop" style="top:{y0}px;left:{x0}px;width:{w}px;height:{h}px;">
      <img src="{GH}{img_name}" style="object-position: top center; object-fit: cover;">
    </div>
    <div class="deck" style="top:{y1}px;left:{x0-40}px;width:{w+80}px;"></div>''')
        return box

    def tablet(self, img_name, box):
        x0, y0, x1, y1 = box
        w, h = x1 - x0, y1 - y0
        self.els.append(f'''<div class="tablet" style="top:{y0}px;left:{x0}px;width:{w}px;height:{h}px;">
      <img src="{GH}{img_name}" style="object-position: top center; object-fit: cover;">
    </div>''')
        return box

    def pill(self, text, x, y, color, font_size=20):
        self.els.append(
            f'<div class="pill" style="top:{y}px;left:{x}px;background:{color};font-size:{font_size}px;">{esc(text)}</div>')

    def badge(self, text, cx, cy, r, color, text_color=CHARCOAL, font_size=20):
        lines = text.split("\n")
        inner = "<br>".join(esc(l) for l in lines)
        self.els.append(
            f'<div class="badge" style="top:{cy-r}px;left:{cx-r}px;width:{2*r}px;height:{2*r}px;'
            f'background:{color};color:{text_color};font-size:{font_size}px;">{inner}</div>')

    def callout(self, text, label_xy, target_xy, align="left", width=210, font_size=18):
        lx, ly = label_xy
        tx, ty = target_xy
        text_html = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc(text).replace("**", "\x00\x00")) if False else _bold(text)
        style_align = "text-align:left;" if align == "left" else "text-align:right;"
        left_css = f"left:{lx}px;" if align == "left" else f"right:{W-lx}px;"
        self.els.append(
            f'<div class="callout" style="top:{ly}px;{left_css}width:{width}px;{style_align}font-size:{font_size}px;">{text_html}</div>')
        edge_x = lx + width if align == "left" else lx - width
        edge_y = ly + 24
        self.svg_lines.append((edge_x, edge_y, tx, ty))

    def trust_bar(self, items, top):
        cells = "".join(
            f'<div class="trustcell"><span class="ic">{ic}</span>{esc(t)}</div>' for ic, t in items)
        self.els.append(f'<div class="trustbar" style="top:{top}px;">{cells}</div>')

    def panel(self, box):
        x0, y0, x1, y1 = box
        return x0, y0, x1, y1

    def panel_open(self, box, heading=None):
        x0, y0, x1, y1 = box
        h = f'<div class="paneltitle">{esc(heading)}</div>' if heading else ""
        self.els.append(f'<div class="panel" style="top:{y0}px;left:{x0}px;width:{x1-x0}px;height:{y1-y0}px;">{h}')

    def panel_close(self):
        self.els.append('</div>')

    def bullet(self, x, y, text, width):
        self.els.append(
            f'<div class="bullet" style="top:{y}px;left:{x}px;width:{width}px;">'
            f'<span class="check">&#10003;</span>{_bold(text)}</div>')

    def dots(self, current, total=8):
        spans = "".join(f'<span class="{"active" if i+1==current else ""}"></span>' for i in range(total))
        self.els.append(f'<div class="dots">{spans}</div>')

    def render(self):
        svg = ""
        if self.svg_lines:
            lines = "".join(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#8c8680" stroke-width="2"/>'
                f'<circle cx="{x1}" cy="{y1}" r="3" fill="#2E2E2E"/>'
                f'<circle cx="{x2}" cy="{y2}" r="5" fill="white" stroke="#2E2E2E" stroke-width="2"/>'
                for x1, y1, x2, y2 in self.svg_lines
            )
            svg = f'<svg class="lines" width="{W}" height="{H}">{lines}</svg>'
        body = "\n    ".join(self.els)
        return f'''<div class="page" data-document-role="page" data-label="{esc(self.label)}">
    {svg}
    {body}
  </div>'''


def _bold(text):
    parts = re.split(r"(\*\*.+?\*\*)", text)
    out = []
    for p in parts:
        if p.startswith("**") and p.endswith("**"):
            out.append(f"<b>{esc(p[2:-2])}</b>")
        else:
            out.append(esc(p))
    return "".join(out)


TRUST_ICONS = {"play": "&#9654;", "stars": "&#9733;&#9733;&#9733;&#9733;&#9733;", "sync": "&#8635;",
                "download": "&#8681;", "sheet": "&#9638;"}

CSS = f"""
* {{ box-sizing: border-box; }}
body {{ margin: 0; font-family: Georgia, 'Times New Roman', serif; }}
.page {{ width: {W}px; height: {H}px; position: relative; overflow: hidden; background: {PAPER}; }}
.eyebrow {{ position: absolute; top: 40px; left: 50%; transform: translateX(-50%);
  background: #ffffffcc; border: 1px solid #ddd6cc; border-radius: 27px; padding: 14px 30px;
  font-family: Arial, sans-serif; font-weight: 700; font-size: 19px; color: #3c3a38; white-space: nowrap; }}
.script {{ position: absolute; left: 50%; transform: translateX(-50%); font-style: italic;
  font-size: 42px; color: {MUTED}; white-space: nowrap; }}
.title {{ position: absolute; left: 50%; transform: translateX(-50%); font-weight: 900;
  color: {CHARCOAL}; text-align: center; white-space: nowrap; }}
.subtitle {{ position: absolute; left: 50%; transform: translateX(-50%); font-family: Arial, sans-serif;
  font-weight: 700; font-size: 23px; letter-spacing: 0.5px; color: {MUTED}; white-space: nowrap; }}
.laptop {{ position: absolute; background: #1c1b1a; border-radius: 16px; box-shadow: 0 30px 60px rgba(0,0,0,0.28); }}
.laptop img {{ position: absolute; top: 16px; left: 16px; right: 16px; bottom: 16px; width: calc(100% - 32px);
  height: calc(100% - 32px); border-radius: 4px; }}
.deck {{ position: absolute; height: 24px; background: #d6d1c9; border-radius: 0 0 8px 8px; }}
.tablet {{ position: absolute; background: white; border: 2px solid #e0dbd0; border-radius: 26px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.18); }}
.tablet img {{ position: absolute; top: 14px; left: 14px; right: 14px; bottom: 14px; width: calc(100% - 28px);
  height: calc(100% - 28px); border-radius: 14px; }}
.pill {{ position: absolute; font-family: Arial, sans-serif; font-weight: 800; color: {CHARCOAL};
  border-radius: 30px; padding: 12px 22px; white-space: nowrap; box-shadow: 0 6px 12px rgba(0,0,0,0.12); }}
.badge {{ position: absolute; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  text-align: center; font-family: Arial, sans-serif; font-weight: 800; box-shadow: 0 8px 16px rgba(0,0,0,0.18);
  border: 4px solid white; line-height: 1.2; }}
.callout {{ position: absolute; font-family: Arial, sans-serif; font-weight: 600; color: {CHARCOAL};
  background: #ffffffee; border-radius: 8px; padding: 4px; line-height: 1.35; }}
.callout b {{ font-weight: 800; }}
.trustbar {{ position: absolute; left: 60px; width: 1080px; height: 110px; background: white;
  border: 1px solid #e0dbd0; border-radius: 18px; display: flex; align-items: center; justify-content: space-around;
  font-family: Arial, sans-serif; }}
.trustcell {{ text-align: center; font-weight: 700; font-size: 17px; color: {CHARCOAL}; }}
.trustcell .ic {{ font-size: 24px; display: block; margin-bottom: 8px; color: #d9a441; }}
.panel {{ position: absolute; background: #ffffffee; border: 1px solid #e0dbd0; border-radius: 28px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.12); padding: 40px 50px; }}
.paneltitle {{ font-family: Georgia, serif; font-weight: 700; font-size: 28px; color: {CHARCOAL}; margin-bottom: 20px; }}
.bullet {{ position: absolute; font-family: Arial, sans-serif; font-weight: 600; font-size: 23px;
  color: {CHARCOAL}; line-height: 1.3; }}
.bullet .check {{ display: inline-block; width: 34px; height: 34px; border-radius: 50%; background: {CHARCOAL};
  color: white; text-align: center; line-height: 34px; margin-right: 14px; font-size: 18px; vertical-align: middle; }}
.dots {{ position: absolute; top: 1560px; left: 50%; transform: translateX(-50%); display: flex; gap: 18px; }}
.dots span {{ width: 14px; height: 14px; border-radius: 50%; background: #ccc5ba; display: block; }}
.dots span.active {{ background: {CHARCOAL}; width: 20px; height: 20px; }}
.lines {{ position: absolute; top: 0; left: 0; pointer-events: none; }}
.catlabel {{ position: absolute; font-family: Georgia, serif; font-weight: 700; font-size: 26px; color: {CHARCOAL}; }}
.catitem {{ position: absolute; font-family: Arial, sans-serif; font-weight: 600; font-size: 21px; color: #46443f; }}
.catdot {{ position: absolute; width: 7px; height: 7px; border-radius: 50%; background: #a09b95; }}
.catbar {{ position: absolute; width: 11px; height: 32px; border-radius: 5px; }}
.badgechip {{ position: absolute; background: white; border: 2px solid #e0dbd0; border-radius: 20px;
  font-family: Arial, sans-serif; font-weight: 700; font-size: 18px; color: {CHARCOAL};
  display: flex; align-items: center; justify-content: center; text-align: center; line-height: 1.25; }}
.darkbar {{ position: absolute; left: 60px; width: 1080px; border-radius: 18px; background: #262422;
  color: white; font-family: Arial, sans-serif; font-weight: 700; font-size: 20px; text-align: center;
  padding: 18px 0; }}
.darkbar .stars {{ color: #e8b23c; font-size: 22px; display: block; margin-bottom: 6px; }}
"""


# =====================================================================
# PAGE 1 - Dashboard + Smart Calendar
# =====================================================================
p = Page("Dashboard and Smart Calendar")
p.eyebrow("GOOGLE SHEETS + EXCEL  |  FULLY AUTOMATED")
p.script_title("All-in-one", "Wedding Dashboard", title_size=80)
box = p.laptop("dashboard.png", (150, 300, 1050, 300 + 900 / 1.6))
p.pill("Live Budget Tracker", 690, 540, BLUSH)
p.pill("Guest + RSVP Sync", 690, 602, SAGE)
p.pill("Checklist Progress", 690, 664, POWDER)
p.pill("Smart Calendar", 690, 726, CREAM)
p.pill("Fully Automated", 690, 788, PEACH)
p.badge("33\nTABS", 940, 985, 58, CHARCOAL, WHITE, 22)
p.badge("Easy To\nUse", 1055, 940, 50, WHITE, CHARCOAL, 16)
p.trust_bar([(TRUST_ICONS["play"], "Video Tutorial Included"), (TRUST_ICONS["stars"], "Made For Real Wedding Planning"),
             (TRUST_ICONS["sync"], "Smart Automation"), (TRUST_ICONS["download"], "Instant Download")], 1300)
p.dots(1)
PAGES.append(p)

# =====================================================================
# PAGE 2 - Budget + Vendor Research
# =====================================================================
p = Page("Wedding Budget and Vendor Research")
p.script_title("Plan Smarter", "Spend Wiser", title_size=76, top=64)
p.subtitle("WEDDING BUDGET + VENDOR RESEARCH", top=210)
bbox = (170, 290, 1030, 290 + 860 / 1.6)
p.laptop("budget.png", bbox)
p.pill("WEDDING BUDGET", 300, bbox[1] - 30, BLUSH, 20)
vbox = (520, bbox[3] + 70, 520 + 520, bbox[3] + 70 + 520 / 1.38)
p.tablet("vendor-selection.png", vbox)
p.pill("VENDOR RESEARCH", vbox[0] + 90, vbox[1] - 28, SAGE, 18)
p.callout("**Know where your money's going**, category by category", (60, bbox[1] + 60), (bbox[0] + 60, bbox[1] + 180), "left")
p.callout("See a **live breakdown** of spending vs. budget", (1060, bbox[1] + 150), (bbox[0] + 500, bbox[1] + 260), "right")
p.callout("**Payments turn red** automatically once they're overdue", (60, bbox[1] + 330), (bbox[0] + 200, bbox[1] + 420), "left")
p.badge("Payment\nReminder", 110, vbox[1] + 20, 54, LAVENDER, CHARCOAL, 15)
p.callout("**Mark a vendor Final** and your budget updates itself", (1080, vbox[1] + 40), (vbox[0] + 60, vbox[1] + 220), "right")
p.badge("Filter\nFeature", 1085, vbox[3] - 30, 50, SAGE, CHARCOAL, 14)
bar_top = vbox[3] + 65
p.trust_bar([(TRUST_ICONS["sync"], "Vendor Cost Auto-Updates"), (TRUST_ICONS["download"], "Instant Download"),
             (TRUST_ICONS["sheet"], "Excel + Google Sheets")], bar_top)
p.dots(2)
PAGES.append(p)

# =====================================================================
# PAGE 3 - Guests + Seating
# =====================================================================
p = Page("Guest List and Seating Plan")
p.script_title("Never Lose Track Of", "Guests &amp; Seating", title_size=68, top=64)
p.subtitle("GUEST LIST + SEATING PLAN", top=210)
gbox = (170, 290, 1030, 290 + 860 / 1.6)
p.laptop("guest-list.png", gbox)
p.pill("GUEST LIST", 280, gbox[1] - 30, BLUSH, 20)
sbox = (520, gbox[3] + 70, 520 + 520, gbox[3] + 70 + 520 / 1.38)
p.tablet("seating-plan.png", sbox)
p.pill("SEATING PLAN", sbox[0] + 95, sbox[1] - 28, SAGE, 18)
p.callout("**Visual dashboard** with live RSVP and meal counts", (60, gbox[1] + 55), (gbox[0] + 60, gbox[1] + 140), "left")
p.callout("**Meal preferences** roll up into a chart automatically", (1060, gbox[1] + 55), (gbox[0] + 730, gbox[1] + 140), "right")
p.callout("**Track RSVPs** for every single guest, Yes / No / Awaited", (60, gbox[1] + 300), (gbox[0] + 260, gbox[1] + 210), "left")
p.badge("Up To\n1,000 Guests", 110, gbox[3] - 40, 56, BLUSH, CHARCOAL, 14)
p.callout("**Smart Seating** groups couples and families at the same table", (1060, sbox[1] + 40), (sbox[0] + 260, sbox[1] + 240), "right")
p.badge("Unique\nFeature", 1085, sbox[3] - 30, 50, SAGE, CHARCOAL, 14)
bar_top = sbox[3] + 65
p.trust_bar([(TRUST_ICONS["sync"], "RSVPs Sync Automatically"), (TRUST_ICONS["download"], "Instant Download"),
             (TRUST_ICONS["sheet"], "Excel + Google Sheets")], bar_top)
p.dots(3)
PAGES.append(p)

# =====================================================================
# PAGE 4 - Venue + Food & Drinks
# =====================================================================
p = Page("Venue Comparison and Food and Drinks")
p.script_title("Venues And Vendors", "Compared Clearly", title_size=70, top=64)
p.subtitle("VENUE COMPARISON + FOOD &amp; DRINKS", top=210)
vebox = (170, 290, 1030, 290 + 860 / 1.6)
p.laptop("venue-comparison.png", vebox)
p.pill("VENUE COMPARISON", 300, vebox[1] - 30, LAVENDER, 20)
fbox = (520, vebox[3] + 70, 520 + 520, vebox[3] + 70 + 520 / 1.38)
p.tablet("food-drinks.png", fbox)
p.pill("FOOD &amp; DRINKS", fbox[0] + 90, fbox[1] - 28, PEACH, 18)
p.callout("**Compare up to 5 venues** side by side on fees and capacity", (60, vebox[1] + 55), (vebox[0] + 60, vebox[1] + 150), "left")
p.callout("**Best value pick** flagged automatically once costs are in", (1060, vebox[1] + 55), (vebox[0] + 650, vebox[1] + 260), "right")
p.badge("5 Venues\nSide By Side", 110, vebox[3] - 40, 58, LAVENDER, CHARCOAL, 15)
p.callout("**Track tasting ratings** for every course, item by item", (1060, fbox[1] + 40), (fbox[0] + 480, fbox[1] + 260), "right")
p.badge("Cost\nTracker", 1085, fbox[3] - 30, 50, PEACH, CHARCOAL, 14)
bar_top = fbox[3] + 65
p.trust_bar([(TRUST_ICONS["sync"], "Costs Roll Up To Your Budget"), (TRUST_ICONS["download"], "Instant Download"),
             (TRUST_ICONS["sheet"], "Excel + Google Sheets")], bar_top)
p.dots(4)
PAGES.append(p)

# =====================================================================
# PAGE 5 - Checklist
# =====================================================================
p = Page("Wedding Checklist")
p.script_title("Jump Start Your Planning", "Ready-Made Checklists", title_size=62, top=64)
p.subtitle("850+ PRE-WRITTEN WEDDING TASKS", top=200)
clbox = (150, 280, 1050, 280 + 900 / 1.6)
p.laptop("checklist.png", clbox)
p.pill("WEDDING CHECKLIST", 270, clbox[1] - 30, CREAM, 20)
p.callout("**Progress bars** show how each timeframe is tracking", (60, clbox[1] + 60), (clbox[0] + 40, clbox[1] + 100), "left")
p.callout("**Assign tasks** to bride, groom, or both", (1060, clbox[1] + 60), (clbox[0] + 500, clbox[1] + 100), "right")
p.badge("850+\nItems", 150, clbox[3] - 10, 58, BLUSH, CHARCOAL, 21)
p.badge("Pre-Filled", 330, clbox[3] + 40, 50, SAGE, CHARCOAL, 16)
p.badge("Editable", 1050, clbox[3] - 10, 56, PEACH, CHARCOAL, 17)
panel_box = (110, clbox[3] + 110, 1090, clbox[3] + 110 + 470)
p.panel_open(panel_box, "12 Timeframes, Fully Organized")
sections = ["12+ Months Before", "10-12 Months Before", "8-10 Months Before", "6-8 Months Before",
            "4-6 Months Before", "2-4 Months Before", "1 Month Before", "2 Weeks Before",
            "1 Week Before", "2 Days Before", "1 Day Before", "Legal Items"]
col_w = (panel_box[2] - panel_box[0] - 100) / 3
for i, sec in enumerate(sections):
    col, row = i % 3, i // 3
    x = 8 + col * col_w
    y = 100 + row * 62
    p.raw(f'<div class="catdot" style="top:{y+8}px;left:{x}px;background:{SAGE};"></div>'
          f'<div class="catitem" style="top:{y}px;left:{x+20}px;">{esc(sec)}</div>')
p.panel_close()
p.dots(5)
PAGES.append(p)

# =====================================================================
# PAGE 6 - Wedding Party + Stationery + Logistics
# =====================================================================
p = Page("Wedding Party, Stationery, and Logistics")
p.script_title("Every Detail", "One Home Base", title_size=72, top=60)
p.subtitle("WEDDING PARTY + STATIONERY + LOGISTICS", top=200)
frames6 = [("wedding-party.png", "WEDDING PARTY", "Track roles, attire, and who's confirmed", LAVENDER),
           ("stationery.png", "STATIONERY", "Design and print status, piece by piece", CREAM),
           ("transportation.png", "LOGISTICS", "Hotel blocks and transportation, together", POWDER)]
gap6, x06, y06 = 34, 70, 300
fw6 = (1200 - 2 * 70 - 2 * gap6) / 3
fh6 = fw6 / 1.35
for i, (ss, label, caption, color) in enumerate(frames6):
    bx0 = x06 + i * (fw6 + gap6)
    box = (bx0, y06, bx0 + fw6, y06 + fh6)
    p.tablet(ss, box)
    p.pill(label, bx0 + fw6 / 2 - len(label) * 5, y06 - 28, color, 16)
    p.raw(f'<div class="catitem" style="top:{y06+fh6+30}px;left:{bx0}px;width:{fw6}px;text-align:center;">{esc(caption)}</div>')
panel6 = (110, y06 + fh6 + 150, 1090, y06 + fh6 + 150 + 380)
p.panel_open(panel6)
bullets6 = ["**Wedding party roles sync** with your Guest List automatically",
            "**Stationery costs roll up** into your Wedding Budget tab",
            "**Every logistics detail** lives in the same file as everything else"]
for i, b in enumerate(bullets6):
    p.bullet(0, i * 100, b, panel6[2] - panel6[0] - 100)
p.panel_close()
bar_top6 = panel6[3] + 65
p.trust_bar([(TRUST_ICONS["sync"], "Everything Stays In Sync"), (TRUST_ICONS["download"], "Instant Download"),
             (TRUST_ICONS["sheet"], "Excel + Google Sheets")], bar_top6)
p.dots(6)
PAGES.append(p)

# =====================================================================
# PAGE 7 - Wedding Theme grid
# =====================================================================
p = Page("Wedding Theme")
p.script_title("Design Your", "Wedding Look", title_size=72, top=60)
p.subtitle("MOODBOARD + DECOR + FLOWERS + ATTIRE", top=200)
items7 = [("moodboard.png", "Moodboard", "Pin every inspiration image in one place", BLUSH),
          ("decor.png", "Decor Inventory", "Track cost and status for every rented piece", SAGE),
          ("flowers.png", "Flower Arrangements", "Every bouquet and centerpiece, costed out", PEACH),
          ("attire-makeup.png", "Attire &amp; Makeup", "Looks organized by event and by person", LAVENDER)]
gap7, x07 = 40, 80
fw7 = (1200 - 2 * 80 - gap7) / 2
fh7 = fw7 / 1.35
y_rows7 = [300, 300 + fh7 + 120]
for i, (ss, label, caption, color) in enumerate(items7):
    col, row = i % 2, i // 2
    bx0 = x07 + col * (fw7 + gap7)
    by0 = y_rows7[row]
    box = (bx0, by0, bx0 + fw7, by0 + fh7)
    p.tablet(ss, box)
    p.pill(label, bx0 + fw7 / 2 - len(label) * 5.5, by0 - 28, color, 17)
    p.raw(f'<div class="catitem" style="top:{by0+fh7+26}px;left:{bx0}px;width:{fw7}px;text-align:center;">{esc(caption) if "&amp;" not in caption else caption}</div>')
bar_top7 = y_rows7[1] + fh7 + 110
p.trust_bar([(TRUST_ICONS["sync"], "Cohesive By Design"), (TRUST_ICONS["download"], "Instant Download"),
             (TRUST_ICONS["sheet"], "Excel + Google Sheets")], bar_top7)
p.dots(7)
PAGES.append(p)

# =====================================================================
# PAGE 8 - What Will You Get
# =====================================================================
p = Page("What Will You Get")
p.script_title("Everything You Need", "What Will You Get?", title_size=66, top=56)
p.subtitle("33 TABS. 1 FILE. EVERY DETAIL COVERED.", top=190)
CATEGORIES = [
    ("Get Started", SAGE, ["Get Started", "Dashboard", "Smart Calendar"]),
    ("Budget &amp; Vendors", LAVENDER, ["Wedding Budget", "Vendor Selection", "Venue Comparison"]),
    ("Guest Management", BLUSH, ["Guest List", "Reception Seating Plan", "Rehearsal Dinner Seating"]),
    ("Wedding Planning", PEACH, ["Wedding Checklist", "Wedding Itinerary", "Wedding Activities", "Aisle Order"]),
    ("Decor &amp; Aesthetics", CREAM, ["Moodboard", "Decor Inventory", "Flower Arrangements", "Attire and Makeup"]),
    ("Wedding Logistics", POWDER, ["Accommodation", "Transportation", "Packing List"]),
    ("Wedding Stationery", SAGE, ["Stationery Checklist", "Save the Date"]),
    ("Entertainment &amp; Food", LAVENDER, ["Music Planner", "Food and Drinks", "Photo and Video Shot List"]),
    ("Wedding Party &amp; Gifts", BLUSH, ["Wedding Party", "Wedding Party Gifts", "Wedding Registry", "Gifts and Thank You"]),
    ("Pre-Wedding Events", PEACH, ["Engagement Party", "Bridal Shower", "Bachelor(ette) Planner"]),
    ("Post-Wedding", CREAM, ["Honeymoon Planner"]),
]
col_assign = [[], [], []]
col_load = [0, 0, 0]
for cat in CATEGORIES:
    load = 1.6 + len(cat[2])
    idx = col_load.index(min(col_load))
    col_assign[idx].append(cat)
    col_load[idx] += load
col_w8 = 360
gap8 = 30
x08 = (W - (col_w8 * 3 + gap8 * 2)) / 2
y_top8 = 280
for c, cats in enumerate(col_assign):
    x = x08 + c * (col_w8 + gap8)
    y = y_top8
    for label, color, tabs in cats:
        p.raw(f'<div class="catbar" style="top:{y}px;left:{x}px;background:{color};"></div>'
              f'<div class="catlabel" style="top:{y-2}px;left:{x+22}px;">{label}</div>')
        y += 46
        for t in tabs:
            p.raw(f'<div class="catdot" style="top:{y+9}px;left:{x+24}px;"></div>'
                  f'<div class="catitem" style="top:{y}px;left:{x+43}px;">{esc(t)}</div>')
            y += 37
        y += 30
p.raw(f'<div class="catlabel" style="top:1100px;left:110px;width:980px;text-align:center;font-size:27px;">'
      f'Everything you need to plan the wedding you actually want, in one file.</div>')
badges8 = ["Excel + Google Sheets", "Instant Digital Download", "LGBTQ+ Friendly", "Editable Colors &amp; Text"]
bw8, bh8, bgap8 = 264, 78, 20
bx08 = (W - (bw8 * 4 + bgap8 * 3)) / 2
trust_y8 = 1210
for i, label in enumerate(badges8):
    bx = bx08 + i * (bw8 + bgap8)
    p.raw(f'<div class="badgechip" style="top:{trust_y8}px;left:{bx}px;width:{bw8}px;height:{bh8}px;">{label}</div>')
dark_y8 = trust_y8 + bh8 + 40
p.raw(f'<div class="darkbar" style="top:{dark_y8}px;height:90px;">'
      f'<span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>'
      f'MADE FOR COUPLES PLANNING THE WEDDING THEY ACTUALLY WANT</div>')
p.dots(8)
PAGES.append(p)

# =====================================================================
body = "\n".join(pg.render() for pg in PAGES)
html = f"""<title>Wedding Planner Etsy Listing Images</title>
<style>{CSS}</style>
{body}
"""

with open("/home/user/wedding-planner-etsy/canva-import/all-8-images.html", "w") as f:
    f.write(html)
print("Wrote", len(html), "bytes,", len(PAGES), "pages")
