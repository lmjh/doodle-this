import time
import json

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.files import File
from orders.models import Order, OrderDrawing, OrderItem
from prints.models import ProductVariant
from accounts.models import UserAccount, Drawing


class StripeWebhookHandler:
    """
    Handles webhooks from Stripe
    """

    def __init__(self, request):
        self.request = request

    def generic_event_handler(self, event):
        """
        Handles all webhook events that don't have another handler
        """
        # return an http response with the type of the event and a 200
        # status code
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200
        )

    def payment_intent_succeeded_handler(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        # get intent object from event
        intent = event.data.object
        # get pid, cart and save_details data from intent
        pid = intent.id
        cart = intent.metadata.cart
        save_details = intent.metadata.save_details

        # get username from intent
        username = intent.metadata.username

        # get billing and shipping details from intent
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        # divide charge by 100 and round to 2 decimal places to get grand_total
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # replace empty strings in shipping details with None
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # create variable to record if order is present in the database
        order_exists = False
        # create variable to track attempts to find the order
        attempt = 1

        # split shipping details name to find first and last names
        split_name = shipping_details.name.split()
        # attempt five times to find the order
        while attempt <= 5:
            try:
                # try to find an order exactly matching details in the intent
                order = Order.objects.get(
                    first_name__iexact=split_name[0],
                    last_name__iexact=split_name[1],
                    email_address__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town__iexact=shipping_details.address.city,
                    address_1__iexact=shipping_details.address.line1,
                    address_2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    shopping_cart=cart,
                    stripe_pid=pid,
                )
                # if order is found, set order_exists to true and break
                order_exists = True
                break

            # if order is not found, increment the attempts counter and wait
            # for one second
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            # if the order is found, return an http response
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]}. '
                    "Successfully verified order exists in database"
                ),
                status=200,
            )
        else:
            # if the order is not found, try to create the order
            order = None
            try:
                order = Order.objects.create(
                    first_name=split_name[0],
                    last_name=split_name[1],
                    email_address=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=billing_details.address.postal_code,
                    town=shipping_details.address.city,
                    address_1=shipping_details.address.line1,
                    address_2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    grand_total=grand_total,
                    shopping_cart=cart,
                    stripe_pid=pid,
                )

                # find the current user's account
                user = User.objects.get(username=username)
                account = UserAccount.objects.get(user=user)

                # declare a dict to store the order drawings
                order_drawings = {}

                # iterate through cart items to construct order_drawings dict
                for item in json.loads(cart):
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

                            # set the order drawing's image field to a copy of
                            # the image in the selected save_slot
                            order_drawing.image = File(drawing.image)
                            order_drawing.save()

                            # add order drawing to order_drawings dict
                            order_drawings[item["drawing"]] = order_drawing

                # iterate through items in user's cart
                for item in json.loads(cart):
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

            except Exception as e:
                # if an error occurs, delete the order and return the error
                if order:
                    order.delete()
                return HttpResponse(
                    content=(
                        f'Webhook received: {event["type"]}. '
                        "An error was encountered: {e}"
                    ),
                    status=500,
                )

        # return success http response if order created
        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]}. '
                "Successfully created order."
            ),
            status=200,
        )

    def payment_intent_failed_handler(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200
        )
