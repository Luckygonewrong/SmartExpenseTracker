# SmartExpenseTracker
python project
# Smart Expense & Budget Tracker

A Python command-line application built for **Computational Thinking and Programming (2026CSAE100)** to help students record daily expenses, analyze category-wise spending, and monitor monthly budget limits.

## Features
- **Add Expenses:** Records category, description, amount, and automatic date (`YYYY-MM-DD`) with input validation.
- **Persistent File Storage:** Saves all expenses in `expenses.csv` and monthly budget in `budget.txt`.
- **Category Summary & Visual Bars:** Displays spending per category, percentages, and ASCII bar charts.
- **Smart Budget Alerts:** Warns at 80% budget usage and alerts when spending exceeds 100%.
- **Search & Delete:** Filter records by keyword, category, or date, and delete entries safely by ID.

## Project Structure
- `main.py` — Interactive menu loop and input validation.
- `storage.py` — CSV and text file read/write operations.
- `analytics.py` — Totals, category breakdown, filtering, and budget alerts.
- `expenses.csv` — Stored expense records.
- `budget.txt` — Stored monthly budget limit.

## Python Concepts Demonstrated
- Tuples, Lists, and Dictionaries
- Conditional Statements (`if / elif / else`)
- Loops (`while` and `for`)
- Modular Functions across multiple files
- File Handling (`csv` and `open`)
- Exception Handling (`try / except`)

## How to Run
Ensure Python 3 is installed, then run:
```bash
python main.py