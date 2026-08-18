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
    sample_items = ["Save the Dates", "Invitation Suite", "RSVP Cards", "Ceremony Programs", "Menu Cards",
                     "Place Cards", "Table Numbers", "Welcome Sign", "Thank You Cards", "Seating Chart"]
    n = 20
    last = first + n - 1
    for i in range(n):
        r = first + i
        if i < len(sample_items):
            ws.cell(row=r, column=2, value=sample_items[i])
        ws.cell(row=r, column=3, value=1)
        ws.cell(row=r, column=4, value="Not Started")
        ws.cell(row=r, column=5, value="Not Ordered")
        ws.cell(row=r, column=6, value=False)
        ws.cell(row=r, column=8).number_format = DATE_FMT
        ws.cell(row=r, column=9, value=0).number_format = CURRENCY_FMT
        ws.cell(row=r, column=10, value=0).number_format = CURRENCY_FMT
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

    helper_col = 13
    hr = kpi_row
    ws.cell(row=hr, column=helper_col, value="Design Status").font = f_header()
    ws.cell(row=hr, column=helper_col + 1, value="Count").font = f_header()
    for i, st in enumerate(DESIGN_STATUS):
        ws.cell(row=hr + 1 + i, column=helper_col, value=st)
        ws.cell(row=hr + 1 + i, column=helper_col + 1, value=f"=COUNTIF($D${first}:$D${last},{ws.cell(row=hr+1+i, column=helper_col).coordinate})")
    dend = hr + len(DESIGN_STATUS)
    letter_c = get_column_letter(helper_col); letter_v = get_column_letter(helper_col + 1)
    make_bar(ws, "Design Status", f"'Stationery Checklist'!${letter_c}${hr+1}:${letter_c}${dend}",
             f"'Stationery Checklist'!${letter_v}${hr}:${letter_v}${dend}", "M4", width=12, height=7)

    hr2 = dend + 2
    ws.cell(row=hr2, column=helper_col, value="Print Status").font = f_header()
    ws.cell(row=hr2, column=helper_col + 1, value="Count").font = f_header()
    for i, st in enumerate(PRINT_STATUS):
        ws.cell(row=hr2 + 1 + i, column=helper_col, value=st)
        ws.cell(row=hr2 + 1 + i, column=helper_col + 1, value=f"=COUNTIF($E${first}:$E${last},{ws.cell(row=hr2+1+i, column=helper_col).coordinate})")
    pend = hr2 + len(PRINT_STATUS)
    make_bar(ws, "Print Status", f"'Stationery Checklist'!${letter_c}${hr2+1}:${letter_c}${pend}",
             f"'Stationery Checklist'!${letter_v}${hr2}:${letter_v}${pend}", "M17", width=12, height=7)

    hr3 = pend + 2
    ws.cell(row=hr3, column=helper_col, value="Category").font = f_header()
    ws.cell(row=hr3, column=helper_col + 1, value="Cost").font = f_header()
    for i, cat in enumerate(STATIONERY_CATEGORY):
        ws.cell(row=hr3 + 1 + i, column=helper_col, value=cat)
        ws.cell(row=hr3 + 1 + i, column=helper_col + 1, value=f"=SUMIFS($K${first}:$K${last},$A${first}:$A${last},{ws.cell(row=hr3+1+i, column=helper_col).coordinate})")
    cend = hr3 + len(STATIONERY_CATEGORY)
    make_donut(ws, "Cost by Category", f"'Stationery Checklist'!${letter_c}${hr3+1}:${letter_c}${cend}",
               f"'Stationery Checklist'!${letter_v}${hr3+1}:${letter_v}${cend}", "R4", width=10, height=8)

    freeze_header(ws, header_row)
    set_col_widths(ws, {"A": 18, "B": 20, "C": 10, "D": 14, "E": 14, "F": 12, "G": 18, "H": 14, "I": 14, "J": 14, "K": 12})


def build_save_the_date(wb):
    ws = new_sheet(wb, "Save the Date", tab_color=BLUSH)
    row = title_banner(ws, "SAVE THE DATE", BLUSH, row=1, col_start=1, col_end=6, size=16)
    row += 1
    labels = ["Fully Automated", "3 Options", "Ready to Share"]
    for i, lab in enumerate(labels):
        col = 1 + i * 2
        ws.merge_cells(start_row=row, start_column=col, end_row=row, end_column=col + 1)
        c = ws.cell(row=row, column=col, value=lab)
        c.font = f_header()
        c.fill = fill(BLUSH)
        c.alignment = CENTER
    row += 1
    for i in range(3):
        col = 1 + i * 2
        ws.merge_cells(start_row=row, start_column=col, end_row=row + 8, end_column=col + 1)
        ph = ws.cell(row=row, column=col, value=f"[ Save the Date mockup {i+1} ]")
        ph.font = f_body(italic=True, color="9A9A9A")
        ph.alignment = CENTER
        ph.fill = fill(OFFWHITE)
        for rr in range(row, row + 9):
            for cc in (col, col + 1):
                ws.cell(row=rr, column=cc).border = BORDER_ALL
    row += 10
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
