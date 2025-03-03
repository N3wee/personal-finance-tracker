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
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import datetime
import logging
import requests
import os

from .models import Transaction, Budget
from .forms import TransactionForm, BudgetForm, CustomUserEditForm  # Import the new form

# Configure logging
logger = logging.getLogger(__name__)

def user_owns_object(user, obj):
    """Check if the user owns the object or is a superuser."""
    if obj is None:
        logger.error("Object is None in user_owns_object")
        return False
    owner = getattr(obj, 'user', None)
    if owner is None:
        logger.error(f"No user associated with object: {obj}")
        return False
    # Allow superusers to bypass ownership check
    result = user.is_superuser or owner == user
    logger.debug(f"Checking ownership: User {user.username}, Object user {owner.username if owner else 'None'}, "
                 f"Object type {type(obj).__name__}, Object ID {obj.id if obj.id else 'None'}, Result {result}")
    return result

@login_required(login_url='login')  # Explicitly specify login URL for clarity
def landing_page(request):
    # Ensure user is authenticated (should be handled by @login_required, but handle gracefully)
    if not request.user.is_authenticated:
        logger.warning("Unauthenticated user attempted to access landing_page, redirecting to login")
        return redirect('login')  # Redirect to login if unauthenticated

    # Calculate financial summary for the authenticated user
    try:
        transactions = Transaction.objects.filter(user=request.user)
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

        return render(request, 'transactions/landing.html', {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': net_balance,
            'total_budgets': total_budgets,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
        })
    except Exception as e:
        # Log the error for debugging (especially on Heroku)
        logger.error(f"Error in landing_page: {str(e)}")
        return redirect('login')  # Fallback redirect if something goes wrong

@login_required
def transaction_list(request):
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
    transaction = get_object_or_404(Transaction, id=transaction_id)
    logger.debug(f"Attempting to edit transaction {transaction_id} by user {request.user.username}")
    if not user_owns_object(request.user, transaction):
        logger.error("Permission denied: User %s tried to edit transaction %s owned by %s", request.user.username, transaction_id, transaction.user.username if transaction.user else "None")
        raise PermissionDenied("You do not have permission to edit this transaction.")
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            logger.debug(f"Transaction {transaction_id} updated by user {request.user.username}")
            return redirect('transaction_list')
        else:
            logger.error("Form errors for editing transaction %s by user %s: %s", transaction_id, request.user.username, form.errors)
            print(form.errors)  # Debug: Check terminal for errors
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    logger.debug(f"Attempting to delete transaction {transaction_id} by user {request.user.username}")
    if not user_owns_object(request.user, transaction):
        logger.error("Permission denied: User %s tried to delete transaction %s owned by %s", request.user.username, transaction_id, transaction.user.username if transaction.user else "None")
        raise PermissionDenied("You do not have permission to delete this transaction.")
    if request.method == "POST":
        transaction.delete()
        logger.debug(f"Transaction {transaction_id} deleted by user {request.user.username}")
        return redirect('transaction_list')
    return render(request, 'transactions/delete_transaction.html', {'transaction': transaction})

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'transactions/budget_list.html', {'budgets': budgets})

@login_required
def add_budget(request):
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
    budget = get_object_or_404(Budget, id=budget_id)
    logger.debug(f"Attempting to edit budget {budget_id} by user {request.user.username}")
    if not user_owns_object(request.user, budget):
        logger.error("Permission denied: User %s tried to edit budget %s owned by %s", request.user.username, budget_id, budget.user.username if budget.user else "None")
        raise PermissionDenied("You do not have permission to edit this budget.")
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            logger.debug(f"Budget {budget_id} updated by user {request.user.username}")
            return redirect('budget_list')
        else:
            logger.error("Form errors for editing budget %s by user %s: %s", budget_id, request.user.username, form.errors)
            print(form.errors)  # Debug: Check terminal for errors
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'transactions/edit_budget.html', {'form': form})

@login_required
def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id)
    logger.debug(f"Attempting to delete budget {budget_id} by user {request.user.username}")
    if not user_owns_object(request.user, budget):
        logger.error("Permission denied: User %s tried to delete budget {budget_id} owned by %s", request.user.username, budget_id, budget.user.username if budget.user else "None")
        raise PermissionDenied("You do not have permission to delete this budget.")
    if request.method == "POST":
        budget.delete()
        logger.debug(f"Budget {budget_id} deleted by user {request.user.username}")
        return redirect('budget_list')
    return render(request, 'transactions/delete_budget.html', {'budget': budget})

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request, 'Registration successful! Please log in.')
        return super().form_valid(form)

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserEditForm  # Use the custom form instead of fields
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('transaction_list')

    def get_object(self):
        return self.request.user
    
def login_redirect_if_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('landing_page')  # Redirect to landing page if logged in
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
def download_report(request):
    # Get user data
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date')
    budgets = Budget.objects.filter(user=user).order_by('-start_date')

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="financial_report_{}.pdf".format(datetime.date.today())'

    # Create PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title = Paragraph("Personal Finance Report - {}".format(datetime.date.today()), styles['Title'])
    elements.append(title)
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Financial Summary Table
    summary_data = [
        ['Metric', 'Amount'],
        ['Total Income', '${:.2f}'.format(sum(t.amount for t in transactions.filter(transaction_type='Income')) or 0)],
        ['Total Expenses', '${:.2f}'.format(sum(t.amount for t in transactions.filter(transaction_type='Expense')) or 0)],
        ['Net Balance', '${:.2f}'.format(sum(t.amount for t in transactions.filter(transaction_type='Income')) - sum(t.amount for t in transactions.filter(transaction_type='Expense')) or 0)],
        ['Total Budgets', '${:.2f}'.format(sum(b.amount for b in budgets) or 0)],
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
            trans_data.append([t.date.strftime('%Y-%m-%d'), t.title, '${:.2f}'.format(t.amount), t.transaction_type, t.category])
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
            budget_data.append([b.category, '${:.2f}'.format(b.amount), b.start_date.strftime('%Y-%m-%d'), b.end_date.strftime('%Y-%m-%d') if b.end_date else 'Ongoing'])
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