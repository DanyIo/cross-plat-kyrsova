from django.urls import path

from .views import DashboardView

urlpatterns = [
    path("overview/", DashboardView.as_view(), name="dashboard_overview"),
]
