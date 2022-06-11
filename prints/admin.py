from django.contrib import admin
from .models import Category, Product, ProductVariant


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "name",
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "name",
        "category",
        "variant_type",
        "description",
        "image",
    )


class ProductVariantAdmin(admin.ModelAdmin):
    list_display: (
        "display_name",
        "name",
        "product",
        "sku",
        "cost",
        "description",
        "image",
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
