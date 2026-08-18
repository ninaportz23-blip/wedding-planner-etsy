# -*- coding: utf-8 -*-
"""Tabs 11-13: Venue Comparison, Food & Drinks, Photo & Video Shot List."""
from lib import *

def build_venue_comparison(wb):
    ws = new_sheet(wb, "Venue Comparison", tab_color=LAVENDER)
    row = title_banner(ws, "VENUE COMPARISON", LAVENDER, row=1, col_start=1, col_end=6, size=16)
    row += 1
    fields = ["Name", "Photo Placeholder", "Contact Info", "Capacity", "Availability", "Venue Fee",
              "Ceremony Fee", "Reception Fee", "Setup Fee", "Cleanup Fee", "Service Charge",
              "Food and Drinks", "Alcohol", "Cake Cutting Fee", "Total", "Winner"]
    header_row = row
    ws.cell(row=header_row, column=1, value="Field").font = f_header()
    ws.cell(row=header_row, column=1).fill = fill(LAVENDER)
    ws.cell(row=header_row, column=1).border = BORDER_ALL
    for v in range(5):
        c = ws.cell(row=header_row, column=2 + v, value=f"Venue {v+1}")
        c.font = f_header()
        c.fill = fill(LAVENDER)
        c.alignment = CENTER
        c.border = BORDER_ALL
    fee_rows = {}
    r = header_row + 1
    total_row = None
    for field in fields:
        ws.cell(row=r, column=1, value=field).font = f_body(bold=True)
        ws.cell(row=r, column=1).border = BORDER_ALL
        ws.cell(row=r, column=1).fill = fill(OFFWHITE)
        for v in range(5):
            c = ws.cell(row=r, column=2 + v)
            c.border = BORDER_ALL
            c.font = f_body()
            if field in ("Photo Placeholder",):
                c.value = "[ photo ]"
                c.font = f_body(italic=True, color="9A9A9A")
                c.alignment = CENTER
            if field.endswith("Fee") or field in ("Food and Drinks", "Alcohol", "Service Charge"):
                c.number_format = CURRENCY_FMT
                fee_rows.setdefault(v, []).append(r)
        if field == "Total":
            total_row = r
        r += 1
    winner_row = r - 1
    for v in range(5):
        col_letter = get_column_letter(2 + v)
        rows_to_sum = fee_rows.get(v, [])
        formula = "=" + "+".join(f"{col_letter}{rr}" for rr in rows_to_sum)
        cell = ws.cell(row=total_row, column=2 + v, value=formula)
        cell.number_format = CURRENCY_FMT
        cell.font = f_header()
    # winner: lowest total flagged
    min_formula_cells = ",".join(f"{get_column_letter(2+v)}{total_row}" for v in range(5))
    for v in range(5):
        col_letter = get_column_letter(2 + v)
        wcell = ws.cell(row=winner_row, column=2 + v,
                         value=f'=IF(AND({col_letter}{total_row}<>0,{col_letter}{total_row}=MIN({min_formula_cells})),"Best Value","")')
        wcell.font = f_body(bold=True)
        wcell.alignment = CENTER
    ws.conditional_formatting.add(f"B{winner_row}:F{winner_row}",
        FormulaRule(formula=[f'B{winner_row}<>""'], fill=fill(STATUS_GREEN)))
    # sample data for three venues so the comparison shows a filled example
    sample = {
        "Name": ["Willow Creek Barn", "The Grand Hall", "Seaside Terrace"],
        "Contact Info": ["555-0101", "555-0180", "555-0199"],
        "Capacity": [200, 150, 120],
        "Availability": ["Available", "Available", "Waitlist"],
        "Venue Fee": [8500, 6000, 7200],
        "Ceremony Fee": [500, 800, 0],
        "Reception Fee": [0, 1200, 0],
        "Setup Fee": [300, 250, 400],
        "Cleanup Fee": [250, 200, 300],
        "Service Charge": [1200, 900, 1100],
        "Food and Drinks": [6500, 5200, 7000],
        "Alcohol": [2000, 1500, 2200],
        "Cake Cutting Fee": [150, 200, 0],
    }
    for idx, field in enumerate(fields):
        if field in sample:
            frow = header_row + 1 + idx
            for v, val in enumerate(sample[field]):
                ws.cell(row=frow, column=2 + v, value=val)
    set_col_widths(ws, {"A": 18, "B": 18, "C": 18, "D": 18, "E": 18, "F": 18})
    freeze_header(ws, header_row + 1)

def build_food_drinks(wb, dv_named):
    ws = new_sheet(wb, "Food and Drinks", tab_color=PEACH)
    row = title_banner(ws, "FOOD AND DRINKS", PEACH, row=1, col_start=1, col_end=6, size=16)
    row += 1
    courses = ["Appetizers", "Main Course", "Desserts", "Drinks"]
    events = ["Rehearsal Dinner", "Reception"]
    # light sample data so the cost chart shows something in the demo
    sample = {
        "Rehearsal Dinner": {"Appetizers": ("Bruschetta platter", 180), "Main Course": ("Family-style pasta", 640),
                              "Desserts": ("Tiramisu", 150), "Drinks": ("House wine", 220)},
        "Reception": {"Appetizers": ("Passed canapés", 900), "Main Course": ("Plated dinner", 4200),
                      "Desserts": ("Wedding cake", 650), "Drinks": ("Open bar", 1800)},
    }
    helper_col = 30  # AD, hidden
    hr = 2
    ws.cell(row=hr, column=helper_col, value="Event")
    ws.cell(row=hr, column=helper_col + 1, value="Total Cost")
    event_totals_rows = {}
    for i, ev in enumerate(events):
        ws.cell(row=hr + 1 + i, column=helper_col, value=ev)
    for ev in events:
        ws.cell(row=row, column=1, value=ev.upper()).font = f_title(size=13)
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
        ws.cell(row=row, column=1).fill = fill(PEACH)
        for cc in range(1, 7):
            ws.cell(row=row, column=cc).fill = fill(PEACH)
        row += 1
        ev_total_terms = []
        for course in courses:
            ws.cell(row=row, column=1, value=course.upper()).font = f_header()
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
            for cc in range(1, 7):
                ws.cell(row=row, column=cc).fill = fill(CREAM)
            row += 1
            hdr = table_header(ws, row, 1, ["Final", "Item", "Tasting Rating", "Amount", "Qty", "Total"], CREAM)
            first = hdr
            n = 4
            for i in range(n):
                r = hdr + i
                ws.cell(row=r, column=1, value=False)
                if i == 0 and ev in sample and course in sample[ev]:
                    itm, amt = sample[ev][course]
                    ws.cell(row=r, column=2, value=itm)
                    ws.cell(row=r, column=4, value=amt).number_format = CURRENCY_FMT
                else:
                    ws.cell(row=r, column=2, value="")
                    ws.cell(row=r, column=4, value=0).number_format = CURRENCY_FMT
                ws.cell(row=r, column=3, value="")
                ws.cell(row=r, column=5, value=1)
                ws.cell(row=r, column=6, value=f"=D{r}*E{r}").number_format = CURRENCY_FMT
                for cc in range(1, 7):
                    ws.cell(row=r, column=cc).border = BORDER_ALL
                    ws.cell(row=r, column=cc).font = f_body()
                    ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
            add_checkbox_col(ws, f"A{first}:A{first+n-1}")
            ev_total_terms.append(f"SUM(F{first}:F{first+n-1})")
            row = hdr + n + 1
        ev_total_row = row
        ws.cell(row=row, column=1, value=f"{ev} Total Cost").font = f_header()
        tcell = ws.cell(row=row, column=2, value="=" + "+".join(ev_total_terms))
        tcell.number_format = CURRENCY_FMT
        tcell.font = f_header()
        event_totals_rows[ev] = ev_total_row
        row += 3
    for i, ev in enumerate(events):
        ws.cell(row=hr + 1 + i, column=helper_col + 1, value=f"=B{event_totals_rows[ev]}").number_format = CURRENCY_FMT
    letter_c = get_column_letter(helper_col)
    letter_v = get_column_letter(helper_col + 1)
    for hcol in (helper_col, helper_col + 1):
        ws.column_dimensions[get_column_letter(hcol)].hidden = False
    make_donut(ws, "Total Cost by Event", f"'Food and Drinks'!${letter_c}${hr+1}:${letter_c}${hr+len(events)}",
               f"'Food and Drinks'!${letter_v}${hr+1}:${letter_v}${hr+len(events)}", "H4", width=9, height=6.6,
               colors=[BLUSH, SAGE])
    set_col_widths(ws, {"A": 14, "B": 22, "C": 14, "D": 12, "E": 8, "F": 12})

def build_shot_list(wb):
    ws = new_sheet(wb, "Photo and Video Shot List", tab_color=SAGE)
    row = title_banner(ws, "PHOTO AND VIDEO SHOT LIST", SAGE, row=1, col_start=1, col_end=3, size=16)
    row += 1
    moments = {
        "Getting Ready": ["Dress on hanger", "Rings close up", "Invitation suite flat lay", "Bride getting into dress",
                           "Groom getting dressed", "Bridesmaids helping bride", "Groomsmen candid moments", "First look with parent"],
        "Ceremony": ["Ceremony site before guests arrive", "Guests arriving", "Processional", "Bride's entrance",
                     "Vows exchange", "Ring exchange", "First kiss", "Recessional"],
        "Family Formals": ["Immediate family with couple", "Extended family with couple", "Bridal party with couple",
                            "Bride with her parents", "Groom with his parents", "Grandparents with couple"],
        "Reception": ["Reception decor detail shots", "Grand entrance", "First dance", "Parent dances", "Toasts and speeches",
                       "Cake cutting", "Bouquet toss", "Garter toss", "Open dancing", "Send off"],
        "Details": ["Rings", "Bouquet", "Shoes", "Invitation suite", "Centerpieces", "Cake", "Favors", "Signage"],
    }
    for cat_type in ["Photography", "Videography"]:
        ws.cell(row=row, column=1, value=cat_type.upper()).font = f_title(size=14)
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
        ws.cell(row=row, column=1).fill = fill(SAGE)
        ws.cell(row=row, column=2).fill = fill(SAGE)
        ws.cell(row=row, column=3).fill = fill(SAGE)
        row += 1
        for moment, shots in moments.items():
            ws.cell(row=row, column=1, value=moment.upper()).font = f_header()
            ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
            ws.cell(row=row, column=1).fill = fill(CREAM)
            ws.cell(row=row, column=2).fill = fill(CREAM)
            ws.cell(row=row, column=3).fill = fill(CREAM)
            row += 1
            hdr = table_header(ws, row, 1, ["Captured", "Shot", "Notes"], CREAM)
            first = hdr
            for i, shot in enumerate(shots):
                r = hdr + i
                ws.cell(row=r, column=1, value=False)
                ws.cell(row=r, column=2, value=shot)
                ws.cell(row=r, column=3, value="")
                for cc in range(1, 4):
                    ws.cell(row=r, column=cc).border = BORDER_ALL
                    ws.cell(row=r, column=cc).font = f_body()
                    ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
                ws.cell(row=r, column=1).alignment = CENTER
            add_checkbox_col(ws, f"A{first}:A{first+len(shots)-1}")
            ws.conditional_formatting.add(f"A{first}:A{first+len(shots)-1}",
                FormulaRule(formula=[f"A{first}=ChkVal"], fill=fill(STATUS_GREEN)))
            row = hdr + len(shots) + 1
    set_col_widths(ws, {"A": 12, "B": 30, "C": 30})
    freeze_header(ws, 1)
