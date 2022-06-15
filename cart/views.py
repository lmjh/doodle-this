from django.shortcuts import render, redirect


def view_cart(request):
    """
    A view to display the contents of the user's shopping cart
    """

    template = "cart/cart.html"
    return render(request, template)


def add_to_cart(request):
    if request.method == "POST":
        variant_id = request.POST.get('variant')
        quantity = int(request.POST.get('quantity'))
        drawing = request.POST.get('drawing')
        redirect_url = request.POST.get('redirect_url')

        cart = request.session.get('cart', {})

        if variant_id in list(cart.keys()):
            cart[variant_id] += quantity
        else:
            cart[variant_id] = quantity

        request.session['cart'] = cart

        print(request.session['cart'])
        return redirect(redirect_url)
