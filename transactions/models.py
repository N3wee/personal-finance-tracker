from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to user
    title = models.CharField(max_length=255)  # Short description
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Money value
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)  # Income or Expense
    category = models.CharField(max_length=100)  # e.g., Food, Rent, Salary
    date = models.DateField(auto_now_add=True)  # Default to the current date
    notes = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.transaction_type})"
from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links to user
    title = models.CharField(max_length=255)  # Short description
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Money value
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)  # Income or Expense
    category = models.CharField(max_length=100)  # e.g., Food, Rent, Salary
    date = models.DateField() 
    notes = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.transaction_type})"
