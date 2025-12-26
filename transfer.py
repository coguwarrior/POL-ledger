from datetime import datetime
from db import connect
from audit import log_action
from backup import auto_backup

def add_transfer(user, date, to_unit, details, data):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO transfer (
        date, to_unit, details,
        LSHFHSD, Petrol, SS_15W40, SS_RR40,
        HLP_46, SP_150, SF_57, TwoT_Oil,
        HP_90, SP_68, SS_320, Freon_404A, SE_55,
        entered_by, entered_on
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        date, to_unit, details,
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
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    con.commit()
    con.close()

    log_action(user, "TRANSFER OUT", f"To {to_unit} | {details}")
    auto_backup()
