from django.db import models


def product_upload_path(instance, filename):
    """
    Constructs and returns a path for product images to be uploaded to.
    """
    return f"products/{instance.name}/{filename}"


def variant_upload_path(instance, filename):
    """
    Constructs and returns a path for product variant images to be uploaded to.
    """
    return f"products/{instance.product.name}/{instance.name}/{filename}"


class Category(models.Model):
    """
    A model for categorising printed products
    """

    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=120)
    disaply_name = models.CharField(max_length=120, null=False, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    A model to represent each printed product type
    """

    class VariantType(models.TextChoices):
        """
        Defines options for the variant_type field
        """

        COLOURS = "CL"
        SIZES = "SZ"

    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(
        max_length=120, null=False, blank=False, unique=True
    )
    display_name = models.CharField(max_length=120, null=False, blank=False)
    image = models.ImageField(
        null=True, blank=True, upload_to=product_upload_path
    )
    description = models.TextField(null=False, blank=False)
    variant_type = models.CharField(
        max_length=2, choices=VariantType.choices, default=VariantType.SIZES
    )

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """
    A model to represent each individual product variant
    """

    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=120, null=False, blank=False)
    display_name = models.CharField(max_length=120, null=False, blank=False)
    image = models.ImageField(
        null=True, blank=True, upload_to=variant_upload_path
    )
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    sku = models.CharField(max_length=120, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.product} Variant - {self.name}"
