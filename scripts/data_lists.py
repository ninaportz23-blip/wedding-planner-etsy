# -*- coding: utf-8 -*-
"""Static reference data: dropdown lists and the 850+ item wedding checklist."""

ASSIGNED_TO = ["Bride", "Groom", "Both", "Wedding Planner", "Maid of Honor", "Best Man", "Parent", "Other"]
PRIORITY = ["Low", "Medium", "High", "Urgent"]
YES_NO = ["Yes", "No"]
YES_NO_AWAITED = ["Yes", "No", "Awaited"]
GUEST_TAG = ["Bride", "Groom", "Both"]
GUEST_TYPE = ["Family", "Friend", "Colleague", "Neighbor", "Other"]
MEAL_PREF = ["Chicken", "Beef", "Fish", "Vegetarian", "Vegan", "Kids Meal", "No Preference"]
VENDOR_CATEGORY = ["Venue", "Catering", "Photography", "Videography", "Florist", "DJ/Band",
                    "Officiant", "Rentals", "Decor", "Hair & Makeup", "Transportation", "Cake",
                    "Stationery", "Favors", "Lighting"]
FINAL_YN = ["Yes", "No"]
ATTIRE_STATUS = ["Not Started", "Ordered", "Received", "Fitting Scheduled", "Alterations Needed", "Ready"]
WEDDING_PARTY_ROLE = ["Maid of Honor", "Bridesmaid", "Best Man", "Groomsman", "Flower Girl", "Ring Bearer",
                       "Usher", "Officiant", "Parent of Bride", "Parent of Groom", "Other"]
GIFT_STATUS = ["Need to Buy", "Purchased"]
DECOR_LOCATION = ["Ceremony", "Cocktail Hour", "Reception Entrance", "Reception Tables", "Head Table",
                   "Cake Table", "Photo Booth", "Restrooms", "Other"]
DECOR_STATUS = ["Confirmed", "To Be Decided", "Cancelled"]
BUY_RENT = ["Buy", "Rent"]
FLORAL_STATUS = ["Not Started", "Ordered", "Confirmed", "Delivered"]
ATTIRE_CATEGORY = ["Attire", "Hair", "Makeup", "Shoes & Accessories", "Nails"]
ACCOMMODATION_LIST = ["Grand Hotel", "Riverside Inn", "Airport Marriott", "Boutique B and B", "Guest House"]
STATIONERY_CATEGORY = ["Before the Wedding", "Wedding Day", "After the Wedding"]
DESIGN_STATUS = ["Not Started", "In Progress", "Completed"]
PRINT_STATUS = ["Not Needed", "Not Ordered", "Ordered", "Printed"]
PAYMENT_STATUS = ["Not Due", "Due Soon", "Paid", "Overdue"]
PAYMENT_TYPE = ["Deposit", "Progress Payment", "Final Payment", "Gratuity"]
TRUE_FALSE = [True, False]
BACHELOR_TYPE = ["Party", "Trip"]
CURRENCY_LIST = ["USD", "EUR", "GBP", "CAD", "AUD", "MXN", "JPY"]
BOOKING_STATUS = ["Researching", "Contacted", "Booked", "Paid", "Cancelled"]

MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August",
               "September", "October", "November", "December"]

# ---------------------------------------------------------------------------
# CHECKLIST DATA: 12 timeframe sections, 850+ pre-filled real wedding tasks
# ---------------------------------------------------------------------------

VENDOR_CATS_FOR_TASKS = ["Venue", "Caterer", "Photographer", "Videographer", "Florist",
                          "DJ or Band", "Officiant", "Rental Company", "Decor Stylist",
                          "Hair Stylist", "Makeup Artist", "Transportation Company", "Cake Baker",
                          "Stationer", "Favor Supplier", "Lighting Company", "Wedding Planner",
                          "Photo Booth Company"]

def _vendor_research_tasks():
    out = []
    for v in VENDOR_CATS_FOR_TASKS:
        out.append(f"Research {v} options in your area and read reviews")
    return out

def _vendor_shortlist_tasks():
    out = []
    for v in VENDOR_CATS_FOR_TASKS:
        out.append(f"Request quotes from at least 3 {v} candidates")
        out.append(f"Schedule consultations or tastings with shortlisted {v} options")
    return out

def _vendor_booking_tasks():
    out = []
    for v in VENDOR_CATS_FOR_TASKS:
        out.append(f"Compare {v} packages, pricing, and availability")
        out.append(f"Book and sign contract with chosen {v}")
        out.append(f"Pay deposit to secure {v}")
    return out

def _vendor_confirm_tasks():
    out = []
    for v in VENDOR_CATS_FOR_TASKS:
        out.append(f"Confirm final details and timeline with {v}")
    return out

def _vendor_final_payment_tasks():
    out = []
    for v in VENDOR_CATS_FOR_TASKS:
        out.append(f"Pay final balance to {v}")
    return out

def _vendor_admin_tasks():
    out = []
    for v in VENDOR_CATS_FOR_TASKS:
        out.append(f"Add {v} contract to the wedding vendor binder")
        out.append(f"Save {v} contact info to the shared wedding phone list")
    return out

def _vendor_insurance_tasks():
    out = []
    for v in ["Caterer", "DJ or Band", "Rental Company", "Photo Booth Company", "Lighting Company", "Transportation Company"]:
        out.append(f"Confirm {v} has certificate of insurance if required by venue")
    return out

def _vendor_thankyou_tasks():
    out = []
    for v in VENDOR_CATS_FOR_TASKS:
        out.append(f"Send a thank you note to {v} after the wedding")
    return out

SECTION_12_PLUS = [
    "Announce your engagement to family and close friends",
    "Set a realistic wedding budget with your partner",
    "Decide who is contributing to the budget and how much",
    "Choose your wedding date (or a short list of dates)",
    "Decide on wedding size (intimate, medium, large)",
    "Create a rough guest list headcount estimate",
    "Discuss and choose a wedding vision, theme, and color palette",
    "Choose the season and general location for the wedding",
    "Decide whether to hire a wedding planner",
    "Interview and hire a wedding planner if desired",
    "Start a shared wedding planning binder or spreadsheet",
    "Create a private wedding email address for vendor communication",
    "Set up a wedding website",
    "Choose a wedding hashtag",
    "Draft the full guest list with addresses",
    "Consider a guest list cap and stick to it",
    "Research ceremony and reception venue options",
    "Tour at least 5 potential venues",
    "Ask venues about capacity, availability, and included services",
    "Compare venue costs and what's included in each package",
    "Book ceremony venue and sign contract",
    "Book reception venue and sign contract",
    "Pay venue deposit",
    "Consider hiring an officiant or asking a friend to get ordained",
    "Start researching photographers and browsing portfolios",
    "Start researching videographers and browsing reels",
    "Start researching wedding planners or day-of coordinators",
    "Start a Pinterest or moodboard for overall wedding style",
    "Decide on a rough guest count range for catering purposes",
    "Research average wedding costs in your area for budgeting",
    "Open a dedicated wedding savings account",
    "Discuss honeymoon budget separately from wedding budget",
    "Ask parents or family about their wishes to be involved",
    "Decide on wedding party size and who to ask",
    "Draft a wedding party wish list (who you want to ask)",
    "Research marriage license requirements in your state",
    "Check passport expiration dates if honeymooning abroad",
    "Purchase wedding insurance if desired",
    "Create a Pinterest board for dress and suit inspiration",
    "Research caterers and schedule tastings",
    "Book caterer and sign contract",
    "Research florists and their portfolios",
    "Research DJ and live band options",
    "Attend a bridal show for vendor inspiration",
    "Discuss and decide on wedding style: formal, casual, destination",
    "Decide on ceremony type: religious, civil, or symbolic",
    "Research legal requirements for a destination wedding, if applicable",
    "Start a wedding day timeline outline",
    "Choose a wedding party gift budget",
    "Set up a wedding budget spreadsheet by category",
    "Research average vendor deposit amounts to plan cash flow",
] + _vendor_research_tasks()

SECTION_10_12 = [
    "Finalize the guest list headcount for venue and catering",
    "Book photographer and sign contract",
    "Pay photographer deposit",
    "Book videographer and sign contract",
    "Pay videographer deposit",
    "Book florist and sign contract",
    "Book DJ or band and sign contract",
    "Book officiant and confirm ceremony requirements",
    "Start wedding dress shopping",
    "Order the wedding dress",
    "Start suit or tuxedo shopping",
    "Order the groom's attire",
    "Choose bridesmaid dress style and color",
    "Order bridesmaid dresses",
    "Choose groomsmen attire style",
    "Order groomsmen attire",
    "Create your wedding gift registry",
    "Register at 2 to 3 stores for variety",
    "Book a room block for out of town guests",
    "Research and book wedding rentals (tables, chairs, linens)",
    "Book transportation for the wedding day",
    "Book hair stylist and makeup artist",
    "Schedule a hair and makeup trial",
    "Research and book a cake baker",
    "Schedule a cake tasting",
    "Research honeymoon destinations and options",
    "Set honeymoon budget and start saving",
    "Book honeymoon flights if pricing is favorable",
    "Start planning the engagement party, if hosting one",
    "Choose save the date design",
    "Order or design save the dates",
    "Collect mailing addresses for save the dates",
    "Mail save the dates to guests",
    "Book rehearsal dinner venue",
    "Research and book stationery designer",
    "Discuss and finalize the guest list with both families",
    "Create a wedding party group chat",
    "Officially ask wedding party members to participate",
    "Discuss wedding party responsibilities and expectations",
    "Choose bridesmaid proposal gifts, if planned",
    "Book a wedding insurance policy if not done already",
    "Reserve any specialty lighting or decor rental company",
    "Research and shortlist favor suppliers",
    "Research and shortlist photo booth companies",
    "Start researching ceremony musicians if separate from DJ",
    "Confirm venue includes tables, chairs, and linens or plan rentals",
    "Discuss seating chart approach with partner",
    "Draft a first version of the day-of timeline",
    "Confirm officiant meeting schedule for pre-marital counseling",
    "Research local marriage license office hours and requirements",
] + _vendor_shortlist_tasks()

SECTION_8_10 = [
    "Order bridesmaid dresses if not already ordered",
    "Finalize groomsmen attire orders",
    "Choose and order flower girl and ring bearer attire",
    "Schedule first dress fitting",
    "Book hair and makeup trial date",
    "Finalize ceremony readings and rituals with officiant",
    "Choose ceremony music selections",
    "Choose cocktail hour music selections",
    "Choose reception music selections",
    "Draft a do-not-play list for the DJ",
    "Plan the menu with your caterer",
    "Choose bar and beverage package",
    "Decide on wedding cake flavors and design",
    "Finalize cake order details",
    "Start planning wedding favors",
    "Order or make wedding favors",
    "Plan welcome bags for out of town guests",
    "Research and book a calligrapher for invitations, if desired",
    "Design or order wedding invitations",
    "Proofread invitation wording carefully",
    "Order invitation envelopes and inserts",
    "Purchase postage for invitations and RSVP cards",
    "Finalize the wedding party attire and accessories",
    "Shop for wedding rings",
    "Purchase wedding bands",
    "Schedule ring resizing if needed",
    "Book hotel rooms for wedding party, if applicable",
    "Plan rehearsal dinner menu and guest list",
    "Send rehearsal dinner invitations",
    "Finalize honeymoon itinerary",
    "Book honeymoon accommodations",
    "Purchase travel insurance for honeymoon",
    "Start dress alterations",
    "Choose bridal accessories: veil, jewelry, shoes",
    "Purchase bridal accessories",
    "Choose groom's accessories: tie, cufflinks, shoes",
    "Purchase groom's accessories",
    "Plan the ceremony processional order",
    "Discuss unity ritual for ceremony, if desired",
    "Book florist final consultation date",
    "Confirm floral order details: bouquets, centerpieces, boutonnieres",
    "Research and book transportation for wedding party",
    "Plan guest transportation logistics if needed",
    "Confirm decor rental order with vendor",
    "Research photo and video shot list ideas",
    "Draft photo and video shot list",
    "Plan engagement photos, if not already taken",
    "Schedule engagement photo session",
    "Choose thank you card design for gifts",
    "Set up a system for tracking gifts received",
] + _vendor_booking_tasks()

SECTION_6_8 = [
    "Finalize wedding invitation wording",
    "Address wedding invitation envelopes",
    "Mail wedding invitations (aim for 6 to 8 weeks before)",
    "Set an RSVP deadline on invitations",
    "Track RSVPs as they arrive in the guest list",
    "Follow up on wedding website RSVP settings",
    "Plan the bridal shower with maid of honor",
    "Send bridal shower invitations",
    "Plan the bachelorette party or trip",
    "Send bachelorette party invitations",
    "Plan the bachelor party or trip",
    "Send bachelor party invitations",
    "Confirm wedding party attire measurements are submitted",
    "Attend second dress fitting",
    "Purchase undergarments and shapewear for wedding attire",
    "Confirm groomsmen attire measurements are submitted",
    "Plan the rehearsal dinner details and timeline",
    "Finalize rehearsal dinner menu",
    "Order rehearsal dinner invitations if separate from wedding",
    "Meet with officiant to finalize ceremony script",
    "Write personal vows, if applicable",
    "Choose ceremony readers and inform them",
    "Confirm ceremony musicians and song list",
    "Confirm reception band or DJ song list and timeline",
    "Finalize seating chart draft using RSVP data",
    "Plan kids' table or activities, if applicable",
    "Order table numbers and place cards",
    "Order wedding programs",
    "Choose and order guest book",
    "Choose and order card box or gift table sign",
    "Plan welcome sign and other wedding day signage",
    "Order signage for reception (bar menu, seating chart, welcome sign)",
    "Confirm final decor rental order and delivery details",
    "Confirm lighting plan with vendor",
    "Confirm florist delivery and setup timeline",
    "Plan the getting-ready timeline for hair and makeup",
    "Confirm hair and makeup trial results and finalize looks",
    "Purchase gifts for parents",
    "Purchase gifts for wedding party",
    "Wrap wedding party and parent gifts",
    "Confirm honeymoon packing list start",
    "Renew or apply for passport if needed for honeymoon",
    "Confirm travel documents for honeymoon",
    "Schedule a final walkthrough at ceremony venue",
    "Schedule a final walkthrough at reception venue",
    "Draft the detailed wedding day timeline",
    "Share draft timeline with wedding party and vendors for feedback",
    "Confirm transportation pickup times and locations",
    "Order or confirm cake topper and cake serving set",
    "Choose and purchase toasting flutes and cake cutting set",
    "Book a post-wedding brunch venue, if hosting one",
] + _vendor_confirm_tasks()

SECTION_4_6 = [
    "Apply for marriage license (check your state's timing window)",
    "Confirm name change paperwork plan, if applicable",
    "Finalize guest count with venue and caterer",
    "Finalize guest count with rental company",
    "Confirm final headcount for rehearsal dinner",
    "Order additional wedding favors if needed based on headcount",
    "Confirm final floral order based on headcount",
    "Schedule final dress fitting",
    "Schedule final suit or tuxedo fitting",
    "Break in wedding day shoes",
    "Purchase or rent wedding day emergency kit supplies",
    "Confirm final payment schedule for all vendors",
    "Create a vendor payment tracking log with due dates",
    "Confirm rehearsal dinner headcount and menu",
    "Send rehearsal details to wedding party",
    "Finalize seating chart based on final RSVPs",
    "Print seating chart and table assignment cards",
    "Confirm menu choices are collected from guests, if offered",
    "Update caterer with final meal preference counts",
    "Confirm cake flavors and final design with baker",
    "Schedule cake delivery time with baker",
    "Purchase or confirm wedding day accessories: garter, cufflinks, etc.",
    "Finalize the wedding day hair and makeup schedule",
    "Confirm hotel room block final guest count",
    "Send hotel information to out of town guests",
    "Plan welcome bags contents and assembly",
    "Assemble welcome bags for out of town guests",
    "Confirm honeymoon reservations and itinerary details",
    "Purchase honeymoon outfits and essentials",
    "Confirm travel insurance is active",
    "Draft thank you notes for early gifts received",
    "Mail thank you notes for gifts received so far",
    "Confirm ceremony rehearsal date and time with officiant",
    "Confirm ceremony rehearsal date and time with wedding party",
    "Finalize processional and recessional order",
    "Confirm readers and their reading selections",
    "Print ceremony programs",
    "Confirm final floral delivery and setup time",
    "Confirm final lighting and decor setup time",
    "Confirm DJ or band final song list and announcements",
    "Provide DJ or band with a do-not-play list",
    "Confirm photographer and videographer shot list and timeline",
    "Share final day-of timeline with all vendors",
    "Share final day-of timeline with wedding party",
    "Confirm transportation schedule with driver or company",
    "Purchase tip envelopes for vendors",
    "Calculate and set aside vendor gratuities",
    "Confirm final headcount with bar service",
    "Order any additional signage needed for the day",
    "Confirm officiant has the marriage license details",
] + _vendor_final_payment_tasks()

SECTION_2_4 = [
    "Finalize and confirm seating chart",
    "Print place cards and table numbers",
    "Confirm final RSVP count is entered in guest list",
    "Follow up with guests who have not yet RSVPed",
    "Send final headcount to caterer",
    "Send final headcount to venue",
    "Send final headcount to rental company",
    "Confirm final floral order and delivery window",
    "Confirm final cake order and delivery window",
    "Confirm final transportation details",
    "Pick up or confirm delivery of wedding rings",
    "Confirm final dress fitting appointment",
    "Confirm final suit or tuxedo fitting appointment",
    "Break in wedding shoes further if needed",
    "Prepare emergency kit for wedding day",
    "Prepare a day-of essentials bag",
    "Confirm hotel accommodations for wedding party",
    "Confirm accommodations for out of town family",
    "Distribute welcome bags to hotel front desk, if applicable",
    "Finalize the rehearsal dinner run of show",
    "Confirm rehearsal dinner toasts and speakers",
    "Draft wedding day emergency contact sheet",
    "Share emergency contact sheet with wedding party and vendors",
    "Confirm final payment amounts due on wedding day",
    "Prepare vendor tip envelopes with names and amounts",
    "Assign a point person to distribute vendor tips on the day",
    "Confirm officiant will bring the marriage license paperwork",
    "Pack for the honeymoon",
    "Confirm honeymoon travel check-in details",
    "Arrange pet care or plant care during the honeymoon",
    "Arrange mail hold or house sitting during the honeymoon",
    "Confirm final guest meal counts by meal type",
    "Confirm final bar package and signature cocktails",
    "Print or confirm menu cards for reception tables",
    "Confirm final music timeline: processional, first dance, last song",
    "Practice father-daughter or parent dances if planned",
    "Confirm speeches and toasts order with speakers",
    "Ask a friend to manage gifts and cards during reception",
    "Confirm guest book and pen are ready",
    "Confirm card box or gift table setup plan",
    "Confirm final headcount for any kids' activities or table",
    "Reconfirm all vendor arrival times",
    "Draft a setup and breakdown responsibility list",
    "Confirm who is responsible for returning rentals",
    "Confirm getting-ready location logistics for both partners",
    "Plan first look timing and location, if doing one",
    "Finalize photo and video shot list with specific family groupings",
    "Share family formal photo list with photographer",
    "Confirm weather backup plan for outdoor elements",
    "Reconfirm final numbers with all remaining vendors",
]

SECTION_1_MONTH = [
    "Finalize final guest count and share with all vendors",
    "Confirm final seating chart is complete and printed",
    "Pick up wedding dress from final fitting",
    "Pick up suit or tuxedo from final fitting",
    "Confirm all wedding party attire has arrived and fits",
    "Pack the emergency kit fully",
    "Confirm rehearsal dinner final details",
    "Send rehearsal itinerary to wedding party",
    "Confirm officiant has final ceremony script",
    "Reconfirm hair and makeup schedule and arrival times",
    "Reconfirm photographer and videographer arrival times",
    "Reconfirm florist delivery and setup time",
    "Reconfirm cake delivery time and location",
    "Reconfirm DJ or band arrival and setup time",
    "Reconfirm transportation pickup schedule",
    "Prepare final payments and tip envelopes",
    "Confirm marriage license appointment or requirements are met",
    "Pick up marriage license within your state's valid window",
    "Confirm wedding rings are ready and in a safe place",
    "Confirm honeymoon documents are printed and packed",
    "Confirm out of town guest itinerary and welcome bags are ready",
    "Finalize and print the wedding day timeline for all parties",
    "Distribute the day-of timeline to wedding party and family",
    "Distribute the day-of timeline to all vendors",
    "Confirm setup and breakdown crew responsibilities",
    "Assign a day-of point of contact for vendors",
    "Reconfirm final bar and catering headcounts",
    "Confirm menu cards and table signage are printed",
    "Confirm guest book, pens, and card box are packed",
    "Confirm ceremony programs are printed and ready",
    "Confirm favors are packed and ready for setup",
    "Confirm welcome sign and other decor signage are ready",
    "Have a final fitting for both partners' full outfits together",
    "Schedule a mani-pedi or spa day before the wedding",
    "Confirm rehearsal time with the venue",
    "Practice ceremony walk-through at the venue",
    "Confirm final floor plan with venue and rental company",
    "Reconfirm weather backup plan for outdoor elements",
    "Prepare a playlist for getting ready, if desired",
    "Draft toast notes if giving a speech",
    "Confirm speeches order with best man and maid of honor",
    "Reconfirm accommodations for the wedding night",
    "Pack an overnight bag for the wedding night",
]

SECTION_2_WEEKS = [
    "Confirm final vendor payments are prepared",
    "Pay any outstanding vendor deposits",
    "Reconfirm final guest count with caterer",
    "Reconfirm final guest count with venue",
    "Reconfirm final guest count with bar service",
    "Print extra copies of the seating chart",
    "Print extra copies of the day-of timeline",
    "Confirm rehearsal dinner headcount with restaurant or caterer",
    "Confirm final fittings are complete for the whole wedding party",
    "Pick up any remaining wedding attire",
    "Confirm all wedding rings are accounted for",
    "Confirm marriage license is signed and ready, if already obtained",
    "Reconfirm hotel room blocks are finalized",
    "Send final logistics email to out of town guests",
    "Confirm transportation company has final pickup addresses",
    "Confirm florist has final delivery address and time",
    "Confirm cake baker has final delivery address and time",
    "Confirm photographer has the final shot list",
    "Confirm videographer has the final shot list",
    "Reconfirm DJ or band has the final song list",
    "Give DJ or band final pronunciation guide for names",
    "Pack the wedding day emergency kit in the car or with a helper",
    "Assign someone to handle gifts and cards after the reception",
    "Assign someone to handle the getting-ready space cleanup",
    "Confirm weather forecast and backup plans",
    "Reconfirm honeymoon flight and hotel details",
    "Print honeymoon travel documents",
    "Notify credit card companies of honeymoon travel dates",
    "Arrange currency exchange for honeymoon destination, if needed",
    "Confirm pet or house sitting arrangements",
    "Have final trial run of wedding day hairstyle",
    "Have final trial run of wedding day makeup",
    "Confirm all thank you cards from early gifts are mailed",
    "Prepare a list of vendor names and arrival times for the coordinator",
    "Confirm final walk-through with venue coordinator",
    "Reconfirm rehearsal time and location with officiant",
]

SECTION_1_WEEK = [
    "Confirm final numbers one last time with all vendors",
    "Pick up wedding rings if not already done",
    "Confirm bridesmaids and groomsmen have all final attire pieces",
    "Pack for the wedding day: dress, suit, accessories, shoes",
    "Pack the honeymoon suitcase",
    "Confirm rehearsal dinner reservation and headcount",
    "Attend the rehearsal at the ceremony venue",
    "Attend the rehearsal dinner",
    "Give toasts or speeches practice one more time",
    "Distribute final tip envelopes to a trusted point person",
    "Confirm final payment checks are written and ready",
    "Drop off or confirm delivery of welcome bags to hotel",
    "Confirm guest book, cards box, and signage are packed",
    "Confirm getting ready timeline with hair and makeup artists",
    "Confirm getting ready location is stocked with snacks and drinks",
    "Get a manicure and pedicure",
    "Pick up dry cleaning for wedding attire",
    "Confirm someone is assigned to bring the marriage license to the ceremony",
    "Reconfirm transportation pickup times with driver",
    "Charge phone and camera batteries for the week",
    "Set out an outfit for the rehearsal dinner",
    "Relax and spend quality time with close family and friends",
    "Confirm the emergency kit is packed and easy to find",
    "Do a final venue walk-through with the coordinator",
    "Confirm florist delivery window one final time",
]

SECTION_2_DAYS = [
    "Confirm all final payments and tips are ready in labeled envelopes",
    "Confirm all wedding party members know their arrival times",
    "Pack the car or hand off the emergency kit to a helper",
    "Do a final check of all attire, shoes, and accessories",
    "Confirm rehearsal dinner final headcount with the venue",
    "Get plenty of rest",
    "Drink plenty of water and eat regular meals",
    "Confirm hair and makeup artist arrival times one more time",
    "Confirm photographer and videographer arrival times one more time",
    "Confirm the getting ready space is set up and stocked",
    "Do a final manicure touch-up if needed",
    "Set out the wedding day outfit and accessories",
    "Confirm the officiant has the signed marriage license paperwork ready",
    "Confirm a family member or friend has the vendor tip envelopes",
    "Text the wedding party the final timeline one more time",
    "Confirm the reception venue setup crew arrival time",
]

SECTION_1_DAY = [
    "Attend the ceremony rehearsal",
    "Attend the rehearsal dinner",
    "Give and receive wedding party gifts, if not already done",
    "Confirm the getting ready timeline for the morning",
    "Set an alarm and go to bed early",
    "Lay out the wedding dress, suit, and all accessories",
    "Pack the overnight bag for the wedding night",
    "Confirm final weather forecast and backup plan status",
    "Confirm all vendors are still on schedule for tomorrow",
    "Give the emergency kit to the designated helper",
    "Relax, breathe, and enjoy the moment with loved ones",
]

SECTION_LEGAL = [
    "Research marriage license requirements in your state or country",
    "Confirm required identification documents for the license",
    "Confirm waiting period between application and ceremony, if any",
    "Schedule an appointment at the county clerk's office, if required",
    "Apply for the marriage license within the valid time window",
    "Bring two witnesses to sign, if required by your state",
    "Confirm officiant is legally authorized to perform the ceremony",
    "Confirm officiant's registration is filed with the correct county, if required",
    "Sign the marriage license with officiant and witnesses after the ceremony",
    "Confirm who is responsible for filing the signed license with the county",
    "File the signed marriage license with the appropriate government office",
    "Order certified copies of the marriage certificate",
    "Begin the legal name change process, if applicable",
    "Update Social Security card with new name, if applicable",
    "Update driver's license with new name, if applicable",
    "Update passport with new name, if applicable",
    "Update bank accounts and credit cards with new name, if applicable",
    "Update employer records and payroll with new name, if applicable",
    "Update insurance policies with new name and marital status",
    "Update beneficiary designations on accounts and policies",
    "Consider updating or creating a will after marriage",
    "Review health insurance options for adding a spouse",
    "Review auto insurance for potential multi-policy discounts",
    "Update voter registration with new name or address, if applicable",
    "Update your lease or mortgage documents, if applicable",
    "Confirm prenuptial agreement is signed and filed, if applicable",
    "Store the marriage certificate in a safe, accessible place",
]

EXTRA_12_PLUS = [
    "Discuss blended family or step-parent involvement, if applicable",
    "Decide on a guest list policy for plus-ones",
    "Decide on a policy for children at the wedding",
    "Research whether your venue requires liability insurance",
    "Set up a wedding planning shared calendar for both partners",
    "Discuss and agree on non-negotiable wedding priorities",
    "Discuss and agree on where to cut costs if needed",
    "Research off-season or weekday dates for potential savings",
    "Ask trusted friends for vendor recommendations",
    "Join online wedding planning communities for advice",
    "Research local wedding rules and permits for outdoor venues",
    "Discuss blended religious or cultural ceremony traditions to include",
    "Create a shared document of must-have wedding traditions",
    "Research live-streaming options for guests who cannot attend",
    "Discuss accessibility needs for guests with mobility limitations",
]
SECTION_12_PLUS += EXTRA_12_PLUS

EXTRA_10_12 = [
    "Confirm venue's rain plan and tent options, if outdoors",
    "Ask venue about noise curfews and vendor load-in times",
    "Confirm parking availability and valet options with venue",
    "Discuss wedding day insurance coverage details",
    "Choose a bridal salon and schedule an appointment",
    "Set a budget for wedding attire and accessories",
    "Research and choose ring insurance options",
    "Discuss honeymoon travel vaccinations or health requirements",
    "Confirm which family heirlooms will be worn or used",
    "Plan the engagement party guest list, if hosting one",
    "Send engagement party invitations, if hosting one",
    "Research local marriage license waiting periods",
]
SECTION_10_12 += EXTRA_10_12

EXTRA_8_10 = [
    "Confirm bridesmaid dress sizing chart and order deadlines",
    "Confirm groomsmen rental sizing appointments",
    "Choose flower girl basket and ring bearer pillow",
    "Discuss unplugged ceremony policy, if desired",
    "Research local rules for releasing balloons, sparklers, or confetti",
    "Confirm venue's vendor insurance requirements list",
    "Choose a wedding day beauty routine and skincare plan",
    "Schedule any teeth whitening or spa treatments",
]
SECTION_8_10 += EXTRA_8_10

EXTRA_6_8 = [
    "Confirm final RSVP tracking method with wedding website",
    "Set up a physical mailbox check routine for RSVP cards",
    "Confirm children's meal options with caterer",
    "Confirm dietary restriction options with caterer",
    "Discuss and finalize wedding favor packaging",
    "Confirm menu tasting feedback is shared with caterer",
    "Choose and order aisle runner or ceremony decor accents",
    "Confirm ceremony seating arrangement for immediate family",
]
SECTION_6_8 += EXTRA_6_8

EXTRA_4_6 = [
    "Confirm name change document checklist is ready post-wedding",
    "Confirm final headcount adjustments are sent to florist",
    "Reconfirm honeymoon packing list categories",
    "Confirm any dietary needs are communicated to rehearsal dinner venue",
    "Confirm final guest list is shared with the officiant for programs",
    "Draft the wedding party processional walking order diagram",
]
SECTION_4_6 += EXTRA_4_6

EXTRA_2_4 = [
    "Confirm final table layout diagram with venue coordinator",
    "Confirm final linens and chair styles with rental company",
    "Confirm final AV or microphone needs for speeches",
    "Confirm final headcount for any late-night snack service",
    "Confirm umbrella or fan favors for outdoor guests, if needed",
    "Confirm sunset time for outdoor photo planning",
    "Reconfirm all guest dietary restrictions are logged",
    "Confirm final guest list is shared with security or venue staff, if required",
]
SECTION_2_4 += EXTRA_2_4

EXTRA_1_MONTH = [
    "Confirm final fitting alterations are complete for bride and groom",
    "Confirm final numbers for any shuttle service pickups",
    "Reconfirm final table assignments with any last minute RSVP changes",
    "Confirm rehearsal dinner final menu selections",
    "Confirm final approval of all printed signage proofs",
    "Reconfirm the emergency kit contents checklist is complete",
]
SECTION_1_MONTH += EXTRA_1_MONTH

EXTRA_2_WEEKS = [
    "Confirm final approval of the printed wedding programs",
    "Confirm final approval of the printed menu cards",
    "Reconfirm final vendor arrival order with the coordinator",
    "Confirm a backup plan for key vendor no-shows",
    "Reconfirm final guest count changes are logged in guest list",
]
SECTION_2_WEEKS += EXTRA_2_WEEKS

EXTRA_1_WEEK = [
    "Confirm final rehearsal dinner seating plan",
    "Confirm who will drive the getaway car, if applicable",
    "Confirm final playlist edits with the DJ or band",
    "Reconfirm final headcount with the caterer one last time",
]
SECTION_1_WEEK += EXTRA_1_WEEK

EXTRA_2_DAYS = [
    "Reconfirm final rehearsal time with all attendees",
    "Confirm final weather backup decision with the venue",
    "Delegate someone to collect any rented items after the wedding",
]
SECTION_2_DAYS += EXTRA_2_DAYS

EXTRA_1_DAY = [
    "Confirm final morning-of schedule with hair and makeup team",
    "Confirm getaway transportation is ready for the next day",
]
SECTION_1_DAY += EXTRA_1_DAY

EXTRA_LEGAL = [
    "Confirm notarization requirements for any prenuptial documents",
    "Research whether a marriage license translation is needed for destination weddings",
    "Confirm officiant's credentials meet your state's legal requirements",
    "Store copies of the marriage certificate in a fireproof safe",
    "Update immigration or visa documentation, if applicable",
]
SECTION_LEGAL += EXTRA_LEGAL

SECTION_2_4 += _vendor_admin_tasks()
SECTION_1_MONTH += _vendor_insurance_tasks()
SECTION_LEGAL += ["Confirm final marriage certificate copies are ordered for name change use"]
SECTION_LEGAL += _vendor_thankyou_tasks()

def _vendor_generic_tasks(verb_template):
    return [verb_template.format(v=v) for v in VENDOR_CATS_FOR_TASKS]

SECTION_1_WEEK += _vendor_generic_tasks("Save {v} emergency contact number in the wedding day phone list")
SECTION_2_WEEKS += _vendor_generic_tasks("Confirm {v} has the correct venue load-in address and arrival time")
SECTION_4_6 += _vendor_generic_tasks("File {v} payment receipt in the wedding budget records")
SECTION_8_10 += _vendor_generic_tasks("Update the wedding budget spreadsheet after paying {v}")
SECTION_6_8 += _vendor_generic_tasks("Reconfirm {v} booking details in writing by email")

EXTRA_ROUND2 = {
    "SECTION_12_PLUS": [
        "Take engagement photos for save the dates and the wedding website",
        "Discuss whether to have a unity ceremony element",
        "Decide on wedding party attire budget responsibility",
    ],
    "SECTION_10_12": [
        "Confirm venue's alcohol service policy and licensing",
        "Confirm venue's vendor list restrictions, if any",
        "Discuss and choose ceremony seating style: traditional or mixed",
    ],
    "SECTION_8_10": [
        "Confirm final guest list address list is complete for invitations",
        "Choose invitation suite paper stock and printing method",
    ],
    "SECTION_6_8": [
        "Confirm RSVP card return address and postage are correct",
        "Confirm invitation mailing tracking method",
    ],
    "SECTION_2_4": [
        "Confirm final headcount for any late night food truck or snack vendor",
        "Confirm final wedding day parking signage plan",
    ],
    "SECTION_1_MONTH": [
        "Confirm final approval of all family formal photo groupings",
        "Confirm final headcount for shuttle or valet service",
    ],
}
SECTION_12_PLUS += EXTRA_ROUND2["SECTION_12_PLUS"]
SECTION_10_12 += EXTRA_ROUND2["SECTION_10_12"]
SECTION_8_10 += EXTRA_ROUND2["SECTION_8_10"]
SECTION_6_8 += EXTRA_ROUND2["SECTION_6_8"]
SECTION_2_4 += EXTRA_ROUND2["SECTION_2_4"]
SECTION_1_MONTH += EXTRA_ROUND2["SECTION_1_MONTH"]
CHECKLIST_SECTIONS = [
    ("12+ Months Before", SECTION_12_PLUS),
    ("10-12 Months Before", SECTION_10_12),
    ("8-10 Months Before", SECTION_8_10),
    ("6-8 Months Before", SECTION_6_8),
    ("4-6 Months Before", SECTION_4_6),
    ("2-4 Months Before", SECTION_2_4),
    ("1 Month Before", SECTION_1_MONTH),
    ("2 Weeks Before", SECTION_2_WEEKS),
    ("1 Week Before", SECTION_1_WEEK),
    ("2 Days Before", SECTION_2_DAYS),
    ("1 Day Before", SECTION_1_DAY),
    ("Legal Items", SECTION_LEGAL),
]

TOTAL_CHECKLIST_ITEMS = sum(len(v) for _, v in CHECKLIST_SECTIONS)

if __name__ == "__main__":
    for name, items in CHECKLIST_SECTIONS:
        print(name, len(items))
    print("TOTAL:", TOTAL_CHECKLIST_ITEMS)
