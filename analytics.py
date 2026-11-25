from datetime import datetime


def calculate_total(expenses):
    """Return the sum of all expense amounts."""
    total = 0.0
    for item in expenses:
        total += item["amount"]
    return total


def current_month_total(expenses):
    """Return total spent in the current month (dates are YYYY-MM-DD)."""
    month = datetime.now().strftime("%Y-%m")
    total = 0.0
    for item in expenses:
        if item["date"].startswith(month):
            total += item["amount"]
    return total


def check_budget_alert(total_spent, budget):
    """Display budget status and warnings if spending is >= 80% or over 100%."""
    if budget <= 0:
        print("  Monthly Budget : Not set yet (use Option 6 to set one).")
        return

    remaining = budget - total_spent
    percent_used = (total_spent / budget) * 100

    print(f"  Monthly Budget : Rs. {budget:.2f}")
    print(f"  Spent (month)  : Rs. {total_spent:.2f} ({percent_used:.1f}%)")

    if remaining < 0:
        print(f"  [ALERT] Budget exceeded by Rs. {abs(remaining):.2f}!")
    elif percent_used >= 80:
        print(
            f"  [WARNING] You have used {percent_used:.1f}% of your budget. "
            f"Only Rs. {remaining:.2f} left!"
        )
    else:
        print(f"  Remaining      : Rs. {remaining:.2f} (On track)")


def print_expenses_table(expenses):
    """Display a formatted table of expenses and their total."""
    if not expenses:
        print("  No expenses recorded yet.")
        return

    print("-" * 68)
    print(f"{'ID':<4} {'Date':<12} {'Category':<16} {'Description':<22} {'Amount':>10}")
    print("-" * 68)

    for idx, item in enumerate(expenses, start=1):
        desc = item["description"][:20]
        print(
            f"{idx:<4} {item['date']:<12} {item['category']:<16} "
            f"{desc:<22} {item['amount']:>10.2f}"
        )

    print("-" * 68)
    print(f"{'TOTAL':<56} Rs. {calculate_total(expenses):>7.2f}")
    print("-" * 68)


def print_category_summary(expenses, budget):
    """Group spending by category, show percentages/bars, and check budget."""
    if not expenses:
        print("  No expenses to summarize yet.")
        check_budget_alert(0.0, budget)
        return

    category_totals = {}
    for item in expenses:
        cat = item["category"]
        category_totals[cat] = category_totals.get(cat, 0.0) + item["amount"]

    grand_total = calculate_total(expenses)

    print("-" * 65)
    for cat, amt in category_totals.items():
        pct = (amt / grand_total) * 100
        bar = "#" * int(pct // 5)  # 1 '#' per 5%
        print(f"  {cat:<16} | Rs. {amt:>8.2f} ({pct:>5.1f}%) | {bar}")
    print("-" * 65)

    check_budget_alert(current_month_total(expenses), budget)


def filter_expenses(expenses, keyword):
    """Return expenses matching a keyword in description, category, or date."""
    keyword = keyword.strip().lower()
    matches = []
    for item in expenses:
        if (
            keyword in item["description"].lower()
            or keyword in item["category"].lower()
            or keyword in item["date"]
        ):
            matches.append(item)
    return matches