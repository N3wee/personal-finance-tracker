from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
import logging

# Configure logging (optional, but included for consistency)
logger = logging.getLogger(__name__)

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

    return render(request, 'transactions/transaction_list.html', {
        'transactions': transactions,
        'transaction_type': transaction_type,
        'category': category,
        'start_date': start_date,
        'end_date': end_date,
        'sort_by': sort_by
    })

@login_required
def add_transaction(request):
    logger.debug("Processing add_transaction request")
    if request.method == "POST":
        logger.debug("Form submitted with data: %s", request.POST)
        form = TransactionForm(request.POST)
        if form.is_valid():
            logger.debug("Form is valid")
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
        else:
            logger.error("Form errors: %s", form.errors)
            print(form.errors)  # Debug: Check terminal for errors
    else:
        logger.debug("Rendering empty form")
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})

@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
        else:
            print(form.errors)  # Debug: Check terminal for errors
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == "POST":
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'transactions/delete_transaction.html', {'transaction': transaction})