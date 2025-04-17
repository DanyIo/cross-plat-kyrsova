from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Budget, BudgetCategory
from apps.category.models import Category
from .serializers import BudgetSerializer
from django.utils import timezone


class UserBudgetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get or create current month's budget
        from datetime import datetime

        today = datetime.today().replace(day=1)
        budget, created = Budget.objects.get_or_create(user=request.user, month=today)

        if created:
            categories = Category.objects.all()
            for cat in categories:
                BudgetCategory.objects.create(budget=budget, category=cat, amount=0)

        serializer = BudgetSerializer(budget)
        return Response(serializer.data)

    def put(self, request):
        """Update amounts for existing budget"""
        budget = Budget.objects.filter(
            user=request.user, month__month=timezone.now().month
        ).first()
        if not budget:
            return Response(
                {"detail": "No budget found."}, status=status.HTTP_404_NOT_FOUND
            )

        for cat_data in request.data.get("categories", []):
            try:
                bc = BudgetCategory.objects.get(id=cat_data["id"], budget=budget)
                bc.amount = cat_data["amount"]
                bc.save()
            except BudgetCategory.DoesNotExist:
                continue

        serializer = BudgetSerializer(budget)
        return Response(serializer.data)
