import sqlite3
import hashlib

DB_NAME = "pol.db"

def connect():
    return sqlite3.connect(DB_NAME)

def hash_pwd(p):
    return hashlib.sha256(p.encode()).hexdigest()

def create_tables():
    con = connect()
    cur = con.cursor()

    # ================= USERS =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT,
        first_login INTEGER
    )
    """)

    # ================= RECEIPT =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS receipt (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        details TEXT,
        LSHFHSD REAL, Petrol REAL, SS_15W40 REAL, SS_RR40 REAL,
        HLP_46 REAL, SP_150 REAL, SF_57 REAL, TwoT_Oil REAL,
        HP_90 REAL, SP_68 REAL, SS_320 REAL, Freon_404A REAL, SE_55 REAL,
        entered_by TEXT,
        entered_on TEXT,
        entry_type TEXT DEFAULT 'NORMAL',
        is_deleted INTEGER DEFAULT 0,
        delete_reason TEXT,
        deleted_by TEXT,
        deleted_on TEXT
    )
    """)

    # ================= CONSUMPTION =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS consumption (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        details TEXT,
        LSHFHSD REAL, Petrol REAL, SS_15W40 REAL, SS_RR40 REAL,
        HLP_46 REAL, SP_150 REAL, SF_57 REAL, TwoT_Oil REAL,
        HP_90 REAL, SP_68 REAL, SS_320 REAL, Freon_404A REAL, SE_55 REAL,
        entered_by TEXT,
        entered_on TEXT,
        is_deleted INTEGER DEFAULT 0,
        delete_reason TEXT,
        deleted_by TEXT,
        deleted_on TEXT
    )
    """)

    # ================= AUDIT LOG =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        action TEXT,
        details TEXT,
        timestamp TEXT
    )
    """)

    # ================= MONTH LOCK =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS month_lock (
        month TEXT,
        year TEXT,
        locked_by TEXT,
        PRIMARY KEY (month, year)
    )
    """)

    # ================= EMERGENCY RECOVERY KEY =================
    cur.execute("""
    CREATE TABLE IF NOT EXISTS recovery_key (
        key_hash TEXT,
        generated_on TEXT
    )
    """)

    # ================= DEFAULT USERS =================
    default_pwd = hash_pwd("hello@123")
    for u in ["TO", "CHME"]:
        cur.execute(
            "INSERT OR IGNORE INTO users VALUES (?,?,?)",
            (u, default_pwd, 1)
        )

    con.commit()
    con.close()
