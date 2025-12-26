import sqlite3
import hashlib

DB = "pol.db"

# ---------------- HASH ----------------
def hash_text(t):
    return hashlib.sha256(t.encode()).hexdigest()

# ---------------- AUTHENTICATE ----------------
def authenticate(username, password):
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        "SELECT password_hash, first_login FROM users WHERE username=?",
        (username,)
    )
    row = cur.fetchone()
    con.close()

    if not row:
        return False, False

    pwd_hash, first_login = row
    if pwd_hash == hash_text(password):
        return True, bool(first_login)

    return False, False

# ---------------- CHANGE PASSWORD ----------------
def change_password(username, new_pwd):
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
        UPDATE users
        SET password_hash=?,
            first_login=0
        WHERE username=?
    """, (
        hash_text(new_pwd),
        username
    ))

    con.commit()
    con.close()

# ---------------- EMERGENCY RESET (ADMIN AUTHORISED) ----------------
def emergency_reset(username):
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        "SELECT username FROM users WHERE username=?",
        (username,)
    )
    if not cur.fetchone():
        con.close()
        return False

    cur.execute("""
        UPDATE users
        SET password_hash=?,
            first_login=1
        WHERE username=?
    """, (
        hash_text("hello@123"),
        username
    ))

    con.commit()
    con.close()
    return True
