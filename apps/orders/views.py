from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Order, OrderItem
from .serializers import OrderCreateSerializer, OrderDetailSerializer
from apps.cart.views import clear_cart


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = OrderCreateSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        cart = serializer.validated_data["cart"]
        total_amount = serializer.validated_data["total_amount"]

        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            status="pending",
            payment_status="pending",
            full_name=serializer.validated_data.get("full_name"),
            phone=serializer.validated_data.get("phone"),
            address_line=serializer.validated_data.get("address_line"),
            city=serializer.validated_data.get("city"),
            state=serializer.validated_data.get("state"),
            pincode=serializer.validated_data.get("pincode"),
        )

        for item in cart.items.select_related("product_variant"):
            variant = item.product_variant

            # 🔒 reduce stock
            variant.stock -= item.quantity
            variant.save(update_fields=["stock"])

            OrderItem.objects.create(
                order=order,
                product=variant.product,
                quantity=item.quantity,
                price=variant.price,
            )

        clear_cart(cart)

        return Response(
            OrderDetailSerializer(
                order,
                context={"request": request}
            ).data,
            status=status.HTTP_201_CREATED
        )


class MyOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = OrderDetailSerializer(
            orders,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        order = get_object_or_404(
            Order,
            id=id,
            user=request.user
        )
        serializer = OrderDetailSerializer(
            order,
            context={"request": request}
        )
        return Response(serializer.data)


class AdminOrderStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, id):
        order = get_object_or_404(Order, id=id)

        status_value = request.data.get("status")
        if status_value not in dict(Order.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = status_value
        order.save(update_fields=["status"])

        return Response({"message": "Order status updated"})
