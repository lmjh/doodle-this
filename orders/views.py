from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    # get the user's cart from the session
    cart = request.session.get("cart", [])

    # if cart is empty, redirect user to the prints page
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect(reverse('show_all_prints'))

    order_form = OrderForm()

    template = 'orders/checkout.html'

    context = {
        'order_form': order_form,
        'stripe_public_key': "pk_test_51KwoRQEwpXeQoUfQZvs2fLxxCsrLBUVKEU8ZCeddw395W5nPf4jM88LsfskM07e7VMBcN32WgTsYzJ9OawneFhXD002cDbQyQo",
        'client_secret': 'test_client_secret'
    }

    return render(request, template, context)
