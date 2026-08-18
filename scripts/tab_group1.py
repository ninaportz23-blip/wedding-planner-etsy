# -*- coding: utf-8 -*-
"""Tabs 5-8: Wedding Itinerary, Wedding Activities, Music Planner, Packing List."""
from lib import *
from data_lists import ASSIGNED_TO

def _simple_table(ws, start_row, headers, color, rows_data, col_start=1):
    r = table_header(ws, start_row, col_start, headers, color)
    first = r
    for i, rowdata in enumerate(rows_data):
        for j, val in enumerate(rowdata):
            c = ws.cell(row=r, column=col_start + j, value=val)
            c.border = BORDER_ALL
            c.font = f_body()
            c.fill = fill(OFFWHITE if i % 2 else WHITE)
        r += 1
    return first, r - 1

def build_itinerary(wb):
    ws = new_sheet(wb, "Wedding Itinerary", tab_color=PEACH)
    row = title_banner(ws, "WEDDING DAY ITINERARY", PEACH, row=1, col_start=1, col_end=4, size=16)
    row += 1
    events = [
        ("8:00 AM", "Bridal Party Get Ready", "Hair and Makeup Team", "Bridal Suite"),
        ("9:30 AM", "Groom's Party Get Ready", "Groomsmen", "Groom's Suite"),
        ("11:00 AM", "First Look", "Photographer", "Garden"),
        ("11:30 AM", "Wedding Party Photos", "Photographer", "Garden"),
        ("12:30 PM", "Family Formal Photos", "Photographer", "Garden"),
        ("2:00 PM", "Guests Arrive", "Ushers", "Ceremony Site"),
        ("2:30 PM", "Ceremony", "Officiant", "Ceremony Site"),
        ("3:00 PM", "Cocktail Hour", "Catering Staff", "Terrace"),
        ("4:00 PM", "Grand Entrance", "DJ or Band", "Reception Hall"),
        ("4:15 PM", "First Dance", "DJ or Band", "Reception Hall"),
        ("4:30 PM", "Welcome Toast", "Best Man", "Reception Hall"),
        ("5:00 PM", "Dinner Service", "Catering Staff", "Reception Hall"),
        ("6:00 PM", "Toasts and Speeches", "Maid of Honor and Best Man", "Reception Hall"),
        ("6:30 PM", "Parent Dances", "DJ or Band", "Reception Hall"),
        ("7:00 PM", "Cake Cutting", "Caterer", "Reception Hall"),
        ("7:30 PM", "Open Dancing", "DJ or Band", "Reception Hall"),
        ("9:00 PM", "Bouquet and Garter Toss", "DJ or Band", "Reception Hall"),
        ("10:30 PM", "Last Dance", "DJ or Band", "Reception Hall"),
        ("10:45 PM", "Send Off", "Wedding Party", "Venue Exit"),
    ]
    fr, lr = _simple_table(ws, row, ["Time", "Event", "Person in Charge", "Location"], PEACH, events)
    freeze_header(ws, fr)
    set_col_widths(ws, {"A": 12, "B": 26, "C": 24, "D": 20})

def build_activities(wb):
    ws = new_sheet(wb, "Wedding Activities", tab_color=SAGE)
    row = title_banner(ws, "WEDDING ACTIVITIES", SAGE, row=1, col_start=1, col_end=4, size=16)
    row += 1
    ws.cell(row=row, column=1, value="PLANNED ACTIVITIES").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    ws.cell(row=row, column=1).fill = fill(SAGE)
    for cc in range(1, 5):
        ws.cell(row=row, column=cc).fill = fill(SAGE)
    row += 1
    activities = [
        ("3:00 PM", "Terrace", "Wedding Planner", "Photo booth open for guests"),
        ("3:15 PM", "Lawn", "Ushers", "Lawn games: cornhole and giant Jenga"),
        ("4:30 PM", "Reception Hall", "DJ", "Guest book table with instant camera"),
    ]
    fr, lr = _simple_table(ws, row, ["Time Slot", "Location", "Person in Charge", "Activity Description"], SAGE, activities)
    row = lr + 3

    ws.cell(row=row, column=1, value="50+ ACTIVITY IDEAS (REFERENCE LIST)").font = f_header()
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    ws.cell(row=row, column=1).fill = fill(CREAM)
    for cc in range(1, 5):
        ws.cell(row=row, column=cc).fill = fill(CREAM)
    row += 1
    ideas = [
        "Photo booth with props", "Guest book alternative: fingerprint tree", "Guest book alternative: polaroid wall",
        "Lawn games: cornhole", "Lawn games: giant Jenga", "Lawn games: ring toss", "Lawn games: bocce ball",
        "Photo booth with instant camera", "Custom cocktail bar", "Wine pull table", "S'mores bar",
        "Late night snack station", "Donut wall", "Candy bar", "Cigar rolling station", "Caricature artist",
        "Live painter", "Photo booth with backdrop", "Dance floor confetti drop", "Sparkler send off",
        "Fireworks display", "Karaoke station", "Slideshow of couple's photos", "Advice cards for the couple",
        "Wishing well card box", "Time capsule for guests to fill", "Coloring book table for kids",
        "Kids' activity table with crafts", "Photo scavenger hunt", "Trivia about the couple",
        "Custom playlist request cards", "Signature drink naming contest", "Bouquet toss alternative: anniversary dance",
        "Grand exit with bubbles", "Grand exit with ribbon wands", "Grand exit with glow sticks",
        "Lawn croquet", "Giant chess or checkers", "Bean bag toss", "Ladder golf", "Yard Yahtzee",
        "Photo booth with Polaroid guest book", "Wine or whiskey barrel signing ceremony",
        "Unity sand ceremony", "Handfasting ceremony", "Wine box time capsule ceremony",
        "Live band cocktail hour set", "String quartet ceremony music", "Fire pit lounge area",
        "Cigar and whiskey bar", "Popcorn bar", "Hot chocolate bar", "Mini dessert table",
        "Photo booth guest book combo", "Personalized koozies or favors station", "Henna or face painting",
        "Live caricature drawing", "Custom neon sign photo backdrop",
    ]
    for i, idea in enumerate(ideas):
        r = row + (i % 20)
        c = 1 + (i // 20)
        cell = ws.cell(row=r, column=c, value=f"- {idea}")
        cell.font = f_body(size=9)
        cell.alignment = LEFT
    freeze_header(ws, fr)
    set_col_widths(ws, {"A": 26, "B": 26, "C": 26, "D": 30})

def build_music(wb):
    ws = new_sheet(wb, "Music Planner", tab_color=POWDER)
    row = title_banner(ws, "MUSIC PLANNER", POWDER, row=1, col_start=1, col_end=4, size=16)
    row += 1
    ws.cell(row=row, column=1, value="Share this tab with your DJ or band. Fill in artist, notes, and duration for each moment.").font = f_body(italic=True, size=9)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
    row += 2
    sections = [
        ("Ceremony", POWDER, [("Prelude Music", "", "", ""), ("Processional", "", "", ""), ("Recessional", "", "", "")]),
        ("Cocktail Hour", SAGE, [("Background Playlist", "", "", "")]),
        ("Reception Entrance", CREAM, [("Grand Entrance Song", "", "", "")]),
        ("First Dance", BLUSH, [("First Dance Song", "", "", "")]),
        ("Parent Dances", LAVENDER, [("Father Daughter Dance", "", "", ""), ("Mother Son Dance", "", "", "")]),
        ("Party and Dancing", PEACH, [("Open Dance Playlist", "", "", ""), ("Do Not Play List", "", "", "")]),
        ("Last Song", POWDER, [("Last Song of the Night", "", "", "")]),
    ]
    for name, color, rows_data in sections:
        ws.cell(row=row, column=1, value=name.upper()).font = f_header()
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
        for cc in range(1, 5):
            ws.cell(row=row, column=cc).fill = fill(color)
        row += 1
        fr, lr = _simple_table(ws, row, ["Moment", "Artist", "Song / Version Notes", "Duration"], color, rows_data)
        row = lr + 2
    set_col_widths(ws, {"A": 24, "B": 20, "C": 30, "D": 12})
    freeze_header(ws, 1)

def build_packing(wb, dv_named):
    ws = new_sheet(wb, "Packing List", tab_color=CREAM)
    row = title_banner(ws, "PACKING LIST", CREAM, row=1, col_start=1, col_end=4, size=16)
    row += 1
    sections = {
        "Bride Suite": ["Wedding dress", "Veil", "Shoes", "Undergarments", "Jewelry", "Something old, new, borrowed, blue", "Emergency kit", "Robe"],
        "Groom Suite": ["Suit or tuxedo", "Shoes", "Tie or bow tie", "Cufflinks", "Belt", "Socks", "Watch"],
        "Ceremony": ["Vows", "Rings", "Marriage license", "Unity ceremony items", "Programs"],
        "Reception": ["Guest book and pen", "Card box", "Table numbers", "Place cards", "Cake serving set", "Toasting flutes"],
        "Emergency Kit": ["Safety pins", "Stain remover", "Sewing kit", "Bobby pins", "Blister pads", "Tissues", "Mints", "Pain reliever", "Snacks", "Phone charger"],
        "Honeymoon": ["Passport", "Travel documents", "Chargers", "Toiletries", "Outfits", "Swimwear", "Sunscreen"],
    }
    color_cycle = [BLUSH, POWDER, SAGE, CREAM, PEACH, LAVENDER]
    for i, (name, items) in enumerate(sections.items()):
        color = color_cycle[i % len(color_cycle)]
        ws.cell(row=row, column=1, value=name.upper()).font = f_header()
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=4)
        for cc in range(1, 5):
            ws.cell(row=row, column=cc).fill = fill(color)
        row += 1
        rows_data = [(item, False, "Both", "") for item in items]
        fr, lr = _simple_table(ws, row, ["Item", "Packed", "Assigned To", "Notes"], color, rows_data)
        # _simple_table returns fr = first DATA row, lr = last data row.
        for rr in range(fr, lr + 1):
            ws.cell(row=rr, column=2).alignment = CENTER
        add_checkbox_col(ws, f"B{fr}:B{lr}")
        dv_named(ws, f"C{fr}:C{lr}", "AssignedTo")
        ws.conditional_formatting.add(f"B{fr}:B{lr}", FormulaRule(formula=[f"B{fr}=ChkVal"], fill=fill(STATUS_GREEN)))
        row = lr + 2
    set_col_widths(ws, {"A": 26, "B": 10, "C": 14, "D": 26})
    freeze_header(ws, 1)
    return None
