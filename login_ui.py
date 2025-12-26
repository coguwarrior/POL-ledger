import tkinter as tk
from tkinter import messagebox, simpledialog

import main_app
from auth import authenticate, change_password, emergency_reset

# ---------------- CONFIG ----------------
IT_ADMIN_CODE = "ITMC@2025"   # change if required

# ================= LOGIN UI =================
def login():
    root = tk.Tk()
    root.title("POL Ledger Login")
    root.geometry("360x260")
    root.resizable(False, False)

    tk.Label(
        root,
        text="POL LEDGER SYSTEM",
        font=("Arial", 14, "bold")
    ).pack(pady=12)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text="Username").grid(row=0, column=0, pady=6, sticky="e")
    user_e = tk.Entry(frame)
    user_e.grid(row=0, column=1, pady=6)

    tk.Label(frame, text="Password").grid(row=1, column=0, pady=6, sticky="e")
    pass_e = tk.Entry(frame, show="*")
    pass_e.grid(row=1, column=1, pady=6)

    # ================= LOGIN ATTEMPT =================
    def attempt_login():
        user = user_e.get().strip()
        pwd = pass_e.get().strip()

        if not user or not pwd:
            messagebox.showerror("Error", "Enter username and password")
            return

        ok, first_login = authenticate(user, pwd)
        if not ok:
            messagebox.showerror("Login Failed", "Invalid credentials")
            return

        if first_login:
            messagebox.showinfo(
                "Password Change Required",
                "You must change your password now."
            )

            new_pwd = simpledialog.askstring(
                "Change Password",
                "Enter new password",
                show="*"
            )
            if not new_pwd:
                return

            change_password(user, new_pwd)
            messagebox.showinfo("Success", "Password changed. Login again.")

            root.destroy()
            login()
            return

        root.destroy()
        main_app.launch(user)

    # ================= FORGOT PASSWORD =================
    def forgot_password():
        user = simpledialog.askstring(
            "Forgot Password",
            "Enter Username (TO / CHME)"
        )

        if not user or user not in ("TO", "CHME"):
            messagebox.showerror("Error", "Invalid username")
            return

        admin_code = simpledialog.askstring(
            "IT Admin Authorisation",
            "Enter IT Admin Authorisation Code",
            show="*"
        )

        if admin_code != IT_ADMIN_CODE:
            messagebox.showerror(
                "Denied",
                "Invalid IT Admin authorisation"
            )
            return

        ok = emergency_reset(user)
        if not ok:
            messagebox.showerror("Error", "Reset failed")
            return

        messagebox.showinfo(
            "Password Reset Successful",
            "Password reset to default.\n\n"
            "Login using default password and\n"
            "change it immediately."
        )

    # ================= BUTTONS =================
    tk.Button(
        root,
        text="Login",
        width=20,
        command=attempt_login
    ).pack(pady=10)

    tk.Button(
        root,
        text="Forgot Password?",
        fg="blue",
        relief="flat",
        command=forgot_password
    ).pack()

    root.mainloop()


if __name__ == "__main__":
    login()
