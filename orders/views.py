from decimal import Decimal
import stripe

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderDrawing, OrderItem
from prints.models import ProductVariant
from accounts.models import Drawing
from cart.contexts import cart_contents


def checkout(request):
    # get stripe public and secret keys from environment
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # get the user's cart from the session
    cart = request.session.get("cart", [])

    if request.method == 'POST':
        # gather form data from request
        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'address_1': request.POST['address_1'],
            'address_2': request.POST['address_2'],
            'town': request.POST['town'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
            'email_address': request.POST['email_address'],
            'phone_number': request.POST['phone_number'],
        }

        # fill OrderForm with submitted form data
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            # save the order form to create an order
            order = order_form.save()

            # find the current user's account
            account = request.user.useraccount

            # find the user's saved drawing
            saved_drawing_1 = Drawing.objects.filter(
                user_account=account,
                save_slot=1,
                ).first()

            # create an order drawing with the saved drawing
            order_save_slot_1 = OrderDrawing(
                order=order,
                save_slot=1,
                image=saved_drawing_1.image
            )

            # save the order drawing
            order_save_slot_1.save()

            # iterate through items in user's cart
            for item in cart:
                try:
                    # for each item in the cart, add an OrderItem to the Order
                    product_variant = ProductVariant.objects.get(id=item['variant_id'])
                    order_item = OrderItem(
                        order=order,
                        product_variant=product_variant,
                        order_drawing=order_save_slot_1,
                        quantity=item['quantity']
                    )
                    order_item.save()
                except ProductVariant.DoesNotExist:
                    # return an error if the submitted ProductVariant id is
                    # invalid
                    messages.error(request, (
                        "Product not found. Please try again or contact us for"
                        " assistance."
                        )
                    )
                    # delete the order and return the user to the cart view
                    order.delete()
                    return redirect(reverse('view_cart'))

            # get the status of the save_details checkbox and save in session
            request.session['save_details'] = 'save-details' in request.POST

            # send success message and redirect user
            messages.success(request, "Order added!")
            return redirect(reverse('sketchbook'))
        else:
            # send error message if form is invalid
            messages.error(request, (
                "There was a problem with your form. Please check your details"
                " and try again."
                )
            )

    else:
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

        order_form = OrderForm()

    # show error message if stripe public key missing
    if not stripe_public_key:
        messages.error(request, 'Stripe Public Key missing.')

    template = 'orders/checkout.html'

    print(cart)

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
