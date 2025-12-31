from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product_variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ("cart", "product_variant")

    def __str__(self):
        return f"{self.product_variant} x {self.quantity}"
