from rest_framework import serializers
from .models import Order, OrderItem
from apps.cart.models import Cart


class OrderCreateSerializer(serializers.Serializer):
    # address fields (optional at DB level, but validated here if sent)
    full_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    address_line = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    state = serializers.CharField(required=False, allow_blank=True)
    pincode = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        request = self.context["request"]
        user = request.user

        # ❌ HARD BLOCK: frontend sending items
        if "items" in self.initial_data:
            raise serializers.ValidationError(
                "Direct items not allowed. Add to cart first."
            )

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart does not exist")

        if not cart.items.exists():
            raise serializers.ValidationError("Cart is empty")

        total = 0
        for item in cart.items.select_related("product_variant"):
            variant = item.product_variant

            if item.quantity > variant.stock:
                raise serializers.ValidationError(
                    f"Insufficient stock for {variant.product.name}"
                )

            total += variant.price * item.quantity

        data["cart"] = cart
        data["total_amount"] = total
        return data


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "product_name",
            "product_slug",
            "product_image",
            "quantity",
            "price",
        ]

    def get_product_image(self, obj):
        request = self.context.get("request")
        image = obj.product.images.first()
        if image and request:
            return request.build_absolute_uri(image.image.url)
        return None


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
            "full_name",
            "phone",
            "address_line",
            "city",
            "state",
            "pincode",
            "items",
        ]
