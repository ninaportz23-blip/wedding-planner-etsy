# -*- coding: utf-8 -*-
"""Tabs 29-31: Engagement Party, Bridal Shower, Bachelor(ette) Planner."""
from lib import *
from data_lists import YES_NO_AWAITED, BACHELOR_TYPE, BOOKING_STATUS

def _event_overview(ws, row, color, fields):
    ws.cell(row=row, column=1, value="OVERVIEW").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=8)
    for cc in range(1, 9):
        ws.cell(row=row, column=cc).fill = fill(color)
    row += 1
    for i, (label, val) in enumerate(fields):
        col = 1 + (i % 4) * 2
        r = row + (i // 4)
        c = ws.cell(row=r, column=col, value=label)
        c.font = f_kpi_label()
        c.fill = fill(WHITE)
        c.border = BORDER_ALL
        v = ws.cell(row=r, column=col + 1, value=val)
        v.font = f_body(bold=True)
        v.border = BORDER_ALL
    row += (len(fields) + 3) // 4
    return row + 1

def _stat_cards(ws, row, color, cards):
    for i, (label, formula, fmt) in enumerate(cards):
        v = kpi_box(ws, row, 1 + i * 2, label, None, color, width_cols=2, font_size=13)
        v.value = formula
        if fmt:
            v.number_format = fmt
    return row + 3

def _expense_summary(ws, row, color, sheet_name, categories):
    ws.cell(row=row, column=1, value="EXPENSE SUMMARY").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    for cc in range(1, 5):
        ws.cell(row=row, column=cc).fill = fill(color)
    row += 1
    hdr = table_header(ws, row, 1, ["Category", "Budget", "Actual", "Left"], color)
    first = hdr
    for i, cat in enumerate(categories):
        r = hdr + i
        ws.cell(row=r, column=1, value=cat)
        ws.cell(row=r, column=2, value=0).number_format = CURRENCY_FMT
        ws.cell(row=r, column=3, value=0).number_format = CURRENCY_FMT
        ws.cell(row=r, column=4, value=f"=B{r}-C{r}").number_format = CURRENCY_FMT
        for cc in range(1, 5):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    last = hdr + len(categories) - 1
    total_row = last + 1
    ws.cell(row=total_row, column=1, value="Total").font = f_header()
    for col, letter in [(2, "B"), (3, "C"), (4, "D")]:
        c = ws.cell(row=total_row, column=col, value=f"=SUM({letter}{first}:{letter}{last})")
        c.number_format = CURRENCY_FMT
        c.font = f_header()
    for cc in range(1, 5):
        ws.cell(row=total_row, column=cc).fill = fill(CREAM)
        ws.cell(row=total_row, column=cc).border = BORDER_ALL
    letter_c = "A"; letter_v = "C"
    make_donut(ws, "Expense Breakdown", f"'{sheet_name}'!$A${first}:$A${last}",
               f"'{sheet_name}'!$C${first}:$C${last}", f"F{row}", width=12, height=8)
    return total_row + 2, first, last, total_row

def _guest_rsvp_table(ws, row, color, n=25):
    ws.cell(row=row, column=1, value="GUEST LIST AND RSVP").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
    for cc in range(1, 4):
        ws.cell(row=row, column=cc).fill = fill(color)
    row += 1
    hdr = table_header(ws, row, 1, ["Name", "RSVP", "Notes"], color)
    first = hdr
    for i in range(n):
        r = hdr + i
        for cc in range(1, 4):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    last = hdr + n - 1
    return row, first, last


def build_engagement_party(wb, dv_named):
    ws = new_sheet(wb, "Engagement Party", tab_color=BLUSH)
    row = title_banner(ws, "PRE-WEDDING: ENGAGEMENT PARTY", BLUSH, row=1, col_start=1, col_end=8, size=15)
    row += 1
    row = _event_overview(ws, row, BLUSH, [("Date", ""), ("Time", ""), ("Venue", ""), ("Theme", ""), ("Budget", 2000)])
    kpi_row = row
    row = _stat_cards(ws, kpi_row, BLUSH, [
        ("COUNTDOWN", "=IFERROR('Get Started'!$C$4-TODAY(),\"\")", None),
        ("LEFT TO SPEND", None, CURRENCY_FMT),
        ("LEFT TO BUDGET", None, CURRENCY_FMT),
    ])
    row, efirst, elast, etotal = _expense_summary(ws, row, BLUSH, "Engagement Party",
        ["Venue", "Food and Drinks", "Decor", "Invitations", "Favors", "Other"])
    ws.cell(row=kpi_row + 1, column=3, value=f"=D{etotal}").number_format = CURRENCY_FMT
    ws.cell(row=kpi_row + 1, column=5, value=f"=B{etotal}-C{etotal}").number_format = CURRENCY_FMT
    row, gfirst, glast = _guest_rsvp_table(ws, row, BLUSH)
    dv_named(ws, f"B{gfirst}:B{glast}", "YesNoAwaited")
    ws.conditional_formatting.add(f"B{gfirst}:B{glast}", FormulaRule(formula=[f'EXACT(B{gfirst},"Yes")'], fill=fill(STATUS_GREEN)))
    set_col_widths(ws, {"A": 20, "B": 16, "C": 16, "D": 16, "E": 16, "F": 16, "G": 16, "H": 16})
    freeze_header(ws, 1)


def build_bridal_shower(wb, dv_named):
    ws = new_sheet(wb, "Bridal Shower", tab_color=SAGE)
    row = title_banner(ws, "PRE-WEDDING: BRIDAL SHOWER", SAGE, row=1, col_start=1, col_end=8, size=15)
    row += 1
    row = _event_overview(ws, row, SAGE, [("Date", ""), ("Time", ""), ("Venue", ""), ("Theme", ""), ("Budget", 1200)])
    kpi_row = row
    row = _stat_cards(ws, kpi_row, SAGE, [
        ("COUNTDOWN", "=IFERROR('Get Started'!$C$4-TODAY(),\"\")", None),
        ("LEFT TO SPEND", None, CURRENCY_FMT),
        ("LEFT TO BUDGET", None, CURRENCY_FMT),
    ])
    row, efirst, elast, etotal = _expense_summary(ws, row, SAGE, "Bridal Shower",
        ["Venue", "Food and Drinks", "Decor", "Games and Activities", "Favors", "Other"])
    ws.cell(row=kpi_row + 1, column=3, value=f"=D{etotal}").number_format = CURRENCY_FMT
    ws.cell(row=kpi_row + 1, column=5, value=f"=B{etotal}-C{etotal}").number_format = CURRENCY_FMT
    row, gfirst, glast = _guest_rsvp_table(ws, row, SAGE)
    dv_named(ws, f"B{gfirst}:B{glast}", "YesNoAwaited")
    ws.conditional_formatting.add(f"B{gfirst}:B{glast}", FormulaRule(formula=[f'EXACT(B{gfirst},"Yes")'], fill=fill(STATUS_GREEN)))
    set_col_widths(ws, {"A": 20, "B": 16, "C": 16, "D": 16, "E": 16, "F": 16, "G": 16, "H": 16})
    freeze_header(ws, 1)


def build_bachelor(wb, dv_named):
    ws = new_sheet(wb, "Bachelor(ette) Planner", tab_color=PEACH)
    row = title_banner(ws, "PRE-WEDDING: BACHELOR(ETTE) PLANNER", PEACH, row=1, col_start=1, col_end=8, size=14)
    row += 1
    type_row = row + 1
    row = _event_overview(ws, row, PEACH, [("Type", "Party"), ("Date / # of Days", ""), ("Venue / Location", ""), ("Budget", 1500)])
    dv_named(ws, f"B{type_row}:B{type_row}", "BachelorType")
    kpi_row = row
    row = _stat_cards(ws, kpi_row, PEACH, [
        ("CONFIRMED GUESTS", None, None),
        ("LEFT TO BUDGET", None, CURRENCY_FMT),
    ])
    row, gfirst, glast = _guest_rsvp_table(ws, row, PEACH)
    dv_named(ws, f"B{gfirst}:B{glast}", "YesNoAwaited")
    ws.conditional_formatting.add(f"B{gfirst}:B{glast}", FormulaRule(formula=[f'EXACT(B{gfirst},"Yes")'], fill=fill(STATUS_GREEN)))
    ws.cell(row=kpi_row + 1, column=1, value=f'=COUNTIF(B{gfirst}:B{glast},"Yes")').font = f_kpi_number(size=14)

    ws.cell(row=row, column=1, value="ITINERARY").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
    for cc in range(1, 4):
        ws.cell(row=row, column=cc).fill = fill(CREAM)
    row += 1
    hdr = table_header(ws, row, 1, ["Date", "Time", "Details"], CREAM)
    for i in range(10):
        r = hdr + i
        r_ = r
        for cc in range(1, 4):
            ws.cell(row=r_, column=cc).border = BORDER_ALL
            ws.cell(row=r_, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
        ws.cell(row=r_, column=1).number_format = DATE_FMT
    row = hdr + 11

    ws.cell(row=row, column=1, value="BOOKINGS (ACCOMMODATION OPTIONS)").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=9)
    for cc in range(1, 10):
        ws.cell(row=row, column=cc).fill = fill(POWDER)
    row += 1
    bk_headers = ["Option", "Name", "Phone", "Email", "Booking Date", "Duration", "Status", "Payment Info", "Reference"]
    hdr = table_header(ws, row, 1, bk_headers, POWDER)
    bfirst = hdr
    for i in range(2):
        r = hdr + i
        ws.cell(row=r, column=1, value=f"Option {i+1}")
        ws.cell(row=r, column=5).number_format = DATE_FMT
        for cc in range(1, 10):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    blast = hdr + 1
    dv_named(ws, f"G{bfirst}:G{blast}", "BookingStatus")
    row = blast + 2

    ws.cell(row=row, column=1, value="TRAVEL ARRANGEMENT").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    for cc in range(1, 7):
        ws.cell(row=row, column=cc).fill = fill(SAGE)
    row += 1
    hdr = table_header(ws, row, 1, ["Traveler", "Mode", "Departure", "Arrival", "Confirmation #", "Notes"], SAGE)
    for i in range(8):
        r = hdr + i
        for cc in range(1, 7):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    row = hdr + 9

    ws.cell(row=row, column=1, value="EXPENSE TRACKER").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    for cc in range(1, 5):
        ws.cell(row=row, column=cc).fill = fill(BLUSH)
    row += 1
    hdr = table_header(ws, row, 1, ["Date", "Amount", "Category", "Note"], BLUSH)
    tfirst = hdr
    for i in range(15):
        r = hdr + i
        ws.cell(row=r, column=1).number_format = DATE_FMT
        ws.cell(row=r, column=2).number_format = CURRENCY_FMT
        for cc in range(1, 5):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    tlast = hdr + 14
    row = tlast + 2

    row, efirst, elast, etotal = _expense_summary(ws, row, BLUSH, "Bachelor(ette) Planner",
        ["Accommodation", "Travel", "Activities", "Food and Drinks", "Attire", "Other"])
    ws.cell(row=kpi_row + 1, column=3, value=f"=B{etotal}-C{etotal}").number_format = CURRENCY_FMT

    set_col_widths(ws, {"A": 18, "B": 16, "C": 16, "D": 18, "E": 16, "F": 14, "G": 14, "H": 18, "I": 14})
    freeze_header(ws, 1)
