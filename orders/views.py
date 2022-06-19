from decimal import Decimal
import stripe

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from cart.contexts import cart_contents


def checkout(request):
    # get stripe public and secret keys from environment
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # get the user's cart from the session
    cart = request.session.get("cart", [])

    # if cart is empty, redirect user to the prints page
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect(reverse('show_all_prints'))

    # get the current shopping cart contents
    current_cart = cart_contents(request)

    # get the grand_total from the current cart and convert from str to decimal
    total = Decimal(current_cart['grand_total'])

    # set stripe payment total and secret key
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key

    # create stripe payment intent
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    # show error message if stripe public key missing
    if not stripe_public_key:
        messages.error(request, 'Stripe Public Key missing.')

    order_form = OrderForm()

    template = 'orders/checkout.html'

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
