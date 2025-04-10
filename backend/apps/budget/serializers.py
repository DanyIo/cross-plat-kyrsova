from rest_framework import serializers
from .models import Budget, BudgetCategory

class BudgetCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    color = serializers.ReadOnlyField(source="category.color")

    class Meta:
        model = BudgetCategory
        fields = ["id", "category", "category_name", "color", "amount"]

class BudgetSerializer(serializers.ModelSerializer):
    categories = BudgetCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = ["id", "name", "categories", "created_at"]

class BudgetCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    categories = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField())
    )
