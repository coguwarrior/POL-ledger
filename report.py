from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import sqlite3

DB = "pol.db"

POL_ITEMS = [
    "LSHFHSD", "Petrol", "SS_15W40", "SS_RR40", "HLP_46",
    "SP_150", "SF_57", "TwoT_Oil", "HP_90", "SP_68",
    "SS_320", "Freon_404A", "SE_55"
]

styles = getSampleStyleSheet()

cell = ParagraphStyle(
    "cell",
    fontSize=7,
    leading=8,
    wordWrap="CJK"
)

head = ParagraphStyle(
    "head",
    fontSize=7,
    leading=8,
    alignment=1,
    fontName="Helvetica-Bold"
)

# -------------------------------------------------
def fetch_rows(table, month, year):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(f"""
        SELECT date, details, {",".join(POL_ITEMS)}
        FROM {table}
        WHERE is_deleted=0
        AND strftime('%m', date)=?
        AND strftime('%Y', date)=?
        ORDER BY date
    """, (month, year))
    rows = cur.fetchall()
    con.close()
    return rows

# -------------------------------------------------
def totals(rows):
    t = [0.0]*len(POL_ITEMS)
    for r in rows:
        for i in range(len(POL_ITEMS)):
            if r[i+2]:
                t[i] += float(r[i+2])
    return t

# -------------------------------------------------
def build_table(data):
    col_widths = (
        [50, 200] +        # Date, Details
        [44]*len(POL_ITEMS)
    )

    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("FONT", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (2,1), (-1,-1), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    return table

# -------------------------------------------------
def monthly_report(month, year):
    filename = f"POL_Ledger_{month}_{year}.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4),
        leftMargin=15,
        rightMargin=15,
        topMargin=15,
        bottomMargin=15
    )

    elements = []

    # ================= RECEIPT =================
    rec = fetch_rows("receipt", month, year)
    rec_total = totals(rec)

    elements.append(Paragraph(
        f"<b>POL RECEIPT – {month}/{year}</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1, 4))

    header = (
        [Paragraph("Date", head), Paragraph("Details", head)]
        + [Paragraph(p, head) for p in POL_ITEMS]
    )

    data = [header]

    for r in rec:
        row = [Paragraph(r[0], cell), Paragraph(r[1], cell)]
        for i in range(len(POL_ITEMS)):
            row.append(Paragraph(f"{r[i+2]:.2f}" if r[i+2] else "", cell))
        data.append(row)

    data.append(
        ["", "Grand Total"] +
        [f"{v:.2f}" for v in rec_total]
    )

    elements.append(build_table(data))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(
        "Certified that : All transactions appearing in this ledger are truly and faithfully shown "
        "and entries have been verified / cross checked with respective log books. "
        "If equipment’s mentioned in the physical quantities held onboard as on month ending shown "
        "in this ledger are true and correct to the best of my knowledge.",
        cell
    ))

    elements.append(PageBreak())

    # ================= CONSUMPTION =================
    cons = fetch_rows("consumption", month, year)
    cons_total = totals(cons)

    elements.append(Paragraph(
        f"<b>POL CONSUMPTION – {month}/{year}</b>",
        styles["Title"]
    ))
    elements.append(Spacer(1, 4))

    data = [header]

    for r in cons:
        row = [Paragraph(r[0], cell), Paragraph(r[1], cell)]
        for i in range(len(POL_ITEMS)):
            row.append(Paragraph(f"{r[i+2]:.2f}" if r[i+2] else "", cell))
        data.append(row)

    qty_onboard = [
        f"{rec_total[i] - cons_total[i]:.2f}"
        for i in range(len(POL_ITEMS))
    ]

    data.extend([
        ["", "Total Consumed"] + [f"{v:.2f}" for v in cons_total],
        ["", "Total Transferred"] + ["NIL"]*len(POL_ITEMS),
        ["", "Quantity Held Onboard"] + qty_onboard,
        ["", "Grand Total"] + [f"{v:.2f}" for v in rec_total],
    ])

    elements.append(build_table(data))
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(
        "(ii) ________ (Quantity) of ________ (POL) has been surveyed to CGSD (PBD) "
        "in the month vide Survey Voucher ________ dated ________. "
        "Need not to be written if no survey carried out during the month.",
        cell
    ))

    doc.build(elements)
    return filename
