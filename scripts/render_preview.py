#!/usr/bin/env python3
"""Approximate xlsx -> PNG previewer (LibreOffice is unavailable in this env).

Reads real column widths, row heights, merges, fills, fonts and alignment and
draws each sheet close to how Excel/Sheets would, including Excel's "overflow
into empty neighbours, else clip" behaviour, so column-width / clipping / wrap
problems are visible. Not pixel-perfect; good enough to verify layout.
"""
import os
import sys
import warnings

import openpyxl
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.worksheet.formula import ArrayFormula
from PIL import Image, ImageDraw, ImageFont

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "..", "qa_screens")
os.makedirs(OUT, exist_ok=True)

SERIF = os.path.join(FONT_DIR, "PlayfairDisplay-Bold.ttf")
SERIF_BLACK = os.path.join(FONT_DIR, "PlayfairDisplay-Black.ttf")
SANS = os.path.join(FONT_DIR, "Poppins-Regular.ttf")
SANS_SB = os.path.join(FONT_DIR, "Poppins-SemiBold.ttf")
SANS_B = os.path.join(FONT_DIR, "Poppins-Bold.ttf")
_cache = {}


def font(bold, serif, italic, size_pt):
    px = max(9, int(round(size_pt * 1.34)))
    if serif:
        path = SERIF_BLACK if bold else SERIF
    else:
        path = SANS_B if bold else (SANS_SB if italic else SANS)
    key = (path, px)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, px)
    return _cache[key]


def col_px(w):
    if w is None:
        w = 8.43
    return int(round(w * 7)) + 5


def row_px(h):
    if h is None:
        h = 15.0
    return int(round(h * 1.34))


def rgb(color, default=(58, 58, 58)):
    try:
        v = color.rgb if color else None
        if isinstance(v, str) and len(v) == 8:
            return (int(v[2:4], 16), int(v[4:6], 16), int(v[6:8], 16))
    except Exception:
        pass
    return default


def cval(c):
    v = c.value
    if isinstance(v, ArrayFormula):
        v = v.text
    if v is None:
        return ""
    if isinstance(v, float):
        if v == int(v):
            v = int(v)
    return str(v)


def render(path, sheet_names=None, max_rows=34, max_cols=None):
    wb = openpyxl.load_workbook(path)
    names = sheet_names or wb.sheetnames
    outputs = []
    for name in names:
        ws = wb[name]
        # used bounds
        mrow = min(ws.max_row, max_rows)
        mcol = ws.max_column
        if max_cols:
            mcol = min(mcol, max_cols)
        mcol = min(mcol, 40)
        # x/y offsets (hidden col/row -> 0 width, like Excel)
        xs = [0]
        for ci in range(1, mcol + 1):
            cd = ws.column_dimensions[get_column_letter(ci)]
            w = 0 if cd.hidden else cd.width
            xs.append(xs[-1] + (0 if cd.hidden else col_px(w)))
        ys = [0]
        for ri in range(1, mrow + 1):
            rd = ws.row_dimensions[ri]
            ys.append(ys[-1] + (0 if rd.hidden else row_px(rd.height)))
        W, H = xs[-1] + 1, ys[-1] + 1
        img = Image.new("RGB", (W, H), (255, 255, 255))
        d = ImageDraw.Draw(img)

        # merged map: top-left -> (rowspan cols)
        merged_anchor = {}
        covered = set()
        for mr in ws.merged_cells.ranges:
            if mr.min_row > mrow or mr.min_col > mcol:
                continue
            merged_anchor[(mr.min_row, mr.min_col)] = (mr.max_row, mr.max_col)
            for rr in range(mr.min_row, mr.max_row + 1):
                for cc in range(mr.min_col, mr.max_col + 1):
                    if (rr, cc) != (mr.min_row, mr.min_col):
                        covered.add((rr, cc))

        def cell_box(r, c):
            r2, c2 = r, c
            if (r, c) in merged_anchor:
                r2, c2 = merged_anchor[(r, c)]
            x0 = xs[c - 1]
            x1 = xs[min(c2, mcol)] if c2 <= mcol else xs[mcol]
            y0 = ys[r - 1]
            y1 = ys[min(r2, mrow)] if r2 <= mrow else ys[mrow]
            return x0, y0, x1, y1

        # first pass: fills
        for r in range(1, mrow + 1):
            for c in range(1, mcol + 1):
                if (r, c) in covered:
                    continue
                cell = ws.cell(r, c)
                x0, y0, x1, y1 = cell_box(r, c)
                fl = cell.fill
                if fl is not None and fl.patternType == "solid" and x1 > x0 and y1 > y0:
                    d.rectangle((x0, y0, x1 - 1, y1 - 1), fill=rgb(fl.fgColor, (255, 255, 255)))
        # grid (very light) for reference
        for r in range(1, mrow + 1):
            d.line((0, ys[r - 1], W, ys[r - 1]), fill=(238, 236, 232))
        for c in range(1, mcol + 1):
            d.line((xs[c - 1], 0, xs[c - 1], H), fill=(238, 236, 232))

        # second pass: text (with Excel overflow-into-empty-neighbour)
        for r in range(1, mrow + 1):
            for c in range(1, mcol + 1):
                if (r, c) in covered:
                    continue
                cell = ws.cell(r, c)
                txt = cval(cell)
                if not txt:
                    continue
                x0, y0, x1, y1 = cell_box(r, c)
                fnt = cell.font
                is_serif = fnt and fnt.name in ("Lora", "PlayfairDisplay", "Fraunces")
                f = font(bool(fnt and fnt.bold), is_serif, bool(fnt and fnt.italic),
                         float(fnt.size) if fnt and fnt.size else 11)
                col = rgb(fnt.color if fnt else None)
                al = cell.alignment
                wrap = bool(al and al.wrapText)
                halign = (al.horizontal if al and al.horizontal else "general")
                merged = (r, c) in merged_anchor
                is_formula = txt.startswith("=")
                if is_formula:
                    # show formulas as a neutral short stub so their length
                    # never masks the static layout being verified
                    txt = "0.00"
                    col = (150, 150, 150)
                avail = x1 - x0 - 8
                # overflow into empty right neighbours when not wrapped/merged
                if not wrap and not merged and not is_formula:
                    cc = c + 1
                    while cc <= mcol and cval(ws.cell(r, cc)) == "" and (r, cc) not in covered:
                        avail += xs[cc] - xs[cc - 1]
                        cc += 1
                lines = _wrap(txt, f, avail) if wrap else [_clip(txt, f, avail)]
                th = sum(f.getbbox(ln)[3] - f.getbbox(ln)[1] + 4 for ln in lines)
                cy = y0 + max(2, ((y1 - y0) - th) // 2)
                va = al.vertical if al and al.vertical else None
                if va == "top":
                    cy = y0 + 3
                for ln in lines:
                    tw = f.getlength(ln)
                    if halign == "center":
                        tx = x0 + ((x1 - x0) - tw) / 2
                    elif halign == "right":
                        tx = x1 - tw - 6
                    else:
                        indent = (al.indent or 0) * 7 if al else 0
                        tx = x0 + 5 + indent
                    d.text((tx, cy), ln, font=f, fill=col)
                    cy += f.getbbox(ln)[3] - f.getbbox(ln)[1] + 4

        out = os.path.join(OUT, "preview_" + name.split(" ")[-1].replace("/", "_") + ".png")
        # nicer filename
        safe = "".join(ch for ch in name if ch.isalnum() or ch in " -_").strip().replace(" ", "_")
        out = os.path.join(OUT, f"preview_{safe}.png")
        img.save(out)
        outputs.append(out)
        print("wrote", out, f"({W}x{H})")
    return outputs


def _clip(txt, f, avail):
    if f.getlength(txt) <= avail:
        return txt
    while txt and f.getlength(txt + "…") > avail:
        txt = txt[:-1]
    return txt + "…" if txt else ""


def _wrap(txt, f, avail):
    out = []
    for para in txt.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            t = (cur + " " + w).strip()
            if f.getlength(t) <= avail or not cur:
                cur = t
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    return out or [""]


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "dist", "Calm-Money-Reset-Tracker.xlsx")
    sheets = sys.argv[2:] or None
    render(path, sheets)
