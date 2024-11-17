from django.urls import path
from .views import TransactionListView, TransactionDetailView, BudgetListView, BudgetDetailView

urlpatterns = [
    # URLs for Transaction model
    path('transactions/', TransactionListView.as_view(), name="transaction_list"),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name="transaction_detail"),

    # URLs for Budget model
    path('budgets/', BudgetListView.as_view(), name="budget_list"),
    path('budgets/<int:pk>/', BudgetDetailView.as_view(), name="budget_detail"),

    
]
