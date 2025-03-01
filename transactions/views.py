from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Budget
from .forms import TransactionForm, BudgetForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib import messages
import datetime
import logging
import requests
import os

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

def landing_page(request):
    return render(request, 'transactions/landing.html')

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
    fields = ['username', 'email']
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