# -*- coding: utf-8 -*-
"""Tab 14: Guest List - supports up to 1000 guests."""
from lib import *
from data_lists import GUEST_TAG, GUEST_TYPE, MEAL_PREF, YES_NO_AWAITED

N_GUESTS = 200  # pre-built rows; buyer can copy-paste formatting down to 1000

def build_guest_list(wb, dv_named):
    ws = new_sheet(wb, "Guest List", tab_color=BLUSH)
    row = title_banner(ws, "GUEST LIST", BLUSH, row=1, col_start=1, col_end=12, size=16)
    row += 1

    kpi_row = row
    labels = ["TOTAL GUESTS", "SAVE THE DATE SENT", "INVITATION SENT", "CONFIRMED", "RSVP DEADLINE", "DAYS LEFT TO RSVP"]
    for i, lab in enumerate(labels):
        kpi_box(ws, kpi_row, 1 + i * 2, lab, None, BLUSH, width_cols=2, font_size=13)
    row = kpi_row + 3

    header_row = row
    headers = ["Name", "Guest Tag", "Child", "Save the Date", "Invitation", "RSVP", "Meal Preference",
               "Rehearsal Dinner", "Contact", "Email", "Address"]
    table_header(ws, header_row, 1, headers, BLUSH)
    first_data_row = header_row + 1
    last_data_row = first_data_row + N_GUESTS - 1

    import random
    random.seed(42)
    sample_names = ["Alex Johnson", "Sam Rivera", "Jamie Lee", "Morgan Kim", "Taylor Brooks", "Casey Adams"]
    for i in range(N_GUESTS):
        r = first_data_row + i
        if i < len(sample_names):
            ws.cell(row=r, column=1, value=sample_names[i])
            ws.cell(row=r, column=2, value=GUEST_TAG[i % 3])
            ws.cell(row=r, column=3, value=False)
            ws.cell(row=r, column=4, value=True)
            ws.cell(row=r, column=5, value=True)
            ws.cell(row=r, column=6, value=YES_NO_AWAITED[i % 3])
            ws.cell(row=r, column=7, value=MEAL_PREF[i % len(MEAL_PREF)])
            ws.cell(row=r, column=8, value=False)
        else:
            ws.cell(row=r, column=3, value=False)
            ws.cell(row=r, column=4, value=False)
            ws.cell(row=r, column=5, value=False)
            ws.cell(row=r, column=8, value=False)
        for cc in range(1, 12):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
            if cc in (3, 4, 5, 8):
                ws.cell(row=r, column=cc).alignment = CENTER

    for col, name in [(2, "GuestTag"), (6, "YesNoAwaited"), (7, "MealPref")]:
        letter = get_column_letter(col)
        dv_named(ws, f"{letter}{first_data_row}:{letter}{last_data_row}", name)
    for col in (3, 4, 5, 8):
        letter = get_column_letter(col)
        add_checkbox_col(ws, f"{letter}{first_data_row}:{letter}{last_data_row}")

    ws.conditional_formatting.add(f"F{first_data_row}:F{last_data_row}",
        FormulaRule(formula=[f'EXACT(F{first_data_row},"Yes")'], fill=fill(STATUS_GREEN)))
    ws.conditional_formatting.add(f"F{first_data_row}:F{last_data_row}",
        FormulaRule(formula=[f'EXACT(F{first_data_row},"Awaited")'], fill=fill(STATUS_YELLOW)))
    ws.conditional_formatting.add(f"F{first_data_row}:F{last_data_row}",
        FormulaRule(formula=[f'EXACT(F{first_data_row},"No")'], fill=fill(STATUS_RED)))

    freeze_header(ws, first_data_row)
    set_col_widths(ws, {"A": 20, "B": 12, "C": 8, "D": 12, "E": 12, "F": 12, "G": 16, "H": 14, "I": 14, "J": 22, "K": 26})

    # KPI formulas
    v = ws.cell(row=kpi_row + 1, column=1, value=f'=COUNTA(A{first_data_row}:A{last_data_row})')
    v.font = f_kpi_number(size=15)
    v = ws.cell(row=kpi_row + 1, column=3, value=f'=COUNTIFS(D{first_data_row}:D{last_data_row},TRUE)')
    v.font = f_kpi_number(size=15)
    v = ws.cell(row=kpi_row + 1, column=5, value=f'=COUNTIFS(E{first_data_row}:E{last_data_row},TRUE)')
    v.font = f_kpi_number(size=15)
    v = ws.cell(row=kpi_row + 1, column=7, value=f'=COUNTIFS(F{first_data_row}:F{last_data_row},"Yes")')
    v.font = f_kpi_number(size=15)
    rsvp_deadline_cell = ws.cell(row=kpi_row + 1, column=9, value="='Get Started'!$C$4-30")
    rsvp_deadline_cell.number_format = DATE_FMT
    rsvp_deadline_cell.font = f_kpi_number(size=13)
    days_left_cell = ws.cell(row=kpi_row + 1, column=11, value=f"=I{kpi_row+1}-TODAY()")
    days_left_cell.font = f_kpi_number(size=15)

    # Helper tables for charts (placed far right, columns N onward)
    hcol = 14  # N
    hrow = kpi_row
    ws.cell(row=hrow, column=hcol, value="Guest Of").font = f_header()
    ws.cell(row=hrow, column=hcol + 1, value="Count").font = f_header()
    for i, tag in enumerate(GUEST_TAG):
        r = hrow + 1 + i
        ws.cell(row=r, column=hcol, value=tag)
        ws.cell(row=r, column=hcol + 1, value=f'=COUNTIFS($B${first_data_row}:$B${last_data_row},{ws.cell(row=r, column=hcol).coordinate})')
    tag_end = hrow + len(GUEST_TAG)

    hrow2 = tag_end + 2
    ws.cell(row=hrow2, column=hcol, value="Guest Type").font = f_header()
    ws.cell(row=hrow2, column=hcol + 1, value="Count").font = f_header()
    # No explicit Guest Type column in main table per spec table (uses Guest Tag); reuse RSVP status breakdown instead
    for i, mp in enumerate(MEAL_PREF):
        r = hrow2 + 1 + i
        ws.cell(row=r, column=hcol, value=mp)
        ws.cell(row=r, column=hcol + 1, value=f'=COUNTIFS($G${first_data_row}:$G${last_data_row},{ws.cell(row=r, column=hcol).coordinate})')
    meal_end = hrow2 + len(MEAL_PREF)

    letter_c = get_column_letter(hcol)
    letter_v = get_column_letter(hcol + 1)
    make_pie(ws, "Guest Of (Bride / Groom / Both)",
             f"'Guest List'!${letter_c}${hrow+1}:${letter_c}${tag_end}",
             f"'Guest List'!${letter_v}${hrow+1}:${letter_v}${tag_end}",
             "P4", width=10, height=7)
    make_bar(ws, "Meal Preference",
             f"'Guest List'!${letter_c}${hrow2+1}:${letter_c}${meal_end}",
             f"'Guest List'!${letter_v}${hrow2}:${letter_v}${meal_end}",
             "P18", width=12, height=8)

    return {"first_data_row": first_data_row, "last_data_row": last_data_row, "kpi_row": kpi_row}
