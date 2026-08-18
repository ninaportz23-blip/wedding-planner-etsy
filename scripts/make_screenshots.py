# -*- coding: utf-8 -*-
"""Builds a trimmed copy of the workbook with just the sheets needed for
screenshot mockups, sets print areas, converts to PDF, then rasterizes
each target sheet's first page to PNG for the Etsy listing."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from openpyxl import load_workbook
from openpyxl.worksheet.page import PageMargins

SRC = os.path.join(os.path.dirname(__file__), "..", "dist", "Wedding-Planner-All-In-One.xlsx")
TMP = os.path.join(os.path.dirname(__file__), "..", "dist", "_screenshot_src.xlsx")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "qa_screens")
os.makedirs(OUT_DIR, exist_ok=True)

TARGETS = [
    ("Dashboard", "A1:N67"),
    ("Wedding Checklist", "A1:R42"),
    ("Wedding Budget", "A1:U42"),
    ("Guest List", "A1:S26"),
    ("Reception Seating Plan", "A1:N49"),
]
DEPS = ["Get Started", "Vendor Selection", "Wedding Party", "Gifts and Thank You"]

wb = load_workbook(SRC)
keep = [t for t, _ in TARGETS] + DEPS
for name in list(wb.sheetnames):
    if name not in keep:
        del wb[name]

# reorder: targets first, then deps
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
print("Saved trimmed workbook:", TMP)
