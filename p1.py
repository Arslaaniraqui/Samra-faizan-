import tkinter as tk
from tkinter import messagebox
import mysql.connector

# MySQL connection settings
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password',  # <-- Change this!
    'database': 'hotel_db'              # <-- Make sure this DB exists!
}

def get_conn():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
        return None

def setup_db():
    conn = get_conn()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            room_no VARCHAR(20) NOT NULL,
            phone VARCHAR(20)
        )
    """)
    cursor.execute("INSERT IGNORE INTO users (username, password) VALUES (%s, %s)", ("admin", "1234"))
    conn.commit()
    cursor.close()
    conn.close()

def open_home():
    home = tk.Toplevel()
    home.title("Hotel Management System")
    home.geometry("400x450")
    home.configure(bg="#2c3e50")

    tk.Label(
        home,
        text="Welcome to Hotel Management System",
        font=("Arial", 16, "bold"),
        fg="#ecf0f1",
        bg="#2c3e50",
        pady=20
    ).pack()

    tk.Label(
        home,
        text="Enjoy your stay!",
        font=("Arial", 12),
        fg="#f1c40f",
        bg="#2c3e50",
        pady=10
    ).pack()

    # New Member
    def new_member():
        win = tk.Toplevel(home)
        win.title("New Member")
        win.geometry("300x250")
        tk.Label(win, text="Name:").pack()
        name_entry = tk.Entry(win)
        name_entry.pack()
        tk.Label(win, text="Room No:").pack()
        room_entry = tk.Entry(win)
        room_entry.pack()
        tk.Label(win, text="Phone:").pack()
        phone_entry = tk.Entry(win)
        phone_entry.pack()

        def add_member():
            name = name_entry.get()
            room = room_entry.get()
            phone = phone_entry.get()
            if not name or not room:
                messagebox.showerror("Error", "Name and Room No required.")
                return
            conn = get_conn()
            if conn is None:
                return
            cursor = conn.cursor()
            cursor.execute("INSERT INTO members (name, room_no, phone) VALUES (%s, %s, %s)", (name, room, phone))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Member added!")
            win.destroy()

        tk.Button(win, text="Add Member", command=add_member).pack(pady=10)

    # Old Member
    def old_member():
        win = tk.Toplevel(home)
        win.title("Old Member")
        win.geometry("350x250")
        tk.Label(win, text="All Members:").pack()
        conn = get_conn()
        if conn is None:
            return
        cursor = conn.cursor()
        cursor.execute("SELECT member_id, name, room_no, phone FROM members")
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        for m in members:
            tk.Label(win, text=f"ID:{m[0]} Name:{m[1]} Room:{m[2]} Phone:{m[3]}").pack()

    # Update Data
    def update_data():
        win = tk.Toplevel(home)
        win.title("Update Data")
        win.geometry("300x300")
        tk.Label(win, text="Member ID to Update:").pack()
        id_entry = tk.Entry(win)
        id_entry.pack()
        tk.Label(win, text="New Name:").pack()
        name_entry = tk.Entry(win)
        name_entry.pack()
        tk.Label(win, text="New Room No:").pack()
        room_entry = tk.Entry(win)
        room_entry.pack()
        tk.Label(win, text="New Phone:").pack()
        phone_entry = tk.Entry(win)
        phone_entry.pack()

        def update_member():
            member_id = id_entry.get()
            name = name_entry.get()
            room = room_entry.get()
            phone = phone_entry.get()
            if not member_id:
                messagebox.showerror("Error", "Member ID required.")
                return
            conn = get_conn()
            if conn is None:
                return
            cursor = conn.cursor()
            cursor.execute("UPDATE members SET name=%s, room_no=%s, phone=%s WHERE member_id=%s", (name, room, phone, member_id))
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Member not found.")
            else:
                messagebox.showinfo("Success", "Member updated!")
            conn.commit()
            cursor.close()
            conn.close()
            win.destroy()

        tk.Button(win, text="Update Member", command=update_member).pack(pady=10)

    # Search Data
    def search_data():
        win = tk.Toplevel(home)
        win.title("Search Data")
        win.geometry("300x200")
        tk.Label(win, text="Search by Name:").pack()
        search_entry = tk.Entry(win)
        search_entry.pack()

        def search_member():
            name = search_entry.get()
            conn = get_conn()
            if conn is None:
                return
            cursor = conn.cursor()
            cursor.execute("SELECT member_id, name, room_no, phone FROM members WHERE name LIKE %s", ('%' + name + '%',))
            members = cursor.fetchall()
            cursor.close()
            conn.close()
            result_win = tk.Toplevel(win)
            result_win.title("Search Results")
            for m in members:
                tk.Label(result_win, text=f"ID:{m[0]} Name:{m[1]} Room:{m[2]} Phone:{m[3]}").pack()
            if not members:
                tk.Label(result_win, text="No members found.").pack()

        tk.Button(win, text="Search", command=search_member).pack(pady=10)

    # Delete Data
    def delete_data():
        win = tk.Toplevel(home)
        win.title("Delete Data")
        win.geometry("300x150")
        tk.Label(win, text="Member ID to Delete:").pack()
        id_entry = tk.Entry(win)
        id_entry.pack()

        def delete_member():
            member_id = id_entry.get()
            if not member_id:
                messagebox.showerror("Error", "Member ID required.")
                return
            conn = get_conn()
            if conn is None:
                return
            cursor = conn.cursor()
            cursor.execute("DELETE FROM members WHERE member_id=%s", (member_id,))
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Member not found.")
            else:
                messagebox.showinfo("Success", "Member deleted!")
            conn.commit()
            cursor.close()
            conn.close()
            win.destroy()

        tk.Button(win, text="Delete Member", command=delete_member).pack(pady=10)

    # Buttons
    tk.Button(
        home,
        text="New Member",
        font=("Arial", 10, "bold"),
        bg="#27ae60",
        fg="#fff",
        command=new_member,
        padx=20,
        pady=5
    ).pack(pady=8)

    tk.Button(
        home,
        text="Old Member",
        font=("Arial", 10, "bold"),
        bg="#2980b9",
        fg="#fff",
        command=old_member,
        padx=20,
        pady=5
    ).pack(pady=8)

    tk.Button(
        home,
        text="Update Data",
        font=("Arial", 10, "bold"),
        bg="#f39c12",
        fg="#fff",
        command=update_data,
        padx=20,
        pady=5
    ).pack(pady=8)

    tk.Button(
        home,
        text="Search Data",
        font=("Arial", 10, "bold"),
        bg="#8e44ad",
        fg="#fff",
        command=search_data,
        padx=20,
        pady=5
    ).pack(pady=8)

    tk.Button(
        home,
        text="Delete Data",
        font=("Arial", 10, "bold"),
        bg="#c0392b",
        fg="#fff",
        command=delete_data,
        padx=20,
        pady=5
    ).pack(pady=8)

    tk.Button(
        home,
        text="Close",
        font=("Arial", 10, "bold"),
        bg="#e74c3c",
        fg="#fff",
        command=home.destroy,
        padx=20,
        pady=5
    ).pack(pady=15)

def login():
    username = entry_user.get()
    password = entry_pass.get()
    conn = get_conn()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        messagebox.showinfo("Login", "Login successful!")
        open_home()  # Open new page
    else:
        messagebox.showerror("Login", "Invalid credentials.")

def register():
    reg_win = tk.Toplevel()
    reg_win.title("Register")
    reg_win.geometry("300x200")

    tk.Label(reg_win, text="New Username:").pack(pady=5)
    reg_user = tk.Entry(reg_win)
    reg_user.pack()

    tk.Label(reg_win, text="New Password:").pack(pady=5)
    reg_pass = tk.Entry(reg_win, show="*")
    reg_pass.pack()

    def submit_registration():
        username = reg_user.get()
        password = reg_pass.get()
        if not username or not password:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        conn = get_conn()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            reg_win.destroy()
        except mysql.connector.errors.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        cursor.close()
        conn.close()

    tk.Button(reg_win, text="Register", command=submit_registration).pack(pady=10)

def main():
    setup_db()
    global entry_user, entry_pass
    root = tk.Tk()
    root.title("Login Page")
    root.geometry("300x180")

    tk.Label(root, text="Username:").pack(pady=5)
    entry_user = tk.Entry(root)
    entry_user.pack()

    tk.Label(root, text="Password:").pack(pady=5)
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    tk.Button(root, text="Login", command=login).pack(pady=5)
    tk.Button(root, text="Register", command=register).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()