from django.shortcuts import render
from .models import Category, Product, ProductVariant


def show_all_prints(request):
    """
    A view to display all available print product in the shop
    """

    products = Product.objects.all()

    template = "prints/show_all_prints.html"
    context = {
        'products': products,
    }

    return render(request, template, context)