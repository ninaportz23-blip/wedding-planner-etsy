# -*- coding: utf-8 -*-
"""Tabs 25-28: Accommodation, Transportation, Stationery Checklist, Save the Date."""
from lib import *
from data_lists import ACCOMMODATION_LIST, STATIONERY_CATEGORY, DESIGN_STATUS, PRINT_STATUS

def build_accommodation(wb, dv_named, guest_meta):
    ws = new_sheet(wb, "Accommodation", tab_color=POWDER)
    row = title_banner(ws, "WEDDING LOGISTICS: ACCOMMODATION", POWDER, row=1, col_start=1, col_end=5, size=15)
    row += 1
    gfr, glr = guest_meta["first_data_row"], guest_meta["last_data_row"]

    ws.cell(row=row, column=1, value="GUESTS STILL NEEDING A ROOM").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
    ws.cell(row=row, column=1).fill = fill(CREAM)
    ws.cell(row=row, column=2).fill = fill(CREAM)
    row += 1
    hdr0 = table_header(ws, row, 1, ["Confirmed Guest", "Has Room?"], CREAM)
    first0 = hdr0
    n0 = min(30, glr - gfr + 1)
    last0 = first0 + n0 - 1
    for i in range(n0):
        r = first0 + i
        gr = gfr + i
        ws.cell(row=r, column=1, value=f"=IF('Guest List'!$F{gr}=\"Yes\",'Guest List'!$A{gr},\"\")")
        for cc in (1, 2):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
    row_after_note = last0 + 2
    set_col_widths(ws, {"A": 20, "B": 12})

    ws.cell(row=row_after_note, column=1, value="HOTEL ACCOMMODATION").font = f_header()
    ws.merge_cells(start_row=row_after_note, start_column=1, end_row=row_after_note, end_column=5)
    ws.cell(row=row_after_note, column=1).fill = fill(POWDER)
    for cc in range(1, 6):
        ws.cell(row=row_after_note, column=cc).fill = fill(POWDER)
    row2 = row_after_note + 1
    hdr = table_header(ws, row2, 1, ["Guest Name", "Accommodation Name", "Room Number", "Check-in Date/Time", "Check-out Date/Time"], POWDER)
    first = hdr
    n = 30
    last = first + n - 1
    for i in range(n):
        r = first + i
        for cc in range(1, 6):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
        ws.cell(row=r, column=4).number_format = "DD-MMM-YYYY HH:MM"
        ws.cell(row=r, column=5).number_format = "DD-MMM-YYYY HH:MM"
    dv_named(ws, f"B{first}:B{last}", "AccommodationList")
    for i in range(n0):
        r = first0 + i
        ws.cell(row=r, column=2, value=f'=IF(A{r}="","",IF(COUNTIF(A{first}:A{last},A{r})>0,"Yes","No"))')
    ws.conditional_formatting.add(f"B{first0}:B{last0}", FormulaRule(formula=[f'EXACT(B{first0},"No")'], fill=fill(STATUS_RED)))
    set_col_widths(ws, {"C": 12, "D": 20, "E": 20})
    freeze_header(ws, hdr)


def build_transportation(wb, dv_named):
    ws = new_sheet(wb, "Transportation", tab_color=SAGE)
    row = title_banner(ws, "WEDDING LOGISTICS: TRANSPORTATION", SAGE, row=1, col_start=1, col_end=8, size=15)
    row += 1
    hdr = table_header(ws, row, 1, ["Transportation For", "Vendor Name", "Vendor Contact", "Pickup Location",
                                     "Dropoff Location", "Pickup Date", "Pickup Time", "Notes"], SAGE)
    first = hdr
    n = 20
    last = first + n - 1
    for i in range(n):
        r = first + i
        ws.cell(row=r, column=6).number_format = DATE_FMT
        ws.cell(row=r, column=7).number_format = "HH:MM"
        for cc in range(1, 9):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    from data_lists import VENDOR_CATEGORY
    dv_named(ws, f"B{first}:B{last}", "VendorCategory")
    set_col_widths(ws, {"A": 20, "B": 18, "C": 16, "D": 20, "E": 20, "F": 14, "G": 12, "H": 20})
    freeze_header(ws, hdr)


def build_stationery(wb, dv_named):
    ws = new_sheet(wb, "Stationery Checklist", tab_color=CREAM)
    row = title_banner(ws, "WEDDING STATIONERY: CHECKLIST", CREAM, row=1, col_start=1, col_end=10, size=15)
    row += 1
    kpi_row = row
    kpi_box(ws, kpi_row, 1, "PROGRESS", None, CREAM, width_cols=2)
    row = kpi_row + 3

    header_row = row
    table_header(ws, header_row, 1, ["Category", "Item Name", "Quantity", "Design Status", "Printing Status",
                                      "Overall Status", "Vendor / Source", "Due Date", "Total Design Cost",
                                      "Print Cost per Unit", "Total Cost"], CREAM)
    first = header_row + 1
    # (item, category, qty, design status, print status, design cost, print cost/unit)
    sample_items = [
        ("Save the Dates", "Before the Wedding", 80, "Completed", "Printed", 60, 1.2),
        ("Invitation Suite", "Before the Wedding", 80, "Completed", "Ordered", 120, 3.5),
        ("RSVP Cards", "Before the Wedding", 80, "In Progress", "Not Ordered", 40, 0.8),
        ("Ceremony Programs", "Wedding Day", 60, "In Progress", "Not Ordered", 50, 1.1),
        ("Menu Cards", "Wedding Day", 60, "Not Started", "Not Ordered", 0, 0),
        ("Place Cards", "Wedding Day", 80, "Not Started", "Not Ordered", 0, 0),
        ("Table Numbers", "Wedding Day", 15, "Completed", "Printed", 30, 2.0),
        ("Welcome Sign", "Wedding Day", 1, "In Progress", "Not Ordered", 45, 0),
        ("Thank You Cards", "After the Wedding", 80, "Not Started", "Not Needed", 0, 0),
        ("Seating Chart", "Wedding Day", 1, "Completed", "Printed", 55, 0),
    ]
    n = 20
    last = first + n - 1
    for i in range(n):
        r = first + i
        if i < len(sample_items):
            itm, cat, qty, dstat, pstat, dcost, pcost = sample_items[i]
            ws.cell(row=r, column=1, value=cat)
            ws.cell(row=r, column=2, value=itm)
            ws.cell(row=r, column=3, value=qty)
            ws.cell(row=r, column=4, value=dstat)
            ws.cell(row=r, column=5, value=pstat)
            ws.cell(row=r, column=9, value=dcost).number_format = CURRENCY_FMT
            ws.cell(row=r, column=10, value=pcost).number_format = CURRENCY_FMT
        else:
            ws.cell(row=r, column=3, value=1)
            ws.cell(row=r, column=4, value="Not Started")
            ws.cell(row=r, column=5, value="Not Ordered")
            ws.cell(row=r, column=9, value=0).number_format = CURRENCY_FMT
            ws.cell(row=r, column=10, value=0).number_format = CURRENCY_FMT
        ws.cell(row=r, column=6, value=False)
        ws.cell(row=r, column=8).number_format = DATE_FMT
        ws.cell(row=r, column=11, value=f"=I{r}+(J{r}*C{r})").number_format = CURRENCY_FMT
        for cc in range(1, 12):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    dv_named(ws, f"A{first}:A{last}", "StationeryCategory")
    dv_named(ws, f"D{first}:D{last}", "DesignStatus")
    dv_named(ws, f"E{first}:E{last}", "PrintStatus")
    add_checkbox_col(ws, f"F{first}:F{last}")
    ws.conditional_formatting.add(f"D{first}:D{last}", FormulaRule(formula=[f'EXACT(D{first},"Completed")'], fill=fill(STATUS_GREEN)))
    ws.conditional_formatting.add(f"D{first}:D{last}", FormulaRule(formula=[f'EXACT(D{first},"Not Started")'], fill=fill(STATUS_RED)))
    ws.conditional_formatting.add(f"E{first}:E{last}", FormulaRule(formula=[f'EXACT(E{first},"Printed")'], fill=fill(STATUS_GREEN)))
    ws.conditional_formatting.add(f"F{first}:F{last}", FormulaRule(formula=[f"F{first}=ChkVal"], fill=fill(STATUS_GREEN)))

    v = ws.cell(row=kpi_row + 1, column=1, value=f'=IFERROR(COUNTIF(F{first}:F{last},ChkVal)/COUNTA(B{first}:B{last}),0)')
    v.number_format = "0%"; v.font = f_kpi_number(size=15)

    # Chart source data lives far to the right and hidden, so it never overlaps
    # the table or the charts themselves.
    helper_col = 30  # AD
    hr = 2
    ws.cell(row=hr, column=helper_col, value="Design Status")
    ws.cell(row=hr, column=helper_col + 1, value="Count")
    for i, st in enumerate(DESIGN_STATUS):
        ws.cell(row=hr + 1 + i, column=helper_col, value=st)
        ws.cell(row=hr + 1 + i, column=helper_col + 1, value=f"=COUNTIF($D${first}:$D${last},{ws.cell(row=hr+1+i, column=helper_col).coordinate})")
    dend = hr + len(DESIGN_STATUS)
    letter_c = get_column_letter(helper_col); letter_v = get_column_letter(helper_col + 1)

    hr2 = dend + 2
    ws.cell(row=hr2, column=helper_col, value="Print Status")
    ws.cell(row=hr2, column=helper_col + 1, value="Count")
    for i, st in enumerate(PRINT_STATUS):
        ws.cell(row=hr2 + 1 + i, column=helper_col, value=st)
        ws.cell(row=hr2 + 1 + i, column=helper_col + 1, value=f"=COUNTIF($E${first}:$E${last},{ws.cell(row=hr2+1+i, column=helper_col).coordinate})")
    pend = hr2 + len(PRINT_STATUS)

    hr3 = pend + 2
    ws.cell(row=hr3, column=helper_col, value="Category")
    ws.cell(row=hr3, column=helper_col + 1, value="Cost")
    for i, cat in enumerate(STATIONERY_CATEGORY):
        ws.cell(row=hr3 + 1 + i, column=helper_col, value=cat)
        ws.cell(row=hr3 + 1 + i, column=helper_col + 1, value=f"=SUMIFS($K${first}:$K${last},$A${first}:$A${last},{ws.cell(row=hr3+1+i, column=helper_col).coordinate})")
    cend = hr3 + len(STATIONERY_CATEGORY)

    for hcol in (helper_col, helper_col + 1):
        ws.column_dimensions[get_column_letter(hcol)].hidden = False

    # Charts stacked in a clean column to the right of the table (cols A-K).
    make_bar(ws, "Design Status", f"'Stationery Checklist'!${letter_c}${hr+1}:${letter_c}${dend}",
             f"'Stationery Checklist'!${letter_v}${hr}:${letter_v}${dend}", "M4", width=9.5, height=6.4)
    make_bar(ws, "Printing Status", f"'Stationery Checklist'!${letter_c}${hr2+1}:${letter_c}${pend}",
             f"'Stationery Checklist'!${letter_v}${hr2}:${letter_v}${pend}", "M20", width=9.5, height=6.4)
    make_donut(ws, "Cost by Category", f"'Stationery Checklist'!${letter_c}${hr3+1}:${letter_c}${cend}",
               f"'Stationery Checklist'!${letter_v}${hr3+1}:${letter_v}${cend}", "M36", width=9.5, height=6.8)

    set_col_widths(ws, {"A": 18, "B": 20, "C": 10, "D": 15, "E": 15, "F": 13, "G": 18, "H": 14, "I": 15, "J": 15, "K": 13})


def build_save_the_date(wb):
    ws = new_sheet(wb, "Save the Date", tab_color=BLUSH)
    row = title_banner(ws, "Save the Date", BLUSH, row=1, col_start=1, col_end=6, size=20)
    row += 1
    intro = ws.cell(row=row, column=1, value="Mock up your save-the-date options here. Click a frame, then Insert › Picture › Place in cell to drop your design in.")
    intro.font = f_body(italic=True, size=9, color="7A7A7A")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    row += 2
    set_col_widths(ws, {get_column_letter(c): 14 for c in range(1, 7)})
    labels = ["Design 1", "Design 2", "Design 3"]
    cards = ["card_blush.png", "card_cream.png", "card_sage.png"]
    img_rows = 12
    col_px = int(14 * 7 + 5)
    block_w = col_px * 2 - 8
    block_h = int(block_w * 320 / 236)
    for r in range(row, row + img_rows):
        ws.row_dimensions[r].height = (block_h / img_rows) / 1.333
    for i, lab in enumerate(labels):
        col = 1 + i * 2
        ws.merge_cells(start_row=row, start_column=col, end_row=row + img_rows - 1, end_column=col + 1)
        for rr in range(row, row + img_rows):
            for cc in (col, col + 1):
                ws.cell(row=rr, column=cc).fill = fill(WHITE)
        embed_image(ws, cards[i], f"{get_column_letter(col)}{row}", block_w, block_h)
        lr = row + img_rows
        ws.merge_cells(start_row=lr, start_column=col, end_row=lr, end_column=col + 1)
        lc = ws.cell(row=lr, column=col, value=lab)
        lc.font = Font(name=FONT_SERIF, size=12, color=CHARCOAL); lc.alignment = CENTER
        ws.row_dimensions[lr].height = 20
    row += img_rows + 2
    ws.cell(row=row, column=1, value="WORDING NOTES").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    ws.cell(row=row, column=1).fill = fill(CREAM)
    for cc in range(1, 7):
        ws.cell(row=row, column=cc).fill = fill(CREAM)
    row += 1
    ws.merge_cells(start_row=row, start_column=1, end_row=row + 3, end_column=6)
    ws.cell(row=row, column=1, value="Draft your save the date wording here.").font = f_body()
    ws.cell(row=row, column=1).alignment = LEFT_TOP
    for rr in range(row, row + 4):
        for cc in range(1, 7):
            ws.cell(row=rr, column=cc).border = BORDER_ALL
    row += 5
    ws.cell(row=row, column=1, value="MAILING TIMELINE NOTES").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    ws.cell(row=row, column=1).fill = fill(CREAM)
    for cc in range(1, 7):
        ws.cell(row=row, column=cc).fill = fill(CREAM)
    row += 1
    ws.merge_cells(start_row=row, start_column=1, end_row=row + 3, end_column=6)
    ws.cell(row=row, column=1, value="Save the dates typically mail 6 to 8 months before the wedding, sooner for destination weddings.").font = f_body()
    ws.cell(row=row, column=1).alignment = LEFT_TOP
    for rr in range(row, row + 4):
        for cc in range(1, 7):
            ws.cell(row=rr, column=cc).border = BORDER_ALL
    set_col_widths(ws, {get_column_letter(c): 14 for c in range(1, 7)})
