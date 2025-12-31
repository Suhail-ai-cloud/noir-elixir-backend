import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.orders.models import Order
from .models import Payment

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        order_id = request.data.get("order_id")

        if not order_id:
            return Response(
                {"error": "order_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = get_object_or_404(Order, id=order_id, user=request.user)

        # 🚫 Block non-pending orders
        if order.status != "pending":
            return Response(
                {"error": "Order cannot be paid"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 🔒 ATOMIC & SAFE
            payment, created = Payment.objects.get_or_create(
                order=order,
                defaults={
                    "user": request.user,
                    "amount": order.total_amount,
                    "provider": "razorpay",
                }
            )
        except IntegrityError:
            payment = Payment.objects.get(order=order)
            created = False

        # If Razorpay order already exists, return it
        if not created and payment.razorpay_order_id:
            return Response({
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "razorpay_order_id": payment.razorpay_order_id,
                "amount": int(payment.amount * 100),
                "currency": "INR",
                "order_id": order.id,
            }, status=status.HTTP_200_OK)

        # Create Razorpay order ONLY ONCE
        razorpay_order = client.order.create({
            "amount": int(order.total_amount * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        payment.razorpay_order_id = razorpay_order["id"]
        payment.status = "created"
        payment.save(update_fields=["razorpay_order_id", "status"])

        return Response({
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": payment.razorpay_order_id,
            "amount": int(payment.amount * 100),
            "currency": "INR",
            "order_id": order.id,
        }, status=status.HTTP_201_CREATED)


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        data = request.data

        payment = get_object_or_404(
            Payment,
            razorpay_order_id=data.get("razorpay_order_id")
        )

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"],
            })
        except razorpay.errors.SignatureVerificationError:
            payment.status = "failed"
            payment.save(update_fields=["status"])
            return Response({"error": "Payment verification failed"}, status=400)

        payment.razorpay_payment_id = data["razorpay_payment_id"]
        payment.razorpay_signature = data["razorpay_signature"]
        payment.status = "success"
        payment.save()

        order = payment.order
        order.status = "paid"
        order.payment_status = "paid"
        order.save(update_fields=["status", "payment_status"])

        return Response({"message": "Payment successful"})
