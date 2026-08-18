# -*- coding: utf-8 -*-
"""Tab 4: Wedding Checklist - 850+ pre-filled items across 12 timeframe sections."""
from lib import *
from data_lists import CHECKLIST_SECTIONS, PRIORITY, ASSIGNED_TO
import datetime

PRIORITY_COLORS = {"Low": SAGE, "Medium": CREAM, "High": PEACH, "Urgent": STATUS_RED}

def build_checklist(wb, dv_named):
    ws = new_sheet(wb, "Wedding Checklist", tab_color=LAVENDER)
    row = title_banner(ws, "WEDDING CHECKLIST", LAVENDER, row=1, col_start=1, col_end=6, size=16)
    ws.cell(row=row, column=1, value="Check off each task as you complete it. Due dates are examples, set to guide pacing before the wedding date on the Get Started tab.")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=6)
    ws.cell(row=row, column=1).font = f_body(italic=True, size=9)
    row += 2

    header_row_top = row
    headers = ["Done", "Task", "Due Date", "Assigned To", "Priority", "Section"]
    table_header(ws, row, 1, headers, LAVENDER)
    row += 1
    first_data_row = row

    # anchor wedding date reference for due-date formulas: 'Get Started'!C4
    wedding_date_ref = "'Get Started'!$C$4"

    section_ranges = {}
    color_cycle = PALETTE_ROTATION
    total_items = sum(len(items) for _, items in CHECKLIST_SECTIONS)
    idx_all = 0
    for s_i, (section_name, items) in enumerate(CHECKLIST_SECTIONS):
        section_start = row
        for item in items:
            c_done = ws.cell(row=row, column=1, value=False)
            c_done.alignment = CENTER
            c_task = ws.cell(row=row, column=2, value=item)
            c_task.alignment = LEFT
            # due date: spread items within a section backwards from wedding date by rough offset
            c_date = ws.cell(row=row, column=3)
            c_date.number_format = DATE_FMT
            c_assigned = ws.cell(row=row, column=4, value="Both")
            c_priority = ws.cell(row=row, column=5, value="Medium")
            c_section = ws.cell(row=row, column=6, value=section_name)
            for cc in (1, 2, 3, 4, 5, 6):
                ws.cell(row=row, column=cc).border = BORDER_ALL
                ws.cell(row=row, column=cc).font = f_body()
                if row % 2 == 0:
                    ws.cell(row=row, column=cc).fill = fill("FFFFFF")
                else:
                    ws.cell(row=row, column=cc).fill = fill(OFFWHITE)
            idx_all += 1
            row += 1
        section_end = row - 1
        section_ranges[section_name] = (section_start, section_end)

    last_data_row = row - 1

    # Due date formulas: offset per section (approx months-before-wedding midpoints), staggered evenly
    section_offsets_days = {
        "12+ Months Before": 400, "10-12 Months Before": 330, "8-10 Months Before": 270,
        "6-8 Months Before": 210, "4-6 Months Before": 150, "2-4 Months Before": 90,
        "1 Month Before": 30, "2 Weeks Before": 14, "1 Week Before": 7,
        "2 Days Before": 2, "1 Day Before": 1, "Legal Items": 180,
    }
    for section_name, (s0, s1) in section_ranges.items():
        base_offset = section_offsets_days[section_name]
        n = s1 - s0 + 1
        for i, r in enumerate(range(s0, s1 + 1)):
            # spread linearly +/- a few days across section for visual variety
            spread = int((i / max(n - 1, 1)) * 10) - 5
            ws.cell(row=r, column=3, value=f"={wedding_date_ref}-{base_offset}+{spread}")

    # dropdowns
    dv_named(ws, f"D{first_data_row}:D{last_data_row}", "AssignedTo")
    dv_named(ws, f"E{first_data_row}:E{last_data_row}", "Priority")
    dv_named(ws, f"F{first_data_row}:F{last_data_row}", "ChecklistSections")
    add_checkbox_col(ws, f"A{first_data_row}:A{last_data_row}")

    # conditional formatting
    ws.conditional_formatting.add(
        f"E{first_data_row}:E{last_data_row}",
        FormulaRule(formula=[f'EXACT(E{first_data_row},"Urgent")'], fill=fill(STATUS_RED)))
    ws.conditional_formatting.add(
        f"E{first_data_row}:E{last_data_row}",
        FormulaRule(formula=[f'EXACT(E{first_data_row},"High")'], fill=fill(PEACH)))
    ws.conditional_formatting.add(
        f"E{first_data_row}:E{last_data_row}",
        FormulaRule(formula=[f'EXACT(E{first_data_row},"Medium")'], fill=fill(STATUS_YELLOW)))
    ws.conditional_formatting.add(
        f"E{first_data_row}:E{last_data_row}",
        FormulaRule(formula=[f'EXACT(E{first_data_row},"Low")'], fill=fill(SAGE)))
    # overdue + not done -> red task text row banding via date col
    ws.conditional_formatting.add(
        f"C{first_data_row}:C{last_data_row}",
        FormulaRule(formula=[f'AND(C{first_data_row}<TODAY(),A{first_data_row}=FALSE)'], fill=fill(STATUS_RED)))
    # done rows -> green highlight on Task cell
    ws.conditional_formatting.add(
        f"B{first_data_row}:B{last_data_row}",
        FormulaRule(formula=[f'A{first_data_row}=TRUE'], fill=fill(STATUS_GREEN)))

    freeze_header(ws, first_data_row)
    set_col_widths(ws, {"A": 8, "B": 58, "C": 14, "D": 14, "E": 12, "F": 20})
    ws.row_dimensions[header_row_top].height = 20

    # ---- Summary / progress area to the right, plus charts, placed below main table start marker ----
    summary_col = 8  # column H
    srow = 4
    ws.cell(row=srow, column=summary_col, value="PROGRESS BY SECTION").font = f_header()
    ws.merge_cells(start_row=srow, start_column=summary_col, end_row=srow, end_column=summary_col + 2)
    ws.cell(row=srow, column=summary_col).fill = fill(LAVENDER)
    ws.cell(row=srow, column=summary_col + 1).fill = fill(LAVENDER)
    ws.cell(row=srow, column=summary_col + 2).fill = fill(LAVENDER)
    srow += 1
    table_header(ws, srow, summary_col, ["Section", "% Done", "Count"], LAVENDER)
    srow += 1
    section_summary_start = srow
    for section_name, (s0, s1) in section_ranges.items():
        ws.cell(row=srow, column=summary_col, value=section_name).font = f_body()
        pct_cell = ws.cell(row=srow, column=summary_col + 1,
                            value=f"=COUNTIFS(A{s0}:A{s1},TRUE)/COUNTA(B{s0}:B{s1})")
        pct_cell.number_format = "0%"
        pct_cell.font = f_body()
        cnt_cell = ws.cell(row=srow, column=summary_col + 2, value=f"=COUNTA(B{s0}:B{s1})")
        cnt_cell.font = f_body()
        for cc in range(summary_col, summary_col + 3):
            ws.cell(row=srow, column=cc).border = BORDER_ALL
        srow += 1
    section_summary_end = srow - 1

    # donut: tasks left to do by assigned person
    srow += 1
    ws.cell(row=srow, column=summary_col, value="TASKS REMAINING BY PERSON").font = f_header()
    ws.merge_cells(start_row=srow, start_column=summary_col, end_row=srow, end_column=summary_col + 2)
    ws.cell(row=srow, column=summary_col).fill = fill(BLUSH)
    ws.cell(row=srow, column=summary_col + 1).fill = fill(BLUSH)
    ws.cell(row=srow, column=summary_col + 2).fill = fill(BLUSH)
    srow += 1
    person_start = srow
    for person in ["Bride", "Groom", "Both", "Wedding Planner", "Maid of Honor", "Best Man", "Parent", "Other"]:
        ws.cell(row=srow, column=summary_col, value=person).font = f_body()
        ws.cell(row=srow, column=summary_col + 1,
                value=f'=COUNTIFS($D${first_data_row}:$D${last_data_row},{ws.cell(row=srow, column=summary_col).coordinate},$A${first_data_row}:$A${last_data_row},FALSE)').font = f_body()
        srow += 1
    person_end = srow - 1

    letter_cat = get_column_letter(summary_col)
    letter_val = get_column_letter(summary_col + 1)
    make_bar(ws, "Progress by Section (% Done)",
             f"'Wedding Checklist'!${letter_cat}${section_summary_start}:${letter_cat}${section_summary_end}",
             f"'Wedding Checklist'!${letter_val}${section_summary_start - 1}:${letter_val}${section_summary_end}",
             f"J4", width=16, height=9)

    make_donut(ws, "Tasks Remaining by Person",
               f"'Wedding Checklist'!${letter_cat}${person_start}:${letter_cat}${person_end}",
               f"'Wedding Checklist'!${letter_val}${person_start}:${letter_val}${person_end}",
               f"J22", width=12, height=8)

    return {
        "first_data_row": first_data_row,
        "last_data_row": last_data_row,
        "section_ranges": section_ranges,
        "total_items": total_items,
    }
