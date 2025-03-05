from django.contrib import admin

from .models import Budget, Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "transaction_type", "category", "date", "user")
    list_filter = ("transaction_type", "category", "date")
    search_fields = ("title", "category")


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("category", "amount", "start_date", "end_date", "user")
    list_filter = ("category", "start_date", "end_date")
    search_fields = ("category",)
