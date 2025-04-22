from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse
from .services import ReportService


class ReportDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = ReportService(request.user)
        return Response(service.get_monthly_yearly_data())


class ReportPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = ReportService(request.user)
        pdf_response = service.generate_pdf()  # Now returns FileResponse
        return pdf_response
