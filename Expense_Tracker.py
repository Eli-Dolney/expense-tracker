import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# File to store expenses
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
folder_path = os.path.join(desktop_path, "ExpenseTracker")
os.makedirs(folder_path, exist_ok=True)
EXPENSES_FILE = os.path.join(folder_path, 'expenses.json')

print(f"Folder path: {folder_path}")
print(f"Expenses file path: {EXPENSES_FILE}")

def load_expenses():
    """Load expenses from a file."""
    try:
        if os.path.exists(EXPENSES_FILE):
            with open(EXPENSES_FILE, 'r') as file:
                expenses = json.load(file)
        else:
            expenses = []
        return expenses
    except Exception as e:
        print(f"Error loading expenses: {e}")
        return []

def save_expenses(expenses):
    """Save expenses to a file."""
    try:
        with open(EXPENSES_FILE, 'w') as file:
            json.dump(expenses, file, indent=4)
        save_expenses_to_txt(expenses)
    except Exception as e:
        print(f"Error saving expenses: {e}")

def save_expenses_to_txt(expenses):
    """Save expenses to a text file."""
    try:
        txt_file = os.path.join(folder_path, 'expenses.txt')
        with open(txt_file, 'w') as file:
            for expense in expenses:
                file.write(f"{expense['date']} - {expense['category']} - ${expense['amount']} - {expense['description']}\n")
        print(f"Expenses saved to {txt_file}")
    except Exception as e:
        print(f"Error saving expenses to txt file: {e}")

def add_expense(expenses, date, category, amount, description):
    """Add a new expense."""
    expense = {
        'date': date,
        'category': category,
        'amount': amount,
        'description': description
    }
    expenses.append(expense)

def view_expenses(expenses):
    """Display all expenses."""
    if not expenses:
        messagebox.showinfo("View Expenses", "No expenses to show.")
    else:
        expense_list = "\n".join(f"{expense['date']} - {expense['category']} - ${expense['amount']} - {expense['description']}" for expense in expenses)
        messagebox.showinfo("View Expenses", expense_list)

def generate_report_by_category(expenses):
    """Generate a report of expenses by category."""
    report = {}
    for expense in expenses:
        category = expense['category']
        amount = float(expense['amount'])
        if category in report:
            report[category] += amount
        else:
            report[category] = amount
    report_list = "\n".join(f"Category: {category}, Total Spent: ${total:.2f}" for category, total in report.items())
    messagebox.showinfo("Report by Category", report_list)

def generate_report_by_time(expenses):
    """Generate a report of expenses over time."""
    report = {}
    for expense in expenses:
        date = expense['date']
        amount = float(expense['amount'])
        if date in report:
            report[date] += amount
        else:
            report[date] = amount
    report_list = "\n".join(f"Date: {date}, Total Spent: ${total:.2f}" for date, total in sorted(report.items()))
    messagebox.showinfo("Report by Time", report_list)

def main():
    expenses = load_expenses()

    def on_add_expense():
        date = simpledialog.askstring("Input", "Enter the date (YYYY-MM-DD):")
        category = simpledialog.askstring("Input", "Enter the category:")
        amount = simpledialog.askstring("Input", "Enter the amount:")
        description = simpledialog.askstring("Input", "Enter the description:")
        if date and category and amount and description:
            add_expense(expenses, date, category, amount, description)
            save_expenses(expenses)
            messagebox.showinfo("Success", "Expense added successfully!")
        else:
            messagebox.showerror("Error", "All fields must be filled in!")

    def on_view_expenses():
        view_expenses(expenses)

    def on_generate_report_by_category():
        generate_report_by_category(expenses)

    def on_generate_report_by_time():
        generate_report_by_time(expenses)

    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("500x400")

    # Styling
    style = ttk.Style()
    style.theme_use("clam")

    # Configure styles for buttons and labels
    style.configure("TButton", font=("Helvetica", 12), padding=10, background="#4CAF50", foreground="white")
    style.map("TButton", background=[("active", "#45a049")])
    style.configure("TLabel", font=("Helvetica", 14), padding=10, background="#f0f0f0")
    root.configure(bg="#f0f0f0")

    # Adding Widgets
    header_frame = ttk.Frame(root, padding="10")
    header_frame.pack(pady=10)

    label = ttk.Label(header_frame, text="Expense Tracker", font=("Helvetica", 24), background="#f0f0f0")
    label.pack()

    button_frame = ttk.Frame(root, padding="10")
    button_frame.pack(pady=20)

    ttk.Button(button_frame, text="View Expenses", command=on_view_expenses, style="TButton").pack(pady=10, fill=tk.X)
    ttk.Button(button_frame, text="Add Expense", command=on_add_expense, style="TButton").pack(pady=10, fill=tk.X)
    ttk.Button(button_frame, text="Generate Report by Category", command=on_generate_report_by_category, style="TButton").pack(pady=10, fill=tk.X)
    ttk.Button(button_frame, text="Generate Report by Time", command=on_generate_report_by_time, style="TButton").pack(pady=10, fill=tk.X)
    ttk.Button(button_frame, text="Exit", command=root.quit, style="TButton").pack(pady=10, fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main()
