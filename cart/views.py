from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from prints.models import ProductVariant


def view_cart(request):
    """
    A view to display the contents of the user's shopping cart
    """

    template = "cart/cart.html"
    return render(request, template)


def add_to_cart(request):
    """
    A view to add items to the user's shopping cart
    """
    if request.method == "POST":
        # gather data from POST request
        variant_id = request.POST.get("variant")
        variant = get_object_or_404(ProductVariant, pk=variant_id)
        quantity = int(request.POST.get("quantity"))
        drawing = request.POST.get("drawing")
        redirect_url = request.POST.get("redirect_url")

        # set the drawing name to be displayed in messages
        if drawing == "autosave":
            drawing_name = "your current sketchbook"
        else:
            drawing_name = f"Save Slot {drawing}"

        # get cart from session or set to an empty list if not found
        cart = request.session.get("cart", [])

        # declare a variable to record if the variant/drawing pair is already
        # in the cart
        in_cart = False
        # iterate throught the cart list
        for item in cart:
            # if the list contains an object with the same variant id and
            # drawing as the request
            if item['variant_id'] == variant_id and item['drawing'] == drawing:
                # increase that object's quantity and set in_cart to true
                item['quantity'] += quantity
                in_cart = True
                messages.success(
                    request,
                    f"Added {quantity} x {variant.product.display_name} - {variant.display_name} printed with {drawing_name} to your cart",
                )

        # if no matching object was found
        if in_cart is False:
            # add an object to the cart using the submitted data
            item = {
                'variant_id': variant_id,
                'drawing': drawing,
                'quantity': quantity,
            }
            cart.append(item)
            messages.success(
                    request,
                    f"Added {quantity} x {variant.product.display_name} - {variant.display_name} printed with {drawing_name} to your cart",
                )

        request.session["cart"] = cart
        print(request.session["cart"])

        return redirect(redirect_url)
