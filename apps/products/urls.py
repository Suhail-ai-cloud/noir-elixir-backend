from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),

    # ✅ MOVE SLUG DETAIL UP
    path("<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),

    # Admin routes AFTER
    path("create/", ProductCreateView.as_view(), name="product-create"),
    path("<int:id>/update/", ProductUpdateView.as_view(), name="product-update"),
    path("<int:id>/delete/", ProductDeleteView.as_view(), name="product-delete"),
]
