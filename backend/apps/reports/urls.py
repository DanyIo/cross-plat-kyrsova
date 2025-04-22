from django.urls import path
from .views import ReportDataView, ReportPDFView

urlpatterns = [
    path("data/", ReportDataView.as_view(), name="report-data"),
    path("pdf/", ReportPDFView.as_view(), name="report-pdf"),
]
