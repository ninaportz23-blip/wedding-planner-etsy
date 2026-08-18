# -*- coding: utf-8 -*-
"""Tabs 15-16: Reception Seating Plan and Rehearsal Dinner Seating (synced with Guest List)."""
from lib import *
from data_lists import GUEST_TAG, YES_NO_AWAITED

def build_seating(wb, dv_named, guest_meta, sheet_name, color, n_tables=10, table_capacity=8):
    gfr, glr = guest_meta["first_data_row"], guest_meta["last_data_row"]
    ws = new_sheet(wb, sheet_name, tab_color=color)
    row = title_banner(ws, sheet_name.upper(), color, row=1, col_start=1, col_end=10, size=16)
    row += 1

    kpi_row = row
    labels = ["TOTAL SEATS", "CONFIRMED GUESTS", "CONFIRMED SEATS", "TENTATIVE SEATS", "REMAINING SEATS", "CONFIRMED TO BE SEATED"]
    for i, lab in enumerate(labels):
        kpi_box(ws, kpi_row, 1 + i * 2, lab, None, color, width_cols=2, font_size=13)
    row = kpi_row + 3

    ws.cell(row=row, column=1, value="Filter reference: Guest Tag / RSVP status are pulled live from the Guest List tab below.").font = f_body(italic=True, size=9)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    row += 2

    # Unseated guests helper table
    ws.cell(row=row, column=1, value="GUESTS WITHOUT A SEAT").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    ws.cell(row=row, column=1).fill = fill(CREAM)
    for cc in range(1, 5):
        ws.cell(row=row, column=cc).fill = fill(CREAM)
    row += 1
    unseated_header = row
    table_header(ws, unseated_header, 1, ["Name", "Guest Tag", "RSVP", "Table #"], CREAM)
    unseated_first = unseated_header + 1
    n_unseated = min(20, gfr and (glr - gfr + 1) or 20)
    unseated_last = unseated_first + n_unseated - 1
    for i in range(n_unseated):
        r = unseated_first + i
        gr = gfr + i
        ws.cell(row=r, column=1, value=f"=IF('Guest List'!$F{gr}=\"Yes\",'Guest List'!$A{gr},\"\")")
        ws.cell(row=r, column=2, value=f"=IF(A{r}<>\"\",'Guest List'!$B{gr},\"\")")
        ws.cell(row=r, column=3, value=f"=IF(A{r}<>\"\",'Guest List'!$F{gr},\"\")")
        ws.cell(row=r, column=4, value=None)
        for cc in range(1, 5):
            ws.cell(row=r, column=cc).border = BORDER_ALL
            ws.cell(row=r, column=cc).font = f_body()
            ws.cell(row=r, column=cc).fill = fill(OFFWHITE if i % 2 else WHITE)
    set_col_widths(ws, {"A": 20, "B": 12, "C": 10, "D": 10})
    set_col_widths(ws, {get_column_letter(c): 13 for c in range(5, 13)})

    # KPI formulas
    total_seats_cell = ws.cell(row=kpi_row + 1, column=1, value=f"={n_tables}*{table_capacity}")
    total_seats_cell.font = f_kpi_number(size=15)
    confirmed_guests_cell = ws.cell(row=kpi_row + 1, column=3, value="=COUNTIFS('Guest List'!$F$"+str(gfr)+":'Guest List'!$F$"+str(glr)+",\"Yes\")")
    confirmed_guests_cell.font = f_kpi_number(size=15)
    confirmed_seated_cell = ws.cell(row=kpi_row + 1, column=5, value=f"=COUNTIFS(D{unseated_first}:D{unseated_last},\"<>\")")
    confirmed_seated_cell.font = f_kpi_number(size=15)
    tentative_cell = ws.cell(row=kpi_row + 1, column=7,
        value="=COUNTIFS('Guest List'!$F$"+str(gfr)+":'Guest List'!$F$"+str(glr)+",\"Awaited\")")
    tentative_cell.font = f_kpi_number(size=15)
    remaining_cell = ws.cell(row=kpi_row + 1, column=9, value=f"=A{kpi_row+1}-E{kpi_row+1}")
    remaining_cell.font = f_kpi_number(size=15)
    conf_to_seat_cell = ws.cell(row=kpi_row + 1, column=11, value=f"=IFERROR(E{kpi_row+1}/C{kpi_row+1},0)")
    conf_to_seat_cell.number_format = "0%"
    conf_to_seat_cell.font = f_kpi_number(size=15)

    # Table blocks
    tbl_area_row = unseated_last + 3
    ws.cell(row=tbl_area_row - 1, column=1, value="TABLE BLOCKS").font = f_title(size=13)
    block_row = tbl_area_row
    col_offset = 6
    tables_per_row = 2
    block_height = 6 + table_capacity + 2
    for t in range(n_tables):
        tr = block_row + (t // tables_per_row) * (block_height + 1)
        tc = 1 + (t % tables_per_row) * col_offset
        ws.merge_cells(start_row=tr, start_column=tc, end_row=tr, end_column=tc + 3)
        c = ws.cell(row=tr, column=tc, value=f"Table {t+1}")
        c.font = f_header(color=CHARCOAL)
        c.fill = fill(color)
        c.alignment = CENTER
        for cc in range(tc, tc + 4):
            ws.cell(row=tr, column=cc).fill = fill(color)
        info_r = tr + 1
        ws.cell(row=info_r, column=tc, value="Capacity")
        ws.cell(row=info_r, column=tc + 1, value=table_capacity)
        ws.cell(row=info_r, column=tc + 2, value="Confirmed Seats")
        seat_first = info_r + 3
        seat_last = seat_first + table_capacity - 1
        ws.cell(row=info_r, column=tc + 3, value=f'=COUNTIFS(A{seat_first}:A{seat_last},"<>")')
        tags_r = info_r + 1
        ws.cell(row=tags_r, column=tc, value="Guest Tags Included")
        ws.cell(row=tags_r, column=tc + 1,
                value=f'=_xlfn.TEXTJOIN(", ",TRUE,IF(COUNTIF(B{seat_first}:B{seat_last},"Bride")>0,"Bride",""),IF(COUNTIF(B{seat_first}:B{seat_last},"Groom")>0,"Groom",""),IF(COUNTIF(B{seat_first}:B{seat_last},"Both")>0,"Both",""))')
        for cc in range(tc, tc + 4):
            ws.cell(row=info_r, column=cc).font = f_body(size=9)
            ws.cell(row=tags_r, column=cc).font = f_body(size=9)
        sub_header_r = info_r + 2
        table_header(ws, sub_header_r, tc, ["Name", "Guest Tag", "#", ""], color)
        for si in range(table_capacity):
            r = seat_first + si
            ws.cell(row=r, column=tc, value=None)
            ws.cell(row=r, column=tc + 1,
                value=f'=IFERROR(INDEX(\'Guest List\'!$B${gfr}:$B${glr},MATCH({get_column_letter(tc)}{r},\'Guest List\'!$A${gfr}:$A${glr},0)),"")')
            ws.cell(row=r, column=tc + 2, value=si + 1)
            for cc in range(tc, tc + 4):
                ws.cell(row=r, column=cc).border = BORDER_ALL
                ws.cell(row=r, column=cc).font = f_body(size=9)
    freeze_header(ws, unseated_header)
    return {"kpi_row": kpi_row, "unseated_first": unseated_first, "unseated_last": unseated_last}
