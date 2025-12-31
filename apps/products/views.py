from rest_framework import generics, permissions
from .models import Product
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
)


# List products with filters
class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        category = self.request.query_params.get("category")
        gender = self.request.query_params.get("gender")
        price = self.request.query_params.get("price")

        if category:
            queryset = queryset.filter(category__slug=category)

        if gender:
            queryset = queryset.filter(gender=gender)

        if price:
            queryset = queryset.filter(price__lte=price)

        return queryset


# Product detail by slug
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    lookup_field = "slug"


# Admin – create product
class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


# Admin – update product
class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"


# Admin – soft delete
class ProductDeleteView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "id"

    def perform_update(self, serializer):
        serializer.save(is_active=False)
