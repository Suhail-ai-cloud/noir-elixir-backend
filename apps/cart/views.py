from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from apps.products.models import Product
from apps.products.models import ProductVariant

from .serializers import CartSerializer



class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(
            cart,
            context={"request": request}  # ✅ THIS FIXES EVERYTHING
        )
        return Response(serializer.data)



class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        variant_id = request.data.get("variant_id")
        quantity = int(request.data.get("quantity", 1))

        if quantity <= 0:
            return Response(
                {"error": "Invalid quantity"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart, _ = Cart.objects.get_or_create(user=user)

        variant = get_object_or_404(
            ProductVariant,
            id=variant_id,
            is_active=True
        )

        if quantity > variant.stock:
            return Response(
                {"error": "Insufficient stock"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_variant=variant,
            defaults={"quantity": quantity},
        )

        if not created:
            if cart_item.quantity + quantity > variant.stock:
                return Response(
                    {"error": "Insufficient stock"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity += quantity
            cart_item.save()

        return Response({"message": "Item added to cart"})
    
    
class UpdateCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity"))

        if quantity <= 0:
            return Response(
                {"error": "Invalid quantity"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        if quantity > cart_item.product_variant.stock:
            return Response(
                {"error": "Insufficient stock"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Cart item updated"})


class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        item_id = request.data.get("item_id")

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        cart_item.delete()
        return Response({"message": "Item removed"})
def clear_cart(cart):
    cart.items.all().delete()
