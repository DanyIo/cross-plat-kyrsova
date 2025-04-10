from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet, BudgetSummaryView

router = DefaultRouter()
router.register(r'budgets', BudgetViewSet, basename='budget')

urlpatterns = [
    path('budget-summary/', BudgetSummaryView.as_view(), name='budget-summary'),
] + router.urls
