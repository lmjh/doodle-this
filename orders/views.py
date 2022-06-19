from decimal import Decimal
import stripe

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.files import File

from .forms import OrderForm
from .models import Order, OrderDrawing, OrderItem
from prints.models import ProductVariant
from accounts.models import Drawing, UserAccount
from accounts.forms import NameUpdateForm, DefaultAddressForm
from cart.contexts import cart_contents


def checkout(request):
    """
    A view to display the order form and handle order submissions and payments
    """
    # get stripe public and secret keys from environment
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # get the user's cart from the session
    cart = request.session.get("cart", [])

    if request.method == "POST":
        # gather form data from request
        form_data = {
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "address_1": request.POST["address_1"],
            "address_2": request.POST["address_2"],
            "town": request.POST["town"],
            "county": request.POST["county"],
            "postcode": request.POST["postcode"],
            "country": request.POST["country"],
            "email_address": request.POST["email_address"],
            "phone_number": request.POST["phone_number"],
        }

        # fill OrderForm with submitted form data
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            # save the order form to create an order
            order = order_form.save()

            # find the current user's account
            account = request.user.useraccount

            # declare a dict to store the order drawings
            order_drawings = {}

            # iterate through cart items to construct order_drawings dict
            for item in cart:
                # if the current item's drawing is not already in the
                # order_drawings dict, add it
                if item["drawing"] not in order_drawings.keys():
                    # if autosave is selected
                    if item["drawing"] == "0":
                        # add placeholder
                        order_drawings[item["drawing"]] = "drawing_0"
                    else:
                        # get user's saved drawing for selected save_slot
                        drawing = Drawing.objects.filter(
                            user_account=account,
                            save_slot=item["drawing"],
                        ).first()

                        # create an OrderDrawing
                        order_drawing = OrderDrawing(
                            order=order,
                            save_slot=int(item["drawing"]),
                        )

                        # set the order drawing's image field to a copy of the
                        # image in the selected save_slot
                        order_drawing.image = File(drawing.image)
                        order_drawing.save()

                        # add order drawing to order_drawings dict
                        order_drawings[item["drawing"]] = order_drawing

            # iterate through items in user's cart
            for item in cart:
                try:
                    # for each item in the cart, add an OrderItem to the Order
                    product_variant = ProductVariant.objects.get(
                        id=item["variant_id"]
                    )
                    order_item = OrderItem(
                        order=order,
                        product_variant=product_variant,
                        # use order_drawings dict to enter selected drawing
                        order_drawing=order_drawings[item["drawing"]],
                        quantity=item["quantity"],
                    )
                    order_item.save()
                except ProductVariant.DoesNotExist:
                    # return an error if the submitted ProductVariant id is
                    # invalid
                    messages.error(
                        request,
                        (
                            "Product not found. Please try again or contact us"
                            " for assistance."
                        ),
                    )
                    # delete the order and return the user to the cart view
                    order.delete()
                    return redirect(reverse("view_cart"))

            # get the status of the save_details checkbox and save in session
            request.session["save_details"] = "save-details" in request.POST

            # send success message and redirect user
            messages.success(
                request,
                (
                    "Thank you! Your order has been placed."
                ),
            )
            return redirect(
                reverse("order_confirmed", args=[order.order_number])
            )
        else:
            # send error message if form is invalid
            messages.error(
                request,
                (
                    "There was a problem with your form. Please check your "
                    "details and try again."
                ),
            )

    else:
        # if cart is empty, redirect user to the prints page
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect(reverse("show_all_prints"))

        # get the current shopping cart contents
        current_cart = cart_contents(request)

        # get grand_total from current cart and convert from str to decimal
        total = Decimal(current_cart["grand_total"])

        # set stripe payment total and secret key
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

        # create stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    # show error message if stripe public key missing
    if not stripe_public_key:
        messages.error(request, "Stripe Public Key missing.")

    template = "orders/checkout.html"

    context = {
        "order_form": order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
    }

    return render(request, template, context)


def order_confirmed(request, order_number):
    """
    A view to display order confirmation and details to user
    """
    save_details = request.session.get("save_details")
    order = get_object_or_404(Order, order_number=order_number)

    # if the user is logged in
    if request.user.is_authenticated:
        # find the logged in user's account and attach it to the order
        account = UserAccount.objects.get(user=request.user)
        order.user_account = account
        order.save()

        # if the user selected to save their details
        if save_details:
            # save their address with the DefaultAddressForm
            address_data = {
                "default_address_1": order.address_1,
                "default_address_2": order.address_2,
                "default_town": order.town,
                "default_county": order.county,
                "default_postcode": order.postcode,
                "default_country": order.country,
            }
            user_address_form = DefaultAddressForm(
                address_data, instance=account
            )

            if user_address_form.is_valid():
                user_address_form.save()

            # and save their name with the NameUpdateForm
            name_data = {
                "first_name": order.first_name,
                "last_name": order.last_name,
            }
            user_name_form = NameUpdateForm(name_data, instance=account)

            if user_name_form.is_valid():
                user_name_form.save()

    # if the user's session contains a shopping cart, delete it
    if "cart" in request.session:
        del request.session["cart"]

    template = "orders/order_confirmed.html"
    context = {
        "order": order,
    }

    return render(request, template, context)
