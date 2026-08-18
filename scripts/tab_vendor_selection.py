# -*- coding: utf-8 -*-
"""Tab 10: Vendor Selection / Research."""
from lib import *

def build_vendor_selection(wb, dv_named):
    ws = new_sheet(wb, "Vendor Selection", tab_color=PEACH)
    row = title_banner(ws, "VENDOR SELECTION AND RESEARCH", PEACH, row=1, col_start=1, col_end=11, size=16)
    row += 1

    kpi_row = row
    kpi_box(ws, kpi_row, 1, "SELECTION PROGRESS", None, PEACH, width_cols=2)
    kpi_box(ws, kpi_row, 3, "TOTAL COST", None, PEACH, width_cols=2)
    kpi_box(ws, kpi_row, 5, "VENDORS FINALIZED", None, PEACH, width_cols=2)
    row = kpi_row + 3

    header_row = row
    headers = ["Final", "Category", "Name", "Contact", "Email", "Package", "Amount", "Availability", "Rating (1-5)", "Notes"]
    table_header(ws, header_row, 1, headers, PEACH)
    first_data_row = header_row + 1
    n_rows = 90
    last_data_row = first_data_row + n_rows - 1

    sample_vendors = [
        ("Yes", "Venue", "Willow Creek Barn", "555-0101", "info@willowcreekbarn.com", "Full Day Rental", 8500, "Confirmed", 5, "Holds 200 guests, includes tables and chairs"),
        ("Yes", "Catering", "Copper Table Catering", "555-0102", "hello@coppertable.com", "Plated Dinner, 3 Course", 6200, "Confirmed", 5, "Tasting scheduled, great reviews"),
        ("Yes", "Photography", "Golden Hour Studio", "555-0103", "book@goldenhourstudio.com", "8 Hour Coverage", 3200, "Confirmed", 5, "Second shooter included"),
        ("No", "Videography", "Storyframe Films", "555-0104", "team@storyframefilms.com", "Highlight Reel", 2400, "Pending", 4, "Waiting on final quote"),
        ("No", "Florist", "Petal and Vine", "555-0105", "orders@petalandvine.com", "Full Florals Package", 2100, "Pending", 4, ""),
    ]
    for i in range(n_rows):
        r = first_data_row + i
        if i < len(sample_vendors):
            final, cat, name, contact, email, pkg, amt, avail, rating, notes = sample_vendors[i]
        else:
            final, cat, name, contact, email, pkg, amt, avail, rating, notes = ("No", "", "", "", "", "", None, "", "", "")
        ws.cell(row=r, column=1, value=final)
        ws.cell(row=r, column=2, value=cat)
        ws.cell(row=r, column=3, value=name)
        ws.cell(row=r, column=4, value=contact)
        ws.cell(row=r, column=5, value=email)
        ws.cell(row=r, column=6, value=pkg)
        c_amt = ws.cell(row=r, column=7, value=amt)
        c_amt.number_format = CURRENCY_FMT
        ws.cell(row=r, column=8, value=avail)
        ws.cell(row=r, column=9, value=rating)
        ws.cell(row=r, column=10, value=notes)
        for cc in range(1, 11):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)

    dv_named(ws, f"A{first_data_row}:A{last_data_row}", "YesNo")
    dv_named(ws, f"B{first_data_row}:B{last_data_row}", "VendorCategory")
    ws.conditional_formatting.add(f"A{first_data_row}:A{last_data_row}",
        FormulaRule(formula=[f'EXACT(A{first_data_row},"Yes")'], fill=fill(STATUS_GREEN)))

    freeze_header(ws, first_data_row)
    set_col_widths(ws, {"A": 8, "B": 14, "C": 20, "D": 14, "E": 22, "F": 20, "G": 12, "H": 14, "I": 10, "J": 26})

    # KPI formulas
    kpi_pct = ws.cell(row=kpi_row + 1, column=1, value=f'=COUNTIFS(A{first_data_row}:A{last_data_row},"Yes")/COUNTIF(B{first_data_row}:B{last_data_row},"<>")')
    kpi_pct.number_format = "0%"
    kpi_pct.font = f_kpi_number()
    kpi_cost = ws.cell(row=kpi_row + 1, column=3, value=f'=SUMIFS(G{first_data_row}:G{last_data_row},A{first_data_row}:A{last_data_row},"Yes")')
    kpi_cost.number_format = CURRENCY_FMT
    kpi_cost.font = f_kpi_number(size=14)
    kpi_final = ws.cell(row=kpi_row + 1, column=5, value=f'=COUNTIFS(A{first_data_row}:A{last_data_row},"Yes")')
    kpi_final.font = f_kpi_number()

    # Bar chart: vendor cost by category (helper table)
    help_col = 12  # L
    hrow = kpi_row
    ws.cell(row=hrow, column=help_col, value="Category").font = f_header()
    ws.cell(row=hrow, column=help_col + 1, value="Cost").font = f_header()
    from data_lists import VENDOR_CATEGORY
    cats_start = hrow + 1
    for i, cat in enumerate(VENDOR_CATEGORY):
        r = cats_start + i
        ws.cell(row=r, column=help_col, value=cat)
        ws.cell(row=r, column=help_col + 1,
                value=f'=SUMIFS($G${first_data_row}:$G${last_data_row},$B${first_data_row}:$B${last_data_row},{ws.cell(row=r, column=help_col).coordinate},$A${first_data_row}:$A${last_data_row},"Yes")').number_format = CURRENCY_FMT
    cats_end = cats_start + len(VENDOR_CATEGORY) - 1
    letter_c = get_column_letter(help_col)
    letter_v = get_column_letter(help_col + 1)
    make_bar(ws, "Vendor Cost by Category",
             f"'Vendor Selection'!${letter_c}${cats_start}:${letter_c}${cats_end}",
             f"'Vendor Selection'!${letter_v}${hrow}:${letter_v}${cats_end}",
             "N4", width=16, height=9)

    return {"first_data_row": first_data_row, "last_data_row": last_data_row}
