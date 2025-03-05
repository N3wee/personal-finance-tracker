Personal Finance Tracker
------------------------

### Overview

The Personal Finance Tracker is a Django-based web application designed to help users manage their financial transactions and budgets. It provides features for tracking income and expenses, setting budgets, generating financial reports, and ensuring secure user authentication and authorization. This project was developed as part of a Full Stack Development course, utilizing Python, Django, HTML, CSS, and JavaScript, with a focus on robust testing, deployment, and Agile methodologies.

### Features

*   **Transaction Management**: Add, edit, delete, and list transactions (income and expenses) with filtering and sorting options, including motivational quotes.
    
*   **Budget Management**: Create, edit, delete, and view budgets for different categories.
    
*   **Financial Dashboard**: A landing page displaying financial summaries, recent transactions, budgets, and a downloadable PDF report.
    
*   **User Authentication**: Secure login, registration, profile editing, and logout with role-based access (regular users and superusers/admin).
    
*   **Responsive Design**: Utilizes Bootstrap for a responsive and user-friendly interface.
    

### Technologies Used

*   **Backend**: Python 3.10, Django 4.2
    
*   **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
    
*   **Database**: SQLite (for development), PostgreSQL (for production via Heroku)
    
*   **Tools**: Git, GitHub, Heroku, VS Code
    
*   **Testing**: Django’s unittest framework, flake8 for linting, pycodestyle for style checking
    
*   **Dependencies**: whitenoise, reportlab for PDF generation, requests for API calls, widget-tweaks for form rendering
    

### Original Custom Models

This project includes at least one original custom model, Transaction, which tracks financial transactions with fields for title, amount, type (Income/Expense), category, date, and payment method. Additionally, the Budget model, created for this project, manages user budgets with fields for category, amount, start date, and end date. These models are markedly different from those in the To-Do app or Codestar Blog walkthrough projects, providing unique functionality for financial tracking and management, including CRUD operations accessible through the front end.

### Agile Methodology

*   Development followed Agile methodologies using a GitHub Project board to track tasks, bugs, and milestones, organized into To Do, In Progress, and Done columns. Each task is linked to specific user stories, ensuring comprehensive coverage of project requirements. The GitHub Project board is set to public visibility for assessment purposes.
    

### User Stories and Functionality

Below are user stories and descriptions of key pages, with corresponding screenshots linked for reference. These illustrate how the application meets user needs and provides front-end CRUD functionality without requiring admin panel access.

#### 1\. User Story: "As a user, I want to log in to track my finances securely."

*   **Functionality**: The login page allows users to authenticate with a username and password, redirecting them to the dashboard upon success. Unauthenticated users are redirected appropriately.
    
*   **Screenshot**: [Login Page](assets/login_page.png)
    

#### 2\. User Story: "As a user, I want to manage my transaction history to monitor my income and expenses."

*   **Functionality**: The transactions page lists all user transactions, allows filtering by type, category, and date, and provides options to add, edit, or delete transactions via front-end forms and UI elements (e.g., buttons). A motivational quote enhances user engagement.
    
*   **Screenshot**: [Transactions Page](assets/transactions_page.png)
    

#### 3\. User Story: "As a user, I want to set and manage budgets to plan my finances effectively."

*   **Functionality**: The budgets page enables users to create, edit, delete, and view budgets, with a table displaying category, amount, start date, and end date. Front-end forms and buttons provide CRUD functionality for budget management.
    
*   **Screenshot**: [Budgets Page](assets/budget_page.png)
    

#### 4\. User Story: "As a user, I want to view a financial dashboard to understand my financial status."

*   **Functionality**: The landing page displays total income, expenses, net balance, total budgets, and recent activity (transactions and budgets). Users can navigate to detailed views or download a PDF report summarizing their financial data.
    
*   **Screenshot**: [Dashboard Page](assets/landing_page.png)
    

#### 5\. User Story: "As a user, I want to edit my profile to update my details."

*   **Functionality**: The edit profile page allows authenticated users to modify their username and email, ensuring secure profile management through a front-end form.
    
*   **Screenshot**: [Edit Profile Page](assets/edit_profile_page.png)
    

#### 6\. User Story: "As a user, I want to generate a financial report to review my data."

*   **Functionality**: The downloadable PDF report, accessible from the dashboard, summarizes transactions, budgets, and financial metrics in a formatted document.
    
*   **Screenshot**: [PDF Report](assets/pdf_report.png)
    

### Installation

#### Prerequisites

*   Python 3.10 or higher
    
*   Pip (Python package manager)
    
*   Git
    
*   Virtualenv (optional but recommended)
    

#### Steps

1.  **Clone the Repository**:bashCollapseWrapCopygit clone https://github.com/your-username/personal-finance-tracker.gitcd personal-finance-tracker
    
2.  **Set Up a Virtual Environment**:bashCollapseWrapCopypython -m venv venvvenv\\Scripts\\activate _\# On Windows_source venv/bin/activate _\# On macOS/Linux_
    
3.  **Install Dependencies**:bashCollapseWrapCopypip install -r requirements.txt
    
4.  **Configure Settings**:
    
    *   Copy finance\_tracker/settings.py and update:
        
        *   DEBUG = True (for development, set to False for production).
            
        *   Update ALLOWED\_HOSTS (e.g., \['localhost', '127.0.0.1'\] for local, or your Heroku domain for production).
            
        *   Configure database settings in DATABASES (SQLite for local, PostgreSQL for Heroku).
            
5.  **Apply Migrations**:bashCollapseWrapCopypython manage.py migrate
    
6.  **Create a Superuser** (optional, for admin access):bashCollapseWrapCopypython manage.py createsuperuser
    
7.  **Run the Development Server**:bashCollapseWrapCopypython manage.py runserver
    
    *   Access the application at http://127.0.0.1:8000/.
        

### Usage

*   **Register/Login**: Use the login or registration pages to access the application securely.
    
*   **Manage Transactions and Budgets**: Navigate to the respective pages to perform CRUD operations via front-end forms and UI elements.
    
*   **View Dashboard**: Access the financial dashboard to monitor your financial status and download reports.
    
*   **Edit Profile**: Update your user details through the profile page.
    
*   **Admin Access**: Log in as a superuser to manage users and data via the Django admin interface (/admin).
    

### Deployment

*   **Heroku Deployment**:
    
    1.  Install the Heroku CLI and log in:bashCollapseWrapCopyheroku login
        
    2.  Create a Heroku app:bashCollapseWrapCopyheroku create n3-fintrack
        
    3.  Set environment variables in Heroku:bashCollapseWrapCopyheroku config:set SECRET\_KEY=your-secret-keyheroku config:set DEBUG=False
        
    4.  Push to Heroku:bashCollapseWrapCopygit push heroku main
        
    5.  Open the app:bashCollapseWrapCopyheroku open
        

### Testing

*   **Unit Tests**: The project includes unit tests using Django’s unittest framework, covering models, forms, views, and key functionality for transactions and budgets. A total of 31 tests are implemented, verifying authentication, authorization, and data integrity.
    
*   **Current Status**: As of March 4, 2025, four tests are failing due to unauthorized users receiving 302 redirects instead of the expected 403 Forbidden responses for editing and deleting transactions and budgets. These issues are noted for future resolution but remain unresolved due to time constraints. Other tests pass successfully, ensuring partial coverage of the application’s functionality.
    
*   **Code Quality Checks**: The codebase has been validated using standard Python tools to ensure adherence to coding standards, with adjustments made to address style and linting issues.
    

### Code Quality

*   The codebase has been reviewed to remove unnecessary comments and ensure compliance with Python coding standards. Docstrings have been added or updated in key files (e.g., transactions/views.py, transactions/models.py, transactions/forms.py) to improve documentation, following best practices. Other files, such as configuration and migration scripts, maintain minimal documentation as appropriate.
    

### Bugs

#### Solved Bugs

*   Addressed issues with URL redirection mismatches and test failures related to authentication in transactions/tests.py, ensuring tests align with application behavior.
    
*   Resolved linting warnings (e.g., unused imports, unused variables, and indentation issues) using automated tools and manual edits.
    

#### Known Issues

*   Four tests (test\_edit\_transaction\_non\_owner, test\_delete\_transaction\_non\_owner, test\_edit\_budget\_non\_owner, test\_delete\_budget\_non\_owner) fail because non-owners are redirected (302) instead of receiving a 403 Forbidden response. This requires updates to the authorization logic in transactions/views.py, but these changes are pending due to time constraints.
    

### Project Board

*   The project board on GitHub tracks tasks, bugs, and milestones, organized into To Do, In Progress, and Done columns, following Agile methodologies. Each task is linked to specific user stories, ensuring comprehensive coverage. The board is set to public visibility for assessment. Screenshots are included \[insert screenshot placeholder here\].
    

### Screenshots

*   [Login Page](assets/login_page.png): Shows the login interface for user authentication.
    
*   [Transactions Page](assets/transactions_page.png): Displays the transaction list with filtering options and CRUD functionality.
    
*   [Budgets Page](assets/budget_page.png): Illustrates the budget management interface with CRUD operations.
    
*   [Landing Page](assets/landing_page.png): Presents the financial dashboard with summaries and report download options.
    
*   [Edit Profile Page](assets/edit_profile_page.png): Shows the user profile editing form.
    
*   [PDF Report](assets/pdf_report.png): Displays the generated financial report in PDF format.
    

### Contributors

*   Nathan Sweeney 
    

### Acknowledgments

*   Thanks to course instructors and open-source communities for guidance and resources, including Django documentation and libraries such as reportlab and widget-tweaks.