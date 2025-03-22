import json
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime


# ---------------------- Functions ---------------------- #
def add_expense():
    """ Adds an expense to the JSON file after validation. """
    category = category_input.get()
    amount = amount_input.get()

    # Validate input
    if not category or not amount:
        messagebox.showerror("Error", "Please enter category and amount.")
        return

    try:
        amount = float(amount)  # Convert amount to float
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return

    date = datetime.now().strftime("%Y-%m-%d")  # Current date
    new_data = {"category": category, "amount": amount, "date": date}

    # Load existing data or create new file
    try:
        with open("expenses.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Update data and save
    data.append(new_data)
    with open("expenses.json", "w") as file:
        json.dump(data, file, indent=4)

    # Clear input fields
    category_input.delete(0, tk.END)
    amount_input.delete(0, tk.END)

    messagebox.showinfo("Success", "Expense added successfully!")


def show_pie_chart():
    """ Displays a pie chart of expenses by category. """
    try:
        with open("expenses.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "No expenses found.")
        return

    # Aggregate expenses by category
    category_totals = {}
    for item in data:
        category_totals[item["category"]] = category_totals.get(item["category"], 0) + item["amount"]

    if not category_totals:
        messagebox.showinfo("Info", "No expenses available for visualization.")
        return

    # Plot pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(category_totals.values(), labels=category_totals.keys(), autopct="%1.1f%%", startangle=140)
    plt.title("Expense Distribution by Category")
    plt.show()


def show_bar_chart():
    """ Displays a bar chart of total expenses per month. """
    try:
        with open("expenses.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "No expenses found.")
        return

    # Aggregate expenses by month
    monthly_totals = {}
    for item in data:
        month = item["date"][:7]  # Extract YYYY-MM from date
        monthly_totals[month] = monthly_totals.get(month, 0) + item["amount"]

    if not monthly_totals:
        messagebox.showinfo("Info", "No expenses available for visualization.")
        return

    # Plot bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(monthly_totals.keys(), monthly_totals.values(), color="blue")
    plt.xlabel("Month")
    plt.ylabel("Total Expenses (₹)")
    plt.title("Monthly Expense Overview")
    plt.xticks(rotation=45)
    plt.show()


# ---------------------- UI Setup ---------------------- #
root = tk.Tk()
root.title("Expense Tracker")
root.config(padx=20, pady=20)

# Labels & Inputs
tk.Label(root, text="Category:").grid(row=0, column=0, sticky="w")
category_input = tk.Entry(root, width=25)
category_input.grid(row=0, column=1)

tk.Label(root, text="Amount (₹):").grid(row=1, column=0, sticky="w")
amount_input = tk.Entry(root, width=25)
amount_input.grid(row=1, column=1)

# Buttons
add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=2, column=0, columnspan=2, pady=5)

pie_chart_button = tk.Button(root, text="Show Pie Chart", command=show_pie_chart)
pie_chart_button.grid(row=3, column=0, columnspan=2, pady=5)

bar_chart_button = tk.Button(root, text="Show Bar Chart", command=show_bar_chart)
bar_chart_button.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()