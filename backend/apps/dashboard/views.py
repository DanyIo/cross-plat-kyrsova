
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import DashboardService


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = DashboardService(request.user)

        return Response({
            "financial_summary": service.get_financial_summary(),
            "income_expense_chart": service.get_income_expense_chart(),
            "category_breakdown": service.get_category_breakdown(),
            "budget_vs_actual": service.get_budget_vs_actual(),
            "recent_transactions": service.get_recent_transactions()
        })
