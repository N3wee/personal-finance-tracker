from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Landing page at root /
    path('transactions/', views.transaction_list, name='transaction_list'),  # Transaction list at /transactions/
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('transactions/<int:transaction_id>/edit/', views.edit_transaction, name='edit_transaction'),
    path('transactions/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
    path('budgets/', views.budget_list, name='budget_list'),  # Budget list at /budgets/
    path('budgets/add/', views.add_budget, name='add_budget'),  # Add budget at /budgets/add/
    path('budgets/<int:budget_id>/edit/', views.edit_budget, name='edit_budget'),  # Edit budget at /budgets/<id>/edit/
    path('budgets/<int:budget_id>/delete/', views.delete_budget, name='delete_budget'),  # Delete budget at /budgets/<id>/delete/
    path('edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),  # Add edit_profile route
]