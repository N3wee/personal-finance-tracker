from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'transaction_type', 'category', 'date', 'notes']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }