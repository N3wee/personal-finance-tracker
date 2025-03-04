# Personal Finance Tracker

## Description
Welcome to Personal Finance Tracker, a Django-based web application designed to help users manage their personal finances effectively. This project allows users to register, log in, track transactions and budgets, view a financial dashboard, and download detailed PDF reports of their financial data. The application is deployed on Heroku, providing a live, accessible platform for testing and use.

Here is the live version of my project: [https://n3-fintrack-b3c8348b4f8d.herokuapp.com/](https://n3-fintrack-b3c8348b4f8d.herokuapp.com/).

## Features
### Existing Features
- **User Authentication and Registration**: Users can create accounts, log in, log out, and edit their profiles securely using Django’s authentication system.
- **Transaction Management**: Users can add, view, edit, and delete financial transactions (Income or Expense) with details like title, amount, category, and date.
- **Budget Management**: Users can add, view, edit, and delete budgets with details like category, amount, start date, and end date.
- **Financial Dashboard**: Displays a summary of total income, total expenses, net balance, total budgets, recent transactions, and active budgets on the landing page.
- **Downloadable PDF Reports**: Users can download a PDF report summarizing their financial data, including totals, transactions, and budgets.
- **Responsive Design**: The application uses Bootstrap for a responsive layout, ensuring usability across desktops, tablets, and mobile devices.
- **Deployment on Heroku**: The application is live and accessible via Heroku, utilizing PostgreSQL for the database and WhiteNoise for static files.

### Future Features
- **Chart Visualizations**: Reintroduce charts (e.g., bar chart for monthly trends, pie charts for income/expense by category) with improved data handling and testing.
- **Search and Filter**: Add search functionality to filter transactions and budgets by date, category, or amount.
- **Notifications**: Implement email or in-app notifications for budget limits or upcoming budget expirations.
- **Mobile App Integration**: Develop a mobile app version or progressive web app for offline access.

## How to Use
Personal Finance Tracker is a web-based tool for managing personal finances, accessible via a browser. Users interact with the application through a user-friendly interface to perform CRUD operations on transactions and budgets, view financial summaries, and generate reports.

### Steps to Use:
1. **Register or Log In**: Create an account or log in with a test user (e.g., `testuser3` / `testpass123`) at `/accounts/login/`.
2. **View Dashboard**: Access the landing page (`/`) to see your financial summary, recent transactions, and active budgets.
3. **Manage Transactions**: Use “View Transactions” to add, edit, or delete transactions via `/transactions/`.
4. **Manage Budgets**: Use “View Budgets” to add, edit, or delete budgets via `/budgets/`.
5. **Download Report**: Click “Download Report” on the dashboard to generate and download a PDF of your financial data.
6. **Edit Profile**: Use “Edit Profile” to update your user details.

## Screenshots
- **Dashboard (Financial Summary and Recent Activity)**  
  [INSERT SCREENSHOT: Dashboard]
- **Transaction List**  
  [INSERT SCREENSHOT: Transaction List]
- **Add Transaction Form**  
  [INSERT SCREENSHOT: Add Transaction]
- **Budget List**  
  [INSERT SCREENSHOT: Budget List]
- **Add Budget Form**  
  [INSERT SCREENSHOT: Add Budget]
- **Download Report PDF (Sample)**  
  [INSERT SCREENSHOT: Download Report]

## Data Model
The application stores financial data in a PostgreSQL database with the following models:

### `User` (Django Auth Model)
- **Fields**: `username`, `email`, `password`, `is_active`, etc.

### `Transaction`
- **Fields**:
  - `user`: ForeignKey to `User` (the owner of the transaction).
  - `title`: CharField (transaction description, e.g., “Wage”).
  - `amount`: DecimalField (transaction amount, e.g., 2000.00).
  - `transaction_type`: CharField (Income or Expense).
  - `category`: CharField (e.g., “Wage,” “Food,” “Housing”).
  - `date`: DateField (transaction date).

### `Budget`
- **Fields**:
  - `user`: ForeignKey to `User` (the owner of the budget).
  - `category`: CharField (e.g., “Food,” “Housing”).
  - `amount`: DecimalField (budget amount, e.g., 500.00).
  - `start_date`: DateField (budget start date).
  - `end_date`: DateField (optional, budget end date).

## Bugs
### Solved Bugs
- **Template Syntax Error in `landing.html`**: Fixed `{% extends 'base.html' %}` ordering and removed charts due to time constraints, resolving `TemplateSyntaxError` and JavaScript errors.
- **Download Report `NameError`**: Resolved `NameError: name 'total_income' is not defined` in `download_report` by defining variables explicitly.
- **Authentication Redirection**: Fixed redirection to `/password_reset/login/` by ensuring `LOGIN_URL = '/accounts/login/'` and correcting URL patterns.

### Remaining Bugs
- There are no known remaining bugs at this stage.

## Validator Testing
- **PEP8 Compliance**: The code was checked for PEP8 compliance using `pycodestyle` or `flake8`, with minor formatting adjustments made (e.g., line lengths, indentation).
- **HTML/CSS Validation**: Bootstrap and custom HTML/CSS were validated using W3C validators, ensuring no major issues.
- **JavaScript Validation**: Chart.js (removed for simplicity) and custom JavaScript were tested for syntax, though charts are no longer included.

## Deployment
This project was deployed on Heroku for public access.

### Steps for Deployment:
1. Fork or clone this repository:
   ```bash
   git clone https://github.com/your-username/personal-finance-tracker.git# Personal Finance Tracker

## Description
Welcome to Personal Finance Tracker, a Django-based web application designed to help users manage their personal finances effectively. This project allows users to register, log in, track transactions and budgets, view a financial dashboard, and download detailed PDF reports of their financial data. The application is deployed on Heroku, providing a live, accessible platform for testing and use.

Here is the live version of my project: [https://n3-fintrack-b3c8348b4f8d.herokuapp.com/](https://n3-fintrack-b3c8348b4f8d.herokuapp.com/).

## Features
### Existing Features
- **User Authentication and Registration**: Users can create accounts, log in, log out, and edit their profiles securely using Django’s authentication system.
- **Transaction Management**: Users can add, view, edit, and delete financial transactions (Income or Expense) with details like title, amount, category, and date.
- **Budget Management**: Users can add, view, edit, and delete budgets with details like category, amount, start date, and end date.
- **Financial Dashboard**: Displays a summary of total income, total expenses, net balance, total budgets, recent transactions, and active budgets on the landing page.
- **Downloadable PDF Reports**: Users can download a PDF report summarizing their financial data, including totals, transactions, and budgets.
- **Responsive Design**: The application uses Bootstrap for a responsive layout, ensuring usability across desktops, tablets, and mobile devices.
- **Deployment on Heroku**: The application is live and accessible via Heroku, utilizing PostgreSQL for the database and WhiteNoise for static files.

### Future Features
- **Chart Visualizations**: Reintroduce charts (e.g., bar chart for monthly trends, pie charts for income/expense by category) with improved data handling and testing.
- **Search and Filter**: Add search functionality to filter transactions and budgets by date, category, or amount.
- **Notifications**: Implement email or in-app notifications for budget limits or upcoming budget expirations.
- **Mobile App Integration**: Develop a mobile app version or progressive web app for offline access.

## How to Use
Personal Finance Tracker is a web-based tool for managing personal finances, accessible via a browser. Users interact with the application through a user-friendly interface to perform CRUD operations on transactions and budgets, view financial summaries, and generate reports.

### Steps to Use:
1. **Register or Log In**: Create an account or log in with a test user (e.g., `testuser3` / `testpass123`) at `/accounts/login/`.
2. **View Dashboard**: Access the landing page (`/`) to see your financial summary, recent transactions, and active budgets.
3. **Manage Transactions**: Use “View Transactions” to add, edit, or delete transactions via `/transactions/`.
4. **Manage Budgets**: Use “View Budgets” to add, edit, or delete budgets via `/budgets/`.
5. **Download Report**: Click “Download Report” on the dashboard to generate and download a PDF of your financial data.
6. **Edit Profile**: Use “Edit Profile” to update your user details.

## Screenshots
- **Dashboard (Financial Summary and Recent Activity)**  
  [INSERT SCREENSHOT: Dashboard]
- **Transaction List**  
  [INSERT SCREENSHOT: Transaction List]
- **Add Transaction Form**  
  [INSERT SCREENSHOT: Add Transaction]
- **Budget List**  
  [INSERT SCREENSHOT: Budget List]
- **Add Budget Form**  
  [INSERT SCREENSHOT: Add Budget]
- **Download Report PDF (Sample)**  
  [INSERT SCREENSHOT: Download Report]

## Data Model
The application stores financial data in a PostgreSQL database with the following models:

### `User` (Django Auth Model)
- **Fields**: `username`, `email`, `password`, `is_active`, etc.

### `Transaction`
- **Fields**:
  - `user`: ForeignKey to `User` (the owner of the transaction).
  - `title`: CharField (transaction description, e.g., “Wage”).
  - `amount`: DecimalField (transaction amount, e.g., 2000.00).
  - `transaction_type`: CharField (Income or Expense).
  - `category`: CharField (e.g., “Wage,” “Food,” “Housing”).
  - `date`: DateField (transaction date).

### `Budget`
- **Fields**:
  - `user`: ForeignKey to `User` (the owner of the budget).
  - `category`: CharField (e.g., “Food,” “Housing”).
  - `amount`: DecimalField (budget amount, e.g., 500.00).
  - `start_date`: DateField (budget start date).
  - `end_date`: DateField (optional, budget end date).

## Bugs
### Solved Bugs
- **Template Syntax Error in `landing.html`**: Fixed `{% extends 'base.html' %}` ordering and removed charts due to time constraints, resolving `TemplateSyntaxError` and JavaScript errors.
- **Download Report `NameError`**: Resolved `NameError: name 'total_income' is not defined` in `download_report` by defining variables explicitly.
- **Authentication Redirection**: Fixed redirection to `/password_reset/login/` by ensuring `LOGIN_URL = '/accounts/login/'` and correcting URL patterns.

### Remaining Bugs
- There are no known remaining bugs at this stage.

## Validator Testing
- **PEP8 Compliance**: The code was checked for PEP8 compliance using `pycodestyle` or `flake8`, with minor formatting adjustments made (e.g., line lengths, indentation).
- **HTML/CSS Validation**: Bootstrap and custom HTML/CSS were validated using W3C validators, ensuring no major issues.
- **JavaScript Validation**: Chart.js (removed for simplicity) and custom JavaScript were tested for syntax, though charts are no longer included.

## Deployment
This project was deployed on Heroku for public access.

### Steps for Deployment:
1. Fork or clone this repository:
   ```bash
   git clone https://github.com/your-username/personal-finance-tracker.git
   
2.  Navigate to the project directory:

    bash

    CollapseWrapCopy

    `cd personal-finance-tracker`

3.  Create a virtual environment and activate it:

    bash

    CollapseWrapCopy

    `python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate`

5.  Install dependencies:

    bash

    CollapseWrapCopy

    `pip install -r requirements.txt`

7.  Set up environment variables (create a .env file):

    text

    CollapseWrapCopy

    `SECRET_KEY=your-secret-key DEBUG=True\
    DATABASE_URL=your-postgres-url # For local PostgreSQL or Heroku PostgreSQL`

9.  Apply migrations and create a superuser:

    bash

    CollapseWrapCopy

    `python manage.py migrate python manage.py createsuperuser`

11. Deploy to Heroku:

    -   Create a Heroku app:

        bash

        CollapseWrapCopy

        `heroku create n3-fintrack-b3c8348b4f8d`

    -   Set buildpacks for Python and Node.js:

        bash

        CollapseWrapCopy

        `heroku buildpacks:add heroku/python heroku buildpacks:add heroku/nodejs`

    -   Push to Heroku:

        bash

        CollapseWrapCopy

        `git push heroku main`

    -   Run migrations and collect static files:

        bash

        CollapseWrapCopy

        `heroku run "python manage.py migrate" heroku run "python manage.py collectstatic --noinput"`

    -   Restart the dyno:

        bash

        CollapseWrapCopy

        `heroku ps:restart web --app n3-fintrack`

13. Access the application at https://n3-fintrack-b3c8348b4f8d.herokuapp.com/.

Testing
-------

### Manual Testing

-   **User Authentication**: Verified registration, login, logout, and profile editing work correctly with testuser3.

-   **Transaction Management**: Tested adding, viewing, editing, and deleting transactions, ensuring data persistence and validation.

-   **Budget Management**: Tested adding, viewing, editing, and deleting budgets, ensuring data consistency.

-   **Dashboard**: Confirmed the landing page displays financial summary, recent transactions, and active budgets for testuser3.

-   **Download Report**: Verified the PDF report generates correctly with financial data, transactions, and budgets.

-   **Responsive Design**: Tested the layout on desktop, tablet, and mobile devices using browser developer tools.

### Automated Testing

-   Unit tests could be added for models, views, and forms (future enhancement for Merit/Distinction).

Credits
-------

-   **Django**: For the core framework and authentication system.

-   **Bootstrap**: For responsive design and styling.

-   **ReportLab**: For generating PDF reports.

-   **PostgreSQL**: For the database backend.

-   **WhiteNoise**: For serving static files on Heroku.

-   **xAI (Grok 3)**: For guidance and code assistance throughout development.

-   **Code Institute**: For project templates and learning resources.

License
-------

MIT License (or specify your license).

Contributors
------------

-   Nathan Sweeney
