import tkinter as tk
from tkinter import messagebox
import random
import string

# Define a dictionary to store passwords
passwords = {}

# Function to generate a random password
def generate_password():
    length = 12  # You can customize the length
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Function to add a new password
def add_password():
    website = website_entry.get()
    password = password_entry.get()

    if website and password:
        passwords[website] = password
        website_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Password for {website} added successfully.")
    else:
        messagebox.showerror("Error", "Both fields must be filled.")

# Function to retrieve a password
def retrieve_password():
    website = website_entry.get()

    if website in passwords:
        password = passwords[website]
        messagebox.showinfo("Password", f"Password for {website}: {password}")
    else:
        messagebox.showerror("Error", f"No password found for {website}.")

# Create a simple GUI using Tkinter
root = tk.Tk()
root.title("Password Manager")

# Label and Entry for website
website_label = tk.Label(root, text="Website:")
website_label.pack()
website_entry = tk.Entry(root)
website_entry.pack()

# Label and Entry for password
password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root)
password_entry.pack()

# Buttons to add and retrieve passwords
add_button = tk.Button(root, text="Add Password", command=add_password)
add_button.pack()
retrieve_button = tk.Button(root, text="Retrieve Password", command=retrieve_password)
retrieve_button.pack()

# Start the GUI main loop
root.mainloop()
