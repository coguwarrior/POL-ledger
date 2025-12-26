from datetime import datetime
from db import connect

def log_action(user, action, details):
    con = connect()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO audit_log VALUES (NULL,?,?,?,?)
    """, (user, action, details, datetime.now().strftime("%Y-%m-%d %H:%M")))

    con.commit()
    con.close()
