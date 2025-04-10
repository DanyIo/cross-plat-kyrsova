from django.urls import path
from .views import TransactionListCreateView, TransactionUpdateView

urlpatterns = [
    path("transactions/", TransactionListCreateView.as_view(), name="transaction-list"),
    path('transactions/<int:pk>/', TransactionUpdateView.as_view(), name='transaction-update'),

]
