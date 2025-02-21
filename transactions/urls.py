from django.urls import path
from .views import transaction_list, add_transaction, edit_transaction, delete_transaction

urlpatterns = [
    path('', transaction_list, name="transaction_list"),
    path('add/', add_transaction, name="add_transaction"),
    path('<int:transaction_id>/edit/', edit_transaction, name="edit_transaction"),
    path('<int:transaction_id>/delete/', delete_transaction, name="delete_transaction"),
]
