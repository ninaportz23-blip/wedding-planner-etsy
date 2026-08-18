# -*- coding: utf-8 -*-
"""Tab 1: Get Started - welcome, couple info, instructions, table of contents."""
from lib import *

def build_get_started_core(wb):
    ws = new_sheet(wb, "Get Started", tab_color=LAVENDER)
    row = title_banner(ws, "WELCOME TO YOUR WEDDING PLANNER", LAVENDER, row=1, col_start=1, col_end=8, size=18)
    # NOTE: fixed cells A4:D4 (couple names / wedding date / hashtag) are referenced
    # by formulas on many other tabs (Checklist, Dashboard, Smart Calendar). Row 3
    # holds the labels, row 4 the values. Do not move these without updating those tabs.
    row = 3

    ws.cell(row=row, column=1, value="Partner 1 Name").font = f_kpi_label()
    ws.cell(row=row, column=2, value="Partner 2 Name").font = f_kpi_label()
    ws.cell(row=row, column=3, value="Wedding Date").font = f_kpi_label()
    ws.cell(row=row, column=4, value="Wedding Hashtag").font = f_kpi_label()
    for cc in range(1, 5):
        ws.cell(row=row, column=cc).fill = fill(BLUSH)
        ws.cell(row=row, column=cc).border = BORDER_ALL
        ws.cell(row=row, column=cc).alignment = CENTER
    row += 1
    ws.cell(row=row, column=1, value="Taylor")
    ws.cell(row=row, column=2, value="Jordan")
    ws.cell(row=row, column=3, value="__/__/____")
    ws.cell(row=row, column=3).number_format = DATE_FMT
    import datetime
    ws.cell(row=row, column=3, value=datetime.date.today() + datetime.timedelta(days=300))
    ws.cell(row=row, column=4, value="#TaylorAndJordan2026")
    for cc in range(1, 5):
        ws.cell(row=row, column=cc).font = f_body(size=12, bold=True)
        ws.cell(row=row, column=cc).fill = fill(WHITE)
        ws.cell(row=row, column=cc).border = BORDER_ALL
        ws.cell(row=row, column=cc).alignment = CENTER
    ws.row_dimensions[row].height = 22
    row += 2

    ws.cell(row=row, column=1, value="Wedding Photo Placeholder").font = f_kpi_label()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
    ws.cell(row=row, column=1).fill = fill(SAGE)
    row += 1
    ws.merge_cells(start_row=row, start_column=1, end_row=row + 6, end_column=3)
    ph = ws.cell(row=row, column=1, value="[ Insert your favorite photo here: Insert > Image > Cell ]")
    ph.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ph.font = f_body(italic=True, color="9A9A9A")
    ph.fill = fill(OFFWHITE)
    for rr in range(row, row + 7):
        for cc in range(1, 4):
            ws.cell(row=rr, column=cc).border = BORDER_ALL
    photo_end_row = row + 6

    # Instructions block, to the right of the photo
    instr_row = row - 1
    ws.cell(row=instr_row, column=5, value="HOW TO USE THIS PLANNER").font = f_header()
    ws.merge_cells(start_row=instr_row, start_column=5, end_row=instr_row, end_column=8)
    ws.cell(row=instr_row, column=5).fill = fill(POWDER)
    instructions = [
        "1. Fill in your names, wedding date, and hashtag above.",
        "2. Start on the Dashboard tab to see your planning snapshot.",
        "3. Work through the Wedding Checklist tab by timeframe.",
        "4. Add vendors on the Vendor Selection tab. Mark Final Yes and enter the Amount to auto fill your Budget.",
        "5. Add guests on the Guest List tab. RSVPs sync automatically to your Seating Plan.",
        "6. Every dropdown list can be edited on the hidden Lists tab.",
        "7. Tabs with colored banners are organized by wedding planning category. Use the table of contents below to jump to any tab.",
        "8. Video tutorial: [insert your tutorial link here]",
    ]
    ir = instr_row + 1
    for line in instructions:
        ws.cell(row=ir, column=5, value=line).font = f_body(size=10)
        ws.merge_cells(start_row=ir, start_column=5, end_row=ir, end_column=8)
        ws.cell(row=ir, column=5).alignment = LEFT_TOP
        ir += 1

    row = max(photo_end_row, ir) + 2
    toc_start = row
    ws.cell(row=row, column=1, value="TABLE OF CONTENTS").font = f_title(size=14)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=8)
    ws.cell(row=row, column=1).fill = fill(CREAM)
    for cc in range(1, 9):
        ws.cell(row=row, column=cc).fill = fill(CREAM)
    row += 1

    set_col_widths(ws, {"A": 16, "B": 16, "C": 16, "D": 20, "E": 24, "F": 16, "G": 16, "H": 16})
    return ws, row  # row = first empty TOC row


def add_toc_links(ws, start_row, tab_names):
    row = start_row
    col = 1
    per_col_rows = 17
    r = row
    c = col
    for i, name in enumerate(tab_names):
        cell = ws.cell(row=r, column=c, value=f"{i+1}. {name}")
        cell.hyperlink = f"#'{name}'!A1"
        cell.font = Font(name=FONT_NAME, color="6B5CA5", underline="single", size=10)
        cell.alignment = LEFT
        r += 1
        if (i + 1) % per_col_rows == 0:
            r = row
            c += 2
    freeze_header(ws, 1)
