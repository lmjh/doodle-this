from django.shortcuts import render


def view_cart(request):
    """
    A view to display the contents of the user's shopping cart
    """

    template = "cart/cart.html"
    return render(request, template)