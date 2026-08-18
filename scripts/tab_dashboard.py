# -*- coding: utf-8 -*-
"""Tab 2: Dashboard - fully automated, pulls from all other tabs."""
from lib import *
from data_lists import GUEST_TAG, ATTIRE_STATUS

def build_dashboard(wb, dv_named, checklist_meta, budget_meta, guest_meta, reception_meta, vendor_meta):
    ws = new_sheet(wb, "Dashboard", tab_color=LAVENDER)
    ws.sheet_view.showGridLines = False
    row = title_banner(ws, "WEDDING DASHBOARD", LAVENDER, row=1, col_start=1, col_end=14, size=18)
    row += 1

    # Couple names + countdown + photo
    ws.merge_cells(start_row=row, start_column=1, end_row=row + 3, end_column=3)
    cpl = ws.cell(row=row, column=1, value="='Get Started'!$A$4&\" & \"&'Get Started'!$B$4")
    cpl.font = f_title(size=16)
    cpl.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cpl.fill = fill(BLUSH)
    for rr in range(row, row + 4):
        for cc in range(1, 4):
            ws.cell(row=rr, column=cc).fill = fill(BLUSH)
            ws.cell(row=rr, column=cc).border = BORDER_ALL

    cd_label = ws.cell(row=row, column=4, value="DAYS UNTIL THE WEDDING")
    ws.merge_cells(start_row=row, start_column=4, end_row=row, end_column=6)
    cd_label.font = f_kpi_label()
    cd_label.fill = fill(CREAM)
    cd_label.alignment = CENTER
    ws.cell(row=row, column=5).fill = fill(CREAM)
    ws.cell(row=row, column=6).fill = fill(CREAM)
    ws.merge_cells(start_row=row + 1, start_column=4, end_row=row + 3, end_column=6)
    cd_val = ws.cell(row=row + 1, column=4, value="=DATEDIF(TODAY(),'Get Started'!$C$4,\"d\")")
    cd_val.font = Font(name=FONT_NAME, bold=True, size=30, color=CHARCOAL)
    cd_val.alignment = CENTER
    for rr in range(row, row + 4):
        for cc in range(4, 7):
            ws.cell(row=rr, column=cc).border = BORDER_ALL

    wd_label = ws.cell(row=row, column=7, value="WEDDING DATE")
    ws.merge_cells(start_row=row, start_column=7, end_row=row, end_column=8)
    wd_label.font = f_kpi_label()
    wd_label.fill = fill(SAGE)
    ws.cell(row=row, column=8).fill = fill(SAGE)
    ws.merge_cells(start_row=row + 1, start_column=7, end_row=row + 3, end_column=8)
    wd_val = ws.cell(row=row + 1, column=7, value="='Get Started'!$C$4")
    wd_val.number_format = DATE_FMT
    wd_val.font = f_kpi_number(size=16)
    wd_val.alignment = CENTER
    for rr in range(row, row + 4):
        for cc in (7, 8):
            ws.cell(row=rr, column=cc).border = BORDER_ALL

    ws.merge_cells(start_row=row, start_column=9, end_row=row + 3, end_column=11)
    photo = ws.cell(row=row, column=9, value="[ Wedding photo placeholder ]")
    photo.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    photo.font = f_body(italic=True, color="9A9A9A")
    photo.fill = fill(OFFWHITE)
    for rr in range(row, row + 4):
        for cc in (9, 10, 11):
            ws.cell(row=rr, column=cc).border = BORDER_ALL

    row += 5

    # ---- KPI row: budget ----
    kpi_row = row
    ebr = budget_meta["exp_total_row"]
    kb = budget_meta["kpi_row"] + 1
    def link_kpi(col, label, formula, color, fmt=None, width=2):
        v = kpi_box(ws, kpi_row, col, label, None, color, width_cols=width, font_size=13)
        v.value = formula
        if fmt:
            v.number_format = fmt
        return v
    link_kpi(1, "WEDDING BUDGET", f"='Wedding Budget'!A{kb}", LAVENDER, CURRENCY_FMT)
    link_kpi(3, "TOTAL SPENT", f"='Wedding Budget'!E{kb}", BLUSH, CURRENCY_FMT)
    link_kpi(5, "LEFT TO SPEND", f"='Wedding Budget'!G{kb}", SAGE, CURRENCY_FMT)
    link_kpi(7, "VENDOR PAYMENTS LEFT", f"='Wedding Budget'!I{kb}", PEACH, CURRENCY_FMT)
    row = kpi_row + 3

    # ---- KPI row: guests / checklist ----
    kpi_row2 = row
    gk = guest_meta["kpi_row"] + 1
    rk = reception_meta["kpi_row"] + 1
    link_kpi_row2_vals = [
        (1, "CONFIRMED GUESTS", f"='Guest List'!G{gk}", POWDER, None),
        (3, "CONFIRMED AND SEATED", f"='Reception Seating Plan'!E{rk}", CREAM, None),
        (5, "TENTATIVE SEATS", f"='Reception Seating Plan'!G{rk}", SAGE, None),
        (7, "REMAINING SEATS", f"='Reception Seating Plan'!I{rk}", BLUSH, None),
    ]
    for col, lab, formula, color, fmt in link_kpi_row2_vals:
        v = kpi_box(ws, kpi_row2, col, lab, None, color, width_cols=2, font_size=13)
        v.value = formula
        if fmt:
            v.number_format = fmt
    row = kpi_row2 + 3

    # ---- Charts row: checklist progress donut, guest breakdown pie, save-the-date/invite donuts, vendor budget bar ----
    charts_row = row
    ws.cell(row=charts_row, column=1, value="CHECKLIST PROGRESS").font = f_header()
    ws.merge_cells(start_row=charts_row, start_column=1, end_row=charts_row, end_column=4)
    helper_col = 16  # P, far right helper area for chart source data
    hr = 4
    ws.cell(row=hr, column=helper_col, value="Checklist").font = f_header()
    ws.cell(row=hr, column=helper_col + 1, value="Value")
    total_items = checklist_meta["total_items"]
    cfr, clr = checklist_meta["first_data_row"], checklist_meta["last_data_row"]
    ws.cell(row=hr + 1, column=helper_col, value="Done")
    ws.cell(row=hr + 1, column=helper_col + 1, value=f"=COUNTIFS('Wedding Checklist'!A{cfr}:A{clr},TRUE)")
    ws.cell(row=hr + 2, column=helper_col, value="Remaining")
    ws.cell(row=hr + 2, column=helper_col + 1, value=f"=COUNTIFS('Wedding Checklist'!A{cfr}:A{clr},FALSE)")
    letter_hc = get_column_letter(helper_col)
    letter_hv = get_column_letter(helper_col + 1)
    make_donut(ws, "Checklist Progress", f"Dashboard!${letter_hc}${hr+1}:${letter_hc}${hr+2}",
               f"Dashboard!${letter_hv}${hr+1}:${letter_hv}${hr+2}", f"A{charts_row+1}", colors=[SAGE, GREY], width=9, height=7.5)

    # Guest breakdown pie (bride/groom/both)
    ws.cell(row=hr + 4, column=helper_col, value="Bride").font = f_body()
    ws.cell(row=hr + 4, column=helper_col + 1, value=f"=COUNTIFS('Guest List'!B{guest_meta['first_data_row']}:B{guest_meta['last_data_row']},\"Bride\")")
    ws.cell(row=hr + 5, column=helper_col, value="Groom")
    ws.cell(row=hr + 5, column=helper_col + 1, value=f"=COUNTIFS('Guest List'!B{guest_meta['first_data_row']}:B{guest_meta['last_data_row']},\"Groom\")")
    ws.cell(row=hr + 6, column=helper_col, value="Both")
    ws.cell(row=hr + 6, column=helper_col + 1, value=f"=COUNTIFS('Guest List'!B{guest_meta['first_data_row']}:B{guest_meta['last_data_row']},\"Both\")")
    make_pie(ws, "Guest Breakdown", f"Dashboard!${letter_hc}${hr+4}:${letter_hc}${hr+6}",
             f"Dashboard!${letter_hv}${hr+4}:${letter_hv}${hr+6}", f"H{charts_row+1}", width=9, height=7.5)

    # Save the date / invitation donuts
    ws.cell(row=hr + 8, column=helper_col, value="STD Sent").font = f_body()
    ws.cell(row=hr + 8, column=helper_col + 1, value=f"='Guest List'!C{gk}")
    ws.cell(row=hr + 9, column=helper_col, value="STD Not Sent")
    ws.cell(row=hr + 9, column=helper_col + 1, value=f"='Guest List'!A{gk}-'Guest List'!C{gk}")
    make_donut(ws, "Save the Dates Sent", f"Dashboard!${letter_hc}${hr+8}:${letter_hc}${hr+9}",
               f"Dashboard!${letter_hv}${hr+8}:${letter_hv}${hr+9}", f"A{charts_row+17}", colors=[BLUSH, GREY], width=9, height=7.5)
    ws.cell(row=hr + 11, column=helper_col, value="Invites Sent")
    ws.cell(row=hr + 11, column=helper_col + 1, value=f"='Guest List'!E{gk}")
    ws.cell(row=hr + 12, column=helper_col, value="Invites Not Sent")
    ws.cell(row=hr + 12, column=helper_col + 1, value=f"='Guest List'!A{gk}-'Guest List'!E{gk}")
    make_donut(ws, "Invitations Sent", f"Dashboard!${letter_hc}${hr+11}:${letter_hc}${hr+12}",
               f"Dashboard!${letter_hv}${hr+11}:${letter_hv}${hr+12}", f"H{charts_row+17}", colors=[POWDER, GREY], width=9, height=7.5)

    row = charts_row + 33

    # ---- Attire mini bar chart + Vendor Budget vs Actual bar chart ----
    ws.cell(row=hr + 14, column=helper_col, value="Attire Status").font = f_header()
    ws.cell(row=hr + 14, column=helper_col + 1, value="Count")
    astart = hr + 15
    for i, st in enumerate(ATTIRE_STATUS):
        ws.cell(row=astart + i, column=helper_col, value=st)
        ws.cell(row=astart + i, column=helper_col + 1, value=f"=COUNTIFS('Wedding Party'!G$9:G$60,{ws.cell(row=astart+i, column=helper_col).coordinate})")
    aend = astart + len(ATTIRE_STATUS) - 1
    make_bar(ws, "Attire Checklist Status", f"Dashboard!${letter_hc}${astart}:${letter_hc}${aend}",
             f"Dashboard!${letter_hv}${hr+14}:${letter_hv}${aend}", f"A{row}", width=14, height=8)

    efr, elr = budget_meta["exp_first"], budget_meta["exp_last"]
    make_bar(ws, "Vendor Budget vs Actual", f"'Wedding Budget'!$A${efr}:$A${elr}",
             f"'Wedding Budget'!$C${efr-1}:$D${elr}", f"F{row}", width=16, height=8, colors=[LAVENDER, PEACH])

    row2 = row + 17
    # ---- Today panel ----
    ws.cell(row=row2, column=1, value="TODAY").font = f_header()
    ws.merge_cells(start_row=row2, start_column=1, end_row=row2, end_column=4)
    ws.cell(row=row2, column=1).fill = fill(CREAM)
    for cc in (2, 3, 4):
        ws.cell(row=row2, column=cc).fill = fill(CREAM)
    ws.cell(row=row2 + 1, column=1, value="Checklist items due today").font = f_body(bold=True)
    v = ws.cell(row=row2 + 1, column=3, value=f"=COUNTIFS('Wedding Checklist'!C{cfr}:C{clr},TODAY(),'Wedding Checklist'!A{cfr}:A{clr},FALSE)")
    v.font = f_kpi_number(size=13)
    ws.cell(row=row2 + 2, column=1, value="Deadlines due today").font = f_body(bold=True)
    v2 = ws.cell(row=row2 + 2, column=3, value=f"=COUNTIFS('Wedding Budget'!C{budget_meta['pay_first']}:C{budget_meta['pay_last']},TODAY())")
    v2.font = f_kpi_number(size=13)

    # ---- Progress ratios ----
    ws.cell(row=row2, column=6, value="PROGRESS RATIOS").font = f_header()
    ws.merge_cells(start_row=row2, start_column=6, end_row=row2, end_column=9)
    for cc in range(6, 10):
        ws.cell(row=row2, column=cc).fill = fill(POWDER)
    labels_ratios = [
        ("Vendor Selection Progress", f"='Vendor Selection'!A{vendor_meta['first_data_row']-3}"),
        ("Wedding Party Confirmation", "=IFERROR(COUNTIF('Wedding Party'!A8:A60,TRUE)/COUNTA('Wedding Party'!B8:B60),0)"),
        ("Thank You Sent Ratio", "=IFERROR(COUNTIF('Gifts and Thank You'!D8:D400,TRUE)/COUNTA('Gifts and Thank You'!A8:A400),0)"),
    ]
    for i, (lab, formula) in enumerate(labels_ratios):
        r = row2 + 1 + i
        ws.cell(row=r, column=6, value=lab).font = f_body(bold=True)
        v = ws.cell(row=r, column=9, value=formula)
        v.number_format = "0%"
        v.font = f_kpi_number(size=12)

    freeze_header(ws, 1)
    set_col_widths(ws, {get_column_letter(c): 13 for c in range(1, 15)})
    return {}
