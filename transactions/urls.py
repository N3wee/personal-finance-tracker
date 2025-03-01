from django.urls import path
from .views import transaction_list, add_transaction, edit_transaction, delete_transaction, budget_list, add_budget, edit_budget, delete_budget

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('', transaction_list, name="transaction_list"),  # Default view for /transactions/
    path('add/', add_transaction, name="add_transaction"),
    path('<int:transaction_id>/edit/', edit_transaction, name="edit_transaction"),
    path('<int:transaction_id>/delete/', delete_transaction, name="delete_transaction"),
    path('budgets/', budget_list, name="budget_list"),  # List all budgets
    path('budgets/add/', add_budget, name="add_budget"),  # Add a new budget
    path('budgets/<int:budget_id>/edit/', edit_budget, name="edit_budget"),  # Edit a budget
    path('budgets/<int:budget_id>/delete/', delete_budget, name="delete_budget"),  # Delete a budget
]