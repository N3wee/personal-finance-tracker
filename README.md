# Personal Finance Tracker
A full-stack app to track income, expenses, and budgets securely.

## Purpose
Helps users manage finances with CRUD operations, filtering, user authentication, and motivational quotes.

## User Stories
- As a user, I want to log in securely so that my financial data is protected.
  - [x] Login redirects to /transactions/
  - [x] Logout returns to /accounts/login/
  - [x] Non-logged-in users blocked
- As a user, I want to add transactions so I can track my income and expenses.
  - [x] Form saves title, amount (>0), type, category, date
  - [x] Transaction linked to my user
  - [x] Displays in list immediately
- As a user, I want to edit or delete my transactions so I can correct mistakes.
  - [x] Only I (or superuser) can edit/delete my transactions
  - [x] Changes reflect instantly in the list
  - [x] Non-owners get 403 error
- As a user, I want to set budgets so I can manage my spending.
  - [x] Form saves category, amount (>0), start/end dates
  - [x] Budget linked to my user
  - [x] Displays in budget list immediately
- As a user, I want to filter transactions so I can analyze my spending.
  - [x] Filter by type, category, date range
  - [x] Sort by date or amount (asc/desc)
  - [x] Updates list without errors
- As a user, I want to see a motivational quote on my dashboard so I feel encouraged to manage my finances.
  - [x] Fetches a random quote from an API (e.g., Quotable)
  - [x] Displays on transaction list or dashboard
  - [ ] Updates on page refresh

## Setup
1. Clone: `git clone https://github.com/N3wee/personal-finance-tracker`
2. Install: `pip install -r requirements.txt`
3. Set up PostgreSQL: Update settings.py with DB credentials (e.g., NAME: personal_finance_tracker, USER: postgres, PASSWORD: 626918, HOST: localhost, PORT: 5432)
4. Migrate: `python manage.py migrate`
5. Run: `python manage.py runserver`

## Deployment
- Deployed on Heroku (planned for Day 5).
- Steps:
  1. Install Heroku CLI: `brew install heroku` (Mac) or follow Heroku docs for Windows.
  2. Log in: `heroku login`
  3. Create app: `heroku create personal-finance-tracker`
  4. Add PostgreSQL add-on: `heroku addons:create heroku-postgresql:hobby-dev`
  5. Set environment variables (e.g., SECRET_KEY, DATABASE_URL) via `heroku config:set`.
  6. Deploy: `git push heroku main`
  7. Migrate: `heroku run python manage.py migrate`
  8. Test: Visit your Heroku app URL.

## Agile Board
[Link to Project Board](https://github.com/users/N3wee/projects/1)

## Testing
- All 26 unit tests pass (run `python manage.py test`).
- Tests cover models (Transaction, Budget), forms, and views (login, CRUD, permissions).
- JavaScript testing planned (e.g., Jest for quote display, optional for Merit).

## Data Schema
- **Transaction**:
  - user (ForeignKey to User)
  - title (CharField, max_length=255)
  - amount (DecimalField, max_digits=10, decimal_places=2)
  - transaction_type (CharField, choices=Income/Expense)
  - category (CharField, max_length=100)
  - date (DateField, default=today)
  - notes (TextField, optional)
  - recurring (BooleanField, default=False)
  - payment_method (CharField, choices=Cash/Card/Bank Transfer)
- **Budget**:
  - user (ForeignKey to User)
  - category (CharField, max_length=100)
  - amount (DecimalField, max_digits=10, decimal_places=2)
  - start_date (DateField, default=today)
  - end_date (DateField, optional)
  - notes (TextField, optional)