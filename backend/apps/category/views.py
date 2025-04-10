from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Category
from .serializers import CategorySerializer
from .services import CategoryService

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        categories = CategoryService.get_user_categories(request.user)
        return Response(
             categories
        )


    def perform_create(self, serializer):
        CategoryService.create_category(self.request.user, serializer.validated_data)

    def update(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs['pk'], user=request.user)
        category = CategoryService.update_category(category, request.data)
        return Response(CategorySerializer(category).data)

    def destroy(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs['pk'], user=request.user)
        CategoryService.delete_category(category)
        return Response(status=status.HTTP_204_NO_CONTENT)
