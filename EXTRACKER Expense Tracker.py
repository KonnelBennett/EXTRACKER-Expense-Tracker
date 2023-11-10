import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def load_expenses():
    try:
        expenses = []
        with open('expenses.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append(row)
        return expenses
    except FileNotFoundError:
        return []


def save_expenses(expenses):
    with open('expenses.csv', 'w', newline='') as file:
        fieldnames = ['Description', 'Amount', 'Category']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)


def add_expense():
    description = description_entry.get()
    amount = amount_entry.get()
    category = category_entry.get()

    if not description or not amount or not category:
        messagebox.showerror("Error", "All fields must be filled in.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number.")
        return

    expenses = load_expenses()
    expenses.append({'Description': description, 'Amount': amount, 'Category': category})
    save_expenses(expenses)
    update_expense_list()

    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Expense added successfully!")


def update_expense_list():
    for row in expense_list.get_children():
        expense_list.delete(row)

    expenses = load_expenses()
    for expense in expenses:
        expense_list.insert('', 'end', values=(expense['Description'], expense['Amount'], expense['Category']))


def generate_report():
    expenses = load_expenses()

    if not expenses:
        messagebox.showinfo("Info", "No expenses to generate a report.")
        return

    category_expenses = {}
    for expense in expenses:
        category = expense['Category']
        if category not in category_expenses:
            category_expenses[category] = 0
        category_expenses[category] += float(expense['Amount'])

    labels = category_expenses.keys()
    values = category_expenses.values()

    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Expense Distribution by Category")

    report_window = tk.Toplevel(root)
    report_window.title("Expense Report")

    canvas = FigureCanvasTkAgg(plt.gcf(), master=report_window)
    canvas.get_tk_widget().pack()


root = tk.Tk()
root.title("EXTRACKER - Expense Tracking Application")

frame = ttk.LabelFrame(root, text="Add Expense")
frame.grid(row=0, column=0, padx=10, pady=10)

description_label = ttk.Label(frame, text="Description:")
description_label.grid(row=0, column=0)
description_entry = ttk.Entry(frame)
description_entry.grid(row=0, column=1)

amount_label = ttk.Label(frame, text="Amount:")
amount_label.grid(row=1, column=0)
amount_entry = ttk.Entry(frame)
amount_entry.grid(row=1, column=1)

category_label = ttk.Label(frame, text="Category:")
category_label.grid(row=2, column=0)
category_entry = ttk.Entry(frame)
category_entry.grid(row=2, column=1)

add_button = ttk.Button(frame, text="Add Expense", command=add_expense)
add_button.grid(row=3, columnspan=2)

frame = ttk.LabelFrame(root, text="Expense List")
frame.grid(row=1, column=0, padx=10, pady=10)

expense_list = ttk.Treeview(frame, columns=('Description', 'Amount', 'Category'), show='headings')
expense_list.heading('Description', text='Description')
expense_list.heading('Amount', text='Amount')
expense_list.heading('Category', text='Category')
expense_list.pack()

update_expense_list()

report_button = ttk.Button(root, text="Generate Report", command=generate_report)
report_button.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()
