from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import BudgetService
from .serializers import BudgetSerializer, BudgetCreateUpdateSerializer
from .models import Budget

class BudgetViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """Отримати всі бюджети користувача"""
        budgets = BudgetService.get_user_budgets(request.user)
        serializer = BudgetSerializer(budgets, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Створити новий бюджет"""
        serializer = BudgetCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        budget = BudgetService.create_budget(
            request.user,
            serializer.data["name"],
            serializer.data["categories"],
        )
        return Response(BudgetSerializer(budget).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Оновити існуючий бюджет"""
        serializer = BudgetCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        budget = BudgetService.update_budget(
            request.user,
            pk,
            serializer.data["name"],
            serializer.data["categories"],
        )
        return Response(BudgetSerializer(budget).data)

    def destroy(self, request, pk):
        """Видалити бюджет"""
        response = BudgetService.delete_budget(request.user, pk)
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class BudgetSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Отримати підсумкові витрати відносно бюджету"""
        summary = BudgetService.get_budget_summary(request.user)
        return Response(summary)
