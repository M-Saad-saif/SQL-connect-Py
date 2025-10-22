import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

#  MySQL Connection
conn = mysql.connector.connect(
    host="127.0.0.1", user="root", password="saadsaifmysql", database="student_db"
)
cursor = conn.cursor()


# Functions
def save_data():
    sid = entry_id.get()
    name = entry_name.get()
    age = entry_age.get()
    dept = entry_dept.get()

    if sid == "" or name == "" or age == "" or dept == "":
        messagebox.showwarning("Warning", "All fields are required!")
        return

    try:
        cursor.execute(
            "INSERT INTO students (id, name, age, department) VALUES (%s, %s, %s, %s)",
            (sid, name, age, dept),
        )
        conn.commit()

        with open("students_data.txt", "a") as f:
            f.write(f"ID: {sid}, Name: {name}, Age: {age}, Department: {dept}\n")

        messagebox.showinfo("Success", "Data saved successfully!")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def retrieve_data():
    sid = entry_id.get()
    cursor.execute("SELECT * FROM students WHERE id=%s", (sid,))
    result = cursor.fetchone()

    if result:
        entry_name.delete(0, tk.END)
        entry_name.insert(0, result[1])
        entry_age.delete(0, tk.END)
        entry_age.insert(0, result[2])
        entry_dept.delete(0, tk.END)
        entry_dept.insert(0, result[3])
    else:
        messagebox.showinfo("Not Found", "No record found for this ID.")


def delete_data():
    sid = entry_id.get()
    if sid == "":
        messagebox.showwarning("Warning", "Enter an ID to delete.")
        return

    try:
        # Delete from database
        cursor.execute("DELETE FROM students WHERE id=%s", (sid,))
        conn.commit()

        # Delete from file
        lines = []
        with open("students_data.txt", "r") as f:
            lines = f.readlines()

        with open("students_data.txt", "w") as f:
            for line in lines:
                if not line.strip().startswith(f"ID: {sid},"):
                    f.write(line)

        messagebox.showinfo("Deleted", "Record deleted successfully.")
        clear_fields()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_dept.delete(0, tk.END)


# gui==
root = tk.Tk()
root.title("MySQL connect python")
root.geometry("550x400")
root.configure(bg="#79aaff")

# Main Frame
frame = ttk.Frame(root, padding=20)
frame.pack(pady=20)

# Title
title_label = ttk.Label(
    frame, text="Student Information", font=("Segoe UI", 18, "bold")
)
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Labels and Entries
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 11))
style.configure("TEntry", font=("Segoe UI", 11))

ttk.Label(frame, text="Student ID:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
entry_id = ttk.Entry(frame, width=30)
entry_id.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Name:").grid(row=2, column=0, sticky="e", pady=5, padx=5)
entry_name = ttk.Entry(frame, width=30)
entry_name.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Age:").grid(row=3, column=0, sticky="e", pady=5, padx=5)
entry_age = ttk.Entry(frame, width=30)
entry_age.grid(row=3, column=1, pady=5)

ttk.Label(frame, text="Department:").grid(row=4, column=0, sticky="e", pady=5, padx=5)
entry_dept = ttk.Entry(frame, width=30)
entry_dept.grid(row=4, column=1, pady=5)

# Buttons
button_frame = ttk.Frame(frame)
button_frame.grid(row=5, column=0, columnspan=2, pady=20)

style.configure(
    "TButton",
    font=("Segoe UI", 10, "bold"),
    padding=6,
    background="blue",  # Button color
    foreground="black",  # text color
)

style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

ttk.Button(button_frame, text="Save", command=save_data).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Retrieve", command=retrieve_data).grid(
    row=0, column=1, padx=10
)
ttk.Button(button_frame, text="Delete", command=delete_data).grid(
    row=0, column=2, padx=10
)
ttk.Button(button_frame, text="Clear", command=clear_fields).grid(
    row=0, column=3, padx=10
)

root.mainloop()
