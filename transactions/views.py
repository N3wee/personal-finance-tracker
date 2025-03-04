from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import datetime
import logging
import requests
import os
from django.conf import settings  # Import settings to access TEMPLATES
from django.template.loader import get_template

from .models import Transaction, Budget
from .forms import TransactionForm, BudgetForm, CustomUserEditForm  # Import the new form

# Configure logging
logger = logging.getLogger(__name__)

def user_owns_object(user, obj):
    """Check if the user owns the object or is a superuser.

    Args:
        user: The Django User instance checking ownership.
        obj: The object (Transaction or Budget) to check ownership for.

    Returns:
        bool: True if the user is the owner or a superuser, False otherwise.
    """
    if obj is None:
        logger.error("Object is None in user_owns_object")
        return False
    owner = getattr(obj, 'user', None)
    if owner is None:
        logger.error(f"No user associated with object: {obj}")
        return False
    result = user.is_superuser or owner == user
    logger.debug(f"Checking ownership: User {user.username}, Object user {owner.username if owner else 'None'}, "
                 f"Object type {type(obj).__name__}, Object ID {obj.id if obj.id else 'None'}, Result {result}")
    return result

@login_required
def landing_page(request):
    """Render the financial dashboard for the authenticated user.

    Displays a summary of transactions, budgets, and financial metrics for the logged-in user.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response with financial data or error message if an exception occurs.
    """
    logger.debug("Rendering transactions/landing.html for user: %s", request.user.username)

    try:
        # Retrieve transactions for the logged-in user
        transactions = Transaction.objects.filter(user=request.user)

        # Calculate financial summary
        total_income = transactions.filter(transaction_type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = transactions.filter(transaction_type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
        net_balance = total_income - total_expenses
        total_budgets = Budget.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate monthly trends (last 6 months)
        today = datetime.date.today()
        six_months_ago = today - datetime.timedelta(days=180)
        monthly_income = transactions.filter(
            transaction_type='Income', date__gte=six_months_ago
        ).values('date__month').annotate(total=Sum('amount')).order_by('date__month')

        monthly_expenses = transactions.filter(
            transaction_type='Expense', date__gte=six_months_ago
        ).values('date__month').annotate(total=Sum('amount')).order_by('date__month')

        # Get income/expense by category (for pie charts)
        income_by_category = transactions.filter(transaction_type='Income').values('category').annotate(total=Sum('amount')).order_by('-total')
        expenses_by_category = transactions.filter(transaction_type='Expense').values('category').annotate(total=Sum('amount')).order_by('-total')

        # Get recent transactions and budgets (last 5)
        recent_transactions = transactions.order_by('-date')[:5] if transactions.exists() else []
        recent_budgets = Budget.objects.filter(user=request.user).order_by('-start_date')[:5] if Budget.objects.filter(user=request.user).exists() else []

        return render(request, 'transactions/landing.html', {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'total_budgets': total_budgets,
            'monthly_income': list(monthly_income),
            'monthly_expenses': list(monthly_expenses),
            'income_by_category': list(income_by_category),
            'expenses_by_category': list(expenses_by_category),
            'recent_transactions': recent_transactions,
            'recent_budgets': recent_budgets,
        })

    except Exception as e:
        logger.error(f"Error in landing_page: {str(e)}")
        return render(request, 'transactions/landing.html', {
            'error_message': "An error occurred while loading your dashboard.",
            'total_income': 0,
            'total_expenses': 0,
            'net_balance': 0,
            'total_budgets': 0,
            'monthly_income': [],
            'monthly_expenses': [],
            'income_by_category': [],
            'expenses_by_category': [],
            'recent_transactions': [],
            'recent_budgets': [],
        })

@login_required
def transaction_list(request):
    """Display a list of transactions for the authenticated user with filtering and sorting options.

    Supports filtering by transaction type, category, date range, and sorting by date or amount.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response with transaction list and filtering options, or redirect if unauthenticated.
    """
    transactions = Transaction.objects.filter(user=request.user)

    # Get filtering parameters from request
    transaction_type = request.GET.get('transaction_type')
    category = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    sort_by = request.GET.get('sort_by')

    # Apply filters
    if transaction_type in ['Income', 'Expense']:
        transactions = transactions.filter(transaction_type=transaction_type)

    if category:
        transactions = transactions.filter(category__icontains=category)

    if start_date:
        transactions = transactions.filter(date__gte=start_date)

    if end_date:
        transactions = transactions.filter(date__lte=end_date)

    # Apply sorting
    if sort_by == 'date_desc':
        transactions = transactions.order_by('-date')
    elif sort_by == 'date_asc':
        transactions = transactions.order_by('date')
    elif sort_by == 'amount_desc':
        transactions = transactions.order_by('-amount')
    elif sort_by == 'amount_asc':
        transactions = transactions.order_by('amount')

    # Fetch a motivational quote with fallback, bypassing SSL locally for testing
    quote = "Failed to load quote. Check your internet connection."
    try:
        # Try Quotable API first (motivational) with SSL bypass for local testing
        response = requests.get('https://api.quotable.io/random?tags=motivational', 
                             timeout=5, 
                             verify=False)  # Temporary local bypass
        logger.debug(f"Quotable API response status: {response.status_code}, JSON: {response.json()}")
        if response.status_code == 200:
            quote_data = response.json()
            quote = f'"{quote_data["content"]}" — {quote_data["author"]}'
        else:
            # Fallback to Kanye API if Quotable fails
            response = requests.get('https://api.kanye.rest/', timeout=5)
            logger.debug(f"Kanye API response status: {response.status_code}, JSON: {response.json()}")
            if response.status_code == 200:
                quote_data = response.json()
                quote = f'"{quote_data["quote"]}" — Kanye West'
    except requests.RequestException as e:
        logger.error(f"Failed to fetch quote: {e}")

    return render(request, 'transactions/transaction_list.html', {
        'transactions': transactions,
        'transaction_type': transaction_type,
        'category': category,
        'start_date': start_date,
        'end_date': end_date,
        'sort_by': sort_by,
        'quote': quote
    })

@login_required
def add_transaction(request):
    """Handle the addition of a new transaction for the authenticated user.

    Processes form submission, validates data, and redirects to the transaction list upon success.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered form page or redirect to transaction list on success.
    """
    logger.debug("Processing add_transaction request for user: %s", request.user.username)
    if request.method == "POST":
        logger.debug("Form submitted with data: %s", request.POST)
        form = TransactionForm(request.POST)
        if form.is_valid():
            logger.debug("Form is valid")
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            logger.debug(f"Transaction added: ID {transaction.id}, User {request.user.username}")
            return redirect('transaction_list')
        else:
            logger.error("Form errors for user %s: %s", request.user.username, form.errors)
            print(form.errors)  # Debug: Check terminal for errors
    else:
        logger.debug("Rendering empty form for user: %s", request.user.username)
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})

@login_required
def edit_transaction(request, transaction_id):
    """Handle the editing of an existing transaction for the authenticated user.

    Checks ownership, processes form submission, validates data, and redirects to the transaction list on success.

    Args:
        request: The HTTP request object.
        transaction_id: The ID of the transaction to edit.

    Returns:
        HttpResponse: Rendered form page or redirect to transaction list on success, or HttpResponseForbidden if permission denied.
    """
    transaction = get_object_or_404(Transaction, id=transaction_id)
    logger.debug(f"Attempting to edit transaction {transaction_id} by user {request.user.username}")
    if not user_owns_object(request.user, transaction):
        logger.error("Permission denied: User %s tried to edit transaction %d owned by %s", request.user.username, transaction_id, transaction.user.username if transaction.user else "None")
        return HttpResponseForbidden("You do not have permission to edit this transaction.")
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            logger.debug(f"Transaction {transaction_id} updated by user {request.user.username}")
            return redirect('transaction_list')
        else:
            logger.error("Form errors for editing transaction %d by user %s: %s", transaction_id, request.user.username, form.errors)
            print(form.errors)  # Debug: Check terminal for errors
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, transaction_id):
    """Handle the deletion of an existing transaction for the authenticated user.

    Checks ownership, processes POST request, and redirects to the transaction list on success.

    Args:
        request: The HTTP request object.
        transaction_id: The ID of the transaction to delete.

    Returns:
        HttpResponse: Rendered confirmation page or redirect to transaction list on success, or HttpResponseForbidden if permission denied.
    """
    transaction = get_object_or_404(Transaction, id=transaction_id)
    logger.debug(f"Attempting to delete transaction {transaction_id} by user {request.user.username}")
    if not user_owns_object(request.user, transaction):
        logger.error("Permission denied: User %s tried to delete transaction %d owned by %s", request.user.username, transaction_id, transaction.user.username if transaction.user else "None")
        return HttpResponseForbidden("You do not have permission to delete this transaction.")
    if request.method == "POST":
        transaction.delete()
        logger.debug(f"Transaction {transaction_id} deleted by user {request.user.username}")
        return redirect('transaction_list')
    return render(request, 'transactions/delete_transaction.html', {'transaction': transaction})

@login_required
def budget_list(request):
    """Display a list of budgets for the authenticated user.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response with budget list.
    """
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'transactions/budget_list.html', {'budgets': budgets})

@login_required
def add_budget(request):
    """Handle the addition of a new budget for the authenticated user.

    Processes form submission, validates data, and redirects to the budget list upon success.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered form page or redirect to budget list on success.
    """
    logger.debug("Processing add_budget request for user: %s", request.user.username)
    if request.method == "POST":
        logger.debug("Form submitted with data: %s", request.POST)
        form = BudgetForm(request.POST)
        if form.is_valid():
            logger.debug("Form is valid")
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            logger.debug(f"Budget added: ID {budget.id}, User {request.user.username}")
            return redirect('budget_list')
        else:
            logger.error("Form errors for user %s: %s", request.user.username, form.errors)
            print(form.errors)  # Debug: Check terminal for errors
    else:
        logger.debug("Rendering empty form for user: %s", request.user.username)
        form = BudgetForm()
    return render(request, 'transactions/add_budget.html', {'form': form})

@login_required
def edit_budget(request, budget_id):
    """Handle the editing of an existing budget for the authenticated user.

    Checks ownership, processes form submission, validates data, and redirects to the budget list on success.

    Args:
        request: The HTTP request object.
        budget_id: The ID of the budget to edit.

    Returns:
        HttpResponse: Rendered form page or redirect to budget list on success, or HttpResponseForbidden if permission denied.
    """
    budget = get_object_or_404(Budget, id=budget_id)
    logger.debug(f"Attempting to edit budget {budget_id} by user {request.user.username}")
    if not user_owns_object(request.user, budget):
        logger.error("Permission denied: User %s tried to edit budget %d owned by %s", request.user.username, budget_id, budget.user.username if budget.user else "None")
        return HttpResponseForbidden("You do not have permission to edit this budget.")
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            logger.debug(f"Budget {budget_id} updated by user {request.user.username}")
            return redirect('budget_list')
        else:
            logger.error("Form errors for editing budget %d by user %s: %s", budget_id, request.user.username, form.errors)
            print(form.errors)  # Debug: Check terminal for errors
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'transactions/edit_budget.html', {'form': form})

@login_required
def delete_budget(request, budget_id):
    """Handle the deletion of an existing budget for the authenticated user.

    Checks ownership, processes POST request, and redirects to the budget list on success.

    Args:
        request: The HTTP request object.
        budget_id: The ID of the budget to delete.

    Returns:
        HttpResponse: Rendered confirmation page or redirect to budget list on success, or HttpResponseForbidden if permission denied.
    """
    budget = get_object_or_404(Budget, id=budget_id)
    logger.debug(f"Attempting to delete budget {budget_id} by user {request.user.username}")
    if not user_owns_object(request.user, budget):
        logger.error("Permission denied: User %s tried to delete budget %d owned by %s", request.user.username, budget_id, budget.user.username if budget.user else "None")
        return HttpResponseForbidden("You do not have permission to delete this budget.")
    if request.method == "POST":
        budget.delete()
        logger.debug(f"Budget {budget_id} deleted by user {request.user.username}")
        return redirect('budget_list')
    return render(request, 'transactions/delete_budget.html', {'budget': budget})

class RegisterView(CreateView):
    """Handle user registration using Django's UserCreationForm.

    Displays a registration form, validates user input, and redirects to the login page on success.

    Attributes:
        form_class: The UserCreationForm for registration.
        template_name: The HTML template for the registration form.
        success_url: The URL to redirect to after successful registration.
    """
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Registration successful! Please log in.')
        return super().form_valid(form)

class EditProfileView(LoginRequiredMixin, UpdateView):
    """Handle editing of user profile for authenticated users.

    Uses a custom form to update user details, ensuring only the authenticated user can edit their profile.

    Attributes:
        model: The User model.
        form_class: The CustomUserEditForm for profile updates.
        template_name: The HTML template for the edit profile form.
        success_url: The URL to redirect to after successful update.
    """
    model = User
    form_class = CustomUserEditForm  # Use the custom form instead of fields
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('transaction_list')

    def get_object(self):
        return self.request.user

def login_redirect_if_authenticated(view_func):
    """Decorator to redirect authenticated users to the landing page.

    Prevents logged-in users from accessing certain views (e.g., login page).

    Args:
        view_func: The view function to wrap.

    Returns:
        function: The wrapped view function.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('landing_page')  # Redirect to landing page if logged in
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def download_report(request):
    """Generate and download a PDF report of the user's financial data.

    Includes financial summary, transactions, and budgets for the authenticated user.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: PDF response with financial report attached.
    """
    # Get user data
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date')
    budgets = Budget.objects.filter(user=user).order_by('-start_date')

    # Calculate financial summary
    total_income = sum(t.amount for t in transactions.filter(transaction_type='Income')) or 0
    total_expenses = sum(t.amount for t in transactions.filter(transaction_type='Expense')) or 0
    net_balance = total_income - total_expenses
    total_budgets = sum(b.amount for b in budgets) or 0

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="financial_report_{datetime.date.today()}.pdf"'

    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title = Paragraph(f"Personal Finance Report - {datetime.date.today()}", styles['Title'])
    elements.append(title)
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Financial Summary Table
    summary_data = [
        ['Metric', 'Amount'],
        ['Total Income', f'${total_income:.2f}'],
        ['Total Expenses', f'${total_expenses:.2f}'],
        ['Net Balance', f'${net_balance:.2f}'],
        ['Total Budgets', f'${total_budgets:.2f}'],
    ]
    summary_table = Table(summary_data, colWidths=[200, 100])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(summary_table)
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Transactions Table
    if transactions.exists():
        trans_data = [['Date', 'Title', 'Amount', 'Type', 'Category']]
        for t in transactions:
            trans_data.append([t.date.strftime('%Y-%m-%d'), t.title, f'${t.amount:.2f}', t.transaction_type, t.category])
        trans_table = Table(trans_data, colWidths=[80, 100, 60, 60, 80])
        trans_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(Paragraph("Transactions", styles['Heading2']))
        elements.append(trans_table)

    # Budgets Table
    if budgets.exists():
        budget_data = [['Category', 'Amount', 'Start Date', 'End Date']]
        for b in budgets:
            budget_data.append([b.category, f'${b.amount:.2f}', b.start_date.strftime('%Y-%m-%d'), b.end_date.strftime('%Y-%m-%d') if b.end_date else 'Ongoing'])
        budget_table = Table(budget_data, colWidths=[100, 60, 80, 80])
        budget_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(Paragraph("<br/><br/>", styles['Normal']))
        elements.append(Paragraph("Budgets", styles['Heading2']))
        elements.append(budget_table)

    # Build PDF
    doc.build(elements)
    return response