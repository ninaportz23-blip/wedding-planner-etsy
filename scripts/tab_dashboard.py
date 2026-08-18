# -*- coding: utf-8 -*-
"""Tab 2: Dashboard - fully automated, pulls from all other tabs.
Editorial, gap-free layout: hero band, KPI cards, then a tidy grid of
captioned chart cards that fill the width so nothing floats in white space."""
from lib import *
from data_lists import GUEST_TAG, ATTIRE_STATUS

NCOLS = 14  # A..N


def build_dashboard(wb, dv_named, checklist_meta, budget_meta, guest_meta, reception_meta, vendor_meta):
    ws = new_sheet(wb, "Dashboard", tab_color=LAVENDER)
    ws.sheet_view.showGridLines = False
    set_col_widths(ws, {get_column_letter(c): 12 for c in range(1, NCOLS + 1)})

    thin = Side(style="thin", color=GREY)

    def box(r0, c0, r1, c1, color=GREY):
        """Draw a light rectangular outline around a cell block (card edge)."""
        side = Side(style="thin", color=color)
        for c in range(c0, c1 + 1):
            top = ws.cell(row=r0, column=c); bot = ws.cell(row=r1, column=c)
            top.border = Border(top=side, left=top.border.left, right=top.border.right, bottom=top.border.bottom)
            bot.border = Border(bottom=side, left=bot.border.left, right=bot.border.right, top=bot.border.top)
        for r in range(r0, r1 + 1):
            lf = ws.cell(row=r, column=c0); rt = ws.cell(row=r, column=c1)
            lf.border = Border(left=side, top=lf.border.top, bottom=lf.border.bottom, right=lf.border.right)
            rt.border = Border(right=side, top=rt.border.top, bottom=rt.border.bottom, left=rt.border.left)

    def fill_block(r0, c0, r1, c1, color):
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                ws.cell(row=r, column=c).fill = fill(color)

    def card(r0, c0, r1, c1, caption, accent):
        """White card with a soft accent caption strip (serif) and outline."""
        fill_block(r0, c0, r1, c1, WHITE)
        fill_block(r0, c0, r0, c1, accent)
        ws.merge_cells(start_row=r0, start_column=c0, end_row=r0, end_column=c1)
        cap = ws.cell(row=r0, column=c0, value=caption)
        cap.font = Font(name=FONT_SERIF, size=11.5, color=CHARCOAL)
        cap.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[r0].height = 20
        box(r0, c0, r1, c1)

    # ---------------------------------------------------------- title band --
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=NCOLS)
    t = ws.cell(row=1, column=1, value="Wedding Dashboard")
    t.font = Font(name=FONT_SERIF, size=22, color=CHARCOAL)
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    fill_block(1, 1, 1, NCOLS, LAVENDER)
    ws.row_dimensions[1].height = 40
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=NCOLS)
    sub = ws.cell(row=2, column=1, value="EVERYTHING AT A GLANCE")
    sub.font = Font(name=FONT_NAME, size=8, bold=True, color="8A82B0")
    sub.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 16

    # --------------------------------------------------------------- hero ----
    hr0, hr1 = 4, 7
    for r in range(hr0, hr1 + 1):
        ws.row_dimensions[r].height = 36
    # couple names
    ws.merge_cells(start_row=hr0, start_column=1, end_row=hr1, end_column=3)
    cpl = ws.cell(row=hr0, column=1, value="='Get Started'!$A$4&\" & \"&'Get Started'!$B$4")
    cpl.font = Font(name=FONT_SERIF, size=17, color=CHARCOAL)
    cpl.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    fill_block(hr0, 1, hr1, 3, BLUSH); box(hr0, 1, hr1, 3, DARK_BLUSH)
    # countdown
    ws.merge_cells(start_row=hr0, start_column=4, end_row=hr0, end_column=6)
    cdl = ws.cell(row=hr0, column=4, value="DAYS TO GO")
    cdl.font = f_eyebrow(); cdl.alignment = CENTER
    fill_block(hr0, 4, hr0, 6, CREAM)
    ws.merge_cells(start_row=hr0 + 1, start_column=4, end_row=hr1, end_column=6)
    cdv = ws.cell(row=hr0 + 1, column=4, value="=DATEDIF(TODAY(),'Get Started'!$C$4,\"d\")")
    cdv.font = Font(name=FONT_SERIF, bold=False, size=34, color=CHARCOAL)
    cdv.alignment = CENTER
    fill_block(hr0 + 1, 4, hr1, 6, WHITE); box(hr0, 4, hr1, 6, DARK_CREAM)
    # date
    ws.merge_cells(start_row=hr0, start_column=7, end_row=hr0, end_column=9)
    wdl = ws.cell(row=hr0, column=7, value="WEDDING DATE")
    wdl.font = f_eyebrow(); wdl.alignment = CENTER
    fill_block(hr0, 7, hr0, 9, SAGE)
    ws.merge_cells(start_row=hr0 + 1, start_column=7, end_row=hr1, end_column=9)
    wdv = ws.cell(row=hr0 + 1, column=7, value="='Get Started'!$C$4")
    wdv.number_format = DATE_FMT
    wdv.font = Font(name=FONT_SERIF, size=15, color=CHARCOAL)
    wdv.alignment = CENTER
    fill_block(hr0 + 1, 7, hr1, 9, WHITE); box(hr0, 7, hr1, 9, DARK_SAGE)
    # photo frame (embedded placeholder) cols 10..14 (~445px x 192px)
    ws.merge_cells(start_row=hr0, start_column=10, end_row=hr1, end_column=NCOLS)
    fill_block(hr0, 10, hr1, NCOLS, WHITE)
    embed_image(ws, "photo_hero.png", f"J{hr0}", 445, 192)

    # ----------------------------------------------------------- KPI cards ---
    kb = budget_meta["kpi_row"] + 1
    gk = guest_meta["kpi_row"] + 1
    rk = reception_meta["kpi_row"] + 1

    def kpi(r, c, label, formula, color, fmt=CURRENCY_FMT):
        v = kpi_box(ws, r, c, label, None, color, width_cols=2, font_size=14)
        v.value = formula
        if fmt:
            v.number_format = fmt
        v.font = Font(name=FONT_SERIF, size=14, color=CHARCOAL)
        return v

    k1 = 9
    kpi(k1, 1, "TOTAL BUDGET", f"='Wedding Budget'!A{kb}", LAVENDER)
    kpi(k1, 3, "TOTAL SPENT", f"='Wedding Budget'!E{kb}", BLUSH)
    kpi(k1, 5, "LEFT TO SPEND", f"='Wedding Budget'!G{kb}", SAGE)
    kpi(k1, 7, "PAYMENTS LEFT", f"='Wedding Budget'!I{kb}", PEACH)
    kpi(k1, 9, "CONFIRMED GUESTS", f"='Guest List'!G{gk}", POWDER, fmt=None)
    kpi(k1, 11, "SEATS LEFT", f"='Reception Seating Plan'!I{rk}", CREAM, fmt=None)
    kpi(k1, 13, "SEATED", f"='Reception Seating Plan'!E{rk}", BLUSH, fmt=None)

    # ---------------------------------------------- helper data (offscreen) --
    helper_col = 17  # Q+, outside print area
    hc = get_column_letter(helper_col)
    hv = get_column_letter(helper_col + 1)
    hR = 4
    cfr, clr = checklist_meta["first_data_row"], checklist_meta["last_data_row"]
    gfr, glr = guest_meta["first_data_row"], guest_meta["last_data_row"]
    ws.cell(row=hR + 1, column=helper_col, value="Done")
    ws.cell(row=hR + 1, column=helper_col + 1, value=f"=COUNTIFS('Wedding Checklist'!A{cfr}:A{clr},ChkVal)")
    ws.cell(row=hR + 2, column=helper_col, value="Remaining")
    ws.cell(row=hR + 2, column=helper_col + 1, value=f"=COUNTIFS('Wedding Checklist'!A{cfr}:A{clr},UnchkVal)")
    ws.cell(row=hR + 4, column=helper_col, value="Bride")
    ws.cell(row=hR + 4, column=helper_col + 1, value=f"=COUNTIFS('Guest List'!B{gfr}:B{glr},\"Bride\")")
    ws.cell(row=hR + 5, column=helper_col, value="Groom")
    ws.cell(row=hR + 5, column=helper_col + 1, value=f"=COUNTIFS('Guest List'!B{gfr}:B{glr},\"Groom\")")
    ws.cell(row=hR + 6, column=helper_col, value="Both")
    ws.cell(row=hR + 6, column=helper_col + 1, value=f"=COUNTIFS('Guest List'!B{gfr}:B{glr},\"Both\")")
    ws.cell(row=hR + 8, column=helper_col, value="Sent")
    ws.cell(row=hR + 8, column=helper_col + 1, value=f"='Guest List'!C{gk}")
    ws.cell(row=hR + 9, column=helper_col, value="Not Sent")
    ws.cell(row=hR + 9, column=helper_col + 1, value=f"='Guest List'!A{gk}-'Guest List'!C{gk}")
    ws.cell(row=hR + 11, column=helper_col, value="Sent")
    ws.cell(row=hR + 11, column=helper_col + 1, value=f"='Guest List'!E{gk}")
    ws.cell(row=hR + 12, column=helper_col, value="Not Sent")
    ws.cell(row=hR + 12, column=helper_col + 1, value=f"='Guest List'!A{gk}-'Guest List'!E{gk}")
    ws.cell(row=hR + 14, column=helper_col, value="Attire Status")
    astart = hR + 15
    for i, st in enumerate(ATTIRE_STATUS):
        ws.cell(row=astart + i, column=helper_col, value=st)
        ws.cell(row=astart + i, column=helper_col + 1,
                value=f"=COUNTIFS('Wedding Party'!G$9:G$60,{ws.cell(row=astart+i, column=helper_col).coordinate})")
    aend = astart + len(ATTIRE_STATUS) - 1

    def dref(col, r0, r1):
        L = get_column_letter(col)
        return f"Dashboard!${L}${r0}:${L}${r1}"

    # ------------------------------------------------------- chart grid ------
    # eyebrow
    ws.merge_cells(start_row=12, start_column=1, end_row=12, end_column=NCOLS)
    eb = ws.cell(row=12, column=1, value="OVERVIEW")
    eb.font = Font(name=FONT_NAME, size=8, bold=True, color="8A82B0")
    eb.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[12].height = 16

    LCOLS = (1, 7)     # left card A:G
    RCOLS = (8, NCOLS)  # right card H:N

    # --- row A: checklist progress donut + guest breakdown pie
    ra0, ra1 = 13, 25
    card(ra0, LCOLS[0], ra1, LCOLS[1], "Checklist Progress", SAGE)
    card(ra0, RCOLS[0], ra1, RCOLS[1], "Guest Breakdown", BLUSH)
    make_donut(ws, "", dref(helper_col, hR + 1, hR + 2), dref(helper_col + 1, hR + 1, hR + 2),
               f"B{ra0+1}", colors=[SAGE, GREY], width=8.4, height=6.2, legend="b")
    make_pie(ws, "", dref(helper_col, hR + 4, hR + 6), dref(helper_col + 1, hR + 4, hR + 6),
             f"I{ra0+1}", colors=[LAVENDER, BLUSH, SAGE], width=8.4, height=6.2, legend="b")

    # --- row B: save the dates donut + invitations donut
    rb0, rb1 = 27, 39
    card(rb0, LCOLS[0], rb1, LCOLS[1], "Save-the-Dates Sent", BLUSH)
    card(rb0, RCOLS[0], rb1, RCOLS[1], "Invitations Sent", POWDER)
    make_donut(ws, "", dref(helper_col, hR + 8, hR + 9), dref(helper_col + 1, hR + 8, hR + 9),
               f"B{rb0+1}", colors=[BLUSH, GREY], width=8.4, height=6.2, legend="b")
    make_donut(ws, "", dref(helper_col, hR + 11, hR + 12), dref(helper_col + 1, hR + 11, hR + 12),
               f"I{rb0+1}", colors=[POWDER, GREY], width=8.4, height=6.2, legend="b")

    # --- row C: attire status bar + vendor budget vs actual bar
    rc0, rc1 = 41, 54
    card(rc0, LCOLS[0], rc1, LCOLS[1], "Attire Status", CREAM)
    card(rc0, RCOLS[0], rc1, RCOLS[1], "Budget vs Actual by Category", LAVENDER)
    make_bar(ws, "", dref(helper_col, astart, aend), dref(helper_col + 1, hR + 14, aend),
             f"A{rc0+1}", width=10.5, height=6.6, colors=[LAVENDER])
    efr, elr = budget_meta["exp_first"], budget_meta["exp_last"]
    make_bar(ws, "", f"'Wedding Budget'!$A${efr}:$A${elr}", f"'Wedding Budget'!$C${efr-1}:$D${elr}",
             f"H{rc0+1}", width=10.5, height=6.6, colors=[LAVENDER, PEACH], series_titles=True)

    # ------------------------------------------------------ bottom panels ----
    rp0, rp1 = 56, 61
    card(rp0, LCOLS[0], rp1, LCOLS[1], "Due Today", PEACH)
    card(rp0, RCOLS[0], rp1, RCOLS[1], "Progress", POWDER)
    # due today
    ws.cell(row=rp0 + 1, column=1, value="Checklist items due today").font = f_body(bold=True)
    ws.merge_cells(start_row=rp0 + 1, start_column=1, end_row=rp0 + 1, end_column=5)
    v = ws.cell(row=rp0 + 1, column=7,
                value=f"=COUNTIFS('Wedding Checklist'!C{cfr}:C{clr},TODAY(),'Wedding Checklist'!A{cfr}:A{clr},UnchkVal)")
    v.font = Font(name=FONT_SERIF, size=15, color=CHARCOAL); v.alignment = CENTER
    ws.cell(row=rp0 + 3, column=1, value="Vendor payments due today").font = f_body(bold=True)
    ws.merge_cells(start_row=rp0 + 3, start_column=1, end_row=rp0 + 3, end_column=5)
    v2 = ws.cell(row=rp0 + 3, column=7,
                 value=f"=COUNTIFS('Wedding Budget'!C{budget_meta['pay_first']}:C{budget_meta['pay_last']},TODAY())")
    v2.font = Font(name=FONT_SERIF, size=15, color=CHARCOAL); v2.alignment = CENTER
    # progress ratios
    ratios = [
        ("Vendor Selection", f"='Vendor Selection'!A{vendor_meta['first_data_row']-3}"),
        ("Wedding Party Confirmed", "=IFERROR(COUNTIF('Wedding Party'!A8:A60,ChkVal)/COUNTA('Wedding Party'!B8:B60),0)"),
        ("Thank-Yous Sent", "=IFERROR(COUNTIF('Gifts and Thank You'!D8:D400,ChkVal)/COUNTA('Gifts and Thank You'!A8:A400),0)"),
    ]
    for i, (lab, formula) in enumerate(ratios):
        r = rp0 + 1 + i
        ws.cell(row=r, column=8, value=lab).font = f_body(bold=True)
        ws.merge_cells(start_row=r, start_column=8, end_row=r, end_column=12)
        vr = ws.cell(row=r, column=13, value=formula)
        vr.number_format = "0%"
        vr.font = Font(name=FONT_SERIF, size=13, color=CHARCOAL); vr.alignment = CENTER
        ws.merge_cells(start_row=r, start_column=13, end_row=r, end_column=NCOLS)

    freeze_header(ws, 1)
    return {}
