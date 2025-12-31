from django.db import models
from django.conf import settings


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    provider = models.CharField(max_length=50, default="razorpay")
    status = models.CharField(max_length=30, default="created")

    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order_id}"
