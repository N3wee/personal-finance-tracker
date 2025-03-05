from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("Income", "Income"),
        ("Expense", "Expense"),
    ]

    PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("bank_transfer", "Bank Transfer"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    recurring = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHODS, default="cash"
    )

    def clean(self):
        if self.amount is None or self.amount <= 0:  # Fixed syntax here
            raise ValidationError("Amount must be greater than zero.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.transaction_type})"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def clean(self):
        if self.amount is None or self.amount <= 0:
            raise ValidationError("Budget amount must be greater than zero.")
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("End date must be after start date.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category} - ${self.amount} ({self.user.username})"
