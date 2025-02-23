from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required
import logging

# Configure logging
logger = logging.getLogger(__name__)

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})

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