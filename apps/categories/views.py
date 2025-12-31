from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer


# Public – list only active categories
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


# Admin – create category
class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


# Admin – update category
class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


# Admin – delete category
class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"
