import sqlite3
import hashlib

DB = "pol.db"

def hash_text(t):
    return hashlib.sha256(t.encode()).hexdigest()

def tier3_reset_user(username):
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        "SELECT username FROM users WHERE username=?",
        (username,)
    )
    if not cur.fetchone():
        print("❌ User not found")
        con.close()
        return

    cur.execute("""
        UPDATE users
        SET password_hash=?,
            first_login=1,
            reset_otp_hash=NULL
        WHERE username=?
    """, (
        hash_text("hello@123"),
        username
    ))

    con.commit()
    con.close()

    print("✅ TIER III RESET COMPLETE")
    print("Username :", username)
    print("Password :", "hello@123")
    print("Action   : Forced password change on login")

if __name__ == "__main__":
    print("⚠️  TIER III USER RESET (MAINTENANCE MODE)")
    user = input("Enter username to reset (TO / CHME): ").strip()
    tier3_reset_user(user)
