# -*- coding: utf-8 -*-
"""Tabs 32-33: Honeymoon Planner, Gifts and Thank You."""
from lib import *
from data_lists import CURRENCY_LIST, BOOKING_STATUS

def build_honeymoon(wb, dv_named):
    ws = new_sheet(wb, "Honeymoon Planner", tab_color=POWDER)
    row = title_banner(ws, "HONEYMOON PLANNER", POWDER, row=1, col_start=1, col_end=9, size=16)
    row += 1

    kpi_row = row
    kpi_box(ws, kpi_row, 1, "TOTAL SPENT", None, POWDER, width_cols=2)
    kpi_box(ws, kpi_row, 3, "LEFT TO SPEND", None, POWDER, width_cols=2)
    row = kpi_row + 3

    # Expense summary
    ws.cell(row=row, column=1, value="EXPENSES TRACKER").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    for cc in range(1, 5):
        ws.cell(row=row, column=cc).fill = fill(POWDER)
    row += 1
    hdr = table_header(ws, row, 1, ["Category", "Budget", "Actual", "Left"], POWDER)
    efirst = hdr
    categories = ["Flights", "Accommodation", "Food and Drinks", "Activities and Excursions", "Shopping", "Transportation", "Other"]
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
    elast = hdr + len(categories) - 1
    etotal = elast + 1
    ws.cell(row=etotal, column=1, value="Total").font = f_header()
    for col, letter in [(2, "B"), (3, "C"), (4, "D")]:
        c = ws.cell(row=etotal, column=col, value=f"=SUM({letter}{efirst}:{letter}{elast})")
        c.number_format = CURRENCY_FMT
        c.font = f_header()
    for cc in range(1, 5):
        ws.cell(row=etotal, column=cc).fill = fill(CREAM)
        ws.cell(row=etotal, column=cc).border = BORDER_ALL

    ws.cell(row=kpi_row + 1, column=1, value=f"=C{etotal}").number_format = CURRENCY_FMT
    ws.cell(row=kpi_row + 1, column=3, value=f"=B{etotal}-C{etotal}").number_format = CURRENCY_FMT

    make_donut(ws, "Expense Breakdown", f"'Honeymoon Planner'!$A${efirst}:$A${elast}",
               f"'Honeymoon Planner'!$C${efirst}:$C${elast}", "F4", width=11, height=8)
    make_bar(ws, "Budget vs Actual", f"'Honeymoon Planner'!$A${efirst}:$A${elast}",
             f"'Honeymoon Planner'!$B${hdr-1}:$C${elast}", "L4", width=14, height=8, colors=[LAVENDER, PEACH])

    row = etotal + 2
    # Currency calculator
    ws.cell(row=row, column=1, value="CURRENCY CALCULATOR").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
    for cc in range(1, 6):
        ws.cell(row=row, column=cc).fill = fill(CREAM)
    row += 1
    labels = ["From Currency", "To Currency", "Exchange Rate", "Amount", "Converted Amount"]
    for i, lab in enumerate(labels):
        ws.cell(row=row, column=1 + i, value=lab).font = f_kpi_label()
        ws.cell(row=row, column=1 + i).fill = fill(WHITE)
        ws.cell(row=row, column=1 + i).border = BORDER_ALL
    row += 1
    ws.cell(row=row, column=1, value="USD")
    ws.cell(row=row, column=2, value="EUR")
    ws.cell(row=row, column=3, value=0.92)
    ws.cell(row=row, column=4, value=100).number_format = CURRENCY_FMT
    ws.cell(row=row, column=5, value=f"=D{row}*C{row}").number_format = CURRENCY_FMT
    for cc in range(1, 6):
        ws.cell(row=row, column=cc).border = BORDER_ALL
        ws.cell(row=row, column=cc).font = f_body(bold=True)
    dv_named(ws, f"A{row}:A{row}", "CurrencyList")
    dv_named(ws, f"B{row}:B{row}", "CurrencyList")
    calc_row = row
    row += 3

    # Transaction tracker
    ws.cell(row=row, column=1, value="TRANSACTION TRACKER").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    for cc in range(1, 5):
        ws.cell(row=row, column=cc).fill = fill(SAGE)
    row += 1
    hdr = table_header(ws, row, 1, ["Date", "Amount", "Category", "Note"], SAGE)
    for i in range(20):
        r = hdr + i
        ws.cell(row=r, column=1).number_format = DATE_FMT
        ws.cell(row=r, column=2).number_format = CURRENCY_FMT
        for cc in range(1, 5):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    row = hdr + 21

    # Bookings (2 accommodation options) + travel arrangement
    ws.cell(row=row, column=1, value="BOOKINGS (ACCOMMODATION OPTIONS)").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=8)
    for cc in range(1, 9):
        ws.cell(row=row, column=cc).fill = fill(BLUSH)
    row += 1
    hdr = table_header(ws, row, 1, ["Option", "Name", "Phone", "Email", "Booking Date", "Duration", "Status", "Reference"], BLUSH)
    bfirst = hdr
    for i in range(2):
        r = hdr + i
        ws.cell(row=r, column=1, value=f"Option {i+1}")
        ws.cell(row=r, column=5).number_format = DATE_FMT
        for cc in range(1, 9):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    blast = hdr + 1
    dv_named(ws, f"G{bfirst}:G{blast}", "BookingStatus")
    row = blast + 2

    ws.cell(row=row, column=1, value="TRAVEL ARRANGEMENT").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    for cc in range(1, 7):
        ws.cell(row=row, column=cc).fill = fill(PEACH)
    row += 1
    hdr = table_header(ws, row, 1, ["Traveler", "Mode", "Departure", "Arrival", "Confirmation #", "Notes"], PEACH)
    for i in range(6):
        r = hdr + i
        for cc in range(1, 7):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    row = hdr + 8

    # Honeymoon checklist
    ws.cell(row=row, column=1, value="HONEYMOON CHECKLIST").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
    for cc in range(1, 4):
        ws.cell(row=row, column=cc).fill = fill(LAVENDER)
    row += 1
    hdr = table_header(ws, row, 1, ["Done", "Task", "Assigned To"], LAVENDER)
    cfirst = hdr
    tasks = ["Book flights", "Book accommodation", "Confirm passport validity", "Arrange travel insurance",
             "Notify bank of travel dates", "Exchange currency", "Confirm excursion reservations",
             "Pack luggage", "Print travel documents", "Arrange airport transportation"]
    for i, t in enumerate(tasks):
        r = hdr + i
        ws.cell(row=r, column=1, value=False)
        ws.cell(row=r, column=2, value=t)
        ws.cell(row=r, column=3, value="Both")
        for cc in range(1, 4):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    clast = hdr + len(tasks) - 1
    add_checkbox_col(ws, f"A{cfirst}:A{clast}")
    dv_named(ws, f"C{cfirst}:C{clast}", "AssignedTo")
    ws.conditional_formatting.add(f"A{cfirst}:A{clast}", FormulaRule(formula=[f"A{cfirst}=ChkVal"], fill=fill(STATUS_GREEN)))

    helper_col = 6
    ws.cell(row=hdr - 1, column=helper_col, value="Status").font = f_header()
    ws.cell(row=hdr - 1, column=helper_col + 1, value="Count").font = f_header()
    ws.cell(row=hdr, column=helper_col, value="Done")
    ws.cell(row=hdr, column=helper_col + 1, value=f"=COUNTIF(A{cfirst}:A{clast},ChkVal)")
    ws.cell(row=hdr + 1, column=helper_col, value="Incomplete")
    ws.cell(row=hdr + 1, column=helper_col + 1, value=f"=COUNTIF(A{cfirst}:A{clast},UnchkVal)")
    letter_c = get_column_letter(helper_col); letter_v = get_column_letter(helper_col + 1)
    make_donut(ws, "Checklist Progress", f"'Honeymoon Planner'!${letter_c}${hdr}:${letter_c}${hdr+1}",
               f"'Honeymoon Planner'!${letter_v}${hdr}:${letter_v}${hdr+1}", f"F{hdr+3}", colors=[SAGE, GREY], width=10, height=7)

    ws.cell(row=hdr - 1, column=helper_col + 3, value="Assigned To").font = f_header()
    ws.cell(row=hdr - 1, column=helper_col + 4, value="Incomplete").font = f_header()
    from data_lists import ASSIGNED_TO
    for i, person in enumerate(ASSIGNED_TO):
        ws.cell(row=hdr + i, column=helper_col + 3, value=person)
        ws.cell(row=hdr + i, column=helper_col + 4,
                value=f'=COUNTIFS($C${cfirst}:$C${clast},{ws.cell(row=hdr+i, column=helper_col+3).coordinate},$A${cfirst}:$A${clast},UnchkVal)')
    aend = hdr + len(ASSIGNED_TO) - 1
    make_bar(ws, "Incomplete by Assigned To", f"'Honeymoon Planner'!${get_column_letter(helper_col+3)}${hdr}:${get_column_letter(helper_col+3)}${aend}",
             f"'Honeymoon Planner'!${get_column_letter(helper_col+4)}${hdr-1}:${get_column_letter(helper_col+4)}${aend}", f"I{hdr+3}", width=14, height=8)

    row = max(clast, aend) + 3
    ws.cell(row=row, column=1, value="Packing list reference: see the Packing List tab, Honeymoon section.").font = f_body(italic=True, size=9)
    ws.cell(row=row, column=1).hyperlink = "#'Packing List'!A1"

    set_col_widths(ws, {"A": 18, "B": 16, "C": 16, "D": 14, "E": 16})
    freeze_header(ws, 1)


def build_gifts_thank_you(wb, dv_named):
    ws = new_sheet(wb, "Gifts and Thank You", tab_color=SAGE)
    row = title_banner(ws, "GIFTS AND THANK YOU", SAGE, row=1, col_start=1, col_end=6, size=16)
    row += 1
    kpi_row = row
    kpi_box(ws, kpi_row, 1, "THANK YOU CARDS SENT", None, SAGE, width_cols=3)
    row = kpi_row + 3

    header_row = row
    table_header(ws, header_row, 1, ["Guest Name", "Gift Received", "Estimated Value", "Thank You Card Sent", "Date Sent", "Notes"], SAGE)
    first = header_row + 1
    n = 200
    last = first + n - 1
    for i in range(n):
        r = first + i
        ws.cell(row=r, column=3, value=0).number_format = CURRENCY_FMT
        ws.cell(row=r, column=4, value=False)
        ws.cell(row=r, column=5).number_format = DATE_FMT
        for cc in range(1, 7):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    add_checkbox_col(ws, f"D{first}:D{last}")
    ws.conditional_formatting.add(f"D{first}:D{last}", FormulaRule(formula=[f"D{first}=ChkVal"], fill=fill(STATUS_GREEN)))

    v = ws.cell(row=kpi_row + 1, column=1,
                value=f'=IFERROR(COUNTIF(D{first}:D{last},ChkVal)&" / "&COUNTA(A{first}:A{last}),"0 / 0")')
    v.font = f_kpi_number(size=15)

    # Long gift log: keep the column headers visible while scrolling.
    ws.freeze_panes = ws.cell(row=first, column=1)
    set_col_widths(ws, {"A": 20, "B": 22, "C": 14, "D": 16, "E": 14, "F": 26})
    return {"first": first, "last": last}
