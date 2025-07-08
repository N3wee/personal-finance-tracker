# Personal Finance Tracker

The Personal Finance Tracker is a full-stack web application built with Django that allows users to manage their personal finances in a structured and secure environment. Authenticated users can track income and expenses, set budgets, and generate downloadable financial summaries.

The application is designed with simplicity and functionality in mind. It supports user authentication, enforces ownership-based access to financial data, and includes PDF export functionality for records. This project was developed as part of a portfolio submission to demonstrate practical Django development skills and adherence to secure coding practices.

## Key Features

- **User Authentication**
  - Secure registration, login, and logout functionality using Django’s built-in authentication system.
  - Passwords are hashed and protected using Django’s security framework.

- **Transaction Management**
  - Add, edit, and delete income and expense entries.
  - Transactions are categorized by type, date, amount, and payment method.
  - Data is scoped per user—users can only access and modify their own financial records.

- **Budget Planning**
  - Users can define budget categories with allocated amounts.
  - Budget entries can be created, edited, and deleted securely.

- **PDF Export**
  - Users can download their transactions as a formatted PDF summary for offline record-keeping.

- **Responsive UI**
  - Clean and mobile-friendly user interface using HTML5, CSS3, and Bootstrap.
  - Custom templates and form rendering using `django-widget-tweaks`.

- **Security & Permissions**
  - Ownership checks to prevent unauthorized access to financial records.
  - Only authenticated users can interact with the app's core features.
  - Proper use of HTTP response codes for unauthorized attempts (e.g., HTTP 403).

- **Testing**
  - Includes automated unit tests for critical views and permission logic.
  - Manual testing was conducted for form validation, CRUD operations, and login/logout workflows.

- **Heroku Deployment**
  - Fully deployed and accessible via Heroku with persistent PostgreSQL storage.
  - Environment-specific settings handled using `.env` and `django-environ`.

## Technologies Used

### Frameworks & Libraries
- **[Django 5.1.6](https://www.djangoproject.com/)** – High-level Python web framework for rapid development.
- **[Bootstrap 5](https://getbootstrap.com/)** – Responsive frontend framework for styling and layout.
- **[dj-database-url](https://github.com/jacobian/dj-database-url)** – Simplified database configuration for deployment.
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** – Loads environment variables from a `.env` file.
- **[whitenoise](https://whitenoise.evans.io/)** – Serves static files efficiently in production.
- **[django-widget-tweaks](https://pypi.org/project/django-widget-tweaks/)** – Allows flexible customization of form fields in templates.

### Database
- **[PostgreSQL](https://www.postgresql.org/)** – Relational database used in both local and Heroku environments.

### Deployment
- **[Heroku](https://www.heroku.com/)** – Cloud platform used for hosting the live application.

### Tools
- **[Git](https://git-scm.com/)** – Version control.
- **[GitHub](https://github.com/)** – Code hosting and collaboration.
- **[Flake8](https://flake8.pycqa.org/)** – Enforces Python style guide compliance.
- **[pytest](https://docs.pytest.org/)** – Framework for writing and running tests.

## Installation & Setup

Follow the steps below to run the project locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/N3wee/personal-finance-tracker.git
cd personal-finance-tracker
```

### 2. Set Up Virtual Environment
Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add the following:

```ini
SECRET_KEY=your-django-secret-key
DEBUG=True
```

You can generate a new secret key using:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. Set Up the Database
Ensure PostgreSQL is running and then apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

Then visit http://127.0.0.1:8000/ in your browser.

## Features

This Personal Finance Tracker provides users with a streamlined way to manage their income, expenses, and budgets. The key features include:

### ✅ Authentication
- Secure user registration and login system
- Login required for accessing and managing personal financial data
![Authentication - wireframe-login.png](assets/wireframe-login.png)
![Authentication - login_page.png](assets/login_page.png)

### ✅ Transactions Management
- Add income or expense transactions with details like category, date, amount, and payment method
- Edit or delete existing transactions
- Transactions are displayed in a chronological list
![Transactions - wireframe-transactions.png](assets/wireframe-transactions.png)
![Transactions - transaction_page.png](assets/transaction_page.png)

### ✅ Budgeting
- Create budgets for specific categories and date ranges
- View and manage multiple budgets
- Prevent unauthorized access or editing of budgets by other users
![Budgeting - budget_page.png](assets/budget_page.png)

### ✅ PDF Export
- Generate and download PDF reports of transactions for offline records or printing
![PDF Export - pdf_report.png](assets/pdf_report.png)

### ✅ Responsive User Interface
- Clean, user-friendly interface built with HTML/CSS and Django templating
- Mobile-responsive layout for easy access across devices
![UI - landing_page.png](assets/landing_page.png)
![UI - edit_profile_page.png](assets/edit_profile_page.png)

### ✅ Error Handling & Logging
- Graceful error handling with appropriate permission checks
- Logging for permission errors and failed form submissions

### ✅ Security Best Practices
- Secret key and environment variables handled through `.env` file
- DEBUG mode disabled in production

## 6. Testing & Code Quality

### ✅ Automated Tests

The project includes a suite of unit tests to verify core functionality and permission enforcement:

- **Transactions**: Create, edit, delete, and access control
- **Budgets**: Create, edit, delete, and access control
- **Authentication**: Access to protected routes is restricted to logged-in users

Run all tests using:

```bash
python manage.py test
```

These tests are essential to ensure that users can only modify their own data, and that the application behaves as expected.

---

### ✅ Code Linting

The codebase follows Python best practices and is linted using:

- **flake8** – For general style guide enforcement (PEP8)
- **isort** – For automatic sorting of imports
- **black** – For code formatting consistency

To check the code style manually:

```bash
flake8 --max-line-length=120 --exclude=venv
```

Linting helps maintain a clean, readable, and professional codebase.

---

### ✅ Environment Separation

Environment variables such as `SECRET_KEY` and `DEBUG` are loaded via a `.env` file and never hardcoded in the codebase. This prevents sensitive data from being exposed.

---

### ✅ Git Best Practices

- Pre-commit hooks (optional) were used during development to auto-check for formatting issues and common errors.
- `.gitignore` prevents committing virtual environments, environment files, and other unnecessary artifacts.

## Deployment

This project is deployed on [Heroku](https://www.heroku.com/) using the **Heroku Python Buildpack**. Below are the deployment steps and configurations used.

### ⚙️ Deployment Steps

1. **Create a Heroku App**
   ```bash
   heroku create your-app-name
   ```

2. **Add Heroku Remote (if not already added)**
   ```bash
   heroku git:remote -a your-app-name
   ```

3. **Set Config Vars**
   Go to your Heroku Dashboard > Settings > Reveal Config Vars, and add:

   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: your Heroku app URL (e.g. `your-app-name.herokuapp.com`)
   - Any other variables from your `.env` file

4. **Install Heroku CLI (if not installed)**  
   [Heroku CLI Download](https://devcenter.heroku.com/articles/heroku-cli)

5. **Push to Heroku**
   ```bash
   git push heroku main
   ```

6. **Run Database Migrations on Heroku**
   ```bash
   heroku run python manage.py migrate
   ```

7. **Create a Superuser (Optional)**
   ```bash
   heroku run python manage.py createsuperuser
   ```

8. **Open the Live App**
   ```bash
   heroku open
   ```

### 📁 Procfile

Ensure your project contains a `Procfile` with the following content:
```procfile
web: gunicorn finance_tracker.wsgi
```

### 📂 Static Files

The project uses **Whitenoise** for serving static files in production. Make sure you’ve run:
```bash
python manage.py collectstatic
```

## Testing

Thorough testing was conducted to ensure application reliability and security, particularly around user permissions and data ownership. The following test strategies and tools were used:

### 1. Django Unit Tests

The project includes a comprehensive suite of unit tests for key views and functionality.

To run tests locally:

```bash
python manage.py test
```

#### Key Areas Tested:
- **Transaction Tests:**
  - Authenticated vs unauthenticated access to transaction views
  - Owner vs non-owner access when editing and deleting transactions
- **Budget Tests:**
  - Authenticated creation of budgets
  - Permission-based editing and deletion of budgets
- **Access Control:**
  - Non-owners attempting to access protected data return proper `403 Forbidden` responses
  - Unauthorized users are redirected to login when required

### 2. Code Style Checks

To ensure code quality and readability, the following tools were used:

- **flake8**: For enforcing PEP8 standards and flagging syntax issues
- **black**: Auto-formatting code for consistency (locally run)
- **isort**: Ensures consistent import order (optional)

You can run `flake8` like this:

```bash
flake8 --max-line-length=120 --exclude=venv
```

No blocking lint errors were present in the final submitted version.

### 3. Manual Testing

Additional manual tests were performed, including:

- Form submissions with invalid data
- Login/logout functionality
- Permissions testing via multiple user accounts
- Application behaviour with and without authentication

### 4. Heroku Production Testing

The app was deployed to Heroku and tested to ensure:

- Environment variables are respected
- `DEBUG` is disabled in production
- `SECRET_KEY` is kept out of source code
- The production database is properly connected

> ✅ All tests passed and the deployed version functions as expected.


### 📚 Credits / Acknowledgements

This project was developed as part of a Django portfolio submission for educational purposes. The following resources and tools were instrumental in its development:

- [Django Documentation](https://docs.djangoproject.com/) – for framework guidance and best practices.
- [Bootstrap Documentation](https://getbootstrap.com/) – for responsive frontend components.
- [Heroku Documentation](https://devcenter.heroku.com/) – for deployment help and environment configuration.
- [Real Python Tutorials](https://realpython.com/tutorials/django/) – for inspiration and reference on Django patterns.
- [GitHub Copilot & ChatGPT](https://openai.com/chatgpt) – for development assistance and troubleshooting during coding and testing.
- Stack Overflow and Django Discord – for community support.

If any external code or references were adapted in the project, they were modified appropriately and acknowledged where used.


## 2. Possible Future Improvements

While the current version of the Personal Finance Tracker meets its core objectives, there are several enhancements and new features that could be explored in future iterations:

- **Recurring Transactions**  
  Add support for recurring income or expense entries (e.g., monthly rent, salary).

- **Data Visualization**  
  Integrate simple charts or graphs to visualize spending trends over time using libraries like Chart.js or D3.js.

- **Multi-Currency Support**  
  Enable users to manage transactions in different currencies with real-time exchange rate integration.

- **Tagging System**  
  Allow users to tag transactions (e.g., "holiday", "business") for better filtering and analysis.

- **Enhanced Budget Alerts**  
  Notify users when their spending nears or exceeds budget thresholds via email or in-app alerts.

- **Search & Filters**  
  Add dynamic filtering and search functionality for easier transaction lookup.

- **Two-Factor Authentication**  
  Improve account security with optional two-factor authentication (2FA) during login.

These improvements could significantly enhance user experience, accessibility, and functionality.


## 3. License

This project is intended for **educational purposes only** and does not carry a formal software license.  
It was developed as part of a portfolio submission to demonstrate Django development proficiency.

---

## 4. Contact / Author Info

**Author**: Nathan Sweeney  
**GitHub**: [github.com/N3wee](https://github.com/N3wee)  

For any questions regarding this project, feel free to reach out via GitHub or email.