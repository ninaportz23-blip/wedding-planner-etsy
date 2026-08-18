# -*- coding: utf-8 -*-
"""Tab 9: Wedding Budget - core automated tab."""
from lib import *
from data_lists import VENDOR_CATEGORY, PAYMENT_TYPE, PAYMENT_STATUS

def build_budget(wb, dv_named, vendor_meta):
    ws = new_sheet(wb, "Wedding Budget", tab_color=LAVENDER)
    vfr, vlr = vendor_meta["first_data_row"], vendor_meta["last_data_row"]
    row = title_banner(ws, "WEDDING BUDGET", LAVENDER, row=1, col_start=1, col_end=10, size=16)
    row += 1

    kpi_row = row
    labels = ["TOTAL BUDGET", "LEFT TO BUDGET", "TOTAL SPENT", "LEFT TO SPEND", "VENDOR PAYMENTS LEFT"]
    for i, lab in enumerate(labels):
        kpi_box(ws, kpi_row, 1 + i * 2, lab, None, LAVENDER, width_cols=2, font_size=13)
    row = kpi_row + 3

    # --- Budget Funding table ---
    ws.cell(row=row, column=1, value="BUDGET FUNDING").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
    ws.cell(row=row, column=1).fill = fill(BLUSH)
    ws.cell(row=row, column=2).fill = fill(BLUSH)
    row += 1
    fund_header = row
    table_header(ws, fund_header, 1, ["Contributor", "Amount"], BLUSH)
    fund_first = fund_header + 1
    contributors = [("Bride and Groom Savings", 12000), ("Bride's Parents", 5000), ("Groom's Parents", 4000), ("Other Family", 0), ("Other", 0)]
    for i, (name, amt) in enumerate(contributors):
        r = fund_first + i
        ws.cell(row=r, column=1, value=name)
        c = ws.cell(row=r, column=2, value=amt)
        c.number_format = CURRENCY_FMT
        for cc in (1, 2):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
    fund_last = fund_first + len(contributors) - 1
    total_row = fund_last + 1
    ws.cell(row=total_row, column=1, value="Total Budget").font = f_header()
    tb_cell = ws.cell(row=total_row, column=2, value=f"=SUM(B{fund_first}:B{fund_last})")
    tb_cell.number_format = CURRENCY_FMT
    tb_cell.font = f_header()
    for cc in (1, 2):
        ws.cell(row=total_row, column=cc).border = BORDER_ALL
        ws.cell(row=total_row, column=cc).fill = fill(CREAM)
    set_col_widths(ws, {"A": 26, "B": 14})

    # --- Expense Summary table ---
    exp_title_row = total_row + 2
    ws.cell(row=exp_title_row, column=1, value="EXPENSE SUMMARY").font = f_header()
    ws.merge_cells(start_row=exp_title_row, start_column=1, end_row=exp_title_row, end_column=5)
    for cc in range(1, 6):
        ws.cell(row=exp_title_row, column=cc).fill = fill(SAGE)
    exp_header = exp_title_row + 1
    table_header(ws, exp_header, 1, ["Category", "Vendor / Subcategory", "Budget", "Actual", "Left"], SAGE)
    exp_first = exp_header + 1
    exp_last = exp_first + len(VENDOR_CATEGORY) - 1
    default_budgets = {
        "Venue": 6000, "Catering": 4200, "Photography": 3200, "Videography": 1500, "Florist": 900,
        "DJ/Band": 800, "Officiant": 400, "Rentals": 500, "Decor": 400, "Hair & Makeup": 350,
        "Transportation": 250, "Cake": 350, "Stationery": 250, "Favors": 250, "Lighting": 250,
    }
    for i, cat in enumerate(VENDOR_CATEGORY):
        r = exp_first + i
        ws.cell(row=r, column=1, value=cat)
        ws.cell(row=r, column=2, value=f"=IFERROR(INDEX('Vendor Selection'!$C${vfr}:$C${vlr},MATCH(1,('Vendor Selection'!$B${vfr}:$B${vlr}=$A{r})*('Vendor Selection'!$A${vfr}:$A${vlr}=\"Yes\"),0)),\"\")")
        bcell = ws.cell(row=r, column=3, value=default_budgets.get(cat, 500))
        bcell.number_format = CURRENCY_FMT
        acell = ws.cell(row=r, column=4,
            value=f"=IFERROR(SUMIFS('Vendor Selection'!$G${vfr}:$G${vlr},'Vendor Selection'!$B${vfr}:$B${vlr},$A{r},'Vendor Selection'!$A${vfr}:$A${vlr},\"Yes\"),0)")
        acell.number_format = CURRENCY_FMT
        lcell = ws.cell(row=r, column=5, value=f"=C{r}-D{r}")
        lcell.number_format = CURRENCY_FMT
        for cc in range(1, 6):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    exp_total_row = exp_last + 1
    ws.cell(row=exp_total_row, column=1, value="Total").font = f_header()
    for col, letter in [(3, "C"), (4, "D"), (5, "E")]:
        c = ws.cell(row=exp_total_row, column=col, value=f"=SUM({letter}{exp_first}:{letter}{exp_last})")
        c.number_format = CURRENCY_FMT
        c.font = f_header()
    for cc in range(1, 6):
        ws.cell(row=exp_total_row, column=cc).fill = fill(CREAM)
        ws.cell(row=exp_total_row, column=cc).border = BORDER_ALL
    ws.conditional_formatting.add(f"E{exp_first}:E{exp_last}",
        CellIsRule(operator="lessThan", formula=["0"], fill=fill(STATUS_RED)))

    # --- KPI formulas now that totals exist ---
    v_total_budget = ws.cell(row=kpi_row + 1, column=1, value=f"=B{total_row}")
    v_total_budget.number_format = CURRENCY_FMT
    v_total_budget.font = f_kpi_number(size=13)
    v_left_budget = ws.cell(row=kpi_row + 1, column=3, value=f"=B{total_row}-C{exp_total_row}")
    v_left_budget.number_format = CURRENCY_FMT
    v_left_budget.font = f_kpi_number(size=13)
    v_spent = ws.cell(row=kpi_row + 1, column=5, value=f"=D{exp_total_row}")
    v_spent.number_format = CURRENCY_FMT
    v_spent.font = f_kpi_number(size=13)
    v_left_spend = ws.cell(row=kpi_row + 1, column=7, value=f"=B{total_row}-D{exp_total_row}")
    v_left_spend.number_format = CURRENCY_FMT
    v_left_spend.font = f_kpi_number(size=13)

    # --- Payment Schedule & Log ---
    pay_title_row = exp_total_row + 2
    ws.cell(row=pay_title_row, column=1, value="PAYMENT SCHEDULE AND LOG").font = f_header()
    ws.merge_cells(start_row=pay_title_row, start_column=1, end_row=pay_title_row, end_column=7)
    for cc in range(1, 8):
        ws.cell(row=pay_title_row, column=cc).fill = fill(POWDER)
    pay_header = pay_title_row + 1
    table_header(ws, pay_header, 1, ["Type", "Vendor Name", "Due Date", "Amount", "Paid Date", "Status", "Notes"], POWDER)
    pay_first = pay_header + 1
    n_pay = 40
    pay_last = pay_first + n_pay - 1
    sample_payments = [
        ("Deposit", "Willow Creek Barn", -270, 4250, -260),
        ("Deposit", "Copper Table Catering", -240, 3100, -230),
        ("Progress Payment", "Golden Hour Studio", -120, 1600, None),
    ]
    import datetime
    today = datetime.date.today()
    for i in range(n_pay):
        r = pay_first + i
        ws.cell(row=r, column=1, value=PAYMENT_TYPE[i % len(PAYMENT_TYPE)] if i < len(sample_payments) else "")
        if i < len(sample_payments):
            ptype, vname, due_off, amt, paid_off = sample_payments[i]
            ws.cell(row=r, column=1, value=ptype)
            ws.cell(row=r, column=2, value=vname)
            ws.cell(row=r, column=3, value=f"='Get Started'!$C$4+({due_off})")
            ws.cell(row=r, column=4, value=amt).number_format = CURRENCY_FMT
            if paid_off:
                ws.cell(row=r, column=5, value=f"='Get Started'!$C$4+({paid_off})")
            ws.cell(row=r, column=6,
                value=f'=IF(E{r}<>"","Paid",IF(C{r}<TODAY(),"Overdue",IF(C{r}<=TODAY()+14,"Due Soon","Not Due")))')
        else:
            ws.cell(row=r, column=6, value=f'=IF(E{r}<>"","Paid",IF(AND(C{r}<>"",C{r}<TODAY()),"Overdue",IF(AND(C{r}<>"",C{r}<=TODAY()+14),"Due Soon",IF(C{r}<>"","Not Due",""))))')
        ws.cell(row=r, column=3).number_format = DATE_FMT
        ws.cell(row=r, column=4).number_format = CURRENCY_FMT
        ws.cell(row=r, column=5).number_format = DATE_FMT
        for cc in range(1, 8):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)

    dv_named(ws, f"A{pay_first}:A{pay_last}", "PaymentType")
    ws.conditional_formatting.add(f"F{pay_first}:F{pay_last}",
        FormulaRule(formula=[f'EXACT(F{pay_first},"Overdue")'], fill=fill(STATUS_RED)))
    ws.conditional_formatting.add(f"F{pay_first}:F{pay_last}",
        FormulaRule(formula=[f'EXACT(F{pay_first},"Paid")'], fill=fill(STATUS_GREEN)))
    ws.conditional_formatting.add(f"F{pay_first}:F{pay_last}",
        FormulaRule(formula=[f'EXACT(F{pay_first},"Due Soon")'], fill=fill(STATUS_YELLOW)))

    v_vendor_left = ws.cell(row=kpi_row + 1, column=9,
        value=f'=SUMIFS(D{pay_first}:D{pay_last},F{pay_first}:F{pay_last},"<>Paid")-SUMIFS(D{pay_first}:D{pay_last},F{pay_first}:F{pay_last},"")')
    # simplify: vendor payments left = sum of amounts where status not Paid and Type not blank
    v_vendor_left = ws.cell(row=kpi_row + 1, column=9,
        value=f'=SUMPRODUCT((A{pay_first}:A{pay_last}<>"")*(F{pay_first}:F{pay_last}<>"Paid")*D{pay_first}:D{pay_last})')
    v_vendor_left.number_format = CURRENCY_FMT
    v_vendor_left.font = f_kpi_number(size=13)

    ws.cell(row=pay_title_row, column=9, value="Reminder: payments turn red once past due and unpaid.").font = f_body(italic=True, size=9)
    ws.merge_cells(start_row=pay_title_row, start_column=9, end_row=pay_title_row + 1, end_column=11)

    freeze_header(ws, exp_header)
    set_col_widths(ws, {"C": 14, "D": 14, "E": 14, "F": 14, "G": 24})
    set_col_widths(ws, {get_column_letter(c): 13 for c in range(8, 15)})

    # Bar chart: Budget vs Actual by category
    letter_a = get_column_letter(1)
    make_bar(ws, "Expenses: Budget vs Actual",
             f"'Wedding Budget'!$A${exp_first}:$A${exp_last}",
             f"'Wedding Budget'!$C${exp_header}:$D${exp_last}",
             f"I{exp_header}", width=18, height=10, colors=[LAVENDER, PEACH])

    return {
        "kpi_row": kpi_row, "exp_first": exp_first, "exp_last": exp_last, "exp_total_row": exp_total_row,
        "pay_first": pay_first, "pay_last": pay_last, "total_row": total_row,
    }
