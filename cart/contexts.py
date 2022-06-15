from django.conf import settings


def cart_contents(request):
    """
    Handles user shopping cart contents data
    """

    # instantiate variables for items in cart, count of items and total costs
    cart_items = []
    items_total = 0
    cart_count = 0
    delivery = settings.STANDARD_DELIVERY_FEE

    grand_total = items_total + delivery

    # pass variables to context
    context = {
        'cart_items': cart_items,
        'items_total': items_total,
        'cart_count': cart_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
