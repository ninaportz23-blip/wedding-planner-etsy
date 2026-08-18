# -*- coding: utf-8 -*-
"""Tabs 17-20: Wedding Registry, Wedding Party, Aisle Order, Wedding Party Gifts."""
from lib import *
from data_lists import WEDDING_PARTY_ROLE, ATTIRE_STATUS, GIFT_STATUS

def build_registry(wb):
    ws = new_sheet(wb, "Wedding Registry", tab_color=BLUSH)
    row = title_banner(ws, "WEDDING REGISTRY", BLUSH, row=1, col_start=1, col_end=8, size=16)
    row += 1
    hdr = table_header(ws, row, 1, ["Item", "Store", "Link", "Price", "Priority", "Purchased", "Purchased By", "Thank You Sent"], BLUSH)
    first = hdr
    n = 60
    for i in range(n):
        r = hdr + i
        ws.cell(row=r, column=4, value=0).number_format = CURRENCY_FMT
        ws.cell(row=r, column=5, value="Medium")
        ws.cell(row=r, column=6, value=False)
        ws.cell(row=r, column=8, value=False)
        for cc in range(1, 9):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    last = hdr + n - 1
    return ws, first, last

def wire_registry(ws, first, last, dv_named):
    dv_named(ws, f"E{first}:E{last}", "Priority")
    add_checkbox_col(ws, f"F{first}:F{last}")
    add_checkbox_col(ws, f"H{first}:H{last}")
    ws.conditional_formatting.add(f"F{first}:F{last}", FormulaRule(formula=[f"F{first}=ChkVal"], fill=fill(STATUS_GREEN)))
    ws.conditional_formatting.add(f"H{first}:H{last}", FormulaRule(formula=[f"H{first}=ChkVal"], fill=fill(STATUS_GREEN)))
    freeze_header(ws, first)
    set_col_widths(ws, {"A": 24, "B": 16, "C": 24, "D": 12, "E": 12, "F": 12, "G": 16, "H": 14})


def build_wedding_party(wb, dv_named):
    ws = new_sheet(wb, "Wedding Party", tab_color=LAVENDER)
    row = title_banner(ws, "WEDDING PARTY", LAVENDER, row=1, col_start=1, col_end=8, size=16)
    row += 1
    kpi_row = row
    labels = ["CONFIRMED ROLES %", "# OF BRIDESMAIDS", "# OF GROOMSMEN", "ADDITIONAL PARTY"]
    for i, lab in enumerate(labels):
        kpi_box(ws, kpi_row, 1 + i * 2, lab, None, LAVENDER, width_cols=2, font_size=13)
    row = kpi_row + 3

    ws.cell(row=row, column=1, value="Note: syncs with guest list. Add each wedding party member to the Guest List tab as well.").font = f_body(italic=True, size=9)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=8)
    row += 2

    header_row = row
    table_header(ws, header_row, 1, ["Confirmed", "Name", "Role", "Contact", "Email", "Attire", "Attire Status", "Notes"], LAVENDER)
    first = header_row + 1
    n = 20
    last = first + n - 1
    sample = [
        (True, "Jamie Lee", "Maid of Honor", "Ready"),
        (True, "Sam Rivera", "Best Man", "Ready"),
        (True, "Ava Chen", "Bridesmaid", "Fitting Scheduled"),
        (True, "Noah Brooks", "Groomsman", "Ordered"),
        (True, "Mia Torres", "Bridesmaid", "Received"),
        (True, "Ethan Park", "Groomsman", "Ordered"),
        (True, "Zoe Nguyen", "Bridesmaid", "Alterations Needed"),
        (False, "Liam Foster", "Groomsman", "Not Started"),
    ]
    for i in range(n):
        r = first + i
        if i < len(sample):
            conf, name, role, attire = sample[i]
            ws.cell(row=r, column=1, value=conf)
            ws.cell(row=r, column=2, value=name)
            ws.cell(row=r, column=3, value=role)
            ws.cell(row=r, column=7, value=attire)
        else:
            ws.cell(row=r, column=1, value=False)
            ws.cell(row=r, column=7, value="Not Started")
        for cc in range(1, 9):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    add_checkbox_col(ws, f"A{first}:A{last}")
    dv_named(ws, f"C{first}:C{last}", "WeddingPartyRole")
    dv_named(ws, f"G{first}:G{last}", "AttireStatus")
    ws.conditional_formatting.add(f"A{first}:A{last}", FormulaRule(formula=[f"A{first}=ChkVal"], fill=fill(STATUS_GREEN)))
    status_colors = {"Not Started": GREY, "Ordered": CREAM, "Received": POWDER, "Fitting Scheduled": LAVENDER,
                      "Alterations Needed": STATUS_RED, "Ready": STATUS_GREEN}
    for st, color in status_colors.items():
        ws.conditional_formatting.add(f"G{first}:G{last}", FormulaRule(formula=[f'EXACT(G{first},"{st}")'], fill=fill(color)))

    v = ws.cell(row=kpi_row + 1, column=1, value=f'=IFERROR(COUNTIF(A{first}:A{last},ChkVal)/COUNTA(B{first}:B{last}),0)')
    v.number_format = "0%"; v.font = f_kpi_number(size=14)
    v = ws.cell(row=kpi_row + 1, column=3, value=f'=COUNTIF(C{first}:C{last},"Bridesmaid")')
    v.font = f_kpi_number(size=14)
    v = ws.cell(row=kpi_row + 1, column=5, value=f'=COUNTIF(C{first}:C{last},"Groomsman")')
    v.font = f_kpi_number(size=14)
    v = ws.cell(row=kpi_row + 1, column=7,
                value=f'=COUNTA(B{first}:B{last})-COUNTIF(C{first}:C{last},"Bridesmaid")-COUNTIF(C{first}:C{last},"Groomsman")')
    v.font = f_kpi_number(size=14)

    helper_col = 10
    hr = kpi_row
    ws.cell(row=hr, column=helper_col, value="Attire Status").font = f_header()
    ws.cell(row=hr, column=helper_col + 1, value="Count").font = f_header()
    for i, st in enumerate(ATTIRE_STATUS):
        ws.cell(row=hr + 1 + i, column=helper_col, value=st)
        ws.cell(row=hr + 1 + i, column=helper_col + 1, value=f"=COUNTIFS($G${first}:$G${last},{ws.cell(row=hr+1+i, column=helper_col).coordinate})")
    aend = hr + len(ATTIRE_STATUS)
    letter_c = get_column_letter(helper_col)
    letter_v = get_column_letter(helper_col + 1)
    make_bar(ws, "Attire Status", f"'Wedding Party'!${letter_c}${hr+1}:${letter_c}${aend}",
             f"'Wedding Party'!${letter_v}${hr}:${letter_v}${aend}", "J4", width=14, height=8)

    freeze_header(ws, header_row)
    set_col_widths(ws, {"A": 12, "B": 20, "C": 16, "D": 14, "E": 22, "F": 16, "G": 18, "H": 24})
    return {"first": first, "last": last}


def build_aisle_order(wb):
    ws = new_sheet(wb, "Aisle Order", tab_color=CREAM)
    row = title_banner(ws, "AISLE ORDER", CREAM, row=1, col_start=1, col_end=4, size=16)
    row += 1
    header_row = row
    ws.cell(row=row, column=1, value="BRIDE'S SIDE").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
    ws.cell(row=row, column=1).fill = fill(BLUSH)
    ws.cell(row=row, column=2).fill = fill(BLUSH)
    ws.cell(row=row, column=3, value="GROOM'S SIDE").font = f_header()
    ws.merge_cells(start_row=row, start_column=3, end_row=row, end_column=4)
    ws.cell(row=row, column=3).fill = fill(POWDER)
    ws.cell(row=row, column=4).fill = fill(POWDER)
    row += 1
    table_header(ws, row, 1, ["Role", "Name"], BLUSH)
    table_header(ws, row, 3, ["Role", "Name"], POWDER)
    row += 1
    roles = ["Officiant", "Groom", "Best Man", "Groomsman 1", "Groomsman 2", "Maid of Honor", "Bridesmaid 1",
             "Bridesmaid 2", "Flower Girl", "Ring Bearer", "Father of the Bride", "Bride"]
    n = len(roles)
    for i in range(n):
        r = row + i
        for cc in range(1, 5):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    row = row + n + 2
    ws.cell(row=row, column=1, value="ANYONE ELSE").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    ws.cell(row=row, column=1).fill = fill(CREAM)
    for cc in range(1, 5):
        ws.cell(row=row, column=cc).fill = fill(CREAM)
    row += 1
    for i in range(6):
        r = row + i
        for cc in range(1, 5):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).fill = fill(WHITE)
    set_col_widths(ws, {"A": 20, "B": 20, "C": 20, "D": 20})
    freeze_header(ws, header_row + 2)


def build_party_gifts(wb, dv_named):
    ws = new_sheet(wb, "Wedding Party Gifts", tab_color=PEACH)
    row = title_banner(ws, "WEDDING PARTY GIFTS", PEACH, row=1, col_start=1, col_end=9, size=16)
    row += 1
    kpi_row = row
    labels = ["TOTAL GIFTS", "TOTAL COST", "NEED TO BUY", "PURCHASED", "NEED TO WRAP", "GIVEN"]
    for i, lab in enumerate(labels):
        kpi_box(ws, kpi_row, 1 + i * 2, lab, None, PEACH, width_cols=2, font_size=12)
    row = kpi_row + 3

    header_row = row
    table_header(ws, header_row, 1, ["Role", "Gift", "Store", "Link", "Cost per Unit", "Qty", "Total Cost", "Status", "Given", "Note"], PEACH)
    first = header_row + 1
    n = 20
    last = first + n - 1
    for i in range(n):
        r = first + i
        ws.cell(row=r, column=5, value=0).number_format = CURRENCY_FMT
        ws.cell(row=r, column=6, value=1)
        ws.cell(row=r, column=7, value=f"=E{r}*F{r}").number_format = CURRENCY_FMT
        ws.cell(row=r, column=8, value="Need to Buy")
        ws.cell(row=r, column=9, value=False)
        for cc in range(1, 11):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    dv_named(ws, f"H{first}:H{last}", "GiftStatus")
    add_checkbox_col(ws, f"I{first}:I{last}")
    ws.conditional_formatting.add(f"H{first}:H{last}", FormulaRule(formula=[f'EXACT(H{first},"Purchased")'], fill=fill(STATUS_GREEN)))
    ws.conditional_formatting.add(f"H{first}:H{last}", FormulaRule(formula=[f'EXACT(H{first},"Need to Buy")'], fill=fill(STATUS_YELLOW)))
    ws.conditional_formatting.add(f"I{first}:I{last}", FormulaRule(formula=[f"I{first}=ChkVal"], fill=fill(STATUS_GREEN)))

    v = ws.cell(row=kpi_row + 1, column=1, value=f"=COUNTA(B{first}:B{last})")
    v.font = f_kpi_number(size=14)
    v = ws.cell(row=kpi_row + 1, column=3, value=f"=SUM(G{first}:G{last})")
    v.number_format = CURRENCY_FMT; v.font = f_kpi_number(size=14)
    v = ws.cell(row=kpi_row + 1, column=5, value=f'=COUNTIF(H{first}:H{last},"Need to Buy")')
    v.font = f_kpi_number(size=14)
    v = ws.cell(row=kpi_row + 1, column=7, value=f'=COUNTIF(H{first}:H{last},"Purchased")')
    v.font = f_kpi_number(size=14)
    v = ws.cell(row=kpi_row + 1, column=9,
                value=f'=COUNTIFS(H{first}:H{last},"Purchased",I{first}:I{last},UnchkVal)')
    v.font = f_kpi_number(size=14)
    v = ws.cell(row=kpi_row + 1, column=11, value=f"=COUNTIF(I{first}:I{last},ChkVal)")
    v.font = f_kpi_number(size=14)

    freeze_header(ws, header_row)
    set_col_widths(ws, {"A": 16, "B": 20, "C": 16, "D": 20, "E": 12, "F": 8, "G": 12, "H": 14, "I": 10, "J": 20})
    return {"first": first, "last": last}
