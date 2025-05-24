import tkinter as tk
from tkinter import messagebox
import sqlite3

# -------------------------- DATABASE --------------------------
def init_db():
    conn = sqlite3.connect("contact_book.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

# -------------------------- FUNCTIONS --------------------------
def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if name == "" or phone == "":
        messagebox.showerror("Missing Data", "Name and Phone are required.")
        return

    conn = sqlite3.connect("contact_book.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Contact added successfully!")
    clear_fields()
    view_contacts()

def view_contacts():
    contact_listbox.delete(0, tk.END)
    conn = sqlite3.connect("contact_book.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        contact_listbox.insert(tk.END, f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

def on_select(event):
    global selected_contact_id
    try:
        index = contact_listbox.curselection()[0]
        selected = contact_listbox.get(index)
        selected_contact_id, name, phone, email = [i.strip() for i in selected.split('|')]

        name_entry.delete(0, tk.END)
        name_entry.insert(tk.END, name)

        phone_entry.delete(0, tk.END)
        phone_entry.insert(tk.END, phone)

        email_entry.delete(0, tk.END)
        email_entry.insert(tk.END, email)

    except IndexError:
        pass

def update_contact():
    global selected_contact_id

    if not selected_contact_id:
        messagebox.showerror("No Selection", "Please select a contact to update.")
        return

    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()

    if name == "" or phone == "":
        messagebox.showerror("Missing Data", "Name and Phone are required.")
        return

    conn = sqlite3.connect("contact_book.db")
    cur = conn.cursor()
    cur.execute("UPDATE contacts SET name = ?, phone = ?, email = ? WHERE id = ?", (name, phone, email, selected_contact_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Updated", "Contact updated successfully!")
    clear_fields()
    view_contacts()

def delete_contact():
    global selected_contact_id

    if not selected_contact_id:
        messagebox.showerror("No Selection", "Please select a contact to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
    if not confirm:
        return

    conn = sqlite3.connect("contact_book.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id = ?", (selected_contact_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Deleted", "Contact deleted successfully!")
    clear_fields()
    view_contacts()

def clear_fields():
    global selected_contact_id
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    selected_contact_id = None

# -------------------------- GUI SETUP --------------------------
root = tk.Tk()
root.title("Contact Book")
root.geometry("500x500")

selected_contact_id = None

# Labels & Entries
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Phone").grid(row=1, column=0, padx=10, pady=5)
phone_entry = tk.Entry(root, width=30)
phone_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Email").grid(row=2, column=0, padx=10, pady=5)
email_entry = tk.Entry(root, width=30)
email_entry.grid(row=2, column=1, padx=10, pady=5)

# Buttons
add_btn = tk.Button(root, text="Add Contact", width=15, command=add_contact)
add_btn.grid(row=3, column=0, padx=5, pady=5)

view_btn = tk.Button(root, text="View All", width=15, command=view_contacts)
view_btn.grid(row=3, column=1, padx=5, pady=5)

update_btn = tk.Button(root, text="Update", width=15, command=update_contact)
update_btn.grid(row=4, column=0, padx=5, pady=5)

delete_btn = tk.Button(root, text="Delete", width=15, command=delete_contact)
delete_btn.grid(row=4, column=1, padx=5, pady=5)

clear_btn = tk.Button(root, text="Clear Fields", width=15, command=clear_fields)
clear_btn.grid(row=5, column=0, columnspan=2, pady=10)

# Contact List Display
contact_listbox = tk.Listbox(root, height=10, width=60)
contact_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
contact_listbox.bind('<<ListboxSelect>>', on_select)

# Initialize DB and Start App
init_db()
root.mainloop()
