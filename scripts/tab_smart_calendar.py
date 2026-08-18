# -*- coding: utf-8 -*-
"""Tab 3: Smart Calendar - auto-populates from Checklist, Budget, Important Dates."""
from lib import *
import calendar as pycal
import datetime

def build_smart_calendar(wb, dv_named, checklist_meta, budget_meta):
    ws = new_sheet(wb, "Smart Calendar", tab_color=POWDER)
    row = title_banner(ws, "SMART CALENDAR", POWDER, row=1, col_start=1, col_end=7, size=16)
    row += 1

    # Month / Year selectors
    ws.cell(row=row, column=1, value="Month").font = f_kpi_label()
    ws.cell(row=row, column=1).fill = fill(CREAM)
    today = datetime.date.today()
    month_cell = ws.cell(row=row, column=2, value=pycal.month_name[today.month])
    month_cell.font = f_body(bold=True)
    month_cell.fill = fill(WHITE)
    ws.cell(row=row, column=3, value="Year").font = f_kpi_label()
    ws.cell(row=row, column=3).fill = fill(CREAM)
    year_cell = ws.cell(row=row, column=4, value=today.year)
    year_cell.font = f_body(bold=True)
    year_cell.fill = fill(WHITE)
    for cc in (1, 2, 3, 4):
        ws.cell(row=row, column=cc).border = BORDER_ALL
    dv_named(ws, f"B{row}:B{row}", "MonthNames")
    month_sel_row = row
    row += 2

    # Filter toggles
    ws.cell(row=row, column=1, value="SHOW ON CALENDAR:").font = f_body(bold=True, size=9)
    filters = ["Budget", "Checklist", "Important Dates", "Stationery", "Dance Lessons"]
    filt_cells = {}
    for i, fl in enumerate(filters):
        c = ws.cell(row=row, column=2 + i, value=True)
        c.alignment = CENTER
        c.border = BORDER_ALL
        lab = ws.cell(row=row - 1, column=2 + i, value=fl)
        lab.font = f_body(size=8, bold=True)
        lab.alignment = CENTER
        filt_cells[fl] = c.coordinate
    add_checkbox_col(ws, f"B{row}:F{row}")
    filter_row = row
    row += 2

    # Legend
    ws.cell(row=row, column=1, value="LEGEND:").font = f_body(bold=True, size=9)
    legend_items = [("Due Today", STATUS_YELLOW), ("Overdue", STATUS_RED), ("Due Later", SAGE)]
    for i, (lab, color) in enumerate(legend_items):
        c = ws.cell(row=row, column=2 + i, value=lab)
        c.fill = fill(color)
        c.font = f_body(size=9)
        c.alignment = CENTER
        c.border = BORDER_ALL
    row += 2

    # Calendar grid
    dow = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    dow_row = row
    for i, d in enumerate(dow):
        c = ws.cell(row=dow_row, column=1 + i, value=d)
        c.font = f_header()
        c.fill = fill(POWDER)
        c.alignment = CENTER
        c.border = BORDER_ALL
    row += 1
    grid_first_row = row

    cfr, clr = checklist_meta["first_data_row"], checklist_meta["last_data_row"]
    pfr, plr = budget_meta["pay_first"], budget_meta["pay_last"]

    # 6 weeks x 7 days grid, date computed via formula from month/year selector
    for week in range(6):
        for wd in range(7):
            r = grid_first_row + week * 3
            c = 1 + wd
            cell_idx = week * 7 + wd
            # date formula: first day of month + offset, aligned to weekday
            date_formula = (
                f'=DATE($D${month_sel_row},MATCH($B${month_sel_row},MonthNames,0),1)'
                f'-WEEKDAY(DATE($D${month_sel_row},MATCH($B${month_sel_row},MonthNames,0),1))+{cell_idx}+1'
            )
            dcell = ws.cell(row=r, column=c, value=date_formula)
            dcell.number_format = "D"
            dcell.font = f_body(size=9, bold=True)
            dcell.alignment = Alignment(horizontal="right", vertical="top")
            dcell.fill = fill(WHITE)
            ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c)
            # content cell: aggregated items due that date
            content_row = r + 1
            ws.merge_cells(start_row=content_row, start_column=c, end_row=r + 2, end_column=c)
            content_formula = (
                f'=TRIM('
                f'IF(AND(${filt_cells["Checklist"]},COUNTIFS(\'Wedding Checklist\'!$C${cfr}:$C${clr},{dcell.coordinate},\'Wedding Checklist\'!$A${cfr}:$A${clr},FALSE)>0),'
                f'COUNTIFS(\'Wedding Checklist\'!$C${cfr}:$C${clr},{dcell.coordinate},\'Wedding Checklist\'!$A${cfr}:$A${clr},FALSE)&" checklist item(s)"&CHAR(10),"")&'
                f'IF(AND(${filt_cells["Budget"]},COUNTIFS(\'Wedding Budget\'!$C${pfr}:$C${plr},{dcell.coordinate})>0),'
                f'COUNTIFS(\'Wedding Budget\'!$C${pfr}:$C${plr},{dcell.coordinate})&" payment(s) due"&CHAR(10),"")'
                f')'
            )
            ccell = ws.cell(row=content_row, column=c, value=content_formula)
            ccell.font = f_body(size=8)
            ccell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            ccell.fill = fill(OFFWHITE)
            for rr in (r, content_row, r + 2):
                ws.cell(row=rr, column=c).border = BORDER_ALL
            # conditional formatting: overdue vs today vs later, based on date cell vs TODAY()
            rng = f"{get_column_letter(c)}{r}:{get_column_letter(c)}{r+2}"
            ws.conditional_formatting.add(rng,
                FormulaRule(formula=[f'AND({dcell.coordinate}=TODAY())'], fill=fill(STATUS_YELLOW)))
            ws.conditional_formatting.add(rng,
                FormulaRule(formula=[f'AND({dcell.coordinate}<TODAY(),{ccell.coordinate}<>"")'], fill=fill(STATUS_RED)))
            ws.conditional_formatting.add(rng,
                FormulaRule(formula=[f'AND({dcell.coordinate}>TODAY(),{ccell.coordinate}<>"")'], fill=fill(SAGE)))
        ws.row_dimensions[grid_first_row + week * 3].height = 14
        ws.row_dimensions[grid_first_row + week * 3 + 1].height = 30

    grid_last_row = grid_first_row + 6 * 3 - 1
    set_col_widths(ws, {get_column_letter(c): 15 for c in range(1, 8)})

    # Important dates mini table
    imp_row = grid_last_row + 2
    ws.cell(row=imp_row, column=1, value="IMPORTANT DATES").font = f_header()
    ws.merge_cells(start_row=imp_row, start_column=1, end_row=imp_row, end_column=3)
    ws.cell(row=imp_row, column=1).fill = fill(CREAM)
    ws.cell(row=imp_row, column=2).fill = fill(CREAM)
    ws.cell(row=imp_row, column=3).fill = fill(CREAM)
    imp_row += 1
    hdr = table_header(ws, imp_row, 1, ["Task Description", "Due Date"], CREAM)
    imp_first = hdr
    sample_dates = [
        ("Book officiant meeting", -300), ("Order wedding invitations", -180),
        ("Final dress fitting", -30), ("Marriage license appointment", -14),
        ("Rehearsal dinner", -1),
    ]
    n_imp = 20
    for i in range(n_imp):
        r = hdr + i
        if i < len(sample_dates):
            label, off = sample_dates[i]
            ws.cell(row=r, column=1, value=label)
            ws.cell(row=r, column=2, value=f"='Get Started'!$C$4+({off})")
        ws.cell(row=r, column=2).number_format = DATE_FMT
        for cc in (1, 2):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    imp_last = hdr + n_imp - 1
    ws.conditional_formatting.add(f"B{imp_first}:B{imp_last}",
        FormulaRule(formula=[f'AND(B{imp_first}<TODAY(),B{imp_first}<>"")'], fill=fill(STATUS_RED)))

    freeze_header(ws, 1)
    return {"imp_first": imp_first, "imp_last": imp_last}
