from django import forms
from .widgets import ProductImageInput
from .models import ProductImage, Product


class ProductImageForm(forms.ModelForm):
    """
    A form to create product images
    """

    class Meta:
        model = ProductImage
        fields = "__all__"

    # use custom ProductImageInput widget for image field
    image = forms.ImageField(
        label="image", required=True, widget=ProductImageInput
    )


class ProductForm(forms.ModelForm):
    """
    A form to create products
    """

    class Meta:
        model = Product
        fields = "__all__"
