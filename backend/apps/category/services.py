
from .models import Category
from .serializers import CategorySerializer

class CategoryService:
    @staticmethod
    def get_user_categories(user):
        categories = Category.objects.filter(user=user)
        return CategorySerializer(categories, many=True).data

    @staticmethod
    def create_category(user, data: dict):
        return Category.objects.create(user=user, **data)

    @staticmethod
    def update_category(category: Category, data: dict):
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    @staticmethod
    def delete_category(category: Category):
        category.delete()
