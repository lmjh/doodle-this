from django.shortcuts import render
from .models import Category, Product, ProductVariant
from accounts.models import Drawing


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
        variants = ProductVariant.objects.filter(product=product.pk).order_by(
            "price"
        )
        # add min_price for each product to the min_prices dict
        min_prices[product.name] = variants[0].price

    template = "prints/show_all_prints.html"
    context = {
        "products": products,
        "min_prices": min_prices,
    }

    return render(request, template, context)


def product_details(request, product_name):

    product = Product.objects.get(name=product_name)
    variants = ProductVariant.objects.filter(product=product.pk)
    saved_drawings = Drawing.objects.filter(user_account=request.user.pk)

    # create dict to store data to be passed to page javascript
    json_data = {}
    # use dict comprehension to store urls of user's saved drawings, variant
    # prices, and product image urls
    json_data["drawingUrls"] = {
        drawing.save_slot: drawing.image.url for drawing in saved_drawings
    }
    json_data["variantPrices"] = {
        variant.name: variant.price for variant in variants
    }
    # if a variant has an image attached, store its url
    json_data["variantUrls"] = {
        variant.name: variant.image.image.url
        for variant in variants
        if variant.image
    }
    # add the image url for the default product image
    json_data["variantUrls"]["default"] = product.image.image.url
    # if a variant has an image attached, add the overlay data for that image
    # to an array
    json_data["overlay"] = {
        variant.name: [
            variant.image.overlay_width,
            variant.image.overlay_x_offset,
            variant.image.overlay_y_offset,
        ]
        for variant in variants
        if variant.image
    }
    # add the overlay data for the default product image
    json_data["overlay"]["default"] = [
        product.image.overlay_width,
        product.image.overlay_x_offset,
        product.image.overlay_y_offset,
    ]

    template = "prints/product_details.html"
    context = {
        "product": product,
        "variants": variants,
        "saved_drawings": saved_drawings,
        "json_data": json_data,
    }

    return render(request, template, context)
