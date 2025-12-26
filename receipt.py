from datetime import datetime
from db import connect
from audit import log_action
from backup import auto_backup

def add_receipt(user, date, details, data, entry_type="NORMAL"):
    """
    Adds a receipt entry to the POL ledger.

    Parameters:
    user (str)        : Logged-in user (TO / CHME)
    date (str)        : Date in YYYY-MM-DD format
    details (str)     : Description of receipt
    data (dict)       : POL quantities keyed by item name
    entry_type (str)  : NORMAL or OPENING
    """

    con = connect()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO receipt (
        date, details,
        LSHFHSD, Petrol, SS_15W40, SS_RR40,
        HLP_46, SP_150, SF_57, TwoT_Oil,
        HP_90, SP_68, SS_320, Freon_404A, SE_55,
        entered_by, entered_on,
        entry_type
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        date,
        details,

        data.get("LSHFHSD", 0),
        data.get("Petrol", 0),
        data.get("SS_15W40", 0),
        data.get("SS_RR40", 0),
        data.get("HLP_46", 0),
        data.get("SP_150", 0),
        data.get("SF_57", 0),
        data.get("TwoT_Oil", 0),
        data.get("HP_90", 0),
        data.get("SP_68", 0),
        data.get("SS_320", 0),
        data.get("Freon_404A", 0),
        data.get("SE_55", 0),

        user,
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        entry_type
    ))

    con.commit()
    con.close()

    # Audit + Backup
    log_action(
        user=user,
        action="RECEIPT ENTRY",
        details=f"{details} ({entry_type})"
    )

    auto_backup()
