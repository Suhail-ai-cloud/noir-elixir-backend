# apps\orders\models.py
from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    total_amount = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    payment_status = models.CharField(
        max_length=20,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=120, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address_line = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=80, null=True, blank=True)
    state = models.CharField(max_length=80, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
    "products.Product",
    on_delete=models.PROTECT
)

    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product} x {self.quantity}"
