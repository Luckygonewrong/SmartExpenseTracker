import csv
import os

# Fixed categories stored as a Tuple
CATEGORIES = (
    "Food",
    "Transport",
    "Books & Study",
    "Entertainment",
    "Utilities",
    "Other",
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPENSE_FILE = os.path.join(BASE_DIR, "expenses.csv")
BUDGET_FILE = os.path.join(BASE_DIR, "budget.txt")


def load_expenses():
    """Load saved expenses from expenses.csv into a list of dictionaries."""
    expenses = []
    if not os.path.exists(EXPENSE_FILE):
        return expenses

    with open(EXPENSE_FILE, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                expenses.append({
                    "date": row["date"],
                    "category": row["category"],
                    "description": row["description"],
                    "amount": float(row["amount"]),
                })
            except (ValueError, KeyError):
                continue
    return expenses


def save_expenses(expenses):
    """Write all expenses back to expenses.csv."""
    with open(EXPENSE_FILE, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["date", "category", "description", "amount"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)


def load_budget():
    """Load monthly budget from budget.txt (returns 0.0 if missing/invalid)."""
    if not os.path.exists(BUDGET_FILE):
        return 0.0
    try:
        with open(BUDGET_FILE, mode="r", encoding="utf-8") as file:
            return float(file.read().strip())
    except ValueError:
        return 0.0


def save_budget(budget):
    """Save monthly budget to budget.txt."""
    with open(BUDGET_FILE, mode="w", encoding="utf-8") as file:
        file.write(f"{budget:.2f}")