from django.shortcuts import render
from .models import Category, Product, ProductVariant


def show_all_prints(request):
    """
    A view to display all available print product in the shop
    """

    # get all products
    products = Product.objects.all()

    # create a dict to hold minimum prices
    min_prices = {}

    # iterate through products
    for product in products:
        # find variants for each product and order by price
        variants = ProductVariant.objects.filter(product=product.pk).order_by('price')
        # add min_price for each product to the min_prices dict
        min_prices[product.name] = variants[0].price

    template = "prints/show_all_prints.html"
    context = {
        'products': products,
        'min_prices': min_prices,
    }

    return render(request, template, context)


def product_details(request, product_name):

    product = Product.objects.get(name=product_name)

    template = 'prints/product_details.html'
    context = {
        'product': product
    }

    return render(request, template, context)
