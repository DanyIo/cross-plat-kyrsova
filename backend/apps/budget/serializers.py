from rest_framework import serializers
from .models import Budget, BudgetCategory
from apps.category.models import Category


class BudgetCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = BudgetCategory
        fields = ["id", "category", "category_name", "amount"]


class BudgetSerializer(serializers.ModelSerializer):
    categories = BudgetCategorySerializer(many=True)

    class Meta:
        model = Budget
        fields = ["id", "month", "categories"]
