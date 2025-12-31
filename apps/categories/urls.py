from django.urls import path
from .views import (
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
)

urlpatterns = [
    path("", CategoryListView.as_view(), name="category-list"),
    path("create/", CategoryCreateView.as_view(), name="category-create"),
    path("<int:id>/update/", CategoryUpdateView.as_view(), name="category-update"),
    path("<int:id>/delete/", CategoryDeleteView.as_view(), name="category-delete"),
]
