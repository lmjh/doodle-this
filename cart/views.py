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

        # get cart from session or set to an empty dict if not found
        cart = request.session.get("cart", {})

        # if the selected variant is already in the cart
        if variant_id in list(cart.keys()):
            # if the selected variant printed with the selected drawing is in
            # the cart
            if drawing in cart[variant_id]["drawing"].keys():
                # increase the quantity of the selected variant/drawing pair
                cart[variant_id]["drawing"][drawing] += quantity
                messages.success(
                    request,
                    f"Added {quantity} x {variant.product.display_name} - {variant.display_name} printed with {drawing_name} to your cart",
                )
            else:
                # otherwise, add the selected variant/drawing pair
                cart[variant_id]["drawing"][drawing] = quantity
                messages.success(
                    request,
                    f"Added {quantity} x {variant.product.display_name} - {variant.display_name} printed with {drawing_name} to your cart",
                )
        else:
            # add the selected variant/drawing pair
            cart[variant_id] = {"drawing": {drawing: quantity}}
            messages.success(
                request,
                f"Added {quantity} x {variant.product.display_name} - {variant.display_name} printed with {drawing_name} to your cart",
            )

        request.session["cart"] = cart
        print(request.session["cart"])

        return redirect(redirect_url)
