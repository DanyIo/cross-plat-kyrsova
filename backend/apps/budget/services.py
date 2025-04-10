from .models import Budget, BudgetCategory
from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework.exceptions import PermissionDenied

class BudgetService:
    @staticmethod
    def get_user_budgets(user: User):
        """Отримати всі бюджети поточного користувача"""
        return Budget.objects.filter(user=user)

    @staticmethod
    def create_budget(user: User, name: str, categories_data: list):
        """Створити новий бюджет з категоріями"""
        budget = Budget.objects.create(user=user, name=name)
    
        # Додати категорії до бюджету
        for category_data in categories_data:
            BudgetCategory.objects.create(
                budget=budget,
                category_id=category_data["category"],
                amount=category_data["amount"],
            )

        return budget

    @staticmethod
    def update_budget(user: User, budget_id: int, name: str, categories_data: list):
        """Оновити бюджет користувача"""
        budget = Budget.objects.filter(id=budget_id, user=user).first()
        if not budget:
            raise PermissionDenied("Budget not found or access denied.")

        budget.name = name
        budget.save()

        # Оновлення категорій
        BudgetCategory.objects.filter(budget=budget).delete()
        for category_data in categories_data:
            BudgetCategory.objects.create(
                budget=budget,
                category_id=category_data["category"],
                amount=category_data["amount"],
            )

        return budget

    @staticmethod
    def delete_budget(user: User, budget_id: int):
        """Видалити бюджет"""
        budget = Budget.objects.filter(id=budget_id, user=user).first()
        if not budget:
            raise PermissionDenied("Budget not found or access denied.")
        
        budget.delete()
        return {"message": "Budget deleted successfully"}

    @staticmethod
    def get_budget_summary(user: User):
        """Отримати підсумкові витрати відносно бюджету"""
        budgets = Budget.objects.filter(user=user)
        summary = []

        for budget in budgets:
            total_spent = BudgetCategory.objects.filter(budget=budget).aggregate(Sum("amount"))["amount__sum"] or 0
            summary.append({
                "budget_name": budget.name,
                "total_spent": total_spent,
            })

        return summary
