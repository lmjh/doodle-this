from django.shortcuts import render, redirect, get_object_or_404, reverse
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
        if drawing == "0":
            drawing_name = "Current Doodle"
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
            if item["variant_id"] == variant_id and item["drawing"] == drawing:
                # increase that object's quantity and set in_cart to true
                item["quantity"] += quantity
                in_cart = True
                messages.success(
                    request,
                    f"Product: {quantity} x {variant.product.display_name} - "
                    f"{variant.display_name} <br>Doodle: {drawing_name}<br>"
                    "Added to shopping cart.",
                )

        # if no matching object was found
        if in_cart is False:
            # add an object to the cart using the submitted data
            item = {
                "variant_id": variant_id,
                "drawing": drawing,
                "quantity": quantity,
            }
            cart.append(item)
            messages.success(
                request,
                f"Product: {quantity} x {variant.product.display_name} - "
                f"{variant.display_name} <br>Doodle: {drawing_name}<br>"
                "Added to shopping cart.",
            )

        request.session["cart"] = cart
        print(request.session["cart"])

        return redirect(redirect_url)


def update_cart_item(request):
    """
    A view to update the quantity of an item in the shopping cart
    """
    if request.method == "POST":
        # gather data from request
        variant_id = request.POST.get("variant_id")
        drawing = request.POST.get("drawing")
        quantity = int(request.POST.get("quantity"))

        # get cart from session
        cart = request.session.get("cart", [])

        # iterate over a copy of the cart, enumerate to access loop index
        # (https://stackoverflow.com/a/10665631)
        for index, item in enumerate(cart[:]):
            # find the item matching the variant_id and selected drawing
            if item["variant_id"] == variant_id and item["drawing"] == drawing:
                # remove from the cart list if quantity is zero
                if quantity is 0:
                    cart.remove(item)
                    messages.success(
                        request,
                        "Item removed from shopping cart.",
                    )
                # update the cart item's quantity if greater than zero
                else:
                    cart[index]["quantity"] = quantity
                    messages.success(
                        request,
                        "Shopping cart quantity updated.",
                    )

        # update session cart and redirect to view_cart page
        request.session["cart"] = cart
        return redirect(reverse("view_cart"))


def remove_cart_item(request):
    """
    A view to remove an item from the shopping cart
    """
    if request.method == "POST":
        # gather data from request
        variant_id = request.POST.get("variant_id")
        drawing = request.POST.get("drawing")

        # get cart from session
        cart = request.session.get("cart", [])

        # iterate over a copy of the cart
        for item in cart[:]:
            # find the item matching the variant_id and selected drawing
            if item["variant_id"] == variant_id and item["drawing"] == drawing:
                # remove from the cart list
                cart.remove(item)
                messages.success(
                    request,
                    "Item removed from shopping cart.",
                )

        # update session cart and redirect to view_cart page
        request.session["cart"] = cart
        return redirect(reverse("view_cart"))
