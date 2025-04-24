from .models import Category
from .serializers import CategorySerializer

from apps.budget.models import BudgetCategory, Budget


class CategoryService:
    @staticmethod
    def get_user_categories(user):
        categories = Category.objects.filter(user=user)
        return CategorySerializer(categories, many=True).data

    def create_category(user, data: dict):
        category = Category.objects.create(user=user, **data)

        # Get or create the current month's budget for the user
        from datetime import datetime

        today = datetime.today().replace(day=1)
        budget, created = Budget.objects.get_or_create(user=user, month=today)

        # Add the new category to the budget with 0 amount (or default value)
        BudgetCategory.objects.create(budget=budget, category=category, amount=0)

        return category

    @staticmethod
    def update_category(category: Category, data: dict):
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    @staticmethod
    def delete_category(category: Category):
        category.delete()
