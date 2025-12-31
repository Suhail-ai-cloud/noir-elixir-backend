from rest_framework import serializers
from .models import Product, ProductImage,ProductVariant


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image"]

    def get_image(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url



class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    starting_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "starting_price", "image", "scent"]

    def get_starting_price(self, obj):
        variant = obj.variants.filter(is_active=True).order_by("price").first()
        return variant.price if variant else None


    def get_image(self, obj):
        request = self.context.get("request")
        image = obj.images.first()
        if image and request:
            return request.build_absolute_uri(image.image.url)
        return None



class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "size_ml", "price", "stock"]

        
class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "gender",
            "concentration",
            "scent",
            "description",
            "category",
            "images",
            "variants",
        ]



class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "stock",
            "gender",
            "concentration",
            "scent",
            "description",
            "category",
            "is_active",
        ]

