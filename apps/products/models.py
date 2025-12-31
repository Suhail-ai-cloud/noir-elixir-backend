from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    GENDER_CHOICES = (
        ("men", "Men"),
        ("women", "Women"),
        ("unisex", "Unisex"),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    # stock = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    concentration = models.CharField(max_length=100)
    scent = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.PROTECT,
        related_name="products",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductVariant(models.Model):
    ML_CHOICES = (
        (10, "10 ml"),
        (30, "30 ml"),
        (50, "50 ml"),
        (100, "100 ml"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )

    size_ml = models.PositiveIntegerField(choices=ML_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("product", "size_ml")

    def __str__(self):
        return f"{self.product.name} - {self.size_ml}ml"
