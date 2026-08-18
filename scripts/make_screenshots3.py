# -*- coding: utf-8 -*-
"""Renders the Smart Calendar tab screenshot for the marketing images."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from openpyxl import load_workbook
from openpyxl.worksheet.page import PageMargins

SRC = os.path.join(os.path.dirname(__file__), "..", "dist", "Wedding-Planner-All-In-One.xlsx")
TMP = os.path.join(os.path.dirname(__file__), "..", "dist", "_screenshot_src3.xlsx")

TARGETS = [("Smart Calendar", "A1:H29")]
DEPS = ["Get Started", "Wedding Checklist", "Wedding Budget", "Vendor Selection", "Lists"]

wb = load_workbook(SRC)
keep = [t for t, _ in TARGETS] + DEPS
for name in list(wb.sheetnames):
    if name not in keep:
        del wb[name]
order = [t for t, _ in TARGETS] + DEPS
wb._sheets.sort(key=lambda s: order.index(s.title))

for name, area in TARGETS:
    ws = wb[name]
    ws.print_area = area
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins = PageMargins(left=0.2, right=0.2, top=0.2, bottom=0.2, header=0, footer=0)

for name in DEPS:
    ws = wb[name]
    ws.print_area = "A1:A1"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True

wb.active = 0
wb.save(TMP)
print("Saved:", TMP)
