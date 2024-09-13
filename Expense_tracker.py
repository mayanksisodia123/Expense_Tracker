import json
import argparse
from datetime import datetime

# Load expenses from expenses.json
def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save expenses to expenses.json
def save_expenses(expenses):
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)

# Load budget from budget.json
def load_budget():
    try:
        with open("budget.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"budget": 0}

# Save budget to budget.json
def save_budget(budget):
    with open("budget.json", "w") as file:
        json.dump(budget, file, indent=4)

# Add a new expense
def add_expense(description, amount, category):
    expenses = load_expenses()
    expense = {
        "id": len(expenses) + 1,
        "date": str(datetime.now().date()),
        "description": description,
        "amount": amount,
        "category": category
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {expense['id']})")

# Delete an expense by id
def delete_expense(expense_id):
    expenses = load_expenses()
    filtered_expenses = [expense for expense in expenses if expense['id'] != expense_id]
    
    if len(filtered_expenses) == len(expenses):
        print(f"Expense with ID {expense_id} not found.")
    else:
        save_expenses(filtered_expenses)
        print(f"Expense with ID {expense_id} deleted successfully.")

# List all expenses
def list_expenses(category=None, month=None):
    expenses = load_expenses()
    filtered_expenses = expenses

    if category:
        filtered_expenses = [e for e in expenses if e['category'].lower() == category.lower()]

    if month:
        filtered_expenses = [e for e in filtered_expenses if datetime.strptime(e['date'], '%Y-%m-%d').month == month]

    if not filtered_expenses:
        print("No expenses found.")
        return

    print(f"{'ID':<5}{'Date':<12}{'Description':<20}{'Amount':<10}{'Category':<10}")
    for expense in filtered_expenses:
        print(f"{expense['id']:<5}{expense['date']:<12}{expense['description']:<20}{expense['amount']:<10}{expense['category']:<10}")

# View summary of total expenses
def view_summary(month=None, category=None):
    expenses = load_expenses()
    
    if month:
        expenses = [e for e in expenses if datetime.strptime(e['date'], '%Y-%m-%d').month == month]
        
    if category:
        expenses = [e for e in expenses if e['category'].lower() == category.lower()]

    total = sum(expense['amount'] for expense in expenses)
    print(f"Total expenses: ${total:.2f}")

# Set budget
def set_budget(amount):
    budget = {"budget": amount}
    save_budget(budget)
    print(f"Budget set to ${amount:.2f}")

# Check if budget is exceeded
def check_budget():
    expenses = load_expenses()
    budget = load_budget()["budget"]
    total_expenses = sum(expense['amount'] for expense in expenses)

    if total_expenses > budget:
        print(f"Warning: You have exceeded your budget by ${total_expenses - budget:.2f}")
    else:
        print(f"You are within your budget. Remaining budget: ${budget - total_expenses:.2f}")

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Add expense command
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", required=True, type=float)
    add_parser.add_argument("--category", required=True)

    # List expenses command
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--category", required=False)
    list_parser.add_argument("--month", type=int, required=False)

    # Summary command
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month", type=int, required=False)
    summary_parser.add_argument("--category", required=False)

    # Set budget command
    set_budget_parser = subparsers.add_parser("set-budget")
    set_budget_parser.add_argument("--amount", required=True, type=float)

    # Check budget command
    subparsers.add_parser("check-budget")

    # Delete expense command
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", required=True, type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.description, args.amount, args.category)
    elif args.command == "list":
        list_expenses(args.category, args.month)
    elif args.command == "summary":
        view_summary(args.month, args.category)
    elif args.command == "set-budget":
        set_budget(args.amount)
    elif args.command == "check-budget":
        check_budget()
    elif args.command == "delete":
        delete_expense(args.id)

if __name__ == "__main__":
    main()
