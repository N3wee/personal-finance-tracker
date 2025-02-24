from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("bank_transfer", "Bank Transfer"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to user
    title = models.CharField(max_length=255)  # Short description
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Money value
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)  # Income or Expense
    category = models.CharField(max_length=100)  # e.g., Food, Rent, Salary
    date = models.DateField(default=timezone.now)  # Default to today but editable
    notes = models.TextField(blank=True, null=True)  # Optional description
    recurring = models.BooleanField(default=False)  # If transaction repeats
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default="cash")  # Payment method

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.transaction_type})"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to user
    category = models.CharField(max_length=100)  # Budget category (e.g., Food, Rent)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Budgeted amount
    start_date = models.DateField(default=timezone.now)  # Start of budget period
    end_date = models.DateField(blank=True, null=True)  # End of budget period (optional)
    notes = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f"{self.category} - ${self.amount} ({self.user.username})"