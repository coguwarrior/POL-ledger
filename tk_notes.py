import tkinter as tk

root = tk.Tk()
root.title("TK TEST WINDOW")
root.geometry("300x200")

tk.Label(root, text="If you see this, Tkinter works").pack(pady=40)

root.mainloop()
