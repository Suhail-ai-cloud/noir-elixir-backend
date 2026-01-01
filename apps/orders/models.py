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
    variant = models.ForeignKey(
    "products.ProductVariant",
    on_delete=models.PROTECT,
    related_name="order_items",
    null=True,        # 👈 TEMP
    blank=True        # 👈 TEMP
)

# Snapshot fields (VERY IMPORTANT)
    product_name = models.CharField(max_length=200)
    size_ml = models.PositiveIntegerField()


    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} {self.size_ml}ml x {self.quantity}"

