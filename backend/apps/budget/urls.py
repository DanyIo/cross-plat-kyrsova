from django.urls import path
from .views import UserBudgetView

urlpatterns = [
    path("budget/", UserBudgetView.as_view(), name="user-budget"),
]

