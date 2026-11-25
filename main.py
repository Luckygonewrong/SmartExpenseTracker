from datetime import datetime

from storage import (
    CATEGORIES,
    load_expenses,
    save_expenses,
    load_budget,
    save_budget,
)
from analytics import (
    current_month_total,
    check_budget_alert,
    print_expenses_table,
    print_category_summary,
    filter_expenses,
)


def get_positive_amount(prompt):
    """Keep asking until the user enters a valid number > 0."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  [!] Please enter an amount greater than 0.")
            else:
                return round(value, 2)
        except ValueError:
            print("  [!] Invalid input. Please enter numbers only (e.g., 150 or 49.50).")


def choose_category():
    """Display category choices and return the selected category name."""
    print("\nSelect a Category:")
    for index, category in enumerate(CATEGORIES, start=1):
        print(f"  {index}. {category}")

    while True:
        try:
            choice = int(input("Enter category number: "))
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            print(f"  [!] Choose a number between 1 and {len(CATEGORIES)}.")
        except ValueError:
            print("  [!] Invalid input. Enter a number.")


def add_expense(expenses, budget):
    """Option 1: Add a new expense and save immediately."""
    print("\n--- Add New Expense ---")
    category = choose_category()

    while True:
        description = input("Enter short description (e.g., Bus ticket, Lunch): ").strip()
        if description:
            break
        print("  [!] Description cannot be empty.")

    amount = get_positive_amount("Enter amount (Rs.): ")
    today = datetime.now().strftime("%Y-%m-%d")

    expenses.append({
        "date": today,
        "category": category,
        "description": description,
        "amount": amount,
    })
    save_expenses(expenses)

    print("\n[OK] Expense saved successfully!")
    check_budget_alert(current_month_total(expenses), budget)


def search_expenses(expenses):
    """Option 4: Search expenses by keyword or category."""
    print("\n--- Search / Filter Expenses ---")
    if not expenses:
        print("  No expenses to search.")
        return

    keyword = input("Enter keyword, category, or date (YYYY-MM-DD): ").strip()
    if not keyword:
        print("  [!] Search term cannot be empty.")
        return

    matches = filter_expenses(expenses, keyword)
    if not matches:
        print(f"  No expenses matched '{keyword}'.")
    else:
        print(f"\nFound {len(matches)} matching record(s):")
        print_expenses_table(matches)


def delete_expense(expenses):
    """Option 5: Delete an expense by ID."""
    print("\n--- Delete an Expense ---")
    if not expenses:
        print("  No expenses to delete.")
        return

    print_expenses_table(expenses)
    try:
        choice = int(input("Enter the ID to delete (or 0 to cancel): "))
        if choice == 0:
            print("  Deletion cancelled.")
            return
        if 1 <= choice <= len(expenses):
            removed = expenses.pop(choice - 1)
            save_expenses(expenses)
            print(f"  [OK] Deleted '{removed['description']}' (Rs. {removed['amount']:.2f}).")
        else:
            print("  [!] Invalid ID.")
    except ValueError:
        print("  [!] Invalid input. Please enter a number.")


def set_budget():
    """Option 6: Set or update the monthly budget."""
    print("\n--- Set Monthly Budget ---")
    new_budget = get_positive_amount("Enter your monthly budget (Rs.): ")
    save_budget(new_budget)
    print(f"  [OK] Monthly budget updated to Rs. {new_budget:.2f}")
    return new_budget


def main():
    expenses = load_expenses()
    budget = load_budget()

    print("=" * 45)
    print("   SMART EXPENSE & BUDGET TRACKER")
    print("=" * 45)

    while True:
        print("\nMAIN MENU:")
        print("  1. Add New Expense")
        print("  2. View All Expenses")
        print("  3. Category Summary & Budget Report")
        print("  4. Search / Filter Expenses")
        print("  5. Delete an Expense")
        print("  6. Set / Update Monthly Budget")
        print("  7. Exit")

        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
            add_expense(expenses, budget)
        elif choice == "2":
            print("\n--- All Recorded Expenses ---")
            print_expenses_table(expenses)
        elif choice == "3":
            print("\n--- Category-Wise Summary & Budget Report ---")
            print_category_summary(expenses, budget)
        elif choice == "4":
            search_expenses(expenses)
        elif choice == "5":
            delete_expense(expenses)
        elif choice == "6":
            budget = set_budget()
        elif choice == "7":
            print("\nGoodbye! Your expenses are safely saved in expenses.csv.")
            break
        else:
            print("  [!] Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()