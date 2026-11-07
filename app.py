import tkinter as tk
from tkinter import messagebox, ttk
import os
import re
from datetime import datetime, timedelta

# ---------------- EMAIL VALIDATION ---------------- #
def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email)

# ---------------- USER SYSTEM ---------------- #
def register():
    email = user_entry.get().strip()
    password = pass_entry.get().strip()

    if not email or not password:
        messagebox.showwarning("Error", "Fill all fields")
        return

    if not is_valid_email(email):
        messagebox.showerror("Error", "Enter valid Gmail address")
        return

    if os.path.exists("users.txt"):
        with open("users.txt", "r") as f:
            for line in f:
                e, _ = line.strip().split("|")
                if e == email:
                    messagebox.showerror("Error", "Account already exists")
                    return

    with open("users.txt", "a") as f:
        f.write(f"{email}|{password}\n")

    messagebox.showinfo("Success", "Account created 🎉")

def login():
    email = user_entry.get().strip()
    password = pass_entry.get().strip()

    if not os.path.exists("users.txt"):
        messagebox.showerror("Error", "No users found")
        return

    with open("users.txt", "r") as f:
        for line in f:
            e, p = line.strip().split("|")
            if e == email and p == password:
                root.destroy()
                open_main_app()
                return

    messagebox.showerror("Error", "Invalid email or password")

# ---------------- MAIN APP ---------------- #
def open_main_app():
    app = tk.Tk()
    app.title("🌸 Daily Flow")
    app.geometry("420x600")
    app.config(bg="#fef6f9")

    tasks = []
    current_date = datetime.now()

    def format_date(date):
        return date.strftime("%A, %d %B %Y")

    # LOAD TASKS
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            for line in file:
                if "|" in line:
                    try:
                        t, s, d = line.strip().split("|")
                        tasks.append((t, s == "True", d))
                    except:
                        pass

    def save():
        with open("tasks.txt", "w") as f:
            for t, s, d in tasks:
                f.write(f"{t}|{s}|{d}\n")

    def get_today():
        return [x for x in tasks if x[2] == format_date(current_date)]

    # UPDATE UI
    def update():
        listbox.delete(0, tk.END)
        today = get_today()
        done = 0

        for t, s, d in today:
            if s:
                listbox.insert(tk.END, "✔ " + t)
                listbox.itemconfig(tk.END, fg="#aaa")
                done += 1
            else:
                listbox.insert(tk.END, "◻ " + t)

        total = len(today)

        if total == 0:
            progress_label.config(text="No tasks 🌸")
            progress_bar["value"] = 0
        else:
            progress_label.config(text=f"{done}/{total} tasks done ✨")
            progress_bar["value"] = (done / total) * 100

        date_label.config(text=format_date(current_date))

    # FUNCTIONS
    def add():
        t = entry.get().strip()
        if t:
            tasks.append((t, False, format_date(current_date)))
            save()
            update()
            entry.delete(0, tk.END)

    def toggle():
        try:
            i = listbox.curselection()[0]
            today = get_today()
            t, s, d = today[i]
            idx = tasks.index((t, s, d))
            tasks[idx] = (t, not s, d)
            save()
            update()
        except:
            pass

    def delete():
        try:
            i = listbox.curselection()[0]
            today = get_today()
            tasks.remove(today[i])
            save()
            update()
        except:
            pass

    def prev_day():
        nonlocal current_date
        current_date -= timedelta(days=1)
        update()

    def next_day():
        nonlocal current_date
        current_date += timedelta(days=1)
        update()

    # BUTTON PRESS EFFECT
    def press(btn, color):
        btn.config(bg=color)
        app.after(120, lambda: btn.config(bg=btn.default))

    # CARD UI
    card = tk.Frame(app, bg="white", highlightbackground="#eee", highlightthickness=1)
    card.pack(padx=20, pady=20, fill="both", expand=True)

    tk.Label(card, text="Daily Flow ✨", font=("Helvetica", 18, "bold"), bg="white").pack(pady=10)

    # NAV
    nav = tk.Frame(card, bg="white")
    nav.pack()

    prev_btn = tk.Button(nav, text="←", bg="#ffc8dd", relief="flat",
                         command=lambda:[press(prev_btn,"#ffafcc"), prev_day()])
    prev_btn.default = "#ffc8dd"
    prev_btn.grid(row=0, column=0)

    date_label = tk.Label(nav, bg="white")
    date_label.grid(row=0, column=1, padx=10)

    next_btn = tk.Button(nav, text="→", bg="#ffc8dd", relief="flat",
                         command=lambda:[press(next_btn,"#ffafcc"), next_day()])
    next_btn.default = "#ffc8dd"
    next_btn.grid(row=0, column=2)

    # PROGRESS
    progress_label = tk.Label(card, bg="white")
    progress_label.pack(pady=5)

    progress_bar = ttk.Progressbar(card, length=250)
    progress_bar.pack(pady=5)

    # ENTRY
    entry = tk.Entry(card)
    entry.pack(pady=10, ipady=5)

    # BUTTONS
    btns = tk.Frame(card, bg="white")
    btns.pack()

    add_btn = tk.Button(btns, text="Add", bg="#ffcad4", relief="flat",
                        command=lambda:[press(add_btn,"#ffb3c6"), add()])
    add_btn.default = "#ffcad4"
    add_btn.grid(row=0, column=0, padx=5)

    done_btn = tk.Button(btns, text="Done", bg="#cdb4db", relief="flat",
                         command=lambda:[press(done_btn,"#b8a0d6"), toggle()])
    done_btn.default = "#cdb4db"
    done_btn.grid(row=0, column=1, padx=5)

    del_btn = tk.Button(btns, text="Delete", bg="#ffc8dd", relief="flat",
                        command=lambda:[press(del_btn,"#ffafcc"), delete()])
    del_btn.default = "#ffc8dd"
    del_btn.grid(row=1, column=0, columnspan=2, pady=5)

    # LIST
    listbox = tk.Listbox(card, height=15, bd=0, highlightthickness=0)
    listbox.pack(pady=10)

    update()
    app.mainloop()

# ---------------- LOGIN UI ---------------- #
root = tk.Tk()
root.title("Login")
root.geometry("320x320")
root.config(bg="#fef6f9")

tk.Label(root, text="Welcome 🌸", font=("Helvetica", 16), bg="#fef6f9").pack(pady=10)

tk.Label(root, text="Email", bg="#fef6f9").pack()
user_entry = tk.Entry(root)
user_entry.pack(pady=5)

tk.Label(root, text="Password", bg="#fef6f9").pack()
pass_entry = tk.Entry(root, show="*")
pass_entry.pack(pady=5)

tk.Button(root, text="Login", bg="#cdb4db", relief="flat", command=login).pack(pady=10)
tk.Button(root, text="Create Account", bg="#ffcad4", relief="flat", command=register).pack()

root.mainloop()