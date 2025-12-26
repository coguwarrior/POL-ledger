from datetime import datetime
from db import connect
from audit import log_action

def cancel_entry(table, record_id, reason, user):
    con = connect()
    cur = con.cursor()

    cur.execute(f"""
    UPDATE {table}
    SET is_deleted=1, delete_reason=?, deleted_by=?, deleted_on=?
    WHERE id=? AND is_deleted=0
    """, (reason, user, datetime.now().strftime("%Y-%m-%d %H:%M"), record_id))

    con.commit()
    con.close()
    log_action(user, f"{table.upper()} CANCELLED", f"ID {record_id} : {reason}")
