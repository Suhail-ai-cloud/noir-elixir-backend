from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="product.id", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product_id", "price", "quantity"]

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "total_amount",
            "status",
            "payment_status",
            "created_at",
            "items",
        ]
class OrderCreateSerializer(serializers.Serializer):
    payment_status = serializers.CharField()
