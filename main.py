import random
import string
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Define a dictionary to store passwords
passwords = {}

# Function to generate a random password
def generate_password():
    length = 12  # You can customize the length
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# Function to generate a random username
def generate_username():
    username_length = 8  # You can customize the length
    username = ''.join(random.choice(string.ascii_letters) for i in range(username_length))
    username_entry.delete(0, tk.END)
    username_entry.insert(0, username)

# Function to add a new password
def add_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website and username and password:
        conn = sqlite3.connect("password_manager.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO credentials (website, username, password) VALUES (?, ?, ?)",
                       (website, username, password))
        conn.commit()
        conn.close()

        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Credentials for {website} added successfully.")
    else:
        messagebox.showerror("Error", "All fields must be filled.")

# Function to retrieve credentials
def retrieve_credentials():
    website = website_entry.get()

    if website:
        conn = sqlite3.connect("password_manager.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, password FROM credentials WHERE website = ?", (website,))
        result = cursor.fetchone()
        conn.close()

        if result:
            username, password = result
            messagebox.showinfo("Credentials", f"Website: {website}\nUsername: {username}\nPassword: {password}")
        else:
            messagebox.showerror("Error", f"No credentials found for {website}.")

# Create a simple GUI using themed Tkinter for iOS 8-like appearance
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x300")  # Set the window size

# Use themed Tkinter style
style = ttk.Style()
style.theme_use("clam")  # "clam" resembles the iOS 8 style

# Label and Entry for website
website_label = tk.Label(root, text="Website:")
website_label.pack()
website_entry = tk.Entry(root)
website_entry.pack()

# Label and Entry for username
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

# Label and Entry for password
password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root)
password_entry.pack()

# Buttons to add and retrieve credentials
add_button = tk.Button(root, text="Add Credentials", command=add_password)
add_button.pack()
retrieve_button = tk.Button(root, text="Retrieve Credentials", command=retrieve_credentials)
retrieve_button.pack()

# Buttons to generate secure username and password
generate_username_button = tk.Button(root, text="Generate Username", command=generate_username)
generate_username_button.pack()
generate_password_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_password_button.pack()

# Connect to the SQLite database or create it if it doesn't exist
try:
    conn = sqlite3.connect("password_manager.db")
    cursor = conn.cursor()

    # Create a table to store usernames, passwords, and website information
    cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (
                      id INTEGER PRIMARY KEY,
                      website TEXT NOT NULL,
                      username TEXT NOT NULL,
                      password TEXT NOT NULL)''')

    # Commit the changes
    conn.commit()

    print("Connected to the SQLite database successfully!")

except sqlite3.Error as e:
    print(f"Error connecting to the database: {e}")

finally:
    conn.close()

# Start the GUI main loop
root.mainloop()
