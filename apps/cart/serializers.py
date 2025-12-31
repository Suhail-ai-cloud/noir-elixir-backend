from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    variant_id = serializers.IntegerField(
        source="product_variant.id",
        read_only=True
    )
    size_ml = serializers.IntegerField(
        source="product_variant.size_ml",
        read_only=True
    )
    price = serializers.DecimalField(
        source="product_variant.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    stock = serializers.IntegerField(
        source="product_variant.stock",
        read_only=True
    )
    product_name = serializers.CharField(
        source="product_variant.product.name",
        read_only=True
    )

    product_image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "variant_id",
            "product_name",
            "size_ml",
            "price",
            "stock",
            "quantity",
            "product_image",
        ]

    # ✅ THIS METHOD MUST EXIST (NAME MUST MATCH)
    def get_product_image(self, obj):
        image = obj.product_variant.product.images.first()
        request = self.context.get("request")

        if image and request:
            return request.build_absolute_uri(image.image.url)

        if image:
            return image.image.url

        return None



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "created_at", "items"]
