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
        'order_form': order_form
    }

    return render(request, template, context)
