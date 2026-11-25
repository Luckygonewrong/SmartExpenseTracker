"""Web version of the Smart Expense Tracker.

Uses only Python's built-in http.server (no installs needed).
Reuses the same storage.py and analytics.py as the command-line app,
so both versions read and write the same expenses.csv and budget.txt.

Run:  python web.py   then open http://localhost:8000
"""

import json
import os
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

from storage import CATEGORIES, load_expenses, save_expenses, load_budget, save_budget
from analytics import calculate_total, current_month_total

PORT = 8000
PAGE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")


def build_report():
    """Collect everything the web page needs into one dictionary."""
    expenses = load_expenses()
    budget = load_budget()

    category_totals = {}
    for item in expenses:
        cat = item["category"]
        category_totals[cat] = category_totals.get(cat, 0.0) + item["amount"]

    rows = []
    for idx, item in enumerate(expenses, start=1):
        row = dict(item)
        row["id"] = idx
        rows.append(row)

    return {
        "categories": list(CATEGORIES),
        "expenses": rows,
        "budget": budget,
        "total": calculate_total(expenses),
        "month_total": current_month_total(expenses),
        "category_totals": category_totals,
    }


class TrackerHandler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            with open(PAGE_FILE, "rb") as file:
                body = file.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/data":
            self.send_json(build_report())
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self.send_json({"error": "Invalid request"}, 400)
            return

        try:
            if self.path == "/api/add":
                self.add_expense(data)
            elif self.path == "/api/delete":
                self.delete_expense(data)
            elif self.path == "/api/budget":
                self.set_budget(data)
            else:
                self.send_json({"error": "Not found"}, 404)
                return
        except ValueError as error:
            self.send_json({"error": str(error)}, 400)
            return

        self.send_json(build_report())

    def add_expense(self, data):
        category = data.get("category")
        description = str(data.get("description", "")).strip()
        amount = float(data.get("amount", 0))

        if category not in CATEGORIES:
            raise ValueError("Please choose a valid category.")
        if not description:
            raise ValueError("Description cannot be empty.")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        expenses = load_expenses()
        expenses.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "category": category,
            "description": description,
            "amount": round(amount, 2),
        })
        save_expenses(expenses)

    def delete_expense(self, data):
        expenses = load_expenses()
        expense_id = int(data.get("id", 0))
        if not 1 <= expense_id <= len(expenses):
            raise ValueError("Invalid expense ID.")
        expenses.pop(expense_id - 1)
        save_expenses(expenses)

    def set_budget(self, data):
        budget = float(data.get("budget", 0))
        if budget <= 0:
            raise ValueError("Budget must be greater than 0.")
        save_budget(round(budget, 2))

    def log_message(self, format, *args):
        pass  # keep the terminal clean


def main():
    server = HTTPServer(("localhost", PORT), TrackerHandler)
    url = f"http://localhost:{PORT}"
    print(f"Smart Expense Tracker running at {url}  (press Ctrl+C to stop)")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped. Your expenses are saved in expenses.csv.")
        server.server_close()


if __name__ == "__main__":
    main()
