# Personal Finance Tracker
A full-stack app to track income, expenses, and budgets securely.

## Purpose
Helps users manage finances with CRUD operations, filtering, and user authentication.

## User Stories
- As a user, I want to log in securely so that my financial data is protected.
  - [x] Login redirects to /transactions/
  - [x] Logout returns to /accounts/login/
  - [x] Non-logged-in users blocked
- As a user, I want to add transactions so I can track my income and expenses.
  - [x] Form saves title, amount (>0), type, category, date
  - [x] Transaction linked to my user
  - [x] Displays in list immediately
- (Add others similarly for Edit/Delete Transactions, Set Budgets, Filter Transactions)

## Setup
1. Clone: `git clone https://github.com/N3wee/personal-finance-tracker`
2. Install: `pip install -r requirements.txt`
3. Set up PostgreSQL: Update settings.py with DB credentials
4. Migrate: `python manage.py migrate`
5. Run: `python manage.py runserver`

## Agile Board
[Link to Project Board](https://github.com/users/N3wee/projects/1)

## Testing
- All 26 unit tests pass (run `python manage.py test`).