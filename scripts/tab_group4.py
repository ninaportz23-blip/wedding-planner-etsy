# -*- coding: utf-8 -*-
"""Tabs 21-24: Moodboard, Decor Inventory, Flower Arrangements, Attire & Makeup."""
from lib import *
from data_lists import DECOR_LOCATION, DECOR_STATUS, BUY_RENT, ATTIRE_CATEGORY

def build_moodboard(wb):
    ws = new_sheet(wb, "Moodboard", tab_color=LAVENDER)
    row = title_banner(ws, "Moodboard", LAVENDER, row=1, col_start=1, col_end=6, size=20)
    row += 1
    intro = ws.cell(row=row, column=1, value="Collect your inspiration here. Click a frame, then use Insert › Picture › Place in cell, and note the source link underneath.")
    intro.font = f_body(italic=True, size=9, color="7A7A7A")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    ws.row_dimensions[row].height = 16
    row += 2

    set_col_widths(ws, {get_column_letter(c): 16 for c in range(1, 7)})
    tints = ["tile_blush.png", "tile_sage.png", "tile_cream.png",
             "tile_powder.png", "tile_peach.png", "tile_lav.png"]
    col_px = int(16 * 7 + 5)          # ~117px per column
    block_w = col_px * 2 - 6          # two columns, small inset
    block_h = int(block_w * 220 / 300)
    img_rows = 6
    row_h_pt = (block_h / img_rows) / 1.333
    i = 0
    for gr in range(2):
        for r in range(row, row + img_rows):
            ws.row_dimensions[r].height = row_h_pt
        for c in range(3):
            col = 1 + c * 2
            ws.merge_cells(start_row=row, start_column=col, end_row=row + img_rows - 1, end_column=col + 1)
            # subtle card behind the frame
            for rr in range(row, row + img_rows):
                for cc in (col, col + 1):
                    ws.cell(row=rr, column=cc).fill = fill(WHITE)
            anchor = f"{get_column_letter(col)}{row}"
            embed_image(ws, tints[i % len(tints)], anchor, block_w, block_h)
            i += 1
            link_row = row + img_rows
            ws.merge_cells(start_row=link_row, start_column=col, end_row=link_row, end_column=col + 1)
            lc = ws.cell(row=link_row, column=col, value="Source:")
            lc.font = f_body(size=9, color="9A9A9A")
            ws.row_dimensions[link_row].height = 16
        row += img_rows + 2
    freeze_header(ws, 1)


def build_decor(wb, dv_named):
    ws = new_sheet(wb, "Decor Inventory", tab_color=SAGE)
    row = title_banner(ws, "DECOR INVENTORY", SAGE, row=1, col_start=1, col_end=8, size=16)
    row += 1
    kpi_row = row
    kpi_box(ws, kpi_row, 1, "TOTAL COST", None, SAGE, width_cols=2)
    kpi_box(ws, kpi_row, 3, "CONFIRMED", None, SAGE, width_cols=2)
    kpi_box(ws, kpi_row, 5, "TO BE DECIDED", None, SAGE, width_cols=2)
    kpi_box(ws, kpi_row, 7, "CANCELLED", None, SAGE, width_cols=2)
    row = kpi_row + 3

    header_row = row
    table_header(ws, header_row, 1, ["Item", "Decor Location", "Vendor", "Status", "Buy/Rent", "Cost per Unit", "Quantity", "Total Cost", "Image URL"], SAGE)
    first = header_row + 1
    n = 40
    last = first + n - 1
    decor_sample = [
        ("Ceremony arch", "Ceremony", "Petal & Vine", "Confirmed", "Rent", 350, 1),
        ("Aisle lanterns", "Ceremony", "Glow Rentals", "Confirmed", "Rent", 18, 12),
        ("Welcome sign", "Reception Entrance", "Copper Press", "Confirmed", "Buy", 90, 1),
        ("Table centerpieces", "Reception Tables", "Petal & Vine", "Confirmed", "Rent", 45, 15),
        ("Table linens", "Reception Tables", "Linen Co.", "Confirmed", "Rent", 12, 15),
        ("Head table garland", "Head Table", "Petal & Vine", "To Be Decided", "Rent", 220, 1),
        ("String lights", "Reception Tables", "Glow Rentals", "Confirmed", "Rent", 8, 20),
        ("Candles & votives", "Reception Tables", "Copper Press", "To Be Decided", "Buy", 3, 60),
    ]
    for i in range(n):
        r = first + i
        if i < len(decor_sample):
            itm, loc, ven, st, br, cpu, qty = decor_sample[i]
            ws.cell(row=r, column=1, value=itm)
            ws.cell(row=r, column=2, value=loc)
            ws.cell(row=r, column=3, value=ven)
            ws.cell(row=r, column=4, value=st)
            ws.cell(row=r, column=5, value=br)
            ws.cell(row=r, column=6, value=cpu).number_format = CURRENCY_FMT
            ws.cell(row=r, column=7, value=qty)
        else:
            ws.cell(row=r, column=4, value="To Be Decided")
            ws.cell(row=r, column=6, value=0).number_format = CURRENCY_FMT
            ws.cell(row=r, column=7, value=1)
        ws.cell(row=r, column=8, value=f"=F{r}*G{r}").number_format = CURRENCY_FMT
        for cc in range(1, 10):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    dv_named(ws, f"B{first}:B{last}", "DecorLocation")
    dv_named(ws, f"D{first}:D{last}", "DecorStatus")
    dv_named(ws, f"E{first}:E{last}", "BuyRent")
    ws.conditional_formatting.add(f"D{first}:D{last}", FormulaRule(formula=[f'EXACT(D{first},"Confirmed")'], fill=fill(STATUS_GREEN)))
    ws.conditional_formatting.add(f"D{first}:D{last}", FormulaRule(formula=[f'EXACT(D{first},"To Be Decided")'], fill=fill(STATUS_YELLOW)))
    ws.conditional_formatting.add(f"D{first}:D{last}", FormulaRule(formula=[f'EXACT(D{first},"Cancelled")'], fill=fill(STATUS_RED)))

    v = ws.cell(row=kpi_row + 1, column=1, value=f'=SUMIFS(H{first}:H{last},D{first}:D{last},"Confirmed")')
    v.number_format = CURRENCY_FMT; v.font = f_kpi_number(size=14)
    v = ws.cell(row=kpi_row + 1, column=3, value=f'=COUNTIF(D{first}:D{last},"Confirmed")')
    v.font = f_kpi_number(size=14)
    v = ws.cell(row=kpi_row + 1, column=5, value=f'=COUNTIF(D{first}:D{last},"To Be Decided")')
    v.font = f_kpi_number(size=14)
    v = ws.cell(row=kpi_row + 1, column=7, value=f'=COUNTIF(D{first}:D{last},"Cancelled")')
    v.font = f_kpi_number(size=14)

    helper_col = 30  # AD, hidden
    hr = 2
    ws.cell(row=hr, column=helper_col, value="Location")
    ws.cell(row=hr, column=helper_col + 1, value="Confirmed Cost")
    for i, loc in enumerate(DECOR_LOCATION):
        ws.cell(row=hr + 1 + i, column=helper_col, value=loc)
        ws.cell(row=hr + 1 + i, column=helper_col + 1,
                value=f'=SUMIFS($H${first}:$H${last},$B${first}:$B${last},{ws.cell(row=hr+1+i, column=helper_col).coordinate},$D${first}:$D${last},"Confirmed")')
    lend = hr + len(DECOR_LOCATION)
    letter_c = get_column_letter(helper_col)
    letter_v = get_column_letter(helper_col + 1)
    for hcol in (helper_col, helper_col + 1):
        ws.column_dimensions[get_column_letter(hcol)].hidden = False
    make_bar(ws, "Confirmed Decor Cost by Location", f"'Decor Inventory'!${letter_c}${hr+1}:${letter_c}${lend}",
             f"'Decor Inventory'!${letter_v}${hr}:${letter_v}${lend}", "K4", width=12, height=8)

    set_col_widths(ws, {"A": 22, "B": 18, "C": 16, "D": 14, "E": 10, "F": 13, "G": 10, "H": 13, "I": 20})
    freeze_header(ws, first)


def build_flowers(wb, dv_named):
    ws = new_sheet(wb, "Flower Arrangements", tab_color=BLUSH)
    row = title_banner(ws, "FLOWER ARRANGEMENTS", BLUSH, row=1, col_start=1, col_end=8, size=16)
    row += 1
    kpi_row = row
    kpi_box(ws, kpi_row, 1, "# OF ARRANGEMENTS", None, BLUSH, width_cols=3)
    kpi_box(ws, kpi_row, 4, "TOTAL COST", None, BLUSH, width_cols=3)
    row = kpi_row + 3

    header_row = row
    table_header(ws, header_row, 1, ["Item", "Florist", "Cost per Unit", "Quantity", "Total Cost", "Status", "Flowers Needed", "Notes", "Image URL"], BLUSH)
    first = header_row + 1
    n = 30
    last = first + n - 1
    sample_items = [("Bridal Bouquet", 180, 1, "Confirmed"), ("Bridesmaid Bouquets", 75, 4, "Confirmed"),
                    ("Boutonnieres", 18, 6, "Ordered"), ("Corsages", 22, 4, "Ordered"),
                    ("Ceremony Arch Florals", 450, 1, "Not Started"), ("Centerpieces", 65, 15, "Confirmed"),
                    ("Aisle Decor", 40, 8, "Not Started"), ("Cake Florals", 90, 1, "Ordered")]
    for i in range(n):
        r = first + i
        if i < len(sample_items):
            itm, cpu, qty, st = sample_items[i]
            ws.cell(row=r, column=1, value=itm)
            ws.cell(row=r, column=3, value=cpu).number_format = CURRENCY_FMT
            ws.cell(row=r, column=4, value=qty)
            ws.cell(row=r, column=6, value=st)
        else:
            ws.cell(row=r, column=3, value=0).number_format = CURRENCY_FMT
            ws.cell(row=r, column=4, value=1)
            ws.cell(row=r, column=6, value="Not Started")
        ws.cell(row=r, column=5, value=f"=C{r}*D{r}").number_format = CURRENCY_FMT
        for cc in range(1, 10):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    from data_lists import FLORAL_STATUS
    dv_named(ws, f"F{first}:F{last}", "FloralStatus")
    ws.conditional_formatting.add(f"F{first}:F{last}", FormulaRule(formula=[f'EXACT(F{first},"Delivered")'], fill=fill(STATUS_GREEN)))
    ws.conditional_formatting.add(f"F{first}:F{last}", FormulaRule(formula=[f'EXACT(F{first},"Not Started")'], fill=fill(STATUS_RED)))

    v = ws.cell(row=kpi_row + 1, column=1, value=f"=COUNTA(A{first}:A{last})")
    v.font = f_kpi_number(size=15)
    v = ws.cell(row=kpi_row + 1, column=4, value=f"=SUM(E{first}:E{last})")
    v.number_format = CURRENCY_FMT; v.font = f_kpi_number(size=15)

    # Chart: total cost per arrangement (uses the item + total columns directly).
    srow = first
    send = first + len(sample_items) - 1
    make_bar(ws, "Cost by Arrangement", f"'Flower Arrangements'!$A${srow}:$A${send}",
             f"'Flower Arrangements'!$E${header_row}:$E${send}", "K4", width=12, height=8, colors=[BLUSH])

    set_col_widths(ws, {"A": 20, "B": 16, "C": 13, "D": 10, "E": 13, "F": 14, "G": 20, "H": 20, "I": 18})
    freeze_header(ws, first)


def build_attire_makeup(wb, dv_named):
    ws = new_sheet(wb, "Attire and Makeup", tab_color=CREAM)
    row = title_banner(ws, "ATTIRE AND MAKEUP", CREAM, row=1, col_start=1, col_end=4, size=16)
    row += 1
    ws.cell(row=row, column=1, value="SETUP").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    ws.cell(row=row, column=1).fill = fill(CREAM)
    for cc in range(1, 5):
        ws.cell(row=row, column=cc).fill = fill(CREAM)
    row += 1
    hdr1 = table_header(ws, row, 1, ["Event", "For Person / Role", "Category", "Notes"], CREAM)
    first1 = hdr1
    n1 = 10
    last1 = first1 + n1 - 1
    for i in range(n1):
        r = first1 + i
        for cc in range(1, 5):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    dv_named(ws, f"C{first1}:C{last1}", "AttireCategory")
    row = last1 + 3

    ws.cell(row=row, column=1, value="PHOTO REFERENCE GALLERY").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=5)
    ws.cell(row=row, column=1).fill = fill(POWDER)
    for cc in range(1, 6):
        ws.cell(row=row, column=cc).fill = fill(POWDER)
    row += 1
    hdr2 = table_header(ws, row, 1, ["Image URL", "Event", "For Person / Role", "Category", "Notes"], POWDER)
    first2 = hdr2
    n2 = 15
    last2 = first2 + n2 - 1
    for i in range(n2):
        r = first2 + i
        for cc in range(1, 6):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    dv_named(ws, f"D{first2}:D{last2}", "AttireCategory")
    set_col_widths(ws, {"A": 24, "B": 20, "C": 18, "D": 30, "E": 22})
    freeze_header(ws, hdr1)
