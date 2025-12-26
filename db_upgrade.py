import sqlite3

con = sqlite3.connect("pol.db")
cur = con.cursor()

# ---------------- USERS TABLE UPGRADE ----------------
try:
    cur.execute("ALTER TABLE users ADD COLUMN reset_otp_hash TEXT")
    print("✅ Database upgraded: reset_otp_hash added")
except Exception as e:
    print("ℹ️ users.reset_otp_hash already exists")

# ---------------- TRANSFER TABLE ----------------
try:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transfer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        to_unit TEXT,
        details TEXT,
        LSHFHSD REAL, Petrol REAL, SS_15W40 REAL, SS_RR40 REAL,
        HLP_46 REAL, SP_150 REAL, SF_57 REAL, TwoT_Oil REAL,
        HP_90 REAL, SP_68 REAL, SS_320 REAL, Freon_404A REAL, SE_55 REAL,
        entered_by TEXT,
        entered_on TEXT,
        is_deleted INTEGER DEFAULT 0
    )
    """)
    print("✅ Transfer table verified/created")
except Exception as e:
    print("❌ Error creating transfer table:", e)

con.commit()
con.close()

print("✔ DB upgrade complete")
